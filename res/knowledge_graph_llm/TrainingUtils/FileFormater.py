import os
import fnmatch
import json
import jsonlines
import config
from tqdm import tqdm


def convert_format(input_jsonl, output_jsonl, format='hf'):
    with (jsonlines.open(input_jsonl, mode='r') as f_in,
          jsonlines.open(output_jsonl, mode='w') as f_out):
        last_sentence = None
        conversation = None
        # 逐行读取文件
        for line in tqdm(f_in, desc="Processing lines"):
            # 对数据行的sentence_b做切割
            sentence_b_parts = line['sentence_b'].split(',')

            # 当前是新的一轮对话（跟上一个对话不同），也代表重复的对话结束了，则——
            if line['sentence'] != last_sentence:
                # 把上一个对话写入文件
                if conversation is not None:
                    conversation['conversations'][1]['content'] = '```' + conversation['conversations'][1]['content'] + '```'
                    conversation['conversations'][2]['content'] = json.dumps(conversation['conversations'][2]['content'], ensure_ascii=False, indent=4)
                    f_out.write(conversation)
                # 开始新的对话
                conversation = {
                    'conversations': [
                        {
                            "role": "system",
                            "content": config.SYS_PROMPT
                        },
                        {
                            "role": "user",
                            "content": line['sentence']
                        },
                        {
                            "role": "assistant",
                            "content": []
                        }
                    ]
                }
            # 当前对话跟上一个对话相同，则追加output中的内容
            conversation['conversations'][2]['content'].append(json.dumps({
                'node_1': sentence_b_parts[0],
                'edge': sentence_b_parts[1],
                'node_2': sentence_b_parts[2] if len(sentence_b_parts) > 2 else ''
            }, ensure_ascii=False, indent=4))
            # 更新上一个对话的记录
            last_sentence = line['sentence']

        # for line in tqdm(f_in, desc="Processing lines"):
        #     # 对数据行的sentence_b做切割
        #     sentence_b_parts = line['sentence_b'].split(',')
        #
        #     # 当前是新的一轮对话（跟上一个对话不同），也代表重复的对话结束了，则——
        #     if line['sentence'] != last_sentence:
        #         # 把上一个对话写入文件
        #         if conversation is not None:
        #             conversation['conversation'][0]['input'] = '```' + conversation['conversation'][0]['input'] + '```'
        #             conversation['conversation'][0]['output'] = json.dumps(conversation['conversation'][0]['output'],
        #                                                                    ensure_ascii=False, indent=4)
        #             f_out.write(conversation)
        #         # 开始新的对话
        #         conversation = {
        #             'conversation': [
        #                 {
        #                     'system': config.SYS_PROMPT,
        #                     'input': line['sentence'],
        #                     'output': []
        #                 }
        #             ]
        #         }
        #     # 当前对话跟上一个对话相同，则追加output中的内容
        #     conversation['conversation'][0]['output'].append(json.dumps({
        #         'node_1': sentence_b_parts[0],
        #         'edge': sentence_b_parts[1],
        #         'node_2': sentence_b_parts[2] if len(sentence_b_parts) > 2 else ''
        #     }, ensure_ascii=False, indent=4))
        #     # 更新上一个对话的记录
        #     last_sentence = line['sentence']
        # 如果文件为空，则写入 None
        if conversation is not None:
            f_out.write(conversation)


def find_input_files(directory):
    input_file_list = []
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, '*input*'):
            input_file_list.append(os.path.join(directory, filename))
    return input_file_list


def merge_files(input_file_list, merge_file_name):
    output_data = []
    for file_path in tqdm(input_file_list, desc="Merging files"):
        with jsonlines.open(file_path, mode='r') as f_in:
            for obj in f_in:
                output_data.append(obj)
    with open(merge_file_name, 'w', encoding='utf-8') as f_out:
        f_out.write(json.dumps(output_data, ensure_ascii=False, indent=4))


def find_output_files(directory):
    output_file_list = []
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, '*output*'):
            output_file_list.append(os.path.join(directory, filename))
    return output_file_list


def find_cache_files():
    cache_file_list = []
    for filename in os.listdir('output_dir'):
        cache_file_list.append(os.path.join('output_dir', filename))
    return cache_file_list

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted, cache cleared.")
    except FileNotFoundError:
        print(f"File {file_path} does not exist, no cache need to be deleted.")


if __name__ == '__main__':
    # for cache_file in find_cache_files():
    #     delete_file(cache_file)
    # 输入文件都在input_dir目录下，输入文件的文件名都含有 'input'
    # 输出文件都在output_dir目录下，输出文件的文件名都含改为 'output'
    for input_file_name in tqdm(find_input_files('input_dir'), desc="Processing files"):
        output_file = os.path.join('output_dir', os.path.basename(input_file_name).replace('input', 'output'))
        convert_format(input_file_name, output_file)
    # 输出文件都在 'output_dir' 目录下，合并为一个文件 'merged_output.json'
    merge_files(find_output_files('output_dir'), 'merged_output.json')
