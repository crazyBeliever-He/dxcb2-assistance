import cv2
import time
from utils import get_image_from_process

def read_images_from_process(interval=1/3):
    while True:
        image = get_image_from_process()
        if image is not None:
            # 在这里添加图像处理逻辑
            cv2.imshow('Process Output', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(interval)

    cv2.destroyAllWindows()