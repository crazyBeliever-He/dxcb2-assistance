import threading
import time

from utils.image_utils import capture_window, advanced_random_generator
from utils.orc_utils import release_ocr
from .image_analysis import analyze_image_42botty, analyze_image_bar

class CaptureWindows:
    def __init__(self, process_name, function_id):
        self.process_name = process_name
        self.function_id = function_id  # 存储功能ID
        self.stop_event = threading.Event()  # 线程安全的事件标志
        self.lock = threading.Lock()
        self.ocr_lock = threading.Lock()  # OCR专用锁

    def run(self):
        try:
            while not self.stop_event.is_set():  # 检查停止标志
                with self.lock:
                    with self.ocr_lock:
                        # 根据 function_id 执行不同操作
                        if self.function_id == 1:  # 酒馆
                            analyze_image_bar(self.process_name, stop_event=self.stop_event)
                            print(f"酒馆招募: {self.process_name}")
                        elif self.function_id == 2:  # 战利品龙骨
                            analyze_image_42botty(self.process_name)
                            print(f"战利品龙骨: {self.process_name}")
                        elif self.function_id == 3:  # 其他功能
                            # 执行其他分析，有需要就补全
                            print(f"执行其他分析: {self.process_name}")
                        else:
                            print(f"未知功能ID: {self.function_id}")
        except Exception as e:
            print(f"捕获线程异常: {e}")
        finally:
            try:
                release_ocr()
            except Exception as e:
                print(f"释放资源时出错: {e}")

    def stop(self):
        self.stop_event.set()  # 触发停止标志