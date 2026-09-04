"""临时自检:验证 ch10 答案自洽(跑完即删)"""
import random
import shutil
import tempfile
from pathlib import Path
from string import ascii_letters, digits

import ch10.answers as a

# 练习 1
r = a.most_common_words("py go py go go cat", 2)
assert r == [("go", 3), ("py", 2)], f"练1: {r!r}"
r = a.most_common_words("a a a", 1)
assert r == [("a", 3)], f"练1b: {r!r}"

# 练习 2
r = a.group_by_first_letter(["apple", "banana", "avocado"])
assert r == {"a": ["apple", "avocado"], "b": ["banana"]}, f"练2: {r!r}"
assert a.group_by_first_letter([]) == {}, "练2b: 空列表"

# 练习 3
random.seed(42)
r1 = a.roll_dice(5)
random.seed(42)
r2 = a.roll_dice(5)
assert r1 == r2, f"练3: 不可复现 {r1} vs {r2}"
assert len(r1) == 5 and all(1 <= x <= 6 for x in r1), f"练3b: {r1}"

# 练习 4
tmp = tempfile.mkdtemp()
try:
    for name in ["b.py", "a.py", "notes.txt", "c.py"]:
        Path(tmp, name).write_text("# t", encoding="utf-8")
    r = a.py_files_in(tmp)
    assert r == ["a.py", "b.py", "c.py"], f"练4: {r!r}"
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# 练习 5
assert a.days_between(2026, 1, 1, 2026, 2, 1) == 31, "练5a"
assert a.days_between(2024, 2, 1, 2024, 3, 1) == 29, "练5b: 闰年"
assert a.days_between(2026, 3, 1, 2026, 3, 1) == 0, "练5c: 同一天"

# 练习 6
r = a.exam_stats([2, 4, 4, 10])
assert r == (5.0, 4.0), f"练6: {r!r}"
assert a.exam_stats([7]) == (7, 7), "练6b: 单元素"

# 练习 7
pw = a.gen_password(8)
assert isinstance(pw, str) and len(pw) == 8, f"练7: {pw!r}"
allowed = ascii_letters + digits
assert all(ch in allowed for ch in pw), f"练7b: 字符范围 {pw!r}"

print("ch10 answers 自检全部通过 ✅")
