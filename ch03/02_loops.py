"""02_loops.py — 循环：for / while / break / continue。

运行：python ch03/02_loops.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#for-statements
"""

# 1. for + range()：range 含头不含尾，和切片一致
for i in range(5):          # 0 1 2 3 4
    print(i, end=" ")
print()

for i in range(1, 10, 2):   # 1 3 5 7 9（步长 2）
    print(i, end=" ")
print()

# 2. 遍历字符串
for ch in "你好":
    print(ch)

# 3. 经典结构：累加器（先在循环外定义 total = 0，循环里 total += i）
total = 0
for i in range(1, 101):
    total += i
print("1 到 100 的和:", total)   # 5050

# 4. while：不知道循环几次，只知道"什么时候停"
count = 0
while count < 3:
    print("while 第", count, "次")
    count += 1              # 忘了这行 = 死循环（Ctrl+C 可中断）

# 5. while True + break：一直运行，直到满足条件才退出
secret = 42
guesses = [10, 50, 42]      # 模拟用户的三次输入
i = 0
while True:
    guess = guesses[i]
    i += 1
    if guess == secret:
        print("猜中了！", guess)
        break               # 立刻跳出整个循环
    print(guess, "不对，再猜")

# 6. continue：跳过本次，进入下一轮
for i in range(10):
    if i % 2 == 1:
        continue            # 奇数跳过下面的 print
    print(i, end=" ")       # 0 2 4 6 8
print()

# 7. 循环的 else：没有被 break 打断（正常结束）才执行
numbers = [3, 7, 11, 15]
target = 12
for n in numbers:
    if n == target:
        print("找到了", target)
        break
else:
    print(target, "不在列表里")   # 循环正常跑完都没找到，走 else

# 8. 嵌套循环 + f-string 对齐：九九乘法表的一部分
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row}x{col}={row * col}", end="  ")
    print()                 # 内层结束换一行
