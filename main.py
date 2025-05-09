"""主程序入口"""

import asyncio
import signal
import sys
from typing import Dict, Any

from tools.clipboard import get_clipboard, hash_content, parse_clipboard, set_clipboard
from tools.graph import graph

# 全局变量
running = True

def signal_handler(sig, frame):
    """处理退出信号"""
    global running
    print("\n正在退出...")
    running = False

async def process_content(content: str) -> Dict[str, Any]:
    """处理剪贴板内容"""
    # 解析剪贴板内容
    parsed = parse_clipboard(content)
    
    # 执行图
    result = await graph.ainvoke({
        "content": parsed["content"],
        "behavior": parsed["behavior"]
    })
    
    return result

async def main():
    """主函数"""
    # 设置信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 初始化变量
    last_hash = hash_content(get_clipboard())
    
    print("正在监听剪贴板变化...")
    print("使用 Ctrl+C 退出程序")
    print("行为指令：")
    print("- topic - 根据话题生成作文")
    print("- rewrite - 重写作文")
    print("- generate - 生成新内容")
    print("- cite - 改写引用并添加哈佛引用格式")
    print("- conclude - 生成结尾段落")
    print("- full - 生成完整的作文")
    
    try:
        while running:
            content = get_clipboard()
            current_hash = hash_content(content)
            
            if content.strip() and current_hash != last_hash:
                print("\n[剪贴板已更新]")
                print(content)
                
                try:
                    # 处理内容
                    result = await process_content(content)
                    
                    # 更新剪贴板
                    if result.get("response"):
                        if set_clipboard(result["response"]):
                            last_hash = hash_content(result["response"])
                            print("\n[生成的响应]")
                            print(result["response"])
                        else:
                            print("\n[错误] 无法更新剪贴板")
                    
                    print("\n[处理完成]")
                    
                except Exception as e:
                    print(f"\n[错误] {str(e)}")
            
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("\n程序被取消")
    finally:
        print("程序已退出")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")
        sys.exit(1) 