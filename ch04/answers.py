"""answers.py — 第四章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""


# 练习 1
def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"


# 练习 2
def add_to(item, items=None):
    if items is None:               # None 占位，避开可变默认值的坑
        items = []
    items.append(item)
    return items


# 练习 3
def divmod_pair(a, b):
    return a // b, a % b            # 商和余数，逗号隔开一次返回


# 练习 4
def avg(*args):
    if not args:                    # 空元组返回 0，避免 ZeroDivisionError
        return 0
    return sum(args) / len(args)


# 练习 5
def profile(**kwargs):
    return ", ".join(f"{k}: {v}" for k, v in kwargs.items())


# 练习 6
def sort_students(students):
    return sorted(students, key=lambda p: p[1], reverse=True)


# 练习 7
def apply(f, x):
    return f(x)                     # 函数名也是值，可以当参数传


# 练习 8
def make_counter():
    count = 0

    def counter():
        nonlocal count              # 没有这行，count += 1 会报 UnboundLocalError
        count += 1
        return count

    return counter


# 练习 9
def wrap_call(f, *args, **kwargs):
    print(f"call {f.__name__}")
    return f(*args, **kwargs)       # 原样转发，一个不多一个不少


if __name__ == "__main__":
    # 运行参考代码，看看效果
    print(greet("小明"))
    print(greet("小明", "早上好"))
    print(add_to(5, [1, 2]), add_to(5), add_to(6))
    print(divmod_pair(17, 5))
    print(avg(1, 2, 3), avg())
    print(profile(name="小明", age=18))
    print(sort_students([("小明", 85), ("小红", 92), ("小刚", 78)]))
    print(apply(lambda x: x * 2, 3))
    c = make_counter()
    print(c(), c(), c())
    print(wrap_call(max, 1, 5, 3))
