from django.shortcuts import redirect, render
from .models import EntityStatePDU
from .tasks import listen_for_dis_packets
from django.middleware.csrf import get_token

def dashboard(request):
    """Main dashboard entry point."""
    return render(request, 'dashboard.html', {'started': False,
                                              "csrf_token": get_token(request) })

def start_ingestion(request):
    if request.method == 'POST':
        listen_for_dis_packets.enqueue()
        return render(request, 'ingestion_control.html', {'started': True})
    return redirect('dashboard')

def pdu_list(request):
    """HTMX endpoint to return the latest 20 PDUs."""
    pdus = EntityStatePDU.objects.all().order_by('-timestamp')[:20]
    template = 'pdu_list.html'
    if not request.htmx:
        template = 'dashboard.html'
    return render(request, template, {'pdus': pdus})