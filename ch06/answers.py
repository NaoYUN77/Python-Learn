"""answers.py — 第六章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""

import json


# 练习 1
def format_date(y, m, d):
    return f"{y:04d}-{m:02d}-{d:02d}"          # :02d 补零到两位


# 练习 2
def parse_int(s):
    try:
        return int(s)
    except ValueError:                          # 转不动说明不是数字
        return None


# 练习 3
def parse_numbers(line):
    return [int(x) for x in line.split()]       # split() 空串返回 []，天然处理空输入


# 练习 4
def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")                # write 不自动换行，自己补


# 练习 5
def read_nonempty(path):
    result = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()             # 去掉首尾空白（含 \n）
            if stripped:                        # 空字符串是假值
                result.append(stripped)
    return result


# 练习 6
def file_stats(path):
    line_count = 0
    word_count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            word_count += len(line.split())     # split 后的个数就是单词数
    return line_count, word_count               # 逗号打包成元组


# 练习 7
def save_data(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)   # 对象 → 文件：dump


# 练习 8
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)                     # 文件 → 对象：load


# 练习 9
def merge_configs(path_a, path_b, out_path):
    a = load_data(path_a)
    b = load_data(path_b)
    merged = {**a, **b}                         # 双星号解包合并，b 在后覆盖同名键
    save_data(out_path, merged)


if __name__ == "__main__":
    print(format_date(2026, 9, 1))
    print(parse_int("42"), parse_int("abc"))
    print(parse_numbers("3 5 8"), parse_numbers(""))

    import os
    import tempfile
    tmp = tempfile.gettempdir()

    write_lines(os.path.join(tmp, "demo.txt"), ["a", "b"])
    print(read_nonempty(os.path.join(tmp, "demo.txt")))

    p = os.path.join(tmp, "demo.json")
    save_data(p, {"name": "小明", "scores": [90, 85]})
    print(load_data(p))

    pa = os.path.join(tmp, "a.json")
    pb = os.path.join(tmp, "b.json")
    out = os.path.join(tmp, "out.json")
    save_data(pa, {"host": "a", "port": 80})
    save_data(pb, {"port": 8080, "debug": True})
    merge_configs(pa, pb, out)
    print(load_data(out))
