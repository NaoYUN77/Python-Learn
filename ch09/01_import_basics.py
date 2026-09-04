"""01 import 三姿势 + 记账缓存现象。

运行:python ch09/01_import_basics.py
盯一个现象:tiny_mod 的顶层 print 只出现一次——这就是"记账"。
"""

import sys

# ── 姿势一:整体搬。import 做三件事:找到 → 执行顶层 → sys.modules 记账 ──
import tiny_mod          # 第一次:真的执行 tiny_mod 顶层 → 会看到那行 print
import tiny_mod          # 第二次:查 sys.modules → 有账,直接绑名字,一行代码不跑!

print(f"tiny_mod.PI = {tiny_mod.PI}")        # 模块对象.名字 → 从它身上取属性
print(f"double(21)  = {tiny_mod.double(21)}")

# 两次 import 拿到的是同一个对象——第二次只是多了一个名字而已
import tiny_mod as tm
print(f"tiny_mod is tm → {tiny_mod is tm}")   # True:同一个模块对象,两个名字

# ── 姿势二:点名搬一件。产物是名字本身,不带前缀直接用 ──
from tiny_mod import triple

print(f"triple(7)   = {triple(7)}")

# 拼错名字当场炸(取消注释试试):报错在说"那个模块的命名空间里没这个名字"
# from tiny_mod import tripl   # ImportError: cannot import name 'tripl'

# ── 姿势三:整体搬+改名。名字太长或约定缩写时用(此处 tm 已在上面用过) ──
print(f"tm.double(5) = {tm.double(5)}")

# ── 标准库一模一样的玩法 ──
import math

print(f"math.sqrt(25) = {math.sqrt(25)}")

# ── 偷看两样东西:模块的内容 & 解释器的总记账本 ──
public_names = [n for n in dir(tiny_mod) if not n.startswith("_")]
print(f"tiny_mod 的公开名字: {public_names}")
print(f"'tiny_mod' 在 sys.modules 里? {'tiny_mod' in sys.modules}")   # True
print(f"'math' 在 sys.modules 里?   {'math' in sys.modules}")         # True

# 预期输出(盯住:顶层 print 只出现一次!)
# tiny_mod 顶层代码执行了!——import 我的人都会看到这一行
# tiny_mod.PI = 3.14159
# double(21)  = 42
# tiny_mod is tm → True
# triple(7)   = 21
# tm.double(5) = 10
# math.sqrt(25) = 5.0
# tiny_mod 的公开名字: ['PI', 'double', 'triple']
# 'tiny_mod' 在 sys.modules 里? True
# 'math' 在 sys.modules 里?   True
