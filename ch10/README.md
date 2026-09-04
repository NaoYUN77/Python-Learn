# ch10 标准库漫游 + 电池库大盘点

> 官方教程:[10. 标准库概览](https://docs.python.org/zh-cn/3/tutorial/stdlib.html) | [11. 标准库概览(续)](https://docs.python.org/zh-cn/3/tutorial/stdlib2.html)
> 运行示例(项目根目录):`python ch10/02_collections.py`

## 10.0 为什么要学这个

ch09 你拿到了"进入标准库的钥匙"(import 三姿势 + 模块对象),
本章用它去真正逛一逛这座**自带电池**的仓库:
不用安装、import 就能用,而且**质量比随手手写的高得多**。

漫游的心法只有三条:

1. **漫游不是背诵**——记住"标准库里大概有什么",忘了"怎么用"就查文档
2. **每到一个景点,先问连接**——它替你手写过哪个模式?(Counter ↔ ch05 计数)
3. **import 区三查铁律继续生效**——幽灵七连的账还挂着(9.7 的仪式)

本章路线图:五个标准库景点 → 第三方库盘点 → Agent 开发库盘点 → 迷你 Agent Loop。

| 景点 | 模块 | 一句话 | 和旧知识的连接 |
|------|------|--------|----------------|
| 工具带盘点 | 多个 | 你早就在用标准库了 | ch01–ch09 全部 |
| 计数与收集 | collections | 手写模式的一行版 | ch05 计数/收集模式 |
| 文件系统 | pathlib | 路径是对象,`/` 能拼路 | ch06 文件三步 |
| 随机世界 | random | 随机 ≠ 不可控,seed 是钥匙 | ch03 循环造数据 |
| 日期时间 + 统计 | datetime / statistics | 日期是对象;统计一行出数 | ch09 闰年题 |
| 正则入门 | re | 一行模式描述"长什么样的文本" | ch06 字符串处理 |
| 测速 | timeit | 别猜,要测 | ch05 集合的伏笔 |
| 第三方库 | pip 装的 | 自带电池之外的外接电池 | 本章新内容 |
| Agent 库 | AI SDK 概念体系 | Agent 开发的"水电煤"地图 | ch08 类、ch11 异步 |

## 10.1 开场:你早就在用标准库了(01)

`01_battery_check.py` 先盘一遍工具带:json、math、string、datetime、
collections、sys——**6 个老朋友**都现场演示一手。
再当场演示 sys.modules 记账本变厚( ch09 9.1 的知识落地)。

## 10.2 collections:你手写过的,它都写好了(02)

### Counter:ch05 计数模式的一行版

ch05 你手写:`counts[ch] = counts.get(ch, 0) + 1`。
标准库把这个模式直接做成了类:

```python
from collections import Counter
counts = Counter("abracadabra")
print(counts)                # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print(counts.most_common(2)) # [('a', 5), ('b', 2)] ← 次数从多到少的热词榜
print(counts["z"])           # 0 ← 缺键不炸!普通 dict 这里会 KeyError
```

三个细节:
- Counter 是 dict 的**子类**(ch08 的话术:"是一种" dict)
- `most_common(n)` 返回 `[(元素, 次数), ...]` 列表,已经按次数排好序
- 查不存在的键返回 0 而不是炸——为计数量身定做

### defaultdict:缺键自动建值的 dict

ch05 收集模式你手写:`groups.setdefault(w[0], []).append(w)`。
defaultdict 的思路:**先把"缺键时的默认值"设成规矩**,之后只管用:

```python
from collections import defaultdict
groups = defaultdict(list)      # 缺键 → 自动调 list() 造空列表
for w in ["apple", "banana", "avocado"]:
    groups[w[0]].append(w)      # 不用 setdefault 了,直接 append
print(dict(groups))             # {'a': ['apple', 'avocado'], 'b': ['banana']}
```

`defaultdict(list)` 读作"一个值默认是空列表的字典"——括号里放什么类型,
缺键就自动造什么,所以叫**缺键工厂**。

### deque:两头都能进出的队列(认个脸即可)

```python
from collections import deque
line = deque(["甲", "乙", "丙"])
line.append("丁")          # 队尾进
first = line.popleft()     # 队头出——瞬间完成
print(first, list(line))   # 甲 ['乙', '丙', '丁']
```

`list.pop(0)` 每次要把后面全部元素往前搬一遍;`popleft()` 不用。
排队、任务列表这类"先进先出"场景直接上 deque,用到再深究。
(预告:Agent 框架的"消息历史"经常就是 deque。)

### 对照表:手写模式 → 标准库一行版

| 你在 ch05 手写的 | 标准库一行版 |
|------------------|--------------|
| `counts[ch] = counts.get(ch, 0) + 1` | `Counter(data)` |
| `groups.setdefault(k, []).append(x)` | `defaultdict(list)` 后直接 append |

## 10.3 pathlib:路径从字符串变对象(03)

ch06 你用字符串拼路径、`open(path)` 开文件。pathlib 把路径变成**对象**:

```python
from pathlib import Path
me = Path(__file__)          # 本文件自己的路径(是个对象!)
print(me.name)               # 03_filesystem.py   ← 文件名
print(me.stem)               # 03_filesystem      ← 去掉扩展名
print(me.suffix)             # .py                ← 扩展名
print(me.parent)             # .../ch10           ← 所在文件夹
```

### `/` 运算符拼路径

```python
from pathlib import Path
here = Path(__file__).parent
box = here / "_temp_box"     # 用 / 拼路径!Windows 自动给 \,Mac/Linux 给 /
box.mkdir(exist_ok=True)     # exist_ok=True:已存在也不炸(不然 FileExistsError,ch07 老朋友)
print(box.exists())          # True
box.rmdir()                  # 只能删空文件夹
print(box.exists())          # False
```

### 按模式找文件:glob

```python
from pathlib import Path
here = Path(__file__).parent
for p in sorted(here.glob("*.py")):   # *.py = 所有 .py 文件(通配符,ch06 见过)
    print(p.name)
```

03 示例会真的列出本章全部 .py 文件——路径对象 + glob,一屏看全。

### read_text / write_text:小文件的便捷门

```python
from pathlib import Path
p = Path("笔记.txt")
p.write_text("你好,标准库!", encoding="utf-8")
print(p.read_text(encoding="utf-8"))    # 你好,标准库!
```

两行顶 ch06 的 open → 读写 → close。**小文件随手用;
大文件、要逐行处理的,仍走 with open**——别把便捷门当正门。

## 10.4 random:随机不等于不可控(04)

### 五件套

| 函数 | 干什么 | 注意 |
|------|--------|------|
| `randint(a, b)` | a~b 随机整数 | **两端都含!**和 range(含头不含尾)正好相反 |
| `choice(seq)` | 随机挑一个 | 空序列 → IndexError |
| `sample(seq, k)` | 抽 k 个,不重复 | **不动原件**,返回新列表 |
| `shuffle(seq)` | 原地打乱 | **返回 None**(sort 同族坑!),要结果用 sample |
| `random()` | [0, 1) 随机小数 | 概率模拟的原料 |

`randint(1, 6)` 想要 1~6 就写 1 和 6,**含头也含尾**——
新手第一大坑:和 range 记反了,写成 `randint(1, 5)` 会永远掷不出 6。
边界条件,盯紧。

### seed:让"随机"可复现

```python
import random
random.seed(42)                              # 定住随机源
a = [random.randint(1, 6) for _ in range(3)]
random.seed(42)                              # 再定一次
b = [random.randint(1, 6) for _ in range(3)]
print(a, b)      # 两次完全一样!同一种子 → 同一序列
```

**同一种子 → 同一序列**。这把钥匙解决两个大问题:

- 测试:测试里 seed 一下,随机函数的结果就能断言了(练习 3 就这么测)
- 调试:bug 在随机场景出现,seed 定住现场,一步一步复现

## 10.5 datetime:日期是对象,能加减能比较(05)

三兄弟:

| 类型 | 装 what | 例 |
|------|---------|-----|
| `date` | 年月日 | `date(2026, 9, 4)` |
| `datetime` | 年月日 + 时分秒 | `datetime.now()` |
| `timedelta` | 时间差 | `timedelta(days=100)` |

### 相减得差,相加得新

```python
from datetime import date, timedelta
today = date.today()
new_year = date(2027, 1, 1)
gap = new_year - today                # date − date → timedelta
print(gap.days)                       # 距 2027 元旦多少天
print(today + timedelta(days=100))    # 100 天后是哪天
```

ch09 的闰年题(date 相减算天数)你已经用过一次——当时是尝鲜,现在正式学。

### 方向题:strftime 出,strptime 进

和 json 四兄弟同一个方向梗(dump 出 / load 进):

| 函数 | 方向 | 原料 → 产物 |
|------|------|-------------|
| `d.strftime("%Y-%m-%d")` | **日期 → 字符串**(format,出去给人看) | date → "2026-09-04" |
| `datetime.strptime(s, "%Y-%m-%d")` | **字符串 → 日期**(parse,进来做计算) | "2026-09-04" → date |

常用格式码:`%Y` 四位年、`%m` 两位月、`%d` 两位日、`%H:%M` 时:分。
**自动补零**:`strftime("%m")` 给 9 月出 "09"——ch06 的"补零位数=下限"这里免费送。

### statistics:一行出统计

```python
import statistics
scores = [88, 92, 79, 93, 85]
statistics.mean(scores)      # 87.4   平均
statistics.median(scores)    # 88     中位数(偶数个取中间两数的平均)
statistics.mode(scores)      # 众数
statistics.stdev(scores)     # 标准差(波动多大)
```

为什么不手写?**边界处理人家都文档化了**:空列表直接抛
`StatisticsError`(ch07:标准库也按型号抛异常,文档的 Raises 段
就是危险行清单)——手写的话,这些坑得自己踩一遍。

## 10.6 re:正则三板斧(06)

正则 = 用**一行模式**描述"长什么样的文本"。
文本清洗、日志提取、格式校验,全是它的主场(Agent 处理 LLM 输出也常用)。

先懂 `r""`:原始字符串。`"\t"` 是真制表符,`r"\t"` 是反斜杠+t 两个字符——
**写正则一律加 r 前缀**,别让 Python 先吃掉反斜杠。

| 板斧 | 干什么 | 返回 |
|------|--------|------|
| `re.findall(r"\d+", s)` | 找出**所有**匹配 | 字符串列表 |
| `re.search(r"\d+", s)` | 找**第一个**匹配 | 匹配对象(`.group()` 取文本);找不到 → None |
| `re.sub(r"\d", "*", s)` | **全部替换** | 新字符串 |

常用符号:`\d` 数字、`\w` 单词字符(字母数字下划线)、`\s` 空白、`.` 任意字符、`+` 一个或多个。

```python
import re
order = "订单 1001 和 1002,共 2 件,实付 88.5 元"
re.findall(r"\d+", order)   # ['1001', '1002', '2', '88', '5'] ← 字符串!要数字自己 int()
re.sub(r"\d", "*", order)   # 订单 **** 和 ****,共 * 件,实付 **.* 元
```

注意 findall 给的是**字符串列表**——要数字自己 `int()` 转换
(input 永远 str,同款道理)。

## 10.7 timeit:别猜,要测(07)

问题:查"9999 在不在 10000 个数里",列表和集合谁快?

```python
import timeit
xs = list(range(10000))
ss = set(xs)
t_list = timeit.timeit(lambda: 9999 in xs, number=1000)
t_set  = timeit.timeit(lambda: 9999 in ss, number=1000)
```

实测集合快上千倍:列表查成员 = 从头扫到尾;集合 = 哈希表直查
(ch05 埋的伏笔在此收线)。**用法观:先跑通,再谈快;要谈快,先 timeit。**

## 10.8 第三方库:pip 装的外接电池(08)

标准库管"通用弹药",第三方库管"专业装备"——`pip install 库名` 装进
site-packages,import 规则和 ch09 一模一样。本节是**盘点认脸**,
用到哪个装哪个;`08_py_libraries.py` 装了的真跑一手、没装的友好提示,
**全没装也能跑通**。

### 网络请求

| 库 | 一句话 | 为什么学 |
|----|--------|----------|
| `requests` | HTTP 请求事实标准:`requests.get(url)` 一行拿网页 | 爬虫/调 API 的入门第一站 |
| `httpx` | requests 的现代继任者,**原生支持 async** | Agent 框架的底层常客,ch11 会用 |

```python
import requests
r = requests.get("https://api.github.com", timeout=10)
print(r.status_code)   # 200
print(r.json())        # JSON 响应直接变 dict——ch06 的 json.load 思路
```

### 数据验证:pydantic(Agent 开发刚需)

用**类**给数据立规矩(ch08 的类,加上自动类型转换和校验):

```python
from pydantic import BaseModel

class City(BaseModel):
    name: str
    population: int      # 声明类型,pydantic 替你把守

c = City(name="杭州", population="1200")   # "1200" 自动转成 int!
City(name="杭州", population="很多")        # → ValidationError,当场挡下
```

LLM 返回的 JSON 结构对不对,靠它把关——Agent 开发里它无处不在。

### 开发体验与工程配套

| 库 | 一句话 |
|----|--------|
| `rich` | 终端排版师:彩色/表格/进度条,调试输出立刻清爽 |
| `python-dotenv` | 配置进 `.env` 文件不进代码:`load_dotenv()` + `os.getenv('API_KEY')` |
| `openpyxl` | 直接读写 .xlsx 表格 |

### 数据三件套(只报到,用到再学)

| 库 | 一句话 |
|----|--------|
| `numpy` | 多维数组与数值计算,pandas 的地基 |
| `pandas` | 表格数据 DataFrame,Excel 杀手 |
| `matplotlib` | 画图:折线/柱状/散点一行出图 |

### 更多常用库速查(知道有这号人即可)

| 库 | 干什么 |
|----|--------|
| `flask` / `fastapi` | 写 Web 服务/HTTP API(fastapi 原生 async + 自带 pydantic) |
| `click` / `typer` | 写命令行工具(参数解析不用手撸 sys.argv) |
| `openpyxl` 之外:`python-docx`、`pypdf` | Word / PDF 文件处理 |
| `pillow` | 图片处理(缩放/裁剪/格式转换) |
| `pytest` | 更强的测试框架(本项目的轻量 runner 升级版) |
| `loguru` | 日志:print 的正经继任者 |

### 装库三律

1. 装法:`pip install 库名`(终端里跑,不是 Python 代码里)
2. **密钥永远不进代码库**——.env + python-dotenv,第一课就守规矩
3. 装之前先 pip list 看看是不是已经有了

## 10.9 Agent 开发常用库:概念地图(09)

> 主要参照 [Vercel AI SDK](https://ai-sdk.dev/docs/introduction) 的概念体系
> (统一 Provider、Tool Calling、Structured Data、Streaming、Agent Loop、
> Memory、Subagent),对应到 Python 生态的各家库。
> 本节先**认脸**;`09_agent_libraries.py` 用纯标准库搭了个 30 行迷你 Agent Loop,
> 装任何框架之前先把那个跑通——所有框架的内核都是它。

### 先建立概念词表(框架文档里的词,提前认识)

| AI SDK 概念 | 一句话 | Python 侧对应 |
|-------------|--------|---------------|
| Provider / 统一模型接口 | 换模型只换一个参数 | openai / anthropic / litellm 等 SDK |
| Tool Calling | 给模型一排工具,它点名"调哪个+参数" | 各框架的 tools/tool 参数 |
| Structured Data | 让模型输出带类型校验的结构化 JSON | pydantic 模型 |
| Agent Loop | 模型↔工具循环直到给出最终回答 | 框架的 agent 核心循环 |
| Loop Control | 循环上限/停止条件,防无限调工具 | max_steps / max_turns |
| Memory | 对话历史与状态管理 | messages 列表 / 框架的 memory |
| Streaming | 一边生成一边输出 | `stream=True` / async 迭代 |
| Subagent / Handoff | 主代理把任务转交子代理 | openai-agents 的 handoffs |
| MCP | 工具接入的开放标准,"AI 界的 USB-C" | `mcp` 包 |

### 第一梯队:模型接口层(怎么跟 LLM 说话)

| 库 | 一句话 |
|----|--------|
| `openai` | OpenAI 官方 SDK;**很多国产模型都提供 OpenAI 兼容接口**,学会一个通吃一片 |
| `anthropic` | Claude 官方 SDK |
| `zai-sdk` | 智谱 GLM 官方 SDK |
| `google-genai` | Google Gemini 官方 SDK |
| `litellm` | 一个接口调 100+ 家模型,统一成 OpenAI 格式 |

共同点:你写 prompt,它管 HTTP、重试、流式;换模型只换一个参数。

### 第二梯队:编排框架层(把模型/工具/记忆拼成 Agent)

| 库 | 一句话 | 适合 |
|----|--------|------|
| `langchain` | 最老牌的 LLM 工具箱:组件多、集成全 | 快速原型、接各种现成集成 |
| `langgraph` | LangChain 家的**有状态流程图**:循环/分支/人工审批 | 复杂、可控的 Agent 工作流(当前主流) |
| `openai-agents` | OpenAI 出的轻量框架:handoffs + guardrails | 想要官方出品、抽象少 |
| `crewai` | 角色扮演式多智能体:定角色/目标,组队干活 | "一个团队"式的多 Agent 协作 |
| `autogen` | 微软出品:多 Agent 对话式协作(并入 Microsoft Agent 框架) | 研究型/对话式多 Agent |
| `pydantic-ai` | 类型安全的 Agent 框架(pydantic 作者出品) | 喜欢强类型、显式数据流 |

**怎么选**:第一个 Agent 用官方 SDK + pydantic 手搭(理解内核);
要复杂流程上 langgraph;要多角色协作看 crewai/autogen;
喜欢强类型看 pydantic-ai。框架选型远不如吃透 Agent Loop 重要——**内核都会了,框架只是加料**。

### 第三梯队:支撑件层(Agent 周边的水电煤)

| 库 | 一句话 |
|----|--------|
| `mcp` | Model Context Protocol:Anthropic 开的工具接入标准,一次接入处处可用 |
| `pydantic` | 结构化输出把关:LLM 吐的 JSON 合不合格,它说了算 |
| `httpx` | 异步 HTTP:所有 SDK 调 API 的底层常客 |
| `tiktoken` | 数 token:上下文窗口花了多少,心里有数 |
| `rich` | Agent 的思考过程打印出来好看又好读 |
| `python-dotenv` | 密钥进 .env 不进代码 |
| `chromadb` / `faiss` | 向量数据库:记忆检索(RAG)的仓库 |

### 迷你 Agent Loop:30 行看穿所有框架(09 示例核心)

```python
def agent_loop(user_text, max_steps=3):
    history = [{"user": user_text}]               # 记忆
    for step in range(max_steps):                 # 循环上限=安全带
        decision = fake_llm(history)              # ① 问模型(真项目=API 调用)
        if "reply" in decision:                   # ② 模型给最终回答 → 收工
            return decision["reply"]
        result = get_weather(**decision["args"])  # ③ 执行模型点名的工具
        history.append({"tool": decision["tool"],
                        "tool_result": result})   # ④ 结果记进记忆,喂回模型
    return "(步数用尽,强制收工)"
```

四步循环:**问模型 → (它要工具就执行) → 结果进记忆 → 再问模型**,
直到模型给出最终回答。LangGraph/CrewAI/pydantic-ai 都在给这个循环加料:
加状态图、加多角色、加类型校验、加人工审批——**内核不变**。

### 学习路线(下一步)

1. **ch11 的 asyncio**:真实框架里 API 调用全是 async 的——先修课
2. 挑一个官方 SDK(`openai` / `zai-sdk`)跑通第一句对话(要 API key)
3. 用 pydantic 给"LLM 返回的 JSON"立规矩(结构化输出)
4. 手搭 Agent Loop(09 示例已是完整骨架),再回头看框架文档——每个词都认识

## 10.10 漫游地图:下一批标准库景点(自学预告)

| 模块 | 一句话 | 什么时候去 |
|------|--------|------------|
| `itertools` | 迭代器乐高(排列/组合/无限流) | 玩数据管道时 |
| `shutil` | 文件手术刀(复制/移动/删文件夹树) | 想批量操作文件时 |
| `zipfile` | 压缩包读写 | 打包文件时 |
| `hashlib` | 文件指纹(哈希) | 想校验"内容没被改过"时 |
| `pprint` | 打印美化师 | dict 印出来太乱时 |
| `os` | pathlib 的老前辈 | 读老代码遇到 os.path 时 |
| `json` | ch06 老朋友 | 存结构化数据时 |
| `functools` | lru_cache 等:给函数加 buff | 想缓存函数结果时 |

漫游的终点不是"全逛完",是养成条件反射:
**这活儿,标准库是不是已经有了?**

## 10.11 小结与自测

一句话:**标准库 = 自带电池,第三方库 = pip 外接电池,Agent 库 = 拼电池的手艺;
Counter/defaultdict 替你写完 ch05 的计数/收集;seed 让随机可复现;
路径是对象(. 取属性,/ 拼路);日期是对象(相减得 timedelta);
strftime 出、strptime 进;正则三板斧 findall/search/sub;别猜要测先 timeit;
pydantic 给数据立规矩;Agent = 问模型→调工具→结果进记忆→再问,循环到答。**

自测八问(合上文件先复述,再翻回对照):

1. Counter 替你写完了 ch05 的哪个模式?`most_common(2)` 返回什么结构?(10.2)
2. `random.randint(1, 6)` 和 `range(1, 7)`:谁两端都含,谁含头不含尾?(10.4)
3. shuffle 和 sample,谁动原件?谁的返回值能用?(10.4)
4. 两个 date 相减得到什么?strftime 和 strptime,哪个是日期→字符串?(10.5)
5. `re.findall(r"\d+", s)` 返回的列表里是数字还是字符串?(10.6)
6. requests / httpx 的分工是什么?为什么说 httpx 是 ch11 的伏笔?(10.8)
7. pydantic 的 `BaseModel` 替你把守什么?为什么它是 Agent 开发刚需?(10.8)
8. 说出迷你 Agent Loop 的四步循环;max_steps 防的是什么?(10.9)

## 动手运行

```bash
python ch10/01_battery_check.py        # 工具带盘点 + sys.modules 记账现场
python ch10/02_collections.py
python ch10/03_filesystem.py           # 会真的列出本章全部 .py 文件
python ch10/04_random_playground.py    # 上半段每次输出不同(seed 段除外)——这不是 bug
python ch10/05_datetime_stats.py
python ch10/06_regex_intro.py
python ch10/07_timeit_race.py          # 数字每次会变,量级不会
python ch10/08_py_libraries.py         # 装了就真跑一手,没装也跑得通
python ch10/09_agent_libraries.py      # 零依赖!迷你 Agent Loop 直接跑
```

## 练习

`exercises.py` 共 7 题。**import 区继续由你自己建**(ch09 规矩)——
骨架里一行 import 都没有,每题 TODO 都标了需要什么模块。
交卷前扫 import 区三查(9.7 的仪式)。

做完在项目根目录运行:

```bash
python -m ch10.test_exercises
```
