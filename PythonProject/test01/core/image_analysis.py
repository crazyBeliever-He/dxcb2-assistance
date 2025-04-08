from PIL import Image
from utils.file_utils import save_image
from paddleocr import PaddleOCR
import os

model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

ocr = PaddleOCR(
    det_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_det_infer"), # 固定检测模型
    rec_model_dir=os.path.join(model_dir, "ch_PP-OCRv4_rec_infer"), # 固定识别模型
    cls_model_dir=os.path.join(model_dir, "ch_ppocr_mobile_v2.0_cls"),  # 固定分类模型（可选）
    lang='ch'
)

def analyze_image(image):
    # 这里可以添加图像分析逻辑
    save_image(image, "output.png")
    print("Analyzing image...")
    # 示例：获取图像尺寸
    width, height = image.size
    print(f"Image size: {width}x{height}")

    # 使用OCR
    result = ocr.ocr("output.png")
    print("txt:",result)
    # for line in result:
    #     print("识别文本:",line[1][0])  # 打印识别文本

