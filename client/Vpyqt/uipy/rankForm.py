# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rank.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        self.rankLabel = QLabel(Form)
        self.rankLabel.setObjectName(u"rankLabel")
        self.rankLabel.setGeometry(QRect(340, 10, 53, 15))
        self.rankScrollArea = QScrollArea(Form)
        self.rankScrollArea.setObjectName(u"rankScrollArea")
        self.rankScrollArea.setGeometry(QRect(20, 60, 361, 431))
        self.rankScrollArea.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.rankScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 359, 429))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.userRankBtn = QPushButton(self.scrollAreaWidgetContents)
        self.userRankBtn.setObjectName(u"userRankBtn")
        self.userRankBtn.setEnabled(True)
        self.userRankBtn.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.userRankBtn)

        self.userRankBtn_2 = QPushButton(self.scrollAreaWidgetContents)
        self.userRankBtn_2.setObjectName(u"userRankBtn_2")
        self.userRankBtn_2.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.userRankBtn_2)

        self.userRankBtn_3 = QPushButton(self.scrollAreaWidgetContents)
        self.userRankBtn_3.setObjectName(u"userRankBtn_3")
        self.userRankBtn_3.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.userRankBtn_3)

        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"border:0px;")

        self.verticalLayout.addWidget(self.widget)

        self.rankScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.back2homeBtn = QToolButton(Form)
        self.back2homeBtn.setObjectName(u"back2homeBtn")
        self.back2homeBtn.setGeometry(QRect(20, 10, 61, 41))
        self.back2homeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back2homeBtn.setStyleSheet(u"")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.rankLabel.setText(QCoreApplication.translate("Form", u"rank:1", None))
        self.userRankBtn.setText(QCoreApplication.translate("Form", u"user1 2889567450@qq.com -score:23", None))
        self.userRankBtn.setProperty(u"type", QCoreApplication.translate("Form", u"userRankBtn", None))
        self.userRankBtn_2.setText(QCoreApplication.translate("Form", u"user2 2889567450@qq.com -score:23", None))
        self.userRankBtn_2.setProperty(u"type", QCoreApplication.translate("Form", u"userRankBtn", None))
        self.userRankBtn_3.setText(QCoreApplication.translate("Form", u"user3 2889567450@qq.com -score:23", None))
        self.userRankBtn_3.setProperty(u"type", QCoreApplication.translate("Form", u"userRankBtn", None))
        self.back2homeBtn.setText(QCoreApplication.translate("Form", u"<-back", None))
    # retranslateUi

