"""Configuration for the writing assistant."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

# 获取API密钥和基础URL
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")

# 如果环境变量中未设置，则要求用户手动输入
if not openai_api_key:
    print("未找到OPENAI_API_KEY环境变量")
    openai_api_key = input("请输入OpenAI API密钥: ").strip()
    if not openai_api_key:
        raise ValueError("API密钥不能为空")

if not openai_base_url:
    print("未找到OPENAI_BASE_URL环境变量")
    use_custom_url = input("是否使用自定义API基础URL? (y/n): ").strip().lower()
    if use_custom_url == 'y':
        openai_base_url = input("请输入OpenAI API基础URL: ").strip()
        if not openai_base_url:
            print("未提供基础URL，将使用默认URL")
            openai_base_url = None

def load_chat_model() -> ChatOpenAI:
    """Load the chat model with configuration."""
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key, base_url=openai_base_url)