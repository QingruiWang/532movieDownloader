# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(886, 391)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_movieUrl = QtWidgets.QLineEdit(self.centralwidget)
        self.label_movieUrl.setGeometry(QtCore.QRect(250, 40, 541, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_movieUrl.setFont(font)
        self.label_movieUrl.setToolTip("")
        self.label_movieUrl.setAutoFillBackground(True)
        self.label_movieUrl.setText("")
        self.label_movieUrl.setObjectName("label_movieUrl")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 30, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.btn_login = QtWidgets.QPushButton(self.centralwidget)
        self.btn_login.setGeometry(QtCore.QRect(380, 120, 121, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.btn_login.setFont(font)
        self.btn_login.setObjectName("btn_login")
        self.textlbl = QtWidgets.QTextEdit(self.centralwidget)
        self.textlbl.setGeometry(QtCore.QRect(70, 200, 741, 141))
        self.textlbl.setAutoFillBackground(False)
        self.textlbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textlbl.setReadOnly(True)
        self.textlbl.setObjectName("textlbl")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 350, 201, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(330, 350, 501, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "532move Downloader"))
        self.label_movieUrl.setPlaceholderText(_translate("MainWindow", "播放页网络路径，如http://532movie.bnu.edu.cn/movie/3988.html"))
        self.label_3.setText(_translate("MainWindow", "Movie Url："))
        self.btn_login.setText(_translate("MainWindow", "Download"))
        self.label.setText(_translate("MainWindow", "Developer: Qingrui Wang"))
        self.label_4.setText(_translate("MainWindow", "GitHub:https://github.com/QingruiWang/532movieDownloader"))
