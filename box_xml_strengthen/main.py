import numpy as np
import cv2
import xml.etree.ElementTree as ET
import os

# 加载数据增强库
from strengthen.xml import read_annotation, write_bbox_to_voc_xml
from strengthen.rotation import rotate_img, rotate_box
from strengthen.turnover import turnover_img, turnover_box
from strengthen.warpaffine import warpAffine_img, warpAffine_box
from strengthen.padding import padding_img, padding_box
from strengthen.cut import cut_img, cut_box

images_path = "./box_xml_strengthen/test_images/JPEGImages/images2.jpg"
xml_path = "./box_xml_strengthen/test_images/Annotations/images2.xml"

images_out_path = "./box_xml_strengthen/test_images/out_images/JPEGImages/images2.jpg"
xml_out_path = "./box_xml_strengthen/test_images/out_images/Annotations/images2.xml"

# 读取原图与注释
img = cv2.imread(images_path, 1)
coordinates = read_annotation(xml_path) 

# 核心处理调用，需要哪一个功能就打开那一个注释，一次只开一个功能

# 旋转原图与注释
# new_img = rotate_img(img, 60)
# new_box = rotate_box(img, coordinates, 60)

# 翻转原图与注释
# new_img = turnover_img(img, -1)
# new_box = turnover_box(img, coordinates, -1)

# 仿射变换原图与注释
new_img = warpAffine_img(img, 20)
new_box = warpAffine_box(img, coordinates, 20)

# # 镜像填充原图的四边
# new_img = padding_img(img, 0, 100, 50, 0)
# new_box = padding_box(img, coordinates, 0, 100, 50, 0)

# 裁剪原图的四边
# new_img = cut_img(img, 20, 0, 100, 0)
# new_box = cut_box(img, coordinates, 20, 0, 100, 0)

# 保存原图与标注
cv2.imwrite(images_out_path, new_img)


xml_dict = {"folder": "VOC2012", 
            "filename": "1011.jpg",
            "path": "value1",
            "width": new_img.shape[0],
            "height": new_img.shape[1],
            "depth": 3,
            "box": new_box,
            "save_path" : xml_out_path
            }
write_bbox_to_voc_xml(xml_dict)
