# 英语作文考试助手

这是一个使用LangGraph框架开发的英语作文辅助工具，专为参加英语作文考试的学生设计。它可以监听系统剪贴板内容，根据用户的指令进行不同类型的英语作文处理。

## 功能特点

- 监听系统剪贴板变化
- 多种作文处理模式：
  - **topic**: 根据给定话题生成作文范例
  - **rewrite**: 根据要求重写现有作文
  - **polish**: 润色和修正现有作文
- 系统托盘显示应用状态
- 快捷键切换暂停/恢复功能

## 安装与设置

1. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

2. 修改`.env.example`文件为`.env`，设置OpenAI API密钥：
   ```
    OPENAI_API_KEY=sk-xxx
    OPENAI_BASE_URL=your_openai_base_url
   ```

## 使用方法

1. 运行应用：
   ```
   python main.py
   ```

2. 复制英语作文文本到剪贴板，在末尾添加指令格式：`行为:提示词`
   
   例如：
   - `topic:环境保护` - 生成一篇关于环境保护的作文范例
   - `rewrite:使用更学术化的语言` - 用更学术化的语言重写剪贴板中的作文
   - `polish:修正语法错误` - 修正作文中的语法错误并润色

3. 应用将自动处理文本，并将结果写回剪贴板

4. 使用 `Command+Shift+F` 快捷键可以暂停/恢复应用

## 注意事项

- 此应用需要访问互联网以使用OpenAI服务
- 确保你的OpenAI API密钥有效且具有足够的配额
- 应用在系统托盘中显示状态：✅ 就绪 或 ⏳ 处理中 

## 示例

Extreme sports, such as sky diving and skiing are very dangerous and should be banned.

To what extent do you agree or disagree?
topic
