# 忽略ccache相关的警告
import warnings
warnings.filterwarnings("ignore", message="No ccache found")



from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QButtonGroup, QFrame, \
    QRadioButton

from core.thread_manager import ThreadManager



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.other_radio = None
        self.record_radio = None
        self.capture_radio = None
        self.function_group = None
        self.status_label = None
        self.stop_button = None
        self.start_button = None
        self.process_name_input = None
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
        self.process_name_input.setPlaceholderText("输入进程名...")
        layout.addWidget(self.process_name_input)

        # === 新增功能选择部分 ===
        # 功能选择标签
        function_label = QLabel("选择功能:", self)
        layout.addWidget(function_label)

        # 功能选择单选按钮组
        self.function_group = QButtonGroup(self)

        # 功能1: 截图
        self.capture_radio = QRadioButton("刷酒馆", self)
        self.capture_radio.setChecked(True)  # 默认选中
        self.function_group.addButton(self.capture_radio, 1)
        layout.addWidget(self.capture_radio)

        # 功能2: 录制
        self.record_radio = QRadioButton("刷战利品龙骨", self)
        self.function_group.addButton(self.record_radio, 2)
        layout.addWidget(self.record_radio)

        # 功能3: 其他功能
        self.other_radio = QRadioButton("其他功能", self)
        self.function_group.addButton(self.other_radio, 3)
        layout.addWidget(self.other_radio)

        # 添加一个水平线分隔
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        # === 结束功能选择部分 ===

        # 开始按钮
        self.start_button = QPushButton("开始", self)
        self.start_button.clicked.connect(self.start_capture)
        layout.addWidget(self.start_button)

        # 暂停按钮
        # self.pause_button = QPushButton("Pause", self)
        # self.pause_button.clicked.connect(self.pause_capture)
        # layout.addWidget(self.pause_button)

        # 结束按钮
        self.stop_button = QPushButton("结束", self)
        self.stop_button.clicked.connect(self.stop_capture)
        layout.addWidget(self.stop_button)

        # 状态标签
        self.status_label = QLabel("状态: 挂起", self)
        layout.addWidget(self.status_label)

        # 设置主布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_capture(self):
        process_name = self.process_name_input.text()
        if process_name:
            # 获取选中的功能ID
            selected_function = self.function_group.checkedId()
            # 将功能ID和进程名一起传递给线程管理器
            self.thread_manager.start_capture(process_name, function_id=selected_function)
            self.status_label.setText("状态: 运行中 - " +
                                      ["刷酒馆", "战利品龙骨", "其他"][selected_function - 1])


    def stop_capture(self):
        self.thread_manager.stop_capture()
        self.status_label.setText("状态: 停止")

