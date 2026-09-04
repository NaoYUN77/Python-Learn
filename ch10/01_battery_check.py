"""01 工具带盘点 — 你早就在用标准库了。

运行:python ch10/01_battery_check.py
两个看点:
1. 用过的模块已有 6 个——标准库不是新知识,是老朋友集合
2. sys.modules 账本当场变厚——import 一个记一笔(ch09 9.1)
"""

import sys

print("=== 标准库工具带盘点 ===\n")

# ── 老朋友 6 个,报个到(每个都现场演示一手) ──
import math
import string
import datetime as dt
from collections import Counter
import json

print("[已经用过的 6 个]")
print(f"  json        ch06  json.dumps({{'py': 1}}) = {json.dumps({'py': 1})!r}")
print(f"  math        ch09  math.sqrt(25) = {math.sqrt(25)}")
print(f"  string      ch09  ascii_uppercase[:3] = {string.ascii_uppercase[:3]!r}")
days = (dt.date.today() - dt.date(2026, 1, 1)).days
print(f"  datetime    ch09  2026-01-01 到今天已过 {days} 天(date 相减)")
print(f"  collections ch09  Counter(['py', 'go', 'py']) = {Counter(['py', 'go', 'py'])}")
print(f"  sys         ch09  账本 sys.modules 现有 {len(sys.modules)} 个模块")
print("  (sys 自己也是标准库——它就是账本本尊)")

# ── 本章新装 6 块电池(先列货,后面示例逐个开箱) ──
print("\n[本章新装 6 个]")
print("  pathlib     路径当对象:.name/.stem/.suffix")
print("  random      随机:randint/choice/shuffle/sample + seed 可复现")
print("  statistics  统计:mean/median")
print("  re          正则:findall/search/sub")
print("  fnmatch     文件名通配:fnmatch('a.txt', '*.txt')")
print("  timeit      测速:别猜,要测")

# ── 演示专用:在代码中途 import,亲眼看着账本变厚 ──
# (练习里仍守规矩:import 全写顶部!)
before = len(sys.modules)
import random
import statistics
import re
from pathlib import Path
from fnmatch import fnmatch

after = len(sys.modules)
print("\n[sys.modules 记账本(ch09 9.1)]")
print(f"  搬 5 个新模块前:{before} 个")
print(f"  搬之后:{after} 个(+{after - before})")
print("  ↑ 数字因 Python 版本而异,重点是'变厚了'")
print(f"  'random' 在账本里?{'random' in sys.modules}")
print(f"  'os' 呢?{'os' in sys.modules} ← 解释器一启动就自己 import 好了!")
print(f"  演示一手 pathlib:{Path('a/b/c.txt').suffix!r} 和 fnmatch:{fnmatch('x.csv', '*.csv')}")

# 预期输出(数字每次启动/每版本会变,形状不变):
# === 标准库工具带盘点 ===
#
# [已经用过的 6 个]
#   json        ch06  json.dumps({'py': 1}) = '{"py": 1}'
#   math        ch09  math.sqrt(25) = 5.0
#   string      ch09  ascii_uppercase[:3] = 'ABC'
#   datetime    ch09  2026-01-01 到今天已过 246 天(date 相减)
#   collections ch09  Counter(['py', 'go', 'py']) = Counter({'py': 2, 'go': 1})
#   sys         ch09  账本 sys.modules 现有 100 个模块
#   (sys 自己也是标准库——它就是账本本尊)
#
# [本章新装 6 个]
#   pathlib     路径当对象:.name/.stem/.suffix
#   ...(六行清单)
#
# [sys.modules 记账本(ch09 9.1)]
#   搬 5 个新模块前:100 个
#   搬之后:103 个(+3)
#   ↑ 数字因 Python 版本而异,重点是'变厚了'
#   'random' 在账本里?True
#   'os' 呢?True ← 解释器一启动就自己 import 好了!
#   演示一手 pathlib:'.txt' 和 fnmatch:True
