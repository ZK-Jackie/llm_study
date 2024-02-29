# 首先导入所需第三方库
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import os
import CustomExceptions as ex


# 获取文件路径函数
def get_file_dirs(dir_path: str) -> list:
    # args：dir_path，目标文件夹路径
    count = 0
    file_list = []
    for filepath, dir_names, filenames in os.walk(dir_path):
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
                # print('loading -- ', filename)
                file_list.append(os.path.join(filepath, filename))
            count = count + 1
            if count == 50:
                break
    return file_list


# 加载路径中的文件函数
def get_text_r(dir_path: str) -> list:
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_file_dirs(dir_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        docs.extend(get_text(one_file))
    return docs


# 加载某一文件函数
def get_text(file):
    # print("getting text!")
    # docs 存放加载之后的纯文本对象
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
        loader = JSONLoader(
            file_path=file,
            jq_schema=".context",
            json_lines=True,
            text_content=False
        )
    elif file_type == 'pdf':
        # print("reading pdf!")
        loader = PyMuPDFLoader(file)
    else:
        # 如果是不符合条件的文件，直接跳过
        return
    # print("read over!")
    return loader.load()


def file_to_chroma(path: str, is_folder: bool = False, chunk_size: int = 500, chunk_overlap: int = 150,
                   embedding_model_path: str = "/root/data/demo/sentence-transformer",
                   persist_directory: str = '/root/data/demo/data_base/vector_db/chroma'):
    pbar = tqdm(total=100)
    # 加载目标文件
    docs = []
    if is_folder:
        docs.extend(get_text_r(path))
    else:
        docs.extend(get_text(path))
    if docs is None or len(docs) < 1:
        raise ex.FileNotFoundException("没有找到文件")
    pbar.update(30)

    # 对纯文本无格式文本进行分块：块大小为500，每个块末端150个字符和下一个块的开端150相同（重叠）
    # print("dividing text!")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = text_splitter.split_documents(docs)  # 分块后的文本
    pbar.update(30)

    # 加载开源词向量模型，embeddings：词向量对象
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_path)
    pbar.update(20)

    # 构建向量数据库
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
