# 第八章 类（OOP 入门）

对应官方文档：[9. 类](https://docs.python.org/zh-cn/3/tutorial/classes.html)

从这章起，你在写"你自己定义的类型"了。前七章的 str/list/dict 都是别人写好的类，
本章你自己写——**类 = 数据 + 操作这些数据的函数，打包成一个东西**。
ch04 的闭包能做的事，类做得更清楚；ch11 的 asyncio 全程面向对象，这章是直接前置。

## 8.0 OOP 四大支柱（先立地图，本章逐个落地）

面向对象的"思想"常被总结成四个词。先给地图，学语法时对号入座：

| 支柱 | 一句话 | 本章哪节落地 |
|------|------|------|
| **封装** Encapsulation | 数据和行为打包；**数据藏起来，通过方法访问** | 8.3 / 8.4 |
| **抽象** Abstraction | **用的人只管"能做什么"，不管"怎么做的"** | 8.5 |
| **继承** Inheritance | 子类自动拥有父类的成员（is-a） | 8.6 |
| **多态** Polymorphism | 同一调用，不同对象不同行为 | 8.7 / 8.8 |

注意顺序：这四个不是并列的技巧，而是一条因果链——
**先封装（藏好数据）→ 才能抽象（暴露简单接口）→ 继承复用这条接口 → 多态让这条接口对不同子类产生不同行为**。
本章的练习（BankAccount、Shape 家族）就是按这条链设计的。

**Go 对照先行**：你在 Go 里写过 `balance` 小写字段 + `Deposit()` 方法吗？
那就是封装；你调用 `w.Write(p)` 从不关心缓冲区怎么刷，那就是抽象；
Go 砍掉继承、用 interface 连接多态——Python 四样全给，但工程判断相同：
**封装和抽象天天用，继承省着用**。

## 8.1 最小的类：数据 + 行为的打包

```python
class Dog:
    def __init__(self, name, age):     # 构造:造对象时自动调用
        self.name = name               # 实例属性:挂在"这一个对象"身上
        self.age = age

    def bark(self):                    # 方法:类里的函数
        return f"{self.name}: 汪汪!"

d = Dog("旺财", 3)      # 造对象(实例化),__init__ 自动执行
print(d.bark())          # 旺财: 汪汪!
```

Go 对照——你熟悉的 struct + method：

```go
type Dog struct {
    name string
    age  int
}

func NewDog(name string, age int) *Dog {   // Go 要手写构造函数
    return &Dog{name: name, age: age}
}

func (d *Dog) Bark() string {              // receiver ≈ self
    return fmt.Sprintf("%s: 汪汪!", d.name)
}
```

| Go | Python |
|------|------|
| `type X struct {...}` | `class X:` |
| `func (d *Dog) Bark()` 的 receiver `d` | `def bark(self)` 的第一个参数 `self` |
| 手写 `NewXxx()` 构造函数 | `__init__` 自动调用 |
| `d.name`（同包可访问） | `d.name`（默认全开放） |
| 方法集大写才有导出 | 没有导出概念，`_name` 约定俗成表示"内部用" |

**self 的真相**：`d.bark()` 完全等价于 `Dog.bark(d)`——self 就是"被点出来的那个对象"，
你调用时**不用传** self，定义时**必须写** self。

**属性的"继承"和方法的继承是两回事**（精确理解，别混）：

- **方法**：类体里写的所有方法，子类**自动全部拥有**（向上查找，就近覆盖）
- **属性**：不是声明出来的，是 `__init__` **执行到 `self.xxx = ...` 那一行才诞生的**——
  Python 类体里没有字段声明（这是和 Go struct 最深的差异）。
  子类没写 `__init__` 就用爹的（等于继承了"装属性的工序"）；
  自己写了就必须 `super().__init__()`，否则爹的工序被跳过，属性根本没被装上
  （→AttributeError）

## 8.2 `__init__` 与实例属性

- `__init__` 不是"创建对象"，是"创建之后立刻初始化"（创建那步是 `__new__` 干的，暂时不碰）
- `self.xxx = ...` 才是真正的属性赋值；**写了才有，没写就没有**——
  它是一段普通代码，跑一行装一个，不是"图纸声明字段"
- 每个实例的属性互不干扰——`d1.name` 和 `d2.name` 是两份独立的内存

```python
d1 = Dog("旺财", 3)
d2 = Dog("小黑", 1)
d1.age = 4              # 只改 d1 的
print(d2.age)           # 1 ← d2 不受影响
```

**类属性**（在类体里、方法外直接赋值）是所有实例共享的——适合放常量：

```python
class Dog:
    legs = 4                    # 类属性:所有狗共享
    def __init__(self, name):
        self.name = name        # 实例属性:每只狗一份

print(Dog.legs, Dog("a").legs)  # 4 4
```

⚠️ 细节：`d1.legs = 3` **不会改类属性**——它只是给 d1 新增了一个同名实例属性
"盖住"类属性（实例查找先于类查找）。想改全体用 `Dog.legs = ...`。
所以惯例：**类属性当常量用，别通过实例赋值**。

Go 对照：实例属性 ≈ struct 字段；类属性 ≈ 包级 var 常量。

## 8.3 封装（一）：打包——数据和规则住在一起

封装有**两层含义**。第一层你已经会了：**打包**。

看散装写法的问题（ch01-07 的风格）：

```python
def deposit(balance, amount):
    if amount <= 0:
        raise ValueError(...)       # 规则在这里写一遍
    return balance + amount

def withdraw(balance, amount):
    if amount <= 0:                 # 同样的校验再抄一遍
        raise ValueError(...)
    if amount > balance:            # 每个碰钱的函数都要记得抄
        raise ValueError(...)
    return balance - amount

# 调用方直接拿 balance 变量乱改:balance = -99999,没人拦得住
```

**数据和规则分离，每个函数各自校验，漏一处就是洞；调用方还绕过所有函数直接改数据。**

类的答案：把数据和行为装进同一个盒子，**关于余额的一切规则只写一遍**：

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")
        self.balance += amount      # 规则有了唯一的家

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(f"余额不足: {self.balance} < {amount}")
        self.balance -= amount
```

谁想动余额都必须过这些方法——**方法的代码就是"合法修改方式说明书"**。
这就是 8.0 因果链的第一环：先打包，才谈得上后面的"藏"。

Go 对照：receiver 方法是同样的打包。你已经写过 `func (a *Account) Deposit(...)`，
只是 Go 不叫它封装。

## 8.4 封装（二）：藏起来——`_` 约定与方法守门

第二层才是重点：**不该让外面随便碰的数据，藏起来**。

问题：上面的类，外面照样能绕过方法直接改：

```python
acc = BankAccount("小明", 100)
acc.balance = -99999        # ❌ 语法完全合法!绕过所有规则
```

Python **默认不设防**——所有属性公开。这和 Go 相反：

| | Go | Python |
|------|------|------|
| 藏字段 | 首字母小写 `balance`，**编译器强制**包外不可访问 | **没有强制机制**，全靠约定 |
| 暴露方法 | 大写 `Deposit()` 公开 | 方法本来就公开 |

Python 的约定两档：

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner              # 公开:随便读,无所谓
        self._balance = balance         # 受保护:一个下划线 = "内部用,别碰"

    def balance(self):                  # 想读余额?走方法(守门)
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"存款必须为正数: {amount}")
        self._balance += amount         # 只有类自己的方法能改 _balance
```

- **单下划线 `_balance`**：纯约定。语法上照样 `acc._balance = -1`——但全社区
  看到下划线都懂："这是内部实现，碰了出事自己负责"。相当于 Go 的小写字段，
  **只是没有编译器替你拦**。
- **双下划线 `__balance`**：Python 悄悄改名为 `_BankAccount__balance`
  （name mangling），外部误碰变难——但主要目的是避免子类意外覆盖属性名，
  **不是真私有**。入门统一用单下划线。

**为什么没有强制也合理？** Python 哲学："We're all consenting adults"
（大家都是成年人）——约定 + 自律替代编译器强制。代价是约束力弱，
好处是没有"为了一点内部访问写一堆 accessor"的繁琐。**用下划线表达意图，
review 时它就是红线。**

**封装完整定义（两层合起来）：打包 = 数据和行为住在一起、规则只写一遍；
隐藏 = 数据标 `_`、修改入口收敛成方法。**

## 8.5 抽象：用的人只管"能做什么"

抽象回答另一个问题：**调用者需要知道多少？** 答案：越少越好。

```python
acc = BankAccount("小明", 100)
acc.deposit(50)         # 你需要知道的全部:有 deposit 方法、传正数 —— 就这些
```

你**不需要知道**：余额存在哪个属性、校验用 raise 还是返回 None、
有没有记日志、要不要加锁。这些"怎么做的"被类**藏**在方法背后——
**类对外的全部承诺 = 方法名 + 参数 + 行为；内部实现是自由细节，随时可换**：

```python
# 某天改成:余额存分不存元、加操作日志、加冻结状态……
# 只要 deposit/withdraw 的签名和行为不变,所有调用代码一行不用改
```

**判断抽象做没做好的一道光：换实现要不要改调用方？** 要改 = 抽象漏了
（"怎么做"泄露到外面去了）。

Go 里你天天享受这个：`w.Write(p)`——不管 w 是文件、网络还是 buffer，
你只知道"能写"，不关心实现。**interface 的方法集就是承诺清单**；
Python 的方法就是对外承诺，**下划线的东西不在承诺范围内**。

> 顺带：为什么你从 ch06 起 `f.read()` 用得这么安心？因为文件对象把光标、
> 缓冲、操作系统文件句柄全部封装在内部，对外只暴露 read/write/close——
> **你早就享受封装+抽象的红利了，本章只是学会自己造这种东西。**

抽象和封装的关系（一对容易混的概念）：

- **封装**是"把数据和实现**藏进来**"（对内的纪律）
- **抽象**是"把承诺**露出去**"（对外的界面）
- 一藏一露，配合工作：藏得越干净，承诺越稳定，调用方越省心

## 8.6 继承：站在父类肩膀上

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):                       # 括号 = 继承谁
    def speak(self):                     # 重写(override)父类方法
        return f"{self.name}: 汪汪!"

