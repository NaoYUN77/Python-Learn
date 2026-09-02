"""test_exercises.py — 第三章练习自动检查。

运行（在项目根目录执行）：python -m ch03.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。
"""

from . import exercises


def test_grade():
    assert exercises.grade(95) == "优秀", f"95 应为 '优秀'，实际得到 {exercises.grade(95)!r}"
    assert exercises.grade(85) == "良好", "85 应为 '良好'"
    assert exercises.grade(60) == "及格", "60 应为 '及格'"
    assert exercises.grade(59) == "不及格", "59 应为 '不及格'"


def test_fizzbuzz():
    assert exercises.fizzbuzz(15) == "FizzBuzz", "15 应同时被 3 和 5 整除"
    assert exercises.fizzbuzz(9) == "Fizz", "9 只被 3 整除"
    assert exercises.fizzbuzz(10) == "Buzz", "10 只被 5 整除"
    assert exercises.fizzbuzz(7) == "7", "7 应返回字符串 '7'"
    assert isinstance(exercises.fizzbuzz(7), str), "返回值必须是字符串"


def test_sum_even():
    result = exercises.sum_even(100)
    assert result == 2550, f"2+4+...+100 应为 2550，实际得到 {result}"
    assert exercises.sum_even(10) == 30, "2+4+6+8+10 应为 30"


def test_count_vowels():
    result = exercises.count_vowels("hello")
    assert result == 2, f"'hello' 有 2 个元音，实际得到 {result}"
    assert exercises.count_vowels("aeiou") == 5
    assert exercises.count_vowels("xyz") == 0


def test_find_first_divisor():
    assert exercises.find_first_divisor(15) == 3, "15 的最小因子是 3"
    assert exercises.find_first_divisor(7) is None, "7 是质数，应返回 None"
    assert exercises.find_first_divisor(2) is None, "2 是质数"
    assert exercises.find_first_divisor(9) == 3, "9 的最小因子是 3"


def test_guess_game():
    result = exercises.guess_game(42, [10, 50, 42])
    assert result == 3, f"第 3 次猜中，实际得到 {result}"
    assert exercises.guess_game(1, [1]) == 1, "第 1 次就猜中"


def test_countdown():
    result = exercises.countdown(5)
    assert result == [5, 4, 3, 2, 1], f"应为 [5, 4, 3, 2, 1]，实际得到 {result}"
    assert exercises.countdown(1) == [1], "countdown(1) 应为 [1]"


def test_dispatch():
    assert exercises.dispatch("start") == "启动"
    assert exercises.dispatch("stop") == "停止"
    assert exercises.dispatch("help") == "帮助"
    assert exercises.dispatch("h") == "帮助"
    assert exercises.dispatch("hack") == "未知命令"


def run_all():
    tests = [
        test_grade,
        test_fizzbuzz,
        test_sum_even,
        test_count_vowels,
        test_find_first_divisor,
        test_guess_game,
        test_countdown,
        test_dispatch,
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
