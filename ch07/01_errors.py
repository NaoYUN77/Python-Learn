"""01_errors.py — 认识异常：语法错误 vs 运行时异常，常见信号型号。

运行：python ch07/01_errors.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/errors.html#syntax-errors
"""

# ══════════════════════════════════════════
# 第一部分：两种不同性质的错
# ══════════════════════════════════════════

# 1. 语法错误：解析阶段就拦下，一行都跑不了
#    （quiz 里 for 少冒号、from calendar import 半截，都是 SyntaxError）
#    取消下面的注释运行本文件试试：
# for ch in "abc"
#     pass
# → SyntaxError: expected ':'
# 注意：语法错误【不能】被 try/except 接住——代码根本没开始执行

# 2. 异常：语法没问题，运行到某行才炸
#    下面逐个演示七大高频信号（都包了 try，炸不崩程序）：

# 2.1 ValueError：值对不上（类型转换的经典款）
try:
    int("abc")
except ValueError as e:
    print("ValueError:", e)        # invalid literal for int() with base 10: 'abc'

# 2.2 TypeError：类型不支持这个操作
try:
    "a" + 1
except TypeError as e:
    print("TypeError:", e)         # can only concatenate str (not "int") to str
# quiz 里 for x in 6 也是 TypeError（int 不可迭代）——同一个家族

# 2.3 ZeroDivisionError：数学上不成立
try:
    1 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e) # division by zero

# 2.4 KeyError：字典键不存在
try:
    {"a": 1}["b"]
except KeyError as e:
    print("KeyError:", e)          # 'b' ← 注意打印出来带引号，这是键的 repr

# 2.5 IndexError：下标越界
try:
    [1, 2][5]
except IndexError as e:
    print("IndexError:", e)        # list index out of range

# 2.6 FileNotFoundError：文件不存在（ch06 模式表里预告过）
try:
    open("不存在的文件.txt", encoding="utf-8")
except FileNotFoundError as e:
    print("FileNotFoundError:", e.filename)   # 不存在的文件.txt
# e.filename 是异常对象自带的属性——异常对象不只有消息，还有专属字段

# 2.7 JSONDecodeError：坏 json 文本（本章新朋友）
import json
try:
    json.loads("{坏掉的")
except json.JSONDecodeError as e:
    print("JSONDecodeError:", e)   # Expecting property name enclosed in double quotes...
# 记住：它是 ValueError 的子类（03 讲继承树时用）


# ══════════════════════════════════════════
# 第二部分：异常对象 = 类型（型号）+ 消息（载荷）
# ══════════════════════════════════════════

# 3. 异常是被"抛出"的对象，可以接住后当数据用
def parse():
    raise ValueError("这里写人能看懂的说明")    # raise = 手动抛信号

try:
    parse()
except ValueError as e:             # as e：信号对象存进变量 e
    print(type(e).__name__)         # ValueError ← 型号
    print(e)                        # 这里写人能看懂的说明 ← 载荷
    print(str(e))                   # 同上，str(e) 取消息文本

# 4. 没接住的异常会一路向上传播，直到顶崩并打印回溯（Traceback）
def inner():
    raise KeyError("secret")

def outer():
    inner()                          # 自己不接，信号继续向上传

def top():
    outer()

try:
    top()                            # 调用链：top → outer → inner 抛出
except KeyError as e:
    print("传到顶层被接住:", e)       # secret
# 传播链：inner 抛出 → outer 不接往上抛 → top 不接往上抛 → 这里接住
# 这就是"接信号的职责"：谁有能力处理谁接，都不接就崩给用户看
