import xml.etree.ElementTree as ET

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

    # 将 XML 写入文件
    tree.write(dict_save_path)