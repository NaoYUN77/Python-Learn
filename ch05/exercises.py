"""exercises.py — 第五章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目围绕官方教程第 5 章（数据结构）：
列表方法、元组解包、集合运算、字典、推导式。
做完可以对照 answers.py 看参考代码。
"""


# 练习 1：列表去重保序
# unique_in_order([3, 1, 3, 2, 1]) → [3, 1, 2]（保持第一次出现的顺序）
# 提示：set() 去重会丢顺序——遍历 + "见过的"集合，not in seen 才 append
import re


def unique_in_order(items):
    # TODO: 准备空列表 result 和空集合 seen；遍历，没见过的两边都记
    result = []
    seen = set()
    for item  in items:
        if item in seen:
            continue
        else: 
            result.append(item)
            seen.add(item)
    return result


# 练习 2：列表操作综合
# rotate_right([1, 2, 3, 4]) → [4, 1, 2, 3]（最后一个挪到最前）
# 提示：pop() 弹出末尾元素 + insert(0, x)；注意 pop 返回弹出的值
def rotate_right(items):
    # TODO: 先 pop 再 insert，返回原列表
    popv = items.pop()
    items.insert(0, popv)
    return items


# 练习 3：元组解包
# swap_ends((1, 2, 3, 4)) → (4, 2, 3, 1)（首尾互换）
# 提示：解包 first, *mid, last = t；用 (last, *mid, first) 拼回去
def swap_ends(t):
    # TODO: 一行解包 + 一行拼回
    fist , *mid , last = t 
    return last , *mid , fist  #返回的是元组?


# 练习 4：集合运算
# common_and_only_a(a, b) 返回两个集合：第一个是交集，第二个是 a-b（a 有 b 没有）
# common_and_only_a({1,2,3}, {3,4,5}) → ({3}, {1, 2})
# 提示：交集 a & b，差集 a - b；return x, y 返回两个
def common_and_only_a(a, b):
    # TODO: 两行计算，return 交集, 差集
    return a & b , a - b


# 练习 5：字典计数
# count_words("a b a c b a") → {"a": 3, "b": 2, "c": 1}
# 提示：text.split() 按空格切开；counts.get(word, 0) + 1（见 04_dicts.py 第 4 段）
def count_words(text):
    # TODO: 空字典 + for word in text.split() + get 计数
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


# 练习 6：字典安全取值
# get_grade(students, "小明") → 分数；不存在 → "未找到"
# students 形如 {"小明": 85, "小红": 92}
# 提示：dict.get(键, 默认值) 一行搞定
def get_grade(students, name):
    # TODO: 一行 return
    return students.get(name, "未找到")


# 练习 7：列表推导式
# squares_of_evens(10) → [0, 4, 16, 36, 64]（10 以内偶数的平方）
# 提示：[x ** 2 for x in range(limit) if x % 2 == 0]
def squares_of_evens(limit):
    
    # TODO: 一行推导式（if 在 for 后面 = 过滤）
    return [x ** 2 for x in range(limit) if x % 2 == 0]


# 练习 8：字典推导式
# invert(d) 反转键值：{"a": 1, "b": 2} → {1: "a", 2: "b"}
# 提示：{v: k for k, v in d.items()}
def invert(d):
    # TODO: 一行字典推导式
    return {v:k for k , v in d.items()}


# 练习 9：合并成绩单（综合）
# merge_scores([("小明", 85), ("小红", 92)], [("小明", 90), ("小刚", 78)])
# → {"小明": [85, 90], "小红": [92], "小刚": [78]}
# 提示：结果字典的值是列表；d.setdefault(name, []).append(score) 
#       （setdefault：键存在返回原值，不存在先设为默认值再返回）
def merge_scores(*score_lists):
    # TODO: 双层循环（每份成绩单、每对名字分数）+ setdefault 追加
    d = {}
    for index in score_lists:
        for name , socere in index:
            d.setdefault(name,[]).append(socere)
    return d