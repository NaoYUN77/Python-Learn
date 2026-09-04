"""05_datetime_stats.py — datetime 计日期 + statistics 一行出统计

运行:python ch10/05_datetime_stats.py
第 1 段的"今天"以你跑的那天为准。
README 对照:10.4 / 10.5
"""

from datetime import date, timedelta
import statistics

print("== 1. 日期是对象:能减、能加 ==")
today = date.today()
print("今天:", today)                          # 例如 2026-09-04
gap = date(2027, 1, 1) - today                 # date − date → timedelta
print("距 2027 元旦:", gap.days, "天")          # .days 是 timedelta 的属性
print("100 天后:", today + timedelta(days=100))

print()
print("== 2. strftime:日期 → 字符串(format 出去) ==")
print(today.strftime("%Y-%m-%d"))              # 例如 2026-09-04
print(today.strftime("%Y 年 %m 月 %d 日"))      # 月日自动补零(%m → 09)
# 方向题:strftime 出(format)、strptime 进(parse),和 json dump/load 同款梗

print()
print("== 3. statistics:一行出统计 ==")
scores = [88, 92, 79, 93, 85]
print("平均:", statistics.mean(scores))         # 87.4
print("中位数:", statistics.median(scores))     # 88(奇数个,正好站中间)
try:
    statistics.mean([])
except statistics.StatisticsError as e:
    print("空列表不给算:", e)
    # ← ch07:标准库也按型号抛异常;文档 Raises 段 = 危险行清单
