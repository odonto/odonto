"""
Urls for the Odonto project
"""
from django.conf.urls import include, url

from opal.urls import urlpatterns as opatterns

from django.contrib import admin
admin.autodiscover()

from odonto import views

urlpatterns = [
    url(r'^episode/for/new/fp17/(?P<pk>\d+)?',
        views.CreateNewEpidsodeForFP17View.as_view(),
        name='episode_for_fp17'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += opatterns
