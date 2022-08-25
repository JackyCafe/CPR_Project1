# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1564, 941)
        self.img_label = QLabel(Form)
        self.img_label.setObjectName(u"img_label")
        self.img_label.setGeometry(QRect(0, 0, 800, 600))
        self.startVideo = QPushButton(Form)
        self.startVideo.setObjectName(u"startVideo")
        self.startVideo.setGeometry(QRect(820, 500, 180, 50))
        self.stopVideo = QPushButton(Form)
        self.stopVideo.setObjectName(u"stopVideo")
        self.stopVideo.setGeometry(QRect(820, 550, 180, 50))
        self.exit_btn = QPushButton(Form)
        self.exit_btn.setObjectName(u"exit_btn")
        self.exit_btn.setGeometry(QRect(820, 650, 180, 50))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(820, 450, 67, 17))
        self.Id = QTextEdit(Form)
        self.Id.setObjectName(u"Id")
        self.Id.setGeometry(QRect(870, 440, 104, 30))
        self.poseLabel = QLabel(Form)
        self.poseLabel.setObjectName(u"poseLabel")
        self.poseLabel.setGeometry(QRect(1030, 710, 400, 300))
        self.frequenceLabel = QLabel(Form)
        self.frequenceLabel.setObjectName(u"frequenceLabel")
        self.frequenceLabel.setGeometry(QRect(1030, 410, 400, 300))
        self.deepLabel = QLabel(Form)
        self.deepLabel.setObjectName(u"deepLabel")
        self.deepLabel.setGeometry(QRect(1030, 110, 400, 300))
        self.analysisBtn = QPushButton(Form)
        self.analysisBtn.setObjectName(u"analysisBtn")
        self.analysisBtn.setGeometry(QRect(820, 600, 180, 50))
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(820, 210, 201, 111))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"Ubuntu Condensed"])
        font.setPointSize(24)
        font.setBold(True)
        self.label_4.setFont(font)

        self.horizontalLayout.addWidget(self.label_4)

        self.left_hand = QLabel(self.layoutWidget)
        self.left_hand.setObjectName(u"left_hand")
        self.left_hand.setFont(font)

        self.horizontalLayout.addWidget(self.left_hand)

        self.layoutWidget1 = QWidget(Form)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(820, 322, 201, 111))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.right_hand = QLabel(self.layoutWidget1)
        self.right_hand.setObjectName(u"right_hand")
        self.right_hand.setFont(font)

        self.horizontalLayout_2.addWidget(self.right_hand)

        self.layoutWidget2 = QWidget(Form)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(820, 0, 201, 101))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(24)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label)

        self.depthLabel = QLabel(self.layoutWidget2)
        self.depthLabel.setObjectName(u"depthLabel")
        self.depthLabel.setFont(font1)

        self.horizontalLayout_3.addWidget(self.depthLabel)

        self.layoutWidget3 = QWidget(Form)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(820, 100, 191, 111))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.layoutWidget3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.frequencyLabel = QLabel(self.layoutWidget3)
        self.frequencyLabel.setObjectName(u"frequencyLabel")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.frequencyLabel.setFont(font2)

        self.horizontalLayout_4.addWidget(self.frequencyLabel)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"AI CPR ", None))
        self.img_label.setText(QCoreApplication.translate("Form", u"imgLabel", None))
        self.startVideo.setText(QCoreApplication.translate("Form", u"\u958b\u59cb\u9304\u5f71", None))
        self.stopVideo.setText(QCoreApplication.translate("Form", u"\u7d50\u675f\u9304\u5f71", None))
        self.exit_btn.setText(QCoreApplication.translate("Form", u"\u96e2\u958b", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7de8\u865f", None))
        self.poseLabel.setText(QCoreApplication.translate("Form", u"poseLabel", None))
        self.frequenceLabel.setText(QCoreApplication.translate("Form", u"frequenceLabel", None))
        self.deepLabel.setText(QCoreApplication.translate("Form", u"deepLabel", None))
        self.analysisBtn.setText(QCoreApplication.translate("Form", u"\u5206\u6790", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5de6\u624b", None))
        self.left_hand.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u53f3\u624b", None))
        self.right_hand.setText(QCoreApplication.translate("Form", u"0", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6df1\u5ea6", None))
        self.depthLabel.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u983b\u7387", None))
        self.frequencyLabel.setText(QCoreApplication.translate("Form", u"0.0", None))
    # retranslateUi

