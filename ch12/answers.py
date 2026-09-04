"""answers.py — 第十二章练习参考答案。

先自己做完 exercises.py,再对照这里。
"""

from pydantic import BaseModel, Field, ValidationError


# 练习 1:第一个模型
class Book(BaseModel):
    title: str
    pages: int
    finished: bool


def make_book(data):
    return Book(**data)


# 练习 2:自动转型
def page_type(data):
    return type(make_book(data).pages).__name__


# 练习 3:挡住脏数据
def check_book(data):
    try:
        Book(**data)
        return "ok"
    except ValidationError:
        return "bad"


# 练习 4:字段约束
class Score(BaseModel):
    course: str
    score: int = Field(ge=0, le=100)


def check_score(data):
    try:
        Score(**data)
        return "ok"
    except ValidationError:
        return "bad"


# 练习 5:嵌套模型
class Library(BaseModel):
    books: list[Book]


def count_finished(data):
    lib = Library(**data)               # 嵌套:字典列表自动变成 Book 实例列表!
    return sum(1 for b in lib.books if b.finished)


# 练习 6:模型 → JSON
class Weather(BaseModel):
    city: str
    temp_c: float


def weather_json(data):
    return Weather(**data).model_dump_json()


# 练习 7:结构化输出模拟
class MovieReview(BaseModel):
    title: str
    score: int = Field(ge=0, le=10)
    recommend: bool


def parse_review(data):
    try:
        return True, MovieReview(**data)
    except ValidationError:
        return False, None


if __name__ == "__main__":
    book = make_book({"title": "流畅的Python", "pages": 800, "finished": False})
    print(book)                                          # 全字段一行展示
    print(page_type({"title": "甲", "pages": "350", "finished": True}))   # int
    print(check_book({"title": "甲", "pages": "很多", "finished": True}))  # bad
    print(check_score({"course": "py", "score": 100}))   # ok
    print(check_score({"course": "py", "score": 101}))   # bad
    print(count_finished({"books": [
        {"title": "甲", "pages": 1, "finished": True},
        {"title": "乙", "pages": 2, "finished": False},
    ]}))                                                 # 1
    print(weather_json({"city": "杭州", "temp_c": 28}))  # {"city":"杭州","temp_c":28.0}
    ok, review = parse_review({"title": "甲传", "score": "8", "recommend": True})
    print(ok, review.score, type(review.score).__name__) # True 8 int
    print(parse_review({"title": "乙传", "score": 99, "recommend": True}))  # (False, None)
