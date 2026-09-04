"""test_exercises.py — 第九章练习自动检查。

运行(在项目根目录执行):python -m ch09.test_exercises
如果你通过了全部测试,会在终端看到 "恭喜!全部通过 🎉"。
"""

from . import exercises


def test_hypotenuse():
    r = exercises.hypotenuse(3, 4)
    assert r == 5.0, f"hypotenuse(3, 4) 应为 5.0,实际 {r!r}"
    r = exercises.hypotenuse(5, 12)
    assert r == 13.0, f"hypotenuse(5, 12) 应为 13.0,实际 {r!r}"


def test_letter_at():
    r = exercises.letter_at(0)
    assert r == "A", f"letter_at(0) 应为 'A',实际 {r!r}"
    r = exercises.letter_at(25)
    assert r == "Z", f"letter_at(25) 应为 'Z',实际 {r!r}"


def test_days_in_year():
    r = exercises.days_in_year(2026)
    assert r == 365, f"2026 是平年,应为 365 天,实际 {r!r}"
    r = exercises.days_in_year(2024)
    assert r == 366, f"2024 是闰年,应为 366 天,实际 {r!r}"


def test_who_am_i():
    r = exercises.who_am_i()
    assert r == "ch09.exercises", (
        f"被测试导入时,exercises 的 __name__ 应为 'ch09.exercises',实际 {r!r}"
        "(提示:直接 return __name__)"
    )


def test_word_counts():
    r = exercises.word_counts(["py", "go", "py"])
    assert r == {"py": 2, "go": 1}, f"应得 {{'py': 2, 'go': 1}},实际 {r!r}"
    assert type(r).__name__ == "Counter", (
        f"应该用标准库 Counter(它就是一种 dict),实际类型 {type(r).__name__}"
    )


def test_math_tools():
    r = exercises.math_tools()
    assert "sqrt" in r, "math 的公开名字里应有 'sqrt'"
    assert "pi" in r, "math 的公开名字里应有 'pi'"
    assert r == sorted(r), "结果应按字母排序(收尾用 sorted)"
    assert all(not n.startswith("_") for n in r), "不该有下划线开头的名字(内部货要筛掉)"


def test_would_shadow():
    assert exercises.would_shadow("json.py"), "'json.py' 会遮蔽标准库 json,应为 True"
    assert exercises.would_shadow("random.py"), "'random.py' 会遮蔽标准库 random,应为 True"
    assert not exercises.would_shadow("my_utils.py"), "'my_utils.py' 不在标准库,应为 False"
    assert not exercises.would_shadow("json"), "不是 .py 结尾谈不上遮蔽,应为 False"


def run_all():
    tests = [
        test_hypotenuse,
        test_letter_at,
        test_days_in_year,
        test_who_am_i,
        test_word_counts,
        test_math_tools,
        test_would_shadow,
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
