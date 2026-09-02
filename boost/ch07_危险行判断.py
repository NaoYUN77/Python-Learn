"""ch07_危险行判断.py — 什么算"危险行"?try 该包哪几行?该在哪儿 return?

运行：python boost/ch07_危险行判断.py
来源：ch07 学习中"外面/里面怎么判断"的追问,沉淀成单主题专题。

核心一句话：
  危险行 = 失败时算"世界的锅"的行(文件/用户/网络/调用方传参/包函数的内部规则),
  不是"来自别的包"的行——判断标准是【这行执行时的前提有没有人向你保证过】。
"""

# ══════════════════════════════════════════
# 第一部分:判断标准 —— 谁的锅?
# ══════════════════════════════════════════

# 1. 判断标准不是"在哪个包",而是"这行失败时,是谁的锅":
#    - 世界的锅(环境不配合)  → 危险行 → 用 try/except 防御
#    - 你的锅(代码写错了)    → bug    → 改代码,except 只会掩盖问题

# 2. "外面"的完整清单(行为不受你代码保证的一切):
#    用户输入 / 文件系统 / 网络 / 调用方传进来的参数 / 包函数的内部规则

# 3. 标准库的函数也是"外面"——math.sqrt(-1) 抛 ValueError,
#    和 open("不存在.txt") 抛 FileNotFoundError 是同一性质:
#    你写不出"保证不炸"的调用,只能"调用 + 接住"或"先校验参数"。

# 4. "有没有人保证过"决定性质——同一个操作,来源不同,危险度不同:
def parse_age(text):          # 危险:text 是参数,没人保证它是数字
    return int(text)

def circle_area(radius):
    # 安全:radius 乘方不会因为"世界不配合"而炸
    # (除非 radius 本身就是坏的——那锅在调用方,让它炸出来喊人)
    import math
    return math.pi * radius ** 2

# 5. 包文档的 Raises 段落 = 作者亲口给你的"危险行清单":
#    json.loads 文档写着 Raises JSONDecodeError → 它是危险行
#    list.append 文档从不写 Raises             → 它几乎永远安全
#    读文档的 Raises 段,是工程动作,不是废话文学。

# ══════════════════════════════════════════
# 第二部分:入口最危险,越往里越安全
# ══════════════════════════════════════════

def demo(data, path):
    # 危险区(入口):参数刚进来、文件刚打开——防御的主战场
    #   data.split("\n")   ← data 若是 None → AttributeError
    #   lines[0]           ← lines 若为空  → IndexError
    #   open(path, ...)    ← 文件系统说了算
    # 安全区(深处):前面已加工出的中间值
    #   len(content) * 2   ← content 刚拿到,str 的 len 必然成功
    #
    # 规律:越靠近函数入口越危险,越往深处越安全。
    lines = data.split("\n")                # 危险
    with open(path, encoding="utf-8") as f: # 危险
        content = f.read()
    return len(content) * 2                 # 安全

# ══════════════════════════════════════════
# 第三部分:该不该在危险行 return?
# ══════════════════════════════════════════

# 6. 三种情形(对应 ch07 exercises 的真实题目):

# 情形 A:危险行成功 = 使命完成 → try 里直接 return(成功即交卷)
def parse_int(s):
    try:
        return int(s)            # 成功直接交卷,合法且常见
    except ValueError:
        return None
    except TypeError:
        return None

# 情形 B:成功后还有收尾活 → 把活放 else,或放 try 外面
def read_config(path):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        return {}
    else:
        # else = try 没炸才执行:成功路径从 try 里解放出来
        return {"raw": f.read()}

# 情形 C:finally 永远只做清理,不 return ——
#         finally 的 return 会【截胡】try/except 里的所有 return
def sneaky():
    try:
        return "try 的返回值"     # 永远轮不到展示
    finally:
        return "finally 截胡了"   # 实际返回这个!真实项目严禁这么写

# ══════════════════════════════════════════
# 第四部分:快问快答自测(遮住下面的答案先自己判断)
# ══════════════════════════════════════════

def quiz():
    results = []
    # Q1: int(user_input) —— user_input 来自 input()
    results.append(("Q1 int(user_input)", "危险", "用户输什么你管不着"))
    # Q2: [1,2,3][5] —— 字面量列表,下标是你自己写的
    results.append(("Q2 [1,2,3][5]", "bug", "字面量越界是你算错下标,改代码"))
    # Q3: requests.get(url) —— 第三方网络库
    results.append(("Q3 requests.get", "危险", "网络状态你管不着"))
    # Q4: d2 = {}; d2["k"] —— 你自己刚建的空字典
    results.append(("Q4 d2['k']", "bug", "空字典取键必炸,这是逻辑错误"))
    # Q5: json.load(f) —— f 是用户给的路径打开的
    results.append(("Q5 json.load(f)", "危险", "文件内容你管不着"))
    # Q6: "abc".upper() —— 字面量字符串调方法
    results.append(("Q6 'abc'.upper()", "安全", "str.upper 不会失败"))
    # Q7: 调用方传来的列表,取 lst[0]
    results.append(("Q7 lst[0]", "危险", "调用方传空列表就炸(IndexError)"))
    return results


if __name__ == "__main__":
    print("═══ 情形 C 实证:finally 的 return 截胡 ═══")
    print("sneaky() 返回:", sneaky())          # finally 截胡了 ← 不是 try 的那个!

    print("\n═══ 入口危险区实证 ═══")
    try:
        demo(None, "任意路径")               # data 是 None
    except AttributeError as e:
        print("data=None 炸在入口:", e)

    print("\n═══ 自测题答案 ═══")
    for name, verdict, why in quiz():
        print(f"{name}: {verdict} —— {why}")

    print("\n口诀:世界的锅用 except,你的锅改代码;入口最危险,越往里越安全;")
    print("      危险行成功即交卷可 return;成功后还有活放 else;finally 只清理不 return。")
