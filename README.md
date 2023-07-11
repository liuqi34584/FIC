# 项目说明

# box_xml_strengthen
这是一个制作目标检测数据增强的文件夹，用于增强数据集。
|原图|同步仿射变换注释|
|---------|---------|
|<left><img src = "./box_xml_strengthen/example_out/images2.jpg"><left> |<left><img src = "./box_xml_strengthen/example_out/warpaffine.jpg"><left>|

# four_corner_mirror
这是一个制作食道癌数据集的文件夹，用于消除数据集的黑边。
|原图|处理后|
|---------|---------|
|<left><img src = "./four_corner_mirror/example_out/images.jpg" width = 80%><left> |<left><img src = "./four_corner_mirror/example_out/step3_images_resize512.jpg" width = 80%><left>|

# labelme_to_everything
这是一个用于解决labelme制作的数据集各种问题的文件夹，主要功能如下：
1. 根据labelme的分割标注框，生成目标检测标注框
2. 更改labelme的名字（有同一对象的不同lael的情况）

|分割原图|处理后|
|---------|---------|
|<left><img src = "./labelme_to_everything/data/github_images/json.png" width = 80%><left> |<left><img src = "./labelme_to_everything/data/github_images/json_to_xml.png" width = 80%><left>|
