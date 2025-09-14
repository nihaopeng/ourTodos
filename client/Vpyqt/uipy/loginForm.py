# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        Form.setMinimumSize(QSize(400, 500))
        Form.setMaximumSize(QSize(400, 500))
        Form.setStyleSheet(u"")
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(70, 40, 261, 401))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.verticalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-image:url(:/image/task.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")

        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.emailLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")
        self.emailLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;\n"
"padding:5px;")

        self.verticalLayout_2.addWidget(self.emailLineEdit)

        self.passwordLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;\n"
"padding:5px;")

        self.verticalLayout_2.addWidget(self.passwordLineEdit)

        self.loginConfirmBtn = QPushButton(self.verticalLayoutWidget)
        self.loginConfirmBtn.setObjectName(u"loginConfirmBtn")
        self.loginConfirmBtn.setMaximumSize(QSize(16777215, 16777215))
        self.loginConfirmBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.loginConfirmBtn.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.loginConfirmBtn)

        self.registerBtn = QPushButton(self.verticalLayoutWidget)
        self.registerBtn.setObjectName(u"registerBtn")
        self.registerBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.registerBtn.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.registerBtn)

        self.customerLoginBtn = QPushButton(self.verticalLayoutWidget)
        self.customerLoginBtn.setObjectName(u"customerLoginBtn")
        self.customerLoginBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.customerLoginBtn.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.customerLoginBtn)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.emailLineEdit.setText(QCoreApplication.translate("Form", u"admin", None))
        self.emailLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u90ae\u7bb1", None))
        self.passwordLineEdit.setText(QCoreApplication.translate("Form", u"admin123", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u5bc6\u7801", None))
        self.loginConfirmBtn.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.registerBtn.setText(QCoreApplication.translate("Form", u"\u6ce8\u518c", None))
        self.customerLoginBtn.setText(QCoreApplication.translate("Form", u"\u6e38\u5ba2\u767b\u5f55", None))
    # retranslateUi

