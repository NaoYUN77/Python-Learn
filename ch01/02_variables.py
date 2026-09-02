"""02_variables.py — 变量与命名规则示例。

运行：python ch01/02_variables.py
"""

# 1. 给数据起个名字（变量）
name = "Alice"
age = 25
height = 1.68

print(name)     # Alice
print(age)      # 25
print(height)   # 1.68

# 2. 变量可以随时重新赋值
age = 26
print(age)      # 26

# 3. 变量可以参与运算
total = age + 5
print(total)    # 31

# 4. 一行给多个变量赋值（很常用的写法）
a, b = 10, 20
print(a, b)     # 10 20

# 5. 交换两个变量的值（Python 的快捷写法）
x, y = 1, 2
x, y = y, x       # 交换
print(x, y)       # 2 1

# 6. 用 type() 查看数据的类型
print(type(name))    # <class 'str'>    字符串
print(type(age))     # <class 'int'>    整数
print(type(height))  # <class 'float'>  浮点数

# 7. 查看所有 Python 关键字
import keyword
print(keyword.kwlist)
