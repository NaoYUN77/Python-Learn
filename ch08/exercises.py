"""exercises.py — 第八章实践练习(类与 OOP 入门)。

请完成下面的每个类/函数,然后运行 python -m ch08.test_exercises 检查。

题目围绕官方教程第 9 章(类),按四大支柱设计:
打包与 __init__(8.1-8.2)→ 封装:守门方法(8.3-8.4)→ __repr__/抽象界面(8.5)
→ 继承与重写(8.6)→ 多态(8.7)→ super()(8.6)→ 鸭子类型(8.8)→ 封装实战(8.4)

⚠️ 注意:方法定义时第一个参数必须写 self;调用方法时不用传 self。
⚠️ except 永远写具体类型(错题本有案底)。
"""

# 练习 1:最小类(热身)
# 定义 Dog 类:__init__(self, name, age) 存两个实例属性;
# 方法 bark(self) 返回 f"{self.name}: 汪汪!"
# 提示:方法都定义在 class 缩进里,第一个参数是 self
class Dog:
    # TODO: __init__ 存 name/age;bark 返回 f"{self.name}: 汪汪!"
    def __init__(self , name , age):
        self.name = name 
        self.age = age 
    def bark(self):
        return f"{self.name}: 汪汪!"

# 练习 2:带默认参数的 __init__ + 方法操作数据
# 定义 Counter 类:__init__(self, start=0) 存 self.count;
# bump(self) 让 count 加 1(不用 return);value(self) 返回 count
# 提示:默认参数写法 __init__(self, start=0) —— ch04 的知识
class Counter:
    # TODO: __init__ 存 count;bump 加 1;value 返回
    def __init__(self,start=0):
        self.count = start 
    def bump(self):
        self.count += 1
    def value(self):
        return self.count


# 练习 3:方法操作数据 + raise(ch07 的正当用途)
# 定义 BankAccount 类:__init__(self, owner, balance=0);
# deposit(self, amount):amount <= 0 时 raise ValueError(f"存款必须为正数: {amount}"),
#   否则余额加 amount;
# withdraw(self, amount):amount > 余额时 raise ValueError(f"余额不足: {balance} < {amount}"),
#   否则余额减 amount
# 提示:f-string 里的数值直接用 {amount} {self.balance} 插入,消息逐字符照抄
class BankAccount:
    # TODO: 两个方法各带一个 if 越界 raise,否则增减余额
    pass


# 练习 4:__repr__
# 给下面的 Point 类加 __repr__ 方法,返回 f"Point({self.x!r}, {self.y!r})"
# 提示:!r 会给字符串值带上引号 ——"给开发者看"的格式
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # TODO: __repr__ 返回 f"Point({self.x!r}, {self.y!r})"
    pass


# 练习 5:实例属性 vs 类属性
# 定义 Car 类:类属性 wheels = 4(所有车共享);
# __init__(self, brand) 存 brand;方法 describe(self) 返回
# f"{self.brand} 有 {self.wheels} 个轮子"(读类属性直接写 self.wheels)
# 提示:类属性写在类体里、方法外;describe 里用 self.wheels 就能读到
class Car:
    # TODO: wheels = 4 写在方法外;__init__ 存 brand;describe 拼字符串
    pass


# 练习 6:继承与重写
# 父类 Shape 已给:有 describe 方法(注意它内部调 self.area()——多态的钩子)
# 定义 Square(Shape):__init__(self, side) 存 side;
#   area(self) 返回 side * side
# 定义 Circle(Shape):__init__(self, r) 存 r;
#   area(self) 返回 3.14159 * r * r
# 提示:括号里写 Shape 表示继承;两个子类都只需重写 area
class Shape:
    def describe(self):
        return f"面积是 {self.area():.2f}"


class Square(Shape):
    # TODO: __init__ 存 side;area 返回 side * side
    pass


class Circle(Shape):
    # TODO: __init__ 存 r;area 返回 3.14159 * r * r
    pass


# 练习 7:super() 扩展 __init__
# 父类 Animal 已给。
# 定义 Cat(Animal):__init__(self, name, indoor) —— 先 super().__init__(name),
#   再存 self.indoor;speak(self) 返回 "喵~"
# 提示:super().__init__(name) 把 name 交给父类处理,别自己重复赋值
class Animal:
    def __init__(self, name):
        self.name = name


class Cat(Animal):
    # TODO: __init__ 先 super().__init__(name) 再存 indoor;speak 返回 "喵~"
    pass


# 练习 8:鸭子类型(挑战)
# 写函数 loudest(items):items 是一串对象,要求每个都有 speak() 方法;
# 返回"叫声最长"的那个对象的 speak() 结果(按 len 比较);
# items 为空列表 → 返回 "";某项没有 speak 方法 → 让 AttributeError 自然炸出(不要接)
# 提示:循环里 result = item.speak(),用 len(result) 和当前最长比较;
#       AttributeError 故意不接——鸭子测试失败就该大声炸(ch07:bug 不接)
def loudest(items):
    # TODO: 空列表返回 "";循环取 item.speak(),len 最长者胜出
    pass


# 练习 9:封装实战(README 8.4 的落地)
# 把 BankAccount 改造成"守门"版:
# __init__(self, owner, balance=0):owner 存公开属性;
#   余额存成受保护属性 self._balance(下划线开头 = "内部用,别碰")
# balance(self) 方法:返回 self._balance(对外只读的窗口)
# deposit(self, amount):amount <= 0 时 raise ValueError(f"存款必须为正数: {amount}"),
#   否则给 self._balance 加 amount
# withdraw(self, amount):amount > self._balance 时
#   raise ValueError(f"余额不足: {self._balance} < {amount}"),否则减
# 想一想(不用写):为什么外面现在改不了余额了?——不是语法拦住了,
#   而是 _balance 这个名字在说"你碰了就是你的责任"——封装是约定,不是牢门
# 提示:和练习 3 只差两处——属性名全部改 _balance、新增 balance() 读窗口
class SafeAccount:
    # TODO: _balance 受保护属性 + balance() 只读窗口 + 守门的 deposit/withdraw
    pass
