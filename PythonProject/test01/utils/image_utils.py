import random

import win32con
import win32gui
import win32ui
from PIL import Image


def advanced_random_generator(lower, upper, *, mode='int', precision=2, count=1):
    """
    高级随机数生成器,未指定则生成一个整数。前两个为位置参数，后面三个为关键字参数

    参数:
        lower: 下限
        upper: 上限
        mode: 生成模式 ('int' 或 'float')
        precision: 浮点数精度（仅mode=float时有效）
        count: 生成随机数的数量

    返回:
        当count=1时返回单个随机数，否则返回列表
    """
    if lower >= upper:
        raise ValueError("下限必须小于上限")

    if mode not in ['int', 'float']:
        raise ValueError("模式必须是int或float")

    if count < 1:
        raise ValueError("生成数量必须大于0")

    def generate():
        if mode == 'int':
            return random.randint(lower, upper)
        else:
            num = random.uniform(lower, upper)
            return round(num, precision)

    if count == 1:
        return generate()
    else:
        return [generate() for _ in range(count)]

def save_image(image, file_path):
    """保存图像"""
    image.save("image/"+file_path)
    print(f"Image saved to image/{file_path}")

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

    return image,[left, top, right, bottom]



