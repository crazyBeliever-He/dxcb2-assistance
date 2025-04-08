import threading
from core.process_capture import ProcessCapture

class ThreadManager:
    def __init__(self):
        self.capture_thread = None
        self.process_capture = None

    def start_capture(self, process_name):
        if self.capture_thread and self.capture_thread.is_alive():
            return

        self.process_capture = ProcessCapture(process_name)
        self.capture_thread = threading.Thread(target=self.process_capture.run)
        self.capture_thread.start()

    def pause_capture(self):
        if self.process_capture:
            self.process_capture.pause()

    def stop_capture(self):
        if self.process_capture:
            self.process_capture.stop()  # 设置停止标志
            if self.capture_thread and self.capture_thread.is_alive():
                self.capture_thread.join(timeout=1.0)  # 等待线程结束（超时1秒）
                if self.capture_thread.is_alive():  # 如果线程仍未停止
                    self.capture_thread = None  # 强制释放资源
        self.process_capture = None  # 清理实例