"""test_exercises.py — 第十一章练习自动检查。

运行(在项目根目录执行):python -m ch11.test_exercises
如果你通过了全部测试,会在终端看到 "恭喜!全部通过 🎉"。

小知识:测试里所有 asyncio.run(...) 都是在替你"兑票"——
你的协程函数光调用不会执行,这是本章第一课。
"""

from . import exercises

import asyncio
import inspect
import time


def test_make_tea():
    assert inspect.iscoroutinefunction(exercises.make_tea), (
        "make_tea 必须用 async def 定义(协程函数)——只差一个关键词!"
    )
    coro = exercises.make_tea()
    try:
        assert type(coro).__name__ == "coroutine", (
            f"调用协程函数应该只得到协程对象(票,还没执行!),"
            f"实际得到 {type(coro).__name__}"
        )
    finally:
        coro.close()   # 测试讲卫生:废票要作废,否则运行结束蹦 RuntimeWarning
    r = asyncio.run(exercises.make_tea())
    assert r == "🍵 茶泡好了", f"await 兑票之后应拿到返回值 '🍵 茶泡好了',实际 {r!r}"


def test_nap():
    assert inspect.iscoroutinefunction(exercises.nap), "nap 必须是 async def 函数"
    t0 = time.perf_counter()
    r = asyncio.run(exercises.nap(0.05))
    elapsed = time.perf_counter() - t0
    assert r == "睡了 0.05 秒", f"应返回 '睡了 0.05 秒'(f-string 拼秒数),实际 {r!r}"
    assert elapsed >= 0.05, (
        f"说好睡 0.05 秒,实际只过了 {elapsed:.3f} 秒——sleep 没生效?"
    )


def test_boil_race():
    durations = [0.08, 0.08, 0.08]
    expected = ["壶1 的开水", "壶2 的开水", "壶3 的开水"]

    r = asyncio.run(exercises.boil_serial(durations))
    assert r == expected, f"排队版应返回 {expected},实际 {r!r}"

    r = asyncio.run(exercises.boil_gather(durations))
    assert r == expected, f"并发版应返回同样的列表 {expected},实际 {r!r}"

    # 边界:没壶可烧,返回 []
    assert asyncio.run(exercises.boil_serial([])) == [], "空列表应返回 [](边界!)"
    assert asyncio.run(exercises.boil_gather([])) == [], "空列表应返回 [](边界!)"

    # 计时对比:并发版要明显快于排队版
    t0 = time.perf_counter()
    asyncio.run(exercises.boil_serial(durations))
    serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    asyncio.run(exercises.boil_gather(durations))
    gather_t = time.perf_counter() - t0
    assert gather_t < serial - 0.08, (
        f"并发版({gather_t:.2f}s)应明显快于排队版({serial:.2f}s)——"
        "gather 是同时点火,总耗时≈最慢那壶(0.08s),不是三壶之和(0.24s)"
    )


def test_fetch_all():
    sites = [("慢站", 0.12), ("中站", 0.06), ("快站", 0.02)]
    t0 = time.perf_counter()
    r = asyncio.run(exercises.fetch_all(sites))
    elapsed = time.perf_counter() - t0
    assert r == ["慢站 下载完成", "中站 下载完成", "快站 下载完成"], (
        f"结果必须按【传入顺序】排列(先完成的快站不能插队!),实际 {r!r}"
    )
    assert elapsed < 0.19, (
        f"三站应该同时下载,总耗时≈最慢的 0.12s,你用了 {elapsed:.2f} 秒"
        "(是不是逐个 await 排队了?排队的话是总和 0.2s)"
    )


def test_cook_dinner():
    t0 = time.perf_counter()
    r = asyncio.run(exercises.cook_dinner())
    elapsed = time.perf_counter() - t0
    assert r == ("菜切好了", "汤炖好了"), (
        f"应返回 ('菜切好了', '汤炖好了'),实际 {r!r}"
    )
    assert elapsed < 0.24, (
        f"炖汤 0.2s + 切菜 0.05s = 0.25s,你用了 {elapsed:.2f} 秒——"
        "汤要用 create_task 提前点火,切菜填进等待里,总耗时应 ≈ 0.2s"
    )


def test_oven_exceptions():
    r = asyncio.run(exercises.check_oven(80))
    assert r == "80 度正常", f"80 度应正常,实际 {r!r}"
    r = asyncio.run(exercises.check_oven(100))
    assert r == "100 度正常", f"边界!100 度算正常(>100 才算太高),实际 {r!r}"
    raised = False
    try:
        asyncio.run(exercises.check_oven(120))
    except ValueError as e:
        raised = True
        assert "120" in str(e), f"报错信息里应带上温度 120,实际 {e!r}"
    assert raised, "120 度应 raise ValueError(大声失败,ch07),不能静默返回"

    r = asyncio.run(exercises.safe_check([80, 120, 100]))
    assert len(r) == 3, f"应返回 3 个结果(异常也算一个),实际 {r!r}"
    assert r[0] == "80 度正常", f"正常结果应原样收进列表,实际 {r[0]!r}"
    assert isinstance(r[1], ValueError), (
        f"炸掉的应收成 ValueError 对象,实际 {type(r[1]).__name__}"
        "(提示:gather 加 return_exceptions=True)"
    )
    assert r[2] == "100 度正常", f"边界值 100 度应正常,实际 {r[2]!r}"


def test_run_tools():
    tools = {"天气": 0.06, "计算": 0.02, "新闻": 0.1}
    t0 = time.perf_counter()
    r = asyncio.run(exercises.run_tools(tools))
    elapsed = time.perf_counter() - t0
    assert r == ["天气 查询完成", "计算 查询完成", "新闻 查询完成"], (
        f"应按传入顺序返回三个工具的结果,实际 {r!r}"
    )
    assert elapsed < 0.17, (
        f"工具应并发调用:总耗时≈最慢的新闻(0.1s),"
        f"你用了 {elapsed:.2f} 秒(三个工具排队的话是总和 0.18s)"
    )
    assert asyncio.run(exercises.run_tools({})) == [], "没有工具应返回 [](边界!)"


def run_all():
    tests = [
        test_make_tea,
        test_nap,
        test_boil_race,
        test_fetch_all,
        test_cook_dinner,
        test_oven_exceptions,
        test_run_tools,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
        except NotImplementedError:
            print(f"⏳ {test.__name__}: 还没完成")
        except Exception as e:
            print(f"❌ {test.__name__}: 出错 {type(e).__name__}: {e}")

    print(f"\n通过 {passed}/{len(tests)}")
    if passed == len(tests):
        print("恭喜!全部通过 🎉")
    else:
        print("继续加油,还没完成全部 😊")


if __name__ == "__main__":
    run_all()
