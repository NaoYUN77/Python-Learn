"""02 — 三件套 + 两个词:async def / await / asyncio.run(README 11.2)

本章地基里的两个词,先用 type() 亲眼验证一遍:
  协程函数(coroutine function):async def 定义的函数——调用它【不执行】,只发一张票
  协程对象(coroutine object):调用协程函数发出来的票——await 它才真正执行

运行:python ch11/02_async_basics.py    (约 1 秒)

预期输出(地址数字每次不同;RuntimeWarning 是 stderr,位置可能略有穿插):
--- 第 1 步:调用协程函数 = 只造票,不执行 ---
make_tea 本尊:<class 'function'>(是协程函数吗?True)
tea = make_tea() 造出来的:<class 'coroutine'>   ← 票!函数体一行都没跑
--- 第 2 步:await = 兑票,这才执行 ---
[ 0.0s] 泡茶中……
[ 0.1s] 🍵 茶泡好了!
await 兑票拿到的结果:🍵 茶泡好了
--- 第 3 步:光造票不兑票——当场抓获 ---
RuntimeWarning: coroutine 'make_tea' was never awaited
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
看到上面那行 RuntimeWarning 了吗?没兑现的票 = 没干的活儿(新手第一大坑)
"""
import asyncio
import inspect
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def make_tea():
    print(f"{stamp()} 泡茶中……")
    await asyncio.sleep(0.1)         # 泡茶要等:await 处可以暂停、让位
    print(f"{stamp()} 🍵 茶泡好了!")  # 醒来了:从暂停点继续往下跑
    return "🍵 茶泡好了"


async def main():
    # ── 第 1 步:调用协程函数 = 只造票,不执行 ──────────────────
    print("--- 第 1 步:调用协程函数 = 只造票,不执行 ---")
    print(f"make_tea 本尊:{type(make_tea)}", end="")
    print(f"(是协程函数吗?{inspect.iscoroutinefunction(make_tea)})")
    tea = make_tea()                 # ⚠️ 函数体一行没跑!只是发了一张票
    print(f"tea = make_tea() 造出来的:{type(tea)}   ← 票!类型就叫 coroutine")

    # ── 第 2 步:await = 兑票,这才执行 ─────────────────────────
    print("--- 第 2 步:await = 兑票,这才执行 ---")
    result = await tea               # await 三件事:①执行 ②等待时让位 ③取回返回值
    print(f"await 兑票拿到的结果:{result}")
    # result = await tea              # 再兑一次?RuntimeError: cannot reuse already
    #                                 # awaited coroutine——票是一次性的!
    #                                 # 要再跑,重新 make_tea() 造新票

    # ── 第 3 步:光造票不兑票——当场抓获 ─────────────────────────
    print("--- 第 3 步:光造票不兑票——当场抓获 ---")
    ticket = make_tea()              # 票造出来,没人兑
    del ticket                       # 转身就丢——垃圾回收当场抓包,RuntimeWarning 蹦出来
    print("看到上面那行 RuntimeWarning 了吗?"
          "没兑现的票 = 没干的活儿(新手第一大坑)")


if __name__ == "__main__":
    asyncio.run(main())              # 点火:同步世界 → 异步世界的唯一大门
