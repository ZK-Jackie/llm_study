from langchain.llms.base import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModel, AutoConfig
from typing import Any, List, Optional


class ChatGLM3(LLM):
    max_token: int = 8192
    do_sample: bool = True
    temperature: float = 0.8
    top_p = 0.8
    tokenizer: object = None
    model: object = None
    history: List = []
    has_search: bool = False

    def __init__(self, model_path: str):
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        model_config = AutoConfig.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            model_path, config=model_config, trust_remote_code=True, device_map="auto").eval()
        print("完成本地模型的加载")

    def _call(self, prompt: str, stop: Optional[List[str]] = ["<|user|>"],
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # one turn chat
        system_prompt = """
                    - You are an AI assistant developed based on ChatGLM3-6b, your name is "AI Note assistant".
                    - The user is conversing with you in a web application called "AI Note", you can answer the user's questions based on the content of the user's notes.
                    - The design goal of the "AI Note" assistant is to be useful, honest, and harmless, you are committed to answering the user's questions.
                    - The "AI Note assistant" can fluently understand and communicate in the user's chosen language, such as English and 中文.
                """
        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        history.append((prompt, response))
        return response

    @property
    def _llm_type(self) -> str:
        return "ChatGLM3"
