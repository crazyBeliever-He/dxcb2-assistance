# main.py
import sys
import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog
from process_image import read_images_from_process, stop_flag

class ImageThread(QThread):
    def __init__(self, process_name):
        super().__init__()
        self.process_name = process_name

    def run(self):
        read_images_from_process(self.process_name)

def on_click():
    global image_thread
    QMessageBox.information(window, "提示", "开始读取图像")
    start_button.setEnabled(False)
    stop_button.setEnabled(True)
    image_thread = ImageThread(process_name)
    image_thread.start()

def on_stop():
    global stop_flag
    stop_flag = True
    QMessageBox.information(window, "提示", "停止读取图像")
    start_button.setEnabled(True)
    stop_button.setEnabled(False)

def on_close():
    global stop_flag
    stop_flag = True
    QMessageBox.information(window, "提示", "关闭应用程序")
    app.quit()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('图像处理App')
window.setGeometry(300, 300, 300, 200)

# 弹出输入对话框获取进程名
process_name, ok = QInputDialog.getText(window, "输入进程名", "请输入进程名:")
if not ok or not process_name:
    QMessageBox.critical(window, "错误", "进程名不能为空")
    sys.exit()

start_button = QPushButton('开始', window)
start_button.clicked.connect(on_click)
start_button.move(100, 80)

stop_button = QPushButton('停止', window)
stop_button.clicked.connect(on_stop)
stop_button.move(100, 120)
stop_button.setEnabled(False)

close_button = QPushButton('关闭', window)
close_button.clicked.connect(on_close)
close_button.move(100, 160)

window.show()
sys.exit(app.exec_())