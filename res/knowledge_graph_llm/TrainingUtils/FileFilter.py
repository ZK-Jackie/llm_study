"""
过滤知识图谱数据
"""
import json
from tqdm import tqdm
import re


def filter_kg_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in tqdm(f_in, desc='Filtering'):
            data = json.loads(line)
            if '[KG]' in data['sentence'] and '[/KG]' in data['sentence']:
                data['sentence'] = re.sub('\[KG\].*?\[/KG\]', '', data['sentence'])
                data['sentence'] = data['sentence'].strip()
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
            if data['label'] == 1:
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    filter_kg_data('raw_dir/raw1.jsonl', 'input_dir/input1.jsonl')
