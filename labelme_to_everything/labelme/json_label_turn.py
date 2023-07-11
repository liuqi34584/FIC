import os
import shutil
import json

# 批量转换json文件 label 标签
# 使用示例： 传入：(json_path, json_out_path, ["blue", "red", "white"], ["1", "2", "3"])
def json_label_turn(json_folder_path, save_path, old_label, new_label):

    json_file_list = []
    for file in os.listdir(json_folder_path):
        if file.endswith('.json'):
            json_file_list.append(file)

            source_path = os.path.join(json_folder_path, file)
            target_path = os.path.join(save_path, file)

            # 读取JSON文件内容
            with open(source_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # 修改标签名字
                for shape in data['shapes']:
                    for index, item in enumerate(old_label):
                        if shape['label'] == item:
                            shape['label'] = new_label[index]
                            break

            # 保存修改后的JSON文件
            with open(target_path, 'w') as file:
                json.dump(data, file, indent=2)
                print(target_path, "标签转换成功!")
