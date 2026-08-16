import datetime
import functools

from django.shortcuts import get_object_or_404, redirect, render
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone

from .models import PduHub, IngestionState
from .tasks import listen_for_dis_packets, send_test_pdus
from . import pdu_models
from .forms import PlaybackSenderForm, ConnectionSettingsForm, PduFilterForm

################ Utility Functions ################

def hx_or_full(template_name="base.html"):
    """Decorator for view functions that return an HTML fragment.
    If the request contains the HTMX header "HX-Target", return the fragment as-is.
    Otherwise render the fragment into `template_name` under `context_key` so a
    full page is produced.
    """
    def decorater(view_func):
        @functools.wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # Check for HTMX header
            is_hx = request.headers.get("HX-Request", None) is not None
            print(f"URL: {request.path} | HTMX request: {is_hx}")
            fragment_html = view_func(request, *args, **kwargs)
            if is_hx:
                content = fragment_html
            else:
                content = render_to_string(template_name, {
                    'content': fragment_html,
                    'csrf_token': get_token(request),
                })
            return HttpResponse(content)
        return _wrapped
    return decorater

################ Main DIS-Live page ################

@hx_or_full(template_name='base.html')
def dashboard(request):
    """Main dashboard entry point."""
    # Fetch from the hub
    pdus = PduHub.objects.all().order_by('-timestamp')[:20]
    pdus = _apply_pdu_filters(request, pdus)

    form_conn_settings = ConnectionSettingsForm()
    # Use request.GET for filters so the URL stays in sync
    form_pdu_filter = PduFilterForm(request.GET)
    
    # Check if there are active fieldsets in URL and pre-hydrate them
    active_fieldsets_html = ""
    fieldset_slugs = request.GET.getlist('filter_type_select', '')
    for fieldset_slug in fieldset_slugs:
        print(f"Hydrating fieldset for slug: {fieldset_slug}")
        # TODO: Consolidate the fieldset slugs with the other definitions of it
        if fieldset_slug and fieldset_slug in ['protocol', 'temporal', 'tactical', 'entity', 'raw_sql']:
            # Re-hydrate the fieldset on page load
            field_options = _get_filter_field_options(fieldset_slug)
            active_fieldsets_html += render_to_string('forms/pdu_filter_fieldset_partial.html', {
                'fieldset_slug': fieldset_slug,
                'field_options': field_options,
                'form_pdu_filter': form_pdu_filter,
                'all_pdu_types': _get_all_pdu_types(),
                'selected_pdus': request.GET.getlist('pdu_type'),
            })
    
    return render_to_string('partial_dis_live.html', {
        'started': False,
        'csrf_token': get_token(request),
        'form_conn_settings': form_conn_settings,
        'form_pdu_filter': form_pdu_filter,
        'filter_action_url': request.path,
        'all_pdu_types': _get_all_pdu_types(),
        'selected_pdus': request.GET.getlist('pdu_type'),
        'pdus': pdus,
        'pdu_count': PduHub.objects.count(),
        'active_fieldsets_html': active_fieldsets_html,
    })

# @HTMX PDU list refresh endpoint, IMPL_HTMX_MESSAGE_LIST, code_impl, [SPEC_HTMX_INTERACTIONS, SPEC_MESSAGES_PAGE]
@hx_or_full(template_name='base.html')
def pdu_list(request):
    """HTMX endpoint to return the latest 20 PDUs from the Hub."""
    pdus = PduHub.objects.all().order_by('-timestamp')[:20]
    return render_to_string("pdus/partial_list.html", {
        'pdus': pdus,
        'pdu_count': PduHub.objects.count(),
    })

# @PDU detail view, IMPL_PDU_DETAIL_VIEW, code_impl, [SPEC_MESSAGES_PAGE]
@hx_or_full(template_name='base.html')
def pdu_detail(request, pk):
    hub_pdu = get_object_or_404(PduHub, pk=pk)
    # GenericForeignKey makes this easy:
    pdu = hub_pdu.content_object
    return render_to_string('pdus/partial_detail.html', {
        'pdu': pdu,
    })

################ DIS Filter ################
# @PDU Filter Add, IMPL_FILTER_PROTOCOL, code_impl, [SPEC_FILTER_PROTOCOL]

def _apply_pdu_filters(request, queryset):
    """Helper to apply filters from request.GET to a PduHub queryset."""
    # Logic to filter PduHub by request.GET params
    return queryset

def _get_all_pdu_types():
    return pdu_models.PDU_TYPES


def _get_filter_field_options(fieldset_slug):
    options = {
        'protocol': [
            {'value': 'pdu_type', 'label': 'PDU Type', 'kind': 'text'},
        ],
        'temporal': [
            {'value': 'start_time', 'label': 'Start Time', 'kind': 'datetime'},
            {'value': 'end_time', 'label': 'End Time', 'kind': 'datetime'},
        ],
        'tactical': [
            {'value': 'force_id', 'label': 'Force ID', 'kind': 'number'},
            {'value': 'site_id', 'label': 'Site ID', 'kind': 'number'},
            {'value': 'application_id', 'label': 'Application ID', 'kind': 'number'},
            {'value': 'exercise_id', 'label': 'Exercise ID', 'kind': 'number'},
        ],
        'entity': [
            {'value': 'entity_id', 'label': 'Entity ID', 'kind': 'number'},
            {'value': 'entity_kind', 'label': 'Entity Kind', 'kind': 'text'},
            {'value': 'entity_domain', 'label': 'Entity Domain', 'kind': 'text'},
            {'value': 'entity_category', 'label': 'Entity Category', 'kind': 'text'},
        ],
        'raw_sql': [
            {'value': 'raw_sql', 'label': 'Raw SQL', 'kind': 'text'},
            {'value': 'show_malformed', 'label': 'Show Malformed', 'kind': 'boolean'},
        ],
    }
    return options.get(fieldset_slug, [])


@hx_or_full(template_name='base.html')
def dis_filter_add_fieldset(request):
    """Render a fieldset for the selected filter type."""
    fieldset_slug = request.GET.get('filter_type_select', '')
    if not fieldset_slug or fieldset_slug not in ['protocol', 'temporal', 'tactical', 'entity', 'raw_sql']:
        return HttpResponse('')

    field_options = _get_filter_field_options(fieldset_slug)
    if not field_options:
        return ""  # TODO: log a problem here, as we've got a weird fieldset.  # TODO: Check that this doesn't break things

    context = {
        'fieldset_slug': fieldset_slug,
        'field_options': field_options,
        'form_pdu_filter': PduFilterForm(),
        'all_pdu_types': _get_all_pdu_types(),
        'selected_pdus': request.GET.getlist('pdu_type'),
    }
    return render_to_string('forms/pdu_filter_fieldset_partial.html', context)

################ DIS Live Ingestion ################

def _ingestion_task_is_running():
    return IngestionState.objects.filter(running=True).exists()

# @Ingestion control API, IMPL_INGESTION_CONTROL_API, code_impl, [SPEC_TASK_CONTROL_API, SPEC_CONNECTION_INFORMATION]
def start_ingestion(request):
    if request.method == 'POST':
        form = ConnectionSettingsForm(request.POST)
        if form.is_valid():
            listen_host = form.cleaned_data['listen_host']
            listen_port = form.cleaned_data['listen_port']
            listen_for_dis_packets.enqueue(listen_host=listen_host, port=listen_port)
            ingestion_state, _ = IngestionState.objects.get_or_create(defaults={
                'listen_host': listen_host,
                'listen_port': listen_port,
                'running': True,
            })
            ingestion_state.listen_host = listen_host
            ingestion_state.listen_port = listen_port
            ingestion_state.running = True
            ingestion_state.save()

            return render(request, 'ingestion_control.html', {
                'started': True,
                'listen_host': listen_host,
                'listen_port': listen_port,
            })
        return render(request, 'ingestion_control.html', {
            'started': False,
            'form': form,
        })
    return redirect('dashboard')

# @Connection information page, IMPL_CONNECTION_INFORMATION, code_impl, [SPEC_CONNECTION_INFORMATION]
@hx_or_full(template_name='base.html')
def connection_info(request):
    connected = _ingestion_task_is_running()

    recent_period_s = 5
    recent_window = timezone.now() - datetime.timedelta(seconds=recent_period_s)
    # Query the hub for rate
    recent_count = PduHub.objects.filter(timestamp__gte=recent_window).count()
    pdu_rate = recent_count / recent_period_s

    return render_to_string('partial_connection_info.html', {
        'connected': connected,
        'pdu_rate': pdu_rate,
    })

################ DIS Playback ################

# @Playback selection page, IMPL_PLAYBACK_SELECTION_PAGE, code_impl, [SPEC_PLAYBACK_SELECTION_VIEW]
@hx_or_full(template_name='base.html')
def playback_selection(request):
    form = PlaybackSenderForm()
    return render_to_string('partial_playback_selection.html', {
        'form': form,
        'message': None,
    })

# @Playback sender task trigger, IMPL_PLAYBACK_SENDER_TRIGGER, code_impl, [SPEC_PLAYBACK_SELECTION_VIEW]
@hx_or_full(template_name='base.html')
def start_pdu_sender(request):
    if request.method != 'POST':
        return redirect('playback_selection')

    form = PlaybackSenderForm(request.POST)
    if not form.is_valid():
        return render_to_string('partial_playback_selection.html', {
            'form': form,
            'message': 'Please fix the errors below.',
        })

    duration_seconds = form.cleaned_data['duration_seconds']
    destination_host = form.cleaned_data['destination_host']
    destination_port = form.cleaned_data['destination_port']

    send_test_pdus.enqueue(
        duration_seconds=duration_seconds,
        destination_host=destination_host,
        destination_port=destination_port,
    )
    return render_to_string('partial_playback_selection.html', {
        'form': PlaybackSenderForm(initial=form.cleaned_data),
        'message': f'PDU playback task enqueued for {duration_seconds} seconds to {destination_host}:{destination_port}. Ensure db_worker is running.',
    })

