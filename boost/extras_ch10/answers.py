"""answers.py — boost 加练参考答案。

先自己做完 exercises.py,再对照这里。
"""

from collections import defaultdict
import random


# 练习 1:int 工厂做计数(缺键自动给 0,+1 完事)
def count_words(text):
    counts = defaultdict(int)
    for w in text.split():
        counts[w] += 1
    return dict(counts)


# 练习 2:元组当 key,get 带默认值当门卫
def locate(points, place_map):
    return [place_map.get(p, "未知地") for p in points]


# 练习 3:缝线在前面调用
def hyphen_join(parts):
    return "-".join(parts)


# 练习 4:拆完顺手 strip(推导式加工厂)
def split_trim(s):
    return [piece.strip() for piece in s.split(",")]


# 练习 5:lambda 说"按什么排",reverse 管方向
def by_score(pairs):
    return sorted(pairs, key=lambda p: p[1], reverse=True)


# 练习 6:同种子读同一档
def same_roll(seed):
    random.seed(seed)
    first = [random.randint(1, 6) for _ in range(3)]
    random.seed(seed)
    second = [random.randint(1, 6) for _ in range(3)]
    return [first, second]


# 练习 7:1 == 1.0 == True → 同一个键,后写覆盖先写
def probe_same_key():
    d = {1: "a"}
    d[1.0] = "b"      # 覆盖 {1: "a"}(不是新增!)
    d[True] = "c"     # 再覆盖
    return d          # {1: 'c'}


# 练习 8:assert 三关卡,全过安静返回 True
def verify_dice(seed, n):
    random.seed(seed)
    r1 = [random.randint(1, 6) for _ in range(n)]
    random.seed(seed)
    r2 = [random.randint(1, 6) for _ in range(n)]
    assert len(r1) == n, f"应掷 {n} 次,实际 {len(r1)} 次"
    assert all(1 <= x <= 6 for x in r1), f"有点数越界(两端都含!),实际 {r1}"
    assert r1 == r2, f"同一种子应同序列,{r1} vs {r2}"
    return True


if __name__ == "__main__":
    print(count_words("py go py go go"))                 # {'py': 2, 'go': 3}
    print(locate([(9, 9), (0, 0)], {(0, 0): "起点"}))     # ['未知地', '起点']
    print(hyphen_join(["2026", "09", "04"]))             # 2026-09-04
    print(split_trim("py, go ,cat"))                     # ['py', 'go', 'cat']
    print(by_score([("甲", 88), ("乙", 95), ("丙", 72)]))
    # [('乙', 95), ('甲', 88), ('丙', 72)]
    print(same_roll(42))                                 # [[6, 1, 1], [6, 1, 1]]
    print(probe_same_key())                              # {1: 'c'}
    print(verify_dice(42, 10))                           # True
