import openxlab
openxlab.login(ak="ak", sk="sk") #进行登录，输入对应的AK/SK
from openxlab.dataset import get
# get(dataset_repo='OpenDataLab/MATH', target_path='../pics/03') # 数学题数据集下载
get(dataset_repo='OpenDataLab/XiaChuFang_Recipe_Corpus', target_path='../pics/03') # 下厨房菜谱数据集下载