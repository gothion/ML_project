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

    get_query_items()
    # get_result(['星空','夜空', '银河系', '黑洞','木星', '水星', '银河'], 'astronmy.csv')
    # get_result(['星空', '夜空', '银河系', '木星', '水星', '银河'], 'astronmy.csv')
    # test_str = '家具,玄关,新中式,背景墙,入户,飘窗, 客厅,中式古典风格,简装修,精装,简欧风格,欧式风格,' \
    #            '田园风格,过道,隔断墙,中式田园风格,阳台,伊姆斯椅,懒人沙发,椅,家私,卧室, 主卧, 次卧, 双人床,儿童床,单人床,' \
    #            '茶几,推拉门,多功能沙发,床垫,茶几,摇椅,沙发床,布艺沙发,斯帝罗兰,吊椅,榻榻米,衣柜,衣帽间,五斗柜,床头柜,壁柜,' \
    #            '窗台,储物柜,碗柜,卫浴柜,玻璃门,木床,转角沙发,皮沙发,雕花床,软床,形沙发,立体墙,照片墙,地板,妆台'
    # test_str = '卡通,动漫,罗小黑,灰太狼,露比,奥特曼,史迪奇,乔巴,米菲,蜡笔小新,米老鼠,炮炮兵,兔八哥,mocmoc,大头,超人,萌娘,猫耳娘,' \
    #            '全是猫,甜甜私房猫,叮当猫,哆啦a梦,魔卡少女樱,火影忍者,守护甜心,航海王,夏目友人帐,阿拉蕾,阿童木,名侦探柯南,犬夜叉,' \
    #            '银魂,千与千寻,' \
    #            '死神,龙珠,海贼王,魂狩,暴君熊,百兽凯多,二次元,犬夜叉,小猪佩奇,熊出没,莽荒纪,海绵宝宝,邋遢大王,狮子王,白雪公主,匹诺曹,灰姑娘,' \
    #            '闪电狗,怪化猫,虫师,妖精的尾巴,食戟之灵,星学院,喜羊羊与灰太狼,猪猪侠,光头强,刀剑神域,奇妙仙子,魔卡少女樱,死神,城市猎人,' \
    #            '棋魂,神奇宝贝,口袋妖怪,皮卡丘,鲁路修,死亡笔记,犬夜叉,樱桃小丸子'
    # test_str = '电影,movie,大片,电视剧,喜剧,武侠,美剧,韩剧,港片,爱情片,动作片,科幻,恐怖,动画,惊悚,犯罪,肖申克的救赎,控方证人,可爱的动物,弗兰肯斯坦的灵与肉,银魂剧场版 银幕前,' \
    #            '这个杀手不太冷,阿甘正传,霸王别姬,美丽人生,辛德勒的名单,泰坦尼克号,银魂完结篇,地球公民,我和世界不一样,德国，一个夏天的,' \
    #            '猫咪物语,不老骑士,舌尖上的新年,我们诞生在中国,百鸟朝凤,路边野餐,小情人,箭士柳白猿,不朽的时光,我不是王毛,魔兽,惊天大逆转,' \
    #            '寻找心中的你,精灵王座,火锅英雄,哪一天我们会飞,美人鱼,寒战,小门神,使徒行者'
    # get_result(test_str.split(','), '卡通')
