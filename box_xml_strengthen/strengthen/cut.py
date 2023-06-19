import numpy as np
import cv2

# 镜像填充图片，参数up, down, left, right是对四边填充的像素宽度
def cut_img(image, up, down, left, right):

    # 获取图像尺寸
    height, width = image.shape[:2]

    cut_img = image[up:height-down, left:width-right]

    # Reflect_img = cv2.copyMakeBorder(cut_img, cut_up, cut_down, cut_left, cut_right, cv2.BORDER_REFLECT)  # 反射法，在图像边缘进行镜像反射
    return cut_img


# 仿射变换注释框,传入原图，原box,旋转角度，返回新box
def cut_box(image, box, up, down, left, right):
    # box格式，如: [('lession', 683, 608, 1047, 939), ('lession', 550, 554, 839, 874)]
    contours_list = [] # 保存翻转后的所有列表

    # 在图像上绘制矩形框,每个坐标都单独绘制一次，防止box重叠
    for (name, x, y, x_max, y_max) in box:
        height, width = image.shape[:2]
        padded_image = np.zeros((height, width), dtype=np.uint8) 
        padded_image[:, :] = 0   # 将图像填充为指定颜色
        cv2.rectangle(padded_image, (x, y), (x_max, y_max), 255, -1) # -1表示边界宽度全填充
        padded_image = cut_img(padded_image, up, down, left, right)

        # 寻找最大的区域
        contours, _ = cv2.findContours(padded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 寻找最大区域的轮廓
        contour = max(contours, key=cv2.contourArea)
        
        x, y, w, h = cv2.boundingRect(contour)
        contours_list.append((name, x, y, x+w, y+h))

    return contours_list