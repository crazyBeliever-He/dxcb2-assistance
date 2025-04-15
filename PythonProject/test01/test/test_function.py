import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取图片
image_path = "test01.jpg"  # 替换为你的图片路径
image = cv2.imread(image_path)  # 替换为你的图片路径
if image is None:
    raise FileNotFoundError("图片未找到，请检查路径！")

# 2. 转为灰度图 + 高斯模糊降噪
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. 自适应阈值二值化（减弱亮斑影响）
thresh = cv2.adaptiveThreshold(
    blurred, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 11, 2
)

# 4. Canny边缘检测
edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# 5. Hough变换检测直线
lines = cv2.HoughLinesP(
    edges, 1, np.pi / 180,
    threshold=100,
    minLineLength=100,
    maxLineGap=10
)

# 6. 绘制检测到的水平线和垂直线
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi  # 计算角度
        print("angle = ", angle)

        # 只保留水平线（角度接近0°或180°）和垂直线（角度接近90°或-90°）
        if abs(angle) < 5:  # 水平线
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 红色
        elif abs(abs(angle) - 90) < 5:  # 垂直线
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色

# 7. 显示结果（适用于 headless 环境）
plt.figure(figsize=(12, 6))

# 显示原始图片
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

# 显示检测结果
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected Lines (Red: Horizontal, Green: Vertical)")
plt.axis('off')

plt.tight_layout()
plt.savefig("result.jpg")  # 保存结果
plt.show()

# 8. 打印统计信息
print(f"检测到线段数量: {len(lines) if lines is not None else 0}")