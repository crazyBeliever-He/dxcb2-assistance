import numpy as np
import pyautogui
from utils.image_utils import save_image, advanced_random_generator, capture_window
from utils.orc_utils import init_ocr, find_text_index

"""TODO: 后面改用别的不影响用户使用鼠标的包"""


def analyze_image_42botty(process_name):
    ocr = init_ocr()  # 惰性初始化   OCR 实例在首次使用时创建（init_ocr()），而非模块加载时创建
    # 1.出征
    # 2.跑图，打怪
    # 3.回城
    # 4.切换队伍（如果需要


def analyze_image_bar(process_name, stop_event=None):
    ocr = init_ocr()  # 惰性初始化   OCR 实例在首次使用时创建（init_ocr()），而非模块加载时创建
    count = 0
    while True:
        if stop_event and stop_event.is_set():  # 检查外部停止信号
            print("收到停止信号，退出循环")
            return 0
        # 截图
        screenshot, screen_coordinate = capture_window(process_name)
        # 文字识别的结果
        result = ocr.ocr(screenshot)
        index = None
        text = None
        bbox = None
        # 处理截图信息
        # TODO: 画一个流程图，根据流程图实现代码

    # # 酒馆是否已满
    # index, text, bbox = find_text_index(result[0], "潜能 ：SS")
    # # 招募SS
    # if index is None:
    #
    # # 循环刷新酒馆
    # else:
    #     if analyze_call_count > 2:
    #         if analyze_call_count % 2 == 0:
    #             index, text, bbox = find_text_index(result[0], "换一批")
    #         else:
    #             index, text, bbox = find_text_index(result[0], "使用金币快速刷新")
    #     elif analyze_call_count == 2:
    #         index, text, bbox = find_text_index(result[0], "新人招募")
    #     elif analyze_call_count == 1:
    #         index, text, bbox = find_text_index(result[0], "酒馆")
    #         if index is not None:
    #             # 在屏幕坐标上添加随机偏移量
    #             random_x = advanced_random_generator(bbox[0], bbox[2])
    #             random_y = advanced_random_generator(bbox[1], bbox[3])
    #             pyautogui.moveTo(screen_coordinate[0] + random_x , screen_coordinate[1] + random_y +
    #                              advanced_random_generator(20, 100))
    #             # 在当前位置点击
    #             pyautogui.click()
    #             print("点击坐标:",screen_coordinate[0] + random_x , screen_coordinate[1] + random_y)
    #             return analyze_call_count + 1
    #         # 未找到目标时抛出异常
    #         raise ValueError("刷新酒馆步骤1：未找到酒馆文本，无法点击")
    #     else:
    #         raise ValueError(f"刷新酒馆步骤{analyze_call_count}：错误的调用次数，无法继续分析")
    #
    # if index is not None:
    #     # 在屏幕坐标上添加随机偏移量
    #     random_x = advanced_random_generator(bbox[0], bbox[2])
    #     random_y = advanced_random_generator(bbox[1], bbox[3])
    #     pyautogui.moveTo(screen_coordinate[0] + random_x,screen_coordinate[1] + random_y)
    #     # 在当前位置点击
    #     pyautogui.click()
    #     print("点击坐标:", screen_coordinate[0] + random_x, screen_coordinate[1] + random_y)
    #     return analyze_call_count + 1
    # raise ValueError(f"刷新酒馆步骤{analyze_call_count}：未找到指定文本，无法点击")
