import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 获取当前目录下的.env文件内容
_ = load_dotenv(find_dotenv())


def get_openai_content_o(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.0, max_tokens: int = 150):
    # 设置代理
    os.environ['HTTP_PROXY'] = 'http://proxy.server:7890'
    os.environ['HTTPS_PROXY'] = 'https://proxy.server:7890'
    # 从 env 文件中获取 openai 的 api_key 并配置
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # 获取 ChatCompletion 对象
    completion = openai.ChatCompletion.create(
        # 选用模型为 ChatGPT-3.5
        model=model,
        # message 即为 prompt
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    ''' completion 样式：
    <OpenAIObject chat.completion id=chatcmpl-80QUFny7lXqOcfu5CZMRYhgXqUCv0 at 0x7f1fbc0bd770> JSON: {
      "choices": [
        {
          "finish_reason": "stop",
          "index": 0,
          "message": {
            "content": "Hello! How can I assist you today?",
            "role": "assistant"
          }
        }
      ],
      "created": 1695112507,
      "id": "chatcmpl-80QUFny7lXqOcfu5CZMRYhgXqUCv0",
      "model": "gpt-3.5-turbo-0613",
      "object": "chat.completion",
      "usage": {
        "completion_tokens": 9,
        "prompt_tokens": 19,
        "total_tokens": 28
      }
    }
    '''
    # 返回 completion 中的 message 的 content
    return completion.choices[0].message['content']


def get_openai_content_l(prompt: str, text: str, model: str = "gpt-3.5-turbo", temperature: float = 0.0,
                         max_tokens: int = 150):
    # 设置代理
    os.environ['HTTP_PROXY'] = 'http://proxy.server:7891'
    os.environ['HTTPS_PROXY'] = 'https://proxy.server:7891'
    # 初始化 ChatOpenAI 对象
    chatOpenai = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        streaming=True
    )
    # 设置 prompt
    """
    此处的prompt为定式字符串，例如下面的翻译模板：
        prompt = '''Translate the text \
        that is delimited by triple backticks \
        into a Chinese. \
        text: '''{text}'''
        '''
    """
    template = ChatPromptTemplate.from_template(prompt)
    # template 中的 text 是变量，替换成实际的文本并制作 message JSON
    message = template.format_messages(text=text)
    # 将信息交给 chatOpenai 对象处理
    aiMessage = chatOpenai(message)
    ''' aiMessage 样式：
    AIMessage(content='今天是个好天气。', additional_kwargs={}, example=False)
    '''
    # 返回 aiMessage 中的 content
    return aiMessage.content
