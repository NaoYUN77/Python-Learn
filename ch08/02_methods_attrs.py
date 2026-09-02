"""02_methods_attrs.py — 实例属性 vs 类属性、__repr__/__str__、属性与方法组合。

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
# 想改全体:Dog.legs = 4(d1 的 3 还是盖着——所以惯例:类属性只读不改单)

# 4. 用途:常量与共享配置
class Http:
    timeout = 30                     # 所有连接默认 30 秒
    max_retries = 3

print(Http.timeout, Http.max_retries)   # 30 3
# Go 对照:类属性 ≈ 包级 const/var;实例属性 ≈ struct 字段。

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
# Go 对照:__str__ ≈ String() string。Go 只有一个,Python 按"观众"分两个。

# ══════════════════════════════════════════
# 第三部分:方法调用方法 + raise 的实战位
# ══════════════════════════════════════════

# 7. 方法里通过 self 调兄弟方法;业务规则用 raise 大声失败(ch07 正当用途)
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")
        self.balance += amount
        return self                    # 返回自己 → 可以链式调用

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(f"余额不足: {self.balance} < {amount}")
        self.balance -= amount
        return self

    def __repr__(self):
        return f"BankAccount({self.owner!r}, {self.balance})"

acc = BankAccount("小明", 100)
acc.deposit(50).withdraw(30)           # 链式:因为 deposit/withdraw 返回 self
print(acc)                             # BankAccount('小明', 120)

try:
    acc.withdraw(999)
except ValueError as e:                # ch07 全套用上:接住、as e、读消息
    print("捕获:", e)                   # 余额不足: 120 < 999

# 8. 链式调用的原理:acc.deposit(50) 的返回值是 acc 自己,
#    所以能接着 .withdraw(30) —— return 通道返回 self,就实现了流水线。
# (setdefault 链式在 ch05 就见过:把"自己"还回去,链条就能继续。)
