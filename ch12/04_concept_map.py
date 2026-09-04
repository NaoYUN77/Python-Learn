"""04_concept_map.py — Agent 库全景地图:先认脸,再动手。

运行:python ch12/04_concept_map.py
参照 Vercel AI SDK(https://ai-sdk.dev)的概念体系,对应到 Python 生态。
骨架零依赖,直接能跑;本章主角 pydantic / pydantic-ai 在 README 12.3/12.4 详讲。
"""

print("=== Agent 开发常用库:先认脸,再动手 ===\n")

# ── 第一梯队:模型接口层("怎么跟 LLM 说话") ──
print("[模型接口层] 统一各家 LLM 的调用方式——AI SDK 称它 Provider")
for name, why in [
    ("openai",      "OpenAI 官方 SDK;很多国产模型都提供 OpenAI 兼容接口"),
    ("anthropic",   "Claude 官方 SDK"),
    ("zai-sdk",     "智谱 GLM 官方 SDK"),
    ("google-genai","Google Gemini 官方 SDK"),
    ("litellm",     "一个接口调所有家:100+ 模型统一成 OpenAI 格式"),
]:
    print(f"    • {name:<14} {why}")
print("    → 共同点:你写 prompt,它管 HTTP、重试、流式;换模型只换一个参数")

# ── 第二梯队:编排框架层("怎么把模型、工具、记忆拼成 Agent") ──
print("\n[编排框架层] AI SDK 里的 Agent / Workflow Patterns,Python 这边对应:")
for name, why in [
    ("pydantic-ai",  "★ 本章主角:类型安全的 Agent 框架(pydantic 官方出品)"),
    ("langchain",    "最老牌的 LLM 应用工具箱:组件多、集成全,原型最快"),
    ("langgraph",    "LangChain 家的'有状态流程图':循环/分支/人工审批,复杂 Agent 首选"),
    ("openai-agents","OpenAI 出的轻量框架:handoffs(子代理交接)+ guardrails"),
    ("crewai",       "角色扮演式多智能体:给每个 Agent 定角色/目标,组队干活"),
    ("autogen",      "微软出品:多 Agent 对话式协作(现已并入 Microsoft Agent 框架)"),
]:
    print(f"    • {name:<15} {why}")

# ── 第三梯队:支撑件层("Agent 周边的水电煤") ──
print("\n[支撑件层]")
for name, why in [
    ("pydantic",      "★ 本章主角:结构化输出把关,LLM 吐的 JSON 合不合格它说了算"),
    ("mcp",           "Model Context Protocol:工具接入的开放标准,'AI 界的 USB-C'"),
    ("httpx",         "异步 HTTP:所有 SDK 调 API 的底层常客(ch10 的 async 正好用上)"),
    ("python-dotenv", "密钥进 .env 不进代码"),
    ("rich",          "Agent 的思考过程打印出来好看又好读"),
    ("tiktoken",      "数 token:上下文窗口花了多少,心里有数"),
    ("chromadb",      "向量数据库:记忆检索(RAG)的仓库"),
]:
    print(f"    • {name:<15} {why}")

print("\n=== AI SDK 概念 ↔ Python 库 对照表 ===")
for concept, py_side in [
    ("Provider / 统一模型接口", "openai / litellm 等官方 SDK"),
    ("Tool Calling(模型点名调工具)", "各框架的 @tool / tools 参数"),
    ("Structured Data(结构化输出)", "pydantic 的 BaseModel / output_type"),
    ("Agent Loop(模型↔工具循环)", "框架核心;01 示例 30 行手搓版"),
    ("Loop Control(停止条件)", "max_steps / AI SDK 的 stopWhen"),
    ("Memory(记忆)", "messages 列表 / deque / 专门的记忆服务"),
    ("Streaming(流式输出)", "async for 迭代文本块(ch10 的异步)"),
    ("Subagent(子代理)", "openai-agents 的 handoffs / 主代理把工具外包"),
    ("MCP(工具接入标准)", "mcp 包,一次接入处处可用"),
]:
    print(f"    {concept:<28} ↔ {py_side}")

print("\n=== 学习路线(下一手) ===")
print("    ① 01_agent_loop.py 手搓内核 → ② 02 学 pydantic 立规矩")
print("    → ③ 03 装 pydantic-ai 跑真 Agent → ④ 框架选型(README 12.5)")
print("    → ⑤ 要并发/流式?回 ch10 把 asyncio 练熟")

# 预期输出:
# === Agent 开发常用库:先认脸,再动手 ===
# ...(三梯队清单 + 对照表 + 路线,全部固定,可逐行对照)
