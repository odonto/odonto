"""
Urls for the Odonto project
"""
from django.conf.urls import include, url
from django.urls import path
from opal.urls import urlpatterns as opatterns

from odonto import views

urlpatterns = [
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='odonto-patient-detail'),
    url('^unsubmitted-fp17s',
        views.UnsubmittedFP17s.as_view(),
        name='unsubmitted-fp17s'),
]

urlpatterns += opatterns
