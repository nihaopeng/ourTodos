from PySide6.QtWidgets import QStackedWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QParallelAnimationGroup

from backend.config import getConfig

class SlideStackedWidget(QStackedWidget):
    """带滑动动画的堆叠窗口控件 - 修复残影问题"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.super_set_index = super().setCurrentIndex
        self.animation_duration = 400  # 动画持续时间(毫秒)
        self.current_index = 0
        self.next_index = 0
        self.now_showing = False
        self.direction = "right"  # 默认动画方向
        
    def setCurrentIndex(self, index):
        if self.now_showing or index == self.current_index:
            return

        self.next_index = index
        self.now_showing = True

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        # 确保下一个部件可见并设置正确的大小
        next_widget.setGeometry(0, 0, self.width(), self.height())
        next_widget.show()
        next_widget.raise_()

        # 根据方向设置初始位置
        if self.direction == "right":
            next_widget.move(self.width(), 0)
            end_pos = QPoint(0, 0)
            current_end_pos = QPoint(-self.width(), 0)
        elif self.direction == "left":
            next_widget.move(-self.width(), 0)
            end_pos = QPoint(0, 0)
            current_end_pos = QPoint(self.width(), 0)
        elif self.direction == "down":
            next_widget.move(0, -self.height())
            end_pos = QPoint(0, 0)
            current_end_pos = QPoint(0, self.height())
        else:  # "up"
            next_widget.move(0, self.height())
            end_pos = QPoint(0, 0)
            current_end_pos = QPoint(0, -self.height())

        # 动画组
        self.animation_group = QParallelAnimationGroup(self)

        # 下一个部件的动画
        slide_anim = QPropertyAnimation(next_widget, b"pos")
        slide_anim.setDuration(self.animation_duration)
        slide_anim.setStartValue(next_widget.pos())
        slide_anim.setEndValue(end_pos)
        slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_group.addAnimation(slide_anim)

        # 当前部件的动画
        if current_widget:
            current_anim = QPropertyAnimation(current_widget, b"pos")
            current_anim.setDuration(self.animation_duration)
            current_anim.setStartValue(current_widget.pos())
            current_anim.setEndValue(current_end_pos)
            current_anim.setEasingCurve(QEasingCurve.InCubic)
            self.animation_group.addAnimation(current_anim)

        def finish_animation():
            # 重置当前部件位置并隐藏
            if current_widget:
                current_widget.move(0, 0)  # 重置位置
                current_widget.hide()
            
            # 更新当前索引
            self.super_set_index(index)
            self.current_index = index
            self.now_showing = False

        self.animation_group.finished.connect(finish_animation)
        self.animation_group.start()
    
    def setCurrentWidget(self, widget):
        self.setCurrentIndex(self.indexOf(widget))

    def setThemeForAllWidgets(self):
        config = getConfig()
        btnColor = config["THEME"]["BTNCOLOR"]
        btnHoverColor = config["THEME"]["BTNHOVERCOLOR"]
        bgColor = config["THEME"]["BGCOLOR"]
        fontColor = config["THEME"]["FONTCOLOR"]
        QPushButtonQss=f"""
            border: 1px solid black;
            border-radius: 5px;
            background-color:{btnColor}"""
        QToolButtonQss=QPushButtonQss
        QPushButtonHoverQss=f"""
            border:1px solid black;
            border-radius:5px;
            background-color:{btnHoverColor};"""
        QToolButtonHoverQss=QPushButtonHoverQss
        QFontQss=f"""color:{fontColor};"""
        with open("ui/src/style.qss",encoding='utf-8') as f:
            qss=f.read().format(
                QPushButton=QPushButtonQss,
                QPushButtonHover=QPushButtonHoverQss,
                QToolButton=QToolButtonQss,
                QToolButtonHover=QToolButtonHoverQss,
                QFont=QFontQss
            )
        for index in range(self.count()):
            w=self.widget(index)
            if w is not None:
                w.setStyleSheet(qss)