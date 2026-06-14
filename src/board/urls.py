from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dis-live/', views.dashboard, name='dis_live'),
    path('index/', views.dashboard, name='dashboard'),
    path('connection-info/', views.connection_info, name='connection_info'),
    path('pdus/', views.pdu_list, name='pdu_list'),
    path('start-ingestion/', views.start_ingestion, name='start_ingestion'),
    path('pdus/<int:pk>/', views.pdu_detail, name='pdu_detail'),
    path('playback-selection/', views.playback_selection, name='playback_selection'),
    path('playback-selection/start-sender/', views.start_pdu_sender, name='start_pdu_sender'),
]