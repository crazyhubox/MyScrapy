import sys
import os
import argparse

point_info = r"""
    myspy startproject  [projectname] 
    myspy crespider [spider] [domain]"""
    
parser = argparse.ArgumentParser(description='myspy is a crawl frame',usage=point_info)

select = sys.argv[1]
if select == 'startproject':
    proname = sys.argv[2]
    os.system(f'python3 -u "/Users/crazyhubox/Desktop/MySpider/create_project.py" {proname}')

elif select == 'crespider':
    spider = sys.argv[2]
    domain = sys.argv[3]
    os.system(f'python3 -u "/Users/crazyhubox/Desktop/MySpider/create_spider.py" {spider} {domain}')
else:
    parser.parse_args()
    # print(point_info)

    