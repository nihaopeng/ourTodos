from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QMovie

class Ui_Form(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # 拦截点击
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # 半透明遮罩

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # 加载动画 (gif)
        self.label = QLabel(self)
        movie = QMovie("ui/src/loading.gif")  # 你需要准备一个 loading.gif
        movie.setScaledSize(QSize(100, 100))
        self.label.setMovie(movie)
        movie.start()

        layout.addWidget(self.label)
        self.hide()

    def showEvent(self, event):
        """调整大小覆盖整个父窗口"""
        if self.parent():
            self.resize(self.parent().size())
        super().showEvent(event)
