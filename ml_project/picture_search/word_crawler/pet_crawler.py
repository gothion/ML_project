# coding=utf8
import json
import time
from ml_project.picture_search.word_crawler.base_crawler import BaseCrawler


class PetCrawler(BaseCrawler):
    def __init__(self):
        self.max_page_num = 500

    def parse_html(self, page):
        result = json.loads(page.content)
        pet_info_arr = result['data'][0]['disp_data']
        for cat_info in pet_info_arr:
            yield cat_info['name']

    def crawl_pets(self, pets=['猫', '狗']):
        for pet in pets:
            url_arr = []
            for i in range(self.max_page_num):
                url_arr.append('https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?format=json&ie=utf-8&oe=utf-8'\
                               '&query={0}&resource_id=6829&rn=12&from_mid=1&pn={1}'.format(pet, 12*i))
            for item in self.crawl_page_by_page(url_arr):
                yield item
            time.sleep(0.5)


if __name__ == '__main__':
    with open('pet.txt', 'w') as output_pet:
        for pet in PetCrawler().crawl_pets():
            output_pet.write(pet.encode('utf8'))
            output_pet.write('\n')
