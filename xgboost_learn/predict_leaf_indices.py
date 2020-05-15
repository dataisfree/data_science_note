# -*- coding: utf-8 -*-

import xgboost as xgb
import numpy as np

kRows, kCols = 20000, 100
kRatio = 0.7


def generate_data():
	x = np.random.randn(kRows, kCols)
	y = np.random.randint(low=0, high=2, size=kRows)
	train_portion = int(kRatio * kRows)
	train_x = x[: train_portion]
	train_y = y[: train_portion]
	dtrain = xgb.DMatrix(data=train_x, label=train_y)
	test_x = x[train_portion:]
	test_y = y[train_portion:]
	dtest = xgb.DMatrix(data=test_x, label=test_y)
	return dtrain, dtest

dtrain, dtest = generate_data()

param = {'max_depth': 6, 'learning_rate': 1, 'silent': 1, 'objective': 'binary:logistic'}
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 5
bst = xgb.train(params=param, dtrain=dtrain, num_boost_round=num_round, evals=watchlist)

print('start testing predict the leaf indices')
leafindex_with_tree2 = bst.predict(data=dtest, ntree_limit=3, pred_leaf=True)
print(leafindex_with_tree2.shape)
print(leafindex_with_tree2)


leafindex_with_alltree = bst.predict(data=dtest, pred_leaf=True)
print(leafindex_with_alltree)

print(1)
