"""answers.py — 第九章参考答案。

先自己写,卡住超过十分钟再看这里!
重点看顶部的 import 区——本章全部知识点就是它。
"""

import math
import sys
import datetime as dt
from collections import Counter
from string import ascii_uppercase


def hypotenuse(a, b):
    return math.sqrt(a * a + b * b)


def letter_at(n):
    return ascii_uppercase[n]


def days_in_year(year):
    return (dt.date(year + 1, 1, 1) - dt.date(year, 1, 1)).days


def who_am_i():
    return __name__


def word_counts(words):
    return Counter(words)


def math_tools():
    return sorted(n for n in dir(math) if not n.startswith("_"))


def would_shadow(filename):
    if not filename.endswith(".py"):
        return False
    return filename[:-3] in sys.stdlib_module_names


if __name__ == "__main__":
    print("=== ch09 参考答案演示 ===")
    print(f"hypotenuse(3, 4)   = {hypotenuse(3, 4)}")          # 5.0
    print(f"letter_at(0)       = {letter_at(0)!r}")            # 'A'
    print(f"days_in_year(2024) = {days_in_year(2024)}")        # 366(闰年)
    print(f"days_in_year(2026) = {days_in_year(2026)}")        # 365(平年)
    print(f"who_am_i()         = {who_am_i()!r}")
    #   ↑ 直接跑是 '__main__',被 import 是 'ch09.answers'——两副面孔现场!
    print(f"word_counts         = {word_counts(['py', 'go', 'py'])}")
    tools = math_tools()
    print(f"math 公开名字共 {len(tools)} 个,前 5 个: {tools[:5]}")
    print(f"would_shadow('json.py')     = {would_shadow('json.py')}")        # True
    print(f"would_shadow('my_utils.py') = {would_shadow('my_utils.py')}")    # False
