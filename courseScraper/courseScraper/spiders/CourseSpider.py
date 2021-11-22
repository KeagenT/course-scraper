from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request
from courseScraper.items import SuCourse
from json import dumps,loads
from os import path
import re

def get_url_filepath(fileName = "CourseUrls.json"):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    urlsRelative = f"..\\..\\{fileName}"
    UrlFile = os.path.join(fileDir, urlsRelative)
    return UrlFile

def load_url_files(UrlFile):
    with open(UrlFile, 'r') as data_file:
        json_data = data_file.read()
    return json.loads(json_data)

def get_url_file(fileName = "CourseUrls.json"):
    UrlFilePath = get_url_filepath(fileName)
    LoadedUrlFile = load_url_files(UrlFilePath)
    return loadedUrlFile

def get_crawlable_url_array(loadedUrlFile):
    unjoined_arrays = [json['urls'] for json in loadedUrlFile]
    
