import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def text_parse(unsolved_text):
    # 原始的乱码字符串
    garbled_text = unsolved_text
    # 将乱码字符串转换为字节
    garbled_bytes = garbled_text.encode('latin1')
    # 使用正确的编码方式将字节转换回字符串
    correct_text = garbled_bytes.decode('utf-8')
    return correct_text


def relative_url_parse(base_url, relative_url):
    if relative_url.startswith('http'):
        return relative_url
    else:
        return urljoin(base_url, relative_url)


if __name__ == '__main__':
    urls = ['http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index.html',
            'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index_1.html',
            'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index_2.html',
            'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index_3.html',
            'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yanglao/index_4.html']

    # 网页URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }

    # 使用requests获取网页内容
    for url in urls:
        response = requests.get(url, headers=headers)
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到所有的<span class="organMenuTxtLink">...</span>标签
        paragraphs = soup.find_all('span', class_='organMenuTxtLink')
        # 从每个<p>标签中提取文本
        for p in paragraphs:
            print(text_parse(p.get_text()).strip())
            try:
                link = p.find('a').get('href')
            except AttributeError:
                continue
            with open('links.txt', 'a') as f:
                f.write(relative_url_parse(url, link) + '\n')
