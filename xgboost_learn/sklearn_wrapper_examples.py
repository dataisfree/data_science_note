# -*- coding: utf-8 -*
'''
created on 1 Jul 2019

@author: chenzhiwei
'''

import xgboost as xgb
import numpy as np
import pickle, time
import joblib

from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, mean_squared_error
from sklearn.datasets import load_iris, load_digits, load_boston

rng = np.random.RandomState(12)

print('zeros and ones from the digits datasets: binary classification')
digits = load_digits(2)
print(digits)

y = digits.target
x = digits.data
kf = KFold(n_splits=2, shuffle=True, random_state=rng)
for train_index, test_index in kf.split(x):
	print(('train_indes:', train_index), ('test_index: ', test_index))
	xgb_model = xgb.XGBClassifier().fit(x[train_index], y[train_index])
	predictions = xgb_model.predict(x[test_index])
	actuals_label = y[test_index]
	print(confusion_matrix(actuals_label, predictions))
	time.sleep(5)

print('iris: multiclass classification')
iris = load_iris()
y = iris.target
X = iris.data
kf = KFold(n_splits=2, shuffle=True, random_state=rng)
for train_index, test_index in kf.split(X):
	xgb_model = xgb.XGBClassifier().fit(X[train_index], y[train_index])
	predictions = xgb_model.predict(X[test_index])
	actuals_label = y[test_index]
	print(confusion_matrix(y_true=actuals_label, y_pred=predictions))

print('boston housing: regression')
boston = load_boston()
y = boston.target
X = boston.data
xgb_model = xgb.XGBRegressor()
clf = GridSearchCV(estimator=xgb_model, param_grid={'max_depth': [2, 4, 6],
													'n_estimators': [50, 100, 200]}, verbose=1)
clf.fit(X, y)
print(clf)
print(clf.best_score_)
print(clf.best_estimator_)
print(clf.best_index_)
print(clf.best_params_)

print('picking sklearn api models')
pickle.dump(clf, open('best_boston.pkl', 'wb'))
clf2 = pickle.load(open('best_boston.pkl', 'rb'))
# joblib.dump(clf, 'test.pkl')
# clf2 = joblib.load('test.pkl')
print(np.allclose(clf.predict(X), clf2.predict(X)))

print('early stopping')
X = digits.data
y = digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
													random_state=0)
clf = xgb.XGBClassifier()
clf.fit(X_train, y_train,
		early_stopping_rounds=50, eval_metric=['auc'],
		eval_set=[(X_train, y_train), (X_test, y_test)])
print(clf)

# print('gridsearchCV: classification')
# X = digits.data
# y = digits.target
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
#
# dtrain = xgb.DMatrix(data=X_train, label=y_train)
# dtest = xgb.DMatrix(data=X_test, label=y_test)
# evals_result = {}
#
# param = {'max_depth': [2, 4, 6, 8], 'eta': [0.2, 0.1, 0.01, 0.001],
# 		 'objective': 'binary:logistic'}
# num_round = 100
#
# # model = xgb.train(dtrain=dtrain, params=param, num_boost_round=num_round,
# # 				  evals=[(dtrain, 'train'), (dtest, 'eval')],
# # 				  evals_result=evals_result)
#
# clf = GridSearchCV(estimator=xgb.train(),
# 				   param_grid={'dtrain': dtrain, 'params': param, 'num_boost_round': num_round,
# 				  'evals': [(dtrain, 'train'), (dtest, 'eval')],
# 				  'evals_result': evals_result})

print(12)
