import threading
import time

from utils.image_utils import capture_window, advanced_random_generator
from utils.orc_utils import release_ocr
from .image_analysis import analyze_image_42botty, analyze_image_bar

class CaptureWindows:
    def __init__(self, process_name):
        self.process_name = process_name
        self.is_running = True
        self.lock = threading.Lock()
        self.ocr_lock = threading.Lock()  # OCR专用锁

    def run(self):
        try:
            while self.is_running:
                with self.lock:
                    # 截图并处理
                    screenshot,screen_coordinate = capture_window(self.process_name)
                    if screenshot:
                        self.process_image(screenshot, screen_coordinate)
                time.sleep(advanced_random_generator(0.8, 1.8, mode='float'))  # 随机延时，避免过于频繁的截图
        except Exception as e:
            print(f"捕获线程异常: {e}")
        finally:
            try:
                release_ocr()
            except Exception as e:
                print(f"释放资源时出错: {e}")

    def process_image(self, image, screen_coordinate):
        """
        处理截图并进行OCR分析.核心功能函数
        :param screen_coordinate: 程序窗口的屏幕坐标
        :param image: 截图图像
        :return: None
        """
        with self.ocr_lock:  # 加锁保护OCR调用(with自动释放锁)
            if image:
                """TODO: 根据不同的参数调用不同的分析函数"""
                analyze_image_bar(image, screen_coordinate)
                print(f"Processing image for process: {self.process_name}")

    def stop(self):
        self.is_running = False