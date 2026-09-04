"""02 __name__ 的两副面孔。

直接跑:  python ch09/02_name_main.py   → __name__ 是 "__main__"(我是主角)
被导入:  __name__ 是模块名(我是配角)——test_exercises 导入 exercises 时,
        exercises 的 __name__ 就是 "ch09.exercises",练习 4 让你亲手 return 它
"""

print(f"这个文件现在的 __name__ = {__name__!r}")

if __name__ == "__main__":
    print("→ 我是被人直接运行的(主角模式)")
    print("  原理:python 直接跑时,Python 把这个文件当成名叫 '__main__' 的")
    print("  临时模块执行——所以它看到的自己是 '__main__'")
    print()
    print("  跟踪表:")
    print("  | 打开方式             | __name__ 的值 | 守卫里的代码 |")
    print("  |----------------------|---------------|--------------|")
    print("  | python xxx.py 直接跑 | '__main__'    | 执行         |")
    print("  | 被别人 import        | 模块名        | 跳过         |")
    print()
    print("  对比实验:")
    print("    python ch09/tiny_mod.py            ← 守卫里的代码执行(主角)")
    print("    在 01_import_basics.py 里 import   ← 守卫不执行(配角)")
else:
    # 直接跑永远走不到这里;只有被 import 时才进 else
    print("→ 我是被别的模块 import 进来的(配角模式)")
