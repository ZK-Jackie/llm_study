from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class InternLM_LLM(LLM):
    # 基于本地 InternLM 自定义 LLM 类
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None
    model_type: str = None

    def __init__(self, model_path: str, model_type: str = "InternLM"):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        self.model_type = model_type
        super().__init__()
        print("正在从本地加载模型...")
        # 根据模型路径自动选择正确的分词器类并加载相应的预训练分词器（允许远程加载模型）
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # 手动加载预训练模型（允许远程加载模型）/也可以选用 HuggingFacePipeline 框架
        # 1. 转换为半精度浮点数（float16），减少模型的内存占用并提高计算速度；2. 将模型移动到 GPU 上运行
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(torch.bfloat16).cuda()
        # 在 PyTorch 中，模型有两种模式：训练模式（training mode）和评估模式（evaluation mode）
        # 模型设置为评估模式的方法，以确保你接下来使用的是处于评估模式的模型
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数
        system_prompt = """- 你是基于 InternLM (书生·浦语)开发的一个软件名字为“AI记”的小助手，你可以根据用户笔记中的内容与用户交谈。
        - “AI记”的小助手的设计目标是有用、诚实和无害，你致力于为用户解答疑惑。- “AI记”的小助手可以流畅地理解和交流用户选择的语言，如英语和中文。"""

        messages = [(system_prompt, '')]
        # 调用本地model，传入：tokenizer，用户输入和历史记录（历史记录功能待完善）
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response

    @property
    def _llm_type(self) -> str:
        return self.model_type
