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

    # PDU Filter
    #path('dis-filter-add-fieldset/', views.dis_filter_add_fieldset, name="dis_filter_add_fieldset"),
    # In order to support :need:`SPEC_FILTER_DIS_UI_BOOLEAN_OPTIONS`, along with :need:`SPEC_FILTER_DIS_URL_SCHEMA`, and the rest, need endpoints
    # @HTMX DIS Filter HTMX Endpoints, IMPL_FILTER_DIS_HTMX_ENDPOINTS, code_impl, [SPEC_FILTER_DIS_HTMX_ENDPOINTS]
    #path('filter/add_group/', views.dis_filter_add_group, name='dis_filter_add_group'),
    #path('filter/add_condition/', views.dis_filter_add_condition, name='dis_filter_add_condition'),
    #path('filter/edit_node/', views.dis_filter_edit_node, name='dis_filter_edit_node'),
    #path('filter/remove_node/', views.dis_filter_remove_node, name='dis_filter_remove_node'),
    #path('filter/reorder_children/', views.dis_filter_reorder_children, name='dis_filter_reorder_children'),
]