# AGENT.md — Agent 协作说明

> 本文件供 AI Agent（或新协作者）快速了解项目状态、约定与环境限制。接手前请先读完。

## 项目定位

基于 [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/) 的中文入门课程，
最终目标是为 **Agent 开发**打基础（类/OOP、异步是直接前置知识）。

## 目录结构约定

| 目录 | 作用 |
|------|------|
| `chNN/` | 各章课程内容（见下方章节格式约定） |
| `mistakes/` | 错题本：学员的错误记录与统计 |
| `boost/` | 强化专题：学员对某知识点集中提问后，Agent 生成的单主题深入文件（如 `boost/ch05_tuples.py`）。命名 `chNN_主题.py`，可运行、带自测题 |
| `boost/quiz/` | 复习测验包：章节总结后的实战自测。格式与 chNN 一致（exercises/answers/test_exercises），test 带评分系统（满分 100 + 评级 🏆😊💪），按测试点计分 |
| `.zed/debug.json` | Zed 调试配置（4 个方案：调试当前文件 + ch04/05/06 测试），adapter=Debugpy |

## 章节格式约定（新章节必须遵守）

每章一个目录 `chNN/`，包含：

| 文件 | 作用 |
|------|------|
| `README.md` | 理论讲解，含官方文档链接、运行说明、练习入口 |
| `01_xxx.py`, `02_xxx.py` … | 编号示例脚本，可直接 `python chNN/01_xxx.py` 运行，注释里写预期输出 |
| `exercises.py` | 练习题，函数体只留 TODO + `pass`，由学员填写 |
| `test_exercises.py` | 自动检查，`from . import exercises`（**显式相对导入**），自带轻量 test runner（不依赖 pytest），风格仿 ch01/ch02 |
| `answers.py` | 参考答案，带 `if __name__ == "__main__"` 演示块 |

### 运行方式（重要）

- 示例脚本：`python chNN/01_xxx.py`
- 测试必须在**项目根目录**用模块方式运行：`python -m chNN.test_exercises`
  （boost/quiz 同理：`python -m boost.quiz.test_exercises`）

### 教学风格

- 所有解释、注释、README 用中文
- 每个 TODO 注释里给提示但不给答案
- 测试失败信息要说明"应为什么，实际得到什么"
- 语气鼓励，带 emoji（✅❌🎉）与主 README 风格一致

## 错题本约定（mistakes/）

每次审读学员练习后，**出错的题必须同步记入 `mistakes/chNN.md`**，格式：

- 状态（⬜ 待改正 / ✅ 已改正——只有看到学员改对或测试通过后才翻 ✅）
- 错误代码原样、报错信息、错因分析、正确写法、一句话教训
- `mistakes/README.md` 里的总索引和错误类型统计同步更新

目的：学员复习时只看 mistakes/ 即可；新 Agent 接手时先读它能快速了解学员的薄弱点。

## 环境限制（已踩过的坑）

- ~~Windows 11 + Zed，无 POSIX shell~~ **已过时（2026-09-03）**：终端恢复可用，
  `python` 可直接跑。**Agent 现在能自己运行/验证命令**（跑测试、出分、演示），
  学员不再需要贴输出；建目录、写文件也可由 Agent 完成。
- ~~写新文件前目录必须已存在（用户提前 mkdir）~~ 已过时（2026-09-03 终端恢复后
  Agent 可自建目录）。ch08/ 已生成全套内容（README + 3 示例 + 练习/测试/答案）。
- 静态检查用 Pylance/Pyright：避免隐式相对导入。注意 boost/quiz 的 answers.py
  需要 `from . import exercises`（学员答案可能组合复用）。
- 学员用编辑器自动补全，出现过"幽灵 import"（ch03 sqlite3、ch04 winreg；
  ch06 第三、四次：calendar 删成半截又炸、asyncio.ensure_future；
  **ch07 第五次：`from json.decoder import JSONDecodeError` + `from shutil import
  RegistryError` 双幽灵，后者连 shutil 都没 import——补全套娃误选**），审读时留意 import 区。
  **教训沉淀：让学员删 import 必须强调"整行删"；交卷前扫 import 区是固定动作。**
- Zed 自带 markdown 预览（命令面板 `markdown: toggle preview`），emoji 渲染在
  Windows 上可能显示为方框——源文件没问题，是预览字体覆盖问题，不影响阅读。

## 各章总结沉淀（供出题/复习引用）

> 完整版在 `boost/review_ch01_05.py`（可运行），测验在 `boost/quiz/`。
> 专题文件：`boost/ch06_json_direction.py`（json 方向）、
> `boost/ch07_危险行判断.py`（危险行判断标准 + return 三情形 + 快问快答）。

### 各章一句话核心

- **ch01-02**：类型决定能做什么。字符串不可变（upper 返回新串）；切片含头不含尾；
  转换显式（int("abc") → ValueError）；真假值（0/""/[] 为假）
- **ch03**：分支选择、循环重复。return 立刻结束函数；结论性 return 和 for 对齐；
  break 跳出整层循环；range 含头不含尾；化简 `return n % 2 == 0`
- **ch04**：函数靠参数+return 交换。`*`/`**` 定义时打包（args 元组/kwargs 字典）、
  调用时解包；可变默认值坑（None 占位）；lambda 当 key；闭包 nonlocal；
  `return a, b` 是逗号打包成元组
- **ch05**：四大容器。原地方法返回 None（sort/append），sorted 造新；
  空集合 set() 而非 {}；推导式是表达式必有值（新列表）；
  if 在 for 后=门卫（减数量），三元 if 在前=加工厂（不减数量）；
  计数模式 `counts[ch] = counts.get(ch, 0) + 1`；
  收集模式 `d.setdefault(name, []).append(x)`
