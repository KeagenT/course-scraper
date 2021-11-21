# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class SuCatalogPipeline(object):
    def open_spider(self,spider):
        if(spider.name == 'urlspider'):
            self.file = open('CourseURLs.json', 'w')
        if(spider.name == 'coursespider'):
            self.file = open('AllCourses.json', 'w')
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
