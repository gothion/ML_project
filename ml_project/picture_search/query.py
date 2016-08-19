# coding=utf8
import copy

import requests

http_url = 'http://10.10.106.219:10201/solr/photo/select'
row_num = 20
keep_field = 'id, url'
payload = {'wt': 'json', 'indent': 'true', 'rows': str(row_num)}

# query_point = ['desc', 'comment', 'tag_name']
query_point = ['desc',  'tag_name']

def get_result(words, out_file_name):
    local_payload = copy.deepcopy(payload)
    local_payload['q'] = get_query_key(words)
    start = 0
    with open(out_file_name, 'w') as out_put_data:
        while True:
            return_num, result = get_result_impl(local_payload, start)
            for result_elem in result:
                out_put_data.write(result_elem + '\n')
            if return_num < row_num:
                break
            start += row_num
    print start


def get_result_impl(input_local_payload, start):
    input_local_payload['start'] = start
    payload_str = '&'.join('{0}={1}'.format(k, v) for k, v in input_local_payload.items())
    r = requests.get(http_url, params=payload_str)
    print r.url
    result = r.json()['response']['docs']
    return len(result), [convert_result_to_str(result_elem) for result_elem in result]


def convert_result_to_str(result_elem):
    field_arr = ['tag_name', 'desc', 'comment', 'url']
    field_info = ','.join(map(str, (result_elem.get(field, '').encode('utf8') for field in field_arr)))
    return str(result_elem.get('photo_id')) + ',' + field_info


def get_query_key(words):
    connection_word = '+OR+'
    words_format = connection_word.join(words)
    query_connection_sep = ':({0}){1}'.format(words_format, connection_word)
    return query_connection_sep.join(query_point) + ":({0})".format(words_format)


def get_query_items():
    with open('query_info.txt') as input_data:
        for line in input_data:
            line_arr = line.split(',')
            file_name = line_arr[0]
            get_result(words=line_arr, out_file_name=file_name)

if __name__ == '__main__':
    # get_result(['电影', 'movie', '大片', '电视剧', '喜剧', '武侠', '美剧', '韩剧', 'moive'], 'moive.txt')

    # get_query_items()
    # get_result(['星空','夜空', '银河系', '黑洞','木星', '水星', '银河'], 'astronmy.csv')
    # get_result(['星空', '夜空', '银河系', '木星', '水星', '银河'], 'astronmy.csv')
    test_str = '家具,玄关,新中式,背景墙,入户,飘窗, 客厅,中式古典风格,简装修,精装,简欧风格,欧式风格,' \
               '田园风格,过道,隔断墙,中式田园风格,阳台,伊姆斯椅,懒人沙发,椅,家私,卧室, 主卧, 次卧, 双人床,儿童床,单人床,' \
               '茶几,推拉门,多功能沙发,床垫,茶几,摇椅,沙发床,布艺沙发,斯帝罗兰,吊椅,榻榻米,衣柜,衣帽间,五斗柜,床头柜,壁柜,' \
               '窗台,储物柜,碗柜,卫浴柜,玻璃门,木床,转角沙发,皮沙发,雕花床,软床,形沙发,立体墙,照片墙,地板,妆台'
    get_result(test_str.split(','), '家具')
