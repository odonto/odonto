"""
Context processors for Odonto
"""
from opal.models import Episode


def odonto_roles(request):
    default = {
        'roles': {
            'is_dentist': False,
            'is_admin'  : False
        }
    }

    if not request.user.is_authenticated:
        return default

    default['roles']['is_admin'] = True

    if request.user.performernumber_set.count() > 0:
        default['roles']['is_dentist'] = True

    return default
