from urllib.parse import urljoin
from scrapy import Selector


class MyResponse:

    def __init__(self,results:'response_obj'):
        self.url = str(results.url)
        self.headers=  results.headers
        self.status = results.status
        self.text = results.text
        self.content = results.content
        self.find = Selector(text=self.text)
        
    def css(self,css_str):
        return self.find.css(css_str)
    
    def join(self,url_):
        return urljoin(base=self.url,url=url_)
        


    