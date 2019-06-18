from django.db import models
from django.db.models import Q
from Basis.models import Tmp
from functools import reduce
from rest_framework.response import Response

import operator

class Tmp_manager(models.Manager):

    def range_slider(self, request):
        draw = int(request.POST.get('draw', None))
        length = int(request.POST.get('length', None))
        start = int(request.POST.get('start', None))
        order_column = int(request.POST.get('order[0][column]', None))
        order = request.POST.get('order[0][dir]', None)
        search_all = request.POST.get('search[value]', None)
        table_id = request.POST.get('id', None)
        ld_cols = [{'data': request.POST['columns[%s][data]' % x],
                    'name': request.POST['columns[%s][name]' % x],
                    'search': request.POST['columns[%s][search][value]' % x]}
                   for x in range(0, int(request.POST["len_columns"]))]
        if order == 'desc':
            order_column = '-' + ld_cols[order_column]['data']
        else:
            order_column = ld_cols[order_column]['data']

        queryset = self.filter(c=Tmp(request.POST['csrf']), table_id = table_id)
        total = queryset.count()
        if search_all:
            queryset = queryset.filter(reduce(operator.or_,
                                              [Q(**{"%s__icontains" % e.get_attname(): search_all})
                                               for e in self.model._meta.fields
                                               if e.get_attname().isupper()]))
        queryset = self._column_filter(queryset, ld_cols).order_by(order_column).distinct(*[e['data']
                                                                                            for e in ld_cols]).values(*[e['data']
                                                                                                                        for e in ld_cols]
                                                                                                                      )
        return Response({'data': queryset[start:start + length],
                         'draw': draw,
                         'recordsTotal': total,
                         'recordsFiltered': queryset.count(),
                         'columns': ld_cols
                         }, status=200, template_name=None, content_type=None)

    def _column_filter(self, query_set, l):
        li = [Q(**{"%s__icontains" % e['data']: e['search']})
              for e in l
              if e['search']
              ]
        if li:
            return query_set.filter(reduce(operator.and_,
                                           li
                                           )
                                    ).distinct()

        return query_set


