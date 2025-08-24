
from PySide6.QtWidgets import (
    QWidget,QMessageBox
)
import sys
from PySide6.QtCore import QTimer, QTime, QDateTime, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from uipy.counterForm import Ui_Form as CounterFormUI

import random
import sys
from PySide6.QtCore import QTimer, QDateTime
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QUrl

from uipy.counterForm import Ui_Form as CounterFormUI  # 你的 counter.ui 转换生成的文件


class CounterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("CounterPage 必须有一个父窗口")

        # 设置UI
        self.ui = CounterFormUI()
        self.ui.setupUi(self)

        # 播放提示音
        self.sound_start = QSoundEffect()
        self.sound_start.setSource(QUrl.fromLocalFile("ui/wav/beep_start.wav"))
        self.sound_start.setVolume(0.7)

        self.sound_end = QSoundEffect()
        self.sound_end.setSource(QUrl.fromLocalFile("ui/wav/beep_end.wav"))
        self.sound_end.setVolume(0.7)

        # 状态变量
        self.total_ms = 0             # 总倒计时时间
        self.end_ts = None            # 结束时间戳
        self.remaining_ms = 0         # 剩余时间
        self.paused = False
        self.resting = False          # 是否处于休息阶段

        # 定时器
        self.timer = QTimer(self)
        self.timer.setInterval(200)  # 每200ms刷新一次
        self.timer.timeout.connect(self.on_tick)

        # 连接信号与槽
        self.ui.startBtn.clicked.connect(self.start)
        self.ui.pauseBtn.clicked.connect(self.pause)
        self.ui.resetBtn.clicked.connect(self.reset)
        self.ui.back2homeBtn.clicked.connect(
            lambda: self.parent_window.switch_to_page("todoList", "left")
        )

    def start(self):
        if not self.timer.isActive() and not self.resting:
            # 初次开始
            if not self.end_ts:
                mins = self.ui.minSpin.value()
                secs = self.ui.secSpin.value()
                total_secs = mins * 60 + secs
                if total_secs <= 0:
                    QMessageBox.information(self, "提示", "请设置大于 0 的时间")
                    return
                self.total_ms = total_secs * 1000
                self.end_ts = QDateTime.currentMSecsSinceEpoch() + self.total_ms

                # 设置第一次随机间隔
                self.schedule_next_break()

            # 如果是暂停后继续
            elif self.paused:
                self.end_ts = QDateTime.currentMSecsSinceEpoch() + self.remaining_ms
                self.paused = False

            self.timer.start()

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
            now = QDateTime.currentMSecsSinceEpoch()
            self.remaining_ms = max(0, self.end_ts - now)
            self.paused = True

    def reset(self):
        self.timer.stop()
        self.total_ms = 0
        self.end_ts = None
        self.remaining_ms = 0
        self.paused = False
        self.resting = False
        self.update_lcd(0)
        self.ui.progressBar.setValue(0)

    def on_tick(self):
        now = QDateTime.currentMSecsSinceEpoch()
        remain = max(0, self.end_ts - now)
        self.remaining_ms = remain
        self.update_lcd(remain)

        # 更新进度条
        if self.total_ms > 0:
            progress = int(100 * (self.total_ms - remain) / self.total_ms)
            self.ui.progressBar.setValue(progress)

        # 倒计时结束
        if remain <= 0:
            self.timer.stop()
            self.sound.play()
            QMessageBox.information(self, "时间到", "倒计时结束！")
            return

        # 检查是否到达随机休息点
        if not self.resting and now >= self.next_break_ts:
            self.enter_rest()

    def update_lcd(self, ms):
        secs = max(0, (ms + 500) // 1000)
        m, s = divmod(secs, 60)
        self.ui.lcd.display(f"{m:02d}:{s:02d}")

    def schedule_next_break(self):
        """设置下一个随机间隔点"""
        a = self.ui.randomASpin.value()
        b = self.ui.randomBSpin.value()
        delta = random.randint(a, b) * 1000 * 60
        self.next_break_ts = QDateTime.currentMSecsSinceEpoch() + delta

    def enter_rest(self):
        """进入休息阶段"""
        self.resting = True
        # self.timer.stop()
        self.sound_start.play()

        rest_secs = self.ui.restTimeSpin.value()
        self.remaining_rest_ms = rest_secs * 1000
        self.rest_end_ts = QDateTime.currentMSecsSinceEpoch() + self.remaining_rest_ms

        # 启动一个新的休息定时器
        self.rest_timer = QTimer(self)
        self.rest_timer.setInterval(200)
        self.rest_timer.timeout.connect(self.on_rest_tick)
        self.rest_timer.start()

    def on_rest_tick(self):
        now = QDateTime.currentMSecsSinceEpoch()
        remain = max(0, self.rest_end_ts - now)

        if remain <= 0:
            self.rest_timer.stop()
            self.sound_end.play()
            self.resting = False
            self.schedule_next_break()
            # self.timer.start()


        