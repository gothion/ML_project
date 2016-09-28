# coding=utf8
import requests
from lxml import html
import time
import operator
from ml_project.picture_search.word_crawler.base_crawler import BaseCrawler


class YoukuCrawler(BaseCrawler):
    def parse_html(self, page):
        tree = html.fromstring(page.content)
        movie_info_arr = tree.xpath('//div[@class="s-body"]/div[@class="yk-content"]'
                                    '/div[@class="vaule_main"]/div[@class="box-series"]/ul[@class="panel"]/'
                                    '/li[@class="yk-col4 mr1"]')
        if len(movie_info_arr) == 0:
            yield None
        movie_info = movie_info_arr[0]
        title_arr = movie_info.xpath('//li[@class="title"]/a/text()')

        for title in title_arr:
            title_name = title.encode('utf8').split(' ')[0]
            yield title_name


class YoukuActorCrawler(BaseCrawler):
    def parse_html(self, page):
        tree = html.fromstring(page.content)
        movie_info_arr = tree.xpath('//div[@class="s-body"]/div[@class="yk-content"]'
                                    '/div[@class="vaule_main"]/div[@class="box-series"]/ul[@class="panel"]/'
                                    '/li[@class="yk-col4 mr1"]')
        if len(movie_info_arr) == 0:
            yield None
        movie_info = movie_info_arr[0]
        title_arr = movie_info.xpath('//li[@class="actor"]/a/text()')

        for title in title_arr:
            title_name = title.encode('utf8').split(' ')[0]
            yield title_name


def parse_html(page):
    tree = html.fromstring(page.content)

    movie_info_arr = tree.xpath('//div[@class="s-body"]/div[@class="yk-content"]'
                                '/div[@class="vaule_main"]/div[@class="box-series"]/ul[@class="panel"]/'
                                '/li[@class="yk-col4 mr1"]')
    if len(movie_info_arr) == 0:
        return None, None
    movie_info = movie_info_arr[0]
    title_arr = movie_info.xpath('//li[@class="title"]/a/text()')
    actor_arr = movie_info.xpath('//li[@class="actor"]/a/text()')
    movie_map = {}
    actor_map = {}
    for title in title_arr:
        title_name = title.encode('utf8').split(' ')[0]
        if title_name not in movie_map:
            movie_map[title_name] = 1
        else:
            movie_map[title_name] += 1

    for actor in actor_arr:
        actor_name = actor.encode('utf8')
        if actor_name not in actor_map:
            actor_map[actor_name] = 1
        else:
            actor_map[actor_name] += 1
    return movie_map, actor_map


def get_movies():
    url_seeds = [
        'http://list.youku.com/category/show/c_85_s_5_d_1_p_',
        'http://list.youku.com/category/show/c_85_s_4_d_1_p_',
        'http://list.youku.com/category/show/c_97_u_2_s_4_d_1_p_',
        'http://list.youku.com/category/show/c_97_u_2_s_5_d_1.html'
        'http://list.youku.com/category/show/c_96_s_4_d_1_p_',
        'http://list.youku.com/category/show/c_96_s_5_d_4_p_',
        'http://list.youku.com/category/show/c_96_s_5_d_1_p_',
    ]
    return get_info_from_youku(url_seeds)


def get_cartoons():
    url_seeds = [
        'http://list.youku.com/category/show/c_100_s_5_d_2_p_',
        'http://list.youku.com/category/show/c_100_s_4_d_2_p_',
    ]
    return get_info_from_youku(url_seeds)


def get_info_from_youku(url_seeds):
    movies_map = {}
    actor_map = {}
    for url in url_seeds:
        one_page_movies, one_page_map = get_youku_movie_impl(url)
        merge_data_to_map(movies_map, one_page_movies)
        merge_data_to_map(actor_map, one_page_map)
    return movies_map, actor_map


def get_youku_movie_impl(url_fore_part):
    movies_map = {}
    actor_map = {}
    if url_fore_part.endswith('.html'):
        print 'crawling url is : {0}'.format(url_fore_part)
        page = _download_html(url_fore_part)
        one_page_movies, one_page_map = parse_html(page)
        merge_data_to_map(movies_map, one_page_movies)
        merge_data_to_map(actor_map, one_page_map)
        return movies_map, actor_map
    for i in range(1, 31):
        url = '{0}{1}.html'.format(url_fore_part, i)
        print 'crawling url is : {0}'.format(url)
        page = _download_html(url)
        one_page_movies, one_page_map = parse_html(page)
        if one_page_movies is None:
            break
        merge_data_to_map(movies_map, one_page_movies)
        merge_data_to_map(actor_map, one_page_map)
        time.sleep(0.5)
    return movies_map, actor_map


def merge_data_to_map(dst_map, source_map):
    for k, v in source_map.iteritems():
        if k not in dst_map:
            dst_map[k] = v
        else:
            dst_map[k] += v


def sort_and_format_map(input_map):
    sorted_map = sorted(input_map.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_map


def _download_html(input_url):
    page = requests.get(input_url)
    return page

if __name__ == '__main__':
    new_movies_arr, author_map = get_movies()
    with open('movie.txt', 'w') as output_movie:
        for key in new_movies_arr.keys():
            output_movie.write(key)
            output_movie.write('\n')
        # output_movie.write(','.join(new_movies_arr.keys()))
    with open('actor.txt', 'a') as output_author:
        for k, v in sort_and_format_map(author_map):
            output_author.write(k)
            output_author.write('\n')
    new_cartoons, _ = get_cartoons()
    with open('cartoon.txt', 'w') as output_cartoon:
        for k in new_cartoons.keys():
            output_cartoon.write(k)
            output_cartoon.write('\n')
