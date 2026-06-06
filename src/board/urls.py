from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pdus/', views.pdu_list, name='pdu_list'),
    path('start-ingestion/', views.start_ingestion, name='start_ingestion'),
]