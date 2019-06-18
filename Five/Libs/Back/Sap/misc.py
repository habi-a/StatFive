from django.utils.decorators import method_decorator
from pyrfc import *

import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime


class Misc():
    """
    pools of method hepling the treatment
    """
    def remove_blank(self, liste):
        """
        Remove all blank space in the beginnig and the end for all element in a list
        :param liste : [...,...,...]
        :return: [...,...,...] or str if an error is raised
        """
        # return using list comprehension
        if isinstance(liste, list):
            return [e.strip() for e in liste]
        else:
            return liste

    def get_bapi_status(self, fm_return):
        """
        Set the Sap message as an int for front end matter
        True = Exist
        1 = Action performed in SAP
        2 = Action no needed to be performed
        3 = Action not performed due to user maintenance
        4 = Users no longer exist
        5 = No value match
        6 = Roles assigned
        7 = Role assignment incomplete (due to 5 error)
        8 = Nb Profil max on user during the assigment
        9 = Other
        :param liste : {sys_name:massage,sys_name:message,...}
        :return: {int:reason,sys_name:Error,...}
        """
        # if fm_result is a str >> error generated
        if isinstance(fm_return, str):
            return fm_return
        else:
            if fm_return['RETURN'] == []:
                return fm_return
            elif isinstance(fm_return['RETURN'], list):
                fm_status = list()
                for element in fm_return['RETURN']:
                    log = self.retreave_bapi_status(element)
                    if log:
                        fm_status.append(log)
                return fm_status
            else:
                return [self.retreave_bapi_status(fm_return['RETURN'])]

    def retreave_bapi_status(self, field):
        if field['NUMBER'] in ['039', '246', '048']:
            return {1: field['MESSAGE']}
        elif field['NUMBER'] in ['029', '060']:
            return {2: field['MESSAGE']}
        elif field['NUMBER'] == '410':
            return {3: field['MESSAGE']}
        elif field['NUMBER'] == '124':
            return {4: field['MESSAGE']}
        elif field['NUMBER'] in ['004', '216']:
            return {5: field['MESSAGE']}
        elif field['NUMBER'] == '088':
            return {True: field['MESSAGE']}
        elif field['NUMBER'] == '049':
            pass
        elif field['NUMBER'] == '263':
            return {8: field['MESSAGE']}
        else:
            return {9: field['MESSAGE']}

    def launch_fm(self, sys, fm, **kwargs):
        """
        Lunch Sap fonction module
        fm = Name of SAP fonction module
        kwargs = parameter used by the function module
        Return Dict like {sys:FMresult, sys:Error}
        """
        try:
            with Connection(**sys) as _:
                if fm[:4] == 'BAPI':
                    return self.get_bapi_status(_.call(fm, **kwargs))
                else:
                    return _.call(fm, **kwargs)
        except ABAPApplicationError:
            return 'ABAPApplicationError'
        except ABAPRuntimeError:
            return 'ABAPRuntimeError'
        except CommunicationError:
            return 'CommunicationError'
        except ExternalApplicationError:
            return 'ExternalApplicationError'
        except ExternalAuthorizationError:
            return 'ExternalAuthorizationError'
        except ExternalRuntimeError:
            return 'ExternalRuntimeError'
        except LogonError:
            return 'LogonError'

    def read_table(self, d_sys, **kwargs):
        """
        Read a given table in SAP on given system
        Max size for options = 2000
        Max field size = 255 caracteres
        :param kwargs: {'QUERY_TABLE': str >> SAP Table,
                        'OPTIONS': ld [option, options etc.] >> for selection,
                        'FIELDS':[fieldname etc..] >> revelant field
        :return: {'SYS':[info...,...]} or {sys_name:Errortype}
        """
        if 'OPTIONS' in kwargs:
            kwargs['OPTIONS'] = [{'TEXT': option.upper()} for option in kwargs['OPTIONS']]
        if 'FIELDS' in kwargs:
            kwargs['FIELDS'] = [{'FIELDNAME': field.upper()} for field in kwargs['FIELDS']]
            if len(kwargs['FIELDS']) != 1:
                kwargs['DELIMITER'] = '|'
        ld_value = self.launch_fm(d_sys,
                                  'RFC_READ_TABLE',
                                  **kwargs)
        if isinstance(ld_value, str):
            return ld_value
        if 'DELIMITER' in kwargs:
            return [self.remove_blank(e['WA'].split(kwargs['DELIMITER']))
                    for e in ld_value['DATA']]
        else:
            return [e['WA'].strip()
                    for e in ld_value['DATA']]

    def fm_bool_info(self, fm_return):
        """
        Return Boolean or Error following result
        """
        if isinstance(fm_return, str):
            return fm_return
        elif fm_return == [] or fm_return == ['']:
            return False
        else:
            return True

    def launch_prg(self, d_sys, prg):
        return [e['ZEILE']
                for e in self.lunch_fm(d_sys,
                                       'RFC_ABAP_INSTALL_AND_RUN',
                                       **{'PROGRAM': prg,
                                          'MODE': 'F', }
                                       )['WRITES']
                ]

    def statrecs(self, d_sys, date=''):
        if not date:
            date = date.today() - timedelta(1)

        d = dict()
        # list comprehension to get the delta by 30 mins 
        for heure in [(str(x) + '0000', str(x) + '2959')
                      for x in range(24)] + \
                [(str(x) + '3000', str(x) + '5959')
                 for x in range(24)]:
            stat = self.lunch_fm(d_sys,
                                 'SWNC_GET_STATRECS_FRAME',
                                 **{'READ_START_DATE': date,
                                    'READ_START_TIME': heure[0],
                                    'READ_END_DATE': date,
                                    'READ_END_TIME': heure[1],
                                    'READ_TIME_ZONE': 'UTC',
                                    'READ_CLIENT': d_sys['client'],
                                    'READ_ONLY_MAINRECORDS': 'X',
                                    'READ_STAT': 'X',
                                    'READ_USERNAME': ''}
                                 )['ALL_STATRECS']
            # stat type = [{},{} ...]
            for instance in stat:
                # e = dico
                # instance['STATRECS'] type = [{},{} ...]
                for info in instance['STATRECS']:
                    info = info['MAINREC']
                    if info['TCODE'] not in ['', 'SESSION_MANAGER', 'SMEN']:
                        try:
                            d[info['ACCOUNT']][info['TCODE']].add(info['TRANSID'])
                        except:
                            try:
                                d[info['ACCOUNT']].update({info['TCODE']: {info['TRANSID']}})
                            except:
                                d[info['ACCOUNT']] = {info['TCODE']: {info['TRANSID']}}
        return d

    def sap_time_stamp(self, date):
        date = date.replace('.', '').split(',')[0]
        return datetime.strftime(datetime.strptime(date, '%Y%m%d%H%M%S'), '%Y.%m.%d %H:%M:%S')

    def options(self, field=str(), liste=list(), *args):
        return ["(%s EQ '%s')" % (field, liste[0].upper())
                if len(liste) == 1
                else
                "(%s EQ '%s' OR" % (field, liste[i].upper())
                if i == 0
                else
                "%s EQ '%s')" % (field, liste[i].upper())
                if i == len(liste) - 1
                else
                "%s EQ '%s' OR" % (field, liste[i].upper())
                for i in range(len(liste))
                ] + [arg
                     for arg in args
                     if arg
                     ]
