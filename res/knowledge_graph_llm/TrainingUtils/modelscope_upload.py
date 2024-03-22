from modelscope.hub.api import HubApi

YOUR_ACCESS_TOKEN = '8fe7b722-fde8-4ae6-80f4-c2d52d85cc54'


def modelscope_upload():
    api = HubApi()
    api.login(YOUR_ACCESS_TOKEN)
    api.push_model(
        model_id="Jackie101/T2KG_InternLM",
        model_dir="/root/knowledge_graph_llm/ft/T2KG_InternLM"  # 本地模型目录，要求目录中必须包含configuration.json
    )


def modelscope_download():
    # 模型下载
    from modelscope import snapshot_download
    model_dir = snapshot_download('Jackie101/T2KG_InternLM')


modelscope_upload()
# modelscope_download()
