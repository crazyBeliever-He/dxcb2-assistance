import threading
from core.capture_screenshot import CaptureWindows

class ThreadManager:
    def __init__(self):
        # capture_thread 是一个 线程对象（threading.Thread），它的核心作用是 让 ProcessCapture 的任务在后台独立运行，避免阻塞主线程。
        self.capture_thread = None
        self.capture_windows = None

    def start_capture(self, process_name, function_id):
        if self.capture_thread and self.capture_thread.is_alive():
            return

        self.capture_windows = CaptureWindows(process_name, function_id)
        self.capture_thread = threading.Thread(target=self.capture_windows.run)
        self.capture_thread.start() # 任务在子线程中运行，主线程不受阻塞

    def stop_capture(self):
        if self.capture_windows:
            self.capture_windows.stop()
            if self.capture_thread:
                self.capture_thread.join(timeout=2.0)
                if self.capture_thread.is_alive():
                    print("警告：线程未正常停止，尝试强制清理")
                    # 强制释放资源
                    from utils.image_utils import release_ocr
                    release_ocr()
                    self.capture_thread = None
            self.capture_windows = None