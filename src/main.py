import sys, os, time
import cv2
import numpy as np
import serial
from skimage.metrics import structural_similarity as ssim
from PyQt5 import QtWidgets, QtCore, QtGui

from UI1 import Ui_MainWindow as UI1_Main
from UI2 import Ui_MainWindow as UI2_Main

import smtplib
from email.mime.text import MIMEText

# ================= EMAIL ALERT =================
EMAIL_GUI = "dat361002@gmail.com"
APP_PASSWORD = "hggm ilca mqzm dyzc"
EMAIL_NHAN = "nguyendat100623@gmail.com"

# ================= CONFIG =================
CAMERA_ID = 1

SERIAL_PORT = "COM7"
BAUDRATE = 9600
SERIAL_TIMEOUT = 0.1

GOOD_PATH = "good.png"

MASTER_W = 256
MASTER_H = 477

PCB_LOWER = np.array([80, 40, 40])
PCB_UPPER = np.array([140, 255, 255])
kernel = np.ones((7, 7), np.uint8)

# [CẤU HÌNH] Bắt lỗi nhỏ
MIN_AREA = 10
PAD = 6

DATA_OK_DIR = "data_crop/DUT"
DATA_NG_DIR = "data_crop/KHUYET"
DATA_LO_DIR = "data_crop/PAD"

COLLECT_DIR = "Collected_Crops"
os.makedirs(COLLECT_DIR, exist_ok=True)

LABEL_COLORS = {
    "DUT": (0, 255, 0),
    "KHUYET": (0, 0, 255),
    "PAD": (0, 255, 255)
}

# ================= SERIAL INIT =================
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=SERIAL_TIMEOUT)
    print(f"🔌 Đã kết nối Arduino {SERIAL_PORT}")
except Exception as e:
    ser = None
    print("⚠️ Không mở được COM:", e)


# ================= LOAD DATA =================
def load_gray_images(folder):
    imgs = []
    if not os.path.isdir(folder): return imgs
    for f in os.listdir(folder):
        if f.lower().endswith(".png"):
            img = cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)
            if img is not None: imgs.append(img)
    return imgs


ok_templates = load_gray_images(DATA_OK_DIR)
ng_templates = load_gray_images(DATA_NG_DIR)
lo_templates = load_gray_images(DATA_LO_DIR)

if not ok_templates: print("⚠️ Cảnh báo: Thiếu mẫu DUT")
if not ng_templates: print("⚠️ Cảnh báo: Thiếu mẫu KHUYET")
if not lo_templates: print("⚠️ Cảnh báo: Thiếu mẫu PAD")


def send_email_alert(ok_count, ng_count, current_consecutive, limit):
    try:
        content = (
            f"CANH BAO: HE THONG DUNG KHAN CAP!\n\n"
            f"Thong tin chi tiet:\n"
            f"- Loi lien tiep: {current_consecutive}\n"
            f"- Nguong cai dat: {limit}\n"
            f"- So mach chuan: {ok_count}\n"
            f"- So mach loi: {ng_count}\n\n"
            f"He thong da dung khan cap - yeu cau kiem tra he thong."
        )
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = f"⚠️ STOP: Lỗi {current_consecutive} mạch liên tiếp"
        msg["From"] = EMAIL_GUI
        msg["To"] = EMAIL_NHAN

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_GUI, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Đã gửi mail báo cáo đầy đủ")
    except Exception as e:
        print("❌ Lỗi gửi mail:", e)


# ================= IMAGE PROCESSING =================
def rotate_image(img, angle, center):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def normalize_pcb(frame):
    if frame is None: return None

    # 1. Xử lý ảnh đầu vào
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, PCB_LOWER, PCB_UPPER)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 2. Tìm contour chính
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts: return None
    pcb = max(cnts, key=cv2.contourArea)
    if cv2.contourArea(pcb) < 8000: return None

    # =========================================================================
    # [LOGIC "AI" XỬ LÝ MỌI GÓC ĐỘ]
    # =========================================================================
    rect = cv2.minAreaRect(pcb)
    (cx, cy), (w, h), angle = rect
    if w > h:
        rotation_angle = angle + 90
    else:
        rotation_angle = angle

    # 3. Thực hiện xoay ảnh
    # Lưu ý: Xoay cả mask và frame để đảm bảo cắt chính xác
    rot_frame = rotate_image(frame, rotation_angle, (int(cx), int(cy)))
    rot_mask = rotate_image(mask, rotation_angle, (int(cx), int(cy)))

    # 4. Tìm lại contour sau khi xoay để cắt (Crop) cho đẹp
    # T sau khi xoay, hộp bao (BoundingRect) đã thay đổi.
    cnts2, _ = cv2.findContours(rot_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts2: return None

    pcb2 = max(cnts2, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(pcb2)

    # [QUAN TRỌNG] Kiểm tra lần cuối
    # Nếu sau khi xoay mà w vẫn > h (vẫn nằm ngang - do nhiễu hoặc lỗi)
    # Ta ép xoay crop bằng cách đảo chiều w, h (nhưng thường bước trên đã fix rồi)

    crop = rot_frame[y:y + h, x:x + w]

    # Resize về kích thước chuẩn để so sánh
    return cv2.resize(crop, (MASTER_W, MASTER_H), interpolation=cv2.INTER_AREA)


# Hàm phụ trợ xoay ảnh (Giữ nguyên hoặc dùng hàm này nếu chưa có)
def rotate_image(image, angle, center=None):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                          borderValue=(0, 0, 0))

def ssim_score(a, b):
    a = cv2.resize(a, (b.shape[1], b.shape[0]))
    score, _ = ssim(a, b, full=True)
    return score


def classify_by_data(crop_bgr):
    gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
    scores = {
        "DUT": max([ssim_score(gray, t) for t in ok_templates]) if ok_templates else 0,
        "KHUYET": max([ssim_score(gray, t) for t in ng_templates]) if ng_templates else 0,
        "PAD": max([ssim_score(gray, t) for t in lo_templates]) if lo_templates else 0
    }
    label = max(scores, key=scores.get)
    return label, scores[label]


def align_homography(src, dst):
    g1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(5000)
    k1, d1 = orb.detectAndCompute(g1, None)
    k2, d2 = orb.detectAndCompute(g2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(d1, d2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance: good.append(m)
    if len(good) < 4: raise RuntimeError("Không đủ match")
    pts1 = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts2 = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5)
    return H

def copper_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, (5, 50, 60), (35, 255, 255))

def inspect_and_collect(good_img, bad_img):
    try:
        H = align_homography(bad_img, good_img)
        h, w = good_img.shape[:2]
        bad_aligned = cv2.warpPerspective(bad_img, H, (w, h))
    except:
        bad_aligned = bad_img.copy()

    k3 = np.ones((3, 3), np.uint8)
    k5 = np.ones((5, 5), np.uint8)
    good_c = cv2.morphologyEx(copper_mask(good_img), cv2.MORPH_OPEN, k3)
    bad_c = cv2.morphologyEx(copper_mask(bad_aligned), cv2.MORPH_OPEN, k3)

    # [QUAN TRỌNG] Thay k5 thành k3 để không bị che mất lỗi dư chân pad
    good_expected = cv2.dilate(good_c, k3, 1)

    defect = cv2.bitwise_and(bad_c, cv2.bitwise_not(good_expected))
    defect = cv2.morphologyEx(defect, cv2.MORPH_CLOSE, k3, 2)

    # [KHÔI PHỤC] Tạo thư mục để lưu ảnh lỗi
    ts = time.strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(COLLECT_DIR, f"run_{ts}")
    os.makedirs(run_dir, exist_ok=True)

    out = bad_aligned.copy()
    cnts, _ = cv2.findContours(defect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defect_count = 0

    for c in cnts:
        # Chỉ dùng MIN_AREA
        if cv2.contourArea(c) < MIN_AREA: continue

        x, y, w, h = cv2.boundingRect(c)
        cw, ch = w + 2 * PAD, h + 2 * PAD
        cx, cy = x + w / 2, y + h / 2
        x1 = max(0, int(cx - cw / 2));
        y1 = max(0, int(cy - ch / 2))
        x2 = min(256, int(cx + cw / 2));
        y2 = min(477, int(cy + ch / 2))

        crop = bad_aligned[y1:y2, x1:x2]
        if crop.size == 0: continue

        label, score = classify_by_data(crop)
        if score < 0.7: continue

        defect_count += 1

        # [KHÔI PHỤC] Lưu ảnh lỗi vào thư mục
        cv2.imwrite(os.path.join(run_dir, f"crop_{defect_count:03d}_{label}_{score:.2f}.png"), crop)

        cv2.rectangle(out, (x1, y1), (x2, y2), LABEL_COLORS[label], 2)
        cv2.putText(out, f"{label} ", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, LABEL_COLORS[label], 2)

    return out, defect_count


# ================= SERIAL THREAD =================
class SerialThread(QtCore.QThread):
    sig_estop = QtCore.pyqtSignal()
    sig_reset_estop = QtCore.pyqtSignal()
    sig_capture = QtCore.pyqtSignal()

    def run(self):
        while True:
            if ser and ser.in_waiting:
                try:
                    raw = ser.readline()
                    cmd = raw.decode(errors="ignore").strip()
                    if cmd:
                        print(f"Arduino Gui: {cmd}")
                        if cmd == "E":
                            self.sig_estop.emit()
                        elif cmd == "T":
                            self.sig_reset_estop.emit()
                        elif cmd == "C":
                            self.sig_capture.emit()
                except Exception as e:
                    print("Serial Thread Err:", e)
            self.msleep(10)


class EmergencyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("🚨 DỪNG KHẨN CẤP")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        layout = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("HỆ THỐNG ĐANG DỪNG KHẨN CẤP!")
        lbl.setStyleSheet("color: red; font-size: 16px; font-weight: bold")
        layout.addWidget(lbl)
        self.setLayout(layout)
        self.resize(300, 100)


class WindowUI1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI1_Main()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(CAMERA_ID)

        if os.path.exists(GOOD_PATH):
            self.good_img = cv2.resize(cv2.imread(GOOD_PATH), (MASTER_W, MASTER_H))
        else:
            self.good_img = np.zeros((MASTER_H, MASTER_W, 3), dtype=np.uint8)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.count_ok = 0
        self.count_ng = 0
        self.consecutive_ng = 0
        self.ng_limit = 5
        self.emergency_box = None
        self.current_pcb = None

        self.ui.label_3.setText("0");
        self.ui.label_4.setText("0")
        self.ui.pushButton_4.clicked.connect(self.start_run)
        self.ui.pushButton_5.clicked.connect(self.stop_run)
        self.ui.pushButton_6.clicked.connect(self.open_ui2)
        self.ui.pushButton_7.clicked.connect(self.reset_counters)

        self.ui.label_3.installEventFilter(self)
        self.ui.label_4.installEventFilter(self)

        self.serial_th = SerialThread()
        self.serial_th.sig_estop.connect(self.show_estop)
        self.serial_th.sig_reset_estop.connect(self.hide_estop)
        self.serial_th.sig_capture.connect(self.process_capture)
        self.serial_th.start()
        print("✅ System Ready")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if source == self.ui.label_4:
                num, ok = QtWidgets.QInputDialog.getInt(self, "Cài đặt OK", "Nhập số lượng Mạch Đạt:", self.count_ok, 0,
                                                        99999)
                if ok:
                    self.count_ok = num
                    self.ui.label_4.setText(str(self.count_ok))
            elif source == self.ui.label_3:
                num, ok = QtWidgets.QInputDialog.getInt(self, "Cài đặt NG", "Nhập số lượng Mạch Lỗi:", self.count_ng, 0,
                                                        99999)
                if ok:
                    self.count_ng = num
                    self.ui.label_3.setText(str(self.count_ng))
        return super().eventFilter(source, event)

    def show_estop(self):
        if not self.emergency_box:
            self.emergency_box = EmergencyDialog(self)
            self.emergency_box.show()

    def hide_estop(self):
        if self.emergency_box:
            self.emergency_box.close()
            self.emergency_box = None

    def start_run(self):
        self.timer.start(30)
        if ser: ser.write(b"RUN\n")

    def stop_run(self):
        self.timer.stop()
        if ser: ser.write(b"STOP\n")

    def reset_counters(self):
        # Reset biến số về 0
        self.count_ok = 0
        self.count_ng = 0
        self.consecutive_ng = 0

        # Cập nhật giao diện ngay lập tức
        self.ui.label_3.setText("0")
        self.ui.label_4.setText("0")

        print("♻️ Đã Reset bộ đếm!")
    def process_capture(self):
        # -----------------------------------------------------------
        # CASE 1: ĐANG Ở UI2 (LẤY MẪU)
        # -----------------------------------------------------------
        if self.isHidden():
            # Arduino gửi 'C' báo có vật.
            # Yêu cầu: Băng tải phải dừng chờ nút bấm.
            # Hành động: KHÔNG GỬI GÌ CẢ. Để Arduino tiếp tục đứng đợi lệnh.
            print("⚠️ Đang ở UI2: Arduino đang dừng chờ người dùng bấm Chụp...")
            return

        # -----------------------------------------------------------
        # CASE 2: ĐANG Ở UI1 (CHẠY TỰ ĐỘNG) - GIỮ NGUYÊN
        # -----------------------------------------------------------
        if self.current_pcb is None:
            print("⚠️ Lỗi: Cảm biến kích hoạt nhưng không thấy PCB!")
            if ser: ser.write(b"NO\n")
            return

        print("📸 Bắt đầu xử lý (UI1)...")

        try:
            res_img, count = inspect_and_collect(self.good_img, self.current_pcb)
            self.show_img(res_img, self.ui.label_14)

            if count == 0:
                print("-> Kết quả: OK")
                if ser: ser.write(b"OK\n")
                self.count_ok += 1
                self.ui.label_4.setText(str(self.count_ok))
                self.consecutive_ng = 0
            else:
                print(f"-> Kết quả: NG ({count} lỗi)")
                self.count_ng += 1
                self.ui.label_3.setText(str(self.count_ng))
                self.consecutive_ng += 1

                limit = self.ui.spinBox.value()
                if self.consecutive_ng >= limit:
                    if ser: ser.write(b"STOP\n")
                    send_email_alert(self.count_ok, self.count_ng, self.consecutive_ng, limit)
                    self.show_ng_warning()
                    self.consecutive_ng = 0
                else:
                    if ser: ser.write(b"NO\n")

        except Exception as e:
            print("❌ Lỗi nghiêm trọng khi xử lý:", e)
            if ser: ser.write(b"NO\n")

    def show_ng_warning(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("⚠️ CẢNH BÁO")
        msg.setText(f"Phát hiện {self.consecutive_ng} PCB lỗi liên tục!\nVui lòng kiểm tra hệ thống.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return
        self.show_img(frame, self.ui.label_15)

        pcb = normalize_pcb(frame)
        if pcb is not None:
            self.current_pcb = pcb

    def show_img(self, img, lbl):
        if img is None: return
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        qimg = QtGui.QImage(rgb.data, w, h, c * w, QtGui.QImage.Format_RGB888)
        lbl.setPixmap(QtGui.QPixmap.fromImage(qimg).scaled(lbl.size(), QtCore.Qt.KeepAspectRatio))

    def open_ui2(self):
        self.timer.stop()
        self.cap.release()
        if ser: ser.write(b"LAY\n")

        self.ui2 = WindowUI2(self)
        self.ui2.show()

        # Ẩn UI1 đi để process_capture biết đường mà dừng
        self.hide()


# ================= UI2 =================
class WindowUI2(QtWidgets.QMainWindow):
    def __init__(self, main_ui):
        super().__init__()
        self.main_ui = main_ui
        self.ui = UI2_Main()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(CAMERA_ID)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.last_pcb = None
        self.ui.pushButton_8.clicked.connect(self.capture)
        self.ui.pushButton_9.clicked.connect(self.back)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return
        self.show_img(frame, self.ui.label_15)
        pcb = normalize_pcb(frame)
        if pcb is not None:
            self.last_pcb = pcb
            self.show_img(pcb, self.ui.label_14)

    def capture(self):
        if self.last_pcb is not None:
            # ==========================================================
            # 1. GỬI LỆNH ĐIỀU KHIỂN
            # ==========================================================
            if ser:
                # Bước 1: Gửi OK để Servo gạt mạch chuẩn
                ser.write(b"OK\n")
                print("UI2: Đã gửi OK -> Servo đang gạt...")

                # Bước 2: [QUAN TRỌNG] Hẹn giờ 1 giây sau tự gửi lệnh RUN để băng tải chạy tiếp
                # (Dùng QTimer để không làm đơ phần mềm)
                QtCore.QTimer.singleShot(1000, self.send_run_signal)

            # 2. LƯU ẢNH
            try:
                cv2.imwrite(GOOD_PATH, self.last_pcb)
                print(f"Đã lưu ảnh mẫu: {GOOD_PATH}")
            except Exception as e:
                print(f"Lỗi lưu ảnh: {e}")

            QtWidgets.QMessageBox.information(self, "Thành công", "Đã lưu mẫu chuẩn.\nBăng tải sẽ chạy lại sau 1 giây.")

        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chưa nhận diện được mạch!")

    # Hàm phụ để gửi lệnh RUN
    def send_run_signal(self):
        if ser:
            ser.write(b"RUN\n")
            print("UI2: Đã gửi lệnh RUN -> Băng tải chạy tiếp!")

    def show_img(self, img, lbl):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        qimg = QtGui.QImage(rgb.data, w, h, c * w, QtGui.QImage.Format_RGB888)
        lbl.setPixmap(QtGui.QPixmap.fromImage(qimg).scaled(lbl.size(), QtCore.Qt.KeepAspectRatio))

    def back(self):
        self.timer.stop()
        self.cap.release()
        if ser: ser.write(b"STOP\n")
        # Hiện lại UI1
        self.main_ui.show()
        self.main_ui.timer.start(30)
        self.main_ui.cap = cv2.VideoCapture(CAMERA_ID)

        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = WindowUI1()
    win.show()
    sys.exit(app.exec_())
