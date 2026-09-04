"""01_agent_loop.py — 迷你 Agent Loop:30 行看穿所有框架。

运行:python ch12/01_agent_loop.py
零依赖、零 API key,直接能跑。
参照 Vercel AI SDK 的定义(https://ai-sdk.dev/docs/agents/overview):
    Agent = LLM 在循环里使用工具完成任务
    (LLMs + Tools + Loop:上下文管理 + 停止条件)

真框架(pydantic-ai/LangGraph/…)只是给这个循环加料:
加类型校验、加状态图、加多角色、加人工审批——内核不变。
"""

import json


# ── 三大件 ──────────────────────────────────────────

def fake_llm(history):
    """假装的模型。真项目里这一步换成真实 API 调用(pydantic-ai 里
    就是 agent.run(...)),其余逻辑一字不改——这就是'接口层'的意义。
    注意它读的是 history:工具结果 append 进去后,下一轮模型就'看见'了。"""
    if not any("tool_result" in item for item in history):
        # 还没查过 → 模型第一反应:我要调工具(Tool Calling)
        return {"tool": "get_weather", "args": {"city": "杭州"}}
    # 已经有工具结果了 → 汇总作答
    weather = history[-1]["tool_result"]
    return {"reply": f"{weather['city']}今天{weather['weather']},气温 {weather['temp']} 度"}


def get_weather(city):
    """一个工具(tool)。真项目里它可能是查库、读文件、调第三方 API。"""
    return {"city": city, "weather": "晴", "temp": 28}


def agent_loop(user_text, max_steps=3):
    """Agent 的心脏:问模型 → (它要工具就执行) → 结果进记忆 → 再问模型。
    max_steps 是安全带:AI SDK 叫 stopWhen / isStepCount,
    防止模型无限循环调工具(ch03 循环 + ch07 防御)。"""
    history = [{"user": user_text}]             # 记忆(Memory)
    for step in range(max_steps):
        decision = fake_llm(history)
        if "reply" in decision:                 # 模型给出最终回答 → 收工
            return decision["reply"]
        result = get_weather(**decision["args"])  # 执行模型点名的工具
        print(f"    第 {step + 1} 步:模型要调工具 {decision['tool']}"
              f"({json.dumps(decision['args'], ensure_ascii=False)}) → 执行得 {result}")
        history.append({"tool": decision["tool"], "tool_result": result})
    return "(步数用尽,强制收工)"


# ── 跑起来 ──
print("问:杭州天气怎么样?")
print("答:", agent_loop("杭州天气怎么样?"))
print()
print("拆开看,这 30 行就是全部概念:")
print("    fake_llm        → 模型接口层(Provider)")
print("    get_weather     → 工具(Tool Calling)")
print("    history         → 记忆(Memory)——工具结果也记进去,模型下一轮才看得见")
print("    for + max_steps → Agent Loop + 停止条件(AI SDK 的 Loop Control)")

# 预期输出(完全确定,可逐行对照):
# 问:杭州天气怎么样?
# 答:     第 1 步:模型要调工具 get_weather({"city": "杭州"}) → 执行得 {'city': '杭州', 'weather': '晴', 'temp': 28}
#     杭州今天晴,气温 28 度
#
# 拆开看,这 30 行就是全部概念:
#     ...
