import cv2
import numpy as np
import os

def find_largest_contour(image):
    # 寻找轮廓
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 寻找最大的轮廓
    largest_contour = max(contours, key=cv2.contourArea)
    
    return largest_contour

def draw_bounding_box(image, contour):
    # 计算最小外接矩形
    x, y, w, h = cv2.boundingRect(contour)

    # 缩小矩形框的高宽
    padding = 5
    x += padding
    y += padding
    w -= 2 * padding
    h -= 2 * padding

    # 绘制矩形框
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    return image


def cut_image_bounding_box(image, contour):
    # 计算最小外接矩形
    x, y, w, h = cv2.boundingRect(contour)

    # 缩小矩形框的高宽
    padding = 10
    x += padding
    y += padding
    w -= 2 * padding
    h -= 2 * padding

    # 裁剪图像
    cropped_image = image[y:y+h, x:x+w]
    
    return cropped_image



# 其目的是排除右上角字符的影响
# 把右上角变为黑色补丁，先新建白色图片，绘制右上角黑色补丁，然后和相 与（and）,就能得到右上角遮挡
def right_up_black(image): # 传入三通道原图

    # 获取原始图像的大小
    height, width = image.shape[:2]

    # 创建一个新的画布，大小与原始图像相同
    canvas = np.zeros_like(image)

    # 取反画布，将黑色区域变为白色
    canvas = cv2.bitwise_not(canvas)

    # 定义矩形区域的大小和颜色
    rectangle_width = int(width * 0.25)
    rectangle_height = int(height * 0.25)
    rectangle_color = (0, 0, 0)  # 黑色

    # 在画布上绘制矩形区域
    canvas[:rectangle_height, width-rectangle_width:] = rectangle_color

    # 将原始图像覆盖到画布上
    image = cv2.bitwise_and(image, canvas)

    return image


# 指定原始图像文件夹和目标保存文件夹
input_folder = './step0/JPEGImages/'
input_segmentation_folder = './step0/SegmentationClassPNG/'

output_folder = './step1/JPEGImages/'
output_segmentation_folder = './step1/SegmentationClassPNG/'

# 确保目标保存文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历原始图像文件夹中的所有文件
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 构建原始图像文件的完整路径
        input_path = os.path.join(input_folder, filename)
        input_segmentation_path = os.path.join(input_segmentation_folder, filename[:-4] + ".png")

        # 读取原始图像
        img = cv2.imread(input_path)
        segmentation_img = cv2.imread(input_segmentation_path)

        # 转换为灰度图像
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 创建腐蚀核（结构元素）
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 此处使用矩形结构元素

        # 对图像进行腐蚀
        gray_image = cv2.erode(gray_image, kernel, iterations=1)

        # 进行二值化处理
        _, binary_image = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY)

        # 寻找最大的白色区域
        largest_contour = find_largest_contour(binary_image)

        # 在原图上绘制矩形框
        image_with_box = draw_bounding_box(img.copy(), largest_contour)

        # 裁剪出矩形框中的内容
        image_with_box = cut_image_bounding_box(img.copy(), largest_contour)
        segmentation_image_with_box = cut_image_bounding_box(segmentation_img.copy(), largest_contour)

        # 构建目标保存文件的完整路径
        output_path = os.path.join(output_folder, filename)

        output_segmentation_path = os.path.join(output_segmentation_folder, filename[:-4] + ".png")

        # 保存图像到目标保存文件夹中
        cv2.imwrite(output_path, image_with_box)
        cv2.imwrite(output_segmentation_path, segmentation_image_with_box)

        print(f'Saved: {output_path}')
        print(f'Saved: {output_segmentation_path}')

print('Image processing and saving complete.')