- **ch06**：程序与外界交换。input 永远返回 str；文件三步与 with（异常也保证关）；
  文件可迭代=迭代协议（next 读一行、光标前进、StopIteration 收工，只能遍历一次）；
  json 四兄弟方向：dump/dumps=序列化（对象→文本），load/loads=反序列化（文本→对象），
  s=走字符串、无 s=走文件；load 返回 dict 还是 list 看文件顶层首字符（{ 或 [）；
  存中文必带 ensure_ascii=False；补零位数=下限（年:04d 月日:02d）
- **ch07**：异常=运行时的信号对象（类型+消息）。except 按类型接、从上往下命中即止；
  子类在前父类在后（遮蔽）；try 只包危险行；else=没炸才跑；finally=永远跑
  （with 的内部原理），finally 里 return 会截胡——只做清理；
  raise 主动抛（大声失败 vs 返回 None 静默失败）；裸 raise 在 except 里=原样转发
  （= Go 的 return err）；raise 新异常 from e=包装+留案底（= Go 的 %w），
  原件在 `__cause__`；except 父类连子类一起接（JSONDecodeError ⊂ ValueError）；
  EAFP vs LBYL；调用者不需要逐层检查——不接自动上传，只在真能处理的那层接；
  型号不匹配=接不住=穿墙继续飞；CLI 入口（main）接用户级错误体面退场（sys.exit(1)），
  bug 类故意不接让 Traceback 示众；危险行判断=「世界的锅用 except，你的锅改代码」，
  入口最危险越往里越安全
- **ch08**：类=图纸 实例=产品。__init__ 打包、self=实例自己；实例属性每对象一份、
  类属性共享；继承=括号写父类、super().__init__() 借父初始化；重写=同名盖父类；
  多态=父类方法里的 self.area() 钩子调到子类实现；鸭子类型=不看血统看会不会叫；
  `_` 开头=内部约定，封装是约定不是牢门；__repr__ 给开发者看（!r 带引号）；
  对象实例可以直接当参数传
- **ch09**：模块=.py 文件；import=找到→执行顶层（只一次）→sys.modules 记账
  （所以 import 有副作用）；`__name__` 两副面孔（直接跑="__main__"/被导入=模块名）
  →演示必须加守卫；from . import exercises=显式相对导入（"."=当前包）；
  sys.path 脚本目录排最前→同名文件会遮蔽标准库（stdlib_module_names 可查）；
  标准库=自带电池（Counter=ch05 计数一行版）

### 学员高频坑（mistakes 提炼，复习时优先盯）

1. split/join 方向写反（ch02）；**json 方向口头反 6 次（ch06，代码全对，专题已建）**
2. 循环内过早 return（ch03）
3. 下标 vs 值混淆（ch03）；数字当可迭代对象（quiz evens 漏 range）
4. join 分隔符逐字符写：`", "` 不是 `","`（ch04）
5. **幽灵 import ×6**（sqlite3/winreg/calendar/asyncio/ch07 双幽灵/ch08 boost 套娃——首次带副作用：import 即执行 boost 顶层演示）——交卷前扫 import 区，整行删
6. 演示代码误入 exercises.py——练习文件只放练习
7. 冒号前空格 **连续四章**（ch03/ch04/ch06/ch07）；语法笔误葬送全卷（quiz for 少冒号）
8. **边界条件**（ch07：`== 100` 写成 `> 100` 的反例——`score == 100` 把满分判非法）；
   **型号接错**（ch07：FileExistsError ≠ FileNotFoundError，一字之差意思相反）
9. **裸 except 违规**（ch07：`except: raise` 想转发却吞 Ctrl+C——转发不需要写，
   没接住的自动上传）
10. **守门后忘正事 / 累加器循环内清零**（ch08：deposit 只 raise 不加钱；best
   缩进在 for 内每轮归零——与 ch03 过早 return 同族）；**手滑三连**（disposit
   拼写、`self.amount += self._balance` 幽灵属性+方向反、漏扣款行）

## 当前进度（更新于 2026-09-03）

| 章节 | 状态 | 备注 |
|------|------|------|
| ch01 起步 | ✅ 内容完成 | 学员练习完成情况未验证 |
| ch02 数据类型与运算符 | ✅ 学员完成 | 8/8 改正后正确 |
| ch03 控制流 | 🔥 差最后确认 | 练习 5/6 代码已见改正；测试输出始终未贴 |
| ch04 函数 | 🔥 差小尾巴 | 9/9 通过 ✅；但 exercises.py 末尾的演示代码（area+print）、练习 3 坏注释、风格项仍未清（错题本 ⬜ 4 条） |
| ch05 数据结构 | ✅ 学员完成 | 9/9 通过，无错题 |
| ch06 输入输出与文件 | ✅ 测试收官 | 8/8 通过（2026-09-02 贴出）；错题本 3 条 ✅，练习 6 哑门卫（代码未改）与风格项仍 ⬜ |
| boost/quiz | ✅ 满分收官（2026-09-03） | 100/100 由 Agent 实跑确认 🏆；三处错误（evens 漏 range、for 少冒号、calendar 半截 import）均已改正核验 |
| ch07 异常 | ✅ 功能收官（2026-09-03 核验） | ②③已改正；测试 8/8 由 Agent 实跑确认（终端已修复）。**遗留卫生项 ⬜**：①双幽灵 import、④`except: raise`、⑤风格——测试可过但代码未清。错题本 ch07.md 已建（5 条；其中 3 条曾误记 ✅，已按盘面改回 ⬜ + RegistryError 勘误：本机 shutil 真实存在，import 不炸）。学员追问质量高：调用链 vs 继承树、异常往哪传、except 接不住会怎样、危险行判断、嵌套 raise from 解读——概念已通 |
| ch08 OOP （类） | 🔥 收尾中（2026-09-03） | 全套已生成（README 8.0-8.11 + 3 示例 + 9 题 + 测试 + 答案；封装两讲 8.3/8.4：打包 + `_` 约定守门）。审读推进：练习 3/8/9 代码错误**均已改正**（盘面核验）；遗留 ⬜：幽灵 import 第六次（L17 `from boost.ch05_tuples import result` 整行删）+ 逗号前空格。mistakes/ch08.md 已建 |
| ch09 模块与包 | 🔥 学员开做（2026-09-03） | 全套已生成并**重构加详**（README 9.0-9.8：import 三帧极慢镜头+跟踪表、三姿势原料产物表、__name__ 跟踪表、sys.path 顺位表、术语表+自测五问；tiny_mod 小白鼠 + **4 示例**（04=模块对象+sys.modules 记账现场，含撕账重演）+ 7 题 + 测试 + 答案；**练习骨架零 import——import 本身是练习**）。幽灵 import 终结章。⚠️ 本章起讲解一律不用 Go 对照（学员要求） |
| ch10 标准库 | ⬜ | 标准库漫游（ch09 README 已预告） |
| ch11 同步与异步 | ⬜ | asyncio 入门，Agent 开发直接前置 |
| boost/ | ✅ 活跃 | ch05_tuples.py、review_ch01_05.py、quiz/、ch06_json_direction.py、**ch07_危险行判断.py（新）** |
| Zed 调试 | ✅ 已配置 | .zed/debug.json；学员已入门（F10/Variables/Console）；basedpyright 报错解读已教（参数挂错函数：open vs dump） |

## 待办 / 下一步

1. ~~ch07 收尾~~ ✅（2026-09-03）：测试已实跑核验 8/8、错题本已建并纠正。
   遗留：学员随时清三处卫生项（双幽灵 import 整行删、删 `except: raise` 块、风格）。
2. **ch08 收尾（只差两处卫生项）**：练习 3/8/9 的代码错误均已改正 ✅（2026-09-03
   盘面核验：deposit 正事已补、best 移出循环、disposit/_balance 方向/扣款行全对）；
   剩 L17 幽灵 import（**整行删**）+ 逗号前空格 ⬜。改完喊 Agent 复核翻账。
   ⚠️ 学员明确要求（2026-09-03）：**学习期间不要主动跑 ch08 测试**，等学员交卷再测。
3. ~~ch09 生成~~ ✅（2026-09-03）：全套 8 文件已生成并验证（01 顶层 print 只出现一次；骨架 0/7 不崩；答案自洽 6/7——who_am_i 例外属预期），学员开做。学习顺序：
   README → `python ch09/tiny_mod.py`（对比 01 的输出）→ 01/02/03/04 → exercises
   （import 自己写）。**交卷后** Agent 实跑 `python -m ch09.test_exercises` 出分
   + 审读 import 区三查 + 建 mistakes/ch09.md。
4. **旧账三笔（随时可清）**：ch03 测试输出未贴；ch04 演示代码/坏注释；
   ch06 练习 6 哑门卫 + `f :` 风格。
5. ~~quiz 出分~~ ✅（2026-09-03）：Agent 实跑 `python -m boost.quiz.test_exercises` → **100/100 满分**，三处错误均已改正核验。
6. **boost/ 维护**：候选专题：推导式专题、原地vs造新专题
   （ch07_危险行判断.py 已建 2026-09-02）；多态/鸭子类型 2026-09-03 已讲通，
   学员随即转入 ch09，暂缓入册。
7. 学员薄弱点与讲解偏好：方向混淆（split/join 已治、json 已锚定——代码全对、口头易反，
   复述时盯"箭头方向+术语标签+原料产物"三件套）、API 细节、编辑器误操作（幽灵 import
   六连）、笔误（fist/itme/test/_name_/disposit——Console 无补全更易手滑；语法笔误会葬送全卷；
   **边界条件/型号接错是 ch07 新增薄弱点**）。
   **讲解偏好：逐行拆解 + 数据流动图 + 跟踪表 + "极慢镜头手动展开"**；
   对"概念属于哪章"敏感；**从 Go 迁移而来，喜欢跨语言对照——但 2026-09-03 起
   新章节/新讲解一律不用 Go 对照（历史材料不动）**；学习方式：调试器逐帧验证（F10 + Variables + Console
   预演）已入门，basedpyright 报错自查已教。
   已透彻掌握：可变默认值坑、*args/**kwargs、lambda key、闭包 nonlocal、
   原地vs造新、推导式=表达式必有值、门卫if vs 三元if（含"抄模式先问前提"——
   strip 前后真假值差异）、字典计数、setdefault 链式、元组逗号身份证、星号解包、
   json 对象指 Python 数据、strip 两端空白、input 永远 str、
   文件迭代协议（next/光标/StopIteration/只遍历一次）、真假值判断依据、
   序列化/反序列化方向、load 类型看文件首字符、return 通道 vs 副作用通道、
   读取对象需变量承接（两级：return + 调用方赋值）、
   **ch07 新增：异常=信号对象（型号+载荷）、调用栈"上"≠继承树、except 型号不匹配=
   穿墙、不接自动上传/只在能处理层接、裸 raise=return err、raise from=%w、
   Traceback 从下往上读+bug 该修码/世界锅才 except、finally 截胡、危险行判断口诀、
   `[]` 通吃容器（序列报位置/字典报键）；
   **ch08 新增：类=图纸/实例=产品、__init__ 打包/self=实例自己、实例属性每对象一份 vs 类属性共享、
   继承括号+super().__init__ 借父初始化、重写、多态（父类 self.area() 钩子）、
   鸭子类型（会 speak 就行，不看血统）、封装 `_`=责任声明不是牢门、
   __repr__ 给开发者看（!r 带引号）、对象实例可直接当参数传**。
8. **学员流程约定（2026-09-03）**：① 先不回头检查旧章节（ch07/ch08 卫生项挂起，
   等学员主动喊复核）；② 学员说「开始」= 按 README 学习流程进入下一章
   （README → 示例 → 练习，交卷后才出分审读）。
