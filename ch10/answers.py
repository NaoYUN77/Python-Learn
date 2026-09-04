"""answers.py — 第十章练习参考答案。

先自己做完 exercises.py,再对照这里。
"""

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from string import ascii_letters, digits
import random
import statistics


# 练习 1:三步一行流
def most_common_words(text, n):
    counts = Counter(text.split())
    return counts.most_common(n)


# 练习 2:缺键工厂接手收集模式
def group_by_first_letter(words):
    groups = defaultdict(list)
    for w in words:
        groups[w[0]].append(w)      # 缺键自动建空列表,append 就完了
    return dict(groups)             # 转回普通 dict


# 练习 3:randint 两端都含
def roll_dice(n):
    return [random.randint(1, 6) for _ in range(n)]


# 练习 4:glob 给 Path,要的是文件名
def py_files_in(folder):
    return sorted([p.name for p in Path(folder).glob("*.py")])


# 练习 5:date 相减得 timedelta
def days_between(y1, m1, d1, y2, m2, d2):
    return (date(y2, m2, d2) - date(y1, m1, d1)).days


# 练习 6:两个统计量,逗号打包成元组
def exam_stats(scores):
    return statistics.mean(scores), statistics.median(scores)


# 练习 7:材料库 + choice 抽签 + join 缝合
def gen_password(n):
    pool = ascii_letters + digits
    return "".join(random.choice(pool) for _ in range(n))


if __name__ == "__main__":
    print(most_common_words("py go py go go cat", 2))    # [('go', 3), ('py', 2)]
    print(group_by_first_letter(["apple", "banana", "avocado"]))
    # {'a': ['apple', 'avocado'], 'b': ['banana']}
    random.seed(42)
    print(roll_dice(3))                                  # 同一种子,输出确定
    print(py_files_in("."))                              # 当前目录的 .py 文件名
    print(days_between(2026, 1, 1, 2026, 2, 1))          # 31
    print(exam_stats([2, 4, 4, 10]))                     # (5.0, 4.0)
    random.seed(7)
    print(gen_password(8))                               # 某个 8 位密码(确定)
