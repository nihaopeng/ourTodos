# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 500)
        Form.setMinimumSize(QSize(400, 500))
        Form.setMaximumSize(QSize(400, 500))
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(70, 40, 261, 401))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.verticalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(259, 197))
        self.widget.setStyleSheet(u"background-image:url(:/image/task.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")

        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.emailLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")
        self.emailLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")

        self.verticalLayout_2.addWidget(self.emailLineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.sendCodeBtn = QPushButton(self.verticalLayoutWidget)
        self.sendCodeBtn.setObjectName(u"sendCodeBtn")
        self.sendCodeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sendCodeBtn.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.sendCodeBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.codeLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.codeLineEdit.setObjectName(u"codeLineEdit")
        self.codeLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")

        self.verticalLayout_2.addWidget(self.codeLineEdit)

        self.usernameLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        self.usernameLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")

        self.verticalLayout_2.addWidget(self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setStyleSheet(u"border:1px solid black;\n"
"border-radius:5px;")

        self.verticalLayout_2.addWidget(self.passwordLineEdit)

        self.registerBtn = QPushButton(self.verticalLayoutWidget)
        self.registerBtn.setObjectName(u"registerBtn")
        self.registerBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.registerBtn.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.registerBtn)

        self.back2loginBtn = QPushButton(self.verticalLayoutWidget)
        self.back2loginBtn.setObjectName(u"back2loginBtn")
        self.back2loginBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back2loginBtn.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.back2loginBtn)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.emailLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u90ae\u7bb1", None))
        self.sendCodeBtn.setText(QCoreApplication.translate("Form", u"\u53d1\u9001\u9a8c\u8bc1\u7801", None))
        self.codeLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u9a8c\u8bc1\u7801", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u5bc6\u7801", None))
        self.registerBtn.setText(QCoreApplication.translate("Form", u"\u6ce8\u518c", None))
        self.back2loginBtn.setText(QCoreApplication.translate("Form", u"\u8fd4\u56de\u767b\u5f55", None))
    # retranslateUi

