from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pysnmp.hlapi import *
from .helpers import *
import os
from graphs import settings
import logging
from .decorators import *

# Set up logging system
LOG_FILENAME = os.path.join(settings.LOG_FILE_LOCATION,'remalm_info.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILENAME)
handler.setFormatter(formatter)
logger.addHandler(handler)


# Create your views here.
@login_required
@verify_user_profile
def dashboard(request):
    member = request.user.profile
    devices = member.get_view()
    data = {
        'devices': devices[0],
        'fa' : devices[1],
        'vista': member.view
    }

    return render(request,'dashboard.html', data)


@login_required
@verify_user_profile
def ajax_alm_graph(request):
    # receive data from the view and send it to the server in order to the the graphs information 
    # and also the manaual fault analysis if requested
    if request.method == 'POST':
        data = {}
        port = request.POST.get('port')
        address = request.POST.get('address')
        typeof = request.POST.get('type')
        # fa = manual ; af = automatico
        if typeof == 'man':
            try:
                message = snmp_manual_petition(port,address,typeof)
                data = {'message': message}
                return JsonResponse(data,status=200)
            except Exception as e:
                logger.info(f"There was an error while asking for a new manual fault analysis . Error: {e}")
                message = 'Ha habido un error cuando se pedia un nuevo Fault Analysis, porfavor contacte con el administrador.'
                data = {'message': message}
                return JsonResponse(data,status=200)
        else:
            
            try:
                value1, value2, keys, faultanalysis, fingerprint, fp_event, fa_event, portname = get_graphs_info(port,address,typeof)
                ##parsear hora para que devuelva la actual
                data = {
                    'keys':keys,
                    'value1': value1,
                    'value2' : value2,
                    'faultanalysis' : faultanalysis,
                    'fingerprint': fingerprint,
                    'fp_event' : fp_event,
                    'fa_event' : fa_event,
                    'portname':portname,
                    'message': False,
                    }
                return JsonResponse(data,status=200)
            except Exception as e:
                logger.info(f"There was an error while perfoming graph's info query. Error: {e}")
    



    
