# -*- coding: utf-8 -*-
import codecs
import glob
import re

import scrapy
from nltk.tokenize import sent_tokenize
from scrapy import Request
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

import links


class VnSpider(scrapy.Spider):
    name = 'vn'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']
    
    def parse(self, response):
        hxs=HtmlXPathSelector(response)
        urls={}
        urls['category']=hxs.select('//nav[@id="main_menu"]/a/@href').extract()
        for url in urls['category']:
            check_url = re.search(pattern=r'(/[\w]+-[\w]+$|/cuoi$)', string=url)
            if check_url:
                res = re.findall(pattern=r'(/[\w]+-[\w]+$|/cuoi)', string=url)               
                file_name="/home/leanh/vnexpress/crawl_url/"+res[0].replace("/","")+".txt"
                links.categories('https://vnexpress.net/'+res[0].replace("/",""),file_name)
                # file_name_out="/home/leanh/vnexpress/crawled_data/"+res[0].replace("/","")+".out"
                # for link in url_links:
                #     f.write(link+"\n")

        list_of_files = glob.glob('/home/leanh/vnexpress/crawl_url/*')
        for file_name in list_of_files:
            FI=open(file_name,"r")
            FO=file_name.replace("crawl_url","crawled_data")
            for line in FI:
                yield  Request(url=line,meta={'ouput_file': FO},callback=self.parse_main)
               
    
    def parse_main(self, response):
        temp=response.meta.get('ouput_file')
        input=codecs.open(temp, "a", "utf-8")
        hxs= HtmlXPathSelector(response)
        data_need_to_crawl={}
        try:
            data_need_to_crawl['title'] = hxs.select('//h1[@class="title_news_detail mb10"]/text() | //h1[@class="title_news_detail"]/text() | //h1[@class="title_gn_detail"]/text() | //div[@class="title_news"]/hl/text() | //h1[@class="title"]/text() | //article[@class=" fck_detail"]/hl/text()').extract()[0]
            # data_need_to_crawl['discription']= hxs.select('//p[@class="description"]/text() | //h2[@class="short_intro"]/text()').extract()[0]           
            data_need_to_crawl['body']= hxs.select('//p[@class="Normal"]/text() | //section[@class="sidebar_1"]/p/text() |//p[@class="description"]/text() | //h2[@class="short_intro"]/text() | p[@class="BoxLink"]/text() | //h3[@class="short_intro txt_666"]/text() | //h2[@class="lead_detail"]/text() | //div[@class="lead_detail"]/text() | //article[@class=" fck_detail"]/c/text() | //h2[@class="lead"]/text() | //div[@class="section-inner inset-column"]/p/text() | //div[@class="ctn_chapter width_medium"]/p/text() | //h2[@class="width_medium subtitle_lf"]/text()').extract()
            input.write(data_need_to_crawl['title']+'. ')
            for x in data_need_to_crawl['body']:
                input.write(x)
        except Exception:
            pass
 
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(VnSpider)
process.start()

# pre-processing
list_of_files = glob.glob('/home/leanh/vnexpress/crawled_data/*.txt')
for file_name in list_of_files:
    FI=codecs.open(file_name,"r","utf-8")
    FO=codecs.open(file_name.replace("txt","out"),"w","utf-8")
    for line in FI:
        for sent in sent_tokenize(line):
            if "/" in sent or sent==".": continue
            FO.write(sent+'\n')
