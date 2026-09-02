"""03_type_conversion.py — 布尔值与类型转换。

运行：python ch02/03_type_conversion.py
参考官方文档：https://docs.python.org/zh-cn/3/library/stdtypes.html#truth-value-testing
"""

# 1. 布尔类型：只有 True 和 False（首字母大写）
print(3 > 2)     # True
print(3 == 3)    # True   相等是两个等号
print(3 != 4)    # True   不等号是 !=
print(type(True))  # <class 'bool'>

# 2. 逻辑运算：and / or / not
print(True and False)  # False  两个都真才真
print(True or False)   # True   有一个真就真
print(not True)        # False  取反

# 3. 布尔参与运算时相当于 1 和 0
print(True + True)  # 2

# 4. 真假值：Python 里任何数据都能当条件用
# 假的只有这些：0、0.0、""、[]、{}、None、False
print(bool(0))      # False
print(bool(42))     # True
print(bool(""))     # False
print(bool("hi"))   # True
print(bool(None))   # False

# 5. 类型转换：int() float() str()
print(int("42"))     # 42
print(int(3.9))      # 3    注意：截断小数，不是四舍五入
print(float("3.14")) # 3.14
print(str(42))       # '42'
print(type(str(42))) # <class 'str'>

# int("3.14")  # ❌ ValueError：字符串必须是纯整数才能转 int

# 6. 想把 "3.9" 转成整数 3？先转 float 再转 int
print(int(float("3.9")))  # 3

# 7. round() 四舍五入
print(round(3.7))      # 4
print(round(3.14159, 2))  # 3.14

# 8. type() 和 isinstance()
x = 100
print(type(x))               # <class 'int'>
print(isinstance(x, int))    # True
print(isinstance(x, str))    # False
