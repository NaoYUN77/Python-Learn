"""05 — 超时 + 异常:异步世界的 ch07(README 11.6)

ch07 的异常知识全套直接复用:异常沿 await 链上传,照常按型号接。
新增两个并发时代的刚需:
  gather(return_exceptions=True) —— 异常当返回值收进列表,不连坐
  asyncio.timeout(秒)            —— 掐表,LLM 卡住时保命(Agent 刚需)

运行:python ch11/05_timeout_errors.py   (约 3 秒)

预期输出(时间戳为约值):
--- ① try/except 原样有效:按型号接 ---
[ 0.3s] 接住 ValueError:易炸站炸了!(ch07 的型号,一字没变)
--- ② gather 默认:一颗雷炸全船 ---
[ 0.6s] gather 整体炸了:2 号站炸了!(其他结果全拿不到了)
--- ③ return_exceptions=True:异常当返回值,不连坐 ---
[ 1.6s] 收齐:['1 号站 OK', ValueError('2 号站炸了!'), '3 号站 OK']
   ✅ 成功:1 号站 OK
   ❌ 失败:2 号站炸了!
   ✅ 成功:3 号站 OK
--- ④ 超时:asyncio.timeout 掐表 ---
[ 2.6s] 超时收工:TimeoutError!——卡住 5 秒的请求,1 秒就掐了
"""
import asyncio
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def fetch(site, seconds, boom=False):
    """模拟请求某个站点:boom=True 的站装了雷,睡完就炸"""
    await asyncio.sleep(seconds)
    if boom:
        raise ValueError(f"{site}炸了!")
    return f"{site} OK"


async def stuck_api():
    """模拟卡死的网络请求:5 秒都不返回"""
    await asyncio.sleep(5)


async def main():
    # ── ① try/except 原样有效:异常沿 await 链上传,照常按型号接 ──
    print("--- ① try/except 原样有效:按型号接 ---")
    try:
        await fetch("易炸站", 0.3, boom=True)
    except ValueError as e:
        print(f"{stamp()} 接住 ValueError:{e}(ch07 的型号,一字没变)")

    # ── ② gather 默认:一颗雷炸全船 ─────────────────────────
    print("--- ② gather 默认:一颗雷炸全船 ---")
    try:
        await asyncio.gather(
            fetch("1 号站", 1.0),
            fetch("2 号站", 0.3, boom=True),    # 0.3s 后它先炸
            fetch("3 号站", 1.0),
        )
    except ValueError as e:
        print(f"{stamp()} gather 整体炸了:{e}(其他结果全拿不到了)")

    # ── ③ return_exceptions=True:异常当返回值,不连坐 ───────
    print("--- ③ return_exceptions=True:异常当返回值,不连坐 ---")
    results = await asyncio.gather(
        fetch("1 号站", 1.0),
        fetch("2 号站", 0.3, boom=True),
        fetch("3 号站", 1.0),
        return_exceptions=True,          # 炸的收成异常对象,等全部干完才放行
    )
    print(f"{stamp()} 收齐:{results}")
    for r in results:                    # 逐个检查型号(ch07 的 isinstance 检查)
        if isinstance(r, Exception):
            print(f"   ❌ 失败:{r}")
        else:
            print(f"   ✅ 成功:{r}")

    # ── ④ 超时:asyncio.timeout 掐表(Python 3.11+)────────────
    print("--- ④ 超时:asyncio.timeout 掐表 ---")
    try:
        async with asyncio.timeout(1.0):         # 1 秒干不完就掐(3.10 及更早:
            await stuck_api()                    #   await asyncio.wait_for(stuck_api(), 1.0))
    except TimeoutError:
        print(f"{stamp()} 超时收工:TimeoutError!——卡住 5 秒的请求,1 秒就掐了")


if __name__ == "__main__":
    asyncio.run(main())
