"""02_params.py — 默认参数、关键字参数、可变默认值的坑。

运行：python ch04/02_params.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#default-argument-values
"""

# 1. 默认参数：调用时可以不传
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")                        # 你好，小明！（用默认值）
greet("小明", "早上好")              # 早上好，小明！（按位置覆盖）

# 2. 关键字参数：按名字传，顺序随意
greet(greeting="晚安", name="小红")  # 晚安，小红！

# 3. ⚠️ 可变默认值的坑：默认值只在 def 时创建一次，列表被所有调用共享
def append_bug(item, items=[]):      # ❌ 经典陷阱
    items.append(item)
    return items

print(append_bug("a"))               # ['a']
print(append_bug("b"))               # ['a', 'b']  ← b 怎么跟 a 在一起？！

# ✅ 惯用写法：用 None 占位，函数体里建新列表
def append_ok(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(append_ok("a"))                # ['a']
print(append_ok("b"))                # ['b']（互不干扰）

# 4. 裸 * 之后的参数只能按关键字传（很多标准库这么设计）
def connect(host, *, port, timeout=5):
    print(f"{host}:{port} (timeout={timeout})")

connect("localhost", port=8080)      # localhost:8080 (timeout=5)
# connect("localhost", 8080)         # ❌ TypeError：port 只能用关键字传

# 5. *args / **kwargs 初步印象（下一节细讲）
def summary(*args, **kwargs):
    print("位置参数:", args)         # 元组
    print("关键字参数:", kwargs)     # 字典

summary(1, 2, mode="fast")           # 位置参数: (1, 2)  关键字参数: {'mode': 'fast'}
