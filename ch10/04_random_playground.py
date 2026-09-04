"""04_random_playground.py — random 游乐场 — 随机,但可复现。

运行:python ch10/04_random_playground.py
看点:上半段每次跑都不一样(这才叫随机),
seed 那两轮一模一样——同种子必同果。
"""

import random

print("=== random 游乐场 ===\n")

# ── 五连(结果每次跑都不一样——这才叫随机) ──
print(f"random()        = {random.random()}   ← [0, 1) 随机小数")
print(f"randint(1, 6)   = {random.randint(1, 6)}   ← 掷骰子,含头含尾(和 range 相反!)")
print(f"choice(猜拳)    = {random.choice(['石头', '剪刀', '布'])}")
print(f"sample(1~49, 6) = {random.sample(range(1, 50), 6)}   ← 不重复抽 6 个")

# ── shuffle 是原地方法(呼应 ch05:原地返回 None) ──
deck = ["红桃A", "黑桃K", "方块Q", "梅花J"]
shuffled = list(deck)        # 先复制!
random.shuffle(shuffled)     # 原地洗,返回 None
print(f"\n原牌堆   = {deck}")
print(f"洗好的牌 = {shuffled}   ← 洗的是副本")
print(f"shuffle 的返回值 = {random.shuffle([1])!r}   ← None,别拿它接结果")

# ── seed:随机界的"存档点" ──
random.seed(42)
first = [random.randint(1, 6) for _ in range(3)]
random.seed(42)
second = [random.randint(1, 6) for _ in range(3)]
print(f"\nseed(42) 第一轮 = {first}")
print(f"seed(42) 第二轮 = {second}   ← 一模一样!")
print("随机数是伪随机:从种子按固定算法走,路线完全确定")
print("→ 测试/调试前 seed 一下,失败才复现得了;真要不可预测(抽奖)才不 seed")

# 预期输出(上半段每次都变;seed 两轮固定 [6, 1, 1],本机实测):
# === random 游乐场 ===
#
# random()        = 0.40166935406358896   ← [0, 1) 随机小数
# randint(1, 6)   = 3   ← 掷骰子,含头含尾(和 range 相反!)
# choice(猜拳)    = 布
# sample(1~49, 6) = [17, 41, 8, 29, 2, 44]   ← 不重复抽 6 个
#
# 原牌堆   = ['红桃A', '黑桃K', '方块Q', '梅花J']
# 洗好的牌 = ['梅花J', '红桃A', '黑桃K', '方块Q']   ← 洗的是副本
# shuffle 的返回值 = None   ← None,别拿它接结果
#
# seed(42) 第一轮 = [6, 1, 1]
# seed(42) 第二轮 = [6, 1, 1]   ← 一模一样!
# 随机数是伪随机:从种子按固定算法走,路线完全确定
# → 测试/调试前 seed 一下,失败才复现得了;真要不可预测(抽奖)才不 seed
