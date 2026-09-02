"""test_exercises.py — 前五章复习测验：自动评分。

在项目根目录运行：python -m boost.quiz.test_exercises
满分 100，按测试点计分，最后给评级。
"""

from . import exercises


def test_safe_sort():
    original = [3, 1, 2]
    result = exercises.safe_sort(original)
    assert result == [1, 2, 3], f"应返回 [1, 2, 3]，实际得到 {result}"


def test_safe_sort_untouched():
    original = [3, 1, 2]
    exercises.safe_sort(original)
    assert original == [3, 1, 2], f"原列表不能被修改，实际变成了 {original}"


def test_safe_sort_not_none():
    result = exercises.safe_sort([3, 1, 2])
    assert result is not None, "返回了 None——是不是用了 numbers.sort()？sort 原地改返回 None，应该用 sorted()"


def test_evens():
    assert exercises.evens(6) == [0, 2, 4], f"evens(6) 应为 [0, 2, 4]，实际 {exercises.evens(6)}"
    assert exercises.evens(0) == [], "evens(0) 应为空列表"
    assert exercises.evens(7) == [0, 2, 4, 6], "evens(7) 应为 [0, 2, 4, 6]"


def test_labels():
    assert exercises.labels([1, 2, 3]) == ["奇", "偶", "奇"], f"实际 {exercises.labels([1, 2, 3])}"
    assert exercises.labels([]) == [], "空列表返回空列表"
    assert exercises.labels([0]) == ["偶"], "0 是偶数"


def test_char_counts():
    assert exercises.char_counts("aab") == {"a": 2, "b": 1}, f"实际 {exercises.char_counts('aab')}"
    assert exercises.char_counts("") == {}, "空字符串返回空字典"
    assert exercises.char_counts("xyz") == {"x": 1, "y": 1, "z": 1}


def test_rare_chars():
    assert exercises.rare_chars("abracadabra", 2) == ["c", "d"], \
        f"应为 ['c', 'd']（出现少于 2 次的），实际 {exercises.rare_chars('abracadabra', 2)}"
    assert exercises.rare_chars("abc", 1) == [], "每个字符都出现 1 次，没有 <1 的"
    assert exercises.rare_chars("aabb", 2) == [], "各出现 2 次，不小于 2"


# ───────────────────────── 评分系统 ─────────────────────────

# 每个测试点的分值（共 100 分）
POINTS = {
    "test_safe_sort": 20,            # 题目 1：排序正确
    "test_safe_sort_untouched": 15,  # 题目 1：不动原列表
    "test_safe_sort_not_none": 15,   # 题目 1：避开 sort 返回 None 的坑
    "test_evens": 15,                # 题目 2a：门卫 if
    "test_labels": 15,               # 题目 2b：三元 if
    "test_char_counts": 10,          # 题目 3a：计数模式
    "test_rare_chars": 10,           # 题目 3b：综合筛选
}

ORDER = [
    test_safe_sort,
    test_safe_sort_untouched,
    test_safe_sort_not_none,
    test_evens,
    test_labels,
    test_char_counts,
    test_rare_chars,
]


def run_all():
    total = 0
    failed = []
    for test in ORDER:
        try:
            test()
            print(f"✅ {test.__name__}  (+{POINTS[test.__name__]} 分)")
            total += POINTS[test.__name__]
        except AssertionError as e:
            print(f"❌ {test.__name__}  (0/{POINTS[test.__name__]} 分) — {e}")
            failed.append(test.__name__)
        except (NotImplementedError, TypeError, AttributeError) as e:
            print(f"⏳ {test.__name__}  (0/{POINTS[test.__name__]} 分) — 未完成或出错: {e}")
            failed.append(test.__name__)

    print("\n" + "=" * 50)
    print(f"总分：{total} / 100")
    if total == 100:
        print("🏆 满分！前五章的概念全部扎实，放心前进！")
    elif total >= 70:
        print("😊 不错！错的地方回 boost/review_ch01_05.py 复习对应章节")
    else:
        print("💪 概念还有漏洞，建议重读错题对应章节 + boost 专题文件")
    if failed:
        print(f"未通过：{', '.join(failed)}")


if __name__ == "__main__":
    run_all()
