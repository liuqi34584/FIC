# 项目说明
这是一个用于解决labelme制作的数据集各种问题的文件夹，主要功能如下：
1. 根据labelme的分割标注框，生成目标检测标注框
2. 更改labelme的名字（有同一对象的不同lael的情况）

# 项目操作使用

0. 具体使用方式查看 main.py 代码调用方式
1. labelme文件夹是核心方法，可以直接复制放在个人工程中直接调用


## 功能一，根据labelme的分割标注框，生成目标检测标注框

生成原理是基于json文件转化，因此不存在标签遗漏问题，使用方式参考main.py

最终效果
|分割原图|处理后|
|---------|---------|
|<left><img src = "./data/github_images/json.png" width = 80%><left> |<left><img src = "./data/github_images/json_to_xml.png" width = 80%><left>|

## 功能二，更改 label 的名字
这个功能主要用在数据集更新过程中以下情况：

第一批数据，我们将分割区域给出标签 "blue", "red", "white"

第二批数据，我们将分割区域给出标签 "1",    "2",   "3"

其实分割的就是同一对象，但软件labelme没有相应批量修改功能，因此这里给出解决函数，使用方法参考main.py。

要特别注意列表索引标签一一对应，如:

```json_label_turn(json_path, json_out_path, ["1", "2", "3"], ["blue", "red", "white"])```

