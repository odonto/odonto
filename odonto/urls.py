"""
Urls for the Odonto project
"""
from django.conf.urls import url
from opal.urls import urlpatterns as opatterns

from odonto import views

urlpatterns = [
    url('^unsubmitted-fp17s',
        views.UnsubmittedFP17s.as_view(),
        name='odonto-unsubmitted-fp17s'),
    url('^open-fp17s',
        views.OpenFP17s.as_view(),
        name='odonto-open-fp17s'),
    url('^stats', views.Stats.as_view(), name="odonto-stats"),
    url('^case-mix-csv', views.CaseMix.as_view(), name="case-mix-csv"),
]

urlpatterns += opatterns
