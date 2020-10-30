
__all__ = [
    'MyItems','MySpy',
    'ThreadImgSaver','AsyncImgSaver','Saver','CsvSaver','AhttpImgSaver',
    'MyRequest',
    'Engine','Field',
]

from myspider.Items import MyItems,Field
from myspider.Saver import ThreadImgSaver,AsyncImgSaver,AhttpImgSaver,Saver,CsvSaver
from myspider.Requests import MyRequest 
from myspider.Scheduler import Scheduler
from myspider.Download import Downloader


class MetaSpider(type):
    """Save the saver() obj for each spider"""
    def __new__(mcs,*args,**kwargs):
        attr_dict = args[2]
        #*保存spider.engine中的saver对象
        attr_dict['my_saver'] = attr_dict['engine'].callback.__dict__['_Scheduler__saver']
        attr_dict['_name'] = args[0]
        
        return super().__new__(mcs,*args,**kwargs)
    
class Engine:
    """
    调度器负责调度任务
        Request --> Downloader
        Item --> Saver
        
    下载器从Scheduler获取请求队列进行下载
    """
    def __init__(self,saver=None):
        self.__callback = Scheduler(saver)
        self.__downloader = Downloader(self.__callback)  

    @property
    def callback(self):
        return self.__callback
    
    @callback.setter
    def callback(self,value):
        self.__callback = value
    
    def run(self,start):
        self.__downloader.download(start)


class MySpy(metaclass=MetaSpider):
    name = str
    domain = 'excample.com'
    start_url = 'http://excample.com.cn/'
    engine = Engine()
    
    def __init__(self):
        pass
    
    def start_request(self):
        return  MyRequest(method='GET',url=self.start_url,callback=self.parse)

    @engine.callback
    def parse(self,Response):
        pass
       
    @engine.callback
    def parse_my(self,Response):
        pass
        
    def run_main(self):
        self.engine.callback = Scheduler(self.my_saver,self._name)  
        try:     
            self.engine.run(self.start_request())
        except Exception as e:
            print('Erro:',e)
        finally:
            if hasattr(self.my_saver,'spider_closed'):
                self.my_saver.spider_closed()




if __name__ == "__main__":
    test = MySpy()  
    print(test.my_saver)