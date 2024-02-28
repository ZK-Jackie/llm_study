import os
from dotenv import load_dotenv, find_dotenv
import zhipuai
from langchain_core.outputs import LLMResult, Generation, RunInfo
from zhipuai_llm import ZhipuAILLM


def createPrompt(role, content, text=[]):
    # role 是指定角色，content 是 prompt 内容
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def get_zhipu_content_o(content: str, temperature: float = 0.0, max_tokens: int = 150, model: str = "chatglm_std"):
    question = createPrompt("user", content)
    response = zhipuai.model_api.invoke(
        model=model,
        prompt=question,
        temperature=temperature
    )
    ''' response 样式：
    {
        'code': 200,
        'msg': '操作成功',
        'data': {
            'request_id': '8023318729410566227',
            'task_id': '8023318729410566227',
            'task_status': 'SUCCESS',
            'choices': [{
                'role': 'assistant',
                'content': '" 你好👋！我是人工智能助手 智谱清言，可以叫我小智🤖，很高兴见到你，欢迎问我任何问题。"'
            }],
            'usage': {
                'prompt_tokens': 2,
                'completion_tokens': 28,
                'total_tokens': 30
            }
        }, 
        'success': True
    }
    '''
    return response["data"]["choices"][0]["content"]


def get_zhipu_content_l():
    # 从 env 文件中获取 zhipuai 的 api_key 并配置
    zhipuai_model = ZhipuAILLM(model="chatglm_std", temperature=0, zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"))
    zhipuai_model.generate(['你好'])
    LLMResult(generations=[[Generation(
        text='" 你好👋！我是人工智能助手 智谱清言，可以叫我小智🤖，很高兴见到你，欢迎问我任何问题。"', generation_info=None)]],
        llm_output=None, run=[RunInfo(run_id='36840571-ce83-4bcb-8095-a222d59f32a4')])
