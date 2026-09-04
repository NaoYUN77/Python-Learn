"""tiny_mod —— 本章的小白鼠模块。

它唯一的使命就是被 import:
- 顶层那行 print 用来演示「import 会执行模块的顶层代码」
- PI / double / triple 是这个模块的「内容」
- 底部的 __name__ 守卫演示「直接跑」和「被导入」的差别(见 02_name_main.py)
"""

print("tiny_mod 顶层代码执行了!——import 我的人都会看到这一行")

PI = 3.14159


def double(x):
    return x * 2


def triple(x):
    return x * 3


if __name__ == "__main__":
    # 只有直接运行才进来:python ch09/tiny_mod.py
    # 被 import 时 __name__ 是 "tiny_mod",不等于 "__main__",这块不执行
    print(f"直接运行:__name__ == {__name__!r}")
    print(f"double(21) = {double(21)}")
    print(f"triple(7)  = {triple(7)}")
