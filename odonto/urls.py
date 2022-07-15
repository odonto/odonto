"""
Urls for the Odonto project
"""
from django.conf.urls import url
from django.urls import path
from opal.urls import urlpatterns as opatterns
from odonto import views

urlpatterns = [
    path('view-fp17/<int:pk>/', views.ViewFP17DetailView.as_view(),
         name='odonto-view-fp17'),
    path('view-fp17-o/<int:pk>/', views.ViewFP17ODetailView.as_view(),
         name='odonto-view-fp17-o'),
    url('^unsubmitted-fp17s',
        views.UnsubmittedFP17s.as_view(),
        name='odonto-unsubmitted-fp17s'),
    url('^all-unsubmitted',
        views.AllUnsubmitted.as_view(),
        name='odonto-all-unsubmitted'),
    url('^open-fp17s',
        views.OpenFP17s.as_view(),
        name='odonto-open-fp17s'),
    path('stats/<int:year>/', views.Stats.as_view(), name="odonto-stats"),
    path(
        'patient-charges/<int:year>/<month>/',
        views.PatientCharges.as_view(),
        name="patient-charges"
    ),
    url('^case-mix-csv', views.CaseMix.as_view(), name="case-mix-csv"),
    path(
        'delete-episode/<int:patient_pk>/<int:episode_pk>/',
        views.DeleteEpisode.as_view(),
        name="delete-episode"
    ),
]

urlpatterns += opatterns
