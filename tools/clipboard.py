"""剪贴板操作模块"""

import hashlib
import platform
from typing import Dict, Optional

if platform.system() == "Darwin":  # macOS
    import pyperclip
elif platform.system() == "Windows":  # Windows
    import win32clipboard
    import win32con
else:
    raise NotImplementedError(f"不支持的操作系统: {platform.system()}")

def get_clipboard() -> str:
    """获取剪贴板内容"""
    try:
        if platform.system() == "Darwin":
            return pyperclip.paste()
        elif platform.system() == "Windows":
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                else:
                    data = ""
            finally:
                win32clipboard.CloseClipboard()
            return data
    except Exception as e:
        print(f"获取剪贴板内容失败: {str(e)}")
        return ""

def set_clipboard(content: str) -> bool:
    """设置剪贴板内容"""
    try:
        if platform.system() == "Darwin":
            pyperclip.copy(content)
        elif platform.system() == "Windows":
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(content, win32con.CF_UNICODETEXT)
            finally:
                win32clipboard.CloseClipboard()
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
    elif last_line == "cite":
        return {
            "content": prompt,
            "behavior": "cite"
        }
    elif last_line == "conclude":
        return {
            "content": prompt,
            "behavior": "conclude"
        }
    else:
        return {
            "content": prompt,
            "behavior": "topic"
        }