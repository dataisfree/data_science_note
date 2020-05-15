import os
os.chdir('C:/Users/chenzhiwei/Desktop')
# 将可视化工具加入环境变量的代码
os.environ["PATH"] += os.pathsep + 'D:/Program Files/Graphviz2.38/bin/'
# 决策树代码
from sklearn import tree
from sklearn.datasets import load_iris
iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

import graphviz
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("iris00")

# 分色可视化
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=iris.feature_names,
                                class_names=list(iris.target_names),		# list array 均可以
                                filled=True,
                                rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('iris11')




import numpy as np
np.loadtxt()