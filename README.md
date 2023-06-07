这是一个制作食道癌数据集的文件夹，用于消除食道癌数据集的黑边

最终效果如图：

|原图|处理后|
|---------|---------|
|<left><img src = "./example_out/images.jpg" width = 80%><left> |<left><img src = "./example_out/step3_images_resize512.jpg" width = 80%><left>|
|<left><img src = "./example_out/mask.png" width = 80%><left>|<left><img src = "./example_out/step3_mask_resize512.png" width = 80%><left>|

# 第一步
|原图|腐蚀去掉文字|
|:---------:|:---------:|
|<left><img src = "./example_out/images.jpg" width = 80%><left>|<left><img src = "./example_out/step1_images_erode.jpg" width = 80%><left> |


|二值化|根据二值找得|裁剪|
|:---------:|:---------:|:---------:|
|<left><img src = "./example_out/step1_binary_image.jpg" width = 80%><left>|<left><img src = "./example_out/step1_images_box.jpg" width = 80%><left>|<left><img src = "./example_out/step1_images_cut.jpg" width = 80%><left>|

# 第二步
|原图|对四角进行镜像|
|:---------:|:---------:|
|<left><img src = "./example_out/step1_images_cut.jpg" width = 80%><left>|<left><img src = "./example_out/step2_images_reflect.jpg" width = 80%><left>|

# 第三步
|原图|重设统一大小|
|:---------:|:---------:|
|<left><img src = "./example_out/step2_images_reflect.jpg" width = 80%><left>|<left><img src = "./example_out/step3_images_resize.jpg" width = 80%><left>|