"""UI模块，实现状态栏图标和快捷键功能"""

import rumps
from typing import Callable, Tuple

class StatusBarApp(rumps.App):
    """状态栏应用"""
    
    def __init__(self):
        """初始化状态栏应用"""
        super().__init__("✍️", "写作助手")
        self.menu = [
            rumps.MenuItem("暂停/恢复", callback=self.toggle_pause),
            rumps.MenuItem("退出", callback=self.quit_app)
        ]
        self.is_paused = False
        
    def toggle_pause(self, _):
        """切换暂停/恢复状态"""
        self.is_paused = not self.is_paused
        self.title = "⏸️" if self.is_paused else "✍️"
        
    def quit_app(self, _):
        """退出应用"""
        rumps.quit_application()

def setup_ui() -> Tuple[StatusBarApp, rumps.App]:
    """设置UI"""
    app = StatusBarApp()
    return app, app

def is_paused() -> bool:
    """检查是否处于暂停状态"""
    return StatusBarApp.is_paused 