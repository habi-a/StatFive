from copy import copy

from django.utils.translation import ugettext as _
from django.urls import get_resolver
from django.conf import settings

from collections import defaultdict as dd
from random import randint,shuffle
from configparser import ConfigParser

import datetime
import json
import importlib
import collections
import string
import csv
import operator

class Misc():
    """
    pools of method hepling the treatment
    """

    def __init__(self):
        pass

    def create_dict(self, liste, nb = 1):
        """
        liste = [[],[],[],[]]
        Return a dict with depth = nb
        return {k:k...k:[[],[],[]]}
        """
        d = dd(list)
        for e in liste:
            d[e[0]].append(e[1:])
        d = dict(d)
        nb -=1
        if nb == 0:
            return d
        else:
            for cle in d:
                d[cle] = self.create_dict(d[cle],nb)

        return d

    def do_dict_set(self, liste, nb = 1):
        """
        liste = [[],[],[],[]]
        Return a dict with depth = nb
        return {k:k...k:{.....(tuple or str)}}
        """
        if isinstance(liste,(list,tuple)):
            d = self.create_dict(liste,nb)
        else:
            d = liste
        for cle in d:
            if isinstance(d[cle],(list,tuple)):
                d[cle] = {e[0]
                          if len(e) == 1
                          else
                          tuple(e)
                          for e in d[cle]}
            else:
                self.do_dict_set(d[cle])
        return d

    def do_dict_sum(self, liste, nb = 1):
        """
        liste = [[],[],[],[]]
        Return a dict with depth = nb
        return {k:k...k:{.....(tuple or str)}}
        """
        if isinstance(liste,(list,tuple)):
            d = self.create_dict(liste,nb)
        else:
            d = liste
        for cle in d:
            if isinstance(d[cle],(list,tuple)):
                d[cle] = sum([e[0]
                              if len(e) == 1
                              else
                              tuple(e)
                              for e in d[cle]])
            else:
                self.do_dict_sum(d[cle])
        return d

    def do_dict_list(self, liste, nb = 1):
        """
        liste = [[],[],[],[]]
        Return a dict with depth = nb
        return {k:k...k:{.....(tuple or str)}}
        """
        if isinstance(liste,(list,tuple)):
            d = self.create_dict(liste,nb)
        else:
            d = liste
        for cle in d:
            if isinstance(d[cle],(list,tuple)):
                d[cle] = [e[0]
                          if len(e) == 1
                          else
                          tuple(e)
                          for e in d[cle]]
            else:
                self.do_dict_list(d[cle])
        return d

    def do_dict_str(self, liste, nb = 1):
        """
        liste = [[],[],[],[]]
        Return a dict with depth = nb
        return {k:k...k:str}}
        """
        if isinstance(liste,(list,tuple)):
            d = self.create_dict(liste,nb)
        else:
            d = liste
        for cle in d:
            if isinstance(d[cle],(list,tuple)):
                d[cle] = d[cle][0][0]
            else:
                self.do_dict_str(d[cle])
        return d

    def union_dicts(self, a, b, op=operator.add):
        if not b:
            return a
        d = dict()
        for k in set(a) & set(b):
            if isinstance(b[k],dict):
                d[k] = self.union_dicts(a[k],b[k],op)
            else:
                d[k] = op(a[k], b[k])

        for i in set(a)-set(b):
            d[i] =a[i]
        return d

    def dict_merge(self,dct, merge_dct,op=operator.or_):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``dct``.
        :param dct: dict onto which the merge is executed
        :param merge_dct: dct merged into dct
        :return: None
        """
        if dct == merge_dct:
            return dct
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
                self.dict_merge(dct[k], merge_dct[k],op)
            else:
                if k not in dct:
                    dct[k] = merge_dct[k]
                else:
                    dct[k] = op(dct[k],merge_dct[k])
        return dct

    def dict_2_list(self,d):
        res = []
        for k,v in d.items():
            li = []
            if isinstance(v,dict):
                for vk,vv in v.items():
                    li.extend([[k]+ e
                               for e in self.dict_2_list({vk:vv})])
            elif isinstance(v,(list,tuple,set)):
                li = [[k,e]
                      for e in v]
            else:
                li = [[k,v]]
            res.extend(li)
        return res

    def create_pwd(self):
        """
        Auto pwd generation
        return str
        """
        pwd = []
        for x in range(5):
            pwd.append(string.ascii_lowercase[randint(0,len(string.ascii_lowercase)-1)])
            pwd.append(string.ascii_uppercase[randint(0,len(string.ascii_uppercase)-1)])
            pwd.append(string.digits[randint(0,len(string.digits)-1)])
            pwd.append(string.punctuation[7:20][randint(0,len(string.punctuation[7:20])-1)])
        shuffle(pwd)
        return ''.join(pwd)

    def base36encode(self,number,taille):
        """Converts an integer into a base36 string."""

        ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if not isinstance(number, int):
            raise TypeError('This function must be called on an integer.')

        base36 = ''

        while number != 0:
            number, i = divmod(number, len(ALPHABET))
            base36 = ALPHABET[i] + base36
        return '0'*(taille-len(base36))+base36


    def base36decode(self,number):
        return int(number, 36)

    def produit_matriciel(self,liste):
        # une liste en entrée [[1,2],[3],[4,5]]
        #pour un résulat [[1,3,4],[1,3,5],[2,3,4],[2,3,5]]
        # sert pour une liste qui contient n liste
        if len(liste) == 1:
            return liste
        for x in range(len(liste)):
            if x == 0:
                li = [[e] for e in liste[x]]
            else:
                li = [e + [i]
                      for e in li
                      for i in liste[x]]
        return li

    def F110(self,liste,option):
        for x in range(len(liste)):
            liste[x]=sorted(liste[x])
        if option=='F110':
            return [[liste[0][z],
                     liste[1][z],
                     liste[2][0]]
                    for z in range(len(liste[0]))]
        else:
            return [[liste[0][z],
                     liste[1][z],
                     liste[2][0],
                     liste[3][0]]
                    for z in range(len(liste[0]))]

    def create_list_dict(self, key, iterable):
        """return a list of dict [{key[0]:iterable[0][0],}...] """
        li = list()
        [li.append(dict(zip(key, values)))
         for values in iterable]
        return li

    def d_depth(self,d):
        """return dico depth as inter"""
        if isinstance(d, dict):
            return 1 + (max(map(self.d_depth, d.values())) if d else 0)
        return 0

    def get_urls(self):
        """return dict for set {apps:{url,url},...}"""
        return self.do_dict_set([e.split('@')
                                 for e in get_resolver(None).reverse_dict.keys()
                                 if isinstance(e,str)
                                 if '@' in e
                                 ])

    def read_file(self, file):
        with open(file, 'r') as f:
            return f.readlines()

    def do_search_list_dict(self, ld, search):
        return [e
                for e in ld
                if search in ''.join([v for k, v in e.items()])]

    def move_item(self, l, old, index=0):
        l.insert(index, l.pop(old))
        return l

    def do_filter_by_columns(self, d, d_col):
        cpt = 0
        for key in d_col:
            if str(d_col[key]).upper() in str(d[key]).upper():
                cpt += 1
            else:
                break

        if cpt == len(d_col):
            return True

    def do_deduplicate_list_dict(self, l_col, ld, order):
        l = [{e.split('|-|-|')[0]: e.split('|-|-|')[1]
              for e in sorted(fs)}
             for fs in list({frozenset('%s|-|-|%s' % (k, d[k])
                                       for k in d
                                       if k in l_col)
                             for d in ld})]
        return sorted(l,
                      key=lambda l: l[l_col[0]],
                      reverse=True if order == 'desc' else False)

    def list_insert(self, li: list, value, position):
        """
        insert element into list or list of list
        Usefull for comprehesion list
        :type li: list
        """
        if isinstance(li, list):
            if isinstance(li[0], list):
                [e.insert(position, value) for e in li]
            else:
                li.insert(position, value)
        return li

    def is_key(self, key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                return True
            elif isinstance(v, dict):
                return self.is_key(key, v)
            elif isinstance(v, list):
                for d in v:
                    if isinstance(d, dict):
                        return self.is_key(key, d)

    def date_range(self,days = 1):
        return sorted({'%s%s'%((datetime.datetime.now()-datetime.timedelta(days =x)).strftime('%m'),
                               (datetime.datetime.now() - datetime.timedelta(days=x)).strftime('%d')
                               )
                       for x in range(days)
                       }
                      )

    def update(self, d1, d2):
        d1.update(d2)
        return d1

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set, tuple):
            return list(obj)
        return json.JSONEncoder.default(self, obj)