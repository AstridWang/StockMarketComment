import re
import os
import sys
from os import path
import datetime
import  requests
from bs4 import BeautifulSoup
import lxml
from wordcloud import WordCloud
import codecs
import jieba
#import jieba.analyse as analyse
from scipy.misc import imread
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import itchat




def cur_file_dir():
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)



def get_title():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "hqEtagMode=-1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

    }

    para = {"cid":57568,"page":1}

    response = requests.get('http://finance.sina.com.cn/roll/index.d.html',headers=headers,params=para)

    response.encoding = 'UTF-8'
    content = response.text
    # print(content)
    soup = BeautifulSoup(content, 'lxml')
    # listBlk = soup.find_all('div', _class="hs01")[0]
    text_list = soup.find_all('ul',class_="list_009")
    title_list = []
    for i in text_list:
        # print(i)
        title = re.findall(re.compile('fina" target="_blank">(.*?)</a'),str(i))
        title_list.append(title)

    time_mark = datetime.datetime.now()
    txt_filename = time_mark.strftime('%Y-%m-%d') + '.txt'
    with open(cur_file_dir() + '\\' + txt_filename,'a') as t:
        t.write(str(title_list))
    return txt_filename


# 绘制词云
def draw_wordcloud(txt_filename):
    #读入一个txt文件
    with open(cur_file_dir() + '\\' + txt_filename,'r') as c:
        comment_text = c.read()
    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__) # 当前文件文件夹所在目录
    color_mask = imread(cur_file_dir() + '\\' + "apple.jpg") # 读取背景图片
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        font_path=cur_file_dir() + '\\' +"simsun.ttf",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=50
    )
    word_cloud = cloud.generate(cut_text) # 产生词云
    time_mark = datetime.datetime.now()
    jpg_filename = time_mark.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    word_cloud.to_file(cur_file_dir() + '\\' + jpg_filename) #保存图片
    return jpg_filename
    #  显示词云图片
    # plt.imshow(word_cloud)
    # plt.axis('off')
    # plt.show()


try:
    if __name__ == '__main__':

        txt_filename = get_title()
        jpg_filename = draw_wordcloud(txt_filename)
        # url = 'https://sc.ftqq.com/SCU21522T9d311436eb4aecc5cda0634237d2b6135a7aca0da53ca.send?text=股民之声&desp=![picture](%s)' %jpg_filename
        # # para = {'text':'股民之声','desp':'![picture](%s)' %jpg_filename}
        # requests.get(url)
        itchat.auto_login(hotReload=True)
        itchat.get_chatrooms(update=True)
        user = itchat.search_chatrooms('股民之声')
        # print(user)
        UserName = user[0]['UserName']
        
        itchat.send_image(cur_file_dir() + '\\' + jpg_filename,toUserName=UserName)
    
except Exception as e:
    print(str(e))
