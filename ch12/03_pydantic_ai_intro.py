"""03_pydantic_ai_intro.py — pydantic-ai 上手:第一个真 Agent。

运行前准备(两步):
    pip install pydantic-ai
    配一个模型的 API key(三选一,放进环境变量或 .env):
        OPENAI_API_KEY=...        (OpenAI)
        ZAI_API_KEY=...           (智谱 GLM)
        ANTHROPIC_API_KEY=...     (Claude)

⚠️ 本章示例需要真实 API key 才能跑通——没配 key 时运行本文件,
会给出友好的安装/配置指引而不是裸 Traceback(ch07 的体面退场)。

核心概念(和 AI SDK 一一对应):
    Agent(模型, instructions=系统提示, tools=工具, output_type=结构化输出)
    agent.run_sync(...)  → 同步跑一轮 agent loop(ch10:asyncio 则用 agent.run)
"""

import os

try:
    from pydantic_ai import Agent
except ImportError:
    print("未安装 pydantic-ai。先执行:pip install pydantic-ai")
    raise SystemExit(1)

# ── key 三选一(装了 python-dotenv 的话,先 load_dotenv() 读 .env) ──
KEY_VARS = ["OPENAI_API_KEY", "ZAI_API_KEY", "ANTHROPIC_API_KEY"]
if not any(os.getenv(v) for v in KEY_VARS):
    print("没检测到 API key。三选一配置(推荐写进 .env,别进代码库):")
    for v in KEY_VARS:
        print(f"    set {v}=你的key      ← Windows CMD")
        print(f"    $env:{v}='你的key'   ← PowerShell")
    print("然后重新运行:python ch12/03_pydantic_ai_intro.py")
    print("(下面 4 个场景的代码照常阅读——key 只是让 run_sync 真的发请求)")
    raise SystemExit(0)


# ── 场景 1:最裸的 Agent——一句话问答 ──
def demo_plain():
    agent = Agent("openai:gpt-4o-mini", instructions="用一句话回答")
    result = agent.run_sync("什么是 Agent?")
    print(result.output)          # 注意:是 result.output,不是 result 本身


# ── 场景 2:Tool Calling——给模型发工具,它自己决定调不调 ──
from pydantic_ai.tools import RunContext


def demo_tools():
    agent = Agent("openai:gpt-4o-mini", instructions="回答前先查工具拿实时数据")


    @agent.tool
    def get_weather(ctx: RunContext, city: str) -> dict:
        """查询某城市当前天气(参数类型和 docstring 会变成给模型看的说明书)"""
        return {"city": city, "weather": "晴", "temp": 28}   # 演示:写死


    result = agent.run_sync("杭州现在穿什么合适?")
    print(result.output)
    # 模型自己决定:调 get_weather("杭州") → 拿到 28 度 → 组织成穿衣建议
    # ——ch12 01 的 for 循环,框架替你转了


# ── 场景 3:Structured Output——让输出直接是 pydantic 对象 ──
from pydantic import BaseModel, Field


class MovieReview(BaseModel):
    title: str
    score: int = Field(ge=0, le=10)
    recommend: bool


def demo_structured():
    agent = Agent(
        "openai:gpt-4o-mini",
        instructions="你是影评人,打分要毒舌但公正",
        output_type=MovieReview,          # ★ 输出即对象,LLM 的 JSON 不合格会自动重试
    )
    result = agent.run_sync("评价一下《流浪地球2》")
    review = result.output                # 已经是 MovieReview 实例!
    print(f"{review.title}:{review.score}/10,推荐?{review.review if False else review.recommend}")
    # 拿到手就是类型安全的对象——不用自己 json.loads 再逐字段检查


if __name__ == "__main__":
    print("== 场景 1:最裸的 Agent ==")
    demo_plain()
    print("\n== 场景 2:Tool Calling ==")
    demo_tools()
    print("\n== 场景 3:Structured Output ==")
    demo_structured()

# 预期输出(带 key 时,模型输出每次不同,形状一致):
# == 场景 1:最裸的 Agent ==
# Agent 是能在循环中使用工具完成任务的 LLM 应用。
#
# == 场景 2:Tool Calling ==
# (模型先调 get_weather,再回答)杭州今天晴、28 度,建议穿短袖……
#
# == 场景 3:Structured Output ==
# 流浪地球2:8/10,推荐?True
