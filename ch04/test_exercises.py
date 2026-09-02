"""test_exercises.py — 第四章练习自动检查。

运行（在项目根目录执行）：python -m ch04.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。
"""

from . import exercises


def test_greet():
    result = exercises.greet("小明")
    assert result == "你好，小明！", f"默认问候应为 '你好，小明！'，实际得到 {result!r}"
    assert exercises.greet("小明", "早上好") == "早上好，小明！", "覆盖默认值时应返回 '早上好，小明！'"


def test_add_to():
    result = exercises.add_to(5, [1, 2])
    assert result == [1, 2, 5], f"[1,2] 加 5 应为 [1, 2, 5]，实际得到 {result}"
    first = exercises.add_to(5)
    assert first == [5], f"第一次调用应返回 [5]，实际得到 {first}"
    second = exercises.add_to(6)
    assert second == [6], f"第二次调用应返回 [6] 而不是被污染的列表，实际得到 {second}"


def test_divmod_pair():
    result = exercises.divmod_pair(17, 5)
    assert result == (3, 2), f"17 除 5 应为 (3, 2)，实际得到 {result}"
    assert isinstance(result, tuple), "返回值应是元组（多返回值自动打包）"
    q, r = exercises.divmod_pair(20, 4)     # 解包验证
    assert q == 5 and r == 0, "解包后商是 5、余数是 0"


def test_avg():
    result = exercises.avg(1, 2, 3)
    assert result == 2.0, f"avg(1,2,3) 应为 2.0，实际得到 {result}"
    assert isinstance(result, float), "返回值应是浮点数"
    assert exercises.avg() == 0, "空参数应返回 0 而不是崩溃"


def test_profile():
    result = exercises.profile(name="小明", age=18)
    assert result == "name: 小明, age: 18", f"实际得到 {result!r}"
    assert exercises.profile(name="小红", city="北京") == "name: 小红, city: 北京"


def test_sort_students():
    students = [("小明", 85), ("小红", 92), ("小刚", 78)]
    result = exercises.sort_students(students)
    expected = [("小红", 92), ("小明", 85), ("小刚", 78)]
    assert result == expected, f"应按分数降序 {expected}，实际得到 {result}"
    assert exercises.sort_students([]) == [], "空列表应返回空列表"


def test_apply():
    double = lambda x: x * 2
    assert exercises.apply(double, 3) == 6, "apply(double, 3) 应为 6"
    assert exercises.apply(lambda x: x + 1, 10) == 11, "apply(x+1, 10) 应为 11"


def test_make_counter():
    counter = exercises.make_counter()
    assert callable(counter), "make_counter() 应返回一个可调用的函数"
    assert counter() == 1, "第 1 次调用应为 1"
    assert counter() == 2, "第 2 次调用应为 2"
    assert counter() == 3, "第 3 次调用应为 3"
    other = exercises.make_counter()
    assert other() == 1, "两个计数器互不干扰，新计数器从 1 开始"


def test_wrap_call():
    def add(a, b, *, scale=1):
        return (a + b) * scale

    result = exercises.wrap_call(add, 3, 4, scale=10)
    assert result == 70, f"(3+4)*10 应为 70，实际得到 {result}"
    result2 = exercises.wrap_call(max, 1, 5, 3)
    assert result2 == 5, "转发位置参数应返回 5"


def run_all():
    tests = [
        test_greet,
        test_add_to,
        test_divmod_pair,
        test_avg,
        test_profile,
        test_sort_students,
        test_apply,
        test_make_counter,
        test_wrap_call,
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
        print("恭喜！全部通过 🎉")
    else:
        print("继续加油，还没完成全部 😊")


if __name__ == "__main__":
    run_all()
