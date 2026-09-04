"""exercises.py — 第九章练习(模块与包)。

请完成下面的每个函数,然后运行 python -m ch09.test_exercises 检查。

本章规则和以前不一样:**import 也要你自己写**——
这份骨架里一行 import 都没有,请在 docstring 结束后、练习 1 之前
建一个 import 区,把每题需要的模块加进去(每题 TODO 会提示要什么)。

⚠️ 三条铁律(幽灵 import 六连的终结章):
   ① import 只写在顶部 import 区,不塞进函数里
   ② 用不到的 import 整行删——交卷前扫一遍
   ③ 补全弹窗塞进来的陌生名字,别顺手回车
"""

import math
from operator import countOf
from string import ascii_uppercase
import datetime as dt
from collections import Counter
import sys 
# 练习 1:斜边长度
# TODO: 顶部 import 区加 import math,用 math.sqrt 完成
# hypotenuse(3, 4) → 5.0
# hypotenuse(5, 12) → 13.0
def hypotenuse(a, b):
    # 提示:直角三角形 a² + b² = c²,开方用 math.sqrt(它返回 float,测试就要 5.0)
    return math.sqrt(a**2 + b**2)


# 练习 2:第 n 个大写字母
# TODO: 顶部加 from string import ascii_uppercase(姿势二:只搬一个名字)
# letter_at(0) → "A"
# letter_at(25) → "Z"
def letter_at(n):
    # 提示:ascii_uppercase 本身就是 "ABC...XYZ" 这个字符串,直接用下标取
    return ascii_uppercase[n]


# 练习 3:这一年的天数
# TODO: 顶部加 import datetime as dt(姿势三:起别名)
# days_in_year(2026) → 365
# days_in_year(2024) → 366
def days_in_year(year):
    # 提示:两个 date 相减得到 timedelta,它有 .days 属性
    # 次年 1 月 1 日 − 当年 1 月 1 日 = 一整年
    return (dt.date(year + 1, 1, 1) - dt.date(year, 1, 1)).days


# 练习 4:我是谁
# TODO: 这题不用 import!__name__ 天生就在每个模块里
# 被测试导入时,exercises 的 __name__ 是 "ch09.exercises"——见证模块的身份证
def who_am_i():
    # 提示:直接 return __name__(直接跑这个文件它会是 "__main__",两种身份都对)
    return __name__ 


# 练习 5:单词计数
# TODO: 顶部加 from collections import Counter
# word_counts(["py", "go", "py"]) → Counter({'py': 2, 'go': 1})
def word_counts(words):
    # 提示:ch05 的计数模式 counts.get(ch, 0) + 1,标准库一行就替你写完了
    # 直接 Counter(words) 返回即可(测试会检查类型确实是 Counter)
    return Counter(words)


# 练习 6:math 工具清单
# TODO: 顶部加 import math
# 返回 math 模块所有"公开"名字(不以下划线开头)的列表,按字母排序
# 结果里要有 "sqrt" 和 "pi"
def math_tools():
    # 提示:dir(math) 列出全部名字 → not n.startswith("_") 筛掉内部货 → sorted() 收尾
    return sorted([n for n in dir(math) if not n.startswith("_")])


# 练习 7:遮蔽检查器
# TODO: 顶部加 import sys
# 判断 filename 会不会顶掉标准库模块:
#   would_shadow("json.py") → True(标准库有 json,重名 = 遮蔽)
#   would_shadow("my_utils.py") → False
#   would_shadow("json") → False(不是 .py 文件,谈不上遮蔽)
def would_shadow(filename):
    # 提示:两步——① filename 以 ".py" 结尾 ② 去掉 ".py" 后的名字在
    # sys.stdlib_module_names 里(它是一个装着所有标准库模块名的集合,3.10+)
    return filename.endswith(".py") and filename[:-3] in sys.stdlib_module_names