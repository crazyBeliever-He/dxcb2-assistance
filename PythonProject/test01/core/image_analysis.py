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


    # print(type(image))  # 输出类型（如 <class 'PIL.Image.Image'>）
    # print(dir(image))  # 查看对象可用方法和属性

    save_image(image, "output.png")

    # 使用OCR
    # 将PIL Image转为numpy数组（RGB格式）
    image_np = np.array(image)  # shape: (height, width, 3)

    """
    PaddleOCR 识别结果数据结构说明:

    整体结构:
      - 返回结果是一个列表，每个元素对应一张输入图片的识别结果（单图片输入时只需关注result[0]）
      - 每张图片的识别结果是一个包含多个文本框信息的列表

    文本框数据结构:
      [
          [
              [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],  # 文本框四边形坐标点
                                                      # 顺序：左上→右上→右下→左下
              (
                  "识别文本",    # 识别出的文字内容
                  置信度        # float类型，范围0-1，表示识别准确度
              )
          ],
          ...  # 更多文本框
      ]

    示例数据:
    [
        [  # 第一张图片结果
            [[[10,20],[100,20],[100,50],[10,50]], ("你好", 0.98)],
            [[[15,60],[90,60],[90,80],[15,80]], ("世界", 0.95)],
        ]
    ]

    使用提示:
    1. 访问单张图片结果: result[0]
    2. 获取第i个文本框: result[0][i]
    3. 获取文本框坐标: result[0][i][0]
    4. 获取识别文本: result[0][i][1][0]
    5. 获取置信度: result[0][i][1][1]
    """
    result = ocr.ocr(image_np)
    for line in result[0]:
        text = line[1][0]  # line[1] = ("文本", 置信度), line[1][0] 就是文本内容
        print(text)

