"""test_exercises.py — 第八章练习自动检查。

运行(在项目根目录执行):python -m ch08.test_exercises
如果你通过了全部测试,会在终端看到 "恭喜!全部通过 🎉"。
"""

from . import exercises


def test_dog():
    d = exercises.Dog("旺财", 3)
    assert d.name == "旺财", f"name 应为 '旺财',实际 {d.name!r}"
    assert d.age == 3, f"age 应为 3,实际 {d.age!r}"
    assert d.bark() == "旺财: 汪汪!", f"bark() 应为 '旺财: 汪汪!',实际 {d.bark()!r}"

    d2 = exercises.Dog("小黑", 1)
    d.age = 4
    assert d2.age == 1, "改 d1 的 age 不应影响 d2(实例属性每对象一份)"


def test_counter():
    c = exercises.Counter()
    assert c.value() == 0, "默认 start=0,value 应为 0"
    c.bump()
    c.bump()
    c.bump()
    assert c.value() == 3, f"bump 三次后 value 应为 3,实际 {c.value()!r}"

    c2 = exercises.Counter(start=10)
    c2.bump()
    assert c2.value() == 11, f"start=10 bump 一次应为 11,实际 {c2.value()!r}"


def test_bank_account():
    acc = exercises.BankAccount("小明", 100)
    acc.deposit(50)
    assert acc.balance == 150, f"存 50 后余额应为 150,实际 {acc.balance!r}"
    acc.withdraw(30)
    assert acc.balance == 120, f"取 30 后余额应为 120,实际 {acc.balance!r}"

    try:
        acc.deposit(0)
    except ValueError as e:
        assert str(e) == "存款必须为正数: 0", (
            f"错误信息应为 '存款必须为正数: 0',实际 {e!r}"
        )
    else:
        raise AssertionError("deposit(0) 应该抛 ValueError 却没有抛")

    try:
        acc.withdraw(999)
    except ValueError as e:
        assert str(e) == "余额不足: 120 < 999", (
            f"错误信息应为 '余额不足: 120 < 999',实际 {e!r}"
        )
    else:
        raise AssertionError("超额 withdraw 应该抛 ValueError 却没有抛")


def test_point_repr():
    p = exercises.Point(3, 4)
    assert repr(p) == "Point(3, 4)", f"repr 应为 'Point(3, 4)',实际 {repr(p)!r}"
    p2 = exercises.Point("a", "b")
    assert repr(p2) == "Point('a', 'b')", (
        f"字符串值应带引号(!r 的作用),应为 \"Point('a', 'b')\",实际 {repr(p2)!r}"
    )


def test_car():
    assert exercises.Car.wheels == 4, "类属性 Car.wheels 应为 4"
    car = exercises.Car("比亚迪")
    assert car.describe() == "比亚迪 有 4 个轮子", (
        f"describe 应为 '比亚迪 有 4 个轮子',实际 {car.describe()!r}"
    )
    car2 = exercises.Car("特斯拉")
    assert car2.describe() == "特斯拉 有 4 个轮子", "每个实例的 describe 都应能用类属性"


def test_shapes():
    sq = exercises.Square(3)
    assert sq.area() == 9, f"边长 3 的正方形面积应为 9,实际 {sq.area()!r}"
    ci = exercises.Circle(2)
    assert abs(ci.area() - 12.56636) < 1e-4, (
        f"半径 2 的圆面积应约 12.5664,实际 {ci.area()!r}"
    )
    # 多态:父类的 describe 调用子类的 area
    assert sq.describe() == "面积是 9.00", (
        f"Square.describe 应为 '面积是 9.00',实际 {sq.describe()!r}"
    )
    assert ci.describe() == "面积是 12.57", (
        f"Circle.describe 应为 '面积是 12.57',实际 {ci.describe()!r}"
    )


def test_cat():
    c = exercises.Cat("咪咪", True)
    assert c.name == "咪咪", f"name 应由 super().__init__ 赋值,实际 {c.name!r}"
    assert c.indoor is True, f"indoor 应为 True,实际 {c.indoor!r}"
    assert c.speak() == "喵~", f"speak 应为 '喵~',实际 {c.speak()!r}"


def test_loudest():
    class Robot:
        def __init__(self, sound):
            self.sound = sound
        def speak(self):
            return self.sound

    assert exercises.loudest([]) == "", "空列表应返回 ''"
    assert exercises.loudest([Robot("汪"), Robot("汪汪汪"), Robot("喵")]) == "汪汪汪", (
        "应返回叫声最长的 speak() 结果"
    )
    assert exercises.loudest([Robot("嗷")]) == "嗷", "单元素直接返回它的叫声"

    class Rock:
        pass    # 没有 speak 方法

    try:
        exercises.loudest([Rock()])
    except AttributeError:
        pass    # 鸭子测试失败自然炸,算过
    else:
        raise AssertionError("没有 speak 方法的对象应让 AttributeError 自然炸出,却被吞了")


def test_safe_account():
    acc = exercises.SafeAccount("小明", 100)
    assert not hasattr(acc, "balance") or callable(getattr(acc, "balance")), (
        "SafeAccount 的 balance 应该是只读方法 balance(),不是公开属性"
    )
    assert acc.balance() == 100, f"balance() 应返回 100,实际 {acc.balance()!r}"
    assert acc._balance == 100, "余额应存在受保护属性 _balance 里"

    acc.deposit(50)
    assert acc.balance() == 150, f"存 50 后应为 150,实际 {acc.balance()!r}"
    acc.withdraw(30)
    assert acc.balance() == 120, f"取 30 后应为 120,实际 {acc.balance()!r}"

    try:
        acc.deposit(0)
    except ValueError as e:
        assert str(e) == "存款必须为正数: 0", (
            f"错误信息应为 '存款必须为正数: 0',实际 {e!r}"
        )
    else:
        raise AssertionError("deposit(0) 应该抛 ValueError 却没有抛")

    try:
        acc.withdraw(999)
    except ValueError as e:
        assert str(e) == "余额不足: 120 < 999", (
            f"错误信息应为 '余额不足: 120 < 999',实际 {e!r}"
        )
    else:
        raise AssertionError("超额 withdraw 应该抛 ValueError 却没有抛")


def run_all():
    tests = [
        test_dog,
        test_counter,
        test_bank_account,
        test_point_repr,
        test_car,
        test_shapes,
        test_cat,
        test_loudest,
        test_safe_account,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
        except NotImplementedError:
            print(f"⏳ {test.__name__}: 还没完成")
        except Exception as e:
            print(f"❌ {test.__name__}: 出错 {type(e).__name__}: {e}")

    print(f"\n通过 {passed}/{len(tests)}")
    if passed == len(tests):
        print("恭喜!全部通过 🎉")
    else:
        print("继续加油,还没完成全部 😊")


if __name__ == "__main__":
    run_all()
