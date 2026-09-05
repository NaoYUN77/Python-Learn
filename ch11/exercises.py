"""exercises.py — 第十一章练习(同步与异步:asyncio 入门)。

请完成下面的每个函数,然后运行 python -m ch11.test_exercises 检查。

⚠️ 本章的函数全是 async def——【调用不会执行,只会发一张"票"】。
   测试会替你 asyncio.run / await 兑票;想自己跑着玩?
   文件最底部有"点火台"(整个文件唯一允许亲手 asyncio.run 的地方)。

延续 ch09/ch10 的规矩:**import 也要你自己写**——
这份骨架里一行 import 都没有,请在 docstring 结束后、练习 1 之前
建一个 import 区,把每题需要的模块加进去(每题 TODO 会提示要什么)。

⚠️ 铁律(幽灵 import 七连之后):
   ① import 只写在顶部 import 区,不塞进函数里
   ② 用不到的 import 整行删——交卷前扫一遍
   ③ 补全弹窗塞进来的陌生名字,别顺手回车
   ④ 协程里"睡觉"只用 await asyncio.sleep(...)——time.sleep 是站桩,
      会卡死整个调度员(11.3 第二大坑)!
"""

# ── import 区:把每题需要的模块加在这里(每题 TODO 会提示要什么)──
# TODO: import asyncio(练习 2 起就要用;练习 1 不用任何 import)
# (建好之前,下面的 boil/stew 会报"asyncio 未定义"——红波浪线就是在催你建 import 区)


# 练习 1:协程函数 vs 协程对象(这题不用 import!async def 是语法,不是模块)
# TODO: 把下面的 def 改成 async def(只加一个词!函数体一个字都不用动)
# 改完体会:make_tea() 这样【调用】它会发生什么?(不执行,只发一张票)
# 真正执行要 await 兑票——测试里会用 asyncio.run 替你兑
async def make_tea():
    return "🍵 茶泡好了"


# 练习 2:小睡一觉(await + asyncio.sleep)
# TODO: 在函数体里 await asyncio.sleep(seconds),醒来后返回 f"睡了 {seconds} 秒"
# ⚠️ 绝不能用 time.sleep——它不让位,整个调度员陪你站桩
async def nap(seconds):
    await asyncio.sleep(seconds)
    return f"睡了 {seconds} 秒"


# 练习 3:排队 vs 并发(烧水竞速)
# 下面这个 boil 是现成的积木(不许改);写两个"拼法":
# TODO: boil_serial(durations):逐个 await boil(f"壶{i}", d) 排队烧,
#       返回 ["壶1 的开水", "壶2 的开水", ...](i 从 1 数起,ch05 的 enumerate)
# TODO: boil_gather(durations):把所有票用 asyncio.gather 同时点火,
#       返回同样的列表(顺序也要一致)
async def boil(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} 的开水"


async def boil_serial(durations):
    results = []
    for i, duration in enumerate(durations, 1):
        results.append(await boil(f"壶{i}", duration))
    return results


async def boil_gather(durations):   
   task = [asyncio.create_task(boil(f"壶{i}", duration)) for i, duration in enumerate(durations, 1)]
   results = await asyncio.gather(*task)
   return results


# 练习 4:gather 的顺序铁律(结果按传入顺序,先完成的不能插队!)
# TODO: 对 sites 里每个 (站名, 秒数) 模拟下载:await asyncio.sleep(各自秒数),
#       返回 f"{站名} 下载完成";用 gather 一次全部并发,收齐后返回结果列表
# ⚠️ 测试故意把"快站"排在最后——先完成的也不许插队!
async def fetch_all(sites):
    tasks = [asyncio.create_task(fetch(site)) for site in sites]
    results = await asyncio.gather(*tasks)
    return results


# 练习 5:create_task 提前点火,把切菜填进炖汤的等待里
# 下面这个 stew 是现成的积木(不许改):
async def stew():
    await asyncio.sleep(0.2)
    return "汤炖好了"


# TODO: cook_dinner() 里按顺序做三件事:
#   ① soup_task = asyncio.create_task(stew())   ← 提前点火,不 await,先走人
#   ② await asyncio.sleep(0.05) 切菜,得到 "菜切好了"
#   ③ await soup_task 收汤
#   返回 ("菜切好了", "汤炖好了")
# ⚠️ create_task 只能在协程里调用(调度员得先上班!)
async def cook_dinner():
    pass


# 练习 6:异步里的异常(ch07 全套直接复用!)
# TODO: check_oven(temp):温度 > 100 就 raise ValueError(f"{temp} 度太高了!");
#       否则 await asyncio.sleep(0.02) 后返回 f"{temp} 度正常"
# ⚠️ 边界:100 度算正常!(== 100 的老账还挂着,ch07 的教训)
async def check_oven(temp):
    pass


# TODO: safe_check(temps):用 gather(..., return_exceptions=True) 批量检查,
#       正常的收字符串、炸的收异常对象,原样返回结果列表(一个不落)
async def safe_check(temps):
    pass


# 练习 7(综合挑战):迷你 Agent——并发调用三个工具(ch12 预演!)
# TODO: run_tools(tools) 的参数是 {工具名: 模拟耗时},如 {"天气": 0.06, "新闻": 0.1}
#       对每个工具:await asyncio.sleep(各自秒数) 模拟调用,
#       返回 f"{工具名} 查询完成";用 gather 一次全部并发,按传入顺序收齐
# 跑通后去下面"点火台"亲手 asyncio.run 一把,看看总耗时 ≈ 最慢那个,不是总和
async def run_tools(tools):
    pass


# ──────────────────────────────────────────────────────────────
# 🔥 点火台(可选):想亲眼看运行效果,在这里亲手 asyncio.run
#    只有直接运行本文件才会执行;被测试导入时 __name__ 是
#    "ch11.exercises",这块永远不跑(ch09 的身份证知识!)
if __name__ == "__main__":
    pass   # TODO(可选): asyncio.run(run_tools({"天气": 0.06, "计算": 0.02, "新闻": 0.1}))
