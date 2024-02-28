import json
import time
import zhipuai
from typing import Any, List, Mapping, Optional, Dict, Union, Tuple
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from pydantic import Field, model_validator


class ZhipuAILLM(LLM):
    # 日常使用时常用的多种参数
    # 默认选用 ERNIE-Bot-turbo 模型，即目前一般所说的百度文心大模型
    model_name: str = Field(default="chatglm_std", alias="model")
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
        # 发起请求
        response = zhipuai.model_api.invoke(
            model=self.model_name,
            prompt=prompt,
            temperature=self.temperature
        )
        if response.status_code == 200:
            # 返回的是一个 Json 字符串
            js = json.loads(response.text)
            return js["result"]
        else:
            return "请求失败"

    @property
    def _default_params(self) -> Dict[str, Any]:
        # 首先定义一个返回默认参数的方法
        """获取调用ZHIPU API的默认参数。"""
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
