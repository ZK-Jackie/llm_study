from urllib.parse import urljoin

# 当前页面的URL
base_url = 'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index.html'

# 读取文件中的所有行
with open('links.txt', 'r') as f:
    lines = f.readlines()

# 对每一行使用 urljoin 函数
full_urls = [urljoin(base_url, line.strip()) for line in lines]

# 将转换后的URL写入一个新的文件
with open('full_links.txt', 'w') as f:
    for url in full_urls:
        f.write(url + '\n')