# 第七章 错误与异常

对应官方文档：[8. 错误和异常](https://docs.python.org/zh-cn/3/tutorial/errors.html)

你其实已经用过异常了：ch06 的 `parse_int` 里 `try: int(s) except ValueError`，
还有 `int("abc")` 抛出的 `ValueError` 本尊。本章把这个机制讲完整：
异常是**程序出错时的信号系统**——出错不可怕，可怕的是信号没人接、或者接错信号。

## 7.1 语法错误 vs 异常：两种不同性质的错

```python
# 语法错误（SyntaxError）：代码根本跑不起来，解析阶段就被拦下
# for ch in text        ← 少冒号，quiz 里炸过整份卷子的就是它
#     pass

# 异常（Exception）：语法没问题，跑到某一行的【运行时】才炸
int("abc")      # ValueError ← 语法全对，运行时才发现转不动
1 / 0           # ZeroDivisionError
```

区分：**语法错误 = 编辑器/解释器读不懂你的代码**（编译期）；**异常 = 代码读懂了，
执行时撞上意外**（运行期）。Go 类比：语法错误 ≈ 编译失败；异常 ≈ panic（但比 panic
温柔得多——异常可以被接住继续跑，panic 接住就完蛋）。

## 7.2 异常对象：错误也是数据（信号型号表）

异常不是一个"崩溃"，而是一个**被抛出的对象**——有类型（型号）、有信息（载荷）。
类型决定"这是什么错"，这也是 `except` 按类型接的依据：

| 异常类型 | 触发场景 | 你在哪见过 |
|------|------|------|
| `ValueError` | 值对不了：`int("abc")` | ch02、ch06 parse_int |
| `TypeError` | 类型不对：`"a" + 1`、`for x in 6` | quiz 的 evens |
| `KeyError` | 字典键不存在：`d["no"]` | ch05 |
| `IndexError` | 下标越界：`[1, 2][5]` | ch02/ch03 |
| `ZeroDivisionError` | `1 / 0` | ch02 |
| `FileNotFoundError` | open 读不存在的文件 | ch06 模式表 |
| `json.JSONDecodeError` | loads 吃到坏 json 文本 | 本章新朋友（ValueError 的子类！） |

```python
try:
    raise ValueError("手动的信号")     # raise = 抛出一个异常对象
except ValueError as e:               # as e：接住信号，对象存进 e
    print(type(e).__name__, e)         # ValueError 手动的信号
    # e 就是异常对象本身——类型 + 消息，能打印、能存变量、能传递
```

## 7.3 try/except：接信号的完整语法

```python
try:
    # 危险行（只包真正可能炸的行，别把整个函数裹进去）
    n = int(user_input)
    result = 100 / n
except ValueError:            # 按类型接：只接这一种信号
    print("不是数字")
except ZeroDivisionError:     # 可以列多个 except，从上往下匹配
    print("不能是 0")
except (TypeError, KeyError) as e:   # 也可以一个 except 接多种
    print("其他错:", e)
```

三条铁律：

1. **except 后面必须写具体类型**。裸 `except:` 连 `KeyboardInterrupt`（Ctrl+C）
   都会吞掉，排查问题时是灾难。
2. **try 只包危险行**。try 块越大，你越分不清是哪一行炸的。
3. **接住 ≠ 消失**。接住后要么处理（给默认值、重试、提示），要么继续往上抛
   （`raise` 裸写 = 原样转发）——什么都不做的空 except 比不接还糟。

## 7.4 else 与 finally：没有炸和无论炸不炸

```python
try:
    f = open("data.txt", encoding="utf-8")
except FileNotFoundError:
    print("文件不存在")
else:
    # else：try 块【没炸】才执行（把"成功路径"从 try 里挪出来）
    print(f.read())
    f.close()
finally:
    # finally：无论炸不炸、接没接住，都执行（清理资源）
    print("收尾工作")
```

| 块 | 什么时候执行 |
|------|------|
| `try` | 总是先试 |
| `except 类型` | try 炸了且类型匹配 |
| `else` | try **没**炸才执行 |
| `finally` | **总是**执行（炸了没接住也执行，然后继续往上抛） |

Go 对照：`defer` ≈ finally（清理收尾）；Go 的 `if err != nil` 是**每次调用后显式检查**，
Python 是**先跑炸了再说**——见 7.6 EAFP。

> with 语句的真相：`with open(...) as f:` 内部就是 try/finally——退出块时
> 自动 `f.close()`，异常也照关。这就是 ch06 说的"无论发生什么都关闭"的实现原理。

## 7.5 raise：主动抛信号 + 异常继承树

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"年龄不能是负数: {age}")   # 主动抛
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)                     # 年龄不能是负数: -5
```

**抛什么类型有讲究**：值不合法 → `ValueError`；类型不对 → `TypeError`；
自己业务规则的错 → 继承 `Exception` 自定义（ch08+ 再展开）。

异常是一个**继承树**，except 按树接——接父类会连子类一起接住：

```python
BaseException                 # 顶级（包括 SystemExit/KeyboardInterrupt——别接它）
└── Exception                 # ← 自定义异常的默认父类
    ├── ValueError
    │   └── json.JSONDecodeError   # 子类：接 ValueError 就能接住它
    ├── TypeError
    ├── KeyError              # 注意：它是 LookupError 的子类
    └── ...
```

```python
import json
try:
    json.loads("{坏掉的 json")
except ValueError:            # JSONDecodeError 是 ValueError 的子类
    print("json 文本坏了")     # 用父类接，照样接得住
```

## 7.6 EAFP vs LBYL：Python 的处世哲学

```python
# LBYL（Look Before You Leap，三思而后跳）—— Go 的习惯
if "port" in config:            # 先检查
    port = config["port"]

# EAFP（Easier to Ask Forgiveness than Permission，先干错了再道歉）—— Python 的习惯
try:
    port = config["port"]       # 先直接干
except KeyError:                # 炸了再接
    port = 8080
```

Python 社区偏爱 EAFP：检查和取值之间可能被别处修改（竞态），而"直接做 + 接异常"
是原子的。Go 的 `if err != nil` 是 LBYL 的极致——每步显式检查；Python 把"检查"
外包给了异常机制。两种都合法，但读 Python 代码时看到 try 别奇怪，那常常就是
一次"正常的分支"。

## 7.7 本章小结

- 语法错误跑不起来；异常是运行期的**信号对象**（类型 + 消息）
- except 写具体类型，从上往下匹配；一个 except 可接多种
- try 只包危险行；else = 没炸才跑；finally = 永远跑（with 的内部原理）
- raise 主动抛；`raise` 裸写在 except 里 = 原样转发
- except 父类连子类一起接（JSONDecodeError ⊂ ValueError）
- EAFP：直接做 + 接异常，是 Python 的惯用法

---

## ✍️ 动手运行

```bash
python ch07/01_errors.py
python ch07/02_try_except.py
python ch07/03_raise_finally.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch07.test_exercises
```

## 🔗 官方文档深入阅读

- 错误和异常：<https://docs.python.org/zh-cn/3/tutorial/errors.html>
- 内置异常继承树全图：<https://docs.python.org/zh-cn/3/library/exceptions.html#exception-hierarchy>
