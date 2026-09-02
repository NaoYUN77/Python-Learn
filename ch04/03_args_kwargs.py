"""03_args_kwargs.py — *args、**kwargs 与调用时的解包。

运行：python ch04/03_args_kwargs.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#arbitrary-argument-lists
"""

# 1. *args：收走多余的"位置参数"，打包成元组（名字随意，* 才是关键）
def total(*args):
    print(args, type(args).__name__)
    s = 0
    for n in args:
        s += n
    return s

print(total(1, 2, 3))                # (1, 2, 3) tuple → 6
print(total())                       # () tuple → 0

# 2. **kwargs：收走多余的"关键字参数"，打包成字典
def show_options(**kwargs):
    print(kwargs)

show_options(color="红", size="大")  # {'color': '红', 'size': '大'}

# 3. 混搭：普通参数 → *args → 关键字参数 → **kwargs（定义时的固定顺序）
def report(title, *tags, sort=False, **fields):
    print(f"标题: {title}")
    print(f"标签: {tags}")
    print(f"排序: {sort}")
    print(f"其他: {fields}")

report("日报", "工作", "学习", sort=True, author="小明")
# 标题: 日报
# 标签: ('工作', '学习')
# 排序: True
# 其他: {'author': '小明'}

# 4. 调用时的 * / ** 是"解包"：把序列/字典拆开成一个个参数
def area(width, height):
    return width * height

size = [3, 4]
print(area(*size))                   # 等价于 area(3, 4) → 12

opts = {"width": 5, "height": 6}
print(area(**opts))                  # 等价于 area(width=5, height=6) → 30

# 5. 参数转发：Agent 框架里"把参数原样转给工具函数"的经典模式
def logged_call(func, *args, **kwargs):
    print(f"调用 {func.__name__}，参数 {args} {kwargs}")
    return func(*args, **kwargs)     # 原样转发

result = logged_call(area, 3, height=4)
print(result)                        # 12
