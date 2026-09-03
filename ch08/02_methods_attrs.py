"""02_methods_attrs.py — 实例属性 vs 类属性、__repr__/__str__、方法守门与链式调用。

运行:python ch08/02_methods_attrs.py
参考官方文档:https://docs.python.org/zh-cn/3/tutorial/classes.html#class-objects
"""

# ══════════════════════════════════════════
# 第一部分:类属性 vs 实例属性
# ══════════════════════════════════════════

# 1. 类属性:写在类体里、方法外 —— 所有实例共享
class Dog:
    legs = 4                         # 类属性:狗这个物种的事实
    def __init__(self, name):
        self.name = name             # 实例属性:每只狗自己的

print(Dog.legs)                      # 4 ← 通过类访问
d1 = Dog("旺财")
d2 = Dog("小黑")
print(d1.legs, d2.legs)              # 4 4 ← 都能读到同一份

# 2. 读取时向上找:实例没有的属性,去类里找(这就是 d1.legs 能读到 4 的原因)

# 3. ⚠️ 赋值永远是写在实例身上,不改类属性:
d1.legs = 3                          # 这只是给 d1 加了个实例属性"盖住"它
print(d1.legs, d2.legs, Dog.legs)    # 3 4 4 ← d2 和类毫发无损
# 想改全体:Dog.legs = 4(d1 的 3 还是盖着——所以惯例:类属性当常量,别通过实例赋值)

# 4. 用途:常量与共享配置
class Http:
    timeout = 30                     # 所有连接默认 30 秒
    max_retries = 3

print(Http.timeout, Http.max_retries)   # 30 3

# ══════════════════════════════════════════
# 第二部分:__repr__ 与 __str__
# ══════════════════════════════════════════

# 5. 01 里 print(d1) 打出一串内存地址——现在救回来:
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):               # 给开发者看:精确、能复现
        return f"Point({self.x!r}, {self.y!r})"

    def __str__(self):                # 给用户看:友好
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(p)             # (3, 4)          ← print / str() 用 __str__
print([p, p])        # [Point(3, 4), Point(3, 4)] ← 容器用 __repr__
print(repr(p))       # Point(3, 4)     ← 手动调 __repr__
# 记忆:print 单个对象 → __str__;放进列表/字典、或调试器里 → __repr__

# 6. 只写一个就写 __repr__ —— 没写 __str__ 时它自动顶上:
class Mini:
    def __repr__(self):
        return "Mini()"
print(Mini())        # Mini() ← __repr__ 顶了 __str__ 的班

# ══════════════════════════════════════════
# 第三部分:封装的"守门"——_ 约定 + 方法收敛入口
# ══════════════════════════════════════════

# 7. 把类想成一家公司:类自己的方法 = 员工,类外面的调用代码 = 顾客
#    _ 开头的属性 = 贴了"员工专用"牌子的房间
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner              # 公开:顾客随便读
        self._balance = balance         # 受保护:牌子说"内部用,别碰"

    def balance(self):                  # 柜台:想看余额,走这里
        return self._balance

    def deposit(self, amount):          # 柜台:想改余额,走这里
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")
        self._balance += amount         # 员工进房间,天经地义

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError(f"余额不足: {self._balance} < {amount}")
        self._balance -= amount
        return self                     # 返回自己 → 可以链式调用

acc = BankAccount("小明", 100)
acc.deposit(50).withdraw(30)           # 链式:deposit 返回 self,接着 .withdraw
print(acc.balance())                   # 120 ← 注意是方法,要加括号

# 8. 牌子不是锁:语法上照样能闯
acc._balance = -999                    # ⚠️ 能跑!但全社区看到 _ 都知道你越界了
print(acc.balance())                   # -999
# Python 哲学:"大家都是成年人"——靠约定不靠门禁。
# 封装的价值在守规矩的世界里:入口唯一(deposit/withdraw),规则只写一遍。
