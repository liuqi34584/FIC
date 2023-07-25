import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random
import os

# 读取 xml 注释文件
def read_annotation(xml_file):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 存储坐标信息的列表
    coordinates = []

    # 遍历每个 object 元素
    for obj in root.iter('object'):
        # 获取标注框的位置信息
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        # 将坐标信息添加到列表中
        coordinates.append((name, xmin, ymin, xmax, ymax))

    return coordinates

# 添加换行符和对齐
def prettify(elem, level=0):
    indent = "    " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = "\n" + indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = "\n" + indent
        for subelem in elem:
            prettify(subelem, level + 1)
            if not subelem.tail or not subelem.tail.strip():
                subelem.tail = "\n" + indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = "\n" + indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = "\n" + indent


# 将坐标保存到 xml 文件
# 传入的键值参考如下
# xml_dict = {"folder": "VOC2012", 
#             "filename": "12.jpg",
#             "path": "JPEGImages",
#             "width": img.shape[0],
#             "height": img.shape[1],
#             "depth": 3,
#             "box": [('lession', 550, 554, 839, 874)],
#             "save_path" : "./Annotations/1011.xml"
#             }
def write_bbox_to_voc_xml(xml_dict):

    dict_folder = xml_dict["folder"]
    dict_filename = xml_dict["filename"]
    dict_path = xml_dict["path"]
    dict_width = xml_dict["width"]
    dict_height = xml_dict["height"]
    dict_depth = xml_dict["depth"]
    dict_box = xml_dict["box"]
    dict_save_path = xml_dict["save_path"]

    # 创建根节点
    root = ET.Element("annotation")

    # 创建子节点
    folder = ET.SubElement(root, "folder")
    folder.text = dict_folder

    filename_elem = ET.SubElement(root, "filename")
    filename_elem.text = dict_filename

    path = ET.SubElement(root, "path")
    path.text = f"{dict_path}"

    source = ET.SubElement(root, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    size = ET.SubElement(root, "size")
    width_elem = ET.SubElement(size, "width")
    width_elem.text = str(dict_width)
    height_elem = ET.SubElement(size, "height")
    height_elem.text = str(dict_height)
    depth = ET.SubElement(size, "depth")
    depth.text = str(dict_depth)

    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"

    for data in dict_box:
        object_elem = ET.SubElement(root, "object")
        name = ET.SubElement(object_elem, "name")
        name.text = str(data[0])
        pose = ET.SubElement(object_elem, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object_elem, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object_elem, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(object_elem, "bndbox")
        xmin_elem = ET.SubElement(bndbox, "xmin")
        xmin_elem.text = str(data[1])
        ymin_elem = ET.SubElement(bndbox, "ymin")
        ymin_elem.text = str(data[2])
        xmax_elem = ET.SubElement(bndbox, "xmax")
        xmax_elem.text = str(data[3])
        ymax_elem = ET.SubElement(bndbox, "ymax")
        ymax_elem.text = str(data[4])

    # 创建 XML 树
    tree = ET.ElementTree(root)
    # 调整换行与对齐
    prettify(root)
    # 将 XML 写入文件
    tree.write(dict_save_path)

# 判断 两个 边框是否重叠
def are_boxes_intersecting(check_box, boxs):
    # box的坐标表示为 (x_min, y_min, x_max, y_max)
    for (name, x, y, x_max, y_max) in boxs:
        # 检查水平方向是否有重叠
        if check_box[0] <= x_max and check_box[2] >= x:
            # 检查垂直方向是否有重叠
            if check_box[1] <= y_max and check_box[3] >= y:
                return True

    return False

# 这是原图无xml的融合函数，融合后会新建一个与原图对应的xml
# 传入大图路径，小图路径，目标坐标点(小图左上角为起点)，小图类别，输出路径
# 结果输出文件夹位置：输出路径 + images和 xml
def simage_add_bimages(big_image_path, small_image_path, set_box, class_name, out_put_path):
    big_image = cv2.imread(big_image_path, 1)
    small_image = cv2.imread(small_image_path, 1)

    b_h = big_image.shape[0]
    b_w = big_image.shape[1]
    b_c = big_image.shape[2]

    s_h = small_image.shape[0]
    s_w = small_image.shape[1]
    
    # 获取融合位置
    y_start,y_end,x_start,x_end = set_box[1],set_box[1]+s_h,set_box[0],set_box[0]+s_w

    # 限制幅度
    if y_end > b_h or x_end > b_w: 
        print("小图坐标越界：", (x_start,y_start,x_end,y_end), "图尺寸：", big_image.shape)
    else:
        # 将小图片覆盖到大图片的指定区域上
        big_image[y_start:y_end, x_start:x_end] = small_image
        xml_box = [(class_name, x_start, y_start, x_end, y_end)]

        images_out_path = os.path.join(out_put_path, "images/")
        if not os.path.exists(images_out_path):os.makedirs(images_out_path)

        file_name = os.path.basename(big_image_path)
        image_path = os.path.join(images_out_path, file_name[:-4] + "_add_stb.jpg")
        cv2.imwrite(image_path, big_image)

        xml_out_path = os.path.join(out_put_path, "xml/")
        if not os.path.exists(xml_out_path):os.makedirs(xml_out_path)

        out_xml_path = os.path.join(xml_out_path, file_name[:-4] + "_add_stb.xml")
        xml_dict = {"folder": images_out_path, 
                    "filename": file_name[:-4] + "_add_stb.jpg",
                    "path": image_path,
                    "width": b_w,
                    "height": b_h,
                    "depth": b_c,
                    "box": xml_box,
                    "save_path" : out_xml_path
                    }
        write_bbox_to_voc_xml(xml_dict)

        print(out_xml_path, xml_box)

# 这是原图有xml的融合函数，融合后会在原来的xml上新添加一个box框
# 传入大图路径，小图路径，xml路径，目标坐标点(小图左上角为起点)，小图类别，输出路径
# 结果输出文件夹位置：输出路径 + images和 xml
def simage_add_bimages_with_xml(big_image_path, small_image_path, xml_path, set_box, class_name, out_put_path):
    # 读取原图与原注释box框
    big_image = cv2.imread(big_image_path, 1)
    small_image = cv2.imread(small_image_path, 1)
    coordinates = read_annotation(xml_path) 

    b_h = big_image.shape[0]
    b_w = big_image.shape[1]
    b_c = big_image.shape[2]

    s_h = small_image.shape[0]
    s_w = small_image.shape[1]
    
    # 获取融合位置
    y_start,y_end,x_start,x_end = set_box[1],set_box[1]+s_h,set_box[0],set_box[0]+s_w
    
    if y_end > b_h or x_end > b_w: # 限制幅度
        print("小图坐标越界：", (x_start,y_start,x_end,y_end), "图尺寸：", big_image.shape)
    elif are_boxes_intersecting((x_start,y_start,x_end,y_end), coordinates) == True:
        print("边界框相交:", (x_start,y_start,x_end,y_end), coordinates)
    else:
        # 将小图片覆盖到大图片的指定区域上
        big_image[y_start:y_end, x_start:x_end] = small_image
        xml_box = [(class_name, x_start, y_start, x_end, y_end)]
        coordinates.append(xml_box[0])

        images_out_path = os.path.join(out_put_path, "images/")
        if not os.path.exists(images_out_path):os.makedirs(images_out_path)

        file_name = os.path.basename(big_image_path)
        image_path = os.path.join(images_out_path, file_name[:-4] + "_addxml_stb.jpg")
        cv2.imwrite(image_path, big_image)

        xml_out_path = os.path.join(out_put_path, "xml/")
        if not os.path.exists(xml_out_path):os.makedirs(xml_out_path)

        out_xml_path = os.path.join(xml_out_path, file_name[:-4] + "_addxml_stb.xml")
        xml_dict = {"folder": images_out_path, 
                    "filename": file_name[:-4] + "_addxml_stb.jpg",
                    "path": image_path,
                    "width": b_w,
                    "height": b_h,
                    "depth": b_c,
                    "box": coordinates,
                    "save_path" : out_xml_path
                    }
        write_bbox_to_voc_xml(xml_dict)

        print(out_xml_path, coordinates)

# -----------------------------------------------原图无xml使用举例：
# from add_small_to_big import simage_add_bimages

# # 大小图路径
# big_image_path = "C:/mycode/github/FIC/images/b_images/class1_train_000.jpg"
# small_image_path = "C:/mycode/github/FIC/images/1/000000_box.jpg"

# # 输出路径
# out_put_path = "C:/mycode/github/FIC/images/"

# simage_add_bimages(big_image_path, small_image_path, (500,500), "label_1", out_put_path)


# -----------------------------------------------原图有xml使用举例
# from add_small_to_big import simage_add_bimages

# # 原图，小图，xml路径
# big_image_path = "C:/mycode/github/FIC/images/images/class1_train_000_add_stb.jpg"
# small_image_path = "C:/mycode/github/FIC/images/1/000000_box.jpg"
# xml_path = "C:/mycode/github/FIC/images/xml/class1_train_000_add_stb.xml"

# # 输出路径
# out_put_path = "C:/mycode/github/FIC/images/"

# simage_add_bimages_with_xml(big_image_path, small_image_path, xml_path, (900,1440), "label_2", out_put_path)

# ---------------------------------------------提示：一张大图可以和多张小图一对一，一对多融合，达到数据扩增的目的