
class Downloader:
    """请求下载器"""
    def __init__(self,Scheduler):
        """需要接收调度器"""
        self.__sche = Scheduler


    def download(self,res_):
        self.__sche.arrange_request(res_)#*得到下载队列
        while not self.__sche.url_queue.empty():
            tasks = []
            while not self.__sche.url_queue.empty():
                my_request = self.__sche.url_queue.get()
                tasks.append(my_request.get(my_request.url,callback=my_request.callback))
            my_request.run(tasks)
        