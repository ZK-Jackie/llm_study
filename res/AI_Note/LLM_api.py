import json
import time
from typing import Any, List, Mapping, Optional, Dict, Union, Tuple
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from pydantic import Field, model_validator


class InternLM_LLM(LLM):

    def __init__(self, model_path: str):
        super().__init__()

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数

        # 指定网址
        url = "http://localhost:23333/v1/chat/completions"
        # 设置 POST 访问
        payload = json.dumps({
            "model": "internlm-chat-7b",
            "messages": "{}".format(prompt),
            "temperature": 0.7,
            "top_p": 1,
            "n": 1,
            "max_tokens": 512,
            "stop": False,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "user": "string",
            "repetition_penalty": 1,
            "renew_session": False,
            "ignore_eos": False
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # 通过 POST 访问获取账户对应的 access_token
        response = requests.request("POST", url, headers=headers, data=payload)
        js = json.loads(response.text)
        # return response
        return js['choices'][0]['message']['content']

    @property
    def _llm_type(self) -> str:
        return "InternLM"


def main():
    # 从本地加载模型
    llm = InternLM_LLM(model_path="")
    # 调用模型
    response = llm("介绍一下你自己")
    print(response)


if __name__ == "__main__":
    main()
