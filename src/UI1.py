
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("BAO CAO")
        MainWindow.resize(1920, 1080)

        # ================== CENTRAL ==================
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ================== GRAY FLAT STYLE ==================
        self.centralwidget.setStyleSheet("""
            #centralwidget {
                background-image: url(D:/Download/Anh-nen-trang-mo-ao.jpg);
                background-repeat: no-repeat;
                background-position: center;
            }
            QWidget {
                background-color: #ebebeb;   
                color: #004aad;
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
            QSpinBox {
                background-color: #ffff;
                color: #00e5ff;
                border: none;
                padding: 4spx;
            }
        """)

        # ================== BUTTONS ==================
        # ================== BUTTONS (CÂN GIỮA MÀN HÌNH) ==================
        font_btn = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)

        # 1. NÚT RESET (Màu Xanh Dương) - Vị trí đầu tiên
        # Tọa độ: x=390
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(390, 850, 230, 71))
        self.pushButton_7.setFont(font_btn)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setText("RESET")
        self.pushButton_7.setStyleSheet("""
                    QPushButton {
                        background-color: #2962ff;
                        color: #ffffff;
                        border-radius: 14px;
                    }
                    QPushButton:hover {
                        background-color: #448aff;
                    }
                """)

        # 2. NÚT LẤY MẪU (Màu Cam) - Cách nút Reset 60px
        # Tọa độ: x=680
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 850, 230, 71))
        self.pushButton_6.setFont(font_btn)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9100;
                        color: #1b1f24;
                        border-radius: 14px;
                    }
                    QPushButton:hover {
                        background-color: #ffab40;
                    }
                """)

        # 3. NÚT BẮT ĐẦU (Màu Xanh Lá) - Cách nút Lấy Mẫu 60px
        # Tọa độ: x=970 (Nằm ngay bên phải tâm màn hình)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(970, 850, 250, 71))
        self.pushButton_4.setFont(font_btn)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
                    QPushButton {
                        background-color: #00c853;
                        color: #1b1f24;
                        border-radius: 14px;
                    }
                    QPushButton:hover {
                        background-color: #00e676;
                    }
                """)

        # 4. NÚT DỪNG (Màu Đỏ) - Vị trí cuối cùng
        # Tọa độ: x=1280
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1280, 850, 250, 71))
        self.pushButton_5.setFont(font_btn)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("""
                    QPushButton {
                        background-color: #d50000;
                        color: #ffffff;
                        border-radius: 14px;
                    }
                    QPushButton:hover {
                        background-color: #ff1744;
                    }
                """)
        # ================== IMAGE AREAS (NO FRAME) ==================
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(1130, 350, 256, 430))
        self.label_14.setText("")
        self.label_14.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(520, 290, 571, 550))
        self.label_15.setText("")
        self.label_15.setFrameShape(QtWidgets.QFrame.NoFrame)

        # ================== COUNTERS ==================
        font_label = QtGui.QFont("Segoe UI", 15)
        font_counter = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 420, 271, 41))
        self.label_2.setFont(font_label)
        self.label_2.setStyleSheet("color: #004aad;")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 420, 80, 41))
        self.label_4.setFont(font_counter)
        self.label_4.setStyleSheet("color: #004aad;")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 500, 271, 41))
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: #004aad;")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 500, 80, 41))
        self.label_3.setFont(font_counter)
        self.label_3.setStyleSheet("color: #004aad;")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(120, 590, 271, 41))
        self.label_5.setFont(font_label)
        self.label_5.setStyleSheet("color: #004aad;")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(430, 600, 60, 36))
        self.spinBox.setFont(QtGui.QFont("Segoe UI", 16))
        self.spinBox.setStyleSheet("color: #004aad;")

        # ================== LOGOS ==================
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(100, 90, 200, 200))
        self.label_6.setPixmap(QtGui.QPixmap(
            "logo.png"
        ))
        self.label_6.setScaledContents(True)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1630, 90, 200, 200))
        self.label_7.setPixmap(QtGui.QPixmap(
            "10.png"
        ))
        self.label_7.setScaledContents(True)

        # ================== TITLES ==================
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(650, 10, 700, 61))
        self.label_9.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        self.label_9.setStyleSheet("color: #004aad;")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(770, 60, 591, 61))
        self.label_12.setFont(QtGui.QFont("Segoe UI", 18,QtGui.QFont.Bold))
        self.label_12.setStyleSheet("color: #004aad;")

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(600, 120, 700, 61))
        self.label_13.setFont(QtGui.QFont("Segoe UI", 27, QtGui.QFont.Bold))
        self.label_13.setStyleSheet("color: #004aad;")

        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(530, 180, 941, 61))
        self.label_16.setFont(QtGui.QFont("Segoe UI",18,QtGui.QFont.Bold))
        self.label_16.setStyleSheet("color: #004aad;")

        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(430, 240, 980, 61))
        self.label_17.setFont(QtGui.QFont("Segoe UI", 18,QtGui.QFont.Bold))
        self.label_17.setStyleSheet("color: #C0392B;")

        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(570, 280, 905, 61))
        self.label_18.setFont(QtGui.QFont("Segoe UI", 18,QtGui.QFont.Bold))
        self.label_18.setStyleSheet("color:#C0392B;")

        # ================== FINAL ==================
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_4.setText(_translate("MainWindow", "BẮT ĐẦU"))
        self.pushButton_5.setText(_translate("MainWindow", "DỪNG"))
        self.pushButton_6.setText(_translate("MainWindow", "LẤY MẪU"))
        self.label.setText(_translate("MainWindow", "Số Lượng PCB lỗi :"))
        self.label_2.setText(_translate("MainWindow", "Số Lượng PCB chuẩn :"))
        self.label_3.setText(_translate("MainWindow", "000"))
        self.label_4.setText(_translate("MainWindow", "000"))
        self.label_5.setText(_translate("MainWindow", "Giá Trị Đặt :"))
        self.pushButton_7.setText(_translate("MainWindow", "RESET"))
        self.label_9.setText(_translate("MainWindow", "TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT"))
        self.label_12.setText(_translate("MainWindow", "KHOA ĐIỆN - ĐIỆN TỬ"))
        self.label_13.setText(_translate("MainWindow", "ĐỒ ÁN TỐT NGHIỆP ĐẠI HỌC"))
        self.label_16.setText(_translate("MainWindow","NGÀNH: CÔNG NGHỆ KỸ THUẬT ĐIỆN TỬ - VIỄN THÔNG"))
        self.label_17.setText(_translate("MainWindow", "ĐỀ TÀI: NGHIÊN CỨU XÂY DỰNG HỆ THỐNG ỨNG DỤNG XỬ LÝ ẢNH"))
        self.label_18.setText(_translate("MainWindow","TRONG PHÁT HIỆN VÀ NHẬN DIỆN LỖI TRÊN PCB"))