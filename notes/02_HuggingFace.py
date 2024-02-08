import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # Set mirror
from huggingface_hub import hf_hub_download  # Load model directly
hf_hub_download(repo_id="internlm/internlm-20b", filename="config.json")
# Download config.json of internlm-20b's "config.json" file
