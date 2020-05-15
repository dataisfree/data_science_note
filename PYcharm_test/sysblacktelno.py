# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
import matplotlib
import time
import datetime

os.chdir(u"C:/Users/chenzhiwei/Desktop/电话黑名单")
df = pd.read_csv("blacklist_telno_0_5000000_type1_productid1.csv", sep=',', dtype={'telNo':object})
print(df.head())
df["productid1"] = int(5)
df["createtime1"] = pd.Timestamp(pd.datetime(2018, 6, 1, 8, 0, 0))
    # "2018-06-01 08:00:00"
# df["createtime"].dtype(time.timezone)
print(df.head())
print(df.shape)
print(df.size)
print(df.shape[0])
print(df["createtime1"][0])
print(df["createtime1"][0] + pd.DateOffset(days=df["inter_days"][0]))
# df["expiryTime"][0] = df["createtime1"][0] + pd.DateOffset(days=df["inter_days"][0])
print(df["createtime1"][0] + pd.DateOffset(days=df["inter_days"][0]))

for i in range(df.shape[0]):
    df["expiryTime"][i] = df["createtime1"][i] + pd.DateOffset(days=df["inter_days"][i])

print(df.head())
aa_list = ["type", "sourceId", "telNo", "custName", "productid1", "expiryTime1", "comments", "createrName", "createtime1" ]
dff = df[aa_list]
df[aa_list]
print(dff.head())
print(dff.shape)
print(dff[dff.duplicated()][:10])

dff_clean = dff.drop_duplicates()
print(dff_clean.shape)
print("done")
# print(dff_clean["telNo"].)

dff_clean.to_csv("clean_blacktelno_productidnotnull_type1.csv", header=True, index=False)
