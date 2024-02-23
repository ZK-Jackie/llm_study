import openxlab
openxlab.login(ak="vzranmjgawe4znm8wl56", sk="qmj6zq9dwxlyanennbvyo2p4wn5le3w1dv4gzavp") #进行登录，输入对应的AK/SK
from openxlab.dataset import get
# get(dataset_repo='OpenDataLab/MATH', target_path='/root/data/') # 数据集下载

get(dataset_repo='OpenDataLab/XiaChuFang_Recipe_Corpus', target_path='/root/data/') # 数据集下载