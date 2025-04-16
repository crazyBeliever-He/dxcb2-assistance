import os
import threading

from paddleocr import PaddleOCR

model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

# 全局OCR实例和锁
_ocr = None
_ocr_init_lock = threading.Lock()

def init_ocr():
    """
    初始化OCR实例，使用惰性加载方式
    :return: OCR实例
    """
    global _ocr
    with _ocr_init_lock:
        if _ocr is None:
            _ocr = PaddleOCR(
                use_gpu=False,
                det_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_det_infer"),
                rec_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_rec_infer"),
                cls_model_dir=os.path.join(model_dir, "ch_ppocr_mobile_v2.0_cls"),
                lang='ch'
            )
    return _ocr

def release_ocr():
    """
    释放OCR资源,ORC是文字识别器
    :return: None
    """
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