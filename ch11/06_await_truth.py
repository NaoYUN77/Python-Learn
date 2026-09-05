"""06 — await 的真相:可能的暂停点,不是必然的暂停点(README 11.7)

await ≠ 必让位。await 只是"驱动执行",真正让位的时刻是:
链条深处有东西**真的在等**(一个还没完成的 Future 冒上来)。
如果被 await 的家伙从头到尾没有这样的操作——它一口气跑到底,
调度员全程靠边站,其他任务全被饿着。

运行:python ch11/06_await_truth.py   (约 3 秒,busy 耗时随机器而变)

预期输出(时间戳为约值,busy 的用时依机器而定):
--- ① await 链:main → middle → deep ---
[ 0.0s] middle:开跑(还没让位)
[ 0.0s] deep:开跑(还没让位)      ← 和 middle 同一瞬间!await 只是接力,不是暂停
[ 0.5s] deep:睡醒了               ← 全链唯一的真暂停点:deep 里的 asyncio.sleep
[ 0.5s] 拿到:deep 的结果(原路一层层传回)

--- ② await busy():一个从不让位的协程 ---
[ 0.5s] 心跳 💓
[ 0.6s] 心跳 💓
[ 0.7s] 心跳 💓
busy 跑完,用了 0.9 秒
↑ 这段时间心跳一声没吟——await 没让位,调度员被饿死 ❌
[ 1.7s] 心跳 💓
[ 1.8s] 心跳 💓
[ 1.9s] 心跳 💓
[ 2.0s] 心跳 💓
对照:await asyncio.sleep(0.35)——真等待的 Future 冒上来,别的任务才有机会 ✅
"""
import asyncio
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def deep():
    print(f"{stamp()} deep:开跑(还没让位)")
    await asyncio.sleep(0.5)          # ← 整条 await 链里唯一的"真闸口"
    print(f"{stamp()} deep:睡醒了")
    return "deep 的结果"


async def middle():
    print(f"{stamp()} middle:开跑(还没让位)")
    return await deep()               # ← 只是接力执行,自己不是暂停点


async def heartbeat():
    """每 0.1 秒跳一下——用来监视'调度员还活着吗'"""
    while True:
        print(f"{stamp()} 心跳 💓")
        await asyncio.sleep(0.1)


async def busy(n):
    """名义上的协程:里面一个 await 都没有——从不让位"""
    total = 0
    for i in range(n):                # 纯 CPU 循环,零让位操作
        total += i
    return total


async def main():
    # ── ① await 链:一根直通的管子,闸口只有深处的 sleep ──
    print("--- ① await 链:main → middle → deep ---")
    result = await middle()           # 看似在这暂停——其实直到 deep 的 sleep 才真挂起
    print(f"{stamp()} 拿到:{result}(原路一层层传回)\n")

    # ── ② 反面实锤:await 一个从不让位的协程 ──
    print("--- ② await busy():一个从不让位的协程 ---")
    hb = asyncio.create_task(heartbeat())   # 心跳排班(还没跑)
    await asyncio.sleep(0.25)               # 先让心跳跳两三下,证明调度员活着
    t0 = time.perf_counter()
    await busy(20_000_000)                  # ⚠️ 语法合法,但全程零让位!
    print(f"busy 跑完,用了 {time.perf_counter() - t0:.1f} 秒")
    print("↑ 这段时间心跳一声没吭——await 没让位,调度员被饿死 ❌")
    await asyncio.sleep(0.35)               # 对照:链条里有"真等待"的定时器
    print("对照:await asyncio.sleep(0.35)——真等待的 Future 冒上来,别的任务才有机会 ✅")
    hb.cancel()                             # 收摊:别让心跳跳个没完(11.6 的取消)


if __name__ == "__main__":
    asyncio.run(main())
