# coding=utf8

from selenium import webdriver


def main(url):
    caps = {
        'takeScreenshot': False,
        'javascriptEnabled': True,
    }
    phantom_link = 'http://127.0.0.1:8080/wd/hub'

    driver = webdriver.Remote(
        command_executor=phantom_link,
        desired_capabilities=caps
    )

    driver.get(url)

    print driver.title
    print driver.find_element_by_xpath('//ul[@id="clock_0"]').text


def get_page_source(url):
    caps = {
        'takeScreenshot': False,
        'javascriptEnabled': True,
    }
    phantom_link = 'http://127.0.0.1:8080/wd/hub'

    driver = webdriver.Remote(
        command_executor=phantom_link,
        desired_capabilities=caps
    )
    driver.get(url)
    return driver.page_source

if __name__ == "__main__":
    url = 'http://s.weibo.com/top/summary?cate=realtimehot'
    main(url)
