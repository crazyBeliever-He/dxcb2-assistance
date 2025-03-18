import time
import threading

import cv2
from PIL import ImageGrab
from .image_analysis import analyze_image
from utils.file_utils import capture_window

class ProcessCapture:
    def __init__(self, process_name):
        self.process_name = process_name
        self.is_running = False
        self.is_paused = False
        self.lock = threading.Lock()

    def run(self):
        self.is_running = True
        while self.is_running:
            with self.lock:
                if not self.is_paused:
                    # 捕获图像并处理
                    screenshot = capture_window(self.process_name)
                    self.process_image(screenshot)
            time.sleep(1)

    def process_image(self, image):
        # 这里可以添加图像分析逻辑
        if image:
            analyze_image(image)
            print(f"Processing image for process: {self.process_name}")

    def pause(self):
        with self.lock:
            self.is_paused = True

    def resume(self):
        with self.lock:
            self.is_paused = False

    def stop(self):
        self.is_running = False