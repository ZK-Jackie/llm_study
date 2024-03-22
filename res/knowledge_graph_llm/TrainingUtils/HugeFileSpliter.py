import os
import json
from tqdm import tqdm


def get_size(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode('utf8'))


def split_json(file_path, max_size):
    # 获取源文件名
    base_name = os.path.basename(file_path).split('.')[0]
    # 创建新的文件夹
    output_dir = f"xtuner_train/{base_name}_parts"
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    size = 0
    new_data = []
    file_count = 1

    for item in tqdm(data, desc='Splitting JSON'):
        item_size = get_size(item)
        if size + item_size > max_size:
            with open(os.path.join(output_dir, f'{base_name}_part{file_count}.json'), 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            size = 0
            new_data = []
            file_count += 1
        size += item_size
        new_data.append(item)

    if new_data:
        with open(os.path.join(output_dir, f'{base_name}_part{file_count}.json'), 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)


# 调用函数，将大的JSON文件拆分为多个小的JSON文件
split_json('hf_train\\upload\\t2kg_hf_train.json', 50 * 1024 * 1024)  # 50MB
