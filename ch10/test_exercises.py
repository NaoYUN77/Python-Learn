"""test_exercises.py — 第十章练习自动检查。

运行(在项目根目录执行):python -m ch10.test_exercises
如果你通过了全部测试,会在终端看到 "恭喜!全部通过 🎉"。
"""

from . import exercises

import random
import shutil
import tempfile
from pathlib import Path
from string import ascii_letters, digits


def test_most_common_words():
    r = exercises.most_common_words("py go py go go cat", 2)
    assert r == [("go", 3), ("py", 2)], f"应为 [('go', 3), ('py', 2)],实际 {r!r}"
    r = exercises.most_common_words("a a a", 1)
    assert r == [("a", 3)], f"只出现一个词,应为 [('a', 3)],实际 {r!r}"


def test_group_by_first_letter():
    r = exercises.group_by_first_letter(["apple", "banana", "avocado"])
    assert r == {"a": ["apple", "avocado"], "b": ["banana"]}, (
        f"应按首字母分组得到 {{'a': ['apple', 'avocado'], 'b': ['banana']}},实际 {r!r}"
    )
    r = exercises.group_by_first_letter([])
    assert r == {}, f"空列表应返回空字典,实际 {r!r}"


def test_roll_dice():
    # 彩蛋:测试和 exercises 拿到的是【同一个】random 模块对象
    #(sys.modules 记账,ch09 的知识)——所以这里的 seed 能管住你函数里的随机
    random.seed(42)
    r1 = exercises.roll_dice(5)
    random.seed(42)
    r2 = exercises.roll_dice(5)
    assert r1 == r2, (
        f"同一种子应得到同一序列——第一次 {r1},第二次 {r2}"
        "(函数内部的随机调用要只由 n 决定,中途别加别的随机调用)"
    )
    assert len(r1) == 5, f"应掷 5 次,实际 {len(r1)} 次"
    assert all(1 <= x <= 6 for x in r1), f"每颗都应在 1~6 之间(两端都含!),实际 {r1}"


def test_py_files_in():
    tmp = tempfile.mkdtemp()          # 测试自建临时文件夹,跑完就删
    try:
        for name in ["b.py", "a.py", "notes.txt", "c.py"]:
            Path(tmp, name).write_text("# 临时文件", encoding="utf-8")
        r = exercises.py_files_in(tmp)
        assert r == ["a.py", "b.py", "c.py"], (
            f"应返回按字母排序的 .py 文件名(不含 notes.txt),实际 {r!r}"
            "(提示:Path(folder).glob('*.py') → 取 .name → sorted)"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)   # 测试也讲卫生:临时文件夹收走


def test_days_between():
    r = exercises.days_between(2026, 1, 1, 2026, 2, 1)
    assert r == 31, f"2026-01-01 → 2026-02-01 应为 31 天,实际 {r!r}"
    r = exercises.days_between(2024, 2, 1, 2024, 3, 1)
    assert r == 29, f"2024 是闰年,2 月有 29 天,实际 {r!r}"
    r = exercises.days_between(2026, 3, 1, 2026, 3, 1)
    assert r == 0, f"同一天相减应为 0 天,实际 {r!r}"


def test_exam_stats():
    r = exercises.exam_stats([2, 4, 4, 10])
    assert r == (5.0, 4.0), (
        f"应为 (5.0, 4.0)——平均 20/4=5,中位数 (4+4)/2=4,实际 {r!r}"
    )
    r = exercises.exam_stats([7])
    assert r == (7, 7), f"单元素:平均=中位数=7,实际 {r!r}"


def test_gen_password():
    pw = exercises.gen_password(8)
    assert isinstance(pw, str), f"应返回字符串,实际 {type(pw).__name__}"
    assert len(pw) == 8, f"密码长度应为 8,实际 {len(pw)}"
    allowed = ascii_letters + digits
    bad = [ch for ch in pw if ch not in allowed]
    assert not bad, (
        f"密码只能含大小写字母和数字,混进了 {bad!r}(提示:材料库 = ascii_letters + digits)"
    )


def run_all():
    tests = [
        test_most_common_words,
        test_group_by_first_letter,
        test_roll_dice,
        test_py_files_in,
        test_days_between,
        test_exam_stats,
        test_gen_password,
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
