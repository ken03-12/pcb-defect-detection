
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        # ================== CENTRAL ==================
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ================== STYLE (GRAY – FLAT) ==================
        self.centralwidget.setStyleSheet("""
            QWidget {
                background-color: #3a3f47;
                color: #e5e7eb;
                font-family: Segoe UI;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #e5e7eb;
            }
            QPushButton {
                border: none;
            }
        """)

        # ================== BUTTON CHỤP ẢNH ==================
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(830, 810, 251, 71))
        font = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("""
            QPushButton {
                background-color: #00c853;
                color: #1b1f24;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: #00e676;
            }
        """)

        # ================== BUTTON QUAY LẠI ==================
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(130, 110, 251, 71))
        font = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setStyleSheet("""
                 QPushButton {
                     background-color: #ff9100;
                     color: #1b1f24;
                     border-radius: 14px;
                 }
                 QPushButton:hover {
                     background-color: #ffab40;
                 }
             """)

        # ================== IMAGE AREAS (NO FRAME) ==================
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(1130, 350, 256, 430))
        self.label_14.setAutoFillBackground(False)
        self.label_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_14.setMidLineWidth(0)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(520, 290, 571, 550))
        self.label_15.setAutoFillBackground(False)
        self.label_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_15.setMidLineWidth(0)
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")

        # ================== FINAL ==================
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_8.setText(_translate("MainWindow", "Chụp Ảnh"))
        self.pushButton_9.setText(_translate("MainWindow", "Quay Lại"))
