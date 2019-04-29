"""
Urls for the Odonto project
"""
from django.conf.urls import include, url

from opal.urls import urlpatterns as opatterns

from odonto import views

urlpatterns = [
    url('^unsubmitted-fp17s',
        views.UnsubmittedFP17s.as_view(),
        name='unsubmitted-fp17s'),
]

urlpatterns += opatterns
