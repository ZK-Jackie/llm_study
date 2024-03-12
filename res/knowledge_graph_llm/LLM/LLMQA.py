from modelscope import snapshot_download
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .InternLM import InternLM
from .InternLM import ChatGLM
import os


class InternLMQA:
    """
    存储检索问答链的对象
    """
    llm: InternLM = None

    def __init__(self):
        # 下载sentence-transformer模型
        if not os.path.exists('sentence-transformer'):
            print("sentensce-transfomer不存在，正在下载..")
            # 设置环境变量
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
            # 下载模型
            os.system(
                'huggingface-cli download --resume-download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir sentence-transformer')
        # 准备NLTK
        if not os.path.exists('/root/nltk_data'):
            os.system('cd /root && git clone https://gitee.com/yzy0612/nltk_data.git  --branch gh-pages && cd nltk_data'
                      '&& mv packages/*  ./ && cd tokenizers && unzip punkt.zip && cd ../taggers && unzip '
                      'averaged_perceptron_tagger.zip')
        # 下载 internlm-chat-20b
        if not os.path.exists('/root/Shanghai_AI_Laboratory/internlm-chat-7b'):
            print("/root/Shanghai_AI_Laboratory/internlm-chat-7b不存在，正在下载..")
            snapshot_download('Shanghai_AI_Laboratory/internlm-chat-7b'
                              , cache_dir='./', revision='v1.0.3')
        # 构造函数，加载问答链
        self.llm = InternLM(
            model_path='/root/share/model_repos/internlm-chat-7b'
        )

    def llm_qa_chain(self, userInput, llm):
        prompt_template = """
            context: ```{sentence}``` \n\n output: 
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["sentence"]
        )
        # 加载自定义 LLM
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt
        )
        return llm_chain.run(userInput['query'])

    def qa_chain_self_answer(self, question: str, chat_history: list = []):
        """
        调用问答链进行回答
        """
        if question == None or len(question) < 1:
            return "", chat_history
        try:
            chat_history.append(
                (question, self.llm_qa_chain({"query": question}, self.llm)))
            # 将问答结果直接附加到问答历史中，Gradio 会将其展示出来
            return "", chat_history
        except Exception as e:
            return e, chat_history
