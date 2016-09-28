# coding=utf8
from bs4 import BeautifulSoup
from ml_project.picture_search.word_crawler.base_crawler import BaseCrawler


class CarCrawler(BaseCrawler):
    def parse_html(self, page):
        soup = BeautifulSoup(page.content.decode('gbk'), 'html.parser')
        result = soup.select('div[class="container"]')

        for elem_result in result:
            for info in elem_result.select('table > tbody > tr '):
                info_brand_arr = info.select('td[class="border-r"] > div > a')
                for info_brand in info_brand_arr:
                    yield info_brand.get_text().strip()
                for car_specific_brand in info.select('td > div[class="column_content"] > ul > li > div > a'):
                    yield car_specific_brand['title']


if __name__ == '__main__':
    url = ['http://newcar.xcar.com.cn/price/']
    crawler = CarCrawler()
    with open('car.txt', 'w') as output_car:
        for car in crawler.crawl_page(url):
            output_car.write(car.encode('utf8'))
            output_car.write('\n')
