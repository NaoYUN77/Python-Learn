"""02_try_except.py — try/except 完整语法：多类型、else、finally、只包危险行。

运行：python ch07/02_try_except.py
参考官方文档：https://docs.python.org/zh-cn/3/tutorial/errors.html#handling-exceptions
"""

# ══════════════════════════════════════════
# 第一部分：except 的三种写法
# ══════════════════════════════════════════

# 1. 一个 try 配多个 except：从上往下匹配，命中一个就跳出去
def to_int(s):
    try:
        return int(s)
    except ValueError:               # 先问：是值的问题吗？
        return None
    except TypeError:                # 再问：是类型的问题吗？（int(None) 会走到这）
        return None

print(to_int("42"), to_int("abc"), to_int(None))   # 42 None None

# 2. 一个 except 接多种类型：括号元组
def head(seq):
    try:
        return seq[0]
    except (IndexError, TypeError) as e:    # 空列表越界 / 对 int 取下标，一起接
        print(f"  拿不到第一个元素（{type(e).__name__}），返回 None")
        return None

print(head([]), head(42), head("ok"))        # None None ok（第一行先打印说明）

# 3. 铁律演示：裸 except 是灾难（认识它，别用它）
def bad(x):
    try:
        return 100 // x
    except:                          # ❌ 裸 except：什么信号都吞，连 Ctrl+C 都吞
        return None
# 反面教材：x=0 时返回 None 尚可理解，但任何别的 bug（比如变量名打错）也被
# 悄悄吞成 None——排查时你根本不知道程序哪里病了。永远写具体类型。


# ══════════════════════════════════════════
# 第二部分：try 只包危险行
# ══════════════════════════════════════════

# 4. ❌ 反面：把整个函数裹进 try——炸了不知道是哪行
def messy_bad(text):
    try:
        path = text.strip() + ".json"
        with open(path, encoding="utf-8") as f:   # 危险的其实只有这一行
            data = json.load(f)
        return data["items"][0]                    # 和这一行
    except Exception:
        return None        # strip 炸？open 炸？load 炸？取键炸？全是谜

# ✅ 正面：危险行单独一小段 try
import json

def messy_good(text):
    path = text.strip() + ".json"          # 不危险的行放外面
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  读不了 {path}: {type(e).__name__}")
        return None
    return data.get("items", [None])[0]    # 成功路径不裹 try

print(messy_good("不存在"))                 # 读不了 不存在.json: FileNotFoundError


# ══════════════════════════════════════════
# 第三部分：else 与 finally
# ══════════════════════════════════════════

# 5. else：try 没炸才执行——把"成功路径"从 try 里解放出来
def read_config(path):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        print("  文件不存在，用默认配置")
        return {}
    else:
        # 走到这里说明 open 成功了
        print("  打开成功，读取内容")
        text = f.read()
        f.close()
        return json.loads(text)

print(read_config("ch07/缺失.json"))        # 文件不存在分支

# 6. finally：无论炸不炸都执行——清理资源的铁底
def demo_finally(n):
    try:
        print(f"  try 开始，准备算 100/{n}")
        result = 100 / n
    except ZeroDivisionError:
        print("  except：除零了")
        return "出错"
    finally:
        print("  finally：无论如何都跑（收尾/清理放这）")
    return result

print(demo_finally(4))      # try 正常 → finally 照跑 → return 25.0
print(demo_finally(0))      # try 炸 → except 接住 → finally 照跑 → return "出错"

# 7. finally 在 return 之后也照样执行（甚至能覆盖 return 值——见识一下即可）
def sneaky():
    try:
        return "try 的返回值"
    finally:
        print("  finally 在 return 之后、函数真正退出之前执行")
print(sneaky())

# 8. with 的真相：它就是 try/finally 的语法糖
with open("ch07/demo.txt", "w", encoding="utf-8") as f:
    f.write("hello")
# 大致等价于：
f = open("ch07/demo.txt", "w", encoding="utf-8")
try:
    f.write("hello")
finally:
    f.close()               # ← ch06 说"异常也保证关闭"，靠的就是这个结构
print("with 块结束，f.closed =", f.closed)   # True


# ══════════════════════════════════════════
# 第四部分：except 命中后，流程去哪
# ══════════════════════════════════════════

# 9. 命中 except 后，try 块里【后面的行不再执行】
try:
    print("  第一行")
    int("炸")                 # 这行抛出
    print("  这行永远不会执行")  # ← 被跳过
except ValueError:
    print("  except 接住")
print("  继续 try/except 之后的正常生活")
