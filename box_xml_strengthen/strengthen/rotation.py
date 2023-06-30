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
def rotate_box(image, box, angle, mode = "rectangle"):
    # box格式，如: [('lession', 683, 608, 1047, 939), ('lession', 550, 554, 839, 874)]
    contours_list = [] # 保存翻转后的所有列表

    # 在图像上绘制矩形框,每个坐标都单独绘制一次，防止box重叠
    for (name, x, y, x_max, y_max) in box:
        height, width = image.shape[:2]
        padded_image = np.zeros((height, width), dtype=np.uint8) 
        padded_image[:, :] = 0   # 将图像填充为指定颜色

        if mode == "cross_line": # 十字架法
            x_center = int((x_max+x)/2)
            y_center = int((y_max+y)/2)
            thickness = 2 # 线宽
            # 绘制十字架的水平线
            cv2.line(padded_image, (x, y_center), (x_max, y_center), 255, thickness)
            # 绘制十字架的垂直线
            cv2.line(padded_image, (x_center, y), (x_center, y_max), 255, thickness)
        elif mode == "ellipse":  # 椭圆法
            x_width = int((x_max-x)/2)
            y_height = int((y_max-y)/2)
            a = x_width if x_width > y_height else y_height
            b = x_width if x_width < y_height else y_height
            center = (int((x_max+x)/2), int((y_max+y)/2))
            axes = (a, b)  # 长轴和短轴长度
            thickness = 2   # 线条粗细
            # 绘制椭圆
            cv2.ellipse(padded_image, center, axes, 0, 0, 360, 255, thickness)
        elif mode == "rectangle":
            cv2.rectangle(padded_image, (x, y), (x_max, y_max), 255, -1) # -1表示边界宽度全填充
        else: # 矩形法
            cv2.rectangle(padded_image, (x, y), (x_max, y_max), 255, -1) # -1表示边界宽度全填充

        # 旋转绘制图
        padded_image = rotate_img(padded_image, angle)

        # 寻找最大的区域
        contours, _ = cv2.findContours(padded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 寻找最大区域的轮廓
        if len(contours) != 0:
           contour = max(contours, key=cv2.contourArea)

        # # 需要绘制对比时打开
        # # 计算最小外接矩形
        # x, y, w, h = cv2.boundingRect(contour)
        # # 转换为三通道图像
        # padded_image = cv2.cvtColor(padded_image, cv2.COLOR_GRAY2BGR)
        # # 绘制矩形框
        # cv2.rectangle(padded_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # # 调试用保存图像
        # cv2.imwrite("./box_xml_strengthen/example_out/rotation_ellipse_out.jpg", padded_image)

        x, y, w, h = cv2.boundingRect(contour)
        contours_list.append((name, x, y, x+w, y+h))

    return contours_list