"""01_print_input.py — print 进阶与 input。

运行：python ch06/01_print_input.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#fancier-output-formatting
"""

# 1. print 的隐藏参数：sep / end
print("2026", "09", "01")                # 2026 09 01（默认空格连接）
print("2026", "09", "01", sep="-")       # 2026-09-01（自定义分隔符）
print("加载中", end="")                   # end=""：不换行，下一个 print 接着写
print("...完成")                          # 加载中...完成（同一行！）

# 2. 进度条的原型就是 end=""
import time
for i in range(3):
    print(f"\r进度 {i + 1}/3", end="")    # \r 回到行首覆盖重画
    time.sleep(0.3)
print()                                   # 最后补个换行

# 3. f-string 格式化进阶
pi = 3.14159
print(f"{pi:.2f}")                        # 3.14（两位小数）
print(f"{1234567:,}")                     # 1,234,567（千分位）
print(f"{0.256:.0%}")                     # 26%（百分比，自动乘 100 取整）
width = 7
print(f"[{'标题':^{width}}]")             # [  标题  ]（居中对齐，中文占 2 格有点歪无妨）
name = "小明"
print(f"{name=}")                         # name='小明'（调试：变量名和值一起打）

# 4. input：从用户读输入（本文件演示用固定值代替，交互版见注释）
# name = input("你叫什么？")              # input 返回的【永远是字符串】
# age = int(input("几岁？"))               # 要算术必须先转换

# 模拟用户输入了 "10"：
raw = "10"
print(type(raw).__name__)                 # str ← 就算输入的是数字！
age = int(raw) + 1                        # 转换后才能算术
print(age)                                # 11

# 5. 不转换的下场（经典报错）
try:
    "10" + 5
except TypeError as e:
    print("报错:", e)                     # can only concatenate str (not "int") to str

# 6. 多值输入的常用套路：split + 转换（把 input 的字符串拆成多个数）
line = "3 5 8"
nums = [int(x) for x in line.split()]     # split() 默认按空白切 → 推导式逐个转 int
print(nums)                               # [3, 5, 8]
