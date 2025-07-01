import os
import threading

from paddleocr import PaddleOCR

model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

# 全局OCR实例和锁
_ocr = None
"""
PaddleOCR 识别结果数据结构说明:
------------------------------------------------------------
整体结构:
  - 返回结果是一个列表，每个元素对应一张输入图片的识别结果
  - 单图片输入时只需关注 result[0]

文本框数据结构:
  [
      [
          [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],  # 文本框坐标,顺序：左上→右上→右下→左下
          ("识别文本", 置信度)                      # 文本和置信度
      ],
      ...  # 更多文本框
  ]
------------------------------------------------------------
"""
_ocr_init_lock = threading.Lock()
def init_ocr():
    """
    初始化OCR实例，使用惰性加载方式
    :return: OCR实例
    """
    global _ocr
    with _ocr_init_lock:
        if _ocr is None:
            print("正在初始化OCR实例...")
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