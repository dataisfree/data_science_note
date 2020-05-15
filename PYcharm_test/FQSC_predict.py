# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:33:51 2018

@author: chenzhiwei
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:27:19 2018

@author: Administrator
"""

print(__doc__)
import os
import pandas as pd

os.chdir(u'D:\【01】行健金融\【01】数据中心\【05】数据分析项目\【03】2018\May\规则引擎_分期商城_风控+授信')
df = pd.read_csv('czw_installment_ShoppingMall_test_clean_verification_clean.csv')

import mlxtend
import time
import numpy as np
from sklearn.externals import joblib

time1 = time.time()
start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('train start time is: ', start_time)

text_var_list = []
data_list = []
for col in df.columns.values:
    if col.upper() not in text_var_list:
        data_list.append(col)
df_Preprocess = df[data_list]
col_index = range(1, len(df_Preprocess.columns)-2)
col_index.append(len(df_Preprocess.columns)-1)
X = df_Preprocess[df_Preprocess.columns[col_index]]
y = df_Preprocess['status']


scaler = joblib.load('scaler.pkl')
X_pre = scaler.transform(X)

clf = joblib.load('stackingpkl.pkl')
pre_result = clf.predict_proba(X_pre)
pre_result_transpose = pre_result[:, 0].reshape(len(pre_result), 1)
# loan_date = df['loan_no']
# loan_date = loan_date.apply(lambda x: x[2:6] + '-' + x[6:8] + '-' + x[8:10] + '-'
#                                       + x[10:12] + ':' + '00' + ':' + '00')
# loan_date = loan_date.reshape(len(loan_date), 1)
base_modelvalue = 300
pre_result_transpose_score = base_modelvalue + 500.0 * pre_result_transpose

X_firstID = df['custid'].reshape(len(X), 1)

# modelname reshape
modelname = np.array('xinyan')
info = ''
# newresult = np.hstack((X_firstID, loan_date, pre_result_transpose_score, pre_result_transpose))
# export_result = pd.DataFrame(newresult, columns=['LOAN_NO', 'LOAN_DATETIME', 'MODELSCORE', 'PROBA'])
newresult = np.hstack((X_firstID, pre_result_transpose_score, pre_result_transpose))
export_result = pd.DataFrame(newresult, columns=['LOAN_NO', 'MODELSCORE', 'PROBA'])
for name, inf in [(modelname, info)]:
    export_result['MODELNAME'] = name
    export_result['INFO'] = inf

for a, b in [('MODELSCORE', 'PROBA')]:
    for i in range((export_result.shape)[0]):
        export_result[a][i] = round(export_result[a][i].astype(int), 0)
        export_result[b][i] = round(export_result[b][i].astype(float), 4)

export_result.to_csv('pbcclf_test_predict_2018.csv', header=True, index=False)
print('process is done!')

time2 = time.time()
end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('train end time is: ', end_time)
print('total run time is: % .2f' % float((time2 - time1) / 60.0))