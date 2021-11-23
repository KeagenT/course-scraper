from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request
from courseScraper.items import SuCatalogItem


baseUrl = "http://catalog.shepherd.edu/content.php?catoid=16&catoid=16&navoid=2902&filter%5Bcpage%5D="
crawlthrough = [baseUrl + str(x) for x in range(1,20)]


class UrlSpider(Spider):
    name = 'urlspider'
    allowed_domains = ['catalog.shepherd.edu']
    start_urls = crawlthrough
    page = 1
    def parse(self, response):

        def url_ajaxify(x):
            unique_course = x.split('?')[1]
            return "http://catalog.shepherd.edu/ajax/preview_course.php?{}&show".format(unique_course)

        item = SuCatalogItem()
        course_urls = response.xpath('//td[@class="width"]//a[contains(@href, "coid")]//@href').getall()
        ajax_urls = [url_ajaxify(x) for x in course_urls]
        item['page'] = self.page
        item['urls'] = ajax_urls
        self.page = self.page+1
        yield item