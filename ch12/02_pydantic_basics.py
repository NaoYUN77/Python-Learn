"""02_pydantic_basics.py — pydantic 打底:用类给数据立规矩。

运行:python ch12/02_pydantic_basics.py
需要:pip install pydantic(Agent 开发的地基,ch08 的类 + 自动校验)

为什么 Agent 开发离不开它?
LLM 吐出来的 JSON 是"自由文本"——结构对不对、类型对不对,没人把关。
pydantic 的 BaseModel 让你**用声明类型的办法**把守入口:
合格的数据放行(还能自动转型),不合格当场 ValidationError 拦下。
AI SDK 用 Zod schema 干同样的事;Python 世界的标准答案就是 pydantic。
"""

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("未安装 pydantic。先执行:pip install pydantic")
    raise SystemExit(1)

# ── 1. 最小模型:声明类型,pydantic 替你把守 ──
print("== 1. BaseModel:类型就是规矩 ==")


class City(BaseModel):
    name: str
    population: int


c = City(name="杭州", population="1200")     # "1200" 是 str,但能转 int → 放行并转型
print(f"{c.name} 人口 {c.population} 万(转型后 type={type(c.population).__name__})")

try:
    City(name="杭州", population="很多")      # "很多" 转不成 int → 当场拦下
except ValidationError as e:
    print(f"乱来的数据?挡下:{e.errors()[0]['type']}(ch07:按型号报错,信息 readable)")

# ── 2. 嵌套与约束:复杂结构也照单全收 ──
print("\n== 2. 嵌套 + Field 约束 ==")


class Ingredient(BaseModel):
    name: str
    amount: str = Field(description="数量,如 '200g'")


class Recipe(BaseModel):
    name: str
    ingredients: list[Ingredient]      # 嵌套列表——ch05 的容器 + ch08 的类
    steps: list[str]


r = Recipe(
    name="番茄炒蛋",
    ingredients=[{"name": "番茄", "amount": "2个"}, {"name": "鸡蛋", "amount": "3个"}],
    steps=["番茄切块", "炒蛋", "混合翻炒"],
)
print(f"{r.name}:{len(r.ingredients)} 种食材,字典直接喂进去 → 变成对象")
print(f"第一个食材:{r.ingredients[0].name}(它是 Ingredient 实例)")

# ── 3. 往模型里塞"回字形的脏数据"──
print("\n== 3. 脏数据进来试试 ==")
bad_json = {"name": 123, "ingredients": "番茄", "steps": []}
try:
    Recipe(**bad_json)
except ValidationError as e:
    print(f"两个字段不合格,全被抓出来({len(e.errors())} 条):")
    for err in e.errors():
        print(f"    {' → '.join(str(x) for x in err['loc'])}:{err['msg']}")

print("\n→ 这就是 ch12 反复出现的句式:LLM 输出 → pydantic 验证 → 类型安全的对象。")
print("   下一手:03 里让 pydantic-ai 把'验证'做进 Agent 里。")

# 预期输出:
# == 1. BaseModel:类型就是规矩 ==
# 杭州人口 1200 万(转型后 type=int)
# 乱来的数据?挡下:int_parsing(ch07:按型号报错,信息 readable)
#
# == 2. 嵌套 + Field 约束 ==
# 番茄炒蛋:2 种食材,字典直接喂进去 → 变成对象
# 第一个食材:番茄(它是 Ingredient 实例)
#
# == 3. 脏数据进来试试 ==
# 两个字段不合格,全被抓出来(2 条):
#     name:Input should be a valid string
#     ingredients:Input should be a valid list
# ...(措辞随 pydantic 版本略异,形状一致)
