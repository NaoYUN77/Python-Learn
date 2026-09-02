"""04_dicts.py — 字典：增删改查、get、遍历三件套。

运行：python ch05/04_dicts.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries
"""

# 1. 基本操作：键 → 值
person = {"name": "小明", "age": 18}

print(person["age"])              # 18（取值；键不存在 → KeyError）
person["city"] = "北京"            # 键不存在 = 新增
person["age"] = 19                # 键已存在 = 修改
print(person)                     # {'name': '小明', 'age': 19, 'city': '北京'}

del person["city"]                # 删除
print("name" in person)           # True ⚠️ in 查的是键，不是值！
print("小明" in person)           # False（"小明"是值）

# 2. 安全取值：get（不存在不报错）
# print(person["phone"])          # ❌ KeyError
print(person.get("phone"))             # None
print(person.get("phone", "未填写"))   # 带默认值

# 3. 遍历三件套
scores = {"数学": 90, "语文": 85, "英语": 92}

for k in scores.keys():           # 只要键
    print(k, end=" ")             # 数学 语文 英语
print()

for v in scores.values():         # 只要值
    print(v, end=" ")             # 90 85 92
print()

for k, v in scores.items():       # 键值成对（ch04 练习 5 用过）
    print(f"{k}: {v}", end="; ")  # 数学: 90; 语文: 85; 英语: 92;
print()

# 4. 计数模式：字典当累加器（超经典结构）
text = "abracadabra"
counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1    # 没见过默认 0，见一次加 1
print(counts)                     # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}

# 5. 键必须是不可变对象：字符串/数字/元组可以，列表不行
d = {(0, 0): "原点"}              # ✅ 元组做键
print(d[(0, 0)])                  # 原点
# d = {[0, 0]: "原点"}            # ❌ TypeError: unhashable type: 'list'

# 6. Agent 视角：工具注册表就是字典（函数当值）
def search_tool(query):
    return f"搜索 {query}"

def calc_tool(expr):
    return f"计算 {expr}"

tools = {"search": search_tool, "calc": calc_tool}
print(tools["search"]("Python"))  # 搜索 Python —— 按名字取出函数并调用
