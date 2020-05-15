# -*- coding: utf-8 -*-

"""
this script demonstrate how to access the eval metrics in xgboost.
"""

import xgboost as xgb
import numpy as np

KRows, KCols = 20000, 30
KRatio = 0.7


def generate_data():
	x = np.random.randn(KRows, KCols)
	y = np.random.randint(low=0, high=2, size=KRows)
	train_portion = int(KRows * KRatio)
	train_x, test_x = x[:train_portion], x[train_portion:]
	train_y, test_y = y[:train_portion], y[train_portion:]
	dtrain = xgb.DMatrix(data=train_x, label=train_y, silent=True)
	dtest = xgb.DMatrix(data=test_x, label=test_y, silent=True)
	return dtrain, dtest

dtrain, dtest = generate_data()

param = {'max_depth': 5, 'objective': 'binary:logistic',
		 'eval_metric': ['logloss', 'error']}

num_round = 30
watch_list = [(dtest, 'eval'), (dtrain, 'train')]

evals_result = {}
bst = xgb.train(params=param, dtrain=dtrain, num_boost_round=num_round,
				evals=watch_list, evals_result=evals_result)

print('access logloss metric directly from evals_result: ')
print(evals_result['eval']['logloss'])
print(evals_result['eval']['error'])
print(evals_result['train']['logloss'])
print(evals_result['train']['error'])

print('access metrics through a loop: ')
for e_name, e_mtrs in evals_result.items():
	print('- {0}'.format(e_name))
	for e_mtr_name, e_mtr_vals in e_mtrs.items():
		print('	- {0}'.format(e_mtr_name))
		print('		- {0}'.format(e_mtr_vals))

print('access complete dictionary: ')
print(evals_result)

print(12)
