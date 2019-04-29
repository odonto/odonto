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
    if not request.user:
        return default

    if not request.user.is_authenticated:
        return default

    default['roles']['is_admin'] = True

    if request.user.performernumber_set.count() > 0:
        default['roles']['is_dentist'] = True

    return default


def stats(request):
    stats = {
    }
    if request.user.is_authenticated:
        if request.user.performernumber_set.count() > 0:
            name = request.user.get_full_name()
            stats['my_unsubmitted_fp17s'] = Episode.objects.filter(
                stage='Open',
                fp17dentalcareprovider__performer=name,
                fp17incompletetreatment__completion_or_last_visit__isnull=False
            ).count()


    return {'stats': stats}
