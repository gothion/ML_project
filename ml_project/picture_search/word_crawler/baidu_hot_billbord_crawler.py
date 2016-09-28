# coding=utf8
import json

import requests

curl_command = "curl 'http://top.baidu.com/population/toplist' -H 'Cookie: BAIDUID=BDA819BF350523B5ECC8ABE13370687D:FG=1; BIDUPSID=BDA819BF350523B5ECC8ABE13370687D; PSTM=1459138090; bdshare_firstime=1472206060927; BDRCVFR[z91LIEeorFR]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=1433_18241_17948_21105_18133_21160_20930; Hm_lvt_79a0e9c520104773e13ccd072bc956aa=1474200729,1474203534,1474207415,1474208037; Hm_lpvt_79a0e9c520104773e13ccd072bc956aa=1474208054' -H 'Origin: http://top.baidu.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://top.baidu.com/population?fr=topbuzz_b1' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'boardid=2&divids[]=0&divids[]=950&divids[]=951' --compressed"


def get_page():
    url = 'http://top.baidu.com/population/toplist'
    headers = {
        'Origin': 'http://top.baidu.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://top.baidu.com/population?fr=topbuzz_b1',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = 'boardid=341&divids[]=0&divids[]=950&divids[]=951'
    return requests.post(url=url, headers=headers, data=data)


def parse_html(page):
    result = json.loads(page.content)
    items_info_list = result['topWords'].values()
    top_num = 3
    for items_info in items_info_list:
        i = 0
        for item in items_info:
            if i >= top_num:
                break
            i += 1
            if item['trend'] == 'rise':
                yield item['searches'], item['keyword'], item['trend'], item['percentage']


def execute_crawl():
    page = get_page()
    for searches, keyword, trend, percentage in parse_html(page):
        yield keyword

