#!/usr/bin/python
import numpy as np
import xgboost as xgb

kRows, kCols = 2000, 10
kOutlier, kNumberOfOutliers = 10000, 64
kRatio = 0.7


def generate_data():
    '''Generate data containing outliers.'''
    x = np.random.randn(kRows, kCols)
    y = np.random.randint(0, 2, size=kRows)
    # y = np.random.randn(kRows)
    # y += np.abs(np.min(y))

    # Create outliers
    # for i in range(0, kNumberOfOutliers):
    #     ind = np.random.randint(0, len(y)-1)
    #     y[ind] += np.random.randint(0, kOutlier)

    train_portion = int(kRows * kRatio)

    # rmsle requires all label be greater than -1.
    assert np.all(y > -1.0)

    train_x: np.ndarray = x[: train_portion]
    train_y: np.ndarray = y[: train_portion]
    dtrain = xgb.DMatrix(train_x, label=train_y)

    test_x = x[train_portion:]
    test_y = y[train_portion:]
    dtest = xgb.DMatrix(test_x, label=test_y)
    return dtrain, dtest

dtrain, dtest = generate_data()
watchlist = [(dtest, 'eval'), (dtrain, 'train')]

# advanced: start from a initial base prediction

print('start running example to start from a initial prediction')
# specify parameters via map, definition are same as c++ version
param = {'max_depth': 20, 'eta': 0.8, 'verbosity': 0, 'objective': 'binary:logistic'}
# train xgboost for 1 round
bst = xgb.train(param, dtrain, 100, watchlist)
# Note: we need the margin value instead of transformed prediction in set_base_margin
# do predict with output_margin=True, will always give you margin values before logistic transformation
ptrain = bst.predict(dtrain, output_margin=True)
ptest = bst.predict(dtest, output_margin=True)
dtrain.set_base_margin(ptrain)
dtest.set_base_margin(ptest)


print('this is result of running from initial prediction')
bst = xgb.train(param, dtrain, 1, watchlist)
print(1)
