import win32con
import win32gui
import win32ui
from PIL import Image

def save_image(image, file_path):
    """保存图像"""
    image.save(file_path)
    print(f"Image saved to {file_path}")

def cut_image(image, left, top, right, bottom):
    """
    裁剪图像
    :param image: PIL 图像对象
    :param left: 裁剪区域左边界
    :param top: 裁剪区域上边界
    :param right: 裁剪区域右边界
    :param bottom: 裁剪区域下边界
    :return: 裁剪后的图像
    """

    return image.crop((left, top, right, bottom))

def capture_window(window_title):
    """
    捕获指定窗口的图像并返回 PIL 图像对象
    :param window_title: 窗口标题
    :return:   PIL 图像对象
    """
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



