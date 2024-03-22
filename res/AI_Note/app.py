from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import os
from ChatGLM import ChatGLM3
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import gradio as gr
import pandas as pd
import vector_db_utils as db


def load_qa_chain():
    # 加载问答链
    # 定义 Embeddings，加载词向量模型
    embeddings = HuggingFaceEmbeddings(model_name="/gemini/code/sentence-transformer")

    # 向量数据库持久化路径，加载数据库对象
    persist_directory = '/gemini/code/data_base/vector_db/chroma'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
        embedding_function=embeddings  # 词向量对象
    )

    # 加载自定义 LLM
    llm = ChatGLM3(
        model_path="/gemini/pretrain"
    )

    # 定义一个 Prompt Template
    template = """
    '''{question}'''，这是一段话，请你依次执行以下步骤：
    ① 前面用三个单引号包围起来的内容是我的话，请判断我说的话是不是对知识提出的问题；
    如果是，请做下一个步骤；如果不是，请用你自己的话回答，并跳过下面的所有步骤；
    不要回答你的思考过程；不要回答你的判断结果。
    ② 以下是我的笔记，你要用我的笔记回答前面用三个单引号包围起来的内容；
    如果你不知道答案，或不能从这些我的笔记中获得符合问题的答案，就说你不知道，不要试图编造答案。尽量使回答简明扼要；
    如果回答比较长，请酌情进行分段，以提高答案的阅读体验；
    如果回答有几点，你应该分点标号回答，让答案清晰具体；
    回答时不要回答你的思考过程，你只回答有用的内容并附上原文的文件名；
    我的笔记：
    {context}
    ③ 基于我的笔记，反思回答中有没有不正确或不是基于我的笔记得到的内容，如果有，修改回答，删去不正确或不是基于我的笔记得到的内容。
    有用的回答:
    """

    # 创建一个 PromptTemplate 对象
    qa_chain_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    # 声明一个检索问答链对象，此处的qa_chain就是回答的结果
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_chain_prompt}
    )

    return qa_chain


class Model_center:
    """
    存储检索问答链的对象
    """
    qa_chain: RetrievalQA = None

    def __init__(self):
        # 构造函数，加载检索问答链
        self.qa_chain = load_qa_chain()

    def qa_chain_self_answer(self, question: str, chat_history: list = None):
        """
        调用问答链进行回答
        """
        if chat_history is None:
            chat_history = []
        if question is None or len(question) < 1:
            return "", chat_history
        try:
            # 将问答结果直接附加到 Gradio 的问答历史中，展示出来
            message = self.qa_chain({"query": question})
            chat_history.append((question, message["result"]))
            print(message)
            return "", chat_history
        except Exception as e:
            return e, chat_history


file_dict = {}


def process_file(file):
    global file_dict
    # 获取文件名
    filename = file.name
    basename = os.path.basename(filename)
    print(f"detecting file: {filename}")
    if len(file_dict) >= 1:
        gr.Warning("当前为测试应用，文件上传数量已达上限！")
        return
    # 更新字典
    if filename in file_dict:
        file_dict[basename] += 1
    else:
        file_dict[basename] = 1

    gr.Info(f"正在加载文件{basename}")
    db.file_to_chroma(filename)
    file_dict = {}
    gr.Info(f"{basename}加载成功")
    return


def display_file():
    # 创建一个数据框来显示文件名和数量
    df = pd.DataFrame(list(file_dict.items()), columns=["File Name", "Count"])
    return df


# 实例化核心功能对象
model_center = Model_center()
# 创建一个 Web 界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):
        with gr.Column(scale=15):
            # 展示的页面标题
            gr.Markdown("""<h1><center>AI记_ChatGLM3(beta)</center></h1>
                <center>个人知识库记录助手</center>
                <center>测试应用，文件上传量仅限一条</center>
                """)

    with gr.Row():
        with gr.Column(scale=4):
            # 创建一个聊天机器人对象
            chatbot = gr.Chatbot(height=450, show_copy_button=True)
            # 创建一个文本框组件，用于输入 prompt。
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                file_output = gr.File()
                upload_button = gr.UploadButton(
                    "上传笔记文件",
                    file_types=["text"],
                    file_count="single",
                    visible=True
                )
                upload_button.upload(process_file, upload_button, file_output)

            with gr.Row():
                # 创建提交按钮。
                db_wo_his_btn = gr.Button("提交文本")
            with gr.Row():
                # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                clear = gr.ClearButton(
                    components=[chatbot], value="清空聊天框")

        # 设置按钮的点击事件。当点击时，调用上面定义的 qa_chain_self_answer 函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
        db_wo_his_btn.click(
            model_center.qa_chain_self_answer,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )

    gr.Markdown("""提醒：<br>
    1. 初始化数据库时间可能较长，请耐心等待。
    2. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。 <br>
    """)
gr.close_all()
# 直接启动
demo.launch()
