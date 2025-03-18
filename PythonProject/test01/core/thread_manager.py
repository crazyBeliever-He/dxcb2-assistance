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
            self.process_capture.stop()
            if self.capture_thread:
                self.capture_thread.join()