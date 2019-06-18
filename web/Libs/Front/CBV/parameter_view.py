import os

from Libs.Back.misc import Misc as m_
from Libs.Front.CBV.base_view import Base_view as cbv
from Libs.Front.CBV.get_urls import get_urls
from Libs.Front.misc import Misc as mf_
from django.utils.translation import ugettext as _

from Basis.apps import BasisConfig as apps
from Basis.models import Parameter as p
from Basis.models import Field as pf

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from operator import __or__
from threading import Thread as th
from importlib import import_module
from time import sleep


# @method_decorator(login_required, name='dispatch')
# @method_decorator(user_is_authorized, name='dispatch')
class Parameter_view():

    def __init__(self):
        pass

    def init_parameters(self):
        """
        Init parameters in database if not in
        It parse all app to get it
        :return: l_url to get
        """

        # Get all apps name
        l_url = mf_().get_list_app()
        # e.split('@')[0] -> App name
        # e.split('@')[1] -> View name
        qs = p.objects.filter(url__in=["/%s/%s/" % (e.split('@')[0].lower(), e.split('@')[1])
                                       for e in l_url]).values_list()

        l_apps = ["%s.Enabled_Views.%s" % (e.split('@')[0], e.split('@')[1])
                  for e in l_url
                  ]

        # Merge all dict PARAMETERS to get all parameters possible in the project from views (init)
        d_ = {"/%s/%s/" % (e.split('.')[0].lower(), e.split('.')[-1]): getattr(import_module(e),
                                                                               e.split('.')[-1].capitalize()).PARAMETERS
              for e in l_apps
              if getattr(import_module(e), e.split('.')[-1].capitalize()).PARAMETERS
              }

        # Insert or update in Parameter table
        # Insert in Parameter_Field table if doesn't exists
        # with the same comprehension list
        #print(d_['/sod/analysis/']['tables']['sod1'])

        # TODO : Trop long !
        """
        test = [(p.objects.update_or_create(url=k,
                                            defaults={'params': v}
                                            ),
                 [pf.objects.update_or_create(f=e[-2])
                  for e in m_().dict_2_list(v)
                  ]
                 )
                for k, v in m_().union_dicts(d_, {e[0]: e[1]
                                                  for e in qs}
                                             , __or__).items()

                ]
        """

        test = [(p(url=k, params=v),
                 [pf(f=e[-2])
                  for e in m_().dict_2_list(v)
                  ]
                 )
                for k, v in m_().union_dicts(d_, {e[0]: e[1]
                                                  for e in qs}
                                             , __or__).items()

                ]
        self._update_database([e[0] for e in test])
        self._update_database(list({a
                                    for e in test
                                    for a in e[1]
                                    })
                              )

        return l_url

    def get_parameters_from_url(self, l_url):
        """
        Retreive dict of param from given list of url
        :param l_url:
        :return: A dict of {url: params}
        """
        l_apps = ["%s.Enabled_Views.%s" % (e.split('@')[0], e.split('@')[1])
                  for e in l_url
                  ]

        return {"/%s/%s/" % (e.split('.')[0].lower(), e.split('.')[-1]): getattr(import_module(e),
                                                                                 e.split('.')[-1].capitalize()).PARAMETERS
                for e in l_apps
                if getattr(import_module(e), e.split('.')[-1].capitalize()).PARAMETERS
                }

    def _update_database(self, li_):
        print(li_)
        for x in range(0, len(li_), 5):
            try:
                a= th(None,
                      self._update_or_create_thread,
                      None,
                      (li_[x],),
                      None)
                a.start()
            except: pass
            try:
                a = th(None,
                       self._update_or_create_thread,
                       None,
                       (li_[x+1],),
                       None)
                a.start()
            except: pass
            try:
                a = th(None,
                       self._update_or_create_thread,
                       None,
                       (li_[x+2],),
                       None)
                a.start()
            except: pass
            try:
                a = th(None,
                       self._update_or_create_thread,
                       None,
                       (li_[x+3],),
                       None)
                a.start()
            except: pass
            try:
                a = th(None,
                       self._update_or_create_thread,
                       None,
                       (li_[x+4],),
                       None)
                a.start()
            except: pass
            a.join()
            sleep(0.250)

    def _update_or_create_thread(self, e):
        #for e in li_:
        if e._meta.model_name == "parameter":
            p.objects.update_or_create(url=e.url, defaults={'params': e.params})
        elif e._meta.model_name == "field":
            pf.objects.update_or_create(f=e.f)
        from django.db import connections
        connections.close_all()
