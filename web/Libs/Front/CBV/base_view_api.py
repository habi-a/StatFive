from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.conf.urls import url
from django.db.models import Q
from django.forms import formset_factory

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


from Libs.Front.CBV.filters import Filters

from Basis.models import Sys_Type
from Basis.models import User_Details
from Basis.models import Tmp

from Libs.Back.misc import Misc as m_
from Libs.Front.misc import Misc as fm_

from datetime import date

import json
import sys

class Base_view_api(APIView, Filters):
    VIEW = ""
    APPS = ""
    TEMPLATE = ""
    HTML = ""  # call Libs.Front.HTML
    URL = ""  # Url of the page
    # forms used by the view
    # go to Libs.front.CBV to get the available value for the kwargs
    # 's' for selectfiels
    # 'sm' for selectmultiplefields
    # 't' for textareafield
    # 'c' for charfield
    # 'f' for filefield
    # 'fs' for filesfiled
    FORMS = {}

    #parser_classes = (JSONParser,)

    def post(self, request):
        url = request.META.get('HTTP_REFERER').split(request.META.get('HTTP_ORIGIN'))[-1]
        d_table = json.loads(request.data.get('tables','[]'))
        d_form = json.loads(request.data.get('data','[]'))
        method = None
        d = {}

        # TODO :error check return
        if not fm_().check_sys(d_form['sys']) or not d_form:
            return Response({'data': {}}, status=200, template_name=None, content_type=None)

        try:
            # Deletion to be sure
            Tmp.objects.filter(*[Q(csrf=request.data['csrf'])|Q(date__lt=date.today())]).delete()
        except Exception as e:
            print("Base_view_api : No line to delete : %s" % e)

        try:
            # try getting method
            method = getattr(self, '_%s'%request.data['method'])
        except Exception as e:
            # If method doesn't exists
            print(e)
            return Response({}, status=400, template_name=None, content_type=None)

        if d_table:
            # if requeset came form datatable
            tmp = Tmp.objects.create(csrf=request.data['csrf'],
                                     url=url,
                                     user=request.user)

            try:
                # Dict comprehension ton get {modelInstance : [list of instruction]}
                # app and model come from front end (_generate_datatable from Basqe_view)
                self._update_database({getattr(__import__("%s.models" % d_table[key]['app']).models,
                                               d_table[key]['model']):
                                           [getattr(__import__("%s.models" % d_table[key]['app']).models,
                                                    d_table[key]['model'])(**m_().update(e,
                                                                                         {'c': tmp,
                                                                                          'table_id': key}
                                                                                         )
                                                                           )
                                            for e in method(d_form)
                                            ]
                                       for key in d_table
                                       }
                                      )
            except Exception as e:
                print("Error : Base_view_api : update_database" % e)
                return Response(status=400, template_name=None, content_type=None)
            return Response({'data': d_table.keys(),
                             }, status=200, template_name=None, content_type=None)

        elif d_form:
            return Response({'data': method(d_form),
                             }, status=200, template_name=None, content_type=None)
        else:
            return Response(status=400, template_name=None, content_type=None)

    def _update_database(self,li_):
        from threading import Thread as th
        for model in li_:
            for x in range(0,len(li_[model]), 10000):
                th(None,
                   self._bulk_thread,
                   None,
                   (model, li_[model][x:x+10000],),
                   None).start()

    def _bulk_thread(self, model, l):
        model.objects.bulk_create(l)
        from django.db import connections
        connections.close_all()

    @classmethod
    def _url(self,f):
        path = f.replace('\\','/').split('/')
        return url(r'^%s/$'%(path[-1][:-3].lower()),
                   self.as_view(),
                   name='%s@%s'%(path[-3],
                                 path[-1][:-3])
                   )

    def _collapse_navs(self, l_users,**kwargs):
        l_qs = {'%s' % e['fk__uuid']: '%s %s - %s' % (e['firstname'], e['lastname'], e['email'])
                for e in User_Details.objects.filter(fk__in=l_users).values('firstname',
                                                                            'lastname',
                                                                            'email',
                                                                            'fk__uuid')}
        d = {}
        if kwargs:
            d_forms = {e:kwargs
                       for e in list(Sys_Type.objects.all().values_list('system',
                                                                        flat=True))}
            for user in l_users:
                for sys in d_forms:
                    l_forms = self._generate_form(**d_forms[sys])
                    for x in range(len(l_forms[0])):
                        # select multiple management
                        if '.sm' in str(type(l_forms[0][x])):
                            if x == 0:
                                l_forms[0][x]['sm'].label = _('Assigned Rights')
                                l_forms[0][x].fields['sm'].widget.attrs['id'] = '%s_%s_before' % (user, sys)
                                l_forms[0][x].fields['sm'].choices = [(str(x),str(x)) for x in range(0,10)]
                            else:
                                l_forms[0][x]['sm'].label = _('Rights to be assigned')
                                l_forms[0][x].fields['sm'].widget.attrs['id'] = '%s_%s_after' % (user, sys)
                                l_forms[0][x].fields['sm'].choices = [(str(x),str(x)) for x in range(10,20)]
                        # datefield multiple management
                        elif '.d' in str(type(l_forms[0][x])):
                            if x == 0:
                                l_forms[0][x]['d'].label = _('From date')
                                l_forms[0][x].fields['d'].widget.attrs['id'] = '%s_%s_before' % (user, sys)
                            else:
                                l_forms[0][x]['d'].label = _('End date')
                                l_forms[0][x].fields['d'].widget.attrs['id'] = '%s_%s_after' % (user, sys)
                    if user in d:
                        d[user].update({sys: l_forms[0]})
                    else:
                        d[user] = {sys: l_forms[0]}
        else:
            d_forms = {e: ''
                       for e in list(Sys_Type.objects.all().values_list('system',
                                                                        flat=True))}
            print(d_forms)
            for user in l_users:
                for form in d_forms:
                    if user in d:
                        d[user].update({form:d_forms[form]})
                    else:
                        d[user] = {form:d_forms[form]}
        return [d,l_qs]

    def _generate_form(self,**kwargs):
        l_forms = list()
        self.FIELDS = set()
        for form in kwargs:
            if form in ['c','d','f','fs','s','sm','t']:
                if kwargs[form] > 0:
                    l_forms.append(formset_factory(eval(form),
                                                   extra=kwargs[form]
                                                   )()
                                   )
                    for x in range(kwargs[form]):
                        self.FIELDS.add('form-%s-%s'%(x,form))
        return l_forms


