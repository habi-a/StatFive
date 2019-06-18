from django.core.management.commands import startapp
import os, sys

def create_apps(apps,desc):
    apps = '_'.join([e.capitalize()
                     for e in apps.replace(' ','').split('_')]
                     )

    #path = 'C:/Users/%s/Desktop/Ticketing/APPS/' % os.environ['USERNAME']
    path = os.path.dirname(sys.argv[0]) + "/APPS/"
    pp = path + '/%s'%apps
    os.makedirs(path + '/' + apps)
    for e in ['Disabled_Views','Enabled_Views','templates','Internal_API']:
        os.makedirs(path + '/' + apps + '/%s'%e)
    os.system('django-admin.py startapp %s %s'%(apps,pp))
    with open(pp+'/views.py','w') as f:
        f.write('from %s.Enabled_views import *'%apps)

    with open(pp+'/urls.py','w') as f:
        [f.write(e) for e in ['from Libs.Front.CBV.get_urls import get_urls\n',
                              'from %s.Enabled_Views import *\n'%apps,
                              '\n',
                              'urlpatterns = get_urls(__file__,__name__)'
                              ]
         ]
    with open(pp+'/apps.py','w',encoding="utf-8") as f:
        [f.write(e) for e in [#'# coding: utf-8\n',
                              'from django.apps import AppConfig\n',
                              'from django.utils.translation import ugettext as _\n',
                              '\n',
                              'class %sConfig(AppConfig):\n'%apps.replace('_',''),
                              "    name = '%s'\n"%apps,
                              "    verbose_name = _('%s')\n"%apps.replace('_',' '),
                              '    desc = _("""%s""")'%desc
                              ]]

    with open(pp+'/workflow.py','a') as f:
        pass

    with open(pp+'/decorator.py','a') as f:
        pass    
        
if __name__ == '__main__':
    apps = input("App name :")
    desc = input("App desc :")
    create_apps(apps,desc)




