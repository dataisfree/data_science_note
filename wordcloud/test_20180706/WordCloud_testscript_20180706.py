# -*- coding: utf-8 -*-
"""
Created on Fri Jul 06 15:08:25 2018

@author: chenzhiwei
"""
import os
os.chdir('D:/private_code/private_project/Proj_python/wordcloud/test_20180706')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
f = open('NINETEEN+EIGHTY-FOUR.txt','r+', encoding='utf-8').read()

#生成词云对象
wc = WordCloud(background_color='white',  #设置背景色
               width=500,  #宽度
               height=150,  #高度
               margin=5,   #图片的边缘
               ).generate(f)
#绘制图片
plt.imshow(wc)
#消除坐标轴
plt.axis('off')
#展示图片
plt.show()
#保存图片
wc.to_file(u'词云测试1.png')
#wc.to_image(u'词云测试2')
