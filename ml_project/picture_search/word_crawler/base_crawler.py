# coding=utf8
import requests
import time


class BaseCrawler(object):

    def download_html(self, input_url):
        page = requests.get(input_url)
        return page

    def parse_html(self, page):
        raise NotImplementedError

    def crawl_page(self, url_seeds, interrupt=False):
        for url in url_seeds:
            page = self.download_html(url)
            parsed_items = self.parse_html(page)
            if parsed_items is None:
                if not interrupt:
                    continue
                else:
                    break
            for item in parsed_items:
                yield item
            time.sleep(0.5)

    def crawl_page_by_page(self, url_seeds, items_num=12):
        for url in url_seeds:
            page = self.download_html(url)
            parsed_items = self.parse_html(page)
            if parsed_items is None:
                break
            current_item_num = 0
            for item in parsed_items:
                yield item
                current_item_num += 1
            if current_item_num+1 < items_num:
                break
