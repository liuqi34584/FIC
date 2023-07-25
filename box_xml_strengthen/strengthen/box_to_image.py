import os
import xml.etree.ElementTree as ET
from PIL import Image
import cv2

# 此文件是用来裁剪出目标区域小图的文件
# 函数输入应该是 原图与xml (名字保持一致)
# 函数输出是指定路径分类别裁剪出的box小图
def box_to_image(input_images_path, input_xml_path, out_images_path):

    num = 0

    # 遍历所有的 XML 标注文件
    for xml_file in os.listdir(input_xml_path):
        xml_path = os.path.join(input_xml_path, xml_file)

        # 解析 XML 文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图像文件名和路径
        image_name = xml_file[:-4] + ".jpg"
        image_path = os.path.join(input_images_path, image_name)

        # 打开图像文件
        image = cv2.imread(image_path, 1)

        # 遍历所有的对象
        for obj in root.iter('object'):
            # 获取边界框坐标
            name = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            # 裁剪图像
            cropped_image = image[ymin:ymax, xmin:xmax]

            out_path = os.path.join(out_images_path, name)
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            image_output_path = os.path.join(out_path, str(num).zfill(6) + "_box.jpg")
            cv2.imwrite(image_output_path, cropped_image)

            print("输出图片", image_output_path)
            num = num + 1

# 调用示例：
# from box_to_image import box_to_image

# # 输入目录和输出目录的路径
# image_dir = 'C:/mycode/iflytek/datasetmake/score1_dataset/score1_12/train/images/'
# xml_dir = 'C:/mycode/iflytek/datasetmake/score1_dataset/score1_12/train/xml/'
# image_output_dir = 'C:/mycode/github/FIC/images/'

# box_to_image(image_dir, xml_dir, image_output_dir)
