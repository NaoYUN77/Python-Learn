"""01_if.py — 条件分支：if / elif / else。

运行：python ch03/01_if.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#if-statements
"""

# 1. 基本结构：冒号 + 缩进（4 个空格）
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:          # elif = else if，从上往下只走第一个命中的分支
    print("良好")           # ← 85 走这里
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 2. 条件组合：and / or / not
age, has_ticket = 20, True
if age >= 18 and has_ticket:
    print("可以入场")       # 两个条件都满足才执行

if age < 12 or age >= 65:
    print("优惠票")
else:
    print("全价票")

# 3. 链式比较（Python 特有的简洁写法）
if 0 <= score <= 100:
    print("分数在合法范围内")

# 4. in 判断成员关系
word = "python"
if "py" in word:
    print("包含 py 子串")

# 5. 真假值：空字符串是假值，不要写 if name == ""
name = ""
if not name:
    print("名字没填")

# 6. 嵌套：分支里面还可以再 if（嵌套太深不好读，能合并就合并）
n = 15
if n > 0:
    if n % 2 == 0:
        print("正偶数")
    else:
        print("正奇数")

# 7. 重要化简：比较的结果本身就是布尔值
#    ❌ 啰嗦写法（你 ch02 练习 2 的写法）：
#    if n % 2 == 0:
#        return True
#    else:
#        return False
#    ✅ 一行就够：
is_even = (n % 2 == 0)
print(f"{n} 是偶数吗？{is_even}")
