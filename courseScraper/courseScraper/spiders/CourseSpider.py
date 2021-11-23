from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request
from courseScraper.items import SuCourseItem
from json import loads
from os import path
import re
DEFAULT_FILE = "CourseUrls.json"
def get_url_filepath(fileName = DEFAULT_FILE):
    fileDir = path.dirname(path.realpath('__file__'))
    urlsRelative = f"..\\{fileName}"
    UrlFile = path.join(fileDir, urlsRelative)
    return UrlFile

def load_url_files(UrlFile):
    with open(UrlFile, 'r') as data_file:
        json_data = data_file.read()
    return loads(json_data)

def get_url_file(fileName = DEFAULT_FILE):
    UrlFilePath = get_url_filepath(fileName)
    LoadedUrlFile = load_url_files(UrlFilePath)
    return LoadedUrlFile

def get_crawlable_url_array(loadedUrlFile):
    url_pages = [json['urls'] for json in loadedUrlFile]
    flattened_urls = [url for page in url_pages for url in page]
    return flattened_urls

def get_urls_from_json(fileName = DEFAULT_FILE):
    loadedUrlFile = get_url_file(fileName)
    crawlableArray = get_crawlable_url_array(loadedUrlFile)
    return crawlableArray

crawlthrough = get_urls_from_json(DEFAULT_FILE)

class CourseSpider(Spider):
    name = 'coursespider'
    allowed_domains = ['catalog.shepherd.edu']
    start_urls = crawlthrough
    REQUISITE = "((?:[A-z/]*?)quisite(?:s?):)"
    P_REQUISITE = re.compile(REQUISITE)
    COURSE = "((?:[A-Z]{3,4}) (?:[0-9]{3}))"
    P_COURSE = re.compile(COURSE)
    def parse(self, response):
        dirty_description = "".join(response.xpath(".//div[h3]/*[strong]/text()|.//div[h3]/text()").getall())
        has_prereq = self.P_REQUISITE.search(dirty_description)
        dirty_title = response.xpath(".//div[h3]//h3/text()").getall()[0]
        def clean_description(dirty_description, has_prereq):
            if has_prereq:
                #clean_description = dirty_description.split(has_prereq.group(0))[0].decode('unicode-escape')
                clean_description = re.split(self.REQUISITE, dirty_description)[0]
                clean_description = clean_description.strip()
                clean_description = clean_description.encode("unicode-escape").decode("unicode-escape")
                return clean_description
            else:
                clean_description = dirty_description.strip()
                return clean_description

        def clean_title(dirty_title):
            ID, Name = (item.strip() for item in dirty_title.split(" - "))
            return ID, Name
        
        def clean_prereqs(has_prereq):
            if(has_prereq):
                #trailing sibling nodes of "prerequisite" text node for all page structure variations
                obnoxious_course_path = response.xpath("//text()[contains(.,'quisites:') or contains(.,'quisite:')]/following-sibling::*/a//text()|//text()[contains(.,'quisites:') or contains(.,'quisite:')]/following-sibling::a//text()|//text()[contains(.,'quisites:') or contains(.,'quisite:')]/following-sibling::*[@class='acalog-permalink-inactive']/text()").getall()
                all_requisites = obnoxious_course_path
                return all_requisites
            else:
                return []
        

        item = SuCourseItem()
        item['id'] = clean_title(dirty_title)[0]
        item['name'] = clean_title(dirty_title)[1]
        item['description'] = clean_description(dirty_description, has_prereq)
        item['prerequisites'] = clean_prereqs( has_prereq)
        #item['url'] = response.request.url
        yield item