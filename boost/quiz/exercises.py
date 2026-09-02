"""exercises.py — 前五章复习测验（8/9/10 题实战版）。

把晨读总结里的三道概念题变成真代码题。
完成后在项目根目录运行：python -m boost.quiz.test_exercises
"""

# ══════════════════════════════════════════════════
# 题目 1（对应自测 8 题：原地方法返回 None 的坑）
# ══════════════════════════════════════════════════
# safe_sort(numbers) 返回【升序排列后的新列表】，且【不能修改传入的列表】
# safe_sort([3, 1, 2]) → [1, 2, 3]，同时调用方的 [3, 1, 2] 保持不变
#
# 提示：sort() 原地改但返回 None；sorted() 返回新列表不动原件。
#       想清楚用哪个（用错一个测试就会挂）


def safe_sort(numbers):
    # TODO: 一行 return
    return sorted(numbers)


# ══════════════════════════════════════════════════
# 题目 2（对应自测 9 题：两种 if 的区别）
# ══════════════════════════════════════════════════
# 2a. evens(limit)：返回 [0, limit) 中所有偶数组成的列表
#     evens(6) → [0, 2, 4]（元素数量比 limit 少——这是"门卫"型）
#
# 2b. labels(nums)：把列表里每个数变成 "偶"/"奇" 的字符串列表
#     labels([1, 2, 3]) → ["奇", "偶", "奇"]（数量不变——这是"加工厂"型）
#
# 提示：两题都是一行推导式。2a 的 if 在 for 后面（过滤）；
#       2b 是 "偶" if 条件 else "奇" 放在 for 前面（三元选择）


def evens(limit):
    # TODO: 一行推导式，if 在后
    return [x for x in range(limit) if x % 2 == 0 ]


def labels(nums):
    # TODO: 一行推导式，三元 if 在前
    return ['偶' if x % 2 == 0 else '奇' for x in nums]


# ══════════════════════════════════════════════════
# 题目 3（对应自测 10 题：字典计数模式）
# ══════════════════════════════════════════════════
# 3a. char_counts(text)：统计每个字符出现次数，返回字典
#     char_counts("aab") → {"a": 2, "b": 1}
#
# 3b. rare_chars(text, n)：返回出现次数【小于 n】的字符，按出现顺序排列的列表
#     rare_chars("abracadabra", 2) → ["c", "d"]（c 和 d 各只出现 1 次）
#     提示：r 和 a 各出现 2 次和 5 次，不小于 2，被过滤掉
#
# 提示：3a 用 counts[ch] = counts.get(ch, 0) + 1（空字典起步）
#       3b 先调用 3a 的函数拿到频次表，再用推导式筛 counts[ch] < n
#       （保持顺序、去重：遍历原字符串而不是频次表；用 seen 集合防重复）


def char_counts(text):
    # TODO: 空字典 + for 循环 + get 计数
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def rare_chars(text, n):
    # TODO: 先拿频次表，再按原顺序筛出 counts[ch] < n 且没收集过的字符
    count = char_counts(text)
    seen = set()
    result = []
    for ch in text:
        if count[ch] < n and ch not in seen:
            result.append(ch)
            seen.add(ch)
    return result