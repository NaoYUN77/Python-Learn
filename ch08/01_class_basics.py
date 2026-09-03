"""01_class_basics.py — 最小的类:定义、__init__、实例属性、调用方法。

运行:python ch08/01_class_basics.py
参考官方文档:https://docs.python.org/zh-cn/3/tutorial/classes.html
"""

# ══════════════════════════════════════════
# 第一部分:定义一个类 + 实例化
# ══════════════════════════════════════════

# 1. 类定义 = 一张图纸:这类东西有【名字/年龄】这些数据,
#    会做【叫】这件事
class Dog:
    def __init__(self, name, age):      # 初始化:造对象时自动调用
        self.name = name                # self.name = 实例属性(挂在这个对象身上)
        self.age = age

    def bark(self):                     # 方法 = 类里的函数,第一个参数永远是 self
        return f"{self.name}: 汪汪!"

# 2. 实例化:类名加括号 = 造一个对象,__init__ 自动执行
#    (不用传 self!Python 自动把新对象塞进 self)
d1 = Dog("旺财", 3)
d2 = Dog("小黑", 1)

print(d1.name, d1.age)      # 旺财 3
print(d2.name, d2.age)      # 小黑 1

# 3. 调用方法:对象.方法()
print(d1.bark())            # 旺财: 汪汪!
print(d2.bark())            # 小黑: 汪汪!

# 4. self 的真相:d1.bark() 完全等价于 Dog.bark(d1)
print(Dog.bark(d1))         # 旺财: 汪汪! ← 和 d1.bark() 一模一样
# 你调用时不用传 self;定义时必须写 self。
# self 就是"被 . 点出来的那个对象"。

# ══════════════════════════════════════════
# 第二部分:实例属性互不干扰
# ══════════════════════════════════════════

# 5. 每个对象的属性是独立的一份
d1.age = 4                  # 只改 d1 的
print(d1.age, d2.age)       # 4 1 ← d2 毫发无损

# 6. 属性不用预先声明,随时可加(动态)
d1.nickname = "财财"
print(d1.nickname)          # 财财
# print(d2.nickname)        # ← AttributeError:d2 没这个属性(ch07 的信号!)

# ══════════════════════════════════════════
# 第三部分:方法操作自己的数据
# ══════════════════════════════════════════

# 7. 方法天然能读写实例属性——self 就是数据的入口
class Counter:
    def __init__(self):
        self.count = 0

    def bump(self):
        self.count += 1         # 改自己的数据,不用 return

    def value(self):
        return self.count

c = Counter()
c.bump()
c.bump()
c.bump()
print(c.value())               # 3
# 对比 ch04 闭包的 nonlocal 计数器:类把"状态"明明白白挂在对象上,
# 比闭包里藏变量更直白——这就是"类 = 数据 + 行为的打包"。

# 8. __init__ 可以有默认参数(ch04 的知识直接复用)
class Timer:
    def __init__(self, label, seconds=0):
        self.label = label
        self.seconds = seconds

t = Timer("泡面")              # seconds 用默认值
print(t.label, t.seconds)      # 泡面 0

# ══════════════════════════════════════════
# 第四部分:print 一个对象会发生什么
# ══════════════════════════════════════════

# 9. 没定义 __repr__/__str__ 时,print 出来是"身份信息"
print(d1)                       # <ch08_01_class_basics.Dog object at 0x...>
# 类名 + 内存地址:能看出是什么类,但对人毫无阅读价值
# → 怎么让它打印得像样?见 02(动手加 __repr__/__str__)
