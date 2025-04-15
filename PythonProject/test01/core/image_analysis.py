import numpy as np
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
    # print()
    # print(type(image))  # 输出类型（如 <class 'PIL.Image.Image'>）
    # print(dir(image))  # 查看对象可用方法和属性
    # print()


    save_image(image, "output.png")
    # print("Analyzing image...")
    # # 示例：获取图像尺寸
    # width, height = image.size
    # print(f"Image size: {width}x{height}")

    # 使用OCR
    # 将PIL Image转为numpy数组（RGB格式）
    image_np = np.array(image)  # shape: (height, width, 3)
    result = ocr.ocr(image_np)
    print("txt:",result)
    # for line in result:
    #     print("识别文本:",line[1][0])  # 打印识别文本

