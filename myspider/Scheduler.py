from queue import Queue
from pybloom_live import BloomFilter
from collections import abc
from functools import wraps   

from myspider.Response import MyResponse
from myspider.Items import MyItems



class MetaScheduler(type):
    """单例模式元类"""
    def __init__(self,*args,**kwargs):
        self._instance = None
        
    def __call__(self,*args,**kwargs):
        if not self._instance:
            self._instance = super().__call__(*args,**kwargs)
        elif args is not ():
            self._instance.__init__(*args,**kwargs)
        return self._instance


class Scheduler(metaclass=MetaScheduler):
    def __init__(self,*args):
        self.__fliter = BloomFilter(capacity=100000, error_rate=0.001)
        self.__rq_queue = Queue(10000)
        self._savers = {}
        #*这里saver的问题在spider中解决
        if args is not ():
            self.__saver = args[0]
        if len(args) == 2:
            self._savers[args[1]] = args[0]


    def arrange_request(self,Requests):
        """arrange requests"""
        if isinstance(Requests,abc.Iterable):
            for each in Requests:
                print(each)
                if isinstance(each,str):
                    return 
                if each.dont_fliter and not self.__fliter.add(each.url):
                    self.__rq_queue.put(each)
                else:
                    self.__rq_queue.put(each)

        elif Requests.dont_fliter and not self.__fliter.add(Requests.url):
            print(Requests)
            self.__rq_queue.put(Requests)

        else:
            print(Requests)
            self.__rq_queue.put(Requests)
        
    def __call__(self,func):
        """调度器的回调装饰器"""
        @wraps(func)
        def f(*args,**kwargs):
            """控制回调"""
            self.__saver = self.fromFuncGetSaver(func)

            #*将来自ahttp的响应对象进行封装
            if not isinstance(args[1],MyItems):
                response = MyResponse(args[1])
                res_ = func(args[0],response)
            else:
                res_ = func(*args,**kwargs)
            #*处理直接返回的item   
            if isinstance(res_,MyItems):
                for each in res_:
                    print(f"<[Item]{res_[each]}>")
                self.__saver.process_item(res_)
                return res_
            #*处理生成器item或者Request
            elif res_:
                for each in res_:
                    if isinstance(each,MyItems):
                        #*csv文件的处理    
                        print(f"<[Item]{each}>")
                        self.__saver.process_item(each)
                    else:
                        #*Request请求的处理
                        self.arrange_request(each)
                return res_
        return f
  
    @property
    def url_queue(self):
        return self.__rq_queue
        
    def fromFuncGetSaver(self,func:'function')->'Saver':
        return self._savers.get(func.__qualname__.split('.')[0],None)
    
    


    
    