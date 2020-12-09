# -*- coding: utf-8 -*-
"""
词频统计/mapreduce

python version: 3.6.*
special attribute：create a generator to count words
"""

import os
import re
import time

import numpy as np


# load_file
def load_file_v1(file_path):
	with open(file_path, 'r+', encoding='utf-8') as inf:
		data = inf.readlines()

	return data


def load_file_v2(file_path):
	f = open(file_path, 'r+', encoding='utf-8')
	return f


# word_map
def word_map(file_path):
	# data = load_file_v1(file_path)
	# # data = load_file_v2(file_path)
	# print(type(data))
	# data_size = len(data)
	if os.path.isfile(file_path) is False:
		raise Exception("args('file_path') is not a file! please check!")

	def word_generator_v1():
		data = load_file_v1(file_path)
		for line in data:
			sub_line_lts = line.split()
			for word in sub_line_lts:
				# 去除首尾空格
				word = word.strip()
				# 转为小写
				word = word.lower()
				# 返回word中字符的部分[a-zA-Z0-9], re.split返回一个list数据结构
				words = re.split(r'\W', word)
				# if len(word) > 2:
				# 	raise ValueError('please check!')
				# else:
				# 	word = word[0]
				for word in words:
					if len(word.strip()) < 1:
						continue
					yield word, 1

	def word_generator_v2():
		data = load_file_v1(file_path)
		cur_word_map = []
		for line in data:
			sub_line_lts = line.split()
			for word in sub_line_lts:
				# 去除首尾空格
				word = word.strip()
				# 转为小写
				word = word.lower()
				words = re.split(r'\W', word)
				# if len(word)>2:
				# 	raise ValueError('please check!')
				# else:
				# 	word = word[0]
				for word in words:
					if len(word.strip()) < 1:
						continue
					cur_word_map.append((word, 1))

		wm_size = len(cur_word_map)
		for idx in range(wm_size):
			yield cur_word_map[idx]

	return word_generator_v1()


# word_reduce
def word_reduce(word_tuple, wc_dict):
	word, word_count = word_tuple[0], word_tuple[1]
	if wc_dict.get(word) is None:
		wc_dict[word] = word_count
	else:
		wc_dict[word] = wc_dict[word] + word_count

	return wc_dict


def wc_run(file_path):
	result_dict = {}
	wc_map = word_map(file_path)
	for wc in wc_map:
		result_dict = word_reduce(wc, result_dict)

	return result_dict


def create_ndArray(data: dict) -> np.ndarray:
	"""
	从dict中利用list(dict.keys()) 和 list(dict.values()) 分别生成的结果list的索引是一一对应的
	基于此可以生成一个np.ndarray数据结构，用于后续计算，诸如信息熵的计算

	--验证前述索引是否一致的测试代码
	for idx, key in enumerate(list(a.keys())[:10]):
		print(key)
		print(a.get(key))
		print(list(a.values())[idx])
		print('-'*10)
	"""
	values = np.array(list(data.values()))
	keys = np.array(list(data.keys()))
	key_and_value_arr = np.stack((values, keys), axis=0)

	return key_and_value_arr


def percent(x: np.ndarray) -> np.ndarray:
	if isinstance(x.dtype, np.float) is False:
		x = x.astype(np.float)

	return x/np.sum(x)


def main():
	pass


if __name__ == '__main__':
	start_time = time.time()
	target_file = '../test_20180706/NINETEEN+EIGHTY-FOUR.txt'
	a = wc_run(file_path=target_file)

	for k_v in a.items():
		print('\n', k_v)
	arr = create_ndArray(a)

	# 计算每个key的频数的占比
	print(percent(arr[0]))

	# time.sleep(0.2)
	end_time = time.time()
	print(end_time - start_time)

	print(1)
