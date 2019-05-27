"""
Urls for the Odonto project
"""
from django.conf.urls import include, url
from django.urls import path
from opal.urls import urlpatterns as opatterns

from odonto import views

urlpatterns = [
    path('patient/<int:pk>/', views.PatientDetailView.as_view(),
         name='odonto-patient-detail'),

    path('submit-fp17/<int:pk>/', views.SubmitFP17DetailView.as_view(),
         name='odonto-submit-fp17'),
    path('view-fp17/<int:pk>/', views.ViewFP17DetailView.as_view(),
         name='odonto-view-fp17'),

    path('submit-fp17-o/<int:pk>/', views.SubmitFP17ODetailView.as_view(),
         name='odonto-submit-fp17-o'),
    path('view-fp17-o/<int:pk>/', views.ViewFP17ODetailView.as_view(),
         name='odonto-view-fp17-o'),


    url('^unsubmitted-fp17s',
        views.UnsubmittedFP17s.as_view(),
        name='odonto-unsubmitted-fp17s'),

    url('^open-fp17s',
        views.OpenFP17s.as_view(),
        name='odonto-open-fp17s'),


]

urlpatterns += opatterns
