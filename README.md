# Python 学习项目

全面的 Python 入门到进阶学习资料，**基于 [Python 官方教程](https://docs.python.org/3/tutorial/) 编写**，每一章都包含：

- 📘 理论讲解（精简）
- ✍️ 代码实例（可直接运行验证）
- 🧪 实践练习（带答案参考）
- 🔗 官方文档链接（深入阅读）

## 建议环境

- Python 3.10+（推荐 3.12），下载地址：https://www.python.org/downloads/
- 用终端运行示例：`python 文件名.py`

## 课程地图

| 章节 | 主题 | 状态 |
|------|------|------|
| ch01 | 起步：安装、Hello World、语法基础 | ✅ 已完成 |
| ch02 | 基础数据类型与运算符 | ✅ 已完成 |
| ch03 | 控制流：条件与循环 | ✅ 已完成 |
| ch04 | 函数：默认参数、*args/**kwargs、lambda、作用域 | ✅ 已完成 |
| ch05 | 数据结构：列表、元组、集合、字典、推导式 | ✅ 已完成 |
| ch06 | 输入输出与文件：print/input、with、json | ✅ 已完成 |
| ch07 | 错误与异常 | ✅ 已完成 |
<<<<<<< HEAD
| ch08 | 类与面向对象编程 | 🔥 收尾中 |
| ch09 | 模块与包 | 🔥 学员开做中 |
| ch10 | 标准库漫游 + 常用第三方库（pydantic/requests/httpx…） | 🔥 内容就绪 |
| ch11 | 同步与异步编程（asyncio，为 Agent 开发打基础） | 🔥 内容就绪 |
| ch12 | Agent 开发入门（Agent Loop、pydantic、pydantic-ai） | 🔥 内容就绪 |
=======
| ch08 | 类与面向对象编程 | ✅ 已完成 |
| ch09 | 模块与包 | 进行中 |
| ch10 | 标准库常用模块 | ⬜ |
| ch11 | 同步与异步编程（asyncio 入门，为 Agent 开发打基础） | ⬜ |
>>>>>>> 49097b94a473541d497f32ae4e7cce82e54f2896

> 学完基础章节后，ch11（异步）是 Agent 开发的直接前置；
> ch10 的 pydantic 和 ch12 的 pydantic-ai 是 Agent 开发主线。
> ch12 主要参照 [Vercel AI SDK](https://ai-sdk.dev/docs/introduction) 概念体系
> 与 [Pydantic AI 官方文档](https://pydantic.dev/docs/ai/)。

## 官方文档参考

- Python 官方教程（英文）: https://docs.python.org/3/tutorial/
- Python 官方教程（中文）: https://docs.python.org/zh-cn/3/tutorial/
- 库参考：https://docs.python.org/3/library/
- 语言参考：https://docs.python.org/3/reference/
- Pydantic AI（Agent 框架）：https://pydantic.dev/docs/ai/

---

## 如何使用本课程

1. **阅读理论**：每个章节有 `README.md`，包含核心知识点。
2. **运行示例**：`python ch01/01_hello.py`（示例脚本可直接运行）。
3. **做练习**：`exercises.py` 里留了需要你填空/补齐的函数，在**项目根目录**运行 `python -m ch01.test_exercises` 自动检查。
4. **对照答案**：做不出来再看 `answers.py`。

> 测试文件内部用了相对导入（`from . import exercises`），所以必须用 `python -m 包名.文件名` 的方式从项目根目录运行，不能直接 `python ch01/test_exercises.py`。
