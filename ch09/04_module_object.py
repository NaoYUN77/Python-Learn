"""04 模块也是对象:翻开 sys.modules 记账本。

运行:python ch09/04_module_object.py

README 9.1 说 import = 找到 → 执行 → 记账。这一集把"记账本"翻开,
亲眼看:模块是对象、账上有谁、撕掉一页账会发生什么。
"""

import sys
import math           # 各章老朋友——import 完它就在账上了
import json           # ch06 老朋友,同理
import tiny_mod       # 第一次:执行顶层(会看到那行 print)→ 记账

# 1. 模块就是个对象——有类型、有名字、有属性
print(f"type(tiny_mod)      = {type(tiny_mod)}")          # <class 'module'>
print(f"tiny_mod.__name__   = {tiny_mod.__name__!r}")     # 'tiny_mod'

# 2. sys.modules = 总记账本:本会话 import 过的模块全在账上
print(f"'tiny_mod' 在账上?  = {'tiny_mod' in sys.modules}")   # True
print(f"'math' 在账上?      = {'math' in sys.modules}")       # True
print(f"'json' 在账上?      = {'json' in sys.modules}")       # True

# 3. 两次 import 拿到同一个对象(所以第二次不会重新执行)
import tiny_mod as tm
print(f"tiny_mod is tm      = {tiny_mod is tm}")   # True:同一对象,两个名字

# 4. 模块的命名空间就是一个 dict:__dict__ 里装着它顶层的所有名字
keys = [k for k in tiny_mod.__dict__ if not k.startswith("__")]
print(f"tiny_mod 的公开内容 = {keys}")              # ['PI', 'double', 'triple']

# 5. 极慢镜头验证:撕掉一页账,再 import 会怎样?
#    (平时别这么干!这里纯粹为了验证"记账"机制)
print("--- 撕账:del sys.modules['tiny_mod'] ---")
del sys.modules["tiny_mod"]    # 账上抹掉 tiny_mod
import tiny_mod                # 查账发现没有 → 重新执行整个文件!
print(f"重演后 tiny_mod is tm  = {tiny_mod is tm}")   # False:新账新对象!

# 预期输出(注意顶层 print 出现两次——第一次正常 import,第二次撕账重演)
# tiny_mod 顶层代码执行了!——import 我的人都会看到这一行
# type(tiny_mod)      = <class 'module'>
# tiny_mod.__name__   = 'tiny_mod'
# 'tiny_mod' 在账上?  = True
# 'math' 在账上?      = True
# 'json' 在账上?      = True
# tiny_mod is tm      = True
# tiny_mod 的公开内容 = ['PI', 'double', 'triple']
# --- 撕账:del sys.modules['tiny_mod'] ---
# tiny_mod 顶层代码执行了!——import 我的人都会看到这一行
# 重演后 tiny_mod is tm  = False
