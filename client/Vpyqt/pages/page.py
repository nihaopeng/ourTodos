from abc import abstractmethod
from PySide6.QtWidgets import QWidget

class Page(QWidget):
    """页面基类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("Page 必须有一个父窗口")
    
    @abstractmethod
    def fresh(self):
        """刷新页面"""
        pass