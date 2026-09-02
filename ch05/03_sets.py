"""03_sets.py — 集合：去重、成员测试、数学运算。

运行：python ch05/03_sets.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets
"""

# 1. 创建：大括号；字面量里的重复自动消失
basket = {"苹果", "橙子", "苹果", "梨", "橙子"}
print(basket)                      # {'苹果', '橙子', '梨'}（顺序不保证）

# ⚠️ 空集合必须写 set()，{} 是空字典！
empty_set = set()
empty_dict = {}
print(type(empty_set).__name__)    # set
print(type(empty_dict).__name__)   # dict

# 2. 从序列建集合 = 去重
letters = set("hello")
print(letters)                     # {'h', 'e', 'l', 'o'}
print(list(set([1, 2, 2, 3, 3])))  # 去重后再转回列表

# 3. 成员测试：集合比列表快得多（尤其数据量大时）
print("苹果" in basket)            # True
seen = set()                       # 经典模式：用集合记录"见过的东西"
for word in ["a", "b", "a", "c"]:
    if word not in seen:
        seen.add(word)
print(seen)                        # {'a', 'b', 'c'}

# 4. 数学运算：交并差
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)                       # 并 {1, 2, 3, 4, 5}
print(a & b)                       # 交 {3}
print(a - b)                       # 差 {1, 2}（a 有 b 没有）
print(a ^ b)                       # 对称差 {1, 2, 4, 5}（只在一边的）

# 5. 增删
s = {1, 2}
s.add(3)
s.discard(99)                      # 删不存在的也不报错
s.remove(2)                        # 删不存在的会 KeyError
print(s)                           # {1, 3}

# 6. 无序 → 没有下标
# s[0]                             # ❌ TypeError: 'set' object is not subscriptable
for x in {10, 20}:                 # 但可以遍历（顺序不保证）
    print(x)
