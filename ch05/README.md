# 第五章 数据结构：列表、元组、集合、字典

对应官方文档：[5. 数据结构](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)

前面我们零散用过列表和元组（`students`、`kwargs.items()`）。本章系统认识 Python 的四大**内置容器**——它们是组织数据的地基：Agent 处理的消息列表、工具注册表（字典）、去重缓存（集合），全靠这四种结构。

## 5.1 列表：可变的有序序列

```python
fruits = ["橙子", "苹果", "梨"]
```

**改**（原地修改，返回 None！）：

| 方法 | 作用 | 示例 |
|------|------|------|
| `append(x)` | 尾部加一个 | `fruits.append("桃")` |
| `insert(i, x)` | 位置 i 插入 | `fruits.insert(0, "莓")` |
| `extend(序列)` | 尾部并进一堆 | `fruits.extend(["a", "b"])` |
| `remove(x)` | 删第一个等于 x 的 | `fruits.remove("苹果")` |
| `pop([i])` | 弹出位置 i（默认末尾）并返回 | `last = fruits.pop()` |
| `clear()` | 清空 | `fruits.clear()` |
| `sort()` | 原地排序 | `fruits.sort()` |
| `reverse()` | 原地反转 | `fruits.reverse()` |

⚠️ **最常见的新手坑**：这些方法**原地修改、返回 None**：

```python
fruits = fruits.sort()      # ❌ fruits 变成 None 了！
fruits.sort()               # ✅ 直接调用，列表自己变
sorted(fruits)              # ✅ 或者用函数版：不改原列表，返回新列表
```

**查**（不改列表，返回值）：

| 操作 | 作用 |
|------|------|
| `x in fruits` | 在不在（成员测试） |
| `fruits.index(x)` | x 第一次出现的位置，没有则 ValueError |
| `fruits.count(x)` | x 出现几次 |
| `len(fruits)` | 长度 |
| `fruits[1:3]` | 切片（含头不含尾，ch02 讲过） |

**栈与队列**：

```python
# 栈（后进先出）：append + pop 一对
stack = []
stack.append(1); stack.append(2)
stack.pop()               # 2

# 队列（先进先出）：用 collections.deque，别用列表（列表头部操作慢）
from collections import deque
queue = deque(["a", "b"])
queue.append("c")
queue.popleft()           # "a"
```

`del` 语句：按位置或切片删除，不是方法：

```python
del fruits[0]             # 删第 0 个
del fruits[1:3]           # 删一段
```

## 5.2 元组：不可变的序列

```python
point = (3, 4)
single = (42,)            # ⚠️ 单元素必须带逗号，(42) 只是数字加括号
empty = ()
```

- **不可变**：没有 append/remove，定义后不能改（`point[0] = 5` ❌ TypeError）
- 能做的：索引、切片、`in`、`len`、`count`、`index`——所有"只读"操作
- **序列解包**（ch04 见过 `q, r = f()`）：

```python
x, y = point              # x=3, y=4
a, b = b, a               # 经典：一行交换两个变量
first, *rest = [1, 2, 3, 4]   # 星号收尾：first=1, rest=[2, 3, 4]
```

**元组 vs 列表怎么选**：内容会增删改 → 列表；一组固定搭配（坐标、键值对、函数多返回值）→ 元组。不可变还意味着可做字典的键、可放进集合——列表不行。

## 5.3 集合：无序、不重复

```python
basket = {"苹果", "橙子", "苹果", "梨"}
# {'苹果', '橙子', '梨'}     ← 重复自动消失，顺序不保证

empty = set()              # ⚠️ {} 是空字典！空集合必须写 set()
letters = set("hello")     # 从序列建集合：{'h', 'e', 'l', 'o'}
```

两大用途——**去重**和**快速成员测试**（`in` 集合比 `in` 列表快得多）：

```python
unique = list(set([1, 2, 2, 3, 3, 3]))    # [1, 2, 3]
```

数学运算：

```python
a = {1, 2, 3}
b = {3, 4, 5}
a | b       # 并 {1, 2, 3, 4, 5}
a & b       # 交 {3}
a - b       # 差 {1, 2}
a ^ b       # 对称差 {1, 2, 4, 5}（不同时在两边）
```

注意：无序 → 没有 `s[0]`，不能按下标取。

## 5.4 字典：键 → 值

ch04 的 `kwargs` 就是字典，现在正式补全：

```python
person = {"name": "小明", "age": 18}

person["age"]             # 取值：18（键不存在 → KeyError）
person["city"] = "北京"    # 新增/修改
del person["city"]        # 删除
"name" in person          # 查键（查的是键，不是值！）

person.get("phone")           # 不存在返回 None，不报错
person.get("phone", "未填写")  # 不存在返回默认值
```

遍历三件套（ch04 你已经用过 items 了）：

```python
for k in person.keys():          # 只要键
    ...
for v in person.values():        # 只要值
    ...
for k, v in person.items():      # 键值成对（元组，可解包）
    ...
```

> 💡 Agent 的"工具注册表"就是字典：`{"search": search_tool, "calc": calc_tool}`——工具名当键，函数当值。

## 5.5 推导式：一行制造容器

**列表推导式**——把"循环 + append"压成一行：

```python
# 普通写法
squares = []
for x in range(10):
    squares.append(x ** 2)

# 推导式
squares = [x ** 2 for x in range(10)]

# 带 if 过滤
evens = [x for x in range(20) if x % 2 == 0]

# 带 if/else 加工
labels = ["偶" if x % 2 == 0 else "奇" for x in range(5)]
```

读法：`[表达式 for 变量 in 序列 if 条件]` —— 取每个元素，过筛子，按模板加工。

字典和集合推导式同理：

```python
{x: x ** 2 for x in range(4)}      # {0: 0, 1: 1, 2: 4, 3: 9}
{ch for ch in "hello" if ch != "l"} # {'h', 'e', 'o'}
```

ch04 练习 5 里 `join(f"..." for k, v in ...)` 那个没方括号的版本是**生成器表达式**——不需要列表中间产物时用它，省内存。嵌套推导式先不深究，双层循环的可读性通常不如普通 for。

## 5.6 本章小结

- 列表方法**原地改、返回 None**；要新列表用 `sorted()` / 切片
- 元组不可变、可解包；单元素 `(42,)` 别忘逗号
- 集合去重 + 快速 `in` + 数学运算；空集合是 `set()` 不是 `{}`
- 字典键值对；`.get()` 安全取值；遍历用 keys/values/items
- 推导式 `[式 for 变量 in 序列 if 条件]` 是循环+append 的压缩语法

---

## ✍️ 动手运行

```bash
python ch05/01_lists.py
python ch05/02_tuples.py
python ch05/03_sets.py
python ch05/04_dicts.py
python ch05/05_comprehensions.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch05.test_exercises
```

## 🔗 官方文档深入阅读

- 列表详解：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists>
- del 语句：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#the-del-statement>
- 元组与序列：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#tuples-and-sequences>
- 集合：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets>
- 字典：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries>
- 推导式：<https://docs.python.org/zh-cn/3/tutorial/datastructures.html#list-comprehensions>
