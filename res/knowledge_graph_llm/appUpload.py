from LLM.LLMQA import InternLMQA
from GraphUtils.TextProcess import FileReader
import gradio as gr
import config


# 实例化核心功能对象
internlm = InternLMQA()
# 创建一个 Web 界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):   
        with gr.Column(scale=15):
            # 展示的页面标题
            gr.Markdown("""<h1><center>Knowledge_graph_llm</center></h1>
                <center>书生浦语</center>
                """)

    with gr.Row():
        with gr.Column(scale=4):
            # 创建一个聊天机器人对象
            chatbot = gr.Chatbot(height=450, show_copy_button=True)
            with gr.Row():
                file_output = gr.File()
                upload_button = gr.UploadButton(
                    "上传笔记文件",
                    file_types=["text"],
                    file_count="single",
                    visible=True
                )
                upload_button.upload(FileReader, upload_button, file_output)

            with gr.Row():
                # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                clear = gr.ClearButton(
                    components=[chatbot],
                    value="Clear console"
                )
    gr.Markdown("""
    提醒：文本处理时间可能较长，请耐心等待。
    """)
gr.close_all()
# 直接启动
demo.launch()