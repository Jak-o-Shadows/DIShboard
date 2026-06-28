from django.shortcuts import get_object_or_404, redirect, render
from .models import PduHub, IngestionState
from .tasks import listen_for_dis_packets, send_test_pdus
from .forms import PlaybackSenderForm, ConnectionSettingsForm
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import functools

def _ingestion_task_is_running():
    return IngestionState.objects.filter(running=True).exists()

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

@hx_or_full(template_name='base.html')
def dashboard(request):
    """Main dashboard entry point."""
    # Fetch from the hub
    pdus = PduHub.objects.all().order_by('-timestamp')[:20]
    form = ConnectionSettingsForm()
    return render_to_string('partial_dis_live.html', {
        'started': False,
        'csrf_token': get_token(request),
        'form': form,
        'pdus': pdus,
        'pdu_count': PduHub.objects.count(),
    })

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

# @Connection information page, IMPL_CONNECTION_INFORMATION, code_impl, [SPEC_CONNECTION_INFORMATION]
@hx_or_full(template_name='base.html')
def connection_info(request):
    connected = _ingestion_task_is_running()

    recent_period_s = 5
    recent_window = timezone.now() - timedelta(seconds=recent_period_s)
    # Query the hub for rate
    recent_count = PduHub.objects.filter(timestamp__gte=recent_window).count()
    pdu_rate = recent_count / recent_period_s

    return render_to_string('partial_connection_info.html', {
        'connected': connected,
        'pdu_rate': pdu_rate,
    })

