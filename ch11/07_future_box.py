"""07 — Future:异步操作结果的占位对象(README 11.8)

Future = 一个"现在还没有、将来会有"的值的容器:
  造出来是空的(PENDING) → 有人 set_result 填值(或 set_exception 装异常) → DONE
  await 没好的盒子 = 挂起;盒子被填 = 醒来拿值(装了异常就原样抛出)
盒子自己不会变好——必须有人填。Task 就是"会自己跑、自己填"的 Future 子类。

运行:python ch11/07_future_box.py   (约 0.6 秒)

预期输出(时间戳为约值):
[ 0.0s] 造好一个空盒子:PENDING,done? False
[ 0.0s] 送货员排班完毕,开始 await 盒子……
[ 0.5s] 送货员:set_result('📦 外卖到了')——填盒只登记'能跑',不打断人,所以这行先打
[ 0.5s] await 醒来,盒子里拿到:'📦 外卖到了',done? True
[ 0.5s] 装了异常的盒子:await 时原样抛出 ValueError:盒子里的雷(ch07 型号照接)
"""
import asyncio
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def deliverer(fut, what, delay):
    """送货员:睡够 delay 秒(真等待),把结果填进盒子"""
    await asyncio.sleep(delay)            # 真等待:定时器闸口
    fut.set_result(what)                  # ← 填盒!等盒子的任务被登记为"能跑了"
    print(f"{stamp()} 送货员:set_result({what!r})"
          f"——填盒只登记'能跑',不打断人,所以这行先打")


async def main():
    loop = asyncio.get_running_loop()

    # ── ① 造一个空盒,交给送货员,await 它 ──────────────────
    fut = loop.create_future()            # 占位盒:PENDING,里面什么都没有
    print(f"{stamp()} 造好一个空盒子:PENDING,done? {fut.done()}")

    asyncio.create_task(deliverer(fut, "📦 外卖到了", 0.5))
    print(f"{stamp()} 送货员排班完毕,开始 await 盒子……")

    result = await fut                    # 没好 → 挂起;被填 → 醒来拿值
    print(f"{stamp()} await 醒来,盒子里拿到:{result!r},done? {fut.done()}")

    # ── ② 装了异常的盒子:await 时原样抛出 ──────────────────
    fut2 = loop.create_future()
    fut2.set_exception(ValueError("盒子里的雷"))   # 填进去的不是值,是异常
    try:
        await fut2                        # 醒来的方式 = 原样抛出(ch07)
    except ValueError as e:
        print(f"{stamp()} 装了异常的盒子:await 时原样抛出"
              f" {type(e).__name__}:{e}(ch07 型号照接)")


if __name__ == "__main__":
    asyncio.run(main())
