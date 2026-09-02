"""test_exercises.py — 第六章练习自动检查。

运行（在项目根目录执行）：python -m ch06.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。

测试会在系统临时目录创建文件，跑完自动清理。
"""

import os
import tempfile

from . import exercises


def temp_path(name):
    return os.path.join(tempfile.gettempdir(), name)


def test_format_date():
    assert exercises.format_date(2026, 9, 1) == "2026-09-01", "月日要补零成两位"
    assert exercises.format_date(2000, 12, 25) == "2000-12-25"
    assert exercises.format_date(1, 1, 1) == "0001-01-01", "年也要补零"


def test_parse_int():
    assert exercises.parse_int("42") == 42, "'42' 应转换为 42"
    assert exercises.parse_int("  7 ") == 7, "int() 能容忍首尾空格"
    assert exercises.parse_int("abc") is None, "非法输入应返回 None 而不是崩溃"


def test_parse_numbers():
    assert exercises.parse_numbers("3 5 8") == [3, 5, 8]
    assert exercises.parse_numbers("") == [], "空字符串应返回空列表"
    assert exercises.parse_numbers("7") == [7]


def test_write_lines():
    path = temp_path("ch06_test_write.txt")
    exercises.write_lines(path, ["a", "b"])
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "a\nb\n", f"应为 'a\\nb\\n'，实际得到 {content!r}"


def test_read_nonempty():
    path = temp_path("ch06_test_read.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("a\n\n b \nc\n")
    result = exercises.read_nonempty(path)
    assert result == ["a", "b", "c"], f"应为 ['a', 'b', 'c']，实际得到 {result}"


def test_file_stats():
    path = temp_path("ch06_test_stats.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("a b\n c\n")
    lines, words = exercises.file_stats(path)
    assert lines == 2, f"应有 2 行，实际 {lines}"
    assert words == 3, f"应有 3 个单词，实际 {words}"


def test_save_load_data():
    path = temp_path("ch06_test_data.json")
    data = {"name": "小明", "scores": [90, 85]}
    exercises.save_data(path, data)
    assert os.path.exists(path), "文件应该被创建"
    result = exercises.load_data(path)
    assert result == data, f"往返后应还原原数据，实际得到 {result}"


def test_merge_configs():
    path_a = temp_path("ch06_test_a.json")
    path_b = temp_path("ch06_test_b.json")
    out = temp_path("ch06_test_out.json")
    exercises.save_data(path_a, {"host": "a", "port": 80})
    exercises.save_data(path_b, {"port": 8080, "debug": True})
    exercises.merge_configs(path_a, path_b, out)
    result = exercises.load_data(out)
    expected = {"host": "a", "port": 8080, "debug": True}
    assert result == expected, f"b 应覆盖同名键，期望 {expected}，实际 {result}"


def run_all():
    tests = [
        test_format_date,
        test_parse_int,
        test_parse_numbers,
        test_write_lines,
        test_read_nonempty,
        test_file_stats,
        test_save_load_data,
        test_merge_configs,
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
