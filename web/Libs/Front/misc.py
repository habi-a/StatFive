from django.utils.translation import ugettext as _
from django.urls import get_resolver
from django.conf import settings

from Basis.models import Sys_Type as st_

from collections import defaultdict as dd
from random import randint,shuffle
from configparser import ConfigParser
from Libs.Front.CBV.get_urls import get_urls

import os
import json
import importlib
import collections
import string
import csv
import operator

class Misc():
    """
    pools of method hepling the treatment for front support of the game yeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah
    """

    def __init__(self):
        pass

    def check_sys(self, l_sys):
        return set(l_sys).issubset({e['system']
                                    for e in st_.objects.values('system')})

    def get_list_app(self):
        config_module = __import__('Swing.settings')
        return [url.name
                for a in [e
                          for e in os.listdir(config_module.settings.APPS_DIR)
                          if e[0].isupper()
                          ]
                for url in get_urls("%s\\%s\\" % (config_module.settings.APPS_DIR, a), "%s.urls" % a)
                ]