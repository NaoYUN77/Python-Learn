"""exercises.py — 第七章实践练习。

请完成下面的每个函数，然后运行 test_exercises.py 检查是否正确。

题目围绕官方教程第 8 章（错误与异常）：
按类型接异常、else/finally、raise 主动抛、EAFP、异常转 None。
做完可以对照 answers.py 看参考代码。

⚠️ except 后面必须写具体类型（裸 except 扣分）。
"""

import json
from json.decoder import JSONDecodeError
from shutil import RegistryError

# 练习 1：安全转换（复习 ch06 的 parse_int，这次自己写全）
# parse_int(s)：输入 "42" → 42；输入 "abc" → 返回 None（不崩溃）
# 输入 None → 也返回 None（提示：int(None) 抛的是 TypeError，不是 ValueError）
# 提示：一个 try 配两个 except，各接各的类型
def parse_int(s):
    # TODO: try 里 return int(s)；except ValueError 和 except TypeError 都 return None
    try :
        return int(s) #危险语句
    except ValueError:
        return None
    except TypeError:
        return None


# 练习 2：安全取键（EAFP 风格）
# get_port(config, default)：从字典取 "port"，键不存在就返回 default
# get_port({"port": 8080}, 80) → 8080；get_port({}, 80) → 80
# 提示：try 直接 config["port"]，except 接 KeyError 返回 default——不许用 in 检查（那是 LBYL）
def get_port(config, default):
    # TODO: EAFP 三行：try 取 / except KeyError 返回 default
    try:
        return config['port']
    except KeyError:
        return default
        

# 练习 3：安全读 json 文件（组合 ch06）
# load_json(path)：文件存在且合法 → 返回读出的对象
# 文件不存在 → 返回 None；文件内容是坏 json → 也返回 None
# 提示：接 FileNotFoundError 和 json.JSONDecodeError（可以一个 except 接两种，元组写法）
def load_json(path):
    # TODO: with + json.load，一个 except 接两种错误类型
    try:
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# 练习 4：按参数抛异常（raise）
# set_score(score)：0~100 返回 score；负数或超过 100 抛 ValueError
# 错误信息必须是 f"分数必须在 0~100: {score}"
# 提示：一个 if 判断越界（score < 0 or score > 100），raise ValueError(f"...")
def set_score(score):
    # TODO: if 越界就 raise，否则 return score
    if score < 0 or score > 100 :
        raise ValueError(f"分数必须在 0~100: {score}")
    else:
        return score


# 练习 5：try/else/finally 三件套（体会各块执行时机）
# safe_divide(a, b) 返回一个字符串，记录执行了哪些块：
#   a/b 能算 → 返回 "try,else,finally"（try 没炸 → else 跑）
#   b 是 0   → 返回 "try,except,finally"（炸了 → except 跑，else 不跑）
#   finally 永远跑
# 提示：用一个列表 steps = [] 当记录仪，每进一个块就 append 块名，
#       最后 ",".join(steps) 返回——join 的分隔符照着目标输出逐字符写（ch04 前科）
def safe_divide(a, b):
    # TODO: steps = [] 起步；try/except/else 里各 append 一次；
    #       finally 里 append "finally" 并 return ",".join(steps)
    steps = []
    try:
        steps.append("try")
        result = a / b 
    except ZeroDivisionError:
        steps.append("except")
    else:
        steps.append("else")
    finally:
        steps.append("finally")
        return ",".join(steps)


# 练习 6：区分错误类型（多 except 分支）
# describe_error(func)：调用 func()，不炸返回 "ok"；
#   炸 ValueError → 返回 "value"；炸 TypeError → 返回 "type"；炸 KeyError → 返回 "key"
#   其他异常 → 裸 raise 原样转发（提示：except 末尾写一个单独的 raise）
# 提示：三个 except 分支从上往下各 return 一个词；最后单独一行 raise 转发没认领的
def describe_error(func):
    # TODO: try 调用 func() return "ok"；三个 except 各 return；其他异常转发
    try: 
        func()
        return "ok"
    except ValueError:
        return "value"
    except TypeError:
        return "type"
    except KeyError:
        return "key"
    except:
        raise


# 练习 7：清理资源（finally 的本职工况）
# class 样板的函数版：write_log(path, text) 打开文件写一行并 close——
# 但要求【无论写没写成功，都要执行 print("清理完成")】
# 写成功返回 "written"；open 就失败（FileNotFoundError 等）返回 "failed"
# 提示：try 包 open+write，except 接 OSError（open 失败的家族型号）返回 "failed"，
#       finally 里 print——注意：finally 里只做清理，不要 return
def write_log(path, text):
    # TODO: try: open+write+close 后 return "written"
    #       except OSError: return "failed"
    #       finally: print("清理完成")
    try:
        f = open(path ,"w" , encoding='utf-8')
        f.write(text)
        f.close()
        return "written"
    except OSError:
        return "failed"
    finally:
        print("清理完成")

# 练习 8：异常链（选做·挑战）
# load_config(path)：读 json 文件，文件缺失时抛 FileNotFoundError 原样转发；
#   json 解析失败时抛 ValueError("配置文件损坏") from e（保留原始异常线索）
# 提示：两个 except 分支——FileNotFoundError 里裸 raise；
#       json.JSONDecodeError as e 里 raise ValueError("配置文件损坏") from e
def load_config(path):
    # TODO: with + json.load；两个 except 分支按要求处理
    try:
        with open(path , 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise ValueError("配置文件损坏") from e
        
