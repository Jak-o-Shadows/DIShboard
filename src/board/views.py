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

def _apply_pdu_filters(request, queryset):
    """Helper to apply filters from request.GET to a PduHub queryset."""
    # Logic to filter PduHub by request.GET params
    return queryset

# @PDU Filter Update, IMPL_FILTER_PROTOCOL, code_impl, [SPEC_FILTER_PROTOCOL]
@hx_or_full(template_name='base.html')
def dis_filter_update(request):
    return render_to_string('forms/pdu_filter.html', {
        'form_pdu_filter': PduFilterForm(request.GET),
        'filter_action_url': request.path,
        'selected_pdus': request.GET.getlist('pdu_type'),
        'all_pdu_types': _get_all_pdu_types(),
    })

# @PDU Filter Add, IMPL_FILTER_PROTOCOL, code_impl, [SPEC_FILTER_PROTOCOL]
@hx_or_full(template_name='base.html')
def dis_filter_add_pdu(request):
    # This logic would ideally update the URL via a redirect or HTMX swap
    # Keeping session logic for now to ensure minimal breaking changes
    pdu = request.GET.get('pdu_search')
    selected = request.GET.getlist('pdu_type')
    if pdu and pdu not in selected:
        selected.append(pdu)
    return render_to_string('forms/pdu_filter.html', {
        'form_pdu_filter': PduFilterForm(request.GET),
        'filter_action_url': request.path,
        'selected_pdus': selected,
        'all_pdu_types': _get_all_pdu_types(),
    })

# @PDU Filter Remove, IMPL_FILTER_PROTOCOL, code_impl, [SPEC_FILTER_PROTOCOL]
@hx_or_full(template_name='base.html')
def dis_filter_remove_pdu(request):
    pdu_name = request.GET.get('pdu_name')
    selected = request.GET.getlist('pdu_type')
    if pdu_name in selected:
        selected.remove(pdu_name)
    return render_to_string('forms/pdu_filter.html', {
        'form_pdu_filter': PduFilterForm(request.GET),
        'filter_action_url': request.path,
        'selected_pdus': selected,
        'all_pdu_types': _get_all_pdu_types(),
    })

def _get_selected_pdus(request):
    return request.session.get('selected_pdus', [])

def _get_all_pdu_types():
    return pdu_models.PDU_TYPES


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


