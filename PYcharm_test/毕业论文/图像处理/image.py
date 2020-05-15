# -*- coding: utf-8 -*-
"""
http://effbot.org/imagingbook/introduction.htm
"""

import os
import ast
from PIL import Image, ImageDraw, ImageFont


# E:\【04】继续教育\毕业论文\论文图像
dir_path = os.path.join('E:', os.sep, u'【04】继续教育')
image_path = os.path.join(dir_path, u'毕业论文', u'论文图像')

image_names = os.listdir(image_path)
a = ['im' + str(index) for index, name in enumerate(image_names)]
for index, name in zip(a, image_names):
    im = Image.open(os.path.join(image_path, name))
    # print im.format, im.size, im.mode
    # im.show()


# 创建画布，合并图并添加文字说明
def open_image(path, image_name, newsize=(100, 80)):
    """
    path:
    image_name:
    newsize:
    return:
    """
    im = Image.open(os.path.join(path, image_name))
    im.reszie(newsize)
    return im
