import os
import threading

import numpy as np
from paddleocr import PaddleOCR

from utils.file_utils import save_image

model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

# 全局OCR实例和锁
_ocr = None
_ocr_init_lock = threading.Lock()

def init_ocr():
    global _ocr
    with _ocr_init_lock:
        if _ocr is None:
            _ocr = PaddleOCR(
                use_gpu=False,
                det_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_det_infer"),
                rec_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_rec_infer"),
                lang='ch'
            )
    return _ocr

def release_ocr():
    global _ocr
    if _ocr is not None:
        # PaddlePaddle的清理方式
        try:
            # 释放检测器资源
            if hasattr(_ocr, 'text_detector') and hasattr(_ocr.text_detector, 'predictor'):
                del _ocr.text_detector.predictor
            # 释放识别器资源
            if hasattr(_ocr, 'text_recognizer') and hasattr(_ocr.text_recognizer, 'predictor'):
                del _ocr.text_recognizer.predictor
        except Exception as e:
            print(f"释放OCR资源时出错: {e}")
        finally:
            _ocr = None


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