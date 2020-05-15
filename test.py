# coding: utf-8
"""
基于numpy的数据可视化
"""

import os
import numpy as np
import matplotlib.pyplot as plt

"""
matplotlib.pyplot提供了简单的绘图功能，
调用的函数都会改变当前的绘图，通过save/show完成保存或显示功能
"""

# 绘图入门
func = np.poly1d(np.array([1, 2, 3, 4]).astype('float64'))
x = np.linspace(-10, 10, 30)
y = func(x)

print(x)
print(y)
print(type(func))

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.savefig(os.getcwd()+'/test.jpg')
plt.show()
