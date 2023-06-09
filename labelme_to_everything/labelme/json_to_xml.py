import os
import json
import xml.etree.ElementTree as ET
import cv2

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

def convert_shapes_to_xml(shapes):
    box_list = []
    for shape in shapes:
        label = str(shape['label'])

        points = shape['points']
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        xmin = min(x_values)
        ymin = min(y_values)
        xmax = max(x_values)
        ymax = max(y_values)

        box_list.append((label, xmin, ymin, xmax, ymax))
    
    return box_list


# 读取 Labelme JSON 文件的像素信息标签,
# 返回值,如:[('blue', 149, 269, 1142, 741), ('blue', 41, 301, 247, 446)]
def read_json_info(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    
    box_list = []
    for shape in json_data['shapes']:
        label = str(shape['label'])

        points = shape['points']
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        xmin = min(x_values)
        ymin = min(y_values)
        xmax = max(x_values)
        ymax = max(y_values)

        box_list.append((label, int(xmin), int(ymin), int(xmax), int(ymax)))
    
    return box_list

def json_to_xml(images_path, json_path, xml_out_path):
    json_file_list = []
    for file in os.listdir(json_path):
        if file.endswith('.json'):
            json_file_list.append(file)

            source_images_path = os.path.join(images_path, file[:-5]+".jpg")
            img = cv2.imread(source_images_path, 1)
            height, width, channels = img.shape

            source_path = os.path.join(json_path, file)
            target_path = os.path.join(xml_out_path, file[:-5]+".xml")

            box_list = read_json_info(source_path)
            xml_dict = {"folder": "../images/", 
                "filename": file[:-5]+".jpg",
                "path": target_path,
                "width": width,
                "height": height,
                "depth": channels,
                "box": box_list,
                "save_path" : target_path
                }
        write_bbox_to_voc_xml(xml_dict)

        print(target_path,"成功生成！")


