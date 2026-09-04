"""06_regex_intro.py — re 三板斧 — findall / search / sub。

运行:python ch10/06_regex_intro.py
正则 = 用一行模式描述"长什么样的文本"。输出全部确定,可对照。
"""

import re

print("=== re 三板斧 ===\n")

# ── 先懂 r"":别让 Python 先吃掉反斜杠 ──
print("正常字符串 \"a\\td\" :", "a\td")    # \t 已被 Python 变成真制表符(中间是空的)
print(r"原始字符串 r\"a\td\" :", r"a\td")  # r"" 原样保留,反斜杠还在
print("→ 写正则一律加 r 前缀,让 \\d 完整交给 re\n")

# ── 板斧一:findall —— 所有匹配,给字符串列表 ──
order = "订单 1001 和 1002,共 2 件,实付 88.5 元"
hits = re.findall(r"\d+", order)
print(f"原文:{order}")
print(f"findall(r'\\d+', ...) = {hits}")
print("  ← 是字符串列表!要数字自己 int() 转换(input 永远 str,同款道理)\n")

# ── 板斧二:search —— 第一个匹配,给个对象 ──
m = re.search(r"\d+", order)
print(f"search 找第一个:m.group() = {m.group()!r},位置 {m.start()}~{m.end()}")
print(f"search 找不到时返回 {re.search(r'x', order)}   ← None,常配 if 判断\n")

# ── 板斧三:sub —— 全部替换,返回新字符串 ──
masked = re.sub(r"\d", "*", order)
print(f"sub(r'\\d', '*', ...) = {masked}\n")

# ── 常用符号速览 ──
print(f"\\d 数字:     {re.findall(r'\\d+', 'abc123def456')}")
print(f"\\w 单词字符: {re.findall(r'\\w+', 'py_3.12 rocks')}")
print(f"\\s 空白:     {re.findall(r'\\s', 'a b\\tc')}")

# 预期输出:
# === re 三板斧 ===
#
# 正常字符串 "a\td" : a	d
# 原始字符串 r"a\td" : a\td
# → 写正则一律加 r 前缀,让 \d 完整交给 re
#
# 原文:订单 1001 和 1002,共 2 件,实付 88.5 元
# findall(r'\d+', ...) = ['1001', '1002', '2', '88', '5']
#   ← 是字符串列表!要数字自己 int() 转换(input 永远 str,同款道理)
#
# search 找第一个:m.group() = '1001',位置 3~7
# search 找不到时返回 None   ← None,常配 if 判断
#
# sub(r'\d', '*', ...) = 订单 **** 和 ****,共 * 件,实付 **.* 元
#
# \d 数字:     ['123', '456']
# \w 单词字符: ['py_3', '12', 'rocks']
# \s 空白:     [' ', '\t']
