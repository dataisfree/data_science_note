# -*- coding: utf-8 -*-
"""
@create: 2019-06-18

@author: chenzhiwei

@desc: 结巴分词练习

@comment: 除了jieba工具库外，还可以利用基于paddle的中文词法分析LAC完成，github:https://github.com/baidu/lac
"""

import jieba
from jieba import posseg
word = u'上海自来水来自海上'

'''几种分词模式'''
word_list = jieba.cut(word)
# 精确匹配
print('/'.join(word_list))

word_list_all = jieba.cut(word, cut_all=True)
# 全部匹配
print('/'.join(word_list_all))

word_list_search = jieba.cut_for_search(word)
# 搜索引擎
print('/'.join(word_list_search))


'''自定义词典分词'''
word = u'上海市一座国际化大都市'
cut_list = jieba.cut(word)
print('/'.join(cut_list))

# 向字典加入词及其频率
# 词频=0
jieba.add_word(word='上海市', freq=0)
cut_list = jieba.cut(word)
print('/'.join(cut_list))
# 词频=2
jieba.add_word(word='上海市', freq=20)
cut_list = jieba.cut(word)
print('/'.join(cut_list))
# 删除已加入的字典值
jieba.del_word(word='上海市')
cut_list = jieba.cut(word)
print('/'.join(cut_list))

'''查看词频临界值'''
res = jieba.suggest_freq(segment='上海市', tune=False)
print(u'上海市的词频临界值是：{0}'.format(res))
res = jieba.suggest_freq(segment='国际化', tune=False)
print(u'“国际化”的词频临界值是：{0}'.format(res))

'''加载自定义字典
格式：值 freq 词性 \n
'''
# word = u'百度2019校园招聘简历提交'
# dict_path = './user_dict/user_dict.txt'
# jieba.load_userdict(dict_path)
# cut_list = jieba.cut(word)
# print('/'.join(cut_list))

'''词性标注'''
word = u'百度2019校园招聘简历提交'
word_split = jieba.posseg.cut(word)
for w, p in word_split:
    print('{0} {1}'.format(w.encode('utf-8'), p.encode('utf-8')))
    # 为什么.format会报ascii错，而%s不会
    # 由于w是Unicode,Unicode在.format方法生成字符串是会报类型转换错误，需要先将其利用encode方法转为utf-8格式
    # 暂时仅找到这一个原因，不排除还有其它原因
    print('%s %s' % (w, p))
