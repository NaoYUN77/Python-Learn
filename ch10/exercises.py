"""exercises.py — 第十章练习(标准库漫游)。

请完成下面的每个函数,然后运行 python -m ch10.test_exercises 检查。

延续 ch09 的规矩:**import 也要你自己写**——
这份骨架里一行 import 都没有,请在 docstring 结束后、练习 1 之前
建一个 import 区,把每题需要的模块加进去(每题 TODO 会提示要什么)。

⚠️ 三条铁律(幽灵 import 七连之后):
   ① import 只写在顶部 import 区,不塞进函数里
   ② 用不到的 import 整行删——交卷前扫一遍
   ③ 补全弹窗塞进来的陌生名字,别顺手回车
"""

# 练习 1:热词榜
# TODO: 顶部 import 区加 from collections import Counter
# 返回 text 里出现次数最多的前 n 个词,格式 [(词, 次数), ...],次数从多到少
# most_common_words("py go py go go cat", 2) → [('go', 3), ('py', 2)]
def most_common_words(text, n):
    # 提示:split() 切词 → Counter 打包 → most_common(n) 收工(三步一行流)
    pass


# 练习 2:按首字母分组
# TODO: 顶部加 from collections import defaultdict
# 用 defaultdict(list) 把单词按首字母分组,返回普通 dict
# group_by_first_letter(["apple", "banana", "avocado"])
#   → {'a': ['apple', 'avocado'], 'b': ['banana']}
def group_by_first_letter(words):
    # 提示:ch05 收集模式 setdefault(k, []).append(x) 的省力版——
    # defaultdict(list) 先把"缺键自动建空列表"设成规矩,循环里只管 append;
    # 最后 dict(groups) 转回普通字典
    pass


# 练习 3:掷骰子
# TODO: 顶部加 import random
# 返回 n 次 randint(1, 6) 的结果列表
# roll_dice(3) → 例如 [4, 1, 6](每次不一样——测试用 seed 验证可复现)
def roll_dice(n):
    # 提示:推导式 + random.randint(1, 6);⚠️ randint 两端都含
    pass


# 练习 4:找 Python 文件
# TODO: 顶部加 from pathlib import Path
# 返回 folder 文件夹里所有 .py 文件的文件名列表,按字母排序
# py_files_in("某个文件夹") → ['a.py', 'b.py']
def py_files_in(folder):
    # 提示:Path(folder).glob("*.py") 逐个给出 Path 对象,
    # 取每个的 .name 拿到文件名,最后 sorted() 收尾
    pass


# 练习 5:隔了多少天
# TODO: 顶部加 from datetime import date
# 返回两个日期之间相隔的天数(后一个减前一个)
# days_between(2026, 1, 1, 2026, 2, 1) → 31
# days_between(2024, 2, 1, 2024, 3, 1) → 29(2024 是闰年!)
def days_between(y1, m1, d1, y2, m2, d2):
    # 提示:两个 date 对象相减得到 timedelta,它有 .days 属性(ch09 闰年题同款)
    pass


# 练习 6:考试成绩速览
# TODO: 顶部加 import statistics
# 返回 (平均分, 中位数) 组成的元组
# exam_stats([2, 4, 4, 10]) → (5.0, 4.0)
def exam_stats(scores):
    # 提示:statistics.mean / statistics.median 各算一个,
    # 逗号打包成元组 return(ch04:return a, b)
    pass


# 练习 7:随机密码生成器(综合挑战)
# TODO: 顶部加 import random 和 from string import ascii_letters, digits
# 返回一个长度为 n 的随机密码,字符只从大小写字母+数字里选
# gen_password(8) → 例如 'xQ3mK9pL'(每次不一样;测试查长度和字符范围)
def gen_password(n):
    # 提示:ascii_letters + digits 拼出"材料库"(一长串字符),
    # 推导式里 random.choice(材料库) 抽 n 次,"".join(...) 缝合成字符串
    pass
