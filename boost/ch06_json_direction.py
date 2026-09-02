"""ch06_json_direction.py — json 四兄弟方向强化专题。

本文件是对 ch06/03_with_json.py 的强化复习，集中攻克一个核心认知：
★ 对象 → 文本是序列化（dump 家族），文本 → 对象是反序列化（load 家族）★

在 ch06 学习中，这个方向被口头问反了 5 次（"文件转 json 用 load？"
"load 是序列化？"），是 split/join 之后第二个需要专题锚定的方向病。

运行：python boost/ch06_json_direction.py
建议：先看每段代码，心里预测输出，再运行对答案。
"""

import json
import os
import tempfile

# ══════════════════════════════════════════════════════════
# 第 1 部分：文件不是序列化概念的一部分 —— 两个正交维度
# ══════════════════════════════════════════════════════════

# 序列化本身只管"对象 ↔ json 文本"这一步。
# 文件只是文本的"投递地址"之一（内存里叫字符串，磁盘上叫文件）。
#
# 维度一（方向，二选一）：
#   序列化：对象 → json 文本        （dump / dumps）
#   反序列化：json 文本 → 对象      （load / loads）
# 维度二（产物/原料给谁）：
#   有 s：走字符串，交到你手里 / 由你提供
#   无 s：走文件，Python 直接写盘 / 直接读盘
#
# 组合表：
# ┌────────────┬─────────────────────┬─────────────────────┐
# │            │ 序列化（对象→文本）  │ 反序列化（文本→对象）│
# ├────────────┼─────────────────────┼─────────────────────┤
# │ 走字符串(s) │ dumps：产物=字符串   │ loads：原料=字符串   │
# │ 走文件     │ dump：直接写进文件   │ load：直接从文件读   │
# └────────────┴─────────────────────┴─────────────────────┘

# 1.1 序列化的原料是对象，产物是文本（主语别装反）
data = {"name": "小明", "scores": [90, 85]}
text = json.dumps(data, ensure_ascii=False)
print(text)                       # {"name": "小明", "scores": [90, 85]}
print(type(text).__name__)        # str ← 产物是文本！
# "将字符串序列化"是病句——字符串本来就是文本，已是出门形态，
# 不需要也不能再序列化。序列化的目的：让内存里的活对象能出门（存盘/走网络）。

# 1.2 "X 化 = 使之变成 X"（构词法判方向）
# 绿化=变绿，美化=变美，序列化=变成序列（json 文本）。
# 判据一句话：产物是 json 文本 → 序列化；产物是 Python 对象 → 反序列化。
restored = json.loads(text)       # 产物是 dict → 反序列化
print(type(restored).__name__)    # dict

# 1.3 Go 对照（同一对双胞胎，换了个马甲）
# Marshal      ≈ dumps   对象 → []byte（你拿着）
# Unmarshal    ≈ loads   []byte → 对象
# NewEncoder(f).Encode ≈ dump   对象 → 直接写 io.Writer
# NewDecoder(f).Decode ≈ load   从 io.Reader → 对象
# Go 也有"带文件的序列化"，只是用 NewEncoder(file) 组合，Python 用少个 s 的函数。


# ══════════════════════════════════════════════════════════
# 第 2 部分：return 的有无 —— 产物走哪条通道
# ══════════════════════════════════════════════════════════

# 判断要不要 return，只问一句：新值从哪个通道送出去？
#   通道①【返回值】return → 等号左边的变量接住
#   通道②【副作用】直接写进外部世界（文件、屏幕……）

# 2.1 dump 的成果直接躺在文件里（通道②），无值可交接
tmp = tempfile.gettempdir()
path = os.path.join(tmp, "boost_json_demo.json")
with open(path, "w", encoding="utf-8") as f:
    result_of_dump = json.dump(data, f, ensure_ascii=False, indent=2)
print(result_of_dump)             # None —— dump 没有产物要交接
# 同族：list.sort()、f.write() 都是"活干在别处，返回 None"（ch05 原地方法家族）

# 2.2 load 的产物是内存新对象（通道①），return 是唯一出口
def load_data(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)       # ← 不 return 的话，对象死在函数里，调用方拿到 None
print(load_data(path)["name"])    # 小明