class Cat(Animal):
    def __init__(self, name, indoor):
        super().__init__(name)           # 借用父类的初始化
        self.indoor = indoor             # 再补自己的
    def speak(self):
        return f"{self.name}: 喵~"

for a in [Dog("旺财"), Cat("咪咪", True)]:
    print(a.speak())                     # 同一句代码,不同行为
```

- `class Dog(Animal)` —— 括号里写父类；子类自动拥有父类的所有方法
  （查找规则：先找 Dog 自己 → 没有就上溯 Animal → 就近覆盖，没有再向上）
- **重写**：子类定义同名方法，覆盖父类版本
- `super().__init__(...)` —— 调用父类版本，别复制粘贴父类的初始化代码
- 最后那个循环 = **多态**（8.7 展开）

**Go 重大差异**：Go **没有继承**！Go 用嵌入（embedding）组合出类似效果，
用 interface 表达"行为约定"。Python 是真继承。

**什么时候该继承？is-a 测试**：

```
"X 是一种 Y" 说得通 → 继承合理(狗是一种动物 ✅、正方形是一种形状 ✅)
"X 是 Y 的一部分 / X 有 Y" → 用组合(汽车有发动机 ❌继承、汽车 has-a 发动机 ✅组合)
```

**组合优于继承**（OOP 名言，Go 用整个语言设计表示赞同）：继承是"我是我爹的延伸"，
耦合深（爹改了，子类跟着晃）；组合是"我雇佣了一个部件"，耦合浅（部件随便换）：

```python
class Car:
    def __init__(self):
        self.engine = Engine()      # 组合:Car has-a Engine
    def start(self):
        self.engine.ignite()        # 借部件的能力
