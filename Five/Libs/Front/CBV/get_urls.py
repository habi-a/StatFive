import os
from importlib import import_module

def get_urls(file_,name_, enabled="Enabled_Views"):
    path = '/'.join(file_.replace('\\','/').split('/')[:-1]+["%s/" % enabled])
    name_ = name_.split('.')[0]+'.%s.'% enabled
    return [getattr(import_module(name_+file[:-3]),
                    file[:-3].capitalize()
                    )._url(path + file)
            for folder in list(os.walk(path))
            if folder[0]== path
            for file in folder[-1]
            if '.pyc' not in file
            ]
