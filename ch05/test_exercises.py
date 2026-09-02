"""test_exercises.py — 第五章练习自动检查。

运行（在项目根目录执行）：python -m ch05.test_exercises
如果你通过了全部测试，会在终端看到 "恭喜！全部通过 🎉"。
"""

from . import exercises


def test_unique_in_order():
    result = exercises.unique_in_order([3, 1, 3, 2, 1])
    assert result == [3, 1, 2], f"应为 [3, 1, 2]，实际得到 {result}"
    assert exercises.unique_in_order(["a", "b", "a"]) == ["a", "b"], "顺序要保持"
    assert exercises.unique_in_order([]) == [], "空列表应返回空列表"


def test_rotate_right():
    result = exercises.rotate_right([1, 2, 3, 4])
    assert result == [4, 1, 2, 3], f"应为 [4, 1, 2, 3]，实际得到 {result}"
    assert exercises.rotate_right(["a"]) == ["a"], "单元素不变"
    assert exercises.rotate_right([1, 2]) == [2, 1], "两元素互换"


def test_swap_ends():
    result = exercises.swap_ends((1, 2, 3, 4))
    assert result == (4, 2, 3, 1), f"应为 (4, 2, 3, 1)，实际得到 {result}"
    assert isinstance(result, tuple), "返回值应是元组"
    assert exercises.swap_ends((7, 8, 9)) == (9, 8, 7)


def test_common_and_only_a():
    common, only_a = exercises.common_and_only_a({1, 2, 3}, {3, 4, 5})
    assert common == {3}, f"交集应为 {{3}}，实际得到 {common}"
    assert only_a == {1, 2}, f"a-b 应为 {{1, 2}}，实际得到 {only_a}"
    assert isinstance(common, set) and isinstance(only_a, set), "两个返回值都应是集合"


def test_count_words():
    result = exercises.count_words("a b a c b a")
    assert result == {"a": 3, "b": 2, "c": 1}, f"实际得到 {result}"
    assert exercises.count_words("hello") == {"hello": 1}
    assert exercises.count_words("") == {}, "空字符串应返回空字典"


def test_get_grade():
    students = {"小明": 85, "小红": 92}
    assert exercises.get_grade(students, "小明") == 85, "小明的分数是 85"
    result = exercises.get_grade(students, "小刚")
    assert result == "未找到", f"不存在的键应返回 '未找到'，实际得到 {result!r}"


def test_squares_of_evens():
    result = exercises.squares_of_evens(10)
    assert result == [0, 4, 16, 36, 64], f"应为 [0, 4, 16, 36, 64]，实际得到 {result}"
    assert exercises.squares_of_evens(0) == [], "limit=0 应返回空列表"


def test_invert():
    result = exercises.invert({"a": 1, "b": 2})
    assert result == {1: "a", 2: "b"}, f"实际得到 {result}"
    assert exercises.invert({}) == {}, "空字典返回空字典"


def test_merge_scores():
    result = exercises.merge_scores(
        [("小明", 85), ("小红", 92)],
        [("小明", 90), ("小刚", 78)],
    )
    expected = {"小明": [85, 90], "小红": [92], "小刚": [78]}
    assert result == expected, f"应为 {expected}，实际得到 {result}"
    assert exercises.merge_scores([]) == {}, "没有成绩单应返回空字典"


def run_all():
    tests = [
        test_unique_in_order,
        test_rotate_right,
        test_swap_ends,
        test_common_and_only_a,
        test_count_words,
        test_get_grade,
        test_squares_of_evens,
        test_invert,
        test_merge_scores,
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
