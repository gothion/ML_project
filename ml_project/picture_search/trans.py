#!/usr/bin/env python
# coding=utf8

"""
引用自yc@2012/4/4, github地址: https://github.com/ichuan/yc-lib
db from http://xh.5156edu.com/zmj.php.js
usage : python trans.py 我 的 世 界
output: wǒ de shì jiè
"""

import re
from pypinyin import lazy_pinyin
diction_pinyin = None


def _get_trans_diction(out_put_file):
    global diction_pinyin
    if diction_pinyin is None:
        load_diction_pinyin()
        with open(out_put_file, 'w') as out_put_dict:
            for k, v in diction_pinyin.iteritems():
                out_put_dict.write('{0},{1}\n'.format(k.encode('utf8'), v.encode('utf8')))


def trans_impl(chinese_word):
    global diction_pinyin
    if diction_pinyin is None:
        load_diction_pinyin()
    return diction_pinyin[chinese_word].split(',') if chinese_word in diction_pinyin else [chinese_word]


def load_diction_pinyin():
    global diction_pinyin
    diction_pinyin = {}
    with open('./unicode_to_hanyu_pinyin.txt') as input_diction:
        for line in input_diction:
            line_trim = line.strip()
            line_arr = line_trim.split(' ')
            chinese_word = unicode(unichr(int(line_arr[0], 16)))
            pinyin_list = set(re.sub(r'[\(\)\d]+', '', line_arr[1]).split(','))
            diction_pinyin[chinese_word] = ','.join(pinyin_list)


def trans(the_str):
    return (''.join(lazy_pinyin(the_str.decode('utf8')))).encode('utf8')

# def trans(the_str):
#     result = []
#     for word in the_str.decode('utf8'):
#         result.append(trans_impl(word))
#     print result
#     return get_combine_info(result)


def get_combine_info(array_list):
    result = array_list
    level = 0
    index_result = [0] * len(result)
    str_stack = []
    while level >= 0:
        if index_result[level] >= len(result[level]):
            index_result[level] = 0
            level -= 1
            index_result[level] += 1
            if len(str_stack):
                str_stack.pop()
            continue
        for row_num in range(level, len(result)):
            str_stack.append(result[row_num][index_result[row_num]])
        level = row_num
        while index_result[level] < len(result[level]):
            if len(str_stack):
                str_stack.pop()
            str_stack.append(result[level][index_result[level]])
            print ''.join(str_stack)
            yield ''.join(str_stack)
            index_result[level] += 1
        if len(str_stack):
            str_stack.pop()


if __name__ == '__main__':
    # _get_trans_diction('chinese2pinyin')
    # print trans_impl('哈'.decode('utf8'))
    print trans('哈,哈')
