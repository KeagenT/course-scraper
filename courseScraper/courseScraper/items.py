# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class SuCatalogItem(scrapy.Item):
    page = Field()
    urls = Field()
    pass

class SuCourseItem(scrapy.Item):
    id = Field()
    name = Field()
    description = Field()
    prerequisites = Field()
    pass



