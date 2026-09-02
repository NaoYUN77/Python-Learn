"""01_lists.py — 列表方法：增删改查、栈、原地修改的坑。

运行：python ch05/01_lists.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists
"""

# 1. 增：append / insert / extend
fruits = ["橙子", "苹果", "梨"]
fruits.append("桃")                # 尾部加一个
print(fruits)                      # ['橙子', '苹果', '梨', '桃']

fruits.insert(0, "莓")             # 插到最前面，后面的往后挪
print(fruits)                      # ['莓', '橙子', '苹果', '梨', '桃']

fruits.extend(["杏", "枣"])        # 并进一堆（和 += 效果一样）
print(fruits)                      # [..., '杏', '枣']

# 2. 删：remove / pop / del / clear
fruits.remove("苹果")              # 按值删（只删第一个匹配；不存在则 ValueError）
popped = fruits.pop()              # 弹出末尾并返回
print(popped, fruits)              # 枣 ['莓', '橙子', '梨', '桃', '杏']

first = fruits.pop(0)              # 带下标 pop：弹出指定位置
print(first)                       # 莓

del fruits[0]                      # del 语句按位置删
print(fruits)                      # ['梨', '桃', '杏']

# 3. ⚠️ 原地方法返回 None 的坑
numbers = [3, 1, 2]
result = numbers.sort()            # 排序发生了，但返回值是 None
print(result)                      # None
print(numbers)                     # [1, 2, 3] ← 列表自己变了

numbers = [3, 1, 2]
new_list = sorted(numbers)         # 函数版：不改原列表，返回新列表
print(numbers, new_list)           # [3, 1, 2] [1, 2, 3]

# 4. 查：in / index / count / len
print("梨" in fruits)              # True（成员测试）
print(fruits.index("杏"))          # 2（第一次出现的位置）
print([1, 2, 2, 2].count(2))       # 3 出现次数
print(len(fruits))                 # 3

# 5. 栈：append + pop 天生一对（后进先出）
stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print(stack.pop(), stack.pop())    # 3 2 ← 后进先出

# 6. 队列：先进先出，用 collections.deque（列表头部操作慢，不合适）
from collections import deque
queue = deque(["a", "b"])
queue.append("c")
print(queue.popleft())             # a ← 最先来的最先走
print(list(queue))                 # ['b', 'c']
