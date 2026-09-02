"""exercises.py — 第六章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目围绕官方教程第 7 章（输入输出与文件）：
print 参数、input 转换、文件读写、with 语句、json 四兄弟。
做完可以对照 answers.py 看参考代码。

⚠️ 所有文件操作的函数都用 with 语句——这是本章的铁律。
"""


# 练习 1：格式化打印日期
# format_date(2026, 9, 1) 返回 "2026-09-01"（月日补零成两位）
# 提示：f"{m:02d}" 补零；return 字符串而不是 print
import json


def format_date(y, m, d):
    # TODO: 一行 return，用 f-string 的 :02d 格式
    return f"{y:04d}-{m:02d}-{d:02d}"

# 练习 2：安全读数字
# 输入字符串 "42" → 返回 42；输入 "abc" → 返回 None（不崩溃）
# 提示：try: int(s) except ValueError: return None（异常处理下章细讲，先照用）
# try:
#     危险操作
# except 具体错误类型:
#     兜底处理


def parse_int(s):
    # TODO: try 里转换并 return，except 里 return None
    try:
        return int(s)
    except ValueError:
        return None


# 练习 3：解析一行数字（input 的黄金搭档）
# "3 5 8" → [3, 5, 8]；"" → []；"7" → [7]
# 提示：split() 切开 + 推导式逐个 int（01_print_input.py 第 6 段）
def parse_numbers(line):
    # TODO: 一行推导式
    return [int(s) for s in line.split()]


# 练习 4：写文本文件
# write_lines(path, lines) 把列表逐行写入文件，每行以 \n 结尾
# write_lines("t.txt", ["a", "b"]) 后文件内容是 "a\nb\n"
# 提示：with open(path, "w", encoding="utf-8") + f.write(f"{line}\n")，或 writelines
def write_lines(path, lines):
    # TODO: with + 循环写入
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")


# 练习 5：读文件并去掉空行
# read_nonempty(path) 返回去掉首尾空白后非空的行组成的列表
# 内容 "a\n\n b \nc\n" → ["a", "b", "c"]
# 提示：with + for line in f + line.strip() + 非空才 append
def read_nonempty(path):
    # TODO: with + 篮子模式
    result = []
    with open(path,encoding="utf-8") as f :
        for line in f :
            line = line.strip()
            if line: 
                result.append(line)
    return result
# 练习 6：统计文件行数与字数
# file_stats(path) → (行数, 单词数)；"a b\n c\n" → (2, 3)
# 提示：两个计数器；每行 line.split() 得到该行单词列表，len() 累加
def file_stats(path):
    # TODO: with + 双计数器，return 两个值（元组）
    with open(path,encoding="utf-8") as f : 
        line_count = 0 
        word = 0 
        for line in f :
            if line:
                line_count += 1
                word += len(line.split())
    return line_count, word  #返回一个元组


# 练习 7：json 存取（方向题！）
# save_data(path, data) 把任意 dict/list 存成 json 文件
# 提示：对象 → 文件用哪个函数？想清楚方向再写（dumps/dump 只差一个 s）
def save_data(path, data):
    # TODO: with + json.???
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 练习 8：json 读取（方向题！）
# load_data(path) 把 json 文件读回 Python 对象
# 提示：文件 → 对象用哪个函数？
def load_data(path):  #为什么要返回?  load不是将json反序列化直接写入文件中了吗
    # TODO: with + json.???
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 练习 9：合并配置（综合）
# merge_configs(path_a, path_b, out_path)：读两个 json 配置文件，
# 合并字典（b 的键覆盖 a 的同名键），存到 out_path
# 提示：练习 8 读两次 → {**a, **b} 合并（双星号解包字典）→ 练习 7 写回
def merge_configs(path_a, path_b, out_path):
    # TODO: 读 a、读 b、合并、写回
    a_load = load_data(path_a)
    b_load = load_data(path_b)
    merged = {**a_load, **b_load}
    save_data(out_path, merged)
