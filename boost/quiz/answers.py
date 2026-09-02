"""answers.py — 前五章复习测验参考答案。

先自己做完 exercises.py，再对照这里。
"""

from . import exercises  # noqa: F401  (演示用，运行本文件需要包上下文)


# 题目 1
def safe_sort(numbers):
    return sorted(numbers)          # sorted 返回新列表，原列表不动
    # 错误示范：return numbers.sort()  ← 返回 None！


# 题目 2a
def evens(limit):
    return [x for x in range(limit) if x % 2 == 0]     # if 在后 = 过滤


# 题目 2b
def labels(nums):
    return ["偶" if x % 2 == 0 else "奇" for x in nums]  # 三元在前 = 加工


# 题目 3a
def char_counts(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


# 题目 3b
def rare_chars(text, n):
    counts = exercises.char_counts(text)   # 复用 3a：组合思维
    result = []
    seen = set()
    for ch in text:                        # 遍历原字符串保住出现顺序
        if counts[ch] < n and ch not in seen:
            result.append(ch)
            seen.add(ch)
    return result


if __name__ == "__main__":
    print(safe_sort([3, 1, 2]))            # [1, 2, 3]
    print(evens(6))                        # [0, 2, 4]
    print(labels([1, 2, 3]))               # ['奇', '偶', '奇']
    print(char_counts("aab"))              # {'a': 2, 'b': 1}
    print(rare_chars("abracadabra", 2))    # ['c', 'd']
