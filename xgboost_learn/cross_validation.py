import numpy as np
import xgboost as xgb

kRows, kCols = 20000, 100
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
param = {
	'max_depth': 20,
	'eta': 0.8,
	'silent': 1,
	'objective': 'binary:logistic'
}
num_round = 2000
print('running cross validation')
res = xgb.cv(
	params=param, dtrain=dtrain, num_boost_round=num_round, nfold=10,
	metrics=['error'], seed=0,
	callbacks=[xgb.callback.print_evaluation(show_stdv=True)]
)
print(res)

print('running cross validation, disable standard deviation display')
res = xgb.cv(
	params=param, dtrain=dtrain, num_boost_round=num_round, nfold=10,
	metrics=['error'], seed=0,
	callbacks=[xgb.callback.print_evaluation(show_stdv=False),
	xgb.callback.early_stop(10)]
)
print(res)

print('running cross validation, with preprocessing function')
'''
define the preprocessing function
purpose to return the preprocessed training, test data, and parameter
e.g. using this prepro_func to do weight rescale, 
blow function is to set scale_pos_weight
'''


def fpreproc(dtrain, dtest, param):
	'''
	set arguments: scale_pos_weight
	'''
	label = dtrain.get_label()
	ratio = float(np.sum(label == 0)) / np.sum(label == 1)
	param['scale_pos_weight'] = ratio
	return (dtrain, dtest, param)


'''
do cross validation, for each fold the dtrain, dtest, 
param will be passed into fpreproc then the return value of fpreproc 
will be used to generate results of that fold
'''
res = xgb.cv(
	params=param, dtrain=dtrain, num_boost_round=num_round, nfold=5,
	metrics=['auc'], seed=0,
	fpreproc=fpreproc
)
print(res)

print('running cross validation, with customized loss function')


def logregobj(preds, dtrain):
	labels = dtrain.get_label()
	preds = 1.0 / (1.0 + np.exp(-preds))
	grad = preds = labels
	hess = preds * (1.0 - preds)
	return grad, hess


def evalerror(preds, dtrain):
	labels = dtrain.get_label()
	return 'error', float(sum(labels != (preds > 0.0))) / len(labels)


param = {'max_depth': 2, 'eta': 1, 'silent': 1}
res = xgb.cv(
	params=param, dtrain=dtrain, num_boost_round=num_round, nfold=5,
	seed=0, obj=logregobj, feval=evalerror)
print(res)

print(1)
