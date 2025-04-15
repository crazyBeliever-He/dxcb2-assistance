import os

import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from PIL import Image

def save_image(image, file_path):
    """保存图像到文件"""
    image.save(file_path)
    print(f"Image saved to {file_path}")

def capture_window(window_title):
    # 查找窗口句柄
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:

        raise Exception(f"Window '{window_title}' not found!")

    # 获取窗口位置和大小
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # 获取窗口设备上下文
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # 创建位图对象
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)

    # 将位图选入设备上下文
    save_dc.SelectObject(save_bitmap)

    # 复制窗口内容到位图
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

    # 将位图转换为 PIL 图像
    bmp_info = save_bitmap.GetInfo()
    bmp_str = save_bitmap.GetBitmapBits(True)
    image = Image.frombuffer(
        "RGB",
        (bmp_info["bmWidth"], bmp_info["bmHeight"]),
        bmp_str,
        "raw",
        "BGRX",
        0,
        1,
    )

    # 释放资源
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return image



