"""02_files.py — 文件读写：open 三步、三种读法、模式与编码。

运行：python ch06/02_files.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files

本脚本会在 ch06/ 目录下创建/读写 demo.txt，可反复运行。
"""

# 1. 写文件三步：open → write → close
f = open("ch06/demo.txt", "w", encoding="utf-8")   # "w"：没有就创建，有就清空！
f.write("第一行：Python 文件读写\n")                 # write 不自动换行，\n 自己写
f.write("第二行：今天天气不错\n")
f.close()                                          # 用完必须关
print("已写入 demo.txt")

# 2. 追加模式 "a"：不清空，接着写
f = open("ch06/demo.txt", "a", encoding="utf-8")
f.write("第三行：追加进来的\n")
f.close()

# 3. 读法一：read() 一次读整个文件
f = open("ch06/demo.txt", "r", encoding="utf-8")
content = f.read()                                 # 一个大字符串（含 \n）
f.close()
print("--- read() ---")
print(content)

# 4. 读法二：readlines() 每行一个元素
f = open("ch06/demo.txt", "r", encoding="utf-8")
lines = f.readlines()                              # ['第一行...\n', '第二行...\n', ...]
f.close()
print("--- readlines() ---")
print(lines, len(lines))                           # 3 行

# 5. 读法三：逐行遍历（推荐，大文件省内存）
f = open("ch06/demo.txt", "r", encoding="utf-8")
print("--- 逐行 ---")
for line in f:                                     # 每轮 line 是一行（带 \n）
    print("这行内容:", line.strip())                # strip() 去掉首尾的换行符
f.close()

# 6. ⚠️ "w" 的危险：再开一次 "w"，内容全没了
f = open("ch06/demo.txt", "w", encoding="utf-8")
f.write("被清空重写了\n")
f.close()
f = open("ch06/demo.txt", "r", encoding="utf-8")
print("--- 被 w 清空后 ---")
print(f.read())                                    # 只剩一句
f.close()

# 7. 手动 close 的坑：中途出异常，close 永远执行不到
def buggy_write():
    f = open("ch06/demo.txt", "w", encoding="utf-8")
    f.write("写了一半\n")
    raise RuntimeError("程序炸了！")                 # close() 没执行 → 文件句柄泄漏
    f.close()                                      # 永远到不了这行（且是死代码）

try:
    buggy_write()
except RuntimeError as e:
    print("捕获:", e)
# 这就是下一节 with 语句要解决的问题
