import cv2
import numpy as np
import os


# 指定原始图像文件夹和目标保存文件夹
input_path = './example_out/step2_images_reflect.jpg'
output_path = './example_out/step3_images_resize.jpg'
# 读取原始图像
img = cv2.imread(input_path)


# 调整图像大小
img = cv2.resize(img, (512, 512))

# 保存图像到目标保存文件夹中
cv2.imwrite(output_path, img)


print('Image processing and saving complete.')


