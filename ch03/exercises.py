"""exercises.py — 第三章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目都来自官方教程第四章（控制流）的内容：
if/elif/else、for+range、while、break/continue、循环 else、match。
做完可以对照 answers.py 看参考代码。
"""


# 练习 1：成绩分级
# score >= 90 返回 "优秀"；>= 80 返回 "良好"；>= 60 返回 "及格"；否则 "不及格"
from sqlite3.dbapi2 import SQLITE_DBCONFIG_RESET_DATABASE


def grade(score):
    # TODO: if / elif / else
    if score >= 90 :
        return "优秀"
    elif score >= 80 :
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


# 练习 2：FizzBuzz（经典面试题）
# n 同时被 3 和 5 整除 → 返回 "FizzBuzz"
# 只被 3 整除 → "Fizz"；只被 5 整除 → "Buzz"
# 都不满足 → 返回数字本身转成字符串，如 "7"
# 提示：ch02 的 % 和 str() 都用得上；注意判断顺序，先判断"同时整除"
def fizzbuzz(n):
    # TODO: if/elif/else + 取余
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


# 练习 3：累加偶数
# 用 for + range() 计算 2 + 4 + 6 + ... + limit 的和并返回
# sum_even(100) 应返回 2550
# 提示：range(2, limit + 1, 2)，别忘了 range 含头不含尾
def sum_even(limit):
    # TODO: 累加器结构
    total = 0
    for num in range(2, limit + 1, 2):
        total += num
    return total


# 练习 4：数元音字母
# 统计字符串里 a e i o u（小写）出现的次数并返回
# count_vowels("hello") 应返回 2
# 提示：for 遍历字符串 + if ch in "aeiou" + 计数器
def count_vowels(text):
    # TODO: 计数器结构
    # 
    count = 0
    for s in text:
        if s in "aeiou":
            count += 1
    return count
    


# 练习 5：找最小因子（用循环的 else）
# 找出 n（n >= 2）最小的因子（大于 1 且能整除 n 的数），找到就返回它
# 如果找不到（说明 n 是质数），返回 None
# find_first_divisor(15) → 3；find_first_divisor(7) → None
# 提示：for m in range(2, n): if n % m == 0: return m；循环后 return None
#       （用 return 提前退出，效果和 break 一样）
def find_first_divisor(n):
    # TODO: for + if + return，循环结束后 return None
    for m in range(2, n):
        if n % m == 0:
            return m 
    return None


# 练习 6：猜数字（while + break）
# guesses 是一串猜测，从第一个开始逐个和 target 比，返回第几次猜中（从 1 开始数）
# guess_game(42, [10, 50, 42]) 应返回 3
# 题目保证 target 一定在 guesses 里
# 提示：while True + 下标 i + if 命中就 break；i 从 0 开始，返回时要 +1
def guess_game(target, guesses):
    # TODO: while True 循环
    i = 0
    while True: 
        if guesses[i] == target : 
            return i + 1
        i  += 1
        
                

# 练习 7：倒计时
# 用 while 循环返回 [n, n-1, ..., 2, 1]
# countdown(5) 应返回 [5, 4, 3, 2, 1]
# 提示：先 results = []，循环里 results.append(数字)（append 是"往列表末尾加东西"）
def countdown(n):
    # TODO: while n > 0
    results = [] 
    while n  > 0 :
        results.append(n)
        n -= 1
    return results


# 练习 8：指令分发（match/case，需要 Python 3.10+）
# "start" → "启动"；"stop" → "停止"；"help" 或 "h" → "帮助"；其他 → "未知命令"
def dispatch(command):
    # TODO: match command: case ...
    match command:
        case "start":
            return "启动"
        case "stop":
            return "停止"
        case "help" | "h":
            return "帮助"
        case _:
            return "未知命令"
            
