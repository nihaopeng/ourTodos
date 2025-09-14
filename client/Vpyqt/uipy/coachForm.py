# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'coach.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QScrollArea, QSizePolicy,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        self.taskLineEdit = QLineEdit(Form)
        self.taskLineEdit.setObjectName(u"taskLineEdit")
        self.taskLineEdit.setGeometry(QRect(60, 80, 211, 41))
        self.taskLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.taskLineEdit.setReadOnly(False)
        self.stepScrollArea = QScrollArea(Form)
        self.stepScrollArea.setObjectName(u"stepScrollArea")
        self.stepScrollArea.setGeometry(QRect(60, 150, 281, 301))
        self.stepScrollArea.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")
        self.stepScrollArea.setWidgetResizable(True)
        self.stepScrollAreaWidgetContents = QWidget()
        self.stepScrollAreaWidgetContents.setObjectName(u"stepScrollAreaWidgetContents")
        self.stepScrollAreaWidgetContents.setGeometry(QRect(0, 0, 279, 299))
        self.verticalLayout_2 = QVBoxLayout(self.stepScrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser = QTextBrowser(self.stepScrollAreaWidgetContents)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.stepScrollArea.setWidget(self.stepScrollAreaWidgetContents)
        self.callCoachBtn = QToolButton(Form)
        self.callCoachBtn.setObjectName(u"callCoachBtn")
        self.callCoachBtn.setGeometry(QRect(280, 80, 61, 41))
        self.callCoachBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.callCoachBtn.setStyleSheet(u"")
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
        self.taskLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u4f60\u73b0\u5728\u5728\u5e72\u4ec0\u4e48\uff0c\u4f60\u60f3\u53bb\u505a\u4ec0\u4e48\uff1f", None))
        self.callCoachBtn.setText(QCoreApplication.translate("Form", u"Coach!!!", None))
        self.back2homeBtn.setText(QCoreApplication.translate("Form", u"<-back", None))
    # retranslateUi

