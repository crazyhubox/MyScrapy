import os
import sys
from mako.template import Template

def create_spider(path):
    if not os.path.exists(path):
        os.mkdir(path)
    
        

current_path = os.getcwd()
project = current_path.split('/')[-1]
project_name = project.capitalize()
current_path += '/' + project
args = sys.argv
SPIDER = args[1].capitalize()       
domain = args[2]        
url = 'https://'+domain+'/'        


create_spider(current_path+'/spider')
now = current_path + '/spider'



with open('/Users/crazyhubox/Desktop/MySpider/templates/settings.tmpl','r') as items_file:
    t = Template(items_file.read())
    with open(current_path+'/settings.py','w') as current_item_f:
        current_item_f.write(t.render(projectname=project_name,spidername=SPIDER))

with open('/Users/crazyhubox/Desktop/MySpider/templates/Spider.tmpl','r') as items_file:
    spider = Template(items_file.read())
    with open(now+'/__init__.py','w') as f:
        pass
    with open(now + '/Spider.py','w') as current_item_f:
        current_item_f.write(spider.render(project=project,projectname=project_name,spidername=SPIDER,domain=domain,url=url))

        
point_str = f"""
Spider {SPIDER} and settings files are created successfully.
"""
print(point_str)