"""answers.py — 第二章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""


# 练习 1
def minutes_and_seconds(total_seconds):
    return (total_seconds // 60, total_seconds % 60)


# 练习 2
def is_even(n):
    return n % 2 == 0


# 练习 3
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


# 练习 4
def clean_text(text):
    return text.strip().upper()


# 练习 5
def first_three(word):
    return word[0:3]


# 练习 6
def reformat_date(date_str):
    parts = date_str.split("-")
    return "/".join(parts)
    # 也可以一行：return "/".join(date_str.split("-"))


# 练习 7
def string_to_int(s):
    return int(float(s))


# 练习 8
def format_price(price):
    return f"总价: ¥{price:.2f}"


if __name__ == "__main__":
    # 运行参考代码，看看效果
    print(minutes_and_seconds(125))
    print(is_even(4), is_even(7))
    print(celsius_to_fahrenheit(100))
    print(clean_text("  Hello, World  "))
    print(first_three("Python"))
    print(reformat_date("2026-09-01"))
    print(string_to_int("3.9"))
    print(format_price(1234.5))
