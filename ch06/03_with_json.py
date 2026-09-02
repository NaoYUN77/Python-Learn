"""03_with_json.py — with 语句与 json 模块。

运行：python ch06/03_with_json.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#saving-structured-data-with-json

本脚本会在 ch06/ 目录下创建 scores.json，可反复运行。
"""

import json

# ══════════════════════════════════════════
# 第一部分：with 语句 —— 自动关闭文件
# ══════════════════════════════════════════

# 1. 基本形态：出了 with 块自动 close，异常也会关
with open("ch06/scores.json", "w", encoding="utf-8") as f:
    f.write("{}")
print(f.closed)               # True ← 离开 with 块后文件已经关了
# f.write("x")                # ❌ ValueError: I/O operation on closed file

# 2. 中途出异常？with 依然保证关闭（02_files.py 第 7 段的解药）
try:
    with open("ch06/scores.json", "w", encoding="utf-8") as f:
        f.write("写了一半\n")
        raise RuntimeError("又炸了！")
except RuntimeError as e:
    print("捕获:", e)
print("文件还是被安全关闭了 ✅")

# ══════════════════════════════════════════
# 第二部分：json —— 结构化数据的存取
# ══════════════════════════════════════════

# 3. dumps：Python 对象 → json 字符串（s = string）
data = {"name": "小明", "scores": [90, 85], "passed": True}
text = json.dumps(data, ensure_ascii=False)    # ensure_ascii=False 让中文可读
print(text)                        # {"name": "小明", "scores": [90, 85], "passed": true}
print(type(text).__name__)         # str ← 是字符串！

# 注意：json 的 true/false/null 对应 Python 的 True/False/None
# （读回来会自动还原，但肉眼看 json 文件时要认识这几个词）

# 4. loads：json 字符串 → Python 对象（从 string 加载）
restored = json.loads(text)
print(restored["name"])           # 小明
print(type(restored).__name__)    # dict ← 还原成字典
print(restored == data)           # True（完整往返，一模一样）

# 5. dump / load：直接对接文件（没有 s = 不经过字符串，直接文件）
with open("ch06/scores.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)    # indent=2 缩进美化

with open("ch06/scores.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["scores"])           # [90, 85]

# 6. 方向自测（划重点，方向病高发区）：
#    dumps：对象 → str   （s 结尾 = 产 string）
#    loads：str → 对象    （从 string 读）
#    dump ：对象 → 文件
#    load ：文件 → 对象
def save_students(students, path):
    """列表/字典 → 文件。方向：对象出去 → 用 dump。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

def load_students(path):
    """文件 → 列表/字典。方向：对象进来 → 用 load。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

save_students([{"name": "小红", "score": 92}], "ch06/students.json")
print(load_students("ch06/students.json"))    # [{'name': '小红', 'score': 92}]

# 7. json 只认这几类：dict / list / str / int / float / bool / None
#    集合、元组不能直接存（元组会变成列表）
try:
    json.dumps({1, 2, 3})
except TypeError as e:
    print("报错:", e)              # Object of type set is not JSON serializable
print(json.dumps((1, 2)))          # '[1, 2]' ← 元组变成 json 数组（还原后是列表）
