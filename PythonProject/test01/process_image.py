# process_image.py
import cv2
import time
from utils import get_image_from_process

stop_flag = False

def read_images_from_process(process_name, interval=1/3):
    global stop_flag
    while not stop_flag:
        image = get_image_from_process(process_name)
        if image is not None:
            # 在这里添加图像处理逻辑
            cv2.imshow('Process Output', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(interval)

    cv2.destroyAllWindows()