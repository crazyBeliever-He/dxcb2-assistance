from PIL import Image
from utils.file_utils import save_image

def analyze_image(image):
    # 这里可以添加图像分析逻辑
    save_image(image, "output.png")
    print("Analyzing image...")
    # 示例：获取图像尺寸
    width, height = image.size
    print(f"Image size: {width}x{height}")