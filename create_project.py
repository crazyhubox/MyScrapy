import sys
import os 
import argparse

args = sys.argv#list
project_name = args[1]
current_filepath = os.getcwd()
project_path = current_filepath+'/'+project_name

def create_project(path):
    if os.path.exists(path):
        pass
        # print(path)
    else:
        os.mkdir(path)

create_project(project_path)    
create_project(project_path+'/'+project_name)

 
from mako.template import Template
PROJECTNAME = project_name.capitalize()


with open(project_path+'/'+project_name+'/__init__.py','w') as f:
    pass

with open('/Users/crazyhubox/Desktop/MySpider/templates/Items.tmpl','r') as items_file:
    t = Template(items_file.read())
    with open(project_path+'/'+project_name+'/Items.py','w') as current_item_f:
        current_item_f.write(t.render(projectname=PROJECTNAME))

with open('/Users/crazyhubox/Desktop/MySpider/templates/Saver.tmpl','r') as items_file:
    t = Template(items_file.read())
    with open(project_path+'/'+project_name+'/Saver.py','w') as current_item_f:
        current_item_f.write(t.render(projectname=PROJECTNAME))

# with open('/Users/crazyhubox/Desktop/MySpider/templates/settings.tmpl','r') as items_file:
#     t = Template(items_file.read())
#     with open(project_path+'/'+project_name+'/settings.py','w') as current_item_f:
#         current_item_f.write(t.render(projectname=PROJECTNAME))

point_str=f"""
Project {project_name} files are created successfully.

Please enter the project {project_name} and

code your project."""
print(point_str)
    




