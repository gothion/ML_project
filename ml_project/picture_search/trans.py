#!/usr/bin/env python
# coding=utf8

"""
引用自yc@2012/4/4, github地址: https://github.com/ichuan/yc-lib
db from http://xh.5156edu.com/zmj.php.js
usage : python trans.py 我 的 世 界
output: wǒ de shì jiè
"""

import cPickle
diction_pinyin = None


def _get_trans_diction(out_put_file):
    global diction_pinyin
    if diction_pinyin is None:
        with open('./py.db') as language_dict:
            with open(out_put_file, 'w') as out_put_dict:
                diction_pinyin = cPickle.load(language_dict)
                for k, v in diction_pinyin.iteritems():
                    out_put_dict.write('{0},{1}\n'.format(k.encode('utf8'), v.encode('utf8')))


def trans_impl(chinese_word):
    global diction_pinyin
    if diction_pinyin is None:
        diction_pinyin = cPickle.load(open('./py.db'))
    return diction_pinyin[chinese_word] if chinese_word in diction_pinyin else chinese_word


def trans(the_str):
    for word in the_str.decode('utf8'):
        print trans_impl(word)

if __name__ == '__main__':
    # _get_trans_diction('chinese2pinyin')
    # print trans_impl('哈'.decode('utf8'))
    trans('哈哈,好可爱')
