"""01_numbers.py — 数字类型与算术运算符。

运行：python ch02/01_numbers.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/introduction.html#numbers
"""

# 1. Python 常用的两种数字类型：int（整数）和 float（浮点数）
a = 42
b = 3.14
print(type(a), type(b))   # <class 'int'> <class 'float'>

# 2. 基本运算
print(7 + 3)    # 10   加
print(7 - 3)    # 4    减
print(7 * 3)    # 21   乘
print(7 / 2)    # 3.5  除法（结果永远是 float）

# 3. 整除 // ：向下取整
print(7 // 2)   # 3
print(7.0 // 2) # 3.0（有 float 参与结果就是 float）
print(-7 // 2)  # -4   注意是向下取整，不是去掉小数

# 4. 取余 % ：返回余数（判断奇偶、循环取值常用）
print(7 % 2)    # 1  奇数
print(8 % 2)    # 0  偶数
print(10 % 3)   # 1

# 5. 幂运算 **
print(2 ** 10)  # 1024
print(9 ** 0.5) # 3.0  平方根

# 6. int 没有大小限制，不会溢出
print(2 ** 100) # 1267650600228229401496703205376

# 7. 优先级：先乘除后加减，括号最优先
print(2 + 3 * 4)   # 14
print((2 + 3) * 4) # 20

# 8. 复合赋值运算符
count = 10
count += 5   # 等价于 count = count + 5
print(count) # 15
count *= 2
print(count) # 30

# 9. 浮点精度陷阱（所有语言都有，不是 bug）
print(0.1 + 0.2)         # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False
print(round(0.1 + 0.2, 10) == 0.3)  # True  用 round 后再比较

# 10. int 和 float 混合运算，结果自动升级为 float
print(type(1 + 1))    # <class 'int'>
print(type(1 + 1.0))  # <class 'float'>
