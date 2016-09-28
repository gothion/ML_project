# coding=utf8
from bs4 import BeautifulSoup
from ml_project.picture_search.word_crawler.base_crawler import BaseCrawler


class BaiduTopCrawler(BaseCrawler):
    def parse_html(self, page):
        soup = BeautifulSoup(page.content.decode('gbk'), 'html.parser')
        result = soup.select('div[class="grayborder"] > table > tr > td[class="keyword"] > a[class="list-title"]')
        for key_word_info in result:
            name = key_word_info.get_text()
            yield format(name.encode('utf8'))

if __name__ == '__main__':
    # with open('hot_person.txt', 'a') as out_put_sport:
    #     url = ['http://top.baidu.com/buzz?b=255']
    #     for item in BaiduTopCrawler().crawl_page(url):
    #         out_put_sport.write('{0}\n'.format(item))
    #
    # # actor
    # url2 = ['http://top.baidu.com/buzz?b=18&c=9&fr=topcategory_c9',
    #         'http://top.baidu.com/buzz?b=17&c=9&fr=topbuzz_b18_c9',
    #         'http://top.baidu.com/buzz?b=16&c=9&fr=topbuzz_b17_c9',
    #         'http://top.baidu.com/buzz?b=15&c=9&fr=topbuzz_b16_c9']
    # with open('actor.txt', 'a') as out_put_author:
    #     for item in BaiduTopCrawler().crawl_page(url2):
    #         out_put_author.write('{0}\n'.format(item))

    # url3 = ['http://top.baidu.com/buzz?b=258&c=9&fr=topcategory_c9',
    #         'http://top.baidu.com/buzz?b=618&c=9&fr=topbuzz_b258_c9',
    #         'http://top.baidu.com/buzz?b=18&c=9&fr=topbuzz_b618_c9',
    #         'http://top.baidu.com/buzz?b=17&c=9&fr=topbuzz_b18_c9',
    #         'http://top.baidu.com/buzz?b=1395&c=9&fr=topbuzz_b17_c9',
    #         'http://top.baidu.com/buzz?b=16&c=9&fr=topbuzz_b1395_c9',
    #         'http://top.baidu.com/buzz?b=15&c=9&fr=topbuzz_b16_c9',
    #         'http://top.baidu.com/buzz?b=1396&c=9&fr=topbuzz_b15_c9',
    #         'http://top.baidu.com/buzz?b=260&c=9&fr=topbuzz_b1396_c9',
    #         'http://top.baidu.com/buzz?b=454&c=9&fr=topbuzz_b260_c9',
    #         'http://top.baidu.com/buzz?b=255&c=9&fr=topbuzz_b454_c9',
    #         'http://top.baidu.com/buzz?b=3&c=9&fr=topbuzz_b255_c9',
    #         'http://top.baidu.com/buzz?b=22&c=9&fr=topbuzz_b3_c9',
    #         'http://top.baidu.com/buzz?b=493&c=9&fr=topbuzz_b22_c9',
    #         'http://top.baidu.com/buzz?b=491&c=9&fr=topbuzz_b493_c9',
    #         'http://top.baidu.com/buzz?b=261&c=9&fr=topbuzz_b491_c9',
    #         'http://top.baidu.com/buzz?b=257&c=9&fr=topbuzz_b261_c9',
    #         'http://top.baidu.com/buzz?b=259&c=9&fr=topbuzz_b257_c9',
    #         'http://top.baidu.com/buzz?b=612&c=9&fr=topbuzz_b259_c9']
    # with open('actor.txt', 'a') as out_put_author:
    #     for item in BaiduTopCrawler().crawl_page(url3):
    #         out_put_author.write('{0}\n'.format(item))

    with open('hot_person.txt', 'w') as out_put_sport:
        url = [
               'http://top.baidu.com/buzz?b=18&c=9&fr=topcategory_c9',
               'http://top.baidu.com/buzz?b=17&c=9&fr=topbuzz_b18_c9',
               'http://top.baidu.com/buzz?b=16&c=9&fr=topbuzz_b17_c9',
               'http://top.baidu.com/buzz?b=15&c=9&fr=topbuzz_b16_c9'
               ]
        person_map = {}
        for item in BaiduTopCrawler().crawl_page(url):
            if item not in person_map:
                person_map[item] = 0
            person_map[item] += 1
            print item
        out_put_sport.write(','.join(person_map.keys()))
