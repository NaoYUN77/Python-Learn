"""02_tuples.py — 元组：不可变、解包、和列表的分工。

运行：python ch05/02_tuples.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#tuples-and-sequences
"""

# 1. 基本面目：小括号、不可变
point = (3, 4)
print(point[0], point[1])          # 3 4（索引、切片、in、len 都能用）
print(len(point), 3 in point)      # 2 True

# point[0] = 5                     # ❌ TypeError: 'tuple' object does not support
#                                  #    item assignment —— 不可变！

# 2. ⚠️ 单元素必须有逗号
not_tuple = (42)                   # 这只是数字 42 加了括号
real_tuple = (42,)
print(type(not_tuple).__name__)    # int
print(type(real_tuple).__name__)   # tuple

# 3. 序列解包：ch04 的多返回值靠的就是它
x, y = point                       # 右边的元组拆给左边的变量
print(x, y)                        # 3 4

a, b = 1, 2
a, b = b, a                        # 经典应用：一行交换两个变量
print(a, b)                        # 2 1

first, *rest = [1, 2, 3, 4]        # 星号收尾：剩下的打包成列表
print(first, rest)                 # 1 [2, 3, 4]

# 4. 元组能做的"只读"操作
t = (1, 2, 2, 3, 2)
print(t.count(2))                  # 3（出现次数）
print(t.index(3))                  # 3（第一次出现的位置）
print(t[1:4])                      # (2, 2, 3)（切片得到新元组）

# 5. 为什么需要元组：能当字典的键、能进集合（列表不行）
locations = {(35.6, 139.7): "东京", (39.9, 116.4): "北京"}   # 坐标做键
print(locations[(39.9, 116.4)])    # 北京

# 6. 函数多返回值 = 自动打包成元组（回顾 ch04）
def min_max(numbers):
    return min(numbers), max(numbers)   # 其实返回了一个元组

low, high = min_max([3, 1, 4])
print(low, high)                   # 1 4

# 7. 怎么选：会增删改 → 列表；固定搭配的一组值 → 元组
weekdays = ("一", "二", "三", "四", "五", "六", "日")   # 固定 7 项，不会变
todo = ["买菜", "写代码"]                                # 会长会短，用列表
