import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # 创建应用
    app = QApplication(sys.argv)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()