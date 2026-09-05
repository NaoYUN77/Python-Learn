import asyncio
import time 


# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     return f"{what} - {delay}"

# async def print_a():
#     await asyncio.sleep(5)
#     print("a")
# async def print_b():
#     await asyncio.sleep(1)
#     print("b")


# async def main():  #coroutine  function
#     task1 = asyncio.create_task(print_a()) #将coroutine object注册到事件循环中
#     task2 = asyncio.create_task(print_b())
#     await task1
#     await task2

#     print("done")

# asyncio.run(main())
# 

# async def download(name,delya):
#     print(f"{name}开始下载")
#     await asyncio.sleep(delya)
#     print(f"{name}下载完成")

# async def main():
#     time_start = time.time()

#     task1 = asyncio.create_task(download("A", 5))
#     task2 = asyncio.create_task(download("B", 2))
#     task3 = asyncio.create_task(download("C", 3))
#     await task1
#     await task2
#     await task3
    
#     time_end = time.time()
#     print("全部下载完成")
#     print(f"总耗时：{time_end - time_start}")

async def request_api(name,delay):
    print(f"开始请求: {name}")
    await asyncio.sleep(delay) #模拟网络io
    print(f"请求完成: {name}")

async def main():
    request_start = time.time()
    task1 = asyncio.create_task(request_api("用户信息", 5))
    task2 = asyncio.create_task(request_api("文章列表", 2))
    task3 = asyncio.create_task(request_api("推荐内容", 3))
    await task1
    await task2
    await task3

    print("全部请求完成")
    request_end = time.time()
    print(f"总耗时：{request_end - request_start}")

asyncio.run(main())
