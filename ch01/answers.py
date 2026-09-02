"""answers.py — 第一章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""


# 练习 1
def greet():
    print("欢迎学习 Python！")


# 练习 2
def add_numbers():
    return 15 + 27


# 练习 3
def divide_numbers():
    return 10 / 4


# 练习 4
def join_strings():
    return "Hello, " + "Python"


# 练习 5
def multiply_with_variable():
    total = 5 * 3
    return total


# 练习 6
def print_two_lines():
    print("第一行\n第二行")


if __name__ == "__main__":
    # 运行参考代码，看看效果
    greet()
    print(add_numbers())
    print(divide_numbers())
    print(join_strings())
    print(multiply_with_variable())
    print_two_lines()
    