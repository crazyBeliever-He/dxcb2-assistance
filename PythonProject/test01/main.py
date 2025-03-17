import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from process_image import read_images_from_process

def on_click():
    QMessageBox.information(window, "提示", "开始读取图像")
    read_images_from_process()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('图像处理App')
window.setGeometry(300, 300, 300, 200)

btn = QPushButton('开始', window)
btn.clicked.connect(on_click)
btn.move(100, 80)

window.show()
sys.exit(app.exec_())