#!/usr/bin/python
import numpy as np
import xgboost as xgb

### load data in do training

kRows, kCols = 2000, 10
kOutlier, kNumberOfOutliers = 10000, 64
kRatio = 0.7


def generate_data():
	'''Generate data containing outliers.'''
	x = np.random.randn(kRows, kCols)
	y = np.random.randint(0, 2, size=kRows)
	train_portion = int(kRows * kRatio)
	train_x: np.ndarray = x[: train_portion]
	train_y: np.ndarray = y[: train_portion]
	dtrain = xgb.DMatrix(train_x, label=train_y)
	test_x = x[train_portion:]
	test_y = y[train_portion:]
	dtest = xgb.DMatrix(test_x, label=test_y)
	return dtrain, dtest

dtrain, dtest = generate_data()
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 5
bst = xgb.train(param, dtrain, num_round, watchlist)

print('start testing prediction from first n trees')
### predict using first 1 tree
label = dtest.get_label()
ypred1 = bst.predict(dtest, ntree_limit=1)
# by default, we predict using all the trees
ypred2 = bst.predict(dtest)
print('error of ypred1=%f' % (np.sum((ypred1 > 0.5) != label) / float(len(label))))
print('error of ypred2=%f' % (np.sum((ypred2 > 0.5) != label) / float(len(label))))
print(1)