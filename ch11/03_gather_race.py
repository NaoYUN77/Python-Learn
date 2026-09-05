"""03 — gather 并发实测:3 个任务 2 秒 vs 6 秒(README 11.4)

运行:python ch11/03_gather_race.py   (约 8 秒)

预期输出(时间戳为约值):
--- 上半场:顺序 await(排队,一张兑完再买下一张)---
[ 0.0s] 壶1:开烧…
[ 2.0s] 壶1:水开了!
[ 2.0s] 壶2:开烧…
[ 4.0s] 壶2:水开了!
[ 4.0s] 壶3:开烧…
[ 6.0s] 壶3:水开了!
顺序 await 总耗时:6.0 秒 —— 2+2+2,逐个等

--- 下半场:gather(三张票同一瞬间开工)---
[ 6.0s] 壶1:开烧…
[ 6.0s] 壶2:开烧…
[ 6.0s] 壶3:开烧…
[ 8.0s] 壶1:水开了!
[ 8.0s] 壶2:水开了!
[ 8.0s] 壶3:水开了!
gather 总耗时:2.0 秒 —— ≈ 最慢那壶,不是三壶之和
三壶的结果(按传入顺序,与完成先后无关):['壶1 的开水', '壶2 的开水', '壶3 的开水']
"""
import asyncio
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def boil(name, seconds):
    print(f"{stamp()} {name}:开烧…")
    await asyncio.sleep(seconds)     # 等水开:让位,别人可以插进来跑
    print(f"{stamp()} {name}:水开了!")
    return f"{name} 的开水"


async def main():
    # ── 上半场:顺序 await(排队)────────────────────────
    print("--- 上半场:顺序 await(排队,一张兑完再买下一张)---")
    t1 = time.perf_counter()
    results = []
    results.append(await boil("壶1", 2))     # 等壶1好了,壶2 才上灶
    results.append(await boil("壶2", 2))
    results.append(await boil("壶3", 2))
    print(f"顺序 await 总耗时:{time.perf_counter() - t1:.1f} 秒 —— 2+2+2,逐个等\n")

    # ── 下半场:gather(同时点火)────────────────────────
    print("--- 下半场:gather(三张票同一瞬间开工)---")
    t2 = time.perf_counter()
    results = await asyncio.gather(
        boil("壶1", 2),
        boil("壶2", 2),
        boil("壶3", 2),
    )
    print(f"gather 总耗时:{time.perf_counter() - t2:.1f} 秒 —— ≈ 最慢那壶,不是三壶之和")
    print(f"三壶的结果(按传入顺序,与完成先后无关):{results}")

    # README 11.4 那张跟踪表,你刚才亲眼看到的整理如下:
    print("""
跟踪表(整理自刚才的时间线):
| 时刻  | 调度员视角                                       |
|-------|--------------------------------------------------|
| t=0   | 三壶同时开烧 → 各自在 await 睡觉,全部让位       |
| t=0~2 | 没人能跑,调度员闲转(单线程也闲着)             |
| t=2   | 三壶同时水开,挨个醒来收结果                     |
| 收工  | gather 把三个返回值按【传入顺序】打包成列表      |""")


if __name__ == "__main__":
    asyncio.run(main())
