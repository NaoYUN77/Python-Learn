"""test_exercises.py — boost 加练自动检查。

运行(项目根目录):python -m boost.extras_ch10.test_exercises
"""

from . import exercises

import random


def test_count_words():
    r = exercises.count_words("py go py go go")
    assert r == {"py": 2, "go": 3}, f"应为 {{'py': 2, 'go': 3}},实际 {r!r}"
    r = exercises.count_words("")
    assert r == {}, f"空串应得空字典,实际 {r!r}"
    assert type(r).__name__ == "dict", "应返回普通 dict(记得 dict() 转换)"


def test_locate():
    r = exercises.locate([(0, 0)], {(0, 0): "起点"})
    assert r == ["起点"], f"应得 ['起点'],实际 {r!r}"
    r = exercises.locate([(9, 9), (0, 0)], {(0, 0): "起点"})
    assert r == ["未知地", "起点"], (
        f"查不到的应得 '未知地' 且保持顺序,实际 {r!r}(提示:place_map.get(p, '未知地'))"
    )


def test_hyphen_join():
    r = exercises.hyphen_join(["2026", "09", "04"])
    assert r == "2026-09-04", f"应为 '2026-09-04',实际 {r!r}"
    r = exercises.hyphen_join(["单"])
    assert r == "单", f"单元素缝合不该出现缝线,实际 {r!r}"


def test_split_trim():
    r = exercises.split_trim("py, go ,cat")
    assert r == ["py", "go", "cat"], f"应去掉碎片两端空白,实际 {r!r}"
    r = exercises.split_trim("a,b")
    assert r == ["a", "b"], f"无空格的原样保留,实际 {r!r}"


def test_by_score():
    r = exercises.by_score([("甲", 88), ("乙", 95), ("丙", 72)])
    assert r == [("乙", 95), ("甲", 88), ("丙", 72)], (
        f"应按分数从大到小,实际 {r!r}(key=lambda + reverse=True)"
    )


def test_same_roll():
    r = exercises.same_roll(42)
    assert isinstance(r, list) and len(r) == 2, f"应返回 [第一次, 第二次],实际 {r!r}"
    assert r[0] == r[1], f"同一种子两次必须相等,实际 {r!r}"
    assert all(1 <= x <= 6 for x in r[0]), f"每颗都应在 1~6(两端都含),实际 {r[0]}"
    # 彩蛋:换种子重跑,剧本换了 → 结果(几乎肯定)不同
    other = exercises.same_roll(7)
    if other[0] == r[0]:
        print("    (小概率:种子 7 和 42 前三步撞了,无视这行)")


def test_probe_same_key():
    d = exercises.probe_same_key()
    assert d == {1: "c"}, f"1/1.0/True 是同一个键,应只剩 {{1: 'c'}},实际 {d!r}"
    assert len(d) == 1, f"应只有 1 个键,实际 {len(d)} 个"


def test_verify_dice():
    r = exercises.verify_dice(42, 10)
    assert r is True, f"三关全过应返回 True,实际 {r!r}"
    # 故意拆关:如果学员漏了某条 assert,这里补一个外部核验
    random.seed(42)
    first = [random.randint(1, 6) for _ in range(10)]
    random.seed(42)
    again = [random.randint(1, 6) for _ in range(10)]
    assert first == again, "这是测试自己的自检,不该炸"


def run_all():
    tests = [
        test_count_words,
        test_locate,
        test_hyphen_join,
        test_split_trim,
        test_by_score,
        test_same_roll,
        test_probe_same_key,
        test_verify_dice,
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