# 2.3 反例：捞出来了但没递出去
def load_data_bad(p):
    with open(p, encoding="utf-8") as f:
        json.load(f)              # ❌ 还原出的 dict 当场蒸发
bad = load_data_bad(path)
print(bad)                        # None（函数没 return 默认返回 None）
# bad["name"] 会 TypeError: 'NoneType' object is not subscriptable


# ══════════════════════════════════════════════════════════
# 第 3 部分：load 返回 dict 还是 list？—— 看文件第一个字符
# ══════════════════════════════════════════════════════════

# json 标准硬规定：顶层只能是 { 或 [。
# load 是"还原剂"：文件顶层长什么样，就还原成什么类型。

# 3.1 顶层 { → dict
p1 = os.path.join(tmp, "boost_json_obj.json")
with open(p1, "w", encoding="utf-8") as f:
    f.write('{"host": "localhost", "port": 8080}')
obj = load_data(p1)
print(type(obj).__name__, obj["port"])     # dict 8080 ← 字典用键取

# 3.2 顶层 [ → list（哪怕元素是字典！）
p2 = os.path.join(tmp, "boost_json_arr.json")
with open(p2, "w", encoding="utf-8") as f:
    f.write('[{"name": "小红"}, {"name": "小明"}]')
arr = load_data(p2)
print(type(arr).__name__, arr[0]["name"])  # list 小红 ← 先下标再键，两步走
# "元素是字典"不等于"整体是字典"——判断只看第一个非空白字符。

# 3.3 Go 视角：Unmarshal 需要先声明 &v 的类型，load 没这个位置，
#     它按文件内容现场决定类型——省了声明，代价是类型藏在文件里。
#     工程习惯：写读文件的代码前，先打开 json 肉眼看顶层结构。


# ══════════════════════════════════════════════════════════
# 第 4 部分：ensure_ascii —— "测试通过"不等于"符合要求"
# ══════════════════════════════════════════════════════════

# 4.1 默认 True：中文全变 \uXXXX 天书
print(json.dumps({"name": "小明"}))        # {"name": "\u5c0f\u660e"}
# 4.2 False：中文原样可读（文件是给人看的）
print(json.dumps({"name": "小明"}, ensure_ascii=False))   # {"name": "小明"}

# 4.3 为什么测试抓不住它：\u 转义是可逆的，往返 == 成立
weird = json.dumps({"name": "小明"})
roundtrip = json.loads(weird)
print(roundtrip == {"name": "小明"})        # True —— 测试能过，文件却不可读
# 工程习惯：存中文必带 ensure_ascii=False, indent=2


# ══════════════════════════════════════════════════════════
# 第 5 部分：Agent 场景 —— 为什么这是 Agent 开发的地基
# ══════════════════════════════════════════════════════════

# 模型 API 的请求与响应全是 json 文本（序列化形态）：
#   你发请求：把参数 dict 序列化（dumps 或库替你做）→ 发出去
#   收响应：  json 字符串 → 反序列化（loads）→ 才能当 dict 操作
# 方向错了就是"把字符串当 dict 用"（TypeError）或"把 dict 直接当文本发"。

# 5.1 模拟一次工具调用响应的处理
fake_response = '{"tool": "search", "args": {"query": "python", "top_k": 3}}'
msg = json.loads(fake_response)             # 反序列化：文本 → 对象
print(msg["tool"], msg["args"]["top_k"])    # search 3 ← 现在才是活数据


# ══════════════════════════════════════════════════════════
# 自测（遮住上面，预测输出再核对）
# ══════════════════════════════════════════════════════════
# Q1: "把 dict 存进文件"用哪个？术语叫什么？  → dump，序列化
# Q2: json.load(f) 返回值的类型由什么决定？    → 文件顶层第一个字符（{→dict，[→list）
# Q3: dump 为什么不需要 return？              → 产物直接写进文件（副作用通道），无值交接
# Q4: loads 里 s 的意思？方向是？             → string；json 字符串 → 对象（反序列化）
# Q5: 存中文漏了什么参数？测试为何抓不住？     → ensure_ascii=False；\u 转义可逆，往返相等
# Q6: "将字符串序列化"这句话错在哪？           → 字符串已是文本（出门形态），序列化的原料只能是对象
