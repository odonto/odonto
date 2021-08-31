"""
Context processors for Odonto
"""
from opal.models import Episode
from odonto import episode_categories


def odonto_roles(request):
    default = {
        'roles': {
            'is_dentist': False,
            'is_admin'  : False,
            'can_see_covid': False
        }
    }

    if not request.user.is_authenticated:
        return default

    default['roles']['is_admin'] = True

    if request.user.performernumber_set.count() > 0:
        default['roles']['is_dentist'] = True

    for user_role in request.user.profile.roles.all():
        default['roles'][user_role.name] = True

    return default


def all_unsubmitted_count():
    qs = Episode.objects.all()
    return episode_categories.get_unsubmitted_compass_episodes(qs).count()


def episode_counts(request):
    if not request.user.is_authenticated:
        return {}
    episodes = Episode.objects.filter(stage="Open")
    for_user = episode_categories.get_episodes_for_user(
        episodes, request.user
    )
    unsubmitted = episode_categories.get_unsubmitted_compass_episodes(
        for_user
    )
    open_episodes = for_user.exclude(
        id__in=unsubmitted.values_list("id", flat=True)
    )

    return {
        "episode_counts": {
            "open": open_episodes.count(),
            "unsubmitted": unsubmitted.count(),
            # we return the method so its lazily evaluated if the user
            # has the right permissions
            "all_unsubmitted": all_unsubmitted_count
        }
    }
