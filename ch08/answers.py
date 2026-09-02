"""answers.py — 第八章练习参考答案。

先自己尝试做 exercises.py,实在做不出来再看这里。
"""

# 练习 1
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name}: 汪汪!"


# 练习 2
class Counter:
    def __init__(self, start=0):        # 默认参数:ch04 的知识直接复用
        self.count = start

    def bump(self):
        self.count += 1                 # 改自己的数据,副作用通道,不用 return

    def value(self):
        return self.count


# 练习 3
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")    # 大声失败
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(f"余额不足: {self.balance} < {amount}")
        self.balance -= amount


# 练习 4
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):                 # 给开发者看,!r 给字符串值带引号
        return f"Point({self.x!r}, {self.y!r})"


# 练习 5
class Car:
    wheels = 4                          # 类属性:写在类体里、方法外,全体共享

    def __init__(self, brand):
        self.brand = brand

    def describe(self):
        return f"{self.brand} 有 {self.wheels} 个轮子"   # self.wheels 向上找到类属性


# 练习 6
class Shape:
    def describe(self):
        return f"面积是 {self.area():.2f}"   # 多态钩子:调的是子类的 area


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r * self.r


# 练习 7
class Animal:
    def __init__(self, name):
        self.name = name


class Cat(Animal):
    def __init__(self, name, indoor):
        super().__init__(name)          # 父类的活让父类干
        self.indoor = indoor

    def speak(self):
        return "喵~"


# 练习 8
def loudest(items):
    if not items:                       # 真假值:空列表为假(ch02)
        return ""
    best = ""                           # 当前最长的叫声
    for item in items:
        result = item.speak()           # 没有 speak 就 AttributeError 自然炸(故意的)
        if len(result) > len(best):     # 严格大于:并列时保留先来的
            best = result
    return best


# 练习 9:封装实战 —— 对比练习 3,体会"守门"版多了什么
class SafeAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner              # 公开:读它无所谓
        self._balance = balance         # 受保护:_ 开头 = "内部用,别碰"(约定)

    def balance(self):                  # 对外的只读窗口:想看余额,走这里
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")
        self._balance += amount         # 全类只有这里的规则能改 _balance

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError(f"余额不足: {self._balance} < {amount}")
        self._balance -= amount
    # 思考题答案:acc._balance = -999 语法上仍然合法!
    # 封装没有牢门,只有"下划线"这块警示牌 + 全社区公认的读法。
    # 它的价值是:守门入口唯一化(deposit/withdraw),守规矩的人不会绕。


if __name__ == "__main__":
    d = Dog("旺财", 3)
    print(d.bark())                     # 旺财: 汪汪!

    c = Counter()
    c.bump(); c.bump(); c.bump()
    print(c.value())                    # 3

    acc = BankAccount("小明", 100)
    acc.deposit(50)
    print(acc.balance)                  # 150
    try:
        acc.withdraw(999)
    except ValueError as e:
        print("捕获:", e)                # 余额不足: 150 < 999

    print(repr(Point(3, 4)))            # Point(3, 4)

    car = Car("比亚迪")
    print(car.describe())               # 比亚迪 有 4 个轮子

    print(Square(3).describe())         # 面积是 9.00
    print(Circle(2).describe())         # 面积是 12.57

    cat = Cat("咪咪", True)
    print(cat.name, cat.indoor, cat.speak())   # 咪咪 True 喵~

    class Robot:
        def speak(self):
            return "哔哔哔"
    print(loudest([Dog("旺财"), Robot()]))     # 哔哔哔

    safe = SafeAccount("小红", 200)
    safe.deposit(100)
    print(safe.balance())               # 300 ← 注意是方法,要加括号
