from . import UtilsExceptions as ex
from .Converter import documents2Dataframe, df2Graph, graph2Df
from LLM.InternLMQA import InternLMQA
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import tqdm
import config

class TextProcess:

    llm_qa:InternLMQA = None

    def __init__(self, llm_qa) -> None:
        self.llm_qa = llm_qa
        

    def FileReader(self, file):
        # 获取文件名
        filename = file.name
        basename = os.path.basename(filename)
        print(f"detecting file: {filename} .\n")
        
        pbar = tqdm(total=100)
        # 加载目标文件
        docs = []
        docs.extend(self.get_text(filename))
        if docs is None or len(docs) < 1:
            raise ex.FileNotFoundException("没有找到文件\n")
        pbar.update(10)

        # 对纯文本无格式文本进行分块：块大小为500，每个块末端150个字符和下一个块的开端150相同（重叠）
        print("Dividing...\n")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
            length_function=len,
            is_separator_regex=False,
        )
        split_docs = text_splitter.split_documents(docs)  # 分块后的文本
        pbar.update(10)

        # 变成表格
        df = documents2Dataframe(split_docs)
        df.head()
        pbar.update(10)

        # 让LLM提取信息
        concepts_list = df2Graph(df, model=self.llm_qa)
        dfg1 = graph2Df(concepts_list)
        if not os.path.exists(outputdirectory):
            os.makedirs(outputdirectory)
        
        dfg1.to_csv(outputdirectory/"graph.csv", sep="|", index=False)
        df.to_csv(outputdirectory/"chunks.csv", sep="|", index=False)
        
        # 将加载的向量数据库持久化到磁盘上
        pbar.update(20)
        pbar.close()
        # print("db is ready!")


        return

    def _get_text(self, file):
        # docs 存放加载之后的纯文本对象
        # 查询目标文件类型
        file_type = file.split('.')[-1]
        if file_type == 'md':
            loader = UnstructuredMarkdownLoader(file)
        elif file_type == 'txt':
            loader = UnstructuredFileLoader(file)
        elif file_type == 'jsonl':
            loader = JSONLoader(
                file_path=file,
                jq_schema=".context",
                json_lines=True,
                text_content=False
            )
        elif file_type == 'pdf':
            loader = PyMuPDFLoader(file)
        else:
            # 如果是不符合条件的文件，直接跳过
            return
        print("File Unstructedly Load Over.\n")
        return loader.load()