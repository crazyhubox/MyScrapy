from pprint import pformat
import re

class MetaItem(type):
    """Item的元类，将类的属性全部添加到类的field字典中"""
    _attr_find = re.compile(r'^\_+?')
    _fun_find = re.compile(r'function')
    def __init__(self,*args,**kwargs):
        self._instance = None
    
    def __new__(mcs,*args,**kwargs):
        cls_attrs = args[2]
        #*如果是继承 那么添加field属性
        if 'field' not in cls_attrs:
            cls_attrs.setdefault('field',dict())
            
        for k,v in cls_attrs.items():
            if not mcs._attr_find.search(k) and k != 'field':
                if not isinstance(v,Field) and not mcs._fun_find.search(str(v)):#*item类属性必须是Field类型
                    raise AttributeError(f'{args[0]} attrbute "{k}" must be Field()')  
                cls_attrs['field'].setdefault(k,v)
        
        return super().__new__(mcs,*args,**kwargs)

    def __call__(self,*args,**kwargs):
        if not self._instance:
            self._instance = super().__call__(*args,**kwargs)
        else:
            self._instance.__init__(*args,**kwargs)
        return self._instance


class Field:
    """属性描述符"""
    value = ''
    def __get__(self,instance,owner):
        return self.value

    def __set__(self,instance,value):
        if isinstance(value,str) or isinstance(value,int) or isinstance(value,list) or value is None:
            self.value = value
        else:
            raise ValueError('Must be str or int or list')
    
    def __repr__(self):
        return self.value


class MyItems(metaclass=MetaItem):
    field = {}
    
    def __init__(self):
        self.num = -1
    
    def __getitem__(self,key):
        if not hasattr(self,key):
            raise AttributeError(f'{self.__class__} has no {key}')
        
        elif isinstance(self.field[key],Field):
            getattr(self,key)
            return self.field[key]
        elif key in self.field:
            return self.field[key]
        
    def __setitem__(self,key,value):
        if key not in self.field:
            raise AttributeError(f'{self.__class__} has no {key}')
        else:
            setattr(self,key,value)
            self.field[key] = value
            
    def __repr__(self):
        return pformat(self.field)
        
    def __len__(self):
        return len(self.field)
    
    def __iter__(self):
        return (each  for each in self.field.keys())
   
    def keys(self):
        return self.field.keys()

    def values(self):
        return self.field.values()

