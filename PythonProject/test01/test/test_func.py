import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


def merge_lines(lines, angle_thresh=5, dist_thresh=20):
    """合并相近的直线（水平或垂直）"""
    if lines is None:
        return []

    # 提取直线端点并计算角度和中心点
    lines_info = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        lines_info.append({"angle": angle, "center": center, "line": line})

    # 分水平线和垂直线处理
    merged_lines = []
    for orientation in ["horizontal", "vertical"]:
        # 筛选当前方向的直线
        if orientation == "horizontal":
            subset = [line for line in lines_info if abs(line["angle"]) < angle_thresh]
            coord_idx = 1  # 水平线按 y 坐标聚类
        else:
            subset = [line for line in lines_info if abs(abs(line["angle"]) - 90) < angle_thresh]
            coord_idx = 0  # 垂直线按 x 坐标聚类

        if not subset:
            continue

        # 按中心点坐标聚类
        centers = np.array([line["center"][coord_idx] for line in subset]).reshape(-1, 1)
        clustering = DBSCAN(eps=dist_thresh, min_samples=1).fit(centers)

        # 合并同类直线
        for label in np.unique(clustering.labels_):
            group = [subset[i]["line"] for i in np.where(clustering.labels_ == label)[0]]
            # 取组内直线的平均端点
            x1_avg = int(np.mean([l[0][0] for l in group]))
            y1_avg = int(np.mean([l[0][1] for l in group]))
            x2_avg = int(np.mean([l[0][2] for l in group]))
            y2_avg = int(np.mean([l[0][3] for l in group]))
            merged_lines.append([[x1_avg, y1_avg, x2_avg, y2_avg]])

    return merged_lines


def get_crop_bounds(merged_lines):
    """获取裁剪边界（最外侧的水平和垂直线）"""
    horizontal_ys = []
    vertical_xs = []

    for line in merged_lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

        if abs(angle) < 5:  # 水平线
            horizontal_ys.extend([y1, y2])
        elif abs(abs(angle) - 90) < 5:  # 垂直线
            vertical_xs.extend([x1, x2])

    if not horizontal_ys or not vertical_xs:
        raise ValueError("未检测到足够的直线以形成网格！")

    y_min, y_max = min(horizontal_ys), max(horizontal_ys)
    x_min, x_max = min(vertical_xs), max(vertical_xs)
    return x_min, x_max, y_min, y_max

# 1. 读取图片
image_path = "test.jpg"
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError("图片未找到，请检查路径！")

# 2. 预处理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# 3. 检测直线
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
print("检测到的直线数量:", len(lines) if lines is not None else 0)

# 4. 合并直线并获取裁剪边界
x_min, x_max, y_min, y_max = get_crop_bounds(lines)
merged_lines = merge_lines(lines)
cropped_image = image[y_min:y_max, x_min:x_max]

# 5. 绘制合并后的直线并统计格子数量
horizontal_lines = []
vertical_lines = []
if merged_lines:
    for line in merged_lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        if abs(angle) < 5:  # 水平线
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            horizontal_lines.append(y1)
        elif abs(abs(angle) - 90) < 5:  # 垂直线
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            vertical_lines.append(x1)

# 6. 计算格子数量
rows = len(set(horizontal_lines)) - 1 if horizontal_lines else 0
cols = len(set(vertical_lines)) - 1 if vertical_lines else 0
print(f"网格行数: {rows}, 列数: {cols}")

# 7. 显示结果
plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(f"Merged Lines (Grid: {rows}x{cols})")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
plt.title(f"Cropped Merged Lines (Grid: {rows}x{cols})")
plt.axis('off')

plt.tight_layout()
plt.savefig("result_merged.jpg")
plt.show()