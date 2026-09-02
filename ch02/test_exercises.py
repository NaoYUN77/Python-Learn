"""test_exercises.py — 第二章练习自动检查。

运行（在项目根目录执行）：python -m ch02.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。
"""

from . import exercises


def test_minutes_and_seconds():
    result = exercises.minutes_and_seconds(125)
    assert result == (2, 5), f"125 秒应为 (2, 5)，实际得到 {result}"
    assert exercises.minutes_and_seconds(59) == (0, 59), "59 秒应为 (0, 59)"


def test_is_even():
    assert exercises.is_even(4) is True, "4 应为偶数"
    assert exercises.is_even(7) is False, "7 应为奇数"
    assert exercises.is_even(0) is True, "0 是偶数"


def test_celsius_to_fahrenheit():
    result = exercises.celsius_to_fahrenheit(100)
    assert result == 212.0, f"100°C 应为 212.0°F，实际得到 {result}"


def test_clean_text():
    result = exercises.clean_text("  Hello, World  ")
    assert result == "HELLO, WORLD", f"应为 'HELLO, WORLD'，实际得到 {result!r}"


def test_first_three():
    result = exercises.first_three("Python")
    assert result == "Pyt", f"应为 'Pyt'，实际得到 {result!r}"
    assert exercises.first_three("World") == "Wor", "要使用切片而不是写死字符"


def test_reformat_date():
    result = exercises.reformat_date("2026-09-01")
    assert result == "2026/09/01", f"应为 '2026/09/01'，实际得到 {result!r}"


def test_string_to_int():
    result = exercises.string_to_int("3.9")
    assert result == 3, f"应为 3，实际得到 {result}"
    assert isinstance(result, int), f"返回类型应为 int，实际是 {type(result).__name__}"


def test_format_price():
    result = exercises.format_price(1234.5)
    assert result == "总价: ¥1234.50", f"应为 '总价: ¥1234.50'，实际得到 {result!r}"


def run_all():
    tests = [
        test_minutes_and_seconds,
        test_is_even,
        test_celsius_to_fahrenheit,
        test_clean_text,
        test_first_three,
        test_reformat_date, 
        test_string_to_int,
        test_format_price,
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
