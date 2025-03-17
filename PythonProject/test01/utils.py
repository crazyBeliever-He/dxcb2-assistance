# utils.py
import pygetwindow as gw
from PIL import ImageGrab

def get_image_from_process(process_name):
    try:
        # 根据进程名查找窗口
        window = gw.getWindowsWithTitle(process_name)[0]
        if window:
            # 如果窗口被最小化，则恢复窗口
            if window.isMinimized:
                window.restore()
            # 获取窗口的边界框
            bbox = (window.left, window.top, window.right, window.bottom)
            # 截取图像
            image = ImageGrab.grab(bbox)
            return image
    except IndexError:
        print(f"未找到标题为: {process_name} 的窗口")
    except Exception as e:
        print(f"发生错误: {e}")
    return None