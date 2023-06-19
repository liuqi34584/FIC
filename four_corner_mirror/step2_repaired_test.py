import cv2
import numpy as np

# 指定原始图像文件夹和目标保存文件夹
input_path = './example_out/step1_images_cut.jpg'
output_path = './example_out/step2_images_reflect.jpg'

# 对矩阵左下角进行镜像翻转
def rect_left_right(images):

    # 将OpenCV数组转换为NumPy数组
    matrix = np.array(images)

    # 创建一个与原始矩阵相同大小的零矩阵
    transformed_matrix = np.zeros_like(matrix)

    # 获取左下三角部分的索引
    indices = np.tril_indices(matrix.shape[0])

    # 将左下三角部分的值赋值给零矩阵对应的左下三角位置
    transformed_matrix[indices] = matrix[indices]

    # 转置矩阵，并获取右上三角部分的索引
    transposed_matrix = matrix.transpose()
    indices = np.triu_indices(transposed_matrix.shape[0])

    # 将右上三角部分的值赋值给零矩阵对应的右上三角位置
    transformed_matrix[indices] = transposed_matrix[indices]

    return transformed_matrix

# 对方阵区域进行镜像翻转
def rect_flip(image_with_box,directions):

# 镜像该矩形框,然后合并到输入图像
    if directions == 0:  # 左上角的情况
        image_with_box = cv2.flip(image_with_box, 1)  # 方便矩阵处理，变为左下角矩阵

        b, g, r = cv2.split(image_with_box)
        b = rect_left_right(b)
        g = rect_left_right(g)
        r = rect_left_right(r)
        image_with_box = cv2.merge([b, g, r])

        image_with_box = cv2.flip(image_with_box, 1)

    if directions == 1:  # 右上角的情况

        b, g, r = cv2.split(image_with_box)
        b = rect_left_right(b)
        g = rect_left_right(g)
        r = rect_left_right(r)
        image_with_box = cv2.merge([b, g, r])


    if directions == 2:  # 左下角的情况
        image_with_box = cv2.flip(image_with_box, -1)  # 方便矩阵处理，变为左下角矩阵

        b, g, r = cv2.split(image_with_box)
        b = rect_left_right(b)
        g = rect_left_right(g)
        r = rect_left_right(r)
        image_with_box = cv2.merge([b, g, r])

        image_with_box = cv2.flip(image_with_box, -1)
    
    if directions == 3:  # 右下角的情况
        image_with_box = cv2.flip(image_with_box, 0)  # 方便矩阵处理，变为左下角矩阵

        b, g, r = cv2.split(image_with_box)
        b = rect_left_right(b)
        g = rect_left_right(g)
        r = rect_left_right(r)
        image_with_box = cv2.merge([b, g, r])
        
        image_with_box = cv2.flip(image_with_box, 0)

    return image_with_box


x = 5  # 四个角区域控制因子 x

# 读取图像
image = cv2.imread(input_path)

# 获取图像尺寸
large_height, large_width = image.shape[:2]

# 裁剪四个角的矩形区域
rect_top_left =     image[:large_width//x, :large_width//x]
rect_top_right =    image[:large_width//x, large_width-large_width//x:]
rect_bottom_left =  image[large_height-large_width//x:, :large_width//x]
rect_bottom_right = image[large_height-large_width//x:, large_width-large_width//x:]

rect_top_left = rect_flip(rect_top_left, 0)
image[:large_width//x, :large_width//x] = rect_top_left

rect_top_right = rect_flip(rect_top_right, 1)
image[:large_width//x, large_width-large_width//x:] = rect_top_right

rect_bottom_left = rect_flip(rect_bottom_left, 2)
image[large_height-large_width//x:, :large_width//x] = rect_bottom_left 

rect_bottom_right = rect_flip(rect_bottom_right, 3)
image[large_height-large_width//x:, large_width-large_width//x:] = rect_bottom_right

# 保存图像到目标保存文件夹中
cv2.imwrite(output_path, image)
