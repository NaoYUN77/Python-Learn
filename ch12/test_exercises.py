"""test_exercises.py — 第十二章练习自动检查。

运行(在项目根目录执行):python -m ch12.test_exercises
本章测试需要 pydantic:pip install pydantic(不用 API key)。
"""

from . import exercises

from pydantic import BaseModel


def test_make_book():
    b = exercises.make_book({"title": "流畅的Python", "pages": 800, "finished": False})
    assert isinstance(b, BaseModel), f"应返回 BaseModel 实例,实际 {type(b).__name__}"
    assert b.title == "流畅的Python" and b.pages == 800 and b.finished is False, (
        f"字段值不对,实际 {b!r}"
    )


def test_page_type():
    r = exercises.page_type({"title": "甲", "pages": "350", "finished": True})
    assert r == "int", f"'350' 应被自动转成 int,实际得到类型 {r!r}"


def test_check_book():
    r = exercises.check_book({"title": "甲", "pages": "很多", "finished": True})
    assert r == "bad", f"'很多' 转不成 int,应返回 'bad',实际 {r!r}"
    r = exercises.check_book({"title": "甲", "pages": 1, "finished": True})
    assert r == "ok", f"合格数据应返回 'ok',实际 {r!r}"


def test_check_score():
    assert exercises.check_score({"course": "py", "score": 100}) == "ok", "100 是合法分(两端都含!)"
    assert exercises.check_score({"course": "py", "score": 0}) == "ok", "0 是合法分(两端都含!)"
    assert exercises.check_score({"course": "py", "score": 101}) == "bad", "101 应越界被拦"
    assert exercises.check_score({"course": "py", "score": -1}) == "bad", "-1 应越界被拦"


def test_count_finished():
    data = {"books": [
        {"title": "甲", "pages": 1, "finished": True},
        {"title": "乙", "pages": 2, "finished": False},
        {"title": "丙", "pages": 3, "finished": True},
    ]}
    r = exercises.count_finished(data)
    assert r == 2, f"应数出 2 本读完,实际 {r!r}"
    r = exercises.count_finished({"books": []})
    assert r == 0, f"空书架应为 0,实际 {r!r}"


def test_weather_json():
    r = exercises.weather_json({"city": "杭州", "temp_c": 28})
    assert r == '{"city":"杭州","temp_c":28.0}', f"应为紧凑 JSON 字符串,实际 {r!r}"


def test_parse_review():
    ok, review = exercises.parse_review({"title": "甲传", "score": "8", "recommend": True})
    assert ok and review is not None, "'8' 能转 int,应解析成功"
    assert review.score == 8 and type(review.score).__name__ == "int", (
        f"score 应转为 int 8,实际 {review.score!r}"
    )
    ok, review = exercises.parse_review({"title": "乙传", "score": 99, "recommend": True})
    assert not ok and review is None, f"99 越界,应返回 (False, None),实际 {(ok, review)!r}"


def run_all():
    tests = [
        test_make_book,
        test_page_type,
        test_check_book,
        test_check_score,
        test_count_finished,
        test_weather_json,
        test_parse_review,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
        except NotImplementedError:
            print(f"⏳ {test.__name__}: 还没完成")
        except Exception as e:
            print(f"❌ {test.__name__}: 出错 {type(e).__name__}: {e}")

    print(f"\n通过 {passed}/{len(tests)}")
    if passed == len(tests):
        print("恭喜!全部通过 🎉")
    else:
        print("继续加油,还没完成全部 😊")


if __name__ == "__main__":
    run_all()
