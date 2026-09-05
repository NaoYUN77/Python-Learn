"""exercises.py — boost 加练:标准库弹药房(针对你追问过的知识点)。

覆盖你最近追问过的概念:
缺键工厂 defaultdict · dict 的 key 规矩 · join/split 方向 ·
lambda 当 key · seed 可复现 · assert 断言 · 伪随机。

规矩照旧:import 区自己建(ch09),交卷前扫三查。
做完在项目根目录跑:python -m boost.extras_ch10.test_exercises
"""
from collections import defaultdict
# 练习 1:缺键工厂做计数
# TODO: from collections import defaultdict
# 用 defaultdict(int) 统计每个词出现的次数,返回普通 dict
# count_words("py go py go go") → {'py': 2, 'go': 3}


# 练习 2:元组当 key(坐标查表)
# TODO: 不需要额外 import,普通 dict 即可
# 用"元组当 key"的字典把坐标翻译成地名,查不到返回 "未知地"
# locate([(0, 0)], {(0, 0): "起点"})           → ["起点"]
# locate([(9, 9), (0, 0)], {(0, 0): "起点"})   → ["未知地", "起点"]
def locate(points, place_map):
    # 提示:推导式 + place_map.get(p, "未知地")(get 带默认值,ch05/ch07 的门卫)
    return [place_map.get(p, "未知地") for p in points]


# 练习 3:join 缝合(方向题!谁调用?参数是谁?)
# TODO: 不需要 import
# 把字符串列表用 "-" 缝成一串
# hyphen_join(["2026", "09", "04"]) → '2026-09-04'
def hyphen_join(parts):
    # 提示:缝线在前面调用——"-".join(布片们);别把方向写反!
    return "-".join(parts)

# 练习 4:split 拆解(join 的反义词)
# TODO: 不需要 import
# 把逗号分隔的字符串拆成"去空白后的列表"
# split_trim("py, go ,cat") → ['py', 'go', 'cat']
def split_trim(s):
    # 提示:split(",") 之后每个碎片可能带空格(看 " go "),
    # 对每个碎片 strip() 两端空白——推导式加工厂
    return s.split(" ,")


# 练习 5:lambda 当 key
# TODO: 不需要 import
# 按元组第 1 项(索引 1)从大到小排序,返回排好的列表
# by_score([("甲", 88), ("乙", 95), ("丙", 72)]) → [("乙", 95), ("甲", 88), ("丙", 72)]
def by_score(pairs):
    # 提示:sorted(pairs, key=???) —— key 收一个"加工函数";
    # 从大到小 = reverse=True
    return sorted(pairs, key = lambda p: p[1], reverse=True)


# 练习 6:seed 可复现
# TODO: import random
# 用同一种子抽两次 3 个骰子,返回 [第一次, 第二次](两次必须相等!)
# same_roll(42) → [[6, 1, 1], [6, 1, 1]](具体数字由种子决定)
def same_roll(seed):
    # 提示:random.seed(seed) → 抽 3 个 → 再 seed 同一个 → 再抽 3 个;
    # 抽骰子 = random.randint(1, 6)(两端都含!)
    pass


# 练习 7:数字当 key 的小陷阱
# TODO: 不需要 import
# 往字典里先存 1,再用 1.0 和 True 分别"查"和"存",返回最终字典
# probe_same_key() → {1: 'c'}(想想为什么只有一个键?)
def probe_same_key():
    # 提示:d = {1: "a"};然后 d[1.0] = "b";再 d[True] = "c";return d
    # 1 == 1.0 == True 且哈希相同 → 同一个键,互相覆盖(ch11 追问过的暗坑)
    pass


# 练习 8:assert 当关卡(综合挑战)
# TODO: import random
# 写一个函数:seed 定档后掷 n 颗骰子,用 assert 验证三件事——
#   ① 长度是 n  ② 每颗在 1~6(两端都含) ③ 同种子重掷结果一致
# 三关全过返回 True(写对了 assert 永远不炸,函数安静返回 True)
def verify_dice(seed, n):
    # 提示:random.seed(seed) 抽第一把 r1;再 seed 再抽 r2;
    # assert len(r1) == n, "提示话";assert all(...);assert r1 == r2;最后 return True
    # (assert 条件, "解释" —— 条件炸了才展示解释,ch07 大声失败)
    pass
