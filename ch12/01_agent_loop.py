"""01_agent_loop.py — 手搓最小 Agent Loop:四步渐进,30 行看穿所有框架。

运行:python ch12/01_agent_loop.py
零依赖、零 API key,直接能跑;输出完全确定,可逐行对照。

参照 Vercel AI SDK 的定义(https://ai-sdk.dev/docs/agents/overview):
    Agent = LLM 在循环里使用工具完成任务(LLMs + Tools + Loop)
对应 pydantic-ai 文档的话:Agent 是一个容器,装着
    instructions(怎么干)+ tools(能干什么)+ output_type(交什么差)+ model(谁在干)

我们分四步把这个循环亲手搭出来——每一步都能独立运行:
    第 1 步:只会说话的"模型"(一次调用,一问一答)
    第 2 步:给它发工具(Tool Calling:模型点名,我们执行)
    第 3 步:加循环和停止条件(Agent Loop + max_steps)
    第 4 步:完整跑通 + 逐帧跟踪表
真框架(pydantic-ai/LangGraph/…)只是给这个循环加料:
加类型校验、加状态图、加多角色、加人工审批——内核不变。
"""

import json

# ════════════════════════════════════════════════════════
# 公共道具:一个"假装的模型"和一个真工具
# ════════════════════════════════════════════════════════

TOOLS = {
    "get_weather": {
        "description": "查询某城市当前天气",
        "args": {"city": "城市名"},
        "run": lambda city: {"city": city, "weather": "晴", "temp": 28},
    },
    "get_time": {
        "description": "查询现在的时间",
        "args": {},
        "run": lambda: {"time": "14:00"},
    },
}


def fake_llm(history):
    """假装的模型。真项目里这一步换成真实 API 调用(pydantic-ai 里
    就是 agent.run(...)),其余逻辑一字不改——这就是'接口层'的意义。

    它按剧本演:看 history 里已有什么,决定下一步要什么。
    (真模型是概率输出;这里是确定输出,方便你逐帧跟踪。)
    """
    has_weather = any(m.get("tool") == "get_weather" for m in history)
    if "天气" in history[0]["user"] and not has_weather:
        return {"tool": "get_weather", "args": {"city": "杭州"}}
    if has_weather:
        w = next(m["tool_result"] for m in history if m.get("tool") == "get_weather")
        return {"reply": f"{w['city']}今天{w['weather']},气温 {w['temp']} 度"}
    return {"reply": f"你说:{history[0]['user']}"}


# ════════════════════════════════════════════════════════
# 第 1 步:只会说话的"模型"——一次调用,一问一答
# ════════════════════════════════════════════════════════

def step1():
    print("── 第 1 步:纯对话(没有工具,模型只能凭嘴说)──")
    history = [{"user": "Python 好学吗?"}]
    reply = fake_llm(history)["reply"]
    print(f"    问:{history[0]['user']}")
    print(f"    答:{reply}")
    print("    → 局限:问'天气'它也只能编——它够不着外部世界。\n")


# ════════════════════════════════════════════════════════
# 第 2 步:发工具——模型"点名",我们执行(Tool Calling)
# ════════════════════════════════════════════════════════

def step2():
    print("── 第 2 步:Tool Calling(模型不再直接回答,而是点单)──")
    decision = fake_llm([{"user": "杭州天气怎么样?"}])
    print(f"    模型说:我要调 {decision['tool']},参数 {json.dumps(decision['args'], ensure_ascii=False)}")

    tool = TOOLS[decision["tool"]]                 # 按名找工具
    result = tool["run"](**decision["args"])       # ** 解包参数(ch04!)再执行
    print(f"    我们执行:{decision['tool']} → {result}")
    print("    → 关键:模型自己【不执行】任何东西,它只输出'点名+参数'的 JSON;")
    print("      执行永远发生在你的代码里。这就是 Agent 安全模型的根基。\n")


# ════════════════════════════════════════════════════════
# 第 3 步:循环 + 停止条件——工具结果要喂回模型(Agent Loop)
# ════════════════════════════════════════════════════════

