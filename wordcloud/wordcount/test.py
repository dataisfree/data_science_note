# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import wordcount as wc

file = '../test_20180706/NINETEEN+EIGHTY-FOUR.txt'

wc_dict = wc.wc_run(file_path=file)

k = list(wc_dict.keys())
v = list(wc_dict.values())

a = np.array((k, v))

df = pd.DataFrame(wc_dict.items(), columns=['key', 'value'])
df1 = pd.DataFrame(
	np.concatenate(
		(np.array(k).reshape(-1,1), np.array(v).reshape(-1, 1)),
		axis=1),
	columns=['key', 'value']
)

print(1)