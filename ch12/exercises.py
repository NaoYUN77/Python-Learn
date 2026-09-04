"""exercises.py — 第十二章练习(Agent 开发入门:pydantic 打底)。

请完成下面的每个函数,然后运行 python -m ch12.test_exercises 检查。

本章练习只用 pydantic(不需要 API key)——把"数据立规矩"练熟,
pydantic-ai 的真 Agent 留给你配好 key 之后照 03 示例自己玩。

延续 ch09 的规矩:**import 也要你自己写**——
骨架里一行 import 都没有,请在 docstring 结束后建 import 区。
⚠️ 三条铁律照旧:①import 只写顶部 ②没用整行删 ③弹窗塞的陌生名字别回车。
"""

# 练习 1:第一个模型
# TODO: 顶部加 from pydantic import BaseModel
# 定义一个 Book 模型:书名(str)、页数(int)、是否读完(bool),
# 本函数接收字典,返回 Book 实例(直接 Book(**data) 即可)
# make_book({"title": "流畅的Python", "pages": 800, "finished": False})
#   → Book 实例,且 .pages 的类型是 int
def make_book(data):
    # 提示:先在函数外定义 class Book(BaseModel),再一行打包
    pass
i

# 练习 2:自动转型
# TODO: 同上 import
# pydantic 会自动把 "350" 转成 350——本函数返回转型后的 pages 字段类型名
# page_type({"title": "甲", "pages": "350", "finished": True}) → "int"
def page_type(data):
    # 提示:make_book(data).pages,再 type(x).__name__(ch10 已练)
    pass


# 练习 3:挡住脏数据
# TODO: 顶部加 from pydantic import ValidationError
# 尝试用 data 创建 Book;合格返回 "ok",不合格返回 "bad"
# check_book({"title": "甲", "pages": "很多", "finished": True}) → "bad"
# check_book({"title": "甲", "pages": 1, "finished": True})      → "ok"
def check_book(data):
    # 提示:try 里 Book(**data) 返回 "ok";except ValidationError 返回 "bad"
    # (ch07:只接能处理的型号,ValidationError ⊆ Exception 但要接得准)
    pass


# 练习 4:字段约束
# TODO: 顶部加 from pydantic import BaseModel, Field
# 定义 Score 模型:课程名(str)、分数(int,范围 0~100——用 Field(ge=0, le=100)),
# 返回校验结果:"ok" 或 "bad"
# check_score({"course": "py", "score": 100}) → "ok"
# check_score({"course": "py", "score": 101}) → "bad"(ch07 的边界条件教训!)
def check_score(data):
    # 提示:class Score(BaseModel): score: int = Field(ge=0, le=100)
    # ge=greater or equal,le=less or equal——两端都含
    pass


# 练习 5:嵌套模型
# TODO: 同上 import
# 定义 Library(书架):books 是 Book 列表;本函数统计"读完"的数量
# count_finished({"books": [
#     {"title": "甲", "pages": 1, "finished": True},
#     {"title": "乙", "pages": 2, "finished": False},
# ]}) → 1
def count_finished(data):
    # 提示:Book(**b) 挨个转型(推导式),再数 .finished 为 True 的(ch03/ch05 连击)
    pass


# 练习 6:模型 → JSON
# TODO: 顶部加 from pydantic import BaseModel
# 定义 Weather 模型(city: str, temp_c: float),返回它的 JSON 字符串
# weather_json({"city": "杭州", "temp_c": 28}) → '{"city":"杭州","temp_c":28.0}'
def weather_json(data):
    # 提示:模型实例有 .model_dump_json() 方法;浮点会带 .0
    pass


# 练习 7:结构化输出模拟(综合挑战)
# TODO: 同上 import(顶部加 from pydantic import BaseModel, ValidationError)
# 模拟 ch12 03 场景 3:LLM 返回"可能是脏数据的 dict",你负责把关。
# 定义 MovieReview 模型:title(str)、score(int, 0~10)、recommend(bool)。
# 返回元组 (True, MovieReview实例) 或 (False, None)
# parse_review({"title": "甲传", "score": "8", "recommend": True})
#   → (True, MovieReview 实例,score 已转 int)
# parse_review({"title": "乙传", "score": 99, "recommend": True}) → (False, None)
def parse_review(data):
    # 提示:try → return True, Book(**data) 同款打包;
    # except ValidationError → return False, None(ch04:return a, b)
    pass
