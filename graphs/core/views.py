from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .helpers import *

# Create your views here.
@login_required
def dashboard(request):
    return render(request,'dashboard.html')


@login_required
def ajax_alm_graph(request):
    if request.method == 'POST':
        data = {}
        port = request.POST.get('port')
        address = request.POST.get('address')
        typeof = request.POST.get('type')
        port_info, value1, value2, keys = get_graphs_info(port,address,typeof)
            ##parsear hora para que devuelva la actual
        data = {
            'keys':keys,
            'value1': value1,
            'value2' : value2,
            'port_info' : port_info,
            }
        return JsonResponse(data,status=200)
    