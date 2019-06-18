from django.views import View
from django.shortcuts import render
from django.utils.translation import get_language
from django.conf.urls import url
import json

from Libs.Back.misc import Misc as m_
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import get_messages
from django.forms import formset_factory
from django.utils.translation import ugettext as _


from Libs.Front.CBV.decorators import user_is_authorized
from Libs.Front.Forms.charfield import c
from Libs.Front.Forms.datefield import d
from Libs.Front.Forms.filefield import f
from Libs.Front.Forms.filefield import fs
from Libs.Front.Forms.selectfield import s
from Libs.Front.Forms.selectfield import sm
from Libs.Front.Forms.charfield import t


import operator
@method_decorator(login_required, name='dispatch')
#@method_decorator(user_is_authorized, name='dispatch')

class Base_view(View):
    TEMPLATE = 'template'
    URL = ''
    APPS = ""
    HTML = ""
    VIEW = ""
    API = ""
    # Form used by the view in the form selection included (form_selection.html)
    # its always
    # choices are (in list) :
    # user, ug, accnt, kostl, tcd, risk, cc, ... (more to come)
    PARAMETERS = {}
    FORMS = {}
    MODELS = {}

    def get(self, request, id=None):
        render_ = dict()
        # form creation
        render_ = m_().dict_merge(render_,
                                  self._generate_form(),
                                  operator.add)
        # form selection creation
        render_ = m_().dict_merge(render_,
                                  self._form_selection(),
                                  operator.add)
        # datatable creation
        render_ = m_().dict_merge(render_,
                                  self._generate_datatable(),
                                  operator.add)
        # special form creation
        render_ = m_().dict_merge(render_,
                                  self._special_form(),
                                  operator.add)
        # add somme value in the context
        render_.update({'current_lang' : get_language,
                        'messages': get_messages(request),
                        'APPS': self.APPS,
                        'VIEW': self.VIEW,
                        'HTML': self.HTML,
                        'URL' : self.URL
                        })
        return render(request,
                      self.TEMPLATE,
                      render_,
                      )


    def post(self, request):
        self.get(request)

    @classmethod
    def _url(self,f):
        path = f.replace('\\','/').split('/')
        return url(r'^%s/$'%(path[-1][:-3].lower()),
                   self.as_view(),
                   name='%s@%s'%(path[-3],
                                 path[-1][:-3])
                   )

    def _set_field_html_name(self, cls, new_name):
        """
        This creates wrapper around the normal widget rendering,
        allowing for a custom field name (new_name).
        """
        old_render = cls.widget.render
        def _widget_render_wrapper(name, value, attrs=None):
            return old_render(new_name, value, attrs)

        cls.widget.render = _widget_render_wrapper

    def _form_selection(self):
        return {}

    def _special_form(self):
        return {}

    def _get_parameters(self):
        pass

    def _button_submit_form_selection(self, list_forms):
        return {'l_forms_selection':list_forms,
                'l_id': json.dumps([list_forms[x][0].fields['c'].widget.attrs['id'].split('-')[-1]
                                    for x in range(1, len(list_forms) - 1)])
                }

    def _generate_datatable(self, method = None):
        return {}

    def _generate_form(self):
        if self.FORMS:
            l_forms = list()
            self.FIELDS = set()
            for form in self.FORMS:
                if form in ['c','d','f','fs','s','sm','t','b']:
                    if self.FORMS[form] > 0:
                        l_forms.append(formset_factory(eval(form),
                                                       extra=self.FORMS[form]
                                                       )()
                                       )
                        for x in range(self.FORMS[form]):
                            self.FIELDS.add('form-%s-%s'%(x,form))
            # return the forms and a button submit
            return {'l_forms':self._fill_forms(l_forms + ['<input type="submit" value="%s" class="btn btn-success btn-block" %s />'], self.request.user)}
        return {}

    def _fill_forms(self,list_forms, *args):
        return list_forms