```

入门判断法：**先想组合（把对象当属性装进来），继承只在真 is-a 时用**。

## 8.7 多态：同一接口，不同行为

多态 = 8.6 最后那个循环里发生的事，值得单独点破：

```python
for a in [Dog("旺财"), Cat("咪咪", True)]:
    print(a.speak())        # 汪汪! / 喵~ ← 同一行代码,两种行为
```

**为什么这是大事？** 调用方（这个循环）**不知道也不用知道**列表里装的是什么——
它只知道"每个东西都会 speak()"。新增一个 `Wolf` 类？循环一行不改。
**调用方依赖的是"能力"（有 speak），不是"血统"（是什么类）**——
这就是抽象思想在继承体系上的兑现。

没有多态的写法（感受一下痛苦）：

```python
for thing in zoo:
    if isinstance(thing, Dog):     print(thing.bark())
    elif isinstance(thing, Cat):   print(thing.meow())
    elif isinstance(thing, Robot): print(thing.beep())   # 新类型?回来加 elif!
```

每加一个类型，所有遍历点都要改——**代码围着类型长，而不是围着能力长**。
多态把这坨 isinstance 链拆掉了。实战信号：**发现自己写长串
`isinstance / elif isinstance`，通常就是该上多态的地方**。

## 8.8 鸭子类型：Python 版的 interface，不用声明

> 走起来像鸭子、叫起来像鸭子，那它就是鸭子。

```python
class Dog:
    def speak(self): return "汪汪"

