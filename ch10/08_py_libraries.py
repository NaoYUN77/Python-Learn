"""08_py_libraries.py — 常用第三方库盘点:pip 装的"外接电池"。

运行:python ch10/08_py_libraries.py
标准库 = 自带电池;第三方库 = pip install 装的外接电池。
装法:pip install 库名(装一次,所有项目可用;本项目用到哪个装哪个)。

本示例设计成"装了就真跑一手,没装就友好提示"——
所以**没装任何第三方库它也能跑通**,不会 ImportError 炸脸(ch07 老朋友)。
"""

import sys

print("=== 第三方库盘点:pip 装的外接电池 ===\n")
print(f"解释器:{sys.version.split()[0]}(3.10+ 都能跑本示例)\n")

# ── 1. requests:HTTP 请求事实标准("给网页发 GET"一把梭) ──
# 装:pip install requests
print("[1] requests — HTTP 请求(网络世界的水电煤)")
try:
    import requests
    print(f"    已安装 v{requests.__version__}")
    print("    一行拿网页:r = requests.get('https://api.github.com')")
    print("    带参数:r = requests.get(url, params={'q': 'python'})")
    print("    r.status_code / r.json() / r.text —— 响应也是对象!")
except ImportError:
    print("    ⬜ 未安装。装:pip install requests")

# ── 2. httpx:requests 的现代继任者,原生支持 async(ch11 的伏笔) ──
print("\n[2] httpx — 现代版 requests,还支持异步")
try:
    import httpx
    print(f"    已安装 v{httpx.__version__}")
    print("    API 和 requests 几乎一样,多一手:httpx.AsyncClient()")
    print("    → Agent 开发里调 LLM API 大多是异步的,httpx 是底层常客")
except ImportError:
    print("    ⬜ 未安装。装:pip install httpx")

# ── 3. pydantic:用"类"给数据立规矩(ch08 的类 + 自动验证) ──
print("\n[3] pydantic — 数据验证(LangChain/pydantic-ai 的地基)")
try:
    from pydantic import BaseModel

    class City(BaseModel):
        name: str
        population: int      # 声明类型,pydantic 替你把守

    c = City(name="杭州", population=1200)   # 1200 会自动转成 int
    print(f"    已安装。现场演示:{c.name} 人口 {c.population} 万(type={type(c.population).__name__})")
    try:
        City(name="杭州", population="很多")  # str 转不成 int
    except Exception as e:
        print(f"    乱来的数据?挡下:{type(e).__name__}")
    print("    → LLM 回来的 JSON 结构对不对,靠它把关(Agent 开发刚需,ch12 主角)")
except ImportError:
    print("    ⬜ 未安装。装:pip install pydantic")

# ── 4. rich:终端里的排版师(表格/彩色/进度条) ──
print("\n[4] rich — 让 print 好看起来")
try:
    from rich import print as rprint
    rprint("    已安装。看,这是 [bold blue]蓝色加粗[/bold blue] 和 [red]红色[/red]!")
except ImportError:
    print("    ⬜ 未安装。装:pip install rich(强烈推荐,调试输出立刻清爽)")

# ── 5. dotenv:把 API 密钥等配置放进 .env 文件,不写死在代码里 ──
print("\n[5] python-dotenv — 配置与代码分离")
try:
    from dotenv import load_dotenv
    print("    已安装。用法:代码开头 load_dotenv() → os.getenv('API_KEY')")
    print("    → 密钥永远不进代码库(Agent 开发第一课:先管好你的 key)")
except ImportError:
    print("    ⬜ 未安装。装:pip install python-dotenv")

# ── 6. 数据三件套:一次性点名 ──
print("\n[6] 数据处理三件套(本章只报个到,用到再深学)")
for name, why in [
    ("numpy",   "多维数组与数值计算,pandas 的地基"),
    ("pandas",  "表格数据(DataFrame),Excel 杀手"),
    ("openpyxl","直接读写 .xlsx 文件"),
]:
    try:
        __import__(name)
        print(f"    ✅ {name:<9} 已安装 — {why}")
    except ImportError:
        print(f"    ⬜ {name:<9} 未安装(装:pip install {name}) — {why}")

print("\n=== 一句话总结 ===")
print("标准库管'通用弹药',第三方库管'专业装备';")
print("import 的规则(ch09)一模一样——装进 site-packages,import 照样找到。")

# 预期输出(✅/⬜ 视你装了什么而定;全没装也能跑通,全是 ⬜ + 用法说明):
# === 第三方库盘点:pip 装的外接电池 ===
#
# 解释器:3.12.x(3.10+ 都能跑本示例)
#
# [1] requests — HTTP 请求(网络世界的水电煤)
#     已安装 v2.32.x        ← 或"⬜ 未安装。装:pip install requests"
# ...(每段同理,装了的真跑一手,没装的给用法和安装命令)
