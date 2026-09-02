"""01_basics.py — 定义函数：参数、返回值、文档字符串。

运行：python ch04/01_basics.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions
"""

# 1. 最简单的函数：def + 冒号 + 缩进（和 if/for 同一套规则）
def greet(name):
    """向指定的人问好。"""          # 三引号字符串 = 文档字符串（docstring）
    print(f"你好，{name}！")

greet("小明")                       # 你好，小明！

# 2. return 把结果交还给调用方；没有 return 的函数返回 None
def add(a, b):
    return a + b

result = add(3, 4)
print(result)                       # 7
print(greet("小红"))                # 先打印 你好，小红！ 再打印 None（greet 没有 return）

# 3. return 可以一次返回多个值（实际打包成元组），用两个变量解包
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5])
print(low, high)                    # 1 5

# 4. 提前 return 当"守卫"：参数不合法就直接退出（呼应 ch03 的教训）
def safe_half(n):
    if n is None:
        return None                 # 结论性 return 放最前面
    return n / 2

print(safe_half(10))                # 5.0
print(safe_half(None))              # None

# 5. 函数名也是变量，可以赋给别人（为 lambda 做铺垫）
plus = add
print(plus(2, 3))                   # 5

# 6. help() 能显示函数签名和文档字符串
help(greet)                         # 打印 greet(name) 和 "向指定的人问好。"
