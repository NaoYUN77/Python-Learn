# 第三章 控制流：条件与循环

对应官方文档：[4. 更多控制流工具](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)

前两章的程序都是"从上到下依次执行"。本章让程序学会**做选择**（if）和**重复做事**（for/while）——这是程序"会思考"的第一步。

## 3.1 if / elif / else

```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")      # ← 85 会走这里
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

三条铁律：

- **冒号结尾，缩进成块**：`if` 行末必须有 `:`，下一行缩进 4 个空格。缩进在 Python 里是语法，不是美化。
- **从上往下短路**：逐个检查条件，命中第一个就走该分支并跳过其余，所以范围要从高到低排。
- **else 可省略**：没有 else 且条件都不满足，就什么都不做。

### 一个重要的化简（呼应你的 ch02 练习）

比较运算的结果本身就是布尔值，不要画蛇添足：

```python
# ❌ 啰嗦
if n % 2 == 0:
    return True
else:
    return False

# ✅ 一行就够了
return n % 2 == 0
```

### 条件组合与真假值

```python
if age >= 18 and has_ticket:   # and/or/not 组合
    ...

if 0 <= score <= 100:          # 链式比较，Python 特有
    ...

if not name:                   # 空字符串是假值，比 if name == "" 更 Pythonic
    ...

if "a" in "cat":               # in 判断成员关系
    ...
```

## 3.2 for 循环与 range()

**遍历**序列里的每个元素：

```python
for ch in "abc":
    print(ch)                # 依次打印 a b c
```

需要数字序列时用 `range()`（**含头不含尾**，和切片一致）：

```python
range(5)         # 0 1 2 3 4
range(1, 10)     # 1..9（不含 10）
range(0, 10, 2)  # 0 2 4 6 8（步长 2）
range(10, 0, -1) # 10 9 8 ... 1（倒着数）
```

经典结构——**累加器**：循环外定义 `total = 0`，循环里 `total += x`。

## 3.3 while 循环

**已知次数用 for，只知道"什么时候停"用 while**：

```python
count = 0
while count < 3:
    print(count)
    count += 1    # ⚠️ 忘了这行就是死循环，Ctrl+C 中断
```

"一直运行直到退出"的典型结构：`while True:` + `break`。

## 3.4 break、continue 和循环的 else

- `break`：**立刻跳出整个循环**
- `continue`：**跳过本次**，进入下一轮
- 循环的 `else`：循环**没有被 break 打断**时执行，适合"找东西，找完了没找到"

```python
# 找 100 以内的质数：内层没 break 过 = 没找到因子 = 质数
for n in range(2, 10):
    for m in range(2, n):
        if n % m == 0:
            break
    else:
        print(n, "是质数")   # 2 3 5 7
```

## 3.5 match / case（Python 3.10+）

按值分发时比 `if/elif` 更清晰：

```python
match cmd:
    case "start":
        ...
    case "help" | "h":   # 多个值命中同一分支
        ...
    case _:              # 兜底，相当于 else
        ...
```

> 💡 以后写 Agent，"根据工具名调用对应函数"的调度逻辑就长这个样子。

## 3.6 本章小结

- 缩进即代码块；分支/循环语句都以冒号结尾
- 已知次数 → `for` + `range()`；未知次数 → `while`
- `break` 跳出，`continue` 跳过；循环 `else` = 没被 break 才执行
- `return n % 2 == 0` 优于 if/else 返回 True/False

---

## ✍️ 动手运行

```bash
python ch03/01_if.py
python ch03/02_loops.py
python ch03/03_match.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch03.test_exercises
```

## 🔗 官方文档深入阅读

- if 语句：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#if-statements>
- for 与 range：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#for-statements>
- break/continue/else：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops>
- match 语句：<https://docs.python.org/zh-cn/3/tutorial/controlflow.html#match-statements>
