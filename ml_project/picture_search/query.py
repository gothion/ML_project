# coding=utf8
import copy

import requests

http_url = 'http://10.10.106.219:10201/solr/photo/select'
row_num = 20
keep_field = 'id, url'
payload = {'wt': 'json', 'indent': 'true', 'rows': str(row_num)}

query_point = ['desc', 'comment', 'tag_name']


def get_result(words):
    local_payload = copy.deepcopy(payload)
    local_payload['q'] = get_query_key(words)
    start = 0
    while True:
        return_num, result = get_result_impl(local_payload, start)
        for result_elem in result:
            print result_elem
        if return_num < row_num:
            break
        start += row_num
    print start


def get_result_impl(input_local_payload, start):
    input_local_payload['start'] = start
    payload_str = '&'.join('{0}={1}'.format(k, v) for k, v in input_local_payload.items())
    r = requests.get(http_url, params=payload_str)
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

if __name__ == '__main__':
    get_result(['宝马', '兰博基尼', '奔驰'])