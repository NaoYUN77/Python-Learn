"""test_exercises.py — 第一章练习自动检查。

运行（在项目根目录执行）：python -m ch01.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。
"""

import io
import sys
import contextlib

from . import exercises


def capture_print(func):
    """运行一个函数并捕获它的 print 输出。"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = func() if func is not None else None
    return result, buf.getvalue()


def test_greet():
    _, output = capture_print(exercises.greet)
    assert "欢迎学习 Python" in output, f"应打印'欢迎学习 Python'，实际输出为：{output!r}"


def test_add_numbers():
    result = exercises.add_numbers()
    assert result == 42, f"15 + 27 应为 42，实际得到 {result}"


def test_divide_numbers():
    result = exercises.divide_numbers()
    assert result == 2.5, f"10 / 4 应为 2.5，实际得到 {result}"


def test_join_strings():
    result = exercises.join_strings()
    assert result == "Hello, Python", f"拼接结果应为 'Hello, Python'，实际得到 {result}"


def test_multiply_with_variable():
    result = exercises.multiply_with_variable()
    assert result == 15, f"5*3 应为 15，实际得到 {result}"


def test_print_two_lines():
    _, output = capture_print(exercises.print_two_lines)
    assert "第一行" in output and "第二行" in output, f"输出应包含两行，实际：{output!r}"
    assert "\n" in output, f"应使用换行符，实际：{output!r}"


def run_all():
    tests = [
        test_greet,
        test_add_numbers,
        test_divide_numbers,
        test_join_strings,
        test_multiply_with_variable,
        test_print_two_lines,
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
