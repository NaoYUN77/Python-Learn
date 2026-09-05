"""02_collections.py — collections 漫游:Counter / defaultdict / deque

运行:python ch10/02_collections.py
README 对照:10.2
"""

from collections import Counter, defaultdict, deque

print("== 1. Counter:ch05 计数模式的一行版 ==")
counts = Counter("abracadabra")
print(counts)                    # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print(counts.most_common(2))     # [('a', 5), ('b', 2)] ← 次数从多到少
print(counts["z"])               # 0 ← 缺键不炸,普通 dict 会 KeyError
print(type(counts).__name__)     # Counter ← 它是 dict 的子类(ch08:"是一种" dict)

print()
print("== 2. defaultdict:缺键自动建值 ==")
groups = defaultdict(list)       # 缺键工厂:缺键自动调 list() 造空列表
for w in ["apple", "banana", "avocado"]:
    groups[w[0]].append(w)       # 不用 setdefault,直接 append
print(dict(groups))              # {'a': ['apple', 'avocado'], 'b': ['banana']}
# ch05 对照:groups.setdefault(w[0], []).append(w) —— 同一个模式,少一层心累

print()
print("== 3. deque:两头都能进出的队列 ==")
line = deque(["甲", "乙", "丙"])
line.append("丁")                # 队尾进
first = line.popleft()           # 队头出(瞬间完成;list.pop(0) 要搬全家当)
print(first, list(line))         # 甲 ['乙', '丙', '丁']
# (预告:Agent 框架的"消息历史"经常就是 deque——ch12 会见)
