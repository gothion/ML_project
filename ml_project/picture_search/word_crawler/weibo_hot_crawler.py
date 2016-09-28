# coding=utf8
from bs4 import BeautifulSoup

from ml_project.picture_search.word_crawler.base_crawler import BaseCrawler
from ml_project.picture_search.word_crawler import selenium_service


class WeiboHotCrawler(BaseCrawler):

    def download_html(self, url):
        return selenium_service.get_page_source(url)

    def parse_html(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        result = soup.select('div[class="hot_ranklist"] > table > tbody > tr > td[class="td_02"] > div > p > a')
        for elem in result:
            yield elem.get_text()


if __name__ == '__main__':
    url = ['http://s.weibo.com/top/summary?cate=realtimehot',
           'http://s.weibo.com/top/summary?cate=total&key=all',
           'http://s.weibo.com/top/summary?cate=total&key=films',
           'http://s.weibo.com/top/summary?cate=total&key=person']
    for item in WeiboHotCrawler().crawl_page(url):
        print item
