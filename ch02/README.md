# 第二章 基础数据类型与运算符

对应官方文档：[3. Python 速览](https://docs.python.org/zh-cn/3/tutorial/introduction.html)

程序的本质就是**处理数据**。本章学习 Python 内置的四种基础数据类型：
`int`（整数）、`float`（浮点数）、`bool`（布尔）、`str`（字符串），以及围绕它们的运算符。

## 2.1 数字：int 与 float

### 基本算术运算符

| 运算符 | 含义 | 示例 | 结果 |
|--------|------|------|------|
| `+` | 加 | `7 + 3` | `10` |
| `-` | 减 | `7 - 3` | `4` |
| `*` | 乘 | `7 * 3` | `21` |
| `/` | 除（结果永远是 float） | `7 / 2` | `3.5` |
| `//` | 整除（向下取整） | `7 // 2` | `3` |
| `%` | 取余 | `7 % 2` | `1` |
| `**` | 幂 | `2 ** 10` | `1024` |

两个容易踩的坑：

```python
print(-7 // 2)   # -4  整除是"向下取整"，不是"去掉小数"
print(0.1 + 0.2) # 0.30000000000000004 浮点精度问题，所有语言都有
```

比较浮点数是否相等，用 `round()` 处理后再比。

- `int` 没有大小限制，`2 ** 100` 也能精确计算
- `int` 和 `float` 混合运算，结果自动是 `float`
- 复合赋值：`count += 5` 等价于 `count = count + 5`（同理 `-=  *=  /=  //=  %=  **=`）

### 运算优先级

括号 > `**` > `*  /  //  %` > `+  -`。拿不准就加括号，可读性更好。

## 2.2 布尔：bool

只有两个值：`True` 和 `False`（注意首字母大写）。比较运算的结果就是布尔值：

```python
print(3 > 2)    # True
print(3 == 3)   # True   相等是两个等号
print(3 != 4)   # True   不等
```

| 运算符 | 含义 |
|--------|------|
| `==` `!=` | 等于、不等于 |
| `<` `<=` `>` `>=` | 大小比较 |
| `and` | 与：两个都为 True 才 True |
| `or` | 或：有一个为 True 就 True |
| `not` | 非：取反 |

### 真假值（truthiness）

Python 里任何数据都能放到 `if` 里判断真假，以下是**假**的，其余都是真：

- `0`、`0.0`
- 空字符串 `""`
- 空列表 `[]`、空字典 `{}`、空元组 `()`（第五章会学）
- `None`、`False`

## 2.3 字符串：str

### 不可变

字符串创建后**不能原地修改**，只能创建新字符串：

```python
word = "Python"
# word[0] = "J"        # ❌ TypeError
word = "J" + word[1:]  # ✅ "Jython"
```

### 索引与切片

```python
word = "Python"
word[0]     # 'P'   索引从 0 开始
word[-1]    # 'n'   负数从末尾往前数
word[0:2]   # 'Py'  切片 [start:stop]，含头不含尾
word[2:]    # 'thon' 省略 stop = 取到末尾
word[::-1]  # 'nohtyP' 步长 -1 反转
```

### 常用方法

| 方法 | 作用 |
|------|------|
| `len(s)` | 长度 |
| `s.strip()` | 去掉两端空白 |
| `s.upper()` / `s.lower()` | 大写 / 小写 |
| `s.split(",")` | 按分隔符切成列表 |
| `", ".join(列表)` | 把列表拼成字符串 |
| `s.replace(a, b)` | 替换 |
| `s.startswith(x)` / `s.find(x)` | 开头判断 / 查找位置 |
| `"ab" * 3` | 重复 → `ababab` |

### f-string 格式化（推荐）

```python
name, pi = "Alice", 3.14159
print(f"我叫{name}")            # {} 里放变量
print(f"{pi:.2f}")              # 3.14  保留两位小数
print(f"{name:>10}")            # 右对齐宽度 10
print(f"{1234567:,}")           # 1,234,567 千分位
```

## 2.4 类型转换

用 `int()` `float()` `str()` `bool()` 显式转换：

```python
int("42")     # 42
int(3.9)      # 3    注意是截断，不是四舍五入
float("3.14") # 3.14
str(42)       # '42'
bool(0)       # False
bool("")      # False
bool("hi")    # True
int("3.14")   # ❌ ValueError 字符串必须是纯整数才能转 int
```

用 `type(x)` 查看类型，`isinstance(x, int)` 判断类型（更推荐）。

## 2.5 本章小结

- `/` 结果永远是 float；`//` 向下取整；`%` 取余
- 字符串不可变；切片含头不含尾
- f-string 是格式化首选
- 转换时 `int(3.9)` 是截断；`bool` 的假值只有那几种

---

## ✍️ 动手运行

```bash
python ch02/01_numbers.py
python ch02/02_strings.py
python ch02/03_type_conversion.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch02.test_exercises
```

## 🔗 官方文档深入阅读

- 数字：<https://docs.python.org/zh-cn/3/tutorial/introduction.html#numbers>
- 字符串：<https://docs.python.org/zh-cn/3/tutorial/introduction.html#strings>
- 内置类型总表：<https://docs.python.org/zh-cn/3/library/stdtypes.html>
