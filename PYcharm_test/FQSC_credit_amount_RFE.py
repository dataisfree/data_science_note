# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:06:05 2018

@author: Administrator
"""

print(__doc__)
import os
import time
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import random_projection
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.decomposition import IncrementalPCA, KernelPCA
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, HuberRegressor
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor



time1 = time.time()
start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('train start time is: ', start_time)

# 读数据
os.chdir(u'D:\【01】行健金融\【01】数据中心\【05】数据分析项目\【03】2018\May\规则引擎_分期商城_风控+授信')
df = pd.read_csv('test_FQSC_xinyan_yinlian_clean.csv')

# low_volume_percent,middle_volume_percent,\
# take_amount_in_later_12_month_highest,trans_amount_increase_rate_lately,\
# trans_activity_month,trans_activity_day,\
# transd_mcc,trans_days_interval_filter,trans_days_interval,\
# regional_mobility,student_feature,repayment_capability,\
# is_high_user,number_of_trans_from_2011,historical_trans_amount,\
# historical_trans_day,rank_trad_1_month,trans_amount_3_month,\
# avg_consume_less_12_valid_month,abs,top_trans_count_last_1_month,\
# avg_price_last_12_month,avg_price_top_last_12_valid_month,\
# trans_top_time_last_1_month,trans_top_time_last_6_month,\
# consume_top_time_last_1_month,consume_top_time_last_6_month,\
# cross_consume_count_last_1_month,trans_fail_top_count_enum_last_1_month,\
# trans_fail_top_count_enum_last_6_month,trans_fail_top_count_enum_last_12_month,\
# consume_mini_time_last_1_month,max_cumulative_consume_later_1_month,\
# max_consume_count_later_6_month,railway_consume_count_last_12_month,\
# pawns_auctions_trusts_consume_last_1_month,pawns_auctions_trusts_consume_last_6_month,\
# jewelry_consume_count_last_6_month,status,new_reg_preference_for_trad

text_var_list = []
data_list = []
for col in df.columns.values:
    if col.upper() not in text_var_list:
        data_list.append(col)
df_Preprocess = df[data_list]
print(df_Preprocess.columns.values)
col_index = range(len(df_Preprocess.columns)-2)
col_index.append(len(df_Preprocess.columns)-1)
X = df_Preprocess[df_Preprocess.columns[col_index]]
print(X.columns.values)
y = df_Preprocess['status']

# from stacking import stackingClassifir
from mlxtend.classifier import StackingClassifier

from sklearn.model_selection import train_test_split, cross_val_score
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=43)
from sklearn.feature_selection import SelectPercentile, SelectKBest, chi2

#递归特征消除法 基于随机森灵 或者 逻辑回归
# from sklearn.feature_selection import RFE
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# transRFE_logis = RFE(estimator=LogisticRegression(random_state=40))  #dataset是均衡数据集，如果不是需要设定classwight
# transRFE_RF = RFE(estimator=RandomForestClassifier(n_estimators=200, random_state=40))
# transRFE_logis.fit(X_train, y_train)
# transRFE_logis.score(X_test, y_test)
# transRFE_RF.fit(X_train, y_train)
# transRFE_RF.score(X_test, y_test)
# #X_logis = transRFE_logis(X)
#
# columns = X.columns.values
# RFE_score_bad_logis = transRFE_logis.ranking_
# RFE_sopport_bad_logis = transRFE_logis.support_
# RFE_result_bad_logis = pd.DataFrame(RFE_score_bad_logis, columns=['ranking'])
# RFE_result_bad_logis['support'] = RFE_sopport_bad_logis
# RFE_result_bad_logis['columns'] = columns
# RFE_result_bad_logis.to_csv('xinyanData_FS_test_logis.csv', header=True, index=False)
#
# RFE_score_bad_RF = transRFE_RF.ranking_
# RFE_sopport_bad_RF = transRFE_RF.support_
# RFE_result_bad_RF = pd.DataFrame(RFE_score_bad_RF, columns=['ranking'])
# RFE_result_bad_RF['support'] = RFE_sopport_bad_RF
# RFE_result_bad_RF['columns'] = columns
# RFE_result_bad_RF.to_csv('xinyanData_FS_test_RF.csv', header=True, index=False)

# create StandardScaler
scaler = preprocessing.StandardScaler().fit(X_train)
# (X_train-train_MEAN)/train_STD 其中：train_mean = scaler.mean_ || train_std = scaler.scale_
X_train_standar =scaler.transform(X_train)
X_test_stander = scaler.transform(X_test)

param_MLP = {'hidden_layer_sizes': (100, 80, 50, 10), 'max_iter': 3000, 'alpha': 0.0001, 'learning_rate_init': 0.001, 'random_state': 40}
# param_Cla = {}
# param_GNB = {'hidden_layer_sizes': (100, 80, 50, 10), 'max_iter': 3000, 'alpha': 0.0001, 'learning_rate_init': 0.001, 'random_state': 40}
# param_lg = {}
param_ada = {'n_estimators': 1000, 'learning_rate': 0.01, 'random_state': 40}
param_RF = {'n_estimators': 500, 'max_depth': 5, 'min_samples_leaf': 20, 'random_state': 40}

# clf_MLP = MLPRegressor(random_state=40)
clf_Cla = MLPClassifier(random_state=40)
# clf_Cla = MLPClassifier(**param_MLP)
# clf_GNB = GaussianNB()  #朴素贝叶斯没有random_state
clf_lg = LogisticRegression(random_state=40)
# clf_HR = HuberRegressor() #线性回归对离群值很健壮
# clf_ada =  AdaBoostClassifier(random_state=40)
clf_ada =  AdaBoostClassifier(**param_ada)
# clf_RF = RandomForestClassifier(random_state=40)
clf_RF = RandomForestClassifier(**param_RF)
# clf_RF = RandomForestClassifier(**param_RF)
sclf = StackingClassifier(classifiers=[
#        clf_MLP,
        clf_Cla,
#        clf_HR,
        clf_ada,
        clf_RF],
    use_probas=True,
    average_probas=True,
    meta_classifier=clf_lg)
label = ['stacking']
sclf.fit(X_train_standar, y_train)
score_stacking = cross_val_score(sclf, X_train_standar, y_train, scoring='accuracy')
cross_val_score(sclf, X_train_standar, y_train, scoring='f1')
score_mean_sclf = score_stacking.mean()
print('stacking final score\'s mean is % .2f' % score_mean_sclf)


print('accuracy: %.2f (+/- %.2f) [%s]' % (score_stacking.mean(), score_stacking.std(), label))

result_stacking = sclf.predict(X_test_stander)
result_stacking_proba = sclf.predict_proba(X_test_stander)
clf_stacking_test_score = sclf.score(X_test_stander, y_test)

precision, recall, thresholds = precision_recall_curve(y_test,sclf.predict(X_test))
report = result_stacking_proba[:, 1] > 0.6
print(classification_report(y_test, report, target_names=['0', '1']))

# ==============================================================================
# 模型持久化
# os.chdir(u'D:\【01】行健金融\【01】数据中心\【05】数据分析项目\【03】2018\May\规则引擎_分期商城_风控+授信')
# joblib.dump(sclf, 'stackingpkl.pkl')
# joblib.dump(scaler, 'scaler.pkl')

# ==============================================================================

time2 = time.time()
end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('train end time is: ', end_time)
print('total run time is: % .2f' % float((time2-time1)/60.0))