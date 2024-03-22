from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class InternLM_LLM(LLM):
    # 基于本地 InternLM 自定义 LLM 类
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path: str):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        # print("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(torch.bfloat16).cuda()
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数
        system_prompt = """
            - You are developed based on ChatGLM3-6b, your name is "AI Note assistant".
            - The user is conversing with you in a software called "AI Note", you can answer the user's questions based on the content of the user's notes.
            - The design goal of the "AI Note" assistant is to be useful, honest, and harmless, you are committed to answering the user's questions.
            - The "AI Note assistant" can fluently understand and communicate in the user's chosen language, such as English and Chinese.
        """

        messages = [(system_prompt, '')]
        # # 调用本地model，传入：tokenizer，用户输入和历史记录（历史记录功能待完善）
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        # 指定网址
        # url = "http://0.0.0.0:23333/v1/chat/completion"
        # # 设置 POST 访问
        # payload = json.dumps({
        #         "model": "internlm-chat-7b",
        #         "messages": prompt,
        #         "temperature": 0.7,
        #         "top_p": 1,
        #         "n": 1,
        #         "max_tokens": 512,
        #         "stop": 'false',
        #         "stream": 'false',
        #         "presence_penalty": 0,
        #         "frequency_penalty": 0,
        #         "user": "string",
        #         "repetition_penalty": 1,
        #         "renew_session": 'false',
        #         "ignore_eos": 'false'
        # })
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Accept': 'application/json'
        # }
        # # 通过 POST 访问获取账户对应的 access_token
        # response = requests.request("POST", url, headers=headers, data=payload)
        # js = json.loads(response.text)
        return response
        # return js["choices"]["message"]

    @property
    def _llm_type(self) -> str:
        return "InternLM"