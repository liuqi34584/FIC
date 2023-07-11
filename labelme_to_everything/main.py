import numpy as np
import cv2
import xml.etree.ElementTree as ET
import os




# json转xml
from labelme.json_to_xml import json_to_xml

images_path = "./labelme_to_everything/data/test_dataset/images/"
json_path = "./labelme_to_everything/data/test_dataset/json/"
xml_out_path = "./labelme_to_everything/data/example_out/xml/"

json_to_xml(images_path, json_path, xml_out_path)





# # 改变 json 标签
# from labelme.json_label_turn import json_label_turn

# json_path = "./labelme_to_everything/data/test_dataset/json/"
# json_out_path = "./labelme_to_everything/data/example_out/json/"

# json_label_turn(json_path, json_out_path, ["1", "2", "3"], ["blue", "red", "white"])
