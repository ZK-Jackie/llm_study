# 首先导入所需第三方库
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import os

# 获取文件路径函数
def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 通过后缀名判断文件类型是否满足要求
            if filename.endswith(".md"):
                # 如果满足要求，将其绝对路径加入到结果列表
                file_list.append(os.path.join(filepath, filename))
            elif filename.endswith(".txt"):
                file_list.append(os.path.join(filepath, filename))
            elif filename.endswith(".jsonl"):
                # 如果满足要求，将其绝对路径加入到结果列表
                print('loading -- ', filename)
                count = count + 1
                file_list.append(os.path.join(filepath, filename))
    return file_list

# 加载路径中的文件函数
def get_text_r(dir_path):
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_files(dir_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        file_type = one_file.split('.')[-1]
        if file_type == 'md':
            loader = UnstructuredMarkdownLoader(one_file)
        elif file_type == 'txt':
            loader = UnstructuredFileLoader(one_file)
        elif file_type == 'jsonl':
            loader = JSONLoader(file_path=one_file, jq_schema=".context", json_lines=True, text_content=False)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs.extend(loader.load())
    return docs

    # 加载某一文件函数
def get_text(file):
    print("getting text!")
    # docs 存放加载之后的纯文本对象
    docs = []
    # 查询目标文件类型
    file_type = file.split('.')[-1]
    if file_type == 'md':
        # print("reading md!")
        loader = UnstructuredMarkdownLoader(file)
    elif file_type == 'txt':
        # print("reading txt!")
        loader = UnstructuredFileLoader(file)
    elif file_type == 'jsonl':
        # print("reading jsonl!")
        loader = JSONLoader(file_path=file, jq_schema=".context", json_lines=True, text_content=False)
    else:
        # 如果是不符合条件的文件，直接跳过
        return
    # print("read over!")
    docs.extend(loader.load())
    return docs

def fileToChroma(file):
    pbar = tqdm(total=100)
    # 加载目标文件
    docs = []
    docs.extend(get_text(file))
    pbar.update(30)

    # 对纯文本无格式文本进行分块：块大小为500，每个块末端150个字符和下一个块的开端150相同（重叠）
    # print("dividing text!")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=30, chunk_overlap=5)
    split_docs = text_splitter.split_documents(docs) # 分块后的文本
    pbar.update(30)

    # 加载开源词向量模型，embeddings：词向量对象
    embeddings = HuggingFaceEmbeddings(model_name="/root/data/model/sentence-transformer")
    pbar.update(20)

    # 构建向量数据库
    # 定义持久化路径，存放向量数据库文件
    persist_directory = 'data_base/vector_db_chroma'
    # 加载数据库，分块后的文本列表、词向量对象、持久化数据库路径，最终得到可以直接检索的vectordb向量对象
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    # 将加载的向量数据库持久化到磁盘上
    pbar.update(20)
    pbar.close()
    # print("db is ready!")
    vectordb.persist()