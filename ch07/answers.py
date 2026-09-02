"""answers.py — 第七章练习参考答案。

先自己尝试做 exercises.py，实在做不出来再看这里。
"""

import json


# 练习 1
def parse_int(s):
    try:
        return int(s)
    except ValueError:              # 值转不动（"abc"）
        return None
    except TypeError:               # 类型根本不对（None）——和 ValueError 是两种信号
        return None


# 练习 2
def get_port(config, default):
    try:
        return config["port"]       # EAFP：直接取
    except KeyError:                # 炸了再接，天然原子
        return default


# 练习 3
def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):   # 元组：一个 except 接两种
        return None


# 练习 4
def set_score(score):
    if score < 0 or score > 100:
        raise ValueError(f"分数必须在 0~100: {score}")   # 大声失败，逼调用方面对
    return score


# 练习 5
def safe_divide(a, b):
    steps = []
    try:
        steps.append("try")
        result = a / b
    except ZeroDivisionError:
        steps.append("except")
    else:
        steps.append("else")        # 只有 try 没炸才走这
    finally:
        steps.append("finally")     # 永远走这
        return ",".join(steps)      # 注意：finally 的 return 会"截胡"别的 return


# 练习 6
def describe_error(func):
    try:
        func()
    except ValueError:
        return "value"
    except TypeError:
        return "type"
    except KeyError:
        return "key"
    raise                            # 没被认领的异常：裸 raise 原样转发（不吞）


# 练习 7
def write_log(path, text):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return "written"
    except OSError:                  # open/write 失败的家族型号
        return "failed"
    finally:
        print("清理完成")             # 无论成败都清理（finally 里只做清理，不 return）


# 练习 8
def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise                       # 缺文件：原样转发
    except json.JSONDecodeError as e:
        raise ValueError("配置文件损坏") from e    # 换型号但保留原始线索


if __name__ == "__main__":
    print(parse_int("42"), parse_int("abc"), parse_int(None))
    print(get_port({"port": 8080}, 80), get_port({}, 80))

    import os
    import tempfile
    tmp = tempfile.gettempdir()

    good = os.path.join(tmp, "ch07_ans_good.json")
    with open(good, "w", encoding="utf-8") as f:
        f.write('{"a": 1}')
    print(load_json(good), load_json("缺失的.json"))

    print(set_score(88))
    try:
        set_score(101)
    except ValueError as e:
        print("捕获:", e)

    print(safe_divide(10, 2))
    print(safe_divide(1, 0))

    print(describe_error(lambda: int("x")))
    print(describe_error(lambda: "a" + 1))
    print(describe_error(lambda: 1))

    log = os.path.join(tmp, "ch07_ans_log.txt")
    print(write_log(log, "hello"), write_log(tmp, "x"))    # 第二个会先 print 清理完成

    cfg = os.path.join(tmp, "ch07_ans_cfg.json")
    with open(cfg, "w", encoding="utf-8") as f:
        f.write("{坏的")
    try:
        load_config(cfg)
    except ValueError as e:
        print(f"{e}（原始线索: {e.__cause__.__class__.__name__}）")
