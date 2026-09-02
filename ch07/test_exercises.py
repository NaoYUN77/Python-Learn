"""test_exercises.py — 第七章练习自动检查。

运行（在项目根目录执行）：python -m ch07.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。

测试会用系统临时目录的文件，跑完自动清理。
"""

import os
import tempfile

from . import exercises


def temp_path(name):
    return os.path.join(tempfile.gettempdir(), name)


def test_parse_int():
    assert exercises.parse_int("42") == 42, "'42' 应转换为 42"
    assert exercises.parse_int("abc") is None, "非法字符串应返回 None"
    assert exercises.parse_int(None) is None, (
        "None 输入也应返回 None（int(None) 抛 TypeError，不是 ValueError）"
    )


def test_get_port():
    assert exercises.get_port({"port": 8080}, 80) == 8080, "有键时应返回键值"
    assert exercises.get_port({}, 80) == 80, "无键时应返回 default"


def test_load_json():
    good = temp_path("ch07_good.json")
    with open(good, "w", encoding="utf-8") as f:
        f.write('{"name": "小明"}')
    assert exercises.load_json(good) == {"name": "小明"}, "合法文件应返回读出的对象"

    missing = temp_path("ch07_missing.json")
    assert exercises.load_json(missing) is None, "文件不存在应返回 None"

    bad = temp_path("ch07_bad.json")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("{坏的")
    assert exercises.load_json(bad) is None, "坏 json 应返回 None"


def test_set_score():
    assert exercises.set_score(0) == 0
    assert exercises.set_score(100) == 100
    for bad_score in (-1, 101):
        try:
            exercises.set_score(bad_score)
        except ValueError as e:
            assert str(e) == f"分数必须在 0~100: {bad_score}", (
                f"错误信息应为 '分数必须在 0~100: {bad_score}'，实际 {e!r}"
            )
        else:
            raise AssertionError(f"{bad_score} 应该抛 ValueError 却没有抛")


def test_safe_divide():
    result = exercises.safe_divide(10, 2)
    assert result == "try,else,finally", (
        f"能整除时应为 'try,else,finally'，实际得到 {result!r}"
    )
    result = exercises.safe_divide(1, 0)
    assert result == "try,except,finally", (
        f"除零时应为 'try,except,finally'，实际得到 {result!r}"
    )


def test_describe_error():
    assert exercises.describe_error(lambda: 1) == "ok", "不炸应返回 'ok'"
    assert exercises.describe_error(lambda: int("x")) == "value"
    assert exercises.describe_error(lambda: "a" + 1) == "type"
    assert exercises.describe_error(lambda: {}["k"]) == "key"

    def boom():
        raise ZeroDivisionError("别的错")
    try:
        exercises.describe_error(boom)
    except ZeroDivisionError:
        pass    # 其他异常被原样转发，测试算过
    else:
        raise AssertionError("其他异常应该被原样 raise 转发，却被吞了")


def test_write_log():
    path = temp_path("ch07_log.txt")
    result = exercises.write_log(path, "hello")
    assert result == "written", f"写成功应返回 'written'，实际 {result!r}"
    with open(path, encoding="utf-8") as f:
        assert f.read() == "hello", f"文件内容应为 'hello'"

    # 写到【目录】上触发 OSError（目录上 open 文件会失败）
    result = exercises.write_log(tempfile.gettempdir(), "x")
    assert result == "failed", f"open 失败应返回 'failed'，实际 {result!r}"


def test_load_config():
    good = temp_path("ch07_cfg.json")
    with open(good, "w", encoding="utf-8") as f:
        f.write('{"debug": true}')
    assert exercises.load_config(good) == {"debug": True}

    missing = temp_path("ch07_cfg_missing.json")
    try:
        exercises.load_config(missing)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("文件缺失时应抛 FileNotFoundError（转发）")

    bad = temp_path("ch07_cfg_bad.json")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("{坏的")
    try:
        exercises.load_config(bad)
    except ValueError as e:
        assert str(e) == "配置文件损坏", f"信息应为 '配置文件损坏'，实际 {e!r}"
        assert e.__cause__ is not None, "应该用 raise ... from 保留原始异常线索"
    else:
        raise AssertionError("坏 json 应抛 ValueError('配置文件损坏')")


def run_all():
    tests = [
        test_parse_int,
        test_get_port,
        test_load_json,
        test_set_score,
        test_safe_divide,
        test_describe_error,
        test_write_log,
        test_load_config,
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
