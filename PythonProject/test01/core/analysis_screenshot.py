import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from utils.image_utils import crop_center_square

def process_image(image):
    """
    处理输入图像，检测并合并直线，裁剪为最小方格
    :param image: 输入图像
    :return: 合并后的直线列表
    """
    # 1. 图像预处理
    if image is None:
        raise ValueError("图片未找到")
    image = crop_center_square(image)   # 裁剪为中心正方形

    # 2. 边缘检测的预处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # 高斯模糊
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 11, 2) # 自适应阈值处理
    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)  # 边缘检测

    # 3. 检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is None:
        raise ValueError("未检测到任何直线")

    # 4. 合并直线并获取裁剪边界
    merged_lines = merge_lines(lines)
    cell = crop_image(image, merged_lines)

    # 5. 绘制并显示结果
    visualize_lines(image.copy(), merged_lines)

    # TODO: 已经可以裁剪，下一步是对比最小方格与目标方格，绘制二维矩阵信息，并正确识别每个方格的坐标（重点，要简单），用于接下来的避障算法使用

def merge_lines(lines, angle_thresh=1, dist_thresh=20):
    """
    合并相近的直线
    :param lines: 输入直线集合
    :param angle_thresh: 角度阈值（度）,用于判断水平/垂直线的容忍范围,建议输入值为图像尺寸的 1%~2%（如 1000px 宽的图用 10~20px）
    :param dist_thresh: 距离阈值（像素）,用于判断直线是否相近
    :return: {  [[x1, y1, x2, y2]]
        'horizontal': 水平线列表,
        'vertical': 垂直线列表,
        'merged': 所有合并后的直线(水平和垂直线)
    }
    """
    if lines is None:
        return []

    # 1. 提取直线特征信息
    lines_info = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi  # 计算直线角度（度）
        center = ((x1 + x2) // 2, (y1 + y2) // 2)   # 计算直线中心点坐标
        lines_info.append({
            "angle": angle,  # 直线角度（度）
            "center": center,  # 直线中心点坐标
            "line": line  # 原始直线数据
        })

    # 2. 分别处理水平线和垂直线
    result_lines = {'horizontal': [], 'vertical': [], 'merged': []}

    # 定义方向处理配置（水平/垂直）
    orientation_config = [  # 外层列表，内层字典
        {
            "name": "horizontal",
            "angle_condition": lambda a: abs(a) < angle_thresh,
            "cluster_coord": 1  # 水平线,使用y坐标聚类
        },
        {
            "name": "vertical",
            "angle_condition": lambda a: abs(abs(a) - 90) < angle_thresh,# 匿名函数
            "cluster_coord": 0  # 垂直线,使用x坐标聚类
        }
    ]
    for config in orientation_config:
        # 筛选当前方向的直线(水平或垂直)
        subset = [line for line in lines_info
                  if config["angle_condition"](line["angle"])]
        if not subset:
            continue  # 如果没有当前方向的直线则跳过


        # 阶段3: 空间聚类
        # 提取聚类坐标（水平线用y坐标，垂直线用x坐标），并转换为列向量供DBSCAN使用
        centers = np.array([line["center"][config["cluster_coord"]]
                            for line in subset]).reshape(-1, 1)

        # 使用DBSCAN进行一维聚类，返回聚类后每条直线的标签，符合聚类条件的直线标签相同
        clustering = DBSCAN(
            eps=dist_thresh,  # 邻域距离阈值
            min_samples=1,  # 最小样本数设为1（单条直线也可成簇）
            metric = 'euclidean',  # 默认距离计算方式
            algorithm = 'auto'  # 自动选择最优算法
        ).fit(centers)

        # 合并同类直线
        for label in np.unique(clustering.labels_):
            # 遍历所有簇标签，np.unique用于去重标签
            # 提取当前簇的所有直线
            # np.where(clustering.labels_ == label)：找到当前标签 label 对应的所有直线索引
            # subset[i]["line"]：从预处理数据中提取原始直线坐标 [x1,y1,x2,y2]
            group = [subset[i]["line"] for i in np.where(clustering.labels_ == label)[0]]
            # 方式1： 取组内直线的平均端点
            x1_avg = int(np.mean([l[0][0] for l in group]))
            y1_avg = int(np.mean([l[0][1] for l in group]))
            x2_avg = int(np.mean([l[0][2] for l in group]))
            y2_avg = int(np.mean([l[0][3] for l in group]))
            # 方式2： 选择组内最长的直线作为代表
            # representative = max(group, key=lambda x: x["length"])
            # x1, y1, x2, y2 = representative["line"][0]
            # merged_line = [[x1, y1, x2, y2]]
            merged_line = [[x1_avg, y1_avg, x2_avg, y2_avg]]  # 合并后的直线
            result_lines[config["name"]].append(merged_line)
            result_lines["merged"].append(merged_line)

    return result_lines

def crop_image(image, merged_lines, save_dir=None):
    """
    将图片根据merged_lines裁剪为多个最小方格，用于提取每个方格的信息
    :param image: 原始图像 (numpy数组)
    :param merged_lines: merge_lines函数返回的结果字典
    :param save_dir: 保存裁剪后小方格的目录
    :return: 返回裁剪后的方格列表和坐标信息
    """
    if not merged_lines:
        raise ValueError("没有合并后的直线数据！")
    # 设置默认保存路径（当前文件的同级image目录下的cells子目录）
    if save_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在目录
        parent_dir = os.path.dirname(current_dir)  # 上级目录
        save_dir = os.path.join(parent_dir, "image", "cells")  # 构建目标路径
    # 创建保存目录（包括所有必要父目录）
    os.makedirs(save_dir, exist_ok=True)

    # 1. 提取水平和垂直线坐标
    horizontal_lines = merged_lines['horizontal']
    vertical_lines = merged_lines['vertical']
    if not horizontal_lines or not vertical_lines:
        raise ValueError("缺少水平或垂直直线数据，无法形成网格！")

    # 2. 获取所有唯一的x和y坐标并排序
    y_coords = sorted({line[0][1] for line in horizontal_lines})  # 所有水平线的y坐标
    x_coords = sorted({line[0][0] for line in vertical_lines})  # 所有垂直线的x坐标

    # 3. 检查坐标数量是否足够形成网格
    if len(y_coords) < 2 or len(x_coords) < 2:
        raise ValueError("直线数量不足，无法形成网格！")

    # 4. 裁剪每个网格单元格
    print(f"检测到 {len(y_coords) - 1} 行和 {len(x_coords) - 1} 列的网格，共 {len(y_coords) - 1} * {len(x_coords) - 1} = {(len(y_coords) - 1) * (len(x_coords) - 1)} 个单元格")
    cells = []
    for i in range(len(y_coords) - 1):
        for j in range(len(x_coords) - 1):
            # 计算当前单元格的边界
            x1, x2 = x_coords[j], x_coords[j + 1]
            y1, y2 = y_coords[i], y_coords[i + 1]

            # 确保坐标在图像范围内
            h, w = image.shape[:2]
            x1, x2 = max(0, x1), min(w, x2)
            y1, y2 = max(0, y1), min(h, y2)

            # 裁剪单元格
            cell = image[y1:y2, x1:x2]

            # 保存信息
            cell_info = {
                "image": cell,
                "position": (i, j),  # 网格位置 (行, 列)
                "coordinates": (x1, y1, x2, y2)  # 图像坐标
            }
            cells.append(cell_info)

            # 保存图片 (可选)
            cv2.imwrite(f"{save_dir}/test05_cell_{i}_{j}.jpg", cell)

    return cells


def visualize_lines(image, merged_lines):
    """
    绘制并可视化合并后的直线
    :param image: 原始图像
    :param merged_lines: 合并后的直线结果
    """
    # 创建彩色图像用于绘制
    vis_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 绘制水平线（红色）
    for line in merged_lines['horizontal']:
        x1, y1, x2, y2 = line[0]
        cv2.line(vis_image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # 绘制垂直线（绿色）
    for line in merged_lines['vertical']:
        x1, y1, x2, y2 = line[0]
        cv2.line(vis_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 使用matplotlib显示
    plt.figure(figsize=(12, 8))
    plt.imshow(vis_image)
    plt.title("Merged Lines (Red: Horizontal, Green: Vertical)")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在目录
        parent_dir = os.path.dirname(current_dir)  # 上级目录

        process_image(cv2.imread(parent_dir + "/image/test/test05.jpg"))
        print("处理完成")

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")