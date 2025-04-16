import threading
import time

from utils.image_utils import capture_window
from utils.orc_utils import release_ocr
from .image_analysis import analyze_image


class ProcessCapture:
    def __init__(self, process_name):
        self.process_name = process_name
        self.is_running = True
        self.is_paused = False
        self.lock = threading.Lock()
        self.ocr_lock = threading.Lock()  # OCR专用锁

    def run(self):
        try:
            while self.is_running:
                with self.lock:
                    if not self.is_paused:
                        # 截图并处理
                        screenshot = capture_window(self.process_name)
                        if screenshot:
                            self.process_image(screenshot)
                time.sleep(1)
        except Exception as e:
            print(f"捕获线程异常: {e}")
        finally:
            try:
                release_ocr()
            except Exception as e:
                print(f"释放资源时出错: {e}")

    def process_image(self, image):
        """
        处理截图并进行OCR分析.核心功能函数
        :param image: 截图图像
        :return: None
        """
        with self.ocr_lock:  # 加锁保护OCR调用
            if image:
                analyze_image(image)
                print(f"Processing image for process: {self.process_name}")

    def stop(self):
        self.is_running = False