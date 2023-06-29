import numpy as np
import cv2

# 仿射变换图片
def warpAffine_img(image, angle):

    # 定义变换参数
    # angle = 80  # 旋转角度（单位：度）
    scale = 0.8  # 缩放因子
    translation = (50, 50)  # 平移量（x，y像素）

    # 获取图像尺寸
    height, width = image.shape[:2]

    # 计算旋转矩阵
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

    # 执行仿射变换
    transformed_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # 执行平移变换
    translation_matrix = np.float32([[1, 0, translation[0]], [0, 1, translation[1]]])
    transformed_image = cv2.warpAffine(transformed_image, translation_matrix, (width, height))

    return transformed_image


# 仿射变换注释框,传入原图，原box,旋转角度，返回新box
def warpAffine_box(image, box, angle):
    # box格式，如: [('lession', 683, 608, 1047, 939), ('lession', 550, 554, 839, 874)]
    contours_list = [] # 保存翻转后的所有列表

    # 在图像上绘制矩形框,每个坐标都单独绘制一次，防止box重叠
    for (name, x, y, x_max, y_max) in box:
        height, width = image.shape[:2]
        padded_image = np.zeros((height, width), dtype=np.uint8) 
        padded_image[:, :] = 0   # 将图像填充为指定颜色
        cv2.rectangle(padded_image, (x, y), (x_max, y_max), 255, -1) # -1表示边界宽度全填充
        padded_image = warpAffine_img(padded_image, angle)

        # 寻找最大的区域
        contours, _ = cv2.findContours(padded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 寻找最大区域的轮廓
        if len(contours) != 0:
           contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(contour)
        contours_list.append((name, x, y, x+w, y+h))

    return contours_list