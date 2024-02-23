# 首先导入所需第三方库
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import time
import os
import jq


# 获取文件路径函数
def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    loadingNum = 50
    count = 0
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 遍历50个文件即可，缩短等待时间
            if (count == loadingNum):
                print("!!!break!!!")
                break
            # 通过后缀名判断文件类型是否满足要求
            if filename.endswith(".jsonl"):
                # 如果满足要求，将其绝对路径加入到结果列表
                print('loading -- ', filename)
                count = count + 1
                file_list.append(os.path.join(filepath, filename))

    return file_list


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["name"] = record.get("name")
    metadata["dish"] = record.get("dish")
    metadata["recipeIngredient"] = record.get("recipeIngredient")
    metadata["keywords"] = record.get("keywords")

    return metadata


# 加载文件函数
def get_text(dir_path):
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_files(dir_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        file_type = one_file.split('.')[-1]
        if file_type == 'jsonl':
            loader = JSONLoader(file_path=one_file, jq_schema=".recipeInstructions", json_lines=True,
                                text_content=False)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs.extend(loader.load())
    return docs


# 目标文件夹
tar_dir = [
    "/root/data/OpenDataLab___XiaChuFang_Recipe_Corpus",
]

# 加载目标文件
docs = []
for dir_path in tar_dir:
    docs.extend(get_text(dir_path))

# 对文本进行分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=0)
split_docs = text_splitter.split_documents(docs)

# 加载开源词向量模型
embeddings = HuggingFaceEmbeddings(model_name="/root/data/model/sentence-transformer")

# 构建向量数据库
# 定义持久化路径
persist_directory = 'data_base/vector_db/chroma'
# 加载数据库
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)
# 将加载的向量数据库持久化到磁盘上
vectordb.persist()
