import csv
import hashlib
# import requests
import os
from faker import Faker
from myspider.Requests import MyRequest
from myspider.Scheduler import Scheduler
from concurrent.futures import ThreadPoolExecutor, Executor, as_completed
from aiohttp import ClientSession,ClientTimeout
import asyncio

FILE_PATH = os.getcwd()

class MetaSaver(type):
    """Saver类必须实现process_item方法"""
    def __new__(mcs, *args, **kwargs):
        if 'process_item' not in args[2]:
            raise AttributeError(f'Class {args[0]} need to define "process_item" function')
        return super().__new__(mcs, *args, **kwargs)


class Saver(metaclass=MetaSaver):
    """基类"""
    def process_item(self, Item):#*由spider返回
        pass


class ThreadImgSaver(Saver):
    """多线程版本"""
    def process_item(self, Item):
        img_urls = Item['img_urls']
        executor = ThreadPoolExecutor(max_workers=self.get_length(img_urls))
        tasks = [executor.submit(self.save_img, each) for each in img_urls]
        if __name__ == "__main__":
            pass

    def save_img(self, url):
        try:
            response = requests.get(url, timeout=3)
            print(f"<[ImgRequest] {response.url} {response.status_code}>")
            with open(self.file_path(response.url), 'wb') as img:
                img.write(response.content)
        except:
            pass

    @classmethod
    def file_path(cls, url):
        hex_ = hashlib.md5(url.encode()).hexdigest()
        return FILE_PATH + '/' + hex_ + '.jpg'

    def get_length(self, urls: 'Iterable'):
        eight_num = len(urls)//8
        if eight_num == 0:
            return 2
        else:
            return 8*eight_num


class AhttpImgSaver(Saver):
    """异步版本"""
    callback = Scheduler()

    # *使用调度器操作的版本,因实现的单例模式，全局的调度器只有一个
    @callback
    def process_item(self, Item):
        img_urls = Item['img_urls']
        for each in img_urls:
            yield MyRequest(url=each, callback=self.save_img)

    def save_img(self, response):
        try:
            rand_obj = Faker(locale='zh_CN')
            name = rand_obj.credit_card_number()
            print(f"<[ImgRequest] {response.url} {response.status}>")
            with open(f'{name}.jpg', 'wb') as img:
                print('+'*100)
                img.write(response.content)
        except Exception as e:
            print(e)


class AsyncImgSaver(Saver):
    def process_item(self, Item):
        img_urls = Item['img_urls']
        
        async def download_img(session,url):
            while url:
                try:
                    async with session.get(url) as rq:
                        print(f'<[Request {rq.status}] {url}>')
                        return await rq.read()
                except:
                    pass

        async def aio_res(img_urls:list):        
            time_out = ClientTimeout(total=8)
            tasks = []
            async with ClientSession(timeout=time_out) as session:
                for each in img_urls:
                    task = asyncio.create_task(download_img(session,each))
                    task.add_done_callback(self.save_img2)
                    tasks.append(task)
                await asyncio.gather(*tasks)
                
        asyncio.create_task(aio_res(img_urls))

    def save_img2(self,future):
        rand_obj = Faker(locale='zh_CN')
        name = rand_obj.credit_card_number()
        if future.result(): 
            with open(f'{name}.jpg','wb') as f:
                f.write(future.result())
                print(f'<[Success] {name}.jpg>')
        else:
            print('<[Fail] None to download>')

        

class CsvSaver(Saver):
    def __init__(self, CsvItem):
        try:
            self.fp = open(self.file_name()+'.csv', 'a+')
            headers = CsvItem().keys()
            self.writer = csv.DictWriter(self.fp, headers)
            self.writer.writeheader()
        except Exception as e:
            print(e)
            self.fp.close()

    def process_item(self, item):
        self.writer.writerow(dict(item))

    def spider_closed(self):
        self.fp.close()
        print('文件关闭')

    def file_name(self):
        name = FILE_PATH+'/' + FILE_PATH.split('/')[-1]
        return name


