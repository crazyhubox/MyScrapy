import ahttp
#TODO 将所有的request使用ahttp包装,使用ahttp的逻辑调度下载任务

class MyRequest:

    def __init__(self,
                 url:str,
                 method='GET',
                 callback=None,
                 headers:dict=None,
                 params:dict=None,
                 datas:dict=None,
                 meta:str=None,
                 dont_fliter=True
    ):
        self.method    = method
        self.url       = url
        self.headers   = headers
        self.callback = callback
        self.dont_fliter = dont_fliter
        if method == 'GET':
            self.params = params
        elif method == 'POST':
            self.datas = datas
        else:
            raise ValueError('The method must be "GET" or "POST"')
        self.meta = meta
                    
    @property
    def get_params(self):
        return {each_param:self.__dict__[each_param] for each_param in self.__dict__ if self.__dict__[each_param]}

    @classmethod
    def get(cls,*args,**kwargs):
        """GET"""
        return ahttp.get(*args,**kwargs)#*创建一个协程对象,请求还没有发出
        
    @classmethod    
    def post(cls,*args,**kwargs):
        """POST"""
        pass
    
    def run(self,*args,**kwargs):
        ahttp.run(*args,**kwargs)
    
    def __repr__(self):
        return f"<[Request] {self.url}>"

        