def agent_loop(user_text, max_steps=3, verbose=False):
    """Agent 的心脏(与 AI SDK 的 ToolLoopAgent / pydantic-ai 的 Agent.run 同构):

        ① 问模型(history 全量给它——它靠这个'看见'之前发生了什么)
        ② 模型要么给最终回答(收工),要么点名工具
        ③ 执行工具,结果 append 进 history
        ④ 回到 ①,直到模型给最终回答,或步数用尽

    max_steps 是安全带:AI SDK 叫 stopWhen / isStepCount(默认 20 步),
    pydantic-ai 叫 UsageLimits(request_limit);防的是无限循环烧钱。
    """
    history = [{"user": user_text}]                # 记忆(Memory):一切从这里开始
    for step in range(max_steps):
        decision = fake_llm(history)               # ① 问模型
        if "reply" in decision:                    # ② 最终回答 → 收工
            if verbose:
                print(f"    第 {step + 1} 轮:模型给出最终回答")
            return decision["reply"], history
        tool = TOOLS[decision["tool"]]             # ③ 执行工具
        result = tool["run"](**decision["args"])
        if verbose:
            print(f"    第 {step + 1} 轮:调 {decision['tool']}"
                  f"({json.dumps(decision['args'], ensure_ascii=False)}) → {result}")
        history.append({"tool": decision["tool"], "tool_result": result})
    return "(步数用尽,强制收工)", history


# ════════════════════════════════════════════════════════
# 第 4 步:完整跑通 + 跟踪表
# ════════════════════════════════════════════════════════

def step4():
    print("── 第 3+4 步:完整 Agent Loop(带逐帧跟踪)──")
    print("问:杭州天气怎么样?")
    answer, history = agent_loop("杭州天气怎么样?", verbose=True)
    print(f"答:{answer}")

    print("\n    逐帧跟踪表(history 的成长史):")
    for i, m in enumerate(history):
        kind = "user" if "user" in m else m["tool"]
        content = m.get("user") or m.get("tool_result")
        print(f"    [{i}] {kind:<12} {content}")

    print("\n    三大件对照:")
    print("    fake_llm / history / for+max_steps")
    print("    → 模型接口层 / 记忆(Memory) / 循环+停止条件(Loop Control)")
    print("    → pydantic-ai 把 ①~④ 全部包进 agent.run_sync() 一行;")
    print("      但现在你知道那行代码里发生什么——调试 Agent 就是盯着 history 看。")


if __name__ == "__main__":
    step1()
    step2()
    step4()

# 预期输出(完全确定,可逐行对照):
# ── 第 1 步:纯对话(没有工具,模型只能凭嘴说)──
#     问:Python 好学吗?
#     答:你说:Python 好学吗?
#     → 局限:问'天气'它也只能编——它够不着外部世界。
#
# ── 第 2 步:Tool Calling(模型不再直接回答,而是点单)──
#     模型说:我要调 get_weather,参数 {"city": "杭州"}
#     我们执行:get_weather → {'city': '杭州', 'weather': '晴', 'temp': 28}
#     → 关键:模型自己【不执行】任何东西,它只输出'点名+参数'的 JSON;
#       执行永远发生在你的代码里。这就是 Agent 安全模型的根基。
#
# ── 第 3+4 步:完整 Agent Loop(带逐帧跟踪)──
# 问:杭州天气怎么样?
#     第 1 轮:调 get_weather({"city": "杭州"}) → {'city': '杭州', 'weather': '晴', 'temp': 28}
#     第 2 轮:模型给出最终回答
# 答:杭州今天晴,气温 28 度
#
#     逐帧跟踪表(history 的成长史):
#     [0] user         杭州天气怎么样?
#     [1] get_weather  {'city': '杭州', 'weather': '晴', 'temp': 28}
#
#     三大件对照:
#     fake_llm / history / for+max_steps
#     → 模型接口层 / 记忆(Memory) / 循环+停止条件(Loop Control)
#     → pydantic-ai 把 ①~④ 全部包进 agent.run_sync() 一行;
#       但现在你知道那行代码里发生什么——调试 Agent 就是盯着 history 看。
