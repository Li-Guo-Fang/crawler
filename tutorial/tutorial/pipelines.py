# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TutorialPipeline(object):
    
    def __init__(self):
        self.filename = open("content.txt",'w',encoding="utf-8")
        self.contain = set()  #定义集合用于去重
        self.start_count = 0  #初始化计数器
        self.max_count = 5    #设置最大存储数量
    
    def process_item(self, item, spider):
        text = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.write_to_txt(eval(text))        
        self.start_count += 1
        if self.start_count > self.max_count:
            self.close_spider(spider)
        #return item
    
    def close_spider(self,spider):
        self.filename.close()
        spider.crawler.engine.close_spider(spider,'停止运行')
    
    def write_to_txt(self,text_dict):
        #把抓取到的内容写入文件中
        try:
            for key,value in text_dict.items():
                self.filename.write(key+"内容:\n"+value+'\n')
            self.filename.write(50*'='+'\n')
        except Exception:
            pass #有时候文件IO关闭了，但scrapy没有退出会报错
