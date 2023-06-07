import cv2
import numpy as np
import os


# 指定原始图像文件夹和目标保存文件夹
input_folder = './step2/JPEGImages/'
input_segmentation_folder = './step2/SegmentationClassPNG/'

output_folder = './images/'
output_segmentation_folder = './masks/'


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

        # 调整图像大小
        img = cv2.resize(img, (512, 512))
        segmentation_img = cv2.resize(segmentation_img, (512, 512))

# 构建目标保存文件的完整路径
        output_path = os.path.join(output_folder, filename)
        output_segmentation_path = os.path.join(output_segmentation_folder, filename[:-4] + ".png")

# 保存图像到目标保存文件夹中
        cv2.imwrite(output_path, img)
        cv2.imwrite(output_segmentation_path, segmentation_img)

        print(f'Saved: {output_path}')
        print(f'Saved: {output_segmentation_path}')

print('Image processing and saving complete.')


