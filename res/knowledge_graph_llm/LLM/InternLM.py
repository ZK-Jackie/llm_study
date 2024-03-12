from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class InternLM(LLM):
    # 基于本地 InternLM 自定义 LLM 类
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path: str):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(torch.bfloat16).cuda()
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数
        system_prompt = """
            "You are a network graph maker who extracts terms and their relations from a given context. "
            "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
            "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
            "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, laws, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
            "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
                "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
                "\tTerms can be related to many other terms\n\n"
            "Thought 3: Find out the relation between each such related pair of terms. \n\n"
            "Format your output as a list of json. Each element of the list contains a pair of terms"
            "and the relation between them, like the follwing: \n"
            "[\n"
            "   {\n"
            '       "node_1": "A concept from extracted ontology",\n'
            '       "node_2": "A related concept from extracted ontology",\n'
            '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences or a word"\n'
            "   }, {...}\n"
            "]"
        """

        messages = [(system_prompt, '')]
        # 调用本地model，传入：tokenizer，用户输入和历史记录（历史记录功能待完善）
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response

    @property
    def _llm_type(self) -> str:
        return "InternLM"


