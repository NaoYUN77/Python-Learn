"""exercises.py — 第二章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目都来自官方教程第二章的内容（数字、字符串、布尔、类型转换），
做完可以对照 answers.py 看参考代码。
"""


# 练习 1：整除与取余
# 17 秒是多少分多少秒？返回一个元组 (分钟, 秒)
# 提示：// 是整除，% 是取余
def minutes_and_seconds(total_seconds):
    # TODO: 返回 (total_seconds // 60, total_seconds % 60)
    return (total_seconds // 60, total_seconds % 60)


# 练习 2：判断偶数
# 返回 True 或 False，判断 n 是否为偶数
def is_even(n) -> bool:
    # TODO: 用 % 判断
    if n % 2 == 0:
        return True
    else:
        return False

# 练习 3：摄氏转华氏
# 公式：fahrenheit = celsius * 9 / 5 + 32
# 返回 100 摄氏度对应的华氏温度（应为 212.0）
def celsius_to_fahrenheit(celsius):
    # TODO: 按公式计算并返回
    return celsius * 9 / 5 + 32


# 练习 4：字符串清洗
# 把 "  Hello, World  " 去掉两端空格后全部转成大写并返回
def clean_text(text):
    # TODO: 链式调用 strip() 和 upper()
    return text.strip().upper()


# 练习 5：切片
# 返回 word 的前 3 个字符。注意：不能写死 "Pyt"，要用切片
def first_three(word):
    # TODO: 用切片 [0:3]
    return word[0:3]


# 练习 6：切分与拼接
# 把 "2026-09-01" 按 "-" 切开，再用 "/" 拼接，返回 "2026/09/01"
# 提示：split("/") 不对哦，源字符串的分隔符是 "-"
def reformat_date(date_str):
    # TODO: split + join
    # 
    # split是字符串方法.join是分隔字符串的方法
    return "/".join(date_str.split("-"))


# 练习 7：类型转换
# 参数进来是字符串 "3.9"，返回整数 3
# 提示：int("3.9") 会报错，要先转 float
def string_to_int(s):
    # TODO: 两步转换
    return int(float(s))


# 练习 8：f-string 格式化
# 返回字符串 "总价: ¥1234.50"（用 f-string 把 price 格式化为两位小数）
# 注意返回值里有全角冒号和人民币符号，直接照抄模板
def format_price(price):
    # TODO: 用 f"{price:.2f}" 拼进模板
    return f"总价: ¥{price:.2f}"