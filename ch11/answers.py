"""answers.py — 第十一章练习参考答案。

先自己做完 exercises.py,再对照这里。
演示:python -m ch11.answers(点火台里会并发调三个"工具"给你看)
"""
import asyncio


# 练习 1:只加一个词——async。调用返回协程对象(票),await 兑票才执行
async def make_tea():
    return "🍵 茶泡好了"


# 练习 2:await asyncio.sleep 让位;time.sleep 是站桩,协程里禁用
async def nap(seconds):
    await asyncio.sleep(seconds)
    return f"睡了 {seconds} 秒"


# 练习 3:积木相同,拼法不同——排队 vs 同时点火
async def boil(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} 的开水"


async def boil_serial(durations):
    results = []
    for i, d in enumerate(durations, start=1):      # ch05 的 enumerate:i 从 1 数起
        results.append(await boil(f"壶{i}", d))     # 等一壶好,下一壶才上灶
    return results


async def boil_gather(durations):
    tickets = [boil(f"壶{i}", d) for i, d in enumerate(durations, start=1)]
    return await asyncio.gather(*tickets)           # ch04 的 * 解包:一次交 N 张票


# 练习 4:顺序铁律——gather 的结果按传入顺序排,先完成的不能插队
async def fetch_all(sites):
    async def fetch(name, seconds):                 # 协程函数也能定义在函数里
        await asyncio.sleep(seconds)                # (ch04 闭包的地盘)
        return f"{name} 下载完成"

    return await asyncio.gather(*[fetch(name, s) for name, s in sites])


# 练习 5:create_task 提前点火——切菜的 0.05s 填进炖汤的 0.2s 里
async def stew():
    await asyncio.sleep(0.2)
    return "汤炖好了"


async def cook_dinner():
    soup_task = asyncio.create_task(stew())   # ① 点火!不 await,先走人
    await asyncio.sleep(0.05)                 # ② 自己去切菜(汤在炖)
    dish = "菜切好了"
    soup = await soup_task                    # ③ 回来收汤
    return (dish, soup)                       # 逗号打包成元组(ch04)


# 练习 6:>100 才炸(100 度是边界,算正常);return_exceptions 让异常不连坐
async def check_oven(temp):
    if temp > 100:
        raise ValueError(f"{temp} 度太高了!")
    await asyncio.sleep(0.02)
    return f"{temp} 度正常"


async def safe_check(temps):
    return await asyncio.gather(
        *[check_oven(t) for t in temps],
        return_exceptions=True,               # 炸的收成异常对象,一个不落
    )


# 练习 7:迷你 Agent——工具调用全是"睡一会儿再返回",gather 并发收齐
async def run_tools(tools):
    async def call(name, seconds):
        await asyncio.sleep(seconds)          # 真实场景:这里 await 的是网络请求
        return f"{name} 查询完成"

    return await asyncio.gather(*[call(n, s) for n, s in tools.items()])


if __name__ == "__main__":
    # 演示:并发调三个"工具",总耗时 ≈ 最慢的 0.1s,而不是总和 0.18s
    import time

    t0 = time.perf_counter()
    results = asyncio.run(run_tools({"天气": 0.06, "计算": 0.02, "新闻": 0.1}))
    print(f"工具结果(按传入顺序):{results}")
    print(f"总耗时 {time.perf_counter() - t0:.2f} 秒"
          f" —— ≈ 最慢的新闻(0.1s),不是总和 0.18s 🎉")
