# boost/extras_ch10 — 标准库弹药房(加练包)

> 针对你在 ch10(标准库漫游)学习期间的 8 次追问出的定向加练。
> 做完在项目根目录跑:`python -m boost.extras_ch10.test_exercises`

## 题目 → 追问出处对照

| 题 | 知识点 | 你当时追问的问题 |
|---|---|---|
| 1 | `defaultdict(int)` 缺键工厂做计数 | "groups = defaultdict(list) 逐行解释一下" |
| 2 | 元组当 key + get 默认值 | "dict 对 key 和 value 的类型有没有限制?" |
| 3 | join 缝合(方向!) | "join 解释一下,我忘记了,他会拆分 list 吗" |
| 4 | split 拆解(join 反义词) | 同上——方向题成对练 |
| 5 | lambda 当 key | "复习一下 lambda" |
| 6 | seed 可复现 | "还是不太明白 seed 的作用和意义" |
| 7 | 1 == 1.0 == True 同键暗坑 | "int float 等数型能不能作为 dict 的 key" |
| 8 | assert 当关卡(综合) | "assert 是啥?" |

## 每题一句话提示(卡住再看,先自己想)

1. `counts[w] += 1`——第一次缺键自动造 0,再 +1;最后 `dict()` 转回
2. 推导式 + `place_map.get(p, "未知地")`——get 的第二参数是"查不到时给什么"
3. 缝线在前面调用:`"-".join(parts)`
4. `split(",")` 后每个碎片 `.strip()`——看清楚 `" go "` 两头有空格
5. `sorted(pairs, key=lambda p: p[1], reverse=True)`——lambda 说"按什么",reverse 管方向
6. seed → 抽 → 再 seed 同一个 → 再抽;`[第一把, 第二把]` 打包返回
7. 依次 `d[1.0]="b"`、`d[True]="c"`,返回 d——想想 len 是几
8. 三句 `assert 条件, "解释"`,最后 `return True`

## 交卷流程

```bash
python -m boost.extras_ch10.test_exercises   # 出分
```

8/8 后对照 `answers.py`,喊 Agent 审读;错题照旧记 `mistakes/`。
