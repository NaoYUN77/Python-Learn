"""03 包、sys.path、遮蔽陷阱、import 区卫生三查。

运行:python ch09/03_packages.py
"""

import sys

print("== 1. 包 = 装模块的文件夹 ==")
print("""
本项目就是一个现成的例子:

python-learn/              ← 项目根
├── ch09/                  ← 包(本章)
│   ├── exercises.py       ← 模块
│   ├── test_exercises.py  ← 模块
│   └── tiny_mod.py        ← 模块
├── boost/
│   └── quiz/              ← 包里还能套包
└── ...

你从 ch01 用到现在的第一行测试代码,其实一直在考本章:

    from . import exercises
    │     │ │
    │     │ └─ 拿什么:exercises 这个模块
    │     └─── 从哪拿:. = 当前包(ch09)
    └───────── 关键词:从...拿

为什么必须带点?——规则要求「显式相对导入」。
光写 import exercises 是「隐式相对导入」,Python 3 直接禁止,
这就是 test_exercises.py 第一行要写成 from . import exercises 的原因。

几个配套小知识:
  - 模块名 = 文件名去掉 .py:exercises.py 的模块名就是 "exercises"
  - 点可以叠加:from .. import x = 从上一级包拿(在 boost/quiz 里,.. 是 boost)
  - __init__.py:传统上包的标志文件;3.3+ 没有也能跑(namespace package),
    本项目全程没写——知道即可
""")

print("== 2. sys.path:import 的搜索顺序 ==")
print("import 第一步「找到」就按 sys.path 从上到下找。当前的前 3 个:")
for p in sys.path[:3]:
    print(f"  {p}")
print()
print("搜索规则:从上到下,第一个命中就用,不再往下看。")
print("第 1 个是脚本所在目录——所以 import tiny_mod 能找到同目录的文件。")
print("但这也是遮蔽陷阱的入口:如果你的文件叫 json.py,")
print("它排在标准库 json 前面——import json 拿到的是你的文件!")
print()

print("== 3. 遮蔽检查器:文件名会不会顶掉标准库 ==")


def shadow_risk(filename):
    """'json.py' → True(标准库有 json,重名=遮蔽);'my_utils.py' → False"""
    if not filename.endswith(".py"):
        return False
    return filename[:-3] in sys.stdlib_module_names   # 标准库全部模块名(3.10+)


for name in ["json.py", "random.py", "string.py", "my_utils.py"]:
    mark = "⚠️ 会遮蔽标准库!" if shadow_risk(name) else "✅ 安全"
    print(f"  {name:<14} {mark}")

print()
print("== 4. import 区卫生三查(幽灵六连,本章终结) ==")
print("""
交卷前,把文件顶部的 import 区扫一遍:
  ① 这行 import 用到了吗?没用的【整行删】——
     ch03 sqlite3 → ch04 winreg → ch06 calendar 半截 → ch06 asyncio
     → ch07 双幽灵 → ch08 boost 套娃。六连了,到此为止!
  ② 是编辑器自动补全弹窗塞进来的吗?警觉一点,别顺手回车。
  ③ 带顶层演示输出的模块(比如 tiny_mod)别随手 import——
     import 会执行它的顶层代码,ch08 的测试就是这么被刷屏的。
""")
