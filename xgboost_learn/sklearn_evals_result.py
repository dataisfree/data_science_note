# -*- coding: utf-8 -*-

"""
this script demonstrate how to access the xgboost eval metrics by using sklearn
"""
import xgboost as xgb
import numpy as np
from sklearn.datasets import make_hastie_10_2

X, y = make_hastie_10_2(n_samples=2000, random_state=40)

# map labels from {-1, 1} to {0, 1}
labels, y = np.unique(y, return_inverse=True)

X_train, X_test = X[:1600], X[1600:]
y_train, y_test = y[:1600], y[1600:]

param_dist = {'objective': 'binary:logistic', 'n_estimators': 2}

clf = xgb.XGBModel(**param_dist)

clf.fit(X=X_train, y=y_train,
		eval_set=[(X_train, y_train), (X_test, y_test)],
		eval_metric=['logloss'],
		verbose=True)


# load evals result by calling the evals_result() function
evals_result = clf.evals_result()

print('eval_reult type is: ', type(evals_result))

print('access logloss metrix directly from validation_0: ')
print(evals_result['validation_0']['logloss'])

print('')
print('access metrics through a loop: ')
for e_name, e_mtrs in evals_result.items():
	print('- {0}'.format(e_name))
	for e_mtr_name, e_mtr_vals in e_mtrs.items():
		print('	- {}'.format(e_mtr_name))
		print('		- {}'.format(e_mtr_vals))

print('')
print('access complete dict: ')
print(evals_result)

print(12)
