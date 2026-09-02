"""answers.py — 第三章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""


# 练习 1
def grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


# 练习 2
def fizzbuzz(n):
    if n % 15 == 0:          # 同时被 3 和 5 整除 = 被 15 整除，也可以写 n % 3 == 0 and n % 5 == 0
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


# 练习 3
def sum_even(limit):
    total = 0
    for i in range(2, limit + 1, 2):   # 从 2 开始，步长 2，含 limit 本身
        total += i
    return total


# 练习 4
def count_vowels(text):
    count = 0
    for ch in text:
        if ch in "aeiou":
            count += 1
    return count


# 练习 5
def find_first_divisor(n):
    for m in range(2, n):
        if n % m == 0:
            return m         # return 会立刻结束函数，效果等同 break
    return None              # 循环跑完都没找到，说明是质数


# 练习 6
def guess_game(target, guesses):
    i = 0
    while True:
        if guesses[i] == target:
            return i + 1     # 次数从 1 开始数
        i += 1


# 练习 7
def countdown(n):
    results = []
    while n > 0:
        results.append(n)
        n -= 1
    return results


# 练习 8
def dispatch(command):
    match command:
        case "start":
            return "启动"
        case "stop":
            return "停止"
        case "help" | "h":
            return "帮助"
        case _:
            return "未知命令"


if __name__ == "__main__":
    # 运行参考代码，看看效果
    print(grade(85))
    print(fizzbuzz(15), fizzbuzz(9), fizzbuzz(10), fizzbuzz(7))
    print(sum_even(100))
    print(count_vowels("hello"))
    print(find_first_divisor(15), find_first_divisor(7))
    print(guess_game(42, [10, 50, 42]))
    print(countdown(5))
    print(dispatch("help"), dispatch("hack"))
