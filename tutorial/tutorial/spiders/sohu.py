# -*- coding: utf-8 -*-
import scrapy
import re,os,sys
from tutorial.items import TutorialItem
from scrapy import Request



class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['www.sohu.com']  
    start_urls = ['http://www.sohu.com/']  
    def __init__(self):
        super(SohuSpider)
        self.contain = set() 

    def parse(self, response):
        all_urls = re.findall('href="(.*?)"',response.xpath("/html").extract_first())
        for url in all_urls:
            item = TutorialItem()
            if re.findall("(\.jpg)|(\.jpeg)|(\.gif)|(\.ico)|(\.png)|(\.js)|(\.css)$",url.strip()):
                continue 
            elif url.strip().startswith("http") or url.strip().startswith("//"):
                temp_url = url.strip() if url.strip().startswith('http') else 'http:' + url.strip() 
                item = self.get_all(item,response)
                if 'TEXT' in item and item['TEXT'] != '' and item['TITLE'] != '':
                    for _,targetName in dict(item).items():
                        if "人" in targetName and item['URL'] not in self.contain:
                            yield item  
                            self.contain.add(item['URL'])
                            break 
                print('发送<' + temp_url + '>到下载器') 
                yield Request(temp_url,callback=self.parse) 

    
    def get_all(self,item,response):
        item['URL'] = response.url.strip()
        item['TITLE'] = response.xpath('/html/head/title/text()').extract()[0].strip()
        contain_h1 = response.xpath('//h1/text()').extract()
        contain= contain_h1[0] if len(contain_h1) !=0 else "" 
        item["H1"] = contain.strip()
        main_text = []

        for tag in ['p','br']:
            sub_text = self.get_content(response,tag)
            main_text.extend(sub_text)

        main_text = list(set(main_text))
        if len(main_text) != 0:
            item['TEXT'] = '\n'.join(main_text)
        return item
    
    def get_content(self,response,tag):
        main_text = []
        contexts = response.xpath('//'+tag+'/text()').extract()
        for text in contexts:
            if len(text.strip()) > 100:
                main_text.append(text.strip())
        return main_text

		
		
		
		