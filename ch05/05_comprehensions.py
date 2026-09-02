"""05_comprehensions.py — 推导式：一行制造列表/字典/集合。

运行：python ch05/05_comprehensions.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#list-comprehensions
"""

# 1. 列表推导式 = 循环 + append 的压缩写法
squares = []
for x in range(10):
    squares.append(x ** 2)         # 普通写法（3 行）

squares = [x ** 2 for x in range(10)]          # 推导式（1 行）
print(squares)                     # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 2. 读法：[表达式 for 变量 in 序列] —— 每个元素按模板加工
names = ["tom", "jerry", "spike"]
print([name.upper() for name in names])       # ['TOM', 'JERRY', 'SPIKE']
print([len(name) for name in names])          # [3, 5, 5]

# 3. 带 if 过滤：只要满足条件的
print([x for x in range(20) if x % 3 == 0])   # [0, 3, 6, 9, 12, 15, 18]
print([n for n in names if "r" in n])         # ['jerry', 'spike']

# 4. ⚠️ 两种 if 长得像，位置不同含义不同
# result = 0 
# for x in range(5) :
#   if x % 2 == 0 :
#       result += x ** 2
print([x ** 2 for x in range(5) if x % 2 == 0]) 
# if 在后 = 过滤器：[0, 4, 16]
print(["偶" if x % 2 == 0 else "奇" for x in range(5)]) # if 在前 = 三元选择：['偶','奇',...]


# 5. 字典推导式：{键表达式: 值表达式 for ...}
print({x: x ** 2 for x in range(4)})          # {0: 0, 1: 1, 2: 4, 3: 9}
word = "hello"
print({ch: word.count(ch) for ch in set(word)})  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# 6. 集合推导式：{表达式 for ...}
print({ch for ch in "hello world" if ch != " "})  # {'h', 'e', 'l', 'o', 'w', 'r', 'd'}

# 7. 生成器表达式：圆括号，不建中间列表，省内存
#    ch04 练习 5 的 join(f"..." for ...) 就是它！
total = sum(x ** 2 for x in range(1000))      # 不用先建 1000 个数的列表
print(total)                       # 332833500
joined = ", ".join(str(x) for x in [2, 4, 6])
print(joined)                      # 2, 4, 6

# 8. 什么时候别用推导式：逻辑复杂时，普通 for 更好读
matrix = [[1, 2, 3], [4, 5, 6]]
flat = [num for row in matrix for num in row]   # 嵌套推导式（能看懂即可）
print(flat)                        # [1, 2, 3, 4, 5, 6]
# 上面那行等价于：
flat2 = []
for row in matrix:
    for num in row:
        flat2.append(num)
print(flat2 == flat)               # True
