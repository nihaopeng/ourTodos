# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'todoList.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QLabel, QLineEdit,
    QScrollArea, QSizePolicy, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        Form.setMinimumSize(QSize(400, 500))
        Form.setMaximumSize(QSize(400, 500))
        Form.setStyleSheet(u"")
        self.settingsBtn = QToolButton(Form)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setGeometry(QRect(30, 20, 31, 31))
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settingsBtn.setStyleSheet(u"")
        self.todoListScrollArea = QScrollArea(Form)
        self.todoListScrollArea.setObjectName(u"todoListScrollArea")
        self.todoListScrollArea.setGeometry(QRect(69, 199, 271, 261))
        self.todoListScrollArea.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.todoListScrollArea.setWidgetResizable(True)
        self.todoListScrollAreaVLayout = QWidget()
        self.todoListScrollAreaVLayout.setObjectName(u"todoListScrollAreaVLayout")
        self.todoListScrollAreaVLayout.setGeometry(QRect(0, 0, 269, 259))
        self.verticalLayout = QVBoxLayout(self.todoListScrollAreaVLayout)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.todoListScrollAreaVLayout)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"border:0px solid black;")

        self.verticalLayout.addWidget(self.widget)

        self.todoListScrollArea.setWidget(self.todoListScrollAreaVLayout)
        self.scoreLabel = QLabel(Form)
        self.scoreLabel.setObjectName(u"scoreLabel")
        self.scoreLabel.setGeometry(QRect(302, 30, 91, 20))
        self.scoreLabel.setStyleSheet(u"")
        self.addTodoBtn = QToolButton(Form)
        self.addTodoBtn.setObjectName(u"addTodoBtn")
        self.addTodoBtn.setGeometry(QRect(320, 60, 21, 21))
        self.addTodoBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addTodoBtn.setStyleSheet(u"")
        self.todoLineEdit = QLineEdit(Form)
        self.todoLineEdit.setObjectName(u"todoLineEdit")
        self.todoLineEdit.setGeometry(QRect(70, 60, 241, 21))
        self.todoLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.todoDescribeTextEdit = QTextEdit(Form)
        self.todoDescribeTextEdit.setObjectName(u"todoDescribeTextEdit")
        self.todoDescribeTextEdit.setGeometry(QRect(70, 120, 271, 71))
        self.todoDescribeTextEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.CoachBtn = QToolButton(Form)
        self.CoachBtn.setObjectName(u"CoachBtn")
        self.CoachBtn.setGeometry(QRect(70, 20, 61, 31))
        self.CoachBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.CoachBtn.setStyleSheet(u"")
        self.counterBtn = QToolButton(Form)
        self.counterBtn.setObjectName(u"counterBtn")
        self.counterBtn.setGeometry(QRect(140, 20, 61, 31))
        self.counterBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.counterBtn.setStyleSheet(u"")
        self.rankBtn = QToolButton(Form)
        self.rankBtn.setObjectName(u"rankBtn")
        self.rankBtn.setGeometry(QRect(210, 20, 61, 31))
        self.rankBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.rankBtn.setStyleSheet(u"")
        self.dateEdit = QDateEdit(Form)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(220, 90, 122, 23))
        self.dateEdit.setCalendarPopup(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.settingsBtn.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e", None))
        self.scoreLabel.setText(QCoreApplication.translate("Form", u"Scores:0", None))
        self.addTodoBtn.setText(QCoreApplication.translate("Form", u"\uff0b", None))
        self.todoLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u5f85\u529e\u540d\u79f0", None))
        self.todoDescribeTextEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u5f85\u529e\u63cf\u8ff0\u4e0d\u53ef\u4e3a\u7a7a\uff0c\u8d8a\u8be6\u7ec6\u6e05\u6670\u8d8a\u4f73", None))
        self.CoachBtn.setText(QCoreApplication.translate("Form", u"Coach", None))
        self.counterBtn.setText(QCoreApplication.translate("Form", u"\u8ba1\u65f6\u5668", None))
        self.rankBtn.setText(QCoreApplication.translate("Form", u"\u6392\u540d", None))
    # retranslateUi

