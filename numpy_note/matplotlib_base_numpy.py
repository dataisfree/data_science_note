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

# 绘图入门（多项式函数）
func = np.poly1d(np.array([1, 2, 3, 4]).astype('float64'))		# 创建多项式
x = np.linspace(-10, 10, 30)
y = func(x)		# 计算多项式系数的值

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.show()


# 格式字符串 （指定线条的颜色和风格）
# plot 可以接受多个参数
# 绘制多项式函数及其导函数
func_2 = np.poly1d((np.arange(4)+1).astype(float))
func_2_deriv = func_2.deriv(m=1)		# m=1, 一阶导数
x = np.linspace(-10, 10, 30)
y = func_2(x)
y_deriv = func_2_deriv(x)
plt.plot(x, y, 'ro', x, y_deriv, 'g--')
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.show()


# 子图
# 绘制多项式函数及其一阶导数和二阶导数三张图
# 多项式系数
func = np.poly1d(np.random.random_sample(20)*10)
x = np.linspace(-20, 20, 60)
y = func(x)
func1 = func.deriv(m=1)
y1 = func1(x)
func2 = func.deriv(m=2)
y2 = func2(x)

# 定义子图
"""
subplot创建子图， 参数1：子图行数、参数2： 子图列数、参数3：从1开始的子图序号
"""
# 绘子图1
plt.subplot(311)
plt.plot(x, y, 'r-')
plt.title('polynomial')
# 绘子图2
plt.subplot(312)
plt.plot(x, y1, 'b^')
plt.title('first derivative')
# 绘子图3
plt.subplot(313)
plt.plot(x, y2, 'go')
plt.title('second derivative')
plt.xlabel('x')
plt.ylabel('f=f(x)')
plt.show()

print(x)

# 三维绘图
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')	# 利用projection='3d'关键字指定图像的三维投影
u = np.linspace(-1, 1, 200)
x, y = np.meshgrid(u, u)
z = x**2 + y**2
ax.plot_surface(x, y, z, rstride=4, cstride=4, cmap=cm.YlGnBu_r)
plt.show()
print(1)

# 等高线图
fig = plt.figure()
ax = fig.add_subplot(111)
u = np.linspace(-1, 1, 100)
x, y = np.meshgrid(u, u)
z = x**2 + y**2
ax.contourf(x, y, z)	# 绘制等高线
plt.show()
print(z)


# 绘制动画
import matplotlib.animation as animation
fig = plt.figure()
ax = fig.add_subplot(111)
N = 10
x = np.random.rand(N)
y = np.random.rand(N)
z = np.random.rand(N)
circles, triangles, dots = ax.plot(x, 'ro', y, 'g^', z, 'b.')
ax.set_ylim(0, 1)
plt.axis('off')


def update(data):
	circles.set_ydata(data[0])
	triangles.set_ydata(data[1])
	return circles, triangles


def generated():
	while True:
		yield np.random.rand(2, N)

anim = animation.FuncAnimation(fig, update, generated, interval=150)
plt.show()

print(x)
