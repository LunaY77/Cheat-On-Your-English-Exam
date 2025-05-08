"""剪贴板操作模块"""

import hashlib
from typing import Dict, Optional

import pyperclip

def get_clipboard() -> str:
    """获取剪贴板内容"""
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"获取剪贴板内容失败: {str(e)}")
        return ""

def set_clipboard(content: str) -> bool:
    """设置剪贴板内容"""
    try:
        pyperclip.copy(content)
        return True
    except Exception as e:
        print(f"设置剪贴板内容失败: {str(e)}")
        return False

def hash_content(content: str) -> str:
    """计算内容的哈希值"""
    return hashlib.md5(content.encode()).hexdigest()

def parse_clipboard(content: str) -> Dict[str, str]:
    """解析剪贴板内容，提取行为类型和提示"""
    content_lines = content.strip().split('\n')
    if not content_lines:
        return {
            "content": "",
            "behavior": "topic",
        }
    
    last_line = content_lines[-1].strip().lower()
    prompt = '\n'.join(content_lines[:-1]).strip()
    
    if last_line == "topic":
        return {
            "content": prompt,
            "behavior": "topic"
        }
    elif last_line == "rewrite":
        return {
            "content": prompt,
            "behavior": "rewrite"
        }
    elif last_line == "generate":
        return {
            "content": prompt,
            "behavior": "generate"
        }
    else:
        return {
            "content": prompt,
            "behavior": "topic"
        }