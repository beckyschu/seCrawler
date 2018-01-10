__author__ = 'tixie'
from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import  Selector
import re
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['amazon.com','alibaba.com','baidu.com']
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None
    counter = 0


    def __init__(self, keyword, se = 'amazon', pages = 2,  *args, **kwargs):
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        super(keywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):
        self.driver.get(response.url)
        body = self.driver.page_source
        #next = self.driver.find_element_by_xpath('//div @class="view-label"')


        # print('RESPONSE %s', body)
        totalResults = re.search('View (.*) Product', body).group(1)
        print('RESPONSE TOTAL RESULTS %s' % totalResults)
        with open('alibaba.html', 'w') as f:
            f.write(body)
        f.close()
        self.driver.close()

        for url in Selector(response).xpath(self.selector).extract():
            print(url)

        platform = response.url.split("/")[2].split(".")[1]
        self.log('Response Url %s %s' % (platform, response.url))

        filename = '%s-%s.html' % ('amazon', platform)

        with open(filename, 'wb') as f:
            f.write(response.body)
        f.close()
        self.log('Saved file %s' % filename)

        # get number of results
        if platform == 'alibaba':
            totalResults = re.search('View (.*) Product', response.body.decode('utf-8')).group(1)
        else :
            totalResults = re.search('<h2 class="resultCount" id="resultCount"><span>(.*)of (.*) results for</span>', response.body.decode('utf-8')).group(2)
        #totalResults = response.xpath('//h2/@class="resultCount"').extract()
        print('Total Results [%s]' % totalResults)
