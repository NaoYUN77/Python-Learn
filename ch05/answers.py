"""answers.py — 第五章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""


# 练习 1
def unique_in_order(items):
    result = []
    seen = set()                   # 集合查 in 快，列表保顺序，各干各的活
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# 练习 2
def rotate_right(items):
    last = items.pop()             # 弹出末尾，pop 返回弹出的值
    items.insert(0, last)          # 插到最前
    return items                   # 原地修改，返回同一个列表


# 练习 3
def swap_ends(t):
    first, *mid, last = t          # 星号收中间
    return (last, *mid, first)     # 星号摊开中间


# 练习 4
def common_and_only_a(a, b):
    return a & b, a - b            # 交集、差集


# 练习 5
def count_words(text):
    counts = {}
    for word in text.split():      # split() 默认按空白切
        counts[word] = counts.get(word, 0) + 1
    return counts


# 练习 6
def get_grade(students, name):
    return students.get(name, "未找到")


# 练习 7
def squares_of_evens(limit):
    return [x ** 2 for x in range(limit) if x % 2 == 0]


# 练习 8
def invert(d):
    return {v: k for k, v in d.items()}


# 练习 9
def merge_scores(*score_lists):
    merged = {}
    for score_list in score_lists:
        for name, score in score_list:
            merged.setdefault(name, []).append(score)   # 键不存在先设 []
    return merged


if __name__ == "__main__":
    # 运行参考代码，看看效果
    print(unique_in_order([3, 1, 3, 2, 1]))
    print(rotate_right([1, 2, 3, 4]))
    print(swap_ends((1, 2, 3, 4)))
    print(common_and_only_a({1, 2, 3}, {3, 4, 5}))
    print(count_words("a b a c b a"))
    print(get_grade({"小明": 85}, "小明"), get_grade({"小明": 85}, "小刚"))
    print(squares_of_evens(10))
    print(invert({"a": 1, "b": 2}))
    print(merge_scores([("小明", 85), ("小红", 92)], [("小明", 90), ("小刚", 78)]))
