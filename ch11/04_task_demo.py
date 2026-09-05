"""04 — Task:把票提前塞给调度员(README 11.5)

gather 是"一口气 N 张票同时开工,原地等收工";
create_task 更自由:【单张票提前点火】,你去干别的,回头再收。

  await coro              = 站在灶前等它做完
  create_task(coro)       = 把锅点上火就走人,拿到一个 Task(带进度条的票)

运行:python ch11/04_task_demo.py   (约 5 秒)

预期输出(时间戳为约值):
--- 上半场:不用 Task(await 谁,就站桩等谁)---
[ 0.0s] 汤:上灶慢炖(要 2.0s)...
[ 2.0s] 汤:炖好了!
[ 2.0s] 切菜:咯吱咯吱(要 0.5s)...
[ 2.5s] 切菜:切好了
不点火总耗时 2.5 秒:先等汤(一锅鲜汤)再切菜(一盘青菜)

--- 下半场:create_task(先点火,等待里干活)---
[ 2.5s] 点火拿到 Task 类型——带进度条的票
[ 2.5s] 汤现在干完了吗?False(刚上灶,还没好)
[ 2.5s] 切菜:咯吱咯吱(要 0.5s)...
[ 2.5s] 汤:上灶慢炖(要 2.0s)...     ← 主流程一 await 让位,调度员立刻让汤开工!
[ 3.0s] 切菜:切好了
[ 3.0s] 切完菜,汤干完了吗?False(还炖着)
[ 4.5s] 汤:炖好了!
[ 4.5s] 收汤:一锅鲜汤(task.result() 也能取:一锅鲜汤)
点火总耗时 2.0 秒 —— 切菜的 0.5 秒填进了炖汤的等待里 ✅
"""
import asyncio
import time

START = time.perf_counter()


def stamp():
    return f"[{time.perf_counter() - START:4.1f}s]"


async def stew():
    """炖汤:要 2 秒(演示尺度)"""
    print(f"{stamp()} 汤:上灶慢炖(要 2.0s)...")
    await asyncio.sleep(2.0)
    print(f"{stamp()} 汤:炖好了!")
    return "一锅鲜汤"


async def cut_veg():
    """切菜:要 0.5 秒"""
    print(f"{stamp()} 切菜:咯吱咯吱(要 0.5s)...")
    await asyncio.sleep(0.5)
    print(f"{stamp()} 切菜:切好了")
    return "一盘青菜"


async def main():
    # ── 上半场:不用 Task(await 谁,就站桩等谁)──────────────
    print("--- 上半场:不用 Task(await 谁,就站桩等谁)---")
    t1 = time.perf_counter()
    soup = await stew()              # 汤炖好之前,你哪儿也去不了
    dish = await cut_veg()           # 汤好了才开始切菜——炖汤的等待全浪费了
    print(f"不点火总耗时 {time.perf_counter() - t1:.1f} 秒:"
          f"先等汤({soup})再切菜({dish})\n")

    # ── 下半场:create_task(先点火,等待里干活)──────────────
    print("--- 下半场:create_task(先点火,等待里干活)---")
    t2 = time.perf_counter()
    soup_task = asyncio.create_task(stew())   # ① 点火!汤立刻排班,返回 Task
    print(f"{stamp()} 点火拿到 {type(soup_task).__name__} 类型——带进度条的票")
    print(f"{stamp()} 汤现在干完了吗?{soup_task.done()}(刚上灶,还没好)")
    dish = await cut_veg()                    # ② 你去切菜——主流程一让位,汤就开工
    print(f"{stamp()} 切完菜,汤干完了吗?{soup_task.done()}(还炖着)")
    soup = await soup_task                    # ③ 回来收汤:等待的尾巴它自己补完
    print(f"{stamp()} 收汤:{soup}(task.result() 也能取:{soup_task.result()})")
    print(f"点火总耗时 {time.perf_counter() - t2:.1f} 秒"
          f" —— 切菜的 0.5 秒填进了炖汤的等待里 ✅")


if __name__ == "__main__":
    asyncio.run(main())
