"""01_hello.py — 最基础的打印输出示例。

运行：python ch01/01_hello.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/introduction.html
"""

# 1. 第一个程序
print("Hello, World!")

# 2. 数字运算（Python 会直接打印结果）
print(1 + 1)        # 加法
print(10 - 3)       # 减法
print(4 * 5)        # 乘法
print(20 / 5)       # 除法，结果是小数（浮点数）

# 3. 同时打印多个内容，用逗号分隔（会自动加空格）
print("我的年龄是", 25)

# 4. 单引号 / 双引号都可以包字符串
print('今天是晴天')
print("今天去爬山")

# 5. 换行符 \n 和制表符 \t
print("第一行\n第二行")      # \n 换行
print("目录:\n\t学习\n\t编程")  # \t 缩进

# 6. 用引号打印引号：单引号里用双引号，或反过来
print('他说："你好"')
print("她说：'加油'")

# 7. 字符串之间的加法（拼接）
print("名字:" + " 张伟")