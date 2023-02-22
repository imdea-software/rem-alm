from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pysnmp.hlapi import *
from .helpers import *
import os
from graphs import settings
import logging


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
def dashboard(request):
    return render(request,'dashboard.html')


@login_required
def ajax_alm_graph(request):
    if request.method == 'POST':
        data = {}
        port = request.POST.get('port')
        address = request.POST.get('address')
        typeof = request.POST.get('type')
        print('typeof', typeof)
        # fa = manual ; af = automatico
        if typeof == 'man':
            print('here ', port, address, typeof)
            try:
                snmp_manual_petition(port,address,typeof)
                data = {'message': 'Se ha ejecutado su peticion, porfavor espere unos minutos antes de solicitar ver el analisis manual.'}
                return JsonResponse(data,status=200)
            except Exception as e:
                logger.info(f"There was an error while asking for a new manual fault analysis . Error: {e}")
        else:
            try:
                print('here 2')
                value1, value2, keys, faultanalysis, fingerprint, fp_event, fa_event, portname = get_graphs_info(port,address,typeof)
                ##parsear hora para que devuelva la actual
                print('here 3')
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
    


def snmp_manual_petition(port, address, typeof):
    from . import quicksnmp
    from pysnmp import hlapi
    
    # Set up SNMP parameters
    snmp_version = 1
    snmp_community = 'RTCM'
    snmp_ip = address
    snmp_oid = (f"1.3.6.1.4.1.2544.1.14.6.1.1.1.{port}.4")
    snmp_value = 'new_value'

    # Perform SNMP SET request
    print(type(snmp_version), type(snmp_community), snmp_oid)
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(setCmd(SnmpEngine(), CommunityData(snmp_community, mpModel=snmp_version),UdpTransportTarget((snmp_ip, 161)),ContextData(),ObjectType(ObjectIdentity(snmp_oid))))
        if errorIndication:
            print(f"SNMP SET request failed: {errorIndication}")
        else:
            for varBind in varBinds:
                print(f"{varBind.prettyPrint()}")
    except Exception as e:
        print('This is the exception: ',e)
        pass
    # Print the result
    
