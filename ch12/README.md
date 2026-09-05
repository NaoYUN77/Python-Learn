# ch12 Agent 开发入门:pydantic 打底,pydantic-ai 上手

> 主要参照:[Vercel AI SDK](https://ai-sdk.dev/docs/agents/overview)(概念体系)·
> [Pydantic AI 官方文档](https://pydantic.dev/docs/ai/core-concepts/agent/)(Python 实现)
> 运行示例(项目根目录):`python ch12/01_agent_loop.py`(零依赖零 key,直接跑)

## 12.0 为什么要学这个

这就是整个课程的终点站:ch08 的类、ch09 的模块拼装、ch10 的异步、
ch11 的电池库——全在这里合流。

Agent 开发的第一性原理只有一句话
([AI SDK 的定义](https://ai-sdk.dev/docs/agents/overview)):

> **Agent = LLM 在循环里使用工具完成任务。**

拆开是三个词:

| 组件 | 一句话 | 在哪里学过 |
|------|--------|------------|
| LLM | 理解输入、决定下一步动作的"大脑" | ——(本章接口层) |
| Tools | 超出"会说话"的能力:读文件、查库、调 API | ch06 文件 / ch11 requests |
| Loop | 上下文管理 + 停止条件,编排整个执行 | ch03 循环 / ch07 防御 |

而 pydantic-ai 官方文档对 Agent 的说法是:**Agent 是一个容器**,装着——

| 容器内容 | 干什么 | 对应 AI SDK 概念 |
|----------|--------|------------------|
| `instructions` | 开发者写给 LLM 的说明书(怎么干) | System Prompt / Instructions |
| `tools` | LLM 可以调的函数(能干什么) | Tool Calling |
| `output_type` | 交差格式:最终输出的类型约束 | Structured Output |
| `deps_type` | 运行时依赖注入(API key、数据库连接) | Runtime Context |
| `model` | 默认用哪个 LLM | Provider |

本章路线:**手搓最小 loop(01)→ pydantic 立规矩(02)→ pydantic-ai 上手(03)
→ 全景地图(04)→ 框架选型(12.6)**。

## 12.1 先建立概念词表(读任何框架文档都不迷路)

各家框架的文档术语已经高度收敛(互抄……借鉴),先认全:

| 概念 | 一句话 | Python 侧对应 |
|------|--------|---------------|
| Provider / 统一模型接口 | 换模型只换一个参数 | `openai:` `anthropic:` 前缀 / litellm |
| Tool Calling | 给模型一排工具,它点名"调哪个+参数" | `@agent.tool` |
| Structured Output | 让模型输出带类型校验的 JSON | pydantic `output_type` |
| Agent Loop | 模型↔工具循环直到给出最终回答 | 框架核心;01 示例手搓版 |
| Loop Control | 循环上限/停止条件,防无限调工具 | `max_steps` / UsageLimits |
| Memory | 对话历史管理,多轮对话不失忆 | `message_history` |
| Streaming | 一边生成一边输出(打字机效果) | `async for`(ch10 的异步!) |
| Subagent | 主代理把任务外包给专职子代理 | handoffs / delegation |
| MCP | 工具接入的开放标准,"AI 界的 USB-C" | `mcp` 包 |

**为什么这些概念值得先认?** 因为框架文档(无论哪家)默认你已经认识它们。
先认词,再读文档,效率差十倍。

## 12.2 手搓最小 Agent Loop(01)——本章的重头戏

`01_agent_loop.py` 用纯标准库分四步搭出完整循环,**零依赖零 key 直接跑**。
这里按步骤拆解,建议边跑边对照。

### 第 1 步:纯对话——模型的局限

```python
history = [{"user": "Python 好学吗?"}]
reply = fake_llm(history)["reply"]      # 一次调用,一问一答
```

没有工具,模型只能凭"嘴"回答。你问它天气,它只能编——
**它够不着外部世界**。这就是为什么需要工具。

### 第 2 步:Tool Calling——模型点单,我们掌勺

```python
decision = fake_llm(history)            # {"tool": "get_weather", "args": {"city": "杭州"}}
tool = TOOLS[decision["tool"]]          # 按名找工具
result = tool["run"](**decision["args"])  # ** 解包参数(ch04!)再执行
```

最关键的一行认知:

> **模型自己【不执行】任何东西。** 它只输出"点名+参数"的 JSON;
> 执行永远发生在你的代码里。

这就是 Agent 安全模型的根基:危险操作过不过,闸门在你手上
(ch07 的"入口最危险越往里越安全"在这里反过来用——工具就是入口)。

### 第 3 步:Agent Loop——工具结果必须喂回去

```python
def agent_loop(user_text, max_steps=3):
    history = [{"user": user_text}]        # 记忆(Memory)
    for step in range(max_steps):          # 停止条件(Loop Control)
        decision = fake_llm(history)       # ① 问模型(history 全量给它)
        if "reply" in decision:            # ② 最终回答 → 收工
            return decision["reply"], history
        result = run_tool(decision)        # ③ 执行它点名的工具
        history.append({"tool_result": result})  # ④ 结果进记忆,喂回模型
    return "(步数用尽)", history
```

四步循环:**问模型 →(它要工具就执行)→ 结果进记忆 → 再问模型**。

两个新手必懂的细节:

1. **history 是模型的眼睛**。工具结果 append 进去后,下一轮模型才"看见"。
   忘了 append,模型会无限重复要同一个工具——这是手搓 Agent 的头号 bug。
2. **max_steps 是安全带**。AI SDK 默认 `isStepCount(20)`;
   pydantic-ai 用 `UsageLimits(request_limit=3)`。
   没有它,模型陷入循环就是无限烧钱(ch03 的循环 + ch07 的防御,在这里合体)。

### 第 4 步:逐帧跟踪

01 的输出带跟踪表——**history 的成长史**就是 Agent 的思考史:

```
[0] user         杭州天气怎么样?
[1] get_weather  {'city': '杭州', 'weather': '晴', 'temp': 28}
```

调试 Agent 的第一功夫:把 history 打出来看。
(pydantic-ai 里对应 `result.all_messages()`,或接 Logfire 看可视化 trace。)

### 真框架在给这个循环加什么料?

| 加料 | 代表 | 一句话 |
|------|------|--------|
| 类型校验 | pydantic-ai | 工具参数、输出格式自动验证,不合格自动让模型重试 |
| 状态图 | LangGraph | 循环升级成可画出来的流程图,支持分支/人工审批 |
| 多角色 | CrewAI | 多个 Agent 各带人设组队 |
| 子代理 | openai-agents | 主代理把任务 handoff 给专职 Agent |
| 并发 | asyncio 全家 | 多工具/多 Agent 并行跑(ch10 的主场) |

**内核不变。** 这就是先手搓再上框架的原因。

## 12.3 pydantic 打底(02)——先学会"立规矩"

`pip install pydantic` 后跑 `python ch12/02_pydantic_basics.py`。

Agent 开发里 LLM 的输出本质是"自由文本"——结构对不对、类型对不对,
没人把关就是裸奔。pydantic 的 `BaseModel` 用**声明类型**的方式把守:

```python
from pydantic import BaseModel, Field

class City(BaseModel):
    name: str
    population: int          # 声明类型,pydantic 替你把守

c = City(name="杭州", population="1200")   # "1200" 自动转成 int(宽松转型)
City(name="杭州", population="很多")        # → ValidationError,当场拦下
```

四个必会点(02 示例逐个演示):

1. **自动转型**:能转就转(`"1200"` → `1200`),转不动才报错
2. **Field 约束**:`score: int = Field(ge=0, le=100)`——范围卡死,
   **两端都含**(ch07 边界条件教训的官方版)
3. **嵌套模型**:`ingredients: list[Ingredient]`——字典列表自动变成对象列表,
   ch05 容器 + ch08 类的合体
4. **ValidationError 逐字段报错**:`e.errors()` 给出哪个字段、什么问题——
   比 `try/except Exception` 精确得多(ch07:按型号接)

一句话:**LLM 输出 → pydantic 验证 → 类型安全的对象**。
这个句式会贯穿你整个 Agent 开发生涯。

## 12.4 pydantic-ai 上手(03)——第一个真 Agent

> 官方文档:[pydantic.dev/docs/ai](https://pydantic.dev/docs/ai/core-concepts/agent/) ·
> 安装:`pip install pydantic-ai`
> 选它的理由:pydantic 官方出品、类型安全贯穿始终、抽象少、
> 和你已学的 pydantic/ch10 异步无缝衔接。

### 跑前准备(两步)

```
pip install pydantic-ai
```

配一个模型的 API key(放进环境变量或 `.env`,**别写进代码**):

```
OPENAI_API_KEY=...        # OpenAI
ZAI_API_KEY=...           # 智谱 GLM(国内推荐)
ANTHROPIC_API_KEY=...     # Claude
```

没配 key 时 03 会给友好指引而不是裸 Traceback——代码照常可读。

### 场景 1:最裸的 Agent(三行)

```python
from pydantic_ai import Agent

agent = Agent("openai:gpt-4o-mini", instructions="用一句话回答")
result = agent.run_sync("什么是 Agent?")
print(result.output)      # 注意:取 .output,不是 result 本身
```

对照 01 的手搓版:`Agent(...)` = 备好大脑+说明书;
`run_sync()` = 01 的 for 循环整体跑完;`result.output` = 最终回答。

### 场景 2:Tool Calling——给模型发工具

```python
from pydantic_ai.tools import RunContext

agent = Agent("openai:gpt-4o-mini", instructions="回答前先查工具拿实时数据")

@agent.tool
def get_weather(ctx: RunContext, city: str) -> dict:
    """查询某城市当前天气"""
    return {"city": city, "weather": "晴", "temp": 28}

result = agent.run_sync("杭州现在穿什么合适?")
```

三个魔法全部来自你已经学的东西:

1. **参数类型注解 + docstring** → 自动变成给模型看的"工具说明书"
   (模型靠它决定什么时候调、传什么参数——说明书写得越清楚,模型用得越准)
2. **`@agent.tool`** → 注册进 Agent 的工具箱(装饰器 = 函数当参数,ch04)
3. **循环框架替你转了**:模型点名 → pydantic-ai 执行 → 结果喂回 → 再问模型,
   就是 01 的 ①~④,一行没让你写

### 场景 3:Structured Output——输出直接是对象

```python
from pydantic import BaseModel, Field

class MovieReview(BaseModel):
    title: str
    score: int = Field(ge=0, le=10)
    recommend: bool

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="你是影评人,打分要毒舌但公正",
    output_type=MovieReview,          # ★ 交差格式声明在先
)
result = agent.run_sync("评价一下《流浪地球2》")
review = result.output                # 已经是 MovieReview 实例!
```

`output_type` 一旦声明,pydantic-ai 会在内部:

- 把 schema 发给模型(告诉它"照这个格式交差")
- 收到输出后自动验证;**不合格会带着报错让模型重试**
  (官方叫 Reflection and self-correction,默认重试 1 次,可调)

你拿到手的永远是类型安全的对象——`review.score` 一定是 0~10 的 int。
这就是 12.3 那个句式的框架版:**LLM 输出 → 自动验证 → 类型安全的对象**。

### 五种跑法(按需选用)

| 方法 | 场景 | 备注 |
|------|------|------|
| `agent.run_sync()` | 脚本/学习 | 同步阻塞,最简单 |
| `await agent.run()` | 异步应用 | ch10 的 asyncio 正式上岗 |
| `agent.run_stream()` | 聊天界面 | 流式输出(打字机效果) |
| `agent.iter()` | 要逐步观察 | 逐节点遍历内部图,调试神器 |
| `message_history=` | 多轮对话 | 把上次的消息传进去,模型才记得上文 |

### 多轮对话:Memory 不神秘

```python
r1 = agent.run_sync("爱因斯坦是谁?")
r2 = agent.run_sync("他最著名的公式是什么?", message_history=r1.new_messages())
```

没有 `message_history`,第二问的"他"模型根本不知道指谁。
**Memory = 把上一次的消息列表传进下一次**——本质就是 01 里那个 history 列表,
框架只是帮你存取。

### 两个工程必备件(现在知道,用到再深)

- **UsageLimits(预算闸门)**:`UsageLimits(request_limit=3)` 限制请求次数、
  `cost_limit` 限制花费——01 的 `max_steps` 官方版
- **ModelRetry(让模型自我修正)**:工具里 `raise ModelRetry('请给全名')`
  = 不算失败,而是把提示喂回模型重试(默认重试 1 次,`@agent.tool(retries=2)` 可调)

## 12.5 支撑件与生态(04 示例认脸)

`04_concept_map.py` 是零依赖的全景清单,三梯队:

**模型接口层**(换模型只换一个参数):`openai` / `anthropic` / `zai-sdk`(智谱 GLM)/
`google-genai` / `litellm`(一个接口调 100+ 家)

**编排框架层**(见 12.6 选型)

**支撑件层**:

| 库 | 一句话 |
|----|--------|
| `mcp` | Model Context Protocol:工具接入的开放标准,一次接入处处可用 |
| `pydantic` | 结构化输出把关(12.3 已上手) |
| `httpx` | 异步 HTTP:所有 SDK 的底层常客(ch10 的 async 正好用上) |
| `python-dotenv` | 密钥进 .env 不进代码 |
| `tiktoken` | 数 token:上下文窗口花了多少,心里有数 |
| `rich` | Agent 思考过程打印好看又好读 |
| `chromadb` / `faiss` | 向量数据库:记忆检索(RAG)的仓库 |

## 12.6 框架选型:什么时候用什么

| 框架 | 一句话 | 什么时候用它 |
|------|--------|--------------|
| **pydantic-ai** | 类型安全、抽象少,pydantic 官方出品 | ★ 第一个框架;喜欢强类型 |
| langchain | 组件最多、集成最全 | 快速原型、要接各种现成服务 |
| langgraph | 有状态流程图:循环/分支/人工审批 | 复杂、可控的生产级工作流(当前主流) |
| openai-agents | OpenAI 官方轻量框架:handoffs + guardrails | 想要官方出品、要多 Agent 交接 |
| crewai | 角色扮演式多智能体 | "一个团队"式协作场景 |
| autogen | 微软出品,多 Agent 对话式协作 | 研究型/对话式多 Agent |

**选型心法**:

1. 第一个 Agent:官方 SDK(或 pydantic-ai)+ 手搓 loop 的理解——**先内核后框架**
2. 要复杂流程(审批、分支、状态回滚)→ langgraph
3. 要多角色协作 → crewai / openai-agents(handoffs)
4. 纠结时记住:框架选型远不如吃透 Agent Loop 重要。
   **内核都会了,框架只是加料;内核不懂,换什么框架都是裸奔。**

## 12.7 小项目练手(自选难度)

- ⭐ **改 01**:给 TOOLS 加一个 `get_time` 工具,问"现在几点"能答上来
  (fake_llm 的剧本也要加一行)
- ⭐⭐ **改 02**:给 MovieReview 加 `reason: str` 字段和长度约束
- ⭐⭐ **手搓结构化输出**:01 的 `{"reply": ...}` 换成"必须符合某 pydantic 模型",
  不合格打印报错(= 提前手动实现 03 场景 3)
- ⭐⭐⭐ **配 key 后跑 03**:三个场景各跑一遍,再给 get_weather 加第二个城市参数
- ⭐⭐⭐⭐ **手搓多轮对话**:01 加一个 while True 循环,history 跨轮保留
  (= 提前手动实现 `message_history`)

## 12.8 小结与自测

一句话:**Agent = LLM + 工具 + 循环;
模型只点名不执行(安全根基);工具结果必须进 history 喂回模型(否则无限循环);
max_steps/UsageLimits 是防烧钱的安全带;
pydantic 立规矩(类型/范围/嵌套,ValidationError 逐字段报);
pydantic-ai 三件套:@agent.tool(类型注解+docstring 即说明书)、
output_type(输出即对象,不合格自动重试)、message_history(多轮记忆);
框架只是给内核加料——先内核后框架。**

自测八问(合上文件先复述,再翻回对照):

1. Agent 的第一性定义是什么?三大件各管什么?(12.0)
2. 为什么说"执行永远发生在你的代码里"是 Agent 安全模型的根基?(12.2)
3. 手搓 loop 忘了把工具结果 append 进 history,会发生什么?为什么?(12.2)
4. `Field(ge=0, le=100)` 的范围含头含尾吗?哪个 ch07 教训在这里官方化?(12.3)
5. `@agent.tool` 装饰的函数,模型靠什么知道"什么时候调、传什么"?(12.4)
6. `output_type` 声明后,模型输出不合格会发生什么?(12.4)
7. 多轮对话为什么必须传 `message_history`?它的本质是什么?(12.4)
8. 你想做一个"每天自动整理错题本的 Agent",会选哪个框架?为什么?(12.6)

## 动手运行

```bash
python ch12/01_agent_loop.py        # 零依赖零 key!四步渐进 + 跟踪表
python ch12/02_pydantic_basics.py   # 需要:pip install pydantic
python ch12/03_pydantic_ai_intro.py # 需要:pip install pydantic-ai + API key
python ch12/04_concept_map.py       # 零依赖,全景清单 + 概念对照表
```

## 练习

`exercises.py` 共 7 题,只用 pydantic(**不需要 API key**):
从"第一个模型"到"结构化输出模拟",把 12.3 的句式练进肌肉记忆。

```bash
python -m ch12.test_exercises   # 项目根目录运行(pip install pydantic 后)
```

学完本章,课程主线毕业 🎓。下一步自选:
加深异步(ch10 进阶)→ 深入某个框架(langgraph 文档)→
或直接开写你的第一个真实 Agent(12.7 的 ⭐⭐⭐⭐⭐)。
