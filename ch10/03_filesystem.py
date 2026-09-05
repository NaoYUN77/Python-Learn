"""03_filesystem.py — pathlib 实战:把路径当对象使。

运行:python ch10/03_filesystem.py
看点:__file__ 是解释器塞的模块级变量(和 __name__ 一家),
有它就永远知道"我自己在哪",不怕从哪个目录启动。
"""

import os
from pathlib import Path

# ── 我是谁,我在哪 ──
me = Path(__file__)
print(f"__file__              = {__file__}")
print(f"Path(__file__).name   = {me.name!r}")       # 03_filesystem.py
print(f"Path(__file__).stem   = {me.stem!r}")       # 03_filesystem
print(f"Path(__file__).suffix = {me.suffix!r}")     # .py
print(f"所在目录 me.parent.name = {me.parent.name!r}")   # 'ch10'

# ── 拆一个别人的路径 ──
p = Path("photos/2026/vacation.jpg")
print(f"\np = {p}")
print(f"p.name   = {p.name!r}   全名")
print(f"p.stem   = {p.stem!r}   去掉最后一个后缀")
print(f"p.suffix = {p.suffix!r}   只剩 点+后缀")
print(f"p.parent = {p.parent!r}")

# ── exists:问文件系统一句话 ──
print(f"\nPath('没有这个文件.txt').exists() = {Path('没有这个文件.txt').exists()}")
print(f"我自己存在吗?me.exists() = {me.exists()}")

# ── 目录扫描:os 给字符串,pathlib 给对象 ──
here = me.parent
print(f"\nsorted(os.listdir(here))[:4] = {sorted(os.listdir(here))[:4]}")
print("  ↑ os.listdir 给字符串列表;pathlib 的 glob 给 Path 对象:")
py_files = sorted(here.glob("*.py"))
print(f"\nhere 下的 .py 文件(共 {len(py_files)} 个):")
for f in py_files:
    print(f"  {f.name:<24} 主干 {f.stem!r:<24} 后缀 {f.suffix!r}")

# 预期输出(__file__ 那行是完整绝对路径,因机器而异;清单以实际为准):
# __file__              = E:\Code\python-learn\ch10\03_filesystem.py
# Path(__file__).name   = '03_filesystem.py'
# Path(__file__).stem   = '03_filesystem'
# Path(__file__).suffix = '.py'
# 所在目录 me.parent.name = 'ch10'
#
# p = photos/2026/vacation.jpg
# p.name   = 'vacation.jpg'   全名
# p.stem   = 'vacation'   去掉最后一个后缀
# p.suffix = '.jpg'   只剩 点+后缀
# p.parent = photos\2026
#
# Path('没有这个文件.txt').exists() = False
# 我自己存在吗?me.exists() = True
#
# sorted(os.listdir(here))[:4] = ['01_battery_check.py', '02_collections.py', ...]
#   ↑ os.listdir 给字符串列表;pathlib 的 glob 给 Path 对象:
#
# here 下的 .py 文件(共 12 个):
#   01_battery_check.py      主干 '01_battery_check'      后缀 '.py'
#   ...(其余同理)
