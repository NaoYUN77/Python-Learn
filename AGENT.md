# AGENT.md — Agent 协作说明

> 本文件供 AI Agent（或新协作者）快速了解项目状态、约定与环境限制。接手前请先读完。

## 项目定位

基于 [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/) 的中文入门课程，
最终目标是为 **Agent 开发**打基础（类/OOP、异步是直接前置知识；
ch10 标准库与第三方库 + ch12 Agent 开发是收官主线）。

## 目录结构约定

| 目录 | 作用 |
|------|------|
| `chNN/` | 各章课程内容（见下方章节格式约定） |
| `mistakes/` | 错题本：学员的错误记录与统计 |
| `boost/` | 强化专题：学员对某知识点集中提问后，Agent 生成的单主题深入文件（如 `boost/ch05_tuples.py`）。命名 `chNN_主题.py`，可运行、带自测题 |
| `boost/quiz/` | 复习测验包：章节总结后的实战自测。格式与 chNN 一致（exercises/answers/test_exercises），test 带评分系统（满分 100 + 评级 🏆😊💪），按测试点计分 |
| `.zed/debug.json` | Zed 调试配置（4 个方案：调试当前文件 + ch04/05/06 测试），adapter=Debugpy |

### 章节主题对照（2026-09-04 晚二次调整后）

| 章节 | 主题 | 说明 |
|------|------|------|
| ch10 | 标准库漫游 + 常用第三方库 | 含 pip 生态盘点（requests/httpx/pydantic…） |
| ch11 | 同步与异步编程 | asyncio 入门，Agent 开发直接前置 |
| ch12 | Agent 开发入门 | Agent Loop + pydantic + pydantic-ai（参照 Vercel AI SDK 概念体系与 pydantic-ai 官方文档） |

> 📌 2026-09-04 晚二次调整（比 16:02 的重组更新）：章节顺序最终定为
> ch10=标准库（原 ch10 内容就地正式化，幽灵 import 提法同步为"七连"）、
> ch11=异步（全新生成）、ch12=Agent。ch11 旧标准库残留已清理（ch10 有正式版），
> `_del_ch11.py` / `_tmp_check_ch10_answers.py` 临时脚本已删——历史包袱清零。

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
  raise 主动抛（大声失败 vs 返回 None 静默失败）；裸 raise 在 except 里=原样转发；
  raise 新异常 from e=包装+留案底，原件在 `__cause__`；except 父类连子类一起接
  （JSONDecodeError ⊂ ValueError）；EAFP vs LBYL；调用者不需要逐层检查——不接自动上传，
  只在真能处理的那层接；型号不匹配=接不住=穿墙继续飞；CLI 入口接用户级错误体面退场
  （sys.exit(1)），bug 类故意不接让 Traceback 示众；危险行判断=「世界的锅用 except，
  你的锅改代码」，入口最危险越往里越安全
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
- **ch10（标准库+第三方库）**：标准库=自带电池，第三方库=pip 外接电池；
  Counter/defaultdict 替你写完 ch05 的计数/收集；seed 让随机可复现；
  路径是对象（. 取属性，/ 拼路）；日期是对象（相减得 timedelta）；
  strftime 出、strptime 进；正则三板斧 findall/search/sub；别猜要测先 timeit；
  pydantic 用类给数据立规矩（自动转型 + Field 约束 + ValidationError 逐字段报）
- **ch11（同步与异步）**：async def 造票（协程函数调用不执行→协程对象，一次性）；
  await=兑票+驱动执行，但**让位只发生在链条深处有"真等待"的 Future 冒上来时**
  （await 是可能的暂停点，不是必然——没有真等待就一口气跑到底，调度员被饿死；
  06 示例心跳实锤）；可等待对象三兄弟：协程对象/Task/Future（都实现 __await__，
  await 已完成的 Task 也不让位）；**Future=异步操作结果的占位对象**
  （PENDING→set_result/set_exception/cancel→DONE；填盒人：sleep 定时器/网络 I/O/
  to_thread；Task=会自己跑、自己填的 Future 子类；set_result 只把回调登记进就绪
  队列，不立刻切换执行权）；asyncio.run 全程序点火一次；create_task 提前点火
  （Task=带进度条的票，done()/result() 可查）；gather 总时长≈最慢、结果按传入顺序；
  time.sleep 卡死调度员，协程里只用 asyncio.sleep；return_exceptions 让异常不连坐；
  asyncio.timeout 掐表（3.11+）；异步省的是"等待被重叠"，CPU 密集帮不上忙
  （包进协程也救不了，CPU 密集→asyncio.to_thread）
- **ch12（Agent 开发）**：Agent = LLM + 工具 + 循环（AI SDK 定义）；
  模型只点名不执行（安全根基）；工具结果必须进 history 喂回模型（否则无限循环）；
  max_steps/UsageLimits 是防烧钱安全带；pydantic-ai 三件套：
  @agent.tool（类型注解+docstring 即说明书）、output_type（输出即对象，不合格自动重试）、
  message_history（多轮记忆）；框架只是给内核加料——先内核后框架

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

## 当前进度（更新于 2026-09-04）

| 章节 | 状态 | 备注 |
|------|------|------|
| ch01 起步 | ✅ 内容完成 | 学员练习完成情况未验证 |
| ch02 数据类型与运算符 | ✅ 学员完成 | 8/8 改正后正确 |
| ch03 控制流 | 🔥 差最后确认 | 练习 5/6 代码已见改正；测试输出始终未贴 |
| ch04 函数 | 🔥 差小尾巴 | 9/9 通过 ✅；但 exercises.py 末尾的演示代码（area+print）、练习 3 坏注释、风格项仍未清（错题本 ⬜ 4 条） |
| ch05 数据结构 | ✅ 学员完成 | 9/9 通过，无错题 |
| ch06 输入输出与文件 | ✅ 测试收官 | 8/8 通过（2026-09-02 贴出）；错题本 3 条 ✅，练习 6 哑门卫（代码未改）与风格项仍 ⬜ |
| boost/quiz | ✅ 满分收官（2026-09-03） | 100/100 由 Agent 实跑确认 🏆；三处错误均已改正核验 |
| ch07 异常 | ✅ 功能收官（2026-09-03 核验） | 测试 8/8 实跑确认。**遗留卫生项 ⬜**：①双幽灵 import、④`except: raise`、⑤风格。错题本 ch07.md 已建（5 条） |
| ch08 OOP（类） | 🔥 收尾中 | 全套已生成并审读；遗留 ⬜：幽灵 import 第六次（L17 整行删）+ 逗号前空格。mistakes/ch08.md 已建 |
| ch09 模块与包 | 🔥 学员开做（2026-09-03） | 全套已生成并验证，学员开做。交卷后 Agent 实跑测试出分 + 审读 import 区 + 建 mistakes/ch09.md |
| ch10 标准库+第三方库 | ✅ 内容就绪（2026-09-04 晚二次定稿） | 原 ch10 标准库内容就地正式化（README 10.x + 8 示例 + 7 题 + 测试 + 答案），学员未开做 |
| ch11 同步与异步编程 | ✅ 内容就绪（2026-09-05 二次增补：await 精确语义 + Future 专题） | README 11.0-11.10 + 7 示例（01 同步异步对比 / 02 三件套+协程函数vs协程对象 / 03 gather 竞态 / 04 Task 提前点火 / 05 超时+异常 / 06 await 真相+awaitable 三兄弟 / 07 Future 手工造盒）+ 7 题（含点火台）+ 测试 + 答案；空骨架测试 0/7 不崩，7 示例时间线逐一对过。11.7 节与 06 示例系学员质疑"await 未必让位"后增补；11.8 Future 节与 07 示例系学员要求"概念不要糊弄、补 Future"后增补 |
| ch12 Agent 开发入门 | ✅ 内容就绪（2026-09-04） | 全套新生成：README 12.0-12.8（手搓 Agent Loop 四步教学 + pydantic + pydantic-ai 三场景 + 框架选型 + 自选难度练手项目）+ 4 示例（01 手搓 loop 零依赖零 key / 02 pydantic / 03 pydantic-ai 需 key / 04 概念地图零依赖）+ 7 题（只用 pydantic，不需要 key）+ 测试 + 答案 |
| boost/ | ✅ 活跃 | ch05_tuples.py、review_ch01_05.py、quiz/、ch06_json_direction.py、ch07_危险行判断.py |
| Zed 调试 | ✅ 已配置 | .zed/debug.json；学员已入门（F10/Variables/Console）；basedpyright 报错解读已教 |

## 待办 / 下一步

1. ~~ch07 收尾~~ ✅（2026-09-03）：测试已实跑核验 8/8、错题本已建并纠正。
   遗留：学员随时清三处卫生项。
2. **ch08 收尾（只差两处卫生项）**：剩幽灵 import（**整行删**）+ 逗号前空格 ⬜。
   ⚠️ 学员明确要求（2026-09-03）：**学习期间不要主动跑 ch08 测试**，等学员交卷再测。
3. ch09：学员开做中。**交卷后** Agent 实跑 `python -m ch09.test_exercises` 出分
   + 审读 import 区三查 + 建 mistakes/ch09.md。
4. **旧账三笔（随时可清）**：ch03 测试输出未贴；ch04 演示代码/坏注释；
   ch06 练习 6 哑门卫 + `f :` 风格。
5. **boost/ 维护**：候选专题：推导式专题、原地vs造新专题。
6. 学员薄弱点与讲解偏好：方向混淆、API 细节、编辑器误操作（幽灵 import
   六连）、笔误、**边界条件/型号接错**。
   **讲解偏好：逐行拆解 + 数据流动图 + 跟踪表 + "极慢镜头手动展开"**；
   **2026-09-03 起新章节/新讲解一律不用 Go 对照**；调试器逐帧验证已入门。
   **2026-09-05 起概念讲解要给到机制层**：学员已会质疑简化模型
   （主动指出"await 未必让位，取决于 awaitable 是否交还控制权"）——
   比喻之后必须补精确版，别只停在比喻
7. **学员流程约定（2026-09-03）**：① 先不回头检查旧章节；② 学员说「开始」=
   按 README 学习流程进入下一章（README → 示例 → 练习，交卷后才出分审读）。
8. **章节重组（2026-09-04）**：原 ch10（标准库）→ 迁为 **ch11** 并扩写第三方库节；
   **ch12** 新建（Agent 开发：pydantic 打底 + pydantic-ai 上手，参照 Vercel AI SDK
   概念体系）；**ch10** 改题为同步与异步编程（内容待生成）。根 README 课程地图已同步。
   ⚠️ 同日晚间二次调整：标准库留驻 **ch10**、异步改定 **ch11** 并已生成——以
   「章节主题对照」最新表为准（16:02 版的 ch10=异步/ch11=标准库已作废）。
9. ~~ch10 清场~~ ✅（2026-09-04 晚）：ch11 旧标准库残留已清（ch10 有正式版，
   清场前已确认学员未动工），ch11 已重建为 asyncio 新章并实跑核验；
   `_del_ch11.py` / `_tmp_check_ch10_answers.py` 临时脚本均已删除。
