# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'counter.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLCDNumber, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        Form.setMinimumSize(QSize(400, 500))
        Form.setMaximumSize(QSize(400, 500))
        self.pauseBtn = QPushButton(Form)
        self.pauseBtn.setObjectName(u"pauseBtn")
        self.pauseBtn.setGeometry(QRect(165, 390, 75, 31))
        self.pauseBtn.setStyleSheet(u"")
        self.minSpin = QSpinBox(Form)
        self.minSpin.setObjectName(u"minSpin")
        self.minSpin.setGeometry(QRect(60, 260, 70, 23))
        self.minSpin.setStyleSheet(u"")
        self.minSpin.setValue(90)
        self.resetBtn = QPushButton(Form)
        self.resetBtn.setObjectName(u"resetBtn")
        self.resetBtn.setGeometry(QRect(270, 390, 75, 31))
        self.resetBtn.setStyleSheet(u"")
        self.secSpin = QSpinBox(Form)
        self.secSpin.setObjectName(u"secSpin")
        self.secSpin.setGeometry(QRect(170, 260, 70, 23))
        self.startBtn = QPushButton(Form)
        self.startBtn.setObjectName(u"startBtn")
        self.startBtn.setGeometry(QRect(60, 390, 75, 31))
        self.startBtn.setStyleSheet(u"")
        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(60, 190, 281, 23))
        self.progressBar.setValue(0)
        self.lcd = QLCDNumber(Form)
        self.lcd.setObjectName(u"lcd")
        self.lcd.setGeometry(QRect(60, 90, 281, 91))
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 50, 361, 391))
        self.frame.setStyleSheet(u"border:1px solid black;\n"
"border-radius:10px;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.randomASpin = QSpinBox(Form)
        self.randomASpin.setObjectName(u"randomASpin")
        self.randomASpin.setGeometry(QRect(60, 340, 70, 23))
        self.randomASpin.setStyleSheet(u"")
        self.randomASpin.setValue(3)
        self.randomBSpin = QSpinBox(Form)
        self.randomBSpin.setObjectName(u"randomBSpin")
        self.randomBSpin.setGeometry(QRect(170, 340, 70, 23))
        self.randomBSpin.setStyleSheet(u"")
        self.randomBSpin.setValue(5)
        self.restTimeSpin = QSpinBox(Form)
        self.restTimeSpin.setObjectName(u"restTimeSpin")
        self.restTimeSpin.setGeometry(QRect(270, 340, 70, 23))
        self.restTimeSpin.setStyleSheet(u"")
        self.restTimeSpin.setValue(10)
        self.minLabel = QLabel(Form)
        self.minLabel.setObjectName(u"minLabel")
        self.minLabel.setGeometry(QRect(60, 240, 53, 15))
        self.secLabel = QLabel(Form)
        self.secLabel.setObjectName(u"secLabel")
        self.secLabel.setGeometry(QRect(170, 240, 53, 15))
        self.randomALabel = QLabel(Form)
        self.randomALabel.setObjectName(u"randomALabel")
        self.randomALabel.setGeometry(QRect(60, 320, 81, 16))
        self.randomBLabel = QLabel(Form)
        self.randomBLabel.setObjectName(u"randomBLabel")
        self.randomBLabel.setGeometry(QRect(170, 320, 81, 16))
        self.restTimeLabel = QLabel(Form)
        self.restTimeLabel.setObjectName(u"restTimeLabel")
        self.restTimeLabel.setGeometry(QRect(270, 320, 81, 16))
        self.back2homeBtn = QPushButton(Form)
        self.back2homeBtn.setObjectName(u"back2homeBtn")
        self.back2homeBtn.setGeometry(QRect(20, 10, 75, 31))
        self.back2homeBtn.setStyleSheet(u"")
        self.frame.raise_()
        self.pauseBtn.raise_()
        self.minSpin.raise_()
        self.resetBtn.raise_()
        self.secSpin.raise_()
        self.startBtn.raise_()
        self.progressBar.raise_()
        self.lcd.raise_()
        self.randomASpin.raise_()
        self.randomBSpin.raise_()
        self.restTimeSpin.raise_()
        self.minLabel.raise_()
        self.secLabel.raise_()
        self.randomALabel.raise_()
        self.randomBLabel.raise_()
        self.restTimeLabel.raise_()
        self.back2homeBtn.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pauseBtn.setText(QCoreApplication.translate("Form", u"pause", None))
        self.resetBtn.setText(QCoreApplication.translate("Form", u"reset", None))
        self.startBtn.setText(QCoreApplication.translate("Form", u"start", None))
        self.minLabel.setText(QCoreApplication.translate("Form", u"\u5206\u949f:", None))
        self.secLabel.setText(QCoreApplication.translate("Form", u"\u79d2\uff1a", None))
        self.randomALabel.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u8303\u56f4a(m)", None))
        self.randomBLabel.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u8303\u56f4b(m):", None))
        self.restTimeLabel.setText(QCoreApplication.translate("Form", u"\u5fae\u4f11\u606f\u65f6\u95f4(s)", None))
        self.back2homeBtn.setText(QCoreApplication.translate("Form", u"<-back", None))
    # retranslateUi

