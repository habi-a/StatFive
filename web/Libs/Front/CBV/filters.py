from django.views import View

from django.shortcuts import render

from django.utils.translation import get_language

from django.conf.urls import url

from django.utils.decorators import method_decorator

from django.contrib.messages import get_messages

from django.contrib.auth.decorators import login_required

from rest_framework.response import Response

from Test.models import Tmp_Analysis
from Libs.Back.misc import Misc as m_
from Libs.Front.CBV.decorators import user_is_authorized
from Libs.Front.Forms.charfield import c
from Libs.Front.Forms.datefield import d
from Libs.Front.Forms.filefield import f
from Libs.Front.Forms.filefield import fs
from Libs.Front.Forms.selectfield import s
from Libs.Front.Forms.selectfield import sm
from Libs.Front.Forms.charfield import t

from django.utils.translation import ugettext as _
from django.db.models import Q

from Basis.models import Sys_Type
from Basis.models import Tmp
from Basis.models import User_Details
from Sod.models import Tmp_analysis


from django.forms import formset_factory
from rest_framework.views import APIView


class Filters():

    def _filter_analysis(self, request):
        draw = int(request.POST.get('draw', None))
        length = int(request.POST.get('length', None))
        start = int(request.POST.get('start', None))
        order_column = int(request.POST.get('order[0][column]', None)[0])
        order = request.POST.get('order[0][dir]', None)
        search_all = request.POST.get('search[value]', None)
        table_id = request.POST.get('id', None)

        ld_cols = [{'data': request.POST['columns[%s][data]' % x],
                    'name': request.POST['columns[%s][name]' % x],
                    'search': request.POST['columns[%s][search][value]' % x]}
                   for x in range(0, int(request.POST["len_columns"]))]

        if order == 'desc':
            order_column = '-' + order_column

        queryset = Tmp_analysis.objects.filter(c=Tmp(request.POST['csrf']))
        total = queryset.count()
        if search_all:
            queryset = queryset.filter(Q(csrf__TCD__icontains=search_all))
        count = queryset.count()
        #queryset = queryset.order_by(order_column)[start:start + length]

        """
        ld_cols = [{'data': request.POST['columns[%s][data]' % x],
                    'name': request.POST['columns[%s][name]' % x],
                    'search': request.POST['columns[%s][search][value]' % x]}
                   for x in range(0, int(request.POST["len_columns"]))]
        
        
        d_col_filter = {request.POST['columns[%s][data]' % x]: request.POST['columns[%s][search][value]' % x]
                        for x in range(int(request.POST["len_columns"]))
                        if request.POST['columns[%s][search][value]' % x] != ''}

        # move to first index
        l_cols = m_().move_item([col['data']
                                 for col in ld_cols],
                                order_column)
        total = len(Tmp_Analysis.objects.filter(id=request.POST['csrf']).values('content')[0]['content'][table_id])
        tmp = Tmp_Analysis.objects.filter(id=request.POST['csrf']).values('content')

        ld_filtered = m_().do_deduplicate_list_dict(l_cols,
                                                    tmp[0]['content'][table_id],
                                                    order)

        #ld_filtered = tmp[0]['content'][table_id]

        if search_all:
            ld_filtered = m_().do_search_list_dict(ld_filtered, search_all)

        ld_filtered = [d
                       for d in ld_filtered
                       if m_().do_filter_by_columns(d, d_col_filter)
                       ]
        """

        return Response({'data': queryset.values()[start:start + length],
                         'draw': draw,
                         'recordsTotal': total,
                         'recordsFiltered': count,
                         'columns': ld_cols
                         }, status=200, template_name=None, content_type=None)

