import ctypes
from ctypes import windll, wintypes
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,QSystemTrayIcon, QMenu,QMessageBox
)
from PySide6.QtCore import (
    Qt,QRect,QSharedMemory
)
from PySide6.QtGui import (
    QColor,QPainter, QRegion, QPainterPath,QIcon, QPainter, QAction
)
from pages.rank import RankPage
from pages.todoList import TodoListPage
from core.config import getConfig
from core.updater import applyUpdate
from stackWidget import SlideStackedWidget
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.settings import SettingsPage
from pages.counter import CounterPage
from pages.coach import CoachPage  # 假设你有一个 CoachPage 类

# 定义按键码
VK_LWIN = 0x5B
VK_D = 0x44
KEYEVENTF_KEYUP = 0x0002

user32 = ctypes.windll.user32

# --- Win32 helpers ---
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        # 手动绘制避免被父窗口绘制覆盖
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(200,200,200))
        self.setPalette(palette)
        self.start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 记录鼠标点击点和窗口左上角的差值
            self.start_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.start_pos:
            # 移动整个 MainWindow
            self.window().move(event.globalPosition().toPoint() - self.start_pos)
            # print(event.globalPosition().toPoint())

    def mouseReleaseEvent(self, event):
        self.start_pos = None

        
class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ourTodos")
        self.setGeometry(1000, 36, 400, 500)

        # 窗口沉底
        self.radius = 15
        self.updateMask()  # 初始设置遮罩
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 添加可拖动标题栏
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 创建堆叠窗口
        self.stacked_widget = SlideStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # 页面字典
        self.pages = {}
        
        # 注册页面
        self.register_page("login", LoginPage(self))
        self.register_page("register", RegisterPage(self))
        self.register_page("settings", SettingsPage(self))  
        self.register_page("todoList", TodoListPage(self)) # 登录界面后再重新创建
        self.register_page("coach", CoachPage(self))  # 注册教练页面
        self.register_page("counter", CounterPage(self))
        self.register_page("rank", RankPage(self))  # 占位，实际创建在需要时
        
        
        # 初始显示登录页面
        self.switch_to_page("login", "right")

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("ui/src/task.png"))  # 设置托盘图标，替换为你的图标路径

        # 创建托盘菜单
        self.tray_menu = QMenu()

        # 添加最小化
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)
        self.tray_menu.addAction(show_action)
        # 添加显示
        mini_action = QAction("最小化", self)
        mini_action.triggered.connect(self.hide)
        self.tray_menu.addAction(mini_action)
        # 添加退出选项
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(sys.exit)
        self.tray_menu.addAction(exit_action)

        # 将菜单绑定到托盘图标
        self.tray_icon.setContextMenu(self.tray_menu)

        # 显示托盘图标
        self.tray_icon.show()
    
    def register_page(self, name, widget):
        """
        注册新页面
        重复注册需要销毁以前的副本
        """
        if not self.pages.get(name):
            # 如果不存在
            self.pages[name] = widget
        else:
            # 如果存在
            old_widget = self.pages[name]
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
            self.pages[name] = widget
        self.stacked_widget.addWidget(widget)
        # 设置样式
        self.setStyleSheet(f"background-color:{getConfig()["THEME"]["BGCOLOR"]};")
        self.stacked_widget.setThemeForAllWidgets()
    
    def switch_to_page(self, page_name, direction="right"):
        """切换到指定页面"""
        # 设置动画方向
        self.stacked_widget.direction = direction
        # 切换页面
        self.stacked_widget.setCurrentWidget(self.pages[page_name])
        self.pages[page_name].fresh()

    def resizeEvent(self, event):
        self.updateMask()  # 尺寸变化时更新遮罩
        super().resizeEvent(event)

    def updateMask(self):
        """单独更新遮罩的方法"""
        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.radius, self.radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def paintEvent(self, event):
        """只负责绘制视觉效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 50))  # 控制透明度
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

    def unset_desktop_window(self):
        win_hwnd = self.winId()
        # 1. 把 parent 设置回桌面（0 表示 HWND_DESKTOP）
        windll.user32.SetParent(win_hwnd, 0)
        # 2. 恢复窗口 flags（根据需要，这里我给个普通窗口示例）
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)  
        # 你可以改成 Qt.WindowStaysOnTopHint 等等
        # 3. 重新显示
        self.show()

    def _find_shell_defview(self):
        """返回 (shellview_hwnd, parent_top_hwnd, parent_class)；找不到则 (None,None,None)"""
        result = {"shell": None, "parent": None, "cls": None}

        @EnumWindowsProc
        def enum_cb(hwnd, lParam):
            # 在每个顶层窗口下查找 SHELLDLL_DefView
            shell = user32.FindWindowExW(hwnd, None, "SHELLDLL_DefView", None)
            if shell:
                buf = (ctypes.c_wchar * 256)()
                user32.GetClassNameW(hwnd, buf, 256)
                result["shell"] = shell
                result["parent"] = hwnd
                result["cls"] = buf.value
                return False  # 停止枚举
            return True

        user32.EnumWindows(enum_cb, 0)
        return result["shell"], result["parent"], result["cls"]

    # --- 在你的 MainWindow 里调用 ---
    def set_desktop_window(self):
        # 推荐无边框 + 透明背景（按需）
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)  # 子窗口用 Qt.Widget 即可
        win_hwnd = self.winId()
        """根据 DefView 所在位置，决定如何 SetParent"""
        shell, parent, cls = self._find_shell_defview()
        if not shell:
            # print("未找到 SHELLDLL_DefView")
            return False
        user32.SetParent(win_hwnd, shell)
        # print(f"嵌入到 SHELLDLL_DefView: hwnd={shell}")
        user32.ShowWindow(win_hwnd, 1)
        self.show()

    def show_desktop(self):
        # 按下 Win
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
        # 按下 D
        ctypes.windll.user32.keybd_event(VK_D, 0, 0, 0)
        # 松开 D
        ctypes.windll.user32.keybd_event(VK_D, 0, KEYEVENTF_KEYUP, 0)
        # 松开 Win
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)
        self.show()

APP_KEY = "ourTodosKey"  # 全局唯一标识

if __name__ == "__main__":
    # applyUpdate(__file__)
    shared_mem = QSharedMemory(APP_KEY)
    app = QApplication(sys.argv)
    # 重复打开检查
    if not shared_mem.create(1):
        QMessageBox.information(None, "消息", "ourTodos已打开,查看托盘图标")
        sys.exit(0)
    # 应用样式
    app.setStyle("Fusion")
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    sys.exit(app.exec())