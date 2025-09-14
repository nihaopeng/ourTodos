# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'todoStatusCheck.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QTextBrowser, QToolButton,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        Form.setMinimumSize(QSize(400, 500))
        Form.setMaximumSize(QSize(400, 500))
        self.descriptionTextBrowser = QTextBrowser(Form)
        self.descriptionTextBrowser.setObjectName(u"descriptionTextBrowser")
        self.descriptionTextBrowser.setGeometry(QRect(80, 80, 251, 111))
        self.descriptionTextBrowser.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.todoNameLabel = QLabel(Form)
        self.todoNameLabel.setObjectName(u"todoNameLabel")
        self.todoNameLabel.setGeometry(QRect(80, 50, 251, 21))
        self.todoNameLabel.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.scoreJudgeScrollArea = QScrollArea(Form)
        self.scoreJudgeScrollArea.setObjectName(u"scoreJudgeScrollArea")
        self.scoreJudgeScrollArea.setGeometry(QRect(80, 230, 251, 171))
        self.scoreJudgeScrollArea.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.scoreJudgeScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 249, 169))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.scoreJudgeScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.todoFinishedBtn = QPushButton(Form)
        self.todoFinishedBtn.setObjectName(u"todoFinishedBtn")
        self.todoFinishedBtn.setGeometry(QRect(80, 410, 75, 38))
        font = QFont()
        font.setBold(False)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.todoFinishedBtn.setFont(font)
        self.todoFinishedBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.todoFinishedBtn.setStyleSheet(u"")
        self.todoDeleteBtn = QPushButton(Form)
        self.todoDeleteBtn.setObjectName(u"todoDeleteBtn")
        self.todoDeleteBtn.setGeometry(QRect(260, 410, 75, 38))
        self.todoDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.todoDeleteBtn.setStyleSheet(u"")
        self.fileUploadBtn = QPushButton(Form)
        self.fileUploadBtn.setObjectName(u"fileUploadBtn")
        self.fileUploadBtn.setGeometry(QRect(170, 410, 75, 38))
        self.fileUploadBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.fileUploadBtn.setStyleSheet(u"")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 470, 53, 15))
        self.stepAddBtn = QToolButton(Form)
        self.stepAddBtn.setObjectName(u"stepAddBtn")
        self.stepAddBtn.setGeometry(QRect(310, 200, 21, 21))
        self.stepAddBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stepAddBtn.setStyleSheet(u"")
        self.stepLineEdit = QLineEdit(Form)
        self.stepLineEdit.setObjectName(u"stepLineEdit")
        self.stepLineEdit.setGeometry(QRect(80, 200, 221, 21))
        self.stepLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.back2homeBtn = QToolButton(Form)
        self.back2homeBtn.setObjectName(u"back2homeBtn")
        self.back2homeBtn.setGeometry(QRect(10, 10, 61, 41))
        self.back2homeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back2homeBtn.setStyleSheet(u"")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.todoNameLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.todoFinishedBtn.setText(QCoreApplication.translate("Form", u"\u786e\u8ba4\u5b8c\u6210", None))
        self.todoDeleteBtn.setText(QCoreApplication.translate("Form", u"\u786e\u8ba4\u5220\u9664", None))
        self.fileUploadBtn.setText(QCoreApplication.translate("Form", u"\u4e0a\u4f20\u6750\u6599", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"file:", None))
        self.stepAddBtn.setText(QCoreApplication.translate("Form", u"\uff0b", None))
        self.back2homeBtn.setText(QCoreApplication.translate("Form", u"<-back", None))
    # retranslateUi

