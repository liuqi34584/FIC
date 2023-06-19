import numpy as np
import cv2

# 旋转图片
def rotate_img(image, angle):

    # 获取图像的高度和宽度
    height, width = image.shape[:2]

    # 计算旋转中心
    center = (width // 2, height // 2)

    # 定义旋转矩阵
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 执行旋转操作
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image


# 旋转注释框,传入原图，原box,旋转角度，返回新box
def rotate_box(image, box, angle):
    # box格式，如: [('lession', 683, 608, 1047, 939), ('lession', 550, 554, 839, 874)]
    contours_list = [] # 保存翻转后的所有列表

    # 在图像上绘制矩形框,每个坐标都单独绘制一次，防止box重叠
    for (name, x, y, x_max, y_max) in box:
        height, width = image.shape[:2]
        padded_image = np.zeros((height, width), dtype=np.uint8) 
        padded_image[:, :] = 0   # 将图像填充为指定颜色
        cv2.rectangle(padded_image, (x, y), (x_max, y_max), 255, -1) # -1表示边界宽度全填充
        padded_image = rotate_img(padded_image, angle)

        # 寻找最大的区域
        contours, _ = cv2.findContours(padded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 寻找最大区域的轮廓
        contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(contour)
        contours_list.append((name, x, y, x+w, y+h))

    return contours_list