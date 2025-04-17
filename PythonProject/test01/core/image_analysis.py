import numpy as np
import pyautogui
from utils.image_utils import save_image, advanced_random_generator
from utils.orc_utils import init_ocr


def analyze_image_42botty(image, screen_coordinate):
    ocr = init_ocr()  # 惰性初始化   OCR 实例在首次使用时创建（init_ocr()），而非模块加载时创建
    save_image(image, "output.png") # 保存图片
    image_np = np.array(image)   # 将PIL Image转为numpy数组（RGB格式）
    if image_np.dtype != np.uint8:
        image_np = image_np.astype(np.uint8)

    print("screen_coordinate:", screen_coordinate)
    result = ocr.ocr(image_np)
    if result:
        for line in result[0]:
            print("coordinate:",line[0][0], line[0][1], line[0][2], line[0][3])
            print(line[1][0])
    # 1.出征
    # 2.跑图，打怪
    # 3.回城
    # 4.切换队伍（如果需要


def analyze_image_bar(image, screen_coordinate):
    ocr = init_ocr()  # 惰性初始化   OCR 实例在首次使用时创建（init_ocr()），而非模块加载时创建
    image_np = np.array(image)  # 将PIL Image转为numpy数组（RGB格式）
    if image_np.dtype != np.uint8:
        image_np = image_np.astype(np.uint8)

    result = ocr.ocr(image_np)
    index, text, bbox = find_text_index(result[0], "酒馆")
    if index is not None:
        # 在屏幕坐标上添加随机偏移量
        random_x = advanced_random_generator(bbox[0], bbox[2], mode="float")
        random_y = advanced_random_generator(bbox[1], bbox[3], mode="float")
        pyautogui.moveTo(screen_coordinate[0] + random_x + 5 , screen_coordinate[1] + random_y + 5, duration=1)
        # 在当前位置点击
        pyautogui.click()
        print("点击坐标:",screen_coordinate[0] + random_x , screen_coordinate[1] + random_y)


def find_text_index(ocr_result, target_text):
    """
    在OCR结果中查找包含目标文本的条目

    参数:
        ocr_result: OCR识别结果 (result[0])
        target_text: 要查找的文本

    返回:
        如果找到则返回(index, text, bbox)，否则返回(None, None, None)
        bbox格式: [左上x, 左上y, 右下x, 右下y]
    """
    if not ocr_result:
        return None, None, None

    for idx, item in enumerate(ocr_result):
        text = item[1][0]  # 获取识别文本
        if target_text in text:
            # 提取文本框坐标并转换为(x1,y1,x2,y2)格式
            bbox = [
                item[0][0][0],  # 左上x
                item[0][0][1],  # 左上y
                item[0][2][0],  # 右下x
                item[0][2][1]  # 右下y
            ]
            return idx, text, bbox

    return None, None, None