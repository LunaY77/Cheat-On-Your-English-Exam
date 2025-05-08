# 英语写作助手

这是一个简单易用的英语写作辅助工具，可以帮助你快速生成、改写和润色英语文章。它会在后台监听你的剪贴板，当你复制文本并添加特定指令时，它会自动处理并返回结果。

## 功能特点

- 🎯 智能写作：根据话题生成作文
- ✍️ 文章改写：用不同风格重写文章
- 📝 内容扩展：在现有文章基础上添加新内容
- 📚 引用处理：自动改写引用并添加哈佛引用格式
- 🖥️ 系统托盘：在菜单栏显示运行状态
- ⏯️ 暂停/恢复：随时控制程序运行

## 安装步骤


### 1. 安装程序

1. 下载本项目到你的电脑
2. 打开终端（macOS）或命令提示符（Windows）
3. 进入项目目录：
   ```bash
   cd 项目所在路径
   ```
4. 安装所需依赖：
    如果你会用 venv/conda 这种虚拟环境工具，建议你创建一个虚拟环境来安装依赖，不会就直接 pip install 吧()

   ```bash
   pip install -r requirements.txt
   ```

### 2. 配置 OpenAI API

我这边使用的 API 中转平台是 [OhMyGPT](https://next.ohmygpt.com/apis)

请你自行创建一个账号并获取 API 密钥

当你获取到 API 密钥后，创建一个 `.env` 文件(仿照`.env.example`格式)，并在其中添加以下内容：

```
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://c-z0-api-01.hash070.com/v1
```

如果你跟我一样使用的是 OhMyGPT 的API，请直接使用我写的 BASE_URL，不要修改，你只需要修改 API_KEY

## 使用方法

### 启动程序

1. 打开终端（macOS）或命令提示符（Windows）
2. 进入项目目录
3. 运行程序：
   ```bash
   python main.py
   ```
4. 程序启动后，你会在菜单栏（macOS）或系统托盘（Windows）看到 ✍️ 图标

### 使用指令

复制文本到剪贴板，在最后一行添加以下指令之一：

- `topic` - 生成一篇关于该话题的作文
- `rewrite` - 重写文章，改进表达
- `generate` - 在文章基础上添加新内容
- `cite` - 改写引用并添加哈佛引用格式

### 示例

1. 生成作文：
   ```
   sleep and its connection to cognitive function as we age 
   topic
   ```

2. 改写文章：
   ```
   As we grow older, many of us experience changes in our sleep patterns. We may wake up more frequently at night, feel less rested, or even suffer from memory lapses during the day. But is this just a natural part of aging, or is there a deeper connection between sleep quality and cognitive decline? Drawing from the findings in the academic paper titled Age-related Changes in the Cognitive Function of Sleep by Edward F. Pace-Schott and Rebecca M.C. Spencer, I will delve into the ways aging impacts both sleep architecture and cognition—and what this means for our overall brain health.
   rewrite
   ```

3. 生成新内容：
   ```
   The quick brown fox jumps over the lazy dog.
   generate
   ```

4. 添加引用：
   ```
    The quick brown fox jumps over the lazy dog.
    cite
   ```

5. 生成结尾总结
    ```
     As we grow older, many of us experience changes in our sleep patterns. We may wake up more frequently at night, feel less rested, or even suffer from memory lapses during the day. But is this just a natural part of aging, or is there a deeper connection between sleep quality and cognitive decline? Drawing from the findings in the academic paper titled Age-related Changes in the Cognitive Function of Sleep by Edward F. Pace-Schott and Rebecca M.C. Spencer, I will delve into the ways aging impacts both sleep architecture and cognition—and what this means for our overall brain health.
     conclude
    ```