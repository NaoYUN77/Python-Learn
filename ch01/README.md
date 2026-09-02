# 第一章 起步：安装、注释、基本语法

对应官方文档：[The Python Tutorial · 1. Whetting Your Appetite · 2. Using the Python Interpreter](https://docs.python.org/zh-cn/3/tutorial/introduction.html)

## 1.1 安装 Python

1. 前往 <https://www.python.org/downloads/> 下载最新版（本章示例使用 Python 3.12）。
2. **Windows**：安装时记得勾选 **"Add Python to PATH"**。
3. 验证安装，打开终端（Terminal）输入：

```bash
python --version
```

如果显示类似 `Python 3.12.x`，说明安装成功。

## 1.2 两种运行方式

**方式一：交互式解释器（REPL）**
在终端输入 `python` 回车，进入交互界面，逐行输入立即得到结果：

```python
>>> print("你好，世界")
你好，世界
```
输入 `exit()` 或按 `Ctrl+Z` 回车退出。

**方式二：运行脚本文件**
把代码保存为 `.py` 文件，然后：
```bash
python hello.py
```

> 💡 本章代码都在 `ch01` 目录下，你可以直接运行查看效果。

## 1.3 最基础的语法

### 1.3.1 注释（Comment）

注释是给人看的，程序运行时会忽略。

```python
# 这是单行注释，井号后面都是注释

# 多行注释用三个引号包裹（实际上是一个没被赋值的字符串）
"""
这是多行注释。
可以写很多行说明文字。
"""
```

> 参考：[Comments](https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#comments)

### 1.3.2 print() 打印输出

`print()` 是最常用的输出函数。

```python
print(1 + 1)          # 输出：2
print("Hello World!") # 输出：Hello World!
```

### 1.3.3 字符串与引号

Python 中字符串可以用单引号 `''` 或双引号 `""` 包裹，效果一样。

```python
print('单引号字符串')
print("双引号字符串")
```

### 1.3.4 回车符 \n 与制表符 \t

在字符串里，`\n` 表示换行，`\t` 表示 Tab 缩进。

```python
print("第一行\n第二行")
print("名字\t年龄")  # Tab 可以让文字对齐
```

## 1.4 变量（Variable）

变量就是给数据起名字。Python 不需要声明类型，直接赋值即可。

```python
number = 42          # 整数
pi = 3.14159         # 小数（浮点数）
name = "Alice"       # 字符串

print(number)
print(pi)
print(name)
```

### 变量命名的规范

- 只能由 **字母、数字、下划线** `_` 组成
- **不能以数字开头**
- 不能是 Python 关键字（如 `if`、`for`、`class`）
- 建议用**小写字母 + 下划线**（称为 snake_case）：例如 `my_name`、`total_count`

```python
my_name = "Bob"     # ✅ 正确
# 1st_job = "x"     # ❌ 不能以数字开头
# my-name = "x"     # ❌ 不能有连字符
```

## 1.5 关键字（Keywords）

关键字是 Python 保留的单词，不能用作变量名。官方列表见
[Keywords](https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#keywords)。

常用关键字：`if` `else` `for` `while` `def` `return` `class` `import` `True` `False` `None` …

```python
# 查看所有关键字
import keyword
print(keyword.kwlist)
```

## 1.6 本章小结

- Python 用缩进来表示代码块（下一章详细讲）
- 大小写敏感：`Name` 和 `name` 是两个不同的变量
- 一个语句结束不需要分号（但加分号也不报错）

---

## ✍️ 动手运行

打开本目录文件，依次运行：

```bash
python ch01/01_hello.py
python ch01/02_variables.py
```

看看输出是否符合你的预期。改一改里面的数字和文字，观察变化——这是学习的最好方式。

## 🧪 实践练习

打开 `exercises.py`，完成里面的函数，然后在**项目根目录**运行：

```bash
python -m ch01.test_exercises
```

## 🔗 官方文档深入阅读

- 交互式解释器：<https://docs.python.org/zh-cn/3/tutorial/interpreter.html>
- 字符串字面值：<https://docs.python.org/zh-cn/3/tutorial/introduction.html#strings>
- 变量名规则：<https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#identifiers>
