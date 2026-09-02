"""02_strings.py — 字符串：索引、切片、常用方法、f-string。

运行：python ch02/02_strings.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/introduction.html#strings
"""

# 1. 索引：从 0 开始，负数从末尾往前数
word = "Python"
print(word[0])    # P（第一个字符）
print(word[5])    # n（最后一个字符）
print(word[-1])   # n（倒数第一个）
print(word[-2])   # o（倒数第二个）

# 2. 切片 [start:stop]：含头不含尾
print(word[0:2])  # Py
print(word[2:5])  # tho
print(word[:2])   # Py（省略 start = 从头开始）
print(word[2:])   # thon（省略 stop = 取到末尾）
print(word[-2:])  # on（最后两个字符）
print(word[::-1]) # nohtyP（步长 -1，反转字符串）

# 3. 字符串不可变：不能单独修改某个字符
# word[0] = "J"   # ❌ 报错 TypeError
word = "J" + word[1:]  # ✅ 创建新字符串
print(word)            # Jython

# 4. 长度与重复
print(len(word))      # 6
print("ab" * 3)       # ababab
print("-" * 20)       # 常用来做分隔线

# 5. 常用字符串方法
s = "  Hello, Python World  "
print(s.strip())          # 去掉两端空格
print(s.upper())          # 全部大写
print(s.lower())          # 全部小写
print(s.strip().title())  # 链式调用：Hello, Python World

csv = "apple,banana,cherry"
fruits = csv.split(",")   # 按逗号切成列表
print(fruits)             # ['apple', 'banana', 'cherry']
print(", ".join(fruits))  # 再拼回字符串：apple, banana, cherry
print(csv.replace("banana", "orange"))

print("hello".startswith("he"))  # True
print("hello".find("llo"))       # 2（首次出现的索引，找不到返回 -1）
print("123".isdigit())           # True（是否全是数字字符）

# 6. f-string：格式化字符串（最推荐）
name = "Alice"
age = 25
pi = 3.14159

print(f"我叫{name}，今年{age}岁")  # {} 里直接放变量
print(f"明年我 {age + 1} 岁")      # 也可以放表达式
print(f"圆周率约等于 {pi:.2f}")    # 3.14  保留 2 位小数
print(f"{name:>10}!")              # 右对齐，宽度 10
print(f"{name:<10}!")              # 左对齐
print(f"{1234567:,}")              # 1,234,567 千分位