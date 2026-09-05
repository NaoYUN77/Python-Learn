# ch11 同步与异步编程:asyncio 入门

> 官方文档:[asyncio — 异步 IO](https://docs.python.org/zh-cn/3/library/asyncio.html) ·
> 官方教程暂无 async 章,可读 [Real Python: Async IO](https://realpython.com/async-io-python/)(英文)
> 运行示例(项目根目录):`python ch11/01_sync_vs_async.py`(全部零依赖,直接跑)

## 11.0 为什么要学这个

真实世界的大量时间不是花在"计算"上,而是花在**等待**上:
等网络响应、等数据库返回、等文件读盘——LLM API 一次调用动辄几秒。

同步代码在等待时**寸步难行**;异步代码在等待时**转身去干别的**。
ch12 的 Agent 框架里,同时调三个工具、流式接收模型输出,全是 async 的地盘。
**本章目标:看懂 async 代码 + 会写简单的并发程序**,不求一步登天。

本章术语先亮出来(后面反复出现):

| 术语 | 一句话 |
|------|--------|
| 同步 | 一行干完等结果,再下一行——**排队等水开** |
| 异步 | 等的时候先去干别的——**水开之前切菜** |
| 协程函数 | `async def` 定义的函数——调用它**不执行**,只发一张"票" |
| 协程对象 | 调用协程函数得到的"票"——`await` 它(或包成 Task)才真正执行 |
| Task | `create_task` 提前点火的票:立刻排班,可随时查进度、收结果 |
| Future | 异步操作结果的**占位对象**:PENDING→被 set_result 填入→DONE;Task 是它的子类(11.8) |
| 可等待对象 | `await` 后面能接的东西:协程对象、Task、Future——都实现了 `__await__`(11.7) |
| `await` | "这里要等,先让出控制权"——协程的暂停点,顺便收结果 ⚠️简化版,精确版见 11.7 |
| 事件循环 | 调度员:盯着所有任务,谁不等了就轮到谁 |
| 并发 | 同一时间段交替推进多个任务(单核也能) |
| 并行 | 同一时刻真的同时执行(要多核) |

## 11.1 心智模型:煮两壶水(01)

同步 vs 异步,用"煮两壶水,每壶要 2 秒(演示尺度),煮开后还要倒水 0.5 秒"来演:

**同步版时间线**(01 示例上半段):

```
煮水1 ████████(等2s) 倒水1 ████(0.5s) 煮水2 ████████(等2s) 倒水2 ████
总耗时:5.0 秒 —— 等水开的 4 秒里,你干站着
```

**异步版时间线**(01 示例下半段):

```
煮水1 ████████
煮水2 ████████     ← 两壶同时煮!
倒水1 ████ 倒水2 ████
总耗时:3.0 秒 —— 等水开的时候,另一壶也在烧
```

省下的 2 秒 = **等待时间被重叠了**。计算本身没有变快(倒水还是要 1 秒总量),
快的是"等待被填满"。这就是异步的全部价值:**等网络/磁盘时别闲着**。

什么活适合异步?**I/O 密集**(网络请求、读文件)。
什么活不适合?**CPU 密集**(大循环算数)——那是多进程的地盘,本章不展开。

## 11.2 三件套:async def / await / asyncio.run(02)

### async def:定义协程

```python
async def boil(name, seconds):
    print(f"{name}: 开始煮")
    await asyncio.sleep(seconds)      # 等待点
    print(f"{name}: 水开了!")
    return f"{name} 的开水"
```

- `async def` 定义的函数叫**协程函数(coroutine function)**——调用它**不会执行**,而是返回一个"协程对象"(一张任务票)

**两个词先分清**(本章地基,02 示例会用 type() 亲眼验证):

| 名字 | 是什么 | 怎么得到 |
|---|---|---|
| **协程函数**<br>(coroutine function) | `async def` 定义的函数,相当于一张"菜谱" | `async def boil(): ...` 写出来就有 |
| **协程对象**<br>(coroutine object) | 调用协程函数发出来的"任务票" | `boil("壶1", 2)` 这样调用就发一张 |

极慢镜头:调用的那一瞬间发生了什么——

```python
async def boil(name, seconds):   # ← 定义:写下菜谱(函数体一行没跑)
    ...

coro = boil("壶1", 2)            # ← 调用:【不执行函数体!】只发一张票
type(coro)    # <class 'coroutine'>        ← 票的类型就叫 coroutine
coro          # <coroutine object boil at 0x...>
```

- 函数体想跑,票必须被"兑"——两条兑票路:`await coro`,或 `asyncio.create_task(coro)`(11.5)
- **票是一次性的**:一个协程对象只能被 await 一次,兑第二次直接
  `RuntimeError: cannot reuse already awaited coroutine`。要再跑,重新调用再造新票
- **新手第一大坑**:光调用不兑票,Python 会当场提醒
  `RuntimeWarning: coroutine 'boil' was never awaited`——票作废了,活儿根本没干

### await:在等待点让出控制权

```python
result = await boil("壶1", 2)
```

- `await` 做三件事:① 执行这个协程 ② **在它等待时让出控制权**(别人可以插进来跑) ③ 等它完成后**取回返回值**
  ⚠️ ② 是简化说法——让位的前提是**链条深处真的有等待**;没有的话它一口气跑到底。精确版见 11.7
- ⚠️ `await` 只能写在 `async def` 函数内部——不能在普通函数里用

### asyncio.run:点火(入口)

```python
asyncio.run(main())     # 程序入口:启动事件循环,跑完 main 再收摊
```

整个程序**只需要一个** `asyncio.run`,通常套在 `if __name__ == "__main__":` 里
(ch09 的守卫!)。它是同步世界通往异步世界的唯一大门。

### 一张图记住三件套

```
asyncio.run(main())          ← 点火(整个程序一次)
 └─ main() 里:await boil()   ← await 处让出控制权
     └─ async def boil()     ← 协程本体(能暂停/续跑的函数)
     └─ create_task(coro)    ← 也可提前点火,拿到 Task(11.5)
```

### 老规矩对照:sync 函数 vs async 函数

| | 普通函数 | 协程 |
|---|---|---|
| 定义 | `def f():` | `async def f():` |
| 调用 | 立刻执行 | 返回协程对象(票) |
| 拿结果 | 直接拿到 | 必须 `await` 才执行+拿到 |
| 内部暂停 | 不可能 | `await` 处可以暂停 |

## 11.3 事件循环:调度员在干什么

`asyncio.run` 背后站着**事件循环(event loop)**——整个异步世界的调度员。它的工作循环:

1. 看看**谁在等**(sleep 中、等网络中)→ 先不管
2. 找一个**能跑的**任务 → 跑到它**真正挂起**为止
   (不是"下一个 await"!await 只是接力,只有链条深处冒出还没完成的
   Future 才真挂起——精确版见 11.7)
3. 谁等完了(水开了)→ 标记为"能跑"
4. 回到 1,直到所有任务干完

关键认知:**同一时刻只有一行代码在跑**(单线程!),异步不是"同时干"而是
"**等的时候换人干**"。所以:

- 协程之间**不需要锁**来抢数据(不会真的同时改一个东西)——比多线程省心
- 协程里写**死循环不 sleep** 会卡死整个调度员(它只有一个人)
- `time.sleep(2)` 是同步的"站桩等"——协程里**必须用 `await asyncio.sleep(2)`**,
  前者等的时候不让位,后者等的时候让位。这是第二大坑!
  (为什么 asyncio.sleep 能让位?它内部有个"真等待"的定时器——精确机制见 11.7)

## 11.4 并发:gather 同发多票(03)

顺序 await 多个协程,还是排队(总时长 = 各任务之和);**gather 才是并发**:

```python
import asyncio

async def main():
    # 三张票一起交给调度员,等全部完成,结果按传入顺序排列
    results = await asyncio.gather(
        boil("壶1", 2),
        boil("壶2", 2),
        boil("壶3", 2),
    )
    print(results)      # ['壶1 的开水', '壶2 的开水', '壶3 的开水']

asyncio.run(main())
```

- `gather` 把多个协程**同时开跑**,自己也是一个可 await 的对象
- 等到**全部完成**才放行;返回值列表**按传入顺序**(与完成先后无关)
- 总耗时 ≈ **最长那个任务**(03 示例实测:三个 2 秒任务,gather 约 2 秒 vs 顺序 await 约 6 秒)

**跟踪表**(03 示例会真打印):

| 时刻 | 调度员视角 |
|---|---|
| t=0 | 壶1 开煮 → 遇 await 睡 → 让位;壶2 开煮 → 让位;壶3 开煮 → 让位 |
| t=0~2 | 三个都在"等水开",调度员闲转 |
| t=2 | 三壶同时"水开",挨个醒来打水平 |
| 收工 | gather 把三个返回值按传入顺序打包 |

### gather 的兄弟:as_completed(完成一个收一个)

`gather` 是"全部干完一起交卷";`asyncio.as_completed` 是**谁先完成先收谁的**——
适合"多个网络请求,谁先回来先处理"(Agent 并发调多个工具的写法)。认个脸,用到再学。

## 11.5 Task:把票提前塞给调度员(04)

`gather` 是"一口气 N 张票同时开工,原地等收工";
**Task 更自由:单张票提前点火,你去干别的,回头再收**:

```python
async def main():
    soup_task = asyncio.create_task(stew())   # ① 点火!汤立刻排班开炖
                                              #   (不等待,create 完就返回一个 Task)
    dish = await cut_veg()                    # ② 你去切菜——汤的等待被你填上了
    soup = await soup_task                    # ③ 回来收汤:大概率已经炖好了
```

- `create_task(coro)` 收一张**协程对象**,立刻塞进调度员的日程表,返回一个 **Task**;
  事件循环一有空隙(主流程一 await)就开跑它——04 示例的时间线会亲眼看到这一幕
- **Task 也是可等待对象**:`await task` 收结果;还能 `task.done()` 查干完没、
  `task.result()` 取结果(没干完会等)
- Task 内部有状态:点火后 pending(进行中),干完变 done——`done()/result()` 查的就是它
  (这套状态就是 11.8 的 Future 盒子状态——Task 是 Future 的子类)
- ⚠️ `create_task` 必须在**运行中的事件循环里**调用(写在 async def 里就对了);
  在普通函数里调它会报错——调度员还没上班,你把票塞给谁?
- 对照记忆:`await coro` = 站在灶前等它做完;`create_task(coro)` = 把锅点上火就走人。
  gather 底层干的也是"把每张票包成 Task"——所以 11.4 你其实已经用过它了

## 11.6 异常与超时:异步世界的 ch07(05)

```python
async def risky():
    await asyncio.sleep(0.5)
    raise ValueError("网络炸了")

async def main():
    try:
        await risky()
    except ValueError as e:                 # 型号照旧按 ch07 接!
        print(f"接住:{e}")
```

try/except 语法**一字不变**——异常照常沿 await 链上传,按型号接。
gather 有个开关:`return_exceptions=True` 把异常当**返回值**收进列表而不是炸停整船——
并发调多个 LLM 时常用(一个失败别连坐其他)。

**超时**(Agent 开发刚需——LLM 可能卡住):

```python
async def main():
    try:
        async with asyncio.timeout(3):      # 3 秒干不完就掐
            await some_slow_thing()
    except TimeoutError:
        print("超时收工")                    # Python 3.11+;3.10 用 wait_for
```

3.10 的老写法:`await asyncio.wait_for(coro, timeout=3)`——两种都认得。

## 11.7 深一层:await 到底让不让位?(06)

11.2/11.3 说"await = 暂停点、让位"——那是**简化版**。你现在已经见过 gather、Task、
异常了,可以上精确版了。一句话:**`await` 不保证让位,它只是"可能的暂停点"**。

### await 的真实含义:驱动执行,直到"真等待"或"跑完"

`await x` 的本质是**驱动 x 执行**,结果二选一:

1. **链条深处有东西真的在等**——一个还没完成的 Future 从链条深处冒上来
   → 整条链在这里挂起,调度员去跑别人(这才是"让位")
2. **x 一路跑到底完成了**——直接拿返回值,**全程没让位,调度员靠边站**

谁会把 Future 冒上来?**真在等外界的东西**:`asyncio.sleep` 的定时器、
网络 I/O、还没完成的 Task……await 链像**一根直通的管子**,
只有这些"真等待"才是闸口:

```python
async def deep():
    await asyncio.sleep(1)     # ← 真闸口在这:定时器 Future 从这冒上来
    return 42

async def middle():
    return await deep()        # ← 只是"接力执行",自己不是暂停点!

result = await middle()        # main 只在 deep 的 sleep 处挂起过一次
```

06 示例①用时间戳证明了这件事:`middle:开跑` 和 `deep:开跑` 是**同一瞬间**打出来的——
`await middle()` 那一行根本没停,一路接力到 sleep 才真挂起。

### 反面实锤:await 一个"从不让位"的协程

```python
async def busy(n):
    total = 0
    for i in range(n):         # 纯 CPU,零 await——没有任何"真等待"
        total += i
    return total

await busy(20_000_000)         # 语法完全合法!但它一口气跑到底……
```

后果:执行期间**调度员被饿死**,其他任务全部停摆——06 示例②里,
心跳协程在 busy 运行的近 1 秒里一声没吭,一换回 `asyncio.sleep` 立刻复活。
这也从底层解释了 11.3 的两条老话:
- `time.sleep` 为什么是灾难:它压根不走协程链条,连 Future 都没有,直接卡死线程;
- 异步为什么只救 I/O 密集:CPU 密集的活,就算包进协程、await 得再标准,
  也没有真等待可冒,照样饿死调度员。

### await 后面能接什么:可等待对象(Awaitable)三兄弟

凡是实现了 `__await__` 方法的对象都是可等待对象,共三兄弟:

| 可等待对象 | 是什么 | await 它会发生什么 |
|---|---|---|
| 协程对象 | 调用协程函数的产物 | 接力执行函数体,到深处的真闸口才挂起 |
| Task | `create_task` 包出来的、已在排班的任务 | **没干完**→挂起等它;**已干完**→秒拿结果,不让位 |
| Future | 异步操作结果的**占位对象**(11.8 专题解剖) | 没好→挂起;好了→秒拿(Task 是它的子类) |

注意 Task 那一行:await 已完成的 Task **不让位**——又一个"可能暂停"的实锤。
(自己写 `__await__` 定制 awaitable?认个脸就行,那是框架作者的事。)

> **Agent 场景预警(ch12)**:async def 里的每一行都在花"调度员的独占时间"。
> 长活别硬扛——CPU 密集丢给 `asyncio.to_thread`(认个脸),
> 或拆碎步骤、中途 `await asyncio.sleep(0)` 主动让一次位。

## 11.8 Future:异步操作结果的占位对象(07)

11.7 说"让位 = 链条深处冒上来一个还没完成的 Future"。这个 Future 到底是什么?
一句话定义:**它是一个"现在还没有、将来会有"的值的容器——异步操作结果的占位对象。**

### 定义与状态机

Future 创建时是空的(PENDING),将来被填入值或异常,翻转为 DONE。
整个生命周期只有三条路:

```
PENDING ──set_result(v)────→ DONE(值=v;await 它 → 拿到 v)
PENDING ──set_exception(e)─→ DONE(异常=e;await 它 → 原样抛出 e,ch07 型号照接)
PENDING ──cancel()─────────→ CANCELLED(await 它 → 抛 CancelledError)
```

常用 API:`fut.done()` 查好了没;`fut.result()` 取值——⚠️ **PENDING 时调用
直接抛 InvalidStateError**,它不是"阻塞着等",是"没好就别拿";
老式回调风格还有 `fut.add_done_callback(fn)`(认个脸,async 之前的写法)。

### 关键认知:盒子自己不会变好

**必须有人调用 `set_result` 填盒**。这是 Future 和普通变量最大的不同:
变量是你现在赋值它才有值,Future 是"别人将来填"的容器——它把"还没发生的结果"
变成一个可以被**传递、被等待、被填充**的一等公民。

谁来填?应用代码几乎从不手工造 Future,**填盒的都是"外界/循环机器"**:

| 场景 | 谁填盒 |
|---|---|
| `asyncio.sleep(2)` | 循环的定时器到点 → 回调替你 set_result |
| 网络 I/O | 数据到达 → 传输层回调 → set_result |
| `asyncio.to_thread(...)` | 线程里的活干完 → set_result |
| Task | **协程跑完,Task 自己填自己**(见下) |

### 解剖 asyncio.sleep:它只是个"等盒子的普通协程"

把 sleep 的源码骨架摆出来(简化),你会发现"暂停"没有任何魔法:

```python
async def sleep(delay, result=None):
    if delay <= 0:
        await __sleep0()                    # sleep(0):立刻让一次位
        return result                       #  (内部是个裸 yield,课程后面再拆)
    fut = loop.create_future()              # ① 造占位盒
    loop.call_later(delay, fut.set_result, result)
                                            # ② 登记闹钟:到点有人替我填盒
    return await fut                        # ③ 等盒:没好挂起,填了醒来拿值
```

**sleep 的"暂停能力"完全来自 Future。** 它不是语法魔法,只是一个
"等盒子被填"的普通协程——你自己也能造一套(07 示例:一个"送货员"
睡 0.5 秒后 set_result,await 盒子的 main 立刻醒来拿到值)。

### Task 和 Future 的精确关系

`Task 是 Future 的子类`(class Task(Future))——一句话分清两兄弟:

| | 谁执行代码 | 谁填盒 |
|---|---|---|
| **Future(被动盒)** | 不执行任何代码 | 必须**别人**来 set_result |
| **Task(主动盒)** | 事件循环替它**跑包着的协程** | 跑完后**自己给自己 set_result** |

所以 `create_task` 返回的东西两头通吃:既是"进行中的活"(11.5),
又是"将来的结果盒"(本节)。`gather` 的返回值也是 Future——
一个"等里面全部干完才被填入结果列表"的**聚合盒**。

### 两个精确细节(07 示例里都能看到)

1. `set_result` **不会立刻打断别人**:它只是把等待者登记为"能跑了",
   真正切换要等当前代码让位。所以 07 示例里"送货员"填完盒还能先把自己
   那行 print 打完,main 才醒来。
2. 没人填的盒子会**等到天荒地老**——这也是 11.6 的 `asyncio.timeout`
   存在的理由之一。

## 11.9 和 Agent 的连接(ch12 预告)

你现在已具备读懂真实框架代码的全部语法。pydantic-ai 的两兄弟:

```python
result = agent.run_sync("你好")            # 同步版:内部替你跑事件循环
result = await agent.run("你好")           # 异步版:并发场景用这个
```

Agent 的真实并发场景(下一章你会亲眼见到):

```python
results = await asyncio.gather(
    weather_agent.run("杭州天气?"),
    news_agent.run("今日头条?"),
    calc_agent.run("1+1=?"),
)
```

三个模型同时调,总耗时 = 最慢那个——**这就是 11.4 的 gather**,
只不过协程里 await 的不是 sleep,是网络请求。**asyncio 是 Agent 的腿。**

## 11.10 小结与自测

一句话:**async def 造票,await 兑票并驱动执行;让位只发生在链条深处有"真等待"
(Future 冒上来)的时候——没有就一口气跑到底,调度员被饿死;
可等待对象三兄弟:协程对象/Task/Future;Future=异步操作结果的占位盒
(PENDING→set_result/set_exception→DONE,Task 是"会自己跑、自己填"的子类);
asyncio.run 全程序点火一次;gather 同发多票、create_task 单张提前点火
(总时长≈最慢任务);协程里睡觉必须 asyncio.sleep(time.sleep 会卡死调度员);
异常照常按型号接,超时用 asyncio.timeout;
异步省的是"等待被重叠",CPU 密集帮不上忙——包进协程也救不了。**

自测九问(合上文件先复述):

1. 调用 `async def` 函数会发生什么?怎么才真正执行?(11.2)
2. 协程函数和协程对象,哪个是菜谱、哪个是票?票能兑两次吗?(11.2)
3. `await` 写在普通函数里行吗?`time.sleep` 和 `await asyncio.sleep` 在协程里的本质区别?(11.2/11.3)
4. 三个 2 秒任务:顺序 await 总耗时?gather 总耗时?为什么?(11.4)
5. gather 的结果顺序按什么排?`create_task` 和直接 `await` 的差别是什么?(11.4/11.5)
6. gather 默认一颗雷炸全船,怎么让异常"当返回值收进列表"?(11.6)
7. `await` 一定让位吗?什么时候例外?可等待对象有哪三兄弟?(11.7)
8. 为什么把大循环包进协程也快不了?要快该怎么办?(11.7)
9. Future 是什么?谁负责填盒?Task 和 Future 什么关系?await 一个装了异常的盒子会怎样?(11.8)

## 动手运行

```bash
python ch11/01_sync_vs_async.py     # 煮两壶水:时间线对比(计时输出)
python ch11/02_async_basics.py      # 三件套最小演示 + 调用不执行的坑
python ch11/03_gather_race.py       # gather 并发实测:3 个任务 2 秒 vs 6 秒
python ch11/04_task_demo.py         # Task:提前点火,等待里干活
python ch11/05_timeout_errors.py    # 超时 + 异常:Agent 场景预演
python ch11/06_await_truth.py       # await 的真相:可能暂停点 + 被饿死的心跳
python ch11/07_future_box.py        # Future:手工造盒 + 送货员填盒
```

## 练习

`exercises.py` 共 7 题:练习文件里**不许**随手 asyncio.run——
想亲手点火,写进文件底部的"点火台"(守卫内,被导入时不执行)。
其余照旧。交卷前照例扫 import 区三查。

```bash
python -m ch11.test_exercises    # 项目根目录运行
```

下一章预告:**ch12 主流 Agent 开发框架**——pydantic 打底、pydantic-ai 上手,
你刚学的 gather 就要上场并发调模型了。
