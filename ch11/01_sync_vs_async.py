"""01 — 同步 vs 异步:煮两壶水(README 11.1)

同一批积木(boil/pour 都是协程函数),两种拼法:
  排队逐个 await   = 同步节奏
  gather 同时点火  = 异步节奏
同步/异步的分界不在函数,在【调用方式】。

运行:python ch11/01_sync_vs_async.py    (全程约 8 秒,是"等"出来的,不是卡了)

预期输出(时间戳为约值):
[ 0.0s] 壶1:上灶烧水(要 2.0s)...
[ 2.0s] 壶1:水开了!
[ 2.0s] 壶1:倒水(要 0.5s)...
[ 2.5s] 壶2:上灶烧水(要 2.0s)...
[ 4.5s] 壶2:水开了!
[ 4.5s] 壶2:倒水(要 0.5s)...
【同步版】总耗时 5.0 秒 —— 等水开的 4 秒里,你一直干站着

[ 5.0s] 壶1:上灶烧水(要 2.0s)...
[ 5.0s] 壶2:上灶烧水(要 2.0s)...
[ 7.0s] 壶1:水开了!
[ 7.0s] 壶2:水开了!
[ 7.0s] 壶1:倒水(要 0.5s)...
[ 7.5s] 壶1:倒完了
[ 7.5s] 壶2:倒水(要 0.5s)...
[ 8.0s] 壶2:倒完了
【异步版】总耗时 3.0 秒 —— 两壶同时烧,等待被重叠了 ✅
"""
import asyncio
import time

START = time.perf_counter()          # 示例一启动就掐表
BOIL, POUR = 2.0, 0.5                # 演示尺度:烧水 2 秒,倒水 0.5 秒


def stamp():
    """距示例启动过了几秒——拼进输出就是一张时间线"""
    return f"[{time.perf_counter() - START:4.1f}s]"


async def boil(name):
    """烧一壶水:睡 BOIL 秒模拟'等水开',开了返回结果"""
    print(f"{stamp()} {name}:上灶烧水(要 {BOIL}s)...")
    await asyncio.sleep(BOIL)        # await 处让出控制权——异步版的并发空隙就在这
    print(f"{stamp()} {name}:水开了!")
    return f"{name} 的开水"


async def pour(name):
    """倒一壶水:双手只有一双,一壶要倒 POUR 秒"""
    print(f"{stamp()} {name}:倒水(要 {POUR}s)...")
    await asyncio.sleep(POUR)
    print(f"{stamp()} {name}:倒完了")


async def sync_style():
    """同步节奏:一行等完再下一行(逐个 await = 排队)"""
    await boil("壶1")                # 站在灶前,等壶1开
    await pour("壶1")                # 再倒壶1
    await boil("壶2")                # 壶2 这才上灶……
    await pour("壶2")


async def async_style():
    """异步节奏:两壶同时烧(gather 点火);倒水是真'干活',仍要一壶壶倒"""
    await asyncio.gather(boil("壶1"), boil("壶2"))   # 两张票同一瞬间开工
    await pour("壶1")                # 水都开了,挨个倒
    await pour("壶2")


async def main():
    # ── 上半场:同步版 ────────────────────────────────
    t1 = time.perf_counter()
    await sync_style()
    print(f"【同步版】总耗时 {time.perf_counter() - t1:.1f} 秒"
          f" —— 等水开的 {BOIL * 2:.0f} 秒里,你一直干站着\n")

    # ── 下半场:异步版 ────────────────────────────────
    t2 = time.perf_counter()
    await async_style()
    print(f"【异步版】总耗时 {time.perf_counter() - t2:.1f} 秒"
          f" —— 两壶同时烧,等待被重叠了 ✅")


if __name__ == "__main__":           # ch09 的守卫:演示只在自己直接跑时点火
    asyncio.run(main())              # 点火:整个示例共用同一次事件循环