class Robot:
    def speak(self): return "哔哔"      # 和 Dog 毫无血缘关系!

def make_noise(thing):
    return thing.speak()                # 只要求:有 speak 方法就行

make_noise(Dog())      # 汪汪
make_noise(Robot())    # 哔哔 ← 没继承任何东西,照样能用
```

**多态的极致：连继承都不需要**——不看血统，只看当下有没有那个方法。

Go 的 interface 是**静态 duck typing**：编译期检查"方法集齐没有"。
Python 是**动态 duck typing**：运行时真调了才知道，**没有 implements 声明**。

**代价**（03 示例演示过）：对象没有那个方法，Python 不拦，炸在运行时
（AttributeError）——炸点后移，靠测试兜底。**这就是为什么本章测试更重要**：
它们部分扮演了 Go 编译器的角色。

## 8.9 dataclass：struct 的直系亲戚（顺手认识）

写"纯数据类"时有个语法糖，一行顶你手写 `__init__`/`__repr__`：

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)     # __init__ 自动生成
print(p)                # Point(x=3.0, y=4.0) ← __repr__ 也自动生成
```

类型注解 `x: float` 在 Go 里你天天写（struct 字段类型），这里的注解主要是给
编辑器/basedpyright 看。练习先手写 `__init__` 打底，dataclass 当彩蛋认识。

## 8.10 本章小结（对着 8.0 的地图验收）

- **类 = 数据（实例属性）+ 行为（方法）的打包；`__init__` 初始化，self = 被点名的对象**
- `d.bark()` ≡ `Dog.bark(d)`——self 不用传，但必须写
- 实例属性每对象一份（跑一行装一个，写了才有）；类属性全体共享（放常量）；
  `d1.legs = 3` 只是盖住，不改类
- **封装**：打包（规则只写一遍）+ 隐藏（`_` 约定 + 方法守门）——Python 靠约定不靠编译器
- **抽象**：对外只承诺"能做什么"；检验标准 = 换实现不改调用方
- `__repr__` 给开发者（优先写它），`__str__` 给用户（≈ Go 的 String()）
- **继承**：is-a 才继承，通常先想组合；重写就近覆盖；`super().__init__()` 借父类工序
- **多态**：调用方依赖能力不依赖血统；长 isinstance 链 = 该上多态的信号
- **鸭子类型**：多态的极致，连继承都不用；代价是炸点移到运行时，用测试补位
- dataclass：纯数据类的语法糖

---

## ✍️ 动手运行

```bash
python ch08/01_class_basics.py
python ch08/02_methods_attrs.py
python ch08/03_inherit_duck.py
```

## 🧪 实践练习

打开 `exercises.py` 完成函数/类，然后在**项目根目录**运行：

```bash
python -m ch08.test_exercises
```

## 🔗 官方文档深入阅读

- 类：<https://docs.python.org/zh-cn/3/tutorial/classes.html>
- dataclasses：<https://docs.python.org/zh-cn/3/library/dataclasses.html>
