import numpy as np

from utils.image_utils import save_image
from utils.orc_utils import init_ocr


def analyze_image(image):
    ocr = init_ocr()  # 惰性初始化   OCR 实例在首次使用时创建（init_ocr()），而非模块加载时创建
    save_image(image, "output.png") # 保存图片
    image_np = np.array(image)   # 将PIL Image转为numpy数组（RGB格式）
    if image_np.dtype != np.uint8:
        image_np = image_np.astype(np.uint8)

    result = ocr.ocr(image_np)
    if result:
        for line in result[0]:
            print(line[1][0])