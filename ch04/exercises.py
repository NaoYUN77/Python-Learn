"""exercises.py — 第四章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目围绕官方教程 4.7-4.9 节（函数）：
默认参数、关键字参数、*args/**kwargs、lambda、作用域。
做完可以对照 answers.py 看参考代码。
"""


# 练习 1：带默认参数的问候
# greet("小明") → "你好，小明！"
# greet("小明", "早上好") → "早上好，小明！"
# 提示：def greet(name, greeting="你好")，注意 f-string 里中文逗号


def greet(name, greeting="你好"):
    # TODO: 一行 return，用 f-string 拼出 "问候语，名字！"
    return f'{greeting}，{name}！'


# 练习 2：安全版累加（可变默认值的坑）
# add_to(5, [1, 2]) → [1, 2, 5]
# add_to(5) → [5]（第一次调用）
# add_to(6) → [6]（第二次调用，绝不能变成 [5, 6]！）
# 提示：参数写成 items=None，函数体里 if items is None: items = []
def add_to(item, items=None):
    # TODO: 先处理 None，再 append，最后 return
    if items is None: 
        items = []
    items.append(item)
    return items


# 练习 3：多返回值
# 返回 (商, 余数) 组成的元组，divmod(17, 5""" """  """ """"""  """) → (3, 2)
# 提示：return a, b 一次返回两个；17 // 5 是商，17 % 5 是余数
def divmod_pair(a, b):
    # TODO: return 商, 余数
    return a // b, a % b


# 练习 4：*args 求平均
# avg(1, 2, 3) → 2.0；avg() → 0
# 注意返回浮点数；没有参数时返回 0（不要崩溃）
# 提示：*args 是元组，len(args) 判断空；sum(args) / len(args)
def avg(*args):
    # TODO: 空参数返回 0，否则返回平均值
    if len(args) == 0:
        return 0
    return float(sum(args) / len(args))


# 练习 5：**kwargs 生成个人简介
# profile(name="小明", age=18) → "name: 小明, age: 18"
# profile(name="小红", city="北京") → "name: 小红, city: 北京"
# 提示：kwargs 是字典，", ".join(f"{k}: {v}" for k, v in kwargs.items())
#
def profile(**kwargs):
    # TODO: 把字典拼成 "键: 值, 键: 值" 的字符串
    return ", ".join(f"{k}: {v}" for k, v in kwargs.items()) #不太明白


# 练习 6：lambda 当 key
# 返回按分数降序排列的列表，best_student(...) → ("小红", 92)
# 输入形如 [("小明", 85), ("小红", 92)]，返回完整列表
# 提示：sorted(students, key=lambda p: p[1], reverse=True)
def sort_students(students):
    # TODO: 一行 return sorted(...)
    return sorted(students,key=lambda p:p[1],reverse=True)


# 练习 7：函数当参数
# apply(f, 3) → f(3)；double = lambda x: x * 2 时 apply(double, 3) → 6
# apply(lambda x: x + 1, 10) → 11
# 提示：函数名也是值，直接 return f(x)
def apply(f, x):
    # TODO: 一行 return
    return f(x)
    


# 练习 8：计数器工厂（闭包）
# make_counter() 返回一个新函数：每调用一次返回值加 1
# counter = make_counter() 后 counter() → 1, counter() → 2
# 两个 counter 互不干扰
# 提示：外层定义 count = 0，内层函数 count += 1 后 return count（需要 nonlocal count）
def make_counter():
    # TODO: 定义 count = 0；定义内层函数（nonlocal count）做自增并返回；返回内层函数
    count = 0 
    def inner() :
        nonlocal count #?
        count += 1
        return count
    return inner


# 练习 9：参数转发（综合，选做但推荐）
# wrap_call(f, *args, **kwargs)：先打印 "call f.__name__"，再返回 f(*args, **kwargs) 的结果
# 提示：args/kwargs 原样转发，return f(*args, **kwargs)
def wrap_call(f, *args, **kwargs):
    # TODO: print 一句日志，然后转发参数并 return 结果
    print(f"call {f.__name__}")
    return f(*args, **kwargs)

def area(width, height):
    return width * height


print(wrap_call(area, 3, height=5))