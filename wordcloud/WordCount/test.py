# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import wordcount as wc

file = '../test_20180706/NINETEEN+EIGHTY-FOUR.txt'

wc_dict = wc.wc_run(file_path=file)

k = list(wc_dict.keys())
v = list(wc_dict.values())

a = np.array((k, v))

# 在py36中下面的语句会有问题，在DataFrame中不能直接用dict.items()，可以用df1的生成方式来实现
# df = pd.DataFrame(wc_dict.items(), columns=['key', 'value'])

df1 = pd.DataFrame(
	np.concatenate(
		(np.array(k).reshape(-1, 1), np.array(v).reshape(-1, 1)),
		axis=1),
	columns=['key', 'value']
)

print(1)
