# 项目说明
这是一个用于解决labelme制作的数据集各种问题的文件夹，主要功能如下：
1. 根据labelme的分割标注框，生成目标检测标注框
2. 更改labelme的名字（有同一对象的不同lael的情况）


## 一，根据labelme的分割标注框，生成目标检测标注框

使用方式参考main.py

最终效果
|分割原图|处理后|
|---------|---------|
|<left><img src = "./data/github_images/json.png" width = 80%><left> |<left><img src = "./data/github_images/json_to_xml.png" width = 80%><left>|

## 二，更改labelme的名字
这个功能主要用在以下情况：

数据集更新过程中

第一批数据，我们将分割区域给出标签 "blue", "red", "white"
第二批数据，我们将分割区域给出标签 "1",    "2",   "3"

其实分割的就是同一对象，但软件labelme相应功能，因此这里给出解决函数，使用方法参考main.py。
使用

```json_label_turn(json_path, json_out_path, ["blue", "red", "white"], ["1", "2", "3"])```

要特别注意列表索引标签一一对应。