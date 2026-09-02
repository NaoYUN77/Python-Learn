"""03_raise_finally.py — raise 主动抛、异常继承树、EAFP vs LBYL。

运行：python ch07/03_raise_finally.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/errors.html#raising-exceptions
"""

import json

# ══════════════════════════════════════════
# 第一部分：raise —— 主动抛信号
# ══════════════════════════════════════════

# 1. 用异常表达"参数不合法"（比 return -1 / return None 更明确）
def set_age(age):
    if age < 0:
        raise ValueError(f"年龄不能是负数: {age}")   # 抛给调用方处理
    return age

try:
    set_age(-5)
except ValueError as e:
    print("捕获:", e)                    # 年龄不能是负数: -5
# 对比 ch06 的 parse_int（出错返回 None）：返回 None 是"静默失败"，
# 调用方容易忘记检查；raise 是"大声失败"，逼调用方面对。
# 两种都合法，看场景：输入来自用户、有合理兜底 → None；参数违反约定 → raise

# 2. raise 也可以抛内置的其他型号：类型不对就 TypeError
def repeat(text, times):
    if not isinstance(times, int):
        raise TypeError(f"times 必须是 int，拿到 {type(times).__name__}")
    return text * times

try:
    repeat("ab", "2")
except TypeError as e:
    print("捕获:", e)                    # times 必须是 int，拿到 str


# ══════════════════════════════════════════
# 第二部分：异常继承树 —— except 按树接
# ══════════════════════════════════════════

# 3. 树长这样（缩进 = 继承）：
# BaseException
# ├── SystemExit / KeyboardInterrupt      ← 系统级，别接
# └── Exception                           ← 我们能接的都在它下面
#     ├── ValueError
#     │   └── json.JSONDecodeError        ← 子类
#     ├── TypeError
#     ├── LookupError
#     │   ├── KeyError
#     │   └── IndexError
#     └── ArithmeticError
#         └── ZeroDivisionError

# 4. 验证家谱：issubclass(子, 父)
print(issubclass(json.JSONDecodeError, ValueError))    # True
print(issubclass(KeyError, LookupError))               # True
print(issubclass(KeyError, IndexError))                # False 兄弟不是父子

# 5. 接父类 = 连子类一起接
try:
    json.loads("{坏的")
except ValueError:                        # 用父类 ValueError 接
    print("接住了 JSONDecodeError ← 父类能接子类")

# 6. 反过来不行：接子类接不住父类
try:
    try:
        int("abc")                        # 抛的是 ValueError 本尊
    except json.JSONDecodeError:          # 想用子类接
        print("到不了这里")
except ValueError:
    print("子类接不住父类 ← 类型必须匹配自身或祖先")

# 7. 多个 except 的顺序：子类在前、父类在后（反了父类会遮蔽子类）
try:
    json.loads("{坏的")
except json.JSONDecodeError as e:         # 子类在前：精确处理
    print("精确分支:", e.__class__.__name__)
except ValueError:                        # 父类兜底（永远轮不到它处理 JSON 错）
    print("兜底分支")


# ══════════════════════════════════════════
# 第三部分：except 里的 raise —— 记录后转发
# ══════════════════════════════════════════

# 8. 裸 raise = 原样转发（接住看了一眼，继续往上抛）
def load_settings():
    try:
        with open("ch07/缺失配置.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  记个日志：配置文件缺失")
        raise                             # 不吞，转发给上层调用者

try:
    load_settings()
except FileNotFoundError:
    print("  上层收到转发的异常，做自己的处理")

# 9. raise NewType from e：包装后抛（保留原始线索）
try:
    try:
        json.loads("{坏的")
    except json.JSONDecodeError as e:
        raise RuntimeError("配置文件解析失败") from e   # from e 连上原始异常
#raise自定义RuntimeError包装
except RuntimeError as e:
    print("包装后:", e)
    print("原始线索:", e.__cause__)       # __cause__ 就是那个 JSONDecodeError


# ══════════════════════════════════════════
# 第四部分：EAFP vs LBYL —— Python 的处世哲学
# ══════════════════════════════════════════

# 10. LBYL（Look Before You Leap）：先检查再动手 —— Go 的 if err != nil 风格
config = {"host": "localhost"}
if "port" in config:                      # 先看
    port = config["port"]
else:
    port = 8080
print("LBYL:", port)

# 11. EAFP（Easier to Ask Forgiveness than Permission）：直接干，炸了再接 —— Python 惯用
try:
    port = config["port"]                 # 直接取
except KeyError:                          # 炸了再道歉
    port = 8080
print("EAFP:", port)

# 为什么 Python 偏爱 EAFP：
#   a. 检查和行动之间数据可能被改（in 检查完、取值前，别的线程删了键）——EAFP 是原子的
#   b. 只写一次键名，不用写两遍（in 一遍、[] 一遍）
#   c. "异常"在 Python 里不丢人，它常被当正常的分支控制用
# Go 对照：Go 的 err 返回值把检查强加在每次调用后（LBYL 思路）；
# Python 把检查外包给 try——写 Python 时心态要换：炸不是事故，是信号。
