# 第六章 输入输出与文件

对应官方文档：[7. 输入输出](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html)

程序的价值在于和外界交换信息：把结果**打印**给人看、从用户**读**输入、把数据**存**进文件、下次再**读**回来。本章还引入两个重量级工具：`with` 语句（自动管理资源）和 `json`（结构化数据的存取标准）。

## 6.1 print 与 f-string 复习进阶

```python
print("a", "b", "c")              # a b c（多个参数默认用空格连接）
print("a", "b", sep="-")          # a-b（自定义分隔符）
print("不换行", end="")            # end 默认是 "\n"，改成别的就不换行
print("错误信息", file=sys.stderr) # 输出到标准错误流（进阶，了解即可）
```

f-string 进阶格式化：

```python
pi = 3.14159
print(f"{pi:.2f}")                # 3.14（保留两位小数）
print(f"{1234567:,}")             # 1,234,567（千分位）
print(f"{0.25:.0%}")              # 25%（百分比）
print(f"{name=}")                 # name='小明'（调试神器：连变量名一起打印）
```

## 6.2 input：从用户读输入

```python
name = input("你叫什么？")        # 括号里是提示语
age = int(input("几岁？"))         # ⚠️ input 返回的一律是字符串！
```

**铁律：`input()` 的返回值永远是 `str`**，要算术必须先转换（ch02 的 `int()`/`float()`）。忘了转就是 `"10" + 5` → `TypeError`。

## 6.3 文件读写三步：open → 操作 → close

```python
f = open("note.txt", "r")   # 打开（"r" 读、"w" 写、"a" 追加）
content = f.read()          # 读
f.close()                   # 关闭 ⚠️ 忘了会占住资源、可能丢数据
```

三种读法：

| 方法 | 返回 | 适合 |
|------|------|------|
| `f.read()` | 整个文件的字符串 | 小文件 |
| `f.readlines()` | 每行一个元素的列表 | 需要按下标/行号操作 |
| `for line in f:` | 逐行（最省内存，推荐） | 大文件、逐行处理 |

写文件：

```python
f = open("note.txt", "w")   # ⚠️ "w" 模式：文件不存在则创建；存在则【清空重写】！
f.write("第一行\n")          # write 不自动换行，\n 要自己写
f.close()
```

模式表：

| 模式 | 含义 | 文件不存在时 | 文件存在时 |
|------|------|-------------|-----------|
| `"r"` | 只读 | FileNotFoundError | 从头读 |
| `"w"` | 只写 | 创建 | **清空重写** ⚠️ |
| `"a"` | 追加 | 创建 | 在末尾接着写 |
| `"x"` | 只写（排它创建） | 创建 | FileExistsError |

## 6.4 with 语句：自动关文件（本章程牌）

手动 `close()` 有两个坑：忘了关、或中途出异常导致关不上。`with` 保证**无论发生什么，退出时自动 close**：

```python
with open("note.txt", "r", encoding="utf-8") as f:
    content = f.read()
# 出了 with 块，f 已自动关闭，不用（也不能）再 f.close()
```

**规则：打开文件一律用 with**。这是社区铁律，从此不再手写 `open` + `close`。

参数 `encoding="utf-8"`：显式声明编码，避免 Windows 默认 GBK 造成的中文乱码——**Windows 用户必写**。

## 6.5 json：把结构化数据存成文件

字符串/数字存文件简单，但列表、字典怎么办？`json` 模块负责 Python 数据 ↔ 文本格式的互转。

dumps 一件事发生在两个层面：**类型层面** dict → str（产物是 Python 字符串），**格式层面** Python 数据 → json 文本（True 变 true、None 变 null）：

```python
import json

# 对象 → 字符串：dumps（dump string）
# 产物是一个 Python 字符串，内容是 json 格式文本
text = json.dumps({"name": "小明"})               # 默认 ensure_ascii=True：
                                                  # '{"name": "\u5c0f\u660e"}' 中文被转义
text = json.dumps({"name": "小明"}, ensure_ascii=False)
                                                  # '{"name": "小明"}' 中文原样可读

# 字符串 → 对象：loads（load string）
# 拿到 json 文本，还原成能 [ ] 取值、能遍历的活字典/列表
data = json.loads(text)                            # {"name": "小明"}

# 对象 → 文件：dump（少个 s，不经过字符串直接写文件）
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 文件 → 对象：load
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

**方向记忆**（别学反！这是你 split/join 犯过的同款方向病）：

| 函数 | 方向 | 助记 |
|------|------|------|
| `dumps` | 对*象 → **s**tring | **s** = string *|
| `loads` | **s**tring → 对象 | 从 **s**tring 加载 |
| `dump` | 对象 → 文件 | 没有 s = 不进字符串，进文件 |
| `load` | 文件 → 对象 | 从文件加载 |

json 只认这几类（Python ↔ json 对照）：dict↔对象、list/tuple↔数组、str↔字符串、
int/float↔数字、True/False↔true/false、None↔null。集合不能存，元组存了会变数组
（读回来是列表）。

> 💡 Agent 世界里 json 无处不在：模型 API 的请求和响应、工具调用的参数，全是 json。这是本章最值得练熟的部分。

## 6.6 本章小结

- `input()` 永远返回字符串；`sep`/`end` 定制 print
- 文件三步 open → 操作 → close；`"w"` 会清空原文件
- **with 自动关闭文件，永远用它**；Windows 记得 `encoding="utf-8"`
- json 四兄弟：dumps/loads 走字符串，dump/load 走文件；s = string 记方向
- dumps 产物是"长得像 json 的字符串"（标本），loads 之后才是能操作的活数据

---

## ✍️ 动手运行

```bash
python ch06/01_print_input.py
python ch06/02_files.py
python ch06/03_with_json.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数，然后在**项目根目录**运行：

```bash
python -m ch06.test_exercises
```

## 🔗 官方文档深入阅读

- 更漂亮的打印：<https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#fancier-output-formatting>
- 读写文件：<https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files>
- json：<https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#saving-structured-data-with-json>
