# -*- coding: utf-8 -*-
import datetime,socket

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from scrapy.http import Request,FormRequest
from ..items import BaiduImgsItem
import time,urllib
from scrapy_redis.spiders import RedisSpider


class DownloadBaiduSpider(RedisSpider):
    name = 'baidu_redis'
    allowed_domains = ['image.baidu.com']
    redis_key = 'shujunspider:start_urls'
    #start_urls = [urllib.unquote('https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1506762749553_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87&f=3&oq=%E5%9B%BE%E7%89%87&rsp=0')]

    default_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip,deflate, sdch, br',
            'Acccept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'image.baidu.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/52.0.2743.116 Safari/537.36',
            }

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pull-rs"]'),callback='parse_item',follow=True),
        #Rule(LinkExtractor(restrict_xpaths='//img[@class="main_img img-hover"]/@data-imgurl'),callback='parse_item',follow=True),
    )

    def parse(self, response):
        print('=============================')
        print response.url
        print('this is parse method')
        with open('/var/scrapy_img_download/htmlbody.html','w+') as hpage:
            hpage.write(str(response.body))
        print('=============================')

        list_imgs = response.xpath('//img[@class="main_img img-hover"]/@data-imgurl').extract()
        for img in list_imgs:
            item = BaiduImgsItem()
            item['image_url'] = img
            yield item

        new_href = response.xpath(u'//a[@class="pull-rs" and contains(@title,"美女")]/@href').extract()
        #new_href = response.xpath('//a[@class="pull-rs"]/@href').extract()
        for i in new_href[:5]:
            print urllib.unquote(i)
            print '===================='
            print i
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        time.sleep(18)
        for url in new_href:
            yield Request(url='https://image.baidu.com' + url, headers=self.default_headers)

        '''l=ItemLoader(item=BaiduImgsItem(),response=response)
        l.add_xpath('image_url','//img[@class="main_img img-hover"]/@data-imgurl')
        print(l.load_item())
        time.sleep(5)
        return l.load_item()'''


    def parse_item(self, response):
        print('=============================')
        print('this is parse_item method')
        print('=============================')
        time.sleep(6)
        '''
        l=ItemLoader(item=BaiduImgsItem(),response=response)
        l.add_xpath('image_url','//img[@class="main_img img-hover"]/@data-imgurl')
        return l.load_item()
        '''
        list_imgs = response.xpath('//img[@class="main_img img-hover"]/@data-imgurl').extract()
        if list_imgs:
            item = BaiduImgsItem()
            item['image_url'] = list_imgs
            yield item