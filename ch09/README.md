# ch09 模块与包

> 官方教程:[6. 模块](https://docs.python.org/zh-cn/3/tutorial/modules.html)
> 运行示例(项目根目录):`python ch09/01_import_basics.py`

## 9.0 为什么要学这个

Agent 开发的日常,就是把别人写好的模块拼起来:调 API 用现成的库,
你自己的工具函数放 `tools.py`……**import 就是拼装的接口**。

你其实早就在用它了——`test_exercises.py` 第一行
`from . import exercises`,从 ch01 用到现在,只是今天才打开黑盒。

本章还顺便终结一桩悬案:**幽灵 import 六连**
(sqlite3 / winreg / calendar / asyncio / 双幽灵 / boost 套娃)。
学完这章你就知道 import 到底做了什么,为什么没用的 import 必须**整行删**。

先把本章术语亮出来(后面反复出现,忘了随时翻回来查):

| 术语 | 一句话 |
|------|--------|
| 模块 | 一个 .py 文件 |
| 包 | 装模块的文件夹 |
| import | 把模块"搬进来"的动作 |
| 模块对象 | import 拿到的那个东西——模块的全部内容挂在它身上 |
| 命名空间 | 一本"名字 → 对象"的登记册 |
| `sys.modules` | 解释器的**总记账本**:已经 import 过的模块全在里面 |
| `sys.path` | **搜索路径清单**:import 时按从上到下的顺序找文件 |

## 9.1 极慢镜头:import tiny_mod 到底发生了什么

`import tiny_mod` 一共做三件事:**找到 → 执行 → 记账**。
一帧一帧看。

### 第 1 帧:找到

Python 拿着名字 `"tiny_mod"`,按 `sys.path` 从上到下挨个目录问:
"这里面有 tiny_mod.py 吗?"——在脚本所在目录 `ch09/` 命中。
**从上到下,第一个命中就用,不再往下看**(顺位表见 9.4)。

### 第 2 帧:执行(整个文件的顶层代码,从头到尾)

注意"顶层"的意思:**所有不缩进的行**——`def` 的**定义行也是顶层代码**
(执行它 = 造出函数对象,函数体本身此时不执行)。

| 时刻 | 执行到 | tiny_mod 命名空间里有什么 | 你看到的输出 |
|------|--------|---------------------------|--------------|
| t1 | `print("tiny_mod 顶层…")` | (还什么都没有) | tiny_mod 顶层代码执行了!… |
| t2 | `PI = 3.14159` | PI | |
| t3 | `def double(x): …` | PI, double | |
| t4 | `def triple(x): …` | PI, double, triple | |
| t5 | `if __name__ == "__main__":` | PI, double, triple | (条件 False,**整块跳过**) |

看 t1:**顶层 print 在任何函数定义之前就执行了**——这就是为什么
import 一个没加守卫的模块会当场刷屏(Boost 事故的根源,9.3 复盘)。

### 第 3 帧:记账 + 交付

1. 把结果存进总账:`sys.modules["tiny_mod"] = 模块对象`
2. 在**你的文件**里创建一个名字 `tiny_mod`,指向这个模块对象

之后你写 `tiny_mod.PI`、`tiny_mod.double(21)`,
都是**从模块对象身上取属性**——模块对象就是"装着整个模块命名空间的盒子"。

### 第二次 import:只查账,不再执行

```python
import tiny_mod   # 第一次:找到 → 执行 → 记账
import tiny_mod   # 第二次:查 sys.modules → 有账!直接绑名字,一行代码不跑
```

所以 01 的顶层 print 只出现一次。
**"只执行一次"不是什么优化技巧,是记账机制本身**。

想亲眼看记账?`04_module_object.py` 把 sys.modules 翻开给你看,
甚至撕掉一页账再 import,逼 Python 重新执行整个文件。

## 9.2 import 三姿势(盯住原料 → 产物)

| 姿势 | 写法 | 产物(你的文件里多了什么) | 用法 | 场景 |
|------|------|--------------------------|------|------|
| 整体搬 | `import math` | 名字 `math`(模块对象) | `math.sqrt(25)` | 要用多个名字 |
| 点名搬一件 | `from tiny_mod import triple` | 名字 `triple`(直接是函数) | `triple(7)` | 只要一个名字 |
| 整体搬+改名 | `import datetime as dt` | 名字 `dt`(模块对象) | `dt.date(2026, 1, 1)` | 名字长/防遮蔽 |

两种产物,方向别反:
- `import x` → 产物是**模块对象** → 用的时候带前缀 `x.名字`
- `from x import y` → 产物是**名字 y 本身** → 不带前缀直接用

### 每种姿势的注意点

**import x**:名字永远带前缀,不会和你文件里的名字撞车,最安全。

**from x import y**:
- 拼错名字当场炸:`from tiny_mod import tripl` →
  `ImportError: cannot import name 'tripl'`——报错本身在说
  "那个模块的命名空间里没有这个名字",按报错改拼写就行
- 拿到的是 import 那一刻的 y(名字绑定),不是"实时追踪"——知道即可

**import x as z**:纯改名,常用于名字太长或约定缩写(dt、np)。

> ⚠️ `from xxx import *` 别用:把模块里所有公开名字一次性灌进来,
> 来源不明、极易撞车——正是幽灵 import 的温床。

## 9.3 __name__ 的两副面孔

每个模块都有一个 `__name__`,值取决于**它怎么被打开**:

| 打开方式 | `__name__` 的值 | `if __name__ == "__main__":` 守卫里的代码 |
|----------|-----------------|--------------------------------------------|
| `python ch09/tiny_mod.py`(直接跑) | `"__main__"` | **执行** |
| `import tiny_mod`(被导入) | `"tiny_mod"` | **跳过** |

极慢镜头:`python ch09/tiny_mod.py` 时,Python 把这个文件当作
一个名叫 `"__main__"` 的临时模块来执行——所以它看到的自己是 "__main__"。
被 import 时走的是 9.1 的正常流程,`__name__` 被赋成模块名 "tiny_mod"。

守卫的口吻:**"我是主角时才执行下面这块"**。
演示代码放进守卫,别人 import 你时就不会被刷屏。

**复盘 boost 事故(ch08 幽灵第六次)**:
`from boost.ch05_tuples import result` 这行,
① `result` 全程没用——幽灵;
② import 会执行 boost 那个文件的**顶层代码**,它的演示没加守卫,
于是测试一跑,满屏不相关的输出。
两个教训:①没用就**整行删** ②自己的演示一定加 `__name__` 守卫。

## 9.4 sys.path:import 的搜索清单

import 的第 1 帧按 `sys.path` 从上到下找。`python ch09/01_xxx.py` 时:

| 顺位 | 里面是什么 | 说明 |
|------|------------|------|
| 1 | 脚本所在目录(ch09/) | **你的文件都在这**——同名就遮蔽 |
| 2 | python312.zip | 标准库(压缩打包) |
| 3 | DLLs | Windows 的二进制扩展 |
| 后面 | site-packages | 第三方库(pip 装的) |

遮蔽陷阱:你随手建一个 `json.py`,它排在标准库 json 前面——
以后 `import json` 拿到的是你的文件,而且**你多半毫无察觉**。
自检:`sys.stdlib_module_names`(3.10+)装着全部标准库名,
`03_packages.py` 里有现成的遮蔽检查器。

## 9.5 包 = 装模块的文件夹

文件夹(`ch09/`、`boost/quiz/`)就是包,里面每个 .py 是模块。
解密那行老朋友,逐词拆:

```python
from . import exercises
```

| 词 | 意思 |
|----|------|
| `from` | 从哪里拿 |
| `.` | **当前包**(这个点代表 ch09) |
| `import` | 拿 |
| `exercises` | 要的那个模块 |

这叫**显式相对导入**——规则要求必须带点:
光写 `import exercises`(隐式相对导入)在 Python 3 直接报错。

配套小知识:
- 模块名 = 文件名去掉 `.py`:`exercises.py` 的模块名是 `"exercises"`
- 点可以叠加:`from .. import x` = 从**上一级**包拿(在 boost/quiz/ 里,`..` 是 boost)
- `__init__.py`:传统上包的标志文件(很多项目至今仍写);3.3+ 没有也能跑
  (namespace package 的宽容)——本项目全程没写,**知道即可**

## 9.6 标准库 = 自带电池

不用安装、import 就能用。本章用到的:

| 模块 | 干什么 | 和旧知识的连接 |
|------|--------|----------------|
| `math` | sqrt / pi …… | ch01 的运算符不够用了 |
| `string` | ascii_uppercase 等常量 | 字符串的"材料包" |
| `datetime` | 日期计算 | 日期相减得 timedelta |
| `collections` | Counter 等 | **ch05 计数模式的一行版!** |
| `sys` | sys.path / sys.modules / stdlib_module_names | 解释器自己的仪表盘 |

ch10 就是标准库漫游,这里先尝三口。

## 9.7 import 区卫生三查(幽灵终结仪式)

交卷前固定动作,扫文件顶部:

1. **用到了吗?** 没用的【整行删】——不是删名字,是删整行!
2. **是弹窗塞的吗?** 编辑器自动补全顺手回车 = 幽灵入营
3. **它有顶层输出吗?** 没加守卫的模块,import 一次刷一次屏

## 9.8 小结与自测

一句话:**模块 = .py 文件;import = 找到 → 执行顶层(只一次)→ sys.modules 记账;
模块对象身上挂着它的全部名字;包 = 装模块的文件夹,`.` = 当前包。**

自测五问(合上文件先复述,再翻回对应小节对照):

1. import 一个模块,Python 做哪三件事?(9.1)
2. 为什么同一个模块 import 两次,顶层代码只跑一次?(9.1)
3. `__name__` 两副面孔分别是什么?守卫保护的是什么?(9.3)
4. 自己建一个 `json.py` 会发生什么?怎么提前发现?(9.4)
5. `from . import exercises` 的 `.` 是什么意思?为什么必须带?(9.5)

## 动手运行

```bash
python ch09/tiny_mod.py          # 直接跑:守卫里的代码执行(主角)
python ch09/01_import_basics.py  # 顶层 print 只出现一次!
python ch09/02_name_main.py
python ch09/03_packages.py
python ch09/04_module_object.py  # 翻开 sys.modules 记账本
```

对比 01 的输出和 tiny_mod.py 直接跑的输出,体会两副面孔。

## 练习

`exercises.py` 共 7 题。**本章的 import 全部要你自己写**——
骨架里一行 import 都没有,这就是练习的一部分!

```bash
python -m ch09.test_exercises   # 项目根目录运行
```

完成后对照 `answers.py`(先自己写,卡住超过十分钟再看;
它也能直接跑:`python ch09/answers.py`)。

下一章预告:**ch10 标准库漫游**——把自带电池装进你的工具带。
