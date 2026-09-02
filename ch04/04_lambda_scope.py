"""04_lambda_scope.py — lambda、作用域与闭包。

运行：python ch04/04_lambda_scope.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#lambda-expressions
"""

# 1. lambda：一行的小函数，冒号前是参数，后面是返回值表达式
double = lambda x: x * 2
print(double(5))                     # 10

# 等价的 def 写法（逻辑超过一行就老实用 def）
def double_def(x):
    return x * 2

# 2. lambda 最常见的岗位：当 sorted/max/min 的 key
students = [("小明", 85), ("小红", 92), ("小刚", 78)]
print(sorted(students, key=lambda p: p[1]))          # 按分数升序
print(sorted(students, key=lambda p: p[1], reverse=True))  # 降序
print(max(students, key=lambda p: p[1]))             # ('小红', 92) 分数最高的人
print(max("hello world", key=lambda ch: "hello world".count(ch)))  # 出现最多的字符 l

# 3. 作用域：函数内可以"读"外层变量
x = 10

def read_global():
    print(x)                         # ✅ 读没问题 → 10

read_global()

def try_change():
    # x = x + 1                     # ❌ UnboundLocalError：
    #                                #    只要函数内有对 x 的赋值，x 就成了局部变量
    y = x + 1                        # ✅ 只读不写没问题
    print(y)

try_change()                         # 11

# 4. 闭包：内层函数"记住"外层函数的参数
def make_multiplier(n):
    def multiply(x):
        return x * n                 # n 来自外层；make_multiplier 返回后它仍被记住
    return multiply

triple = make_multiplier(3)
print(triple(5))                     # 15
print(triple(10))                    # 30
double2 = make_multiplier(2)
print(double2(7))                    # 14（每个闭包记住自己的 n，互不干扰）

# 5. 类型标注：写给人和工具看的说明书（运行时不强制，Pylance 会查）
def repeat(text: str, times: int = 2) -> str:
    """把 text 重复 times 遍。"""
    return text * times

print(repeat("ab", 3))               # ababab
print(repeat.__annotations__)        # {'text': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
