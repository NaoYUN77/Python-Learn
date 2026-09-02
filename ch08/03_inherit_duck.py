"""03_inherit_duck.py — 继承、super()、多态、鸭子类型、dataclass 彩蛋。

运行:python ch08/03_inherit_duck.py
参考官方文档:https://docs.python.org/zh-cn/3/tutorial/classes.html#inheritance
"""

# ══════════════════════════════════════════
# 第一部分:继承与重写
# ══════════════════════════════════════════

# 1. 父类:通用的"动物"
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def intro(self):
        return f"我是 {self.name},我会叫: {self.speak()}"
        # 注意:intro 里调用了 self.speak() —— 到底叫出什么,看子类

# 2. 子类:括号里写父类 = 继承(自动拥有父类的全部方法)
class Dog(Animal):
    def speak(self):                     # 重写(override):同名覆盖
        return "汪汪!"

class Cat(Animal):
    def speak(self):
        return "喵~"

d = Dog("旺财")
c = Cat("咪咪")
print(d.speak())                # 汪汪! ← 用的是子类版本
print(c.speak())                # 喵~
print(d.intro())                # 我是 旺财,我会叫: 汪汪!
# intro 是从父类继承来的,但它内部调的 speak 走的是子类的版本——
# 这就是多态:同一句 self.speak(),不同对象叫出不同的声。

# 3. isinstance:判断"是不是这个类(或它的子类)" —— 继承树知识直接复用
print(isinstance(d, Dog))       # True
print(isinstance(d, Animal))    # True ← 子类也是父类(ch07:接父类连子类的同款血缘)

# ══════════════════════════════════════════
# 第二部分:super() —— 借用父类的实现
# ══════════════════════════════════════════

# 4. 子类扩展 __init__:先借父类初始化,再补自己的
class Cat(Animal):
    def __init__(self, name, indoor):
        super().__init__(name)          # 父类的活让父类干,别复制粘贴
        self.indoor = indoor            # 再加自己的新属性

    def speak(self):
        return "喵~"

c2 = Cat("咪咪", True)
print(c2.name, c2.indoor)       # 咪咪 True
print(c2.intro())               # 我是 咪咪,我会叫: 喵~ ← 父类方法照样能用
# 不写 super().__init__ 会怎样?name 就没人赋值了,后面用到就 AttributeError。
# Go 对照:Go 没有继承,嵌入结构体要手动传递字段;super() 是 Python 替你干了这层。

# 5. 重写时调用 super() 的另一半用法:扩展而不是替换
class Guard(Dog):
    def speak(self):
        return super().speak() + " (汪汪汪!)"   # 先要父类的结果,再加工

g = Guard("大黄")
print(g.speak())                # 汪汪! (汪汪汪!)
# 与 ch04 的"包装"思路同款:包一层,先借内层结果再加料。

# ══════════════════════════════════════════
# 第三部分:鸭子类型 —— 没有 implements 声明的 interface
# ══════════════════════════════════════════

# 6. 和 Animal 毫无血缘关系的类,只要有 speak 方法就能混进队伍
class Robot:
    def speak(self):                    # 没继承 Animal!
        return "哔哔"

def concert(performers):
    for p in performers:
        print(f"🎤 {p.speak()}")        # 只要求:有 speak 方法

concert([Dog("旺财"), Cat("咪咪", False), Robot()])
# 汪汪! / 喵~ / 哔哔 ← Robot 不是 Animal,照样登台
# Go:interface 是编译期静态检查"方法集齐没";Python:运行时真调了才知道。
# 走起来像鸭子、叫起来像鸭子,那它就是鸭子 —— 方法对上就能用,不看血统。

# 7. duck typing 的代价:没实现方法,炸在运行时(ch07 的 AttributeError)
class Rock:
    pass                                # 什么方法都没有

try:
    concert([Rock()])
except AttributeError as e:
    print("鸭子测试失败:", e)            # 'Rock' object has no attribute 'speak'
# Go 里编译器当场拦下;Python 要跑到那一行才炸 → 炸点后移,靠测试兜底。

# ══════════════════════════════════════════
# 第四部分:dataclass 彩蛋 —— 纯数据类的语法糖
# ══════════════════════════════════════════

# 8. 只装数据的类,@dataclass 一行生成 __init__ + __repr__ 等
from dataclasses import dataclass

@dataclass
class Point:
    x: float                            # 类型注解:Go struct 字段的老朋友
    y: float

p1 = Point(3.0, 4.0)                    # __init__ 自动生成
print(p1)                               # Point(x=3.0, y=4.0) ← __repr__ 也是
# 类型注解在 Go 里你天天写,这里主要是给 basedpyright 看,Python 运行时不强制。
# 练习里先手写 __init__ 打底,dataclass 当甜点认识即可。
