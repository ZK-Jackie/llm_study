# 自定义条件： 1. 实现 LangChain 的 LLM 接口； 2. 重写 LLM 接口的 call 方法和 identifying_params 方法
# Step1： 导入必备库
import json
import time
from typing import Any, List, Mapping, Optional, Dict, Union, Tuple
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from pydantic import Field, model_validator


def get_access_token(api_key: str, secret_key: str):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    # 指定网址
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    # 设置 POST 访问
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # 通过 POST 访问获取账户对应的 access_token
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# Step2： 定义自定义的 LLM 类，属性：日常使用时常用的多种参数；方法：重写的 call 方法
class wenxin_llm(LLM):
    # 日常使用时常用的多种参数
    # 原生接口地址
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant"
    # 默认选用 ERNIE-Bot-turbo 模型，即目前一般所说的百度文心大模型
    model_name: str = Field(default="ERNIE-Bot-turbo", alias="model")
    # 访问时延上限
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    # 温度系数
    temperature: float = 0.1
    # API_Key
    api_key: str = None
    # Secret_Key
    secret_key: str = None
    # access_token
    access_token: str = None
    # 必备的可选参数
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)

    # Step 3： 重写 call 方法
    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 除 prompt 参数外，其他参数并没有被用到，但当我们通过 LangChain 调用时会传入这些参数，因此必须设置
        # 如果 access_token 为空，初始化 access_token
        if self.access_token is None:
            self.init_access_token()
        # API 调用 url
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={}".format(
            self.access_token)
        # 配置 POST 参数
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",  # user prompt
                    "content": "{}".format(prompt)  # 输入的 prompt
                }
            ],
            'temperature': self.temperature
        })
        headers = {
            'Content-Type': 'application/json'
        }
        # 发起请求
        response = requests.request("POST", url, headers=headers, data=payload, timeout=self.request_timeout)
        if response.status_code == 200:
            # 返回的是一个 Json 字符串
            js = json.loads(response.text)
            return js["result"]
        else:
            return "请求失败"

    @property
    def _default_params(self) -> Dict[str, Any]:
        # 首先定义一个返回默认参数的方法
        """获取调用Ennie API的默认参数。"""
        normal_params = {
            "temperature": self.temperature,
            "request_timeout": self.request_timeout,
        }
        return {**normal_params}

    # Step 4： 重写 identifying_params 属性
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}

    @property
    def _llm_type(self) -> str:
        return "custom"


# 备注：
'''
1. 语法相关：
双星号（**）：在字典前使用双星号，可以将字典的键值对解包为单独的元素。这通常用于函数调用时的参数传递，或者在这里的情况，用于合并字典。  
大括号（{}）：在Python中，大括号用于定义字典。字典是一种包含键值对的数据结构。
2. 本文官方链接：
https://python.langchain.com/docs/modules/model_io/llms/custom_llm
'''
