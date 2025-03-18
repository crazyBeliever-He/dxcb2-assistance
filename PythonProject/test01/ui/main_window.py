from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal
from core.thread_manager import ThreadManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Process Image Capture")
        self.setGeometry(100, 100, 400, 300)

        # 初始化 UI
        self.initUI()

        # 初始化线程管理器
        self.thread_manager = ThreadManager()

    def initUI(self):
        # 主布局
        layout = QVBoxLayout()

        # 进程名输入框
        self.process_name_input = QLineEdit(self)
        self.process_name_input.setPlaceholderText("Enter process name...")
        layout.addWidget(self.process_name_input)

        # 开始按钮
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_capture)
        layout.addWidget(self.start_button)

        # 暂停按钮
        # self.pause_button = QPushButton("Pause", self)
        # self.pause_button.clicked.connect(self.pause_capture)
        # layout.addWidget(self.pause_button)

        # 结束按钮
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_capture)
        layout.addWidget(self.stop_button)

        # 状态标签
        self.status_label = QLabel("Status: Idle", self)
        layout.addWidget(self.status_label)

        # 设置主布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_capture(self):
        process_name = self.process_name_input.text()
        if process_name:
            self.thread_manager.start_capture(process_name)
            self.status_label.setText("Status: Running")

    # def pause_capture(self):
    #     self.thread_manager.pause_capture()
    #     self.status_label.setText("Status: Paused")

    def stop_capture(self):
        self.thread_manager.stop_capture()
        self.status_label.setText("Status: Stopped")