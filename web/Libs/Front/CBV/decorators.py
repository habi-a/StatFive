'''
from django.core.exceptions import PermissionDenied
from Basis.models import Group
from Basis.models import User_Group
from Basis.models import Group_Views
'''


def user_is_authorized(function):
    def wrap(request, *args, **kwargs):
        if User_Group.objects.filter(group__in=Group_Views.objects.filter(view=request.path
                                                                          ).values_list('group',
                                                                                        flat = True),
                                     user = request.user).values_list('user',flat = True) or\
            request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def workflow(fonction):
    return fonction
