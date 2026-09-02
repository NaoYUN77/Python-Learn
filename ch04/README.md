# 第四章 函数

对应官方文档：[4. 更多控制流工具 — 定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)（4.7–4.9 节）

前三章的代码都是"一次性脚本"。本章学会把逻辑装进**函数**——可以反复调用、可以组合的积木块。这也是通往 Agent 开发的关键一步：Agent 调用的每一个"工具"，本质上就是一个函数。

## 4.1 定义与返回值

```python
def add(a, b):
    """两数相加。"""        # 三引号文档字符串（docstring）
    return a + b

result = add(3, 4)          # 7
```

要点：

- `def 名字(参数):` + 缩进，和 if/for 同样的语法规则
- `return` 把结果交还给调用方，并**立刻结束函数**（ch03 练习 5 的教训）
- 没有 `return` 的函数返回 `None`
- `return a, b` 一次返回多个值（其实是元组），可用 `low, high = f(...)` 解包

## 4.2 默认参数与关键字参数

```python
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")                       # 用默认值：你好，小明！
greet("小明", "早上好")              # 按位置覆盖默认值
greet(greeting="晚安", name="小红")  # 按名字传，顺序随意
```

- **默认参数**：定义时写 `参数=默认值`，调用时可省略
- **关键字参数**：调用时写 `名字=值`，可读性好且不怕顺序
- 参数列表里出现一个裸 `*` 后，后面的参数**只能**按关键字传（很多标准库这么设计）

## 4.3 可变默认值的坑（高频面试题）⚠️

```python
# ❌ 默认值只在 def 时创建一次，列表被所有调用共享
def append_bug(item, items=[]):
    items.append(item)
    return items

append_bug("a")   # ['a']
append_bug("b")   # ['a', 'b']  ← b 怎么跟 a 在一起？！

# ✅ 惯用写法：用 None 占位，函数体里建新列表
def append_ok(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

> 规则：默认值只用数字、字符串、`None` 这类**不可变对象**；列表/字典要做默认值时走 `None` 占位。

## 4.4 *args、**kwargs 与解包

```python
def total(*args, **kwargs):   # args 是元组，kwargs 是字典
    print(args, kwargs)

total(1, 2, mode="fast")      # (1, 2) {'mode': 'fast'}
```

- `*args`：收走多余的**位置参数**，打包成元组（名字叫什么都行，`*` 才是关键）
- `**kwargs`：收走多余的**关键字参数**，打包成字典
- 定义时顺序：普通参数 → `*args` → 关键字参数 → `**kwargs`

调用时 `*` / `**` 反过来是**解包**：

```python
size = [3, 4]
area(*size)                  # 等价于 area(3, 4)

opts = {"width": 5, "height": 6}
area(**opts)                 # 等价于 area(width=5, height=6)
```

> 💡 以后写 Agent 时，"把参数原样转发给工具函数"的 `func(*args, **kwargs)` 就是这个模式。

## 4.5 lambda：一行的小函数

```python
double = lambda x: x * 2      # 冒号前是参数，后面是返回值表达式

sorted(students, key=lambda p: p[1], reverse=True)   # 按分数排
```

lambda 适合当**一次性配件**（尤其做 `key`）；逻辑超过一行就用 `def`。

函数本身也是值：可以赋给变量、存进列表、当参数传（练习 7 会用到）。

## 4.6 作用域与闭包

```python
x = 10                     # 全局变量

def read_global():
    print(x)               # ✅ 函数内能"读"外面的变量

def try_change():
    # x = x + 1            # ❌ UnboundLocalError：有赋值就成了局部变量
    y = x + 1              # ✅ 只读不写没问题
```

**闭包**：内层函数可以"记住"外层函数的参数：

```python
def make_multiplier(n):
    def multiply(x):
        return x * n       # n 来自外层，函数返回后仍被记住
    return multiply

triple = make_multiplier(3)
triple(5)                  # 15
```

## 4.7 类型标注与文档字符串

```python
def repeat(text: str, times: int = 2) -> str:
    """把 text 重复 times 遍。"""
    return text * times
```

- 标注是写给**人和工具**看的说明书：Python 运行时不强制，但 Pylance 会据此查错、补全
- Agent 开发里函数标注非常重要——模型靠它知道该传什么参数

## 4.8 本章小结

- `return` 立刻结束函数并交回结果；无 return 返回 `None`
- 默认参数让调用更省事；关键字参数让调用更明确
- **可变默认值是坑**，用 `None` 占位
- `*args` 收位置参数成元组，`**kwargs` 收关键字参数成字典；调用时 `*`/`**` 是解包
- lambda 是一行小函数，最常当 `key` 用
- 函数内可读全局变量；内层函数记住外层变量 = 闭包

---

## ✍️ 动手运行

```bash
python ch04/01_basics.py
python ch04/02_params.py
python ch04/03_args_kwargs.py
python ch04/04_lambda_scope.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch04.test_exercises
```

## 🔗 官方文档深入阅读

- 定义函数：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions>
- 默认参数与关键字参数：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#more-on-defining-functions>
- 任意参数列表：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#arbitrary-argument-lists>
- 解包参数列表：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#unpacking-argument-lists>
- lambda 表达式：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#lambda-expressions>
- 文档字符串与函数标注：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#documentation-strings>
