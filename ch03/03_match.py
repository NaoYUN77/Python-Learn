"""03_match.py — match/case 结构化分支（Python 3.10+）。

运行：python ch03/03_match.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#match-statements
"""

# 1. 基本形式：match 值，case 列出可能的选项
def http_message(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:                  # 兜底，相当于 else
            return "未知状态码"

print(http_message(200))   # OK
print(http_message(404))   # Not Found
print(http_message(999))   # 未知状态码

# 2. 多个值命中同一分支：用 | （或模式）
def is_weekend(day):
    match day:
        case "sat" | "sun":
            return True
        case "mon" | "tue" | "wed" | "thu" | "fri":
            return False
        case _:
            return None    # 无效输入

print(is_weekend("sun"))   # True
print(is_weekend("mon"))   # False
print(is_weekend("abc"))   # None

# 3. 带 if 守卫（guard）：case 后面可以再接条件
def classify(n):
    match n:
        case 0:
            return "零"
        case x if x < 0:     # 命中"不是 0 的数"后再判断是否小于 0
            return "负数"
        case x if x % 2 == 0:
            return "正偶数"
        case _:
            return "正奇数"

print(classify(0))     # 零
print(classify(-5))    # 负数
print(classify(8))     # 正偶数
print(classify(7))     # 正奇数

# 4. 简单计算器：按运算符分发（和 if/elif 版本对比一下）
def calc(a, op, b):
    match op:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            if b == 0:
                return "除数不能为 0"   # case 块里照样可以嵌套 if
            return a / b
        case _:
            return f"不支持的运算符 {op}"

print(calc(6, "*", 7))    # 42
print(calc(1, "/", 0))    # 除数不能为 0

# 5. 💡 为什么 Agent 开发离不开它：按用户指令/工具名分发
def dispatch(command):
    match command:
        case "search" | "s":
            return "调用搜索工具"
        case "run" | "r":
            return "执行命令"
        case "exit":
            return "结束会话"
        case _:
            return "未知指令"

for cmd in ["search", "run", "exit", "hack"]:
    print(f"{cmd:>8} -> {dispatch(cmd)}")
