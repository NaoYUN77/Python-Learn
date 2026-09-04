"""07_timeit_race.py — timeit 竞速:别猜,要测。

运行:python ch11/07_timeit_race.py
问题:查"9999 在不在 10000 个数里",列表和集合谁快?
先自己猜,再看结果(数字每次会变,量级不会)。
"""

import timeit

xs = list(range(10000))    # 列表:有序队伍,查人要从头扫到尾
ss = set(xs)               # 集合:哈希表,报门牌号直达(ch05 的伏笔)

N = 1000
t_list = timeit.timeit(lambda: 9999 in xs, number=N)
t_set = timeit.timeit(lambda: 9999 in ss, number=N)

print(f"=== 「9999 在不在?」各查 {N} 次 ===\n")
print(f"list 成员检查总耗时 = {t_list:.6f} 秒")
print(f"set  成员检查总耗时 = {t_set:.6f} 秒")
print(f"\n集合快了约 {t_list / t_set:.0f} 倍")
print("列表查成员 = 从头扫到尾;集合 = 哈希表直查")
print("用法观:先跑通,再谈快;要谈快,先 timeit")

# 预期输出(数字每次会变,量级不变;本机实测约 1400 倍):
# === 「9999 在不在?」各查 1000 次 ===
#
# list 成员检查总耗时 = 0.087101 秒
# set  成员检查总耗时 = 0.000061 秒
#
# 集合快了约 1416 倍
# 列表查成员 = 从头扫到尾;集合 = 哈希表直查
# 用法观:先跑通,再谈快;要谈快,先 timeit
