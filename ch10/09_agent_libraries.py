"""09_agent_libraries.py — Agent 开发常用库盘点:先认脸,再动手。

运行:python ch10/09_agent_libraries.py
参照 Vercel AI SDK(https://ai-sdk.dev)的概念体系:
Agent 开发 = 统一模型接口 + Tool Calling + 结构化输出 + Agent Loop + 记忆 + 流式输出。

本章只做三件事:
① 把每个库"是干什么的、对应哪个概念"讲清楚;
② 用【纯标准库】搭一个 30 行的迷你 Agent Loop——所有框架的内核都是它;
③ 留一张"下一步学什么"的地图(ch11 的 async 是门钥匙)。

框架本身本章不 import(装哪个学哪个),骨架零依赖,直接能跑。
"""

import json

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
    ("langchain",    "最老牌的 LLM 应用工具箱:组件多、集成全,原型最快"),
    ("langgraph",    "LangChain 家的'有状态流程图':循环/分支/人工审批,复杂 Agent 首选"),
    ("openai-agents","OpenAI 出的轻量框架:handoffs(子代理交接)+ guardrails"),
    ("crewai",       "角色扮演式多智能体:给每个 Agent 定角色/目标,组队干活"),
    ("autogen",      "微软出品:多 Agent 对话式协作(现已并入 Microsoft Agent 框架)"),
    ("pydantic-ai",  "类型安全的 Agent 框架:pydantic 作者出品,强类型风格"),
]:
    print(f"    • {name:<15} {why}")

# ── 第三梯队:支撑件层("Agent 周边的水电煤") ──
print("\n[支撑件层]")
for name, why in [
    ("mcp",           "Model Context Protocol:Anthropic 开的工具接入标准,'AI 界的 USB-C'"),
    ("pydantic",      "结构化输出把关:LLM 吐的 JSON 合不合格,它说了算"),
    ("httpx",         "异步 HTTP:所有 SDK 调 API 的底层常客"),
    ("python-dotenv", "密钥进 .env 不进代码"),
    ("rich",          "Agent 的思考过程打印出来好看又好读"),
    ("tiktoken",      "数 token:上下文窗口花了多少,心里有数"),
]:
    print(f"    • {name:<15} {why}")

# ── 重头戏:30 行迷你 Agent Loop(所有框架的内核都是它) ──
print("\n=== 迷你 Agent Loop:框架帮你做的事,亲手做一遍 ===\n")


def fake_llm(history):
    """假装的模型。真项目里这一步换成真实 API 调用,其余逻辑一字不改——
    这就是'接口层'的意义。注意它读的是 history,不是单独的 user_text:
    工具结果 append 进 history 后,下一轮模型就'看见'了(闭合!)。"""
    if not any("tool_result" in item for item in history):
        # 还没查过 → 模型第一反应:我要调工具
        return {"tool": "get_weather", "args": {"city": "杭州"}}
    # 已经有工具结果了 → 汇总作答
    weather = history[-1]["tool_result"]
    return {"reply": f"{weather['city']}今天{weather['weather']},气温 {weather['temp']} 度"}


def get_weather(city):
    """一个工具(tool)。真项目里它可能是查库、读文件、调第三方 API。"""
    return {"city": city, "weather": "晴", "temp": 28}


def agent_loop(user_text, max_steps=3):
    """Agent 的心脏:模型说要调工具 → 执行 → 结果喂回去 → 模型作答 → 收工。
    max_steps 是安全带:防止模型无限循环调工具(ch03 循环 + ch07 防御)。"""
    history = [{"user": user_text}]             # 记忆:对话记在本列表里
    for step in range(max_steps):
        decision = fake_llm(history)
        if "reply" in decision:                 # 模型给出了最终回答 → 收工
            return decision["reply"]
        result = get_weather(**decision["args"])  # 执行模型点名的工具
        print(f"    第 {step + 1} 步:模型要调工具 {decision['tool']}"
              f"({json.dumps(decision['args'], ensure_ascii=False)}) → 执行得 {result}")
        history.append({"tool": decision["tool"], "tool_result": result})
    return "(步数用尽,强制收工)"


print("问:杭州天气怎么样?")
print("答:", agent_loop("杭州天气怎么样?"))
print()
print("拆开看,这 30 行就是全部概念:")
print("    fake_llm        → 模型接口层(Provider)")
print("    get_weather     → 工具(Tool Calling)")
print("    history         → 记忆(Memory)——工具结果也记进去,模型下一轮才看得见")
print("    for + max_steps → Agent Loop + 循环上限(AI SDK 的 Loop Control)")
print("    LangGraph/CrewAI/pydantic-ai……都在给这个循环加料:")
print("    加状态图、加多角色、加类型校验、加人工审批——内核不变。")

# ── 下一步地图 ──
print("\n=== 下一步学什么 ===")
print("    1. ch11 的 asyncio:真实 Agent 框架里 API 调用全是 async 的——先修课")
print("    2. 挑一个官方 SDK(openai / zai-sdk)跑通第一句对话(要 API key)")
print("    3. 用 pydantic 给'LLM 返回的 JSON'立规矩(结构化输出)")
print("    4. 回头再看 LangGraph 等框架文档,你会认得每一个概念——都是本章词表")

# 预期输出(认脸部分固定;迷你 Loop 部分完全确定,可逐行对照):
# === Agent 开发常用库:先认脸,再动手 ===
# ...(三梯队清单同上)
# === 迷你 Agent Loop:框架帮你做的事,亲手做一遍 ===
#
# 问:杭州天气怎么样?
# 答:     第 1 步:模型要调工具 get_weather({"city": "杭州"}) → 执行得 {'city': '杭州', 'weather': '晴', 'temp': 28}
#     杭州今天晴,气温 28 度
#
# 拆开看,这 30 行就是全部概念:
#     ...
