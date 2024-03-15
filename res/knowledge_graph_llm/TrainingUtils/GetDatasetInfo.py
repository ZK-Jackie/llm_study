import json

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    element_count = len(data)
    max_token_count = max(sum(len(str(key)) + len(str(value)) for key, value in element.items()) for element in data)

    print(f"Number of elements: {element_count}")
    print(f"Max token count: {max_token_count}")

# 使用函数
process_json_file("xtuner_train/kg_xtuner.json")