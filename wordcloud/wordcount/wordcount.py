# -*- coding: utf-8 -*-
"""
词频统计/mapreduce

"""

import os
import re
import time

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
				words = re.split(r'\W', word)
				# if len(word) > 2:
				# 	raise ValueError('please check!')
				# else:
				# 	word = word[0]
				for word in words:
					if len(word.strip())<1:
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
					if len(word.strip())<1:
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


if __name__ == '__main__':
	start_time = time.time()
	target_file = '../test_20180706/NINETEEN+EIGHTY-FOUR.txt'
	a = wc_run(file_path=target_file)

	for k_v in a.items():
		print('\n', k_v)
		# time.sleep(0.2)
	end_time = time.time()
	print(end_time-start_time)

	print(1)
