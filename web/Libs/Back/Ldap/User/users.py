from ldap3 import *
from collections import defaultdict as dd
import ssl
#from Libs.misc import Misc as m()

from Libs.misc import Misc as m

class Users():

    def __init__(self,sys):
        """
        Class for managing Users in LDAP
        input dict with the connection info
        self.base = base of LADP tree
        self.sys_name = sys_name of ldap
        self.d_sys = conection info to LDAP
        """
        sys = m().get_sys_info(sys)
        self.base = sys.pop('base')
        self.sys_name = sys.pop('sys_name')
        self.d_sys = sys
        tls_configuration = Tls(validate=ssl.CERT_REQUIRED,
                                version=ssl.PROTOCOL_TLSv1)
        # Free ipa Case has to be removed for customer
        tls_configuration.validate = ssl.CERT_NONE
        self.d_sys['server'] = Server(self.d_sys['server'],
                                      tls = tls_configuration)

    def get_users(self,*args,**kwargs):
        """
        Method to get all the users
        *args = used for getting the attribut of user
        **kwargs used for selected options
                 'USERS' > has to be a Query for searching request
                 'OU' > find the user from a DC or OU
        if USER >> return {sys_name:user:attribute}
        if OU >> return {sys:ou:user:attribute}
            
        """
        d = dd(dict)
        d[self.sys_name]
        if 'USERS' in kwargs:
            with Connection(**self.d_sys) as ad:
                for user in Reader(**{'connection':ad,
                                      'object_def':ObjectDef('inetOrgPerson',
                                                             ad),
                                      'base':self.base,
                                      'query':kwargs['USERS'],
                                      }).search_paged(1000):
                    d_user = dict()
                    if args:
                        d_user[user.entry_attributes_as_dict['uid'][0]] = {
                            k.lower():''
                            if not v
                            else
                            [x.lower() for x in v]
                            if len(v) > 1
                            else
                            v[0].lower()
                            for k,v in user.entry_attributes_as_dict.items()
                            if k in args}
                    else:
                        d_user[user.entry_attributes_as_dict['uid'][0]] = {
                            k.lower():''
                            if not v
                            else
                            [x.lower() for x in v]
                            if len(v) > 1
                            else
                            v[0].lower()
                            for k,v in user.entry_attributes_as_dict.items()
                            if k not in ['uid','objectClass']}
                    d_user[user.entry_attributes_as_dict['uid'][0]].update(
                        {'dn':user.entry_dn})
                    d[self.sys_name].update(d_user)
        elif 'OU' in kwargs:
            with Connection(**self.d_sys) as ad:
                for ou in kwargs['OU']:
                    d_ou = dd(dict)
                    d_ou[ou]
                    for user in Reader(**{'connection':ad,
                                          'object_def':ObjectDef('inetOrgPerson',
                                                                 ad),
                                          'base':ou,
                                          }).search_paged(1000):
                        d_user = dict()
                        if args:
                            d_user[user.entry_attributes_as_dict['uid'][0]] = {
                                k.lower():''
                                if not v
                                else
                                [x.lower() for x in v]
                                if len(v) > 1
                                else
                                v[0].lower()
                                for k,v in user.entry_attributes_as_dict.items()
                                if k in args}
                        else:
                            d_user[user.entry_attributes_as_dict['uid'][0]] = {
                                k.lower():''
                                if not v
                                else
                                [x.lower() for x in v]
                                if len(v) > 1
                                else
                                v[0].lower()
                                for k,v in user.entry_attributes_as_dict.items()
                                if k not in ['uid','objectClass']}
                        d_user[user.entry_attributes_as_dict['uid'][0]].update({'dn':user.entry_dn})
                        d_ou[ou].update(d_user)
                    d[self.sys_name].update(d_ou)
        else:
            d[self.sys_name] = 'ValueSelectionError'
            
        return d

    def change_dn(self, lt):
        """
        Method to change the dn for a user
        lt = list of tuple like [(user, new_dn),
                                 (old_account, new_dn),()...]
        """
        d = dict()
        with Connection(**self.d_sys) as ad:
            for user in lt:
                ad.modify_dn(self.get_users(**{'USERS':'uid: %s'%user[0]}
                                            )[self.sys_name][user[0]]['dn'],
                             'uid = %s'%user[0],
                             new_superior = user[1])
                d.update({tuple(user):ad.result['message']})
        return {self.sys_name:d}

    def rename_user(self, lt):
        """
        Method to rename the user
        lt = list of tuple like [(old_account, new_account),
                                 (old_account, new_account),()...]
        """
        d = dict()
        with Connection(**self.d_sys) as ad:
            for user in lt:
                ad.modify_dn(self.get_users(**{'USERS':'uid: %s'%user[0]}
                                            )[self.sys_name][user[0]]['dn'],
                             'uid = %s'%user[1])
                d.update({tuple(user):ad.result['message']})
        return {self.sys_name:d}

    def delete_user(self,iterable):
        """
        Method to delete user
        l = list of user like  [user,user,user,...]
        """
        d = dict()
        with Connection(**self.d_sys) as ad:
            for user in iterable:
                ad.delete(self.get_users(**{'USERS':'uid: %s'%user}
                                            )[self.sys_name][user]['dn']
                          )
                d.update({user:ad.result['message']})
        return {self.sys_name:d}               

    def reset_pwd(self,iterable):
        """
        Method to reset user pwd
        iterable of  user  [user,user,user,...]
        """
        d = dict()
        with Connection(**self.d_sys) as ad:
            for user in iterable:
                # As to be replaced bt the Generate password form Libs.misc
                pwd = 'Aqwzsx01+'
                ad.extend.microsoft.modifyPassword.ad_modify_password(
                    self.get_users(**{'USERS':'uid: %s'%user}
                                   )[self.sys_name][user]['dn']
                    , new_password)
                d.update({user:ad.result['message']})
        return {self.sys_name:d}

    def unlock(self,iterable):
        """
        Method to unlock user
        iterable of  user  [user,user,user,...]
        """
        d = dict()
        with Connection(**self.d_sys) as ad:
            for user in iterable:
                ad.extend.microsoft.unlockAccount.ad_unlock_account(
                    self.get_users(**{'USERS':'uid: %s'%user}
                                   )[self.sys_name][user]['dn'])
                d.update({user:ad.result['message']})
        return {self.sys_name:d}

    def get_ou(self):
        """
        Retrieve Ldap domain in base
        """
        d = dd(set)
        d[self.sys_name]
        with Connection(**self.d_sys) as ad:
            for ou in Reader(**{'connection':ad,
                                'object_def':ObjectDef('organizationalUnit',
                                                       ad),
                                'base':self.base
                                }).search_paged(1000):
                d[self.sys_name].add(ou.entry_dn)
        return d
    
    # for testing matter no has to be implemanted
    def create_ou(self,ou):
        with Connection(**self.d_sys) as ad:
            ad.add('ou=%s,%s'%(ou,self.base),'organizationalUnit')
            return ad.result['message']


    # get all the attributes of inetorgperson
    def get_attributes(self):
        """
        Method for getting the attribute for inetorgperson
        return list of attribute
        """
        with Connection(**self.d_sys) as ad:
            return {self.sys_name : sorted([(attr.__dict__['name'],'')
                                            for attr in ObjectDef('inetorgperson', ad)
                                            if attr.__dict__['name'] != 'objectClass'])}

    def create_users(self,**kwargs):
        """
        Method for creating Users
        kwargs is like {user:attribue:valeur}
        """
        if not kwargs:
            return 'EntryValueError'
        d = dd(dict)
        d[self.sys_name]
        with Connection(**self.d_sys) as ad:
            w = Writer(**{'connection':ad,
                           'object_def':ObjectDef(['inetOrgPerson'], ad),
                          }
                       )
            for user in kwargs:
                inetorgperson = w.new(self.generate_dn_for_usr_creation(kwargs[user]))
                for attr in kwargs[user]:
                    inetorgperson[attr] = kwargs[user][attr]
                d[self.sys_name].update({user:entry_commit_changes()})
        return d

    def generate_dn_for_usr_creation(self,dict_):
        return 'uid=%s,%s'%(dict_['uid'],dict_['ou'])
        
        

                 
            
            
        
    
        
