from graphs.settings import *
from statistics import *
from graphs import settings
import os
import logging


# Set up logging system
LOG_FILENAME = os.path.join(settings.LOG_FILE_LOCATION,'remalm_info.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILENAME)
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_graphs_info(port,address,petition):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import re 

    url = (f"https://{address}/trace/{port}/{petition}/f")
    try:        
        r = requests.get(url=url, params={}, auth=(ZBX_USER,ZBX_PWD), verify=False)
    except Exception as e:
        logger.info(f"There was an error when trying to connect to the ALM API. Error: {e}")
    if not r.text == 'Not Found':
        soup = bs(r.text, "lxml")
        text = soup.p.text.replace('\n',',')
        text = text.replace('\t',' ')
        text = text.replace('\r',' ')
        text = text.split(',')
        pattern = '^([-+]?\d[-+]? ?)+'
        values = []
        graph_values = {}
        discard_values = {}
        port_info = []
        for value in text:
            result = re.match(pattern,value)
            if result:
                value = value.strip()
                value = value.replace(' ',(','))
                values.append(value)
            else:
                port_info.append(value)
        for value in values:
            value = value.split(',')
            if len(value) == 3:
                graph_values.update({value[0]: [value[1],value[2]]})
            if len(value) == 5:
                graph_values.update({value[0]: [value[3],value[4]]})
        
        
        for graph in graph_values:
            if not graph == '-0.00':
                discard_values.update({graph:graph_values[graph]})
            else:
                break
        for value in discard_values:
            graph_values.pop(value)

        value1 = []
        value2 = []
        keys = []
        i = 0
        ma_v1 = []
        ma_v2 =[]
        s = 0
        if not port_info[0] == 'Not Found':
            faultanalysis = parse_faultanalysis(port_info)
            fingerprint = parse_fingerprint(port_info)
            fp_event, fa_event = parse_events(port_info)
            pn = port_info[23].split(":")[1].strip(" ")
            pns = pn.strip('"')
            portname = (f"Puerto: {pns}")
        else:
            faultanalysis, fingerprint, fp_event, fa_event,  portname = False

        exp = float(list(graph_values.keys())[-1])
        if (exp / 1000) < 50:
            for key in graph_values:
                value1.append(graph_values[key][0])
                value2.append(graph_values[key][1])
                km = (float(key)/1000)                
                keys.append(round(km,2))
        else:
            for key in graph_values:
                ma_v1.append(round(float(graph_values[key][0]),4))
                ma_v2.append(round(float(graph_values[key][1]),4))
                if s == 50:
                    value1.append(round(mean(ma_v1),4))
                    value2.append(round(mean(ma_v2),4))
                    km = (float(key)/1000)
                    keys.append(round(km,2))

                    ma_v1 = []
                    ma_v2 = []
                    s = 0                
                s += 1 
        
        return value1, value2, keys, faultanalysis,fingerprint, fp_event, fa_event, portname
    else:
        
        return None, None, None, faultanalysis, fingerprint, fp_event, fa_event

def parse_faultanalysis(info):
    from datetime import datetime, timedelta
    
    events = []
    port_info = []
    link_loss = ''
    desviation = ''
    faultloss = ''
    for data in info:
        if data.split('):')[0] == 'Trace Time FA (UTC':
            d = datetime.strptime(data.split('):')[1].strip(" "), "%Y-%m-%d %H:%M:%S")
            print(d, type(d))
            d1 = d + timedelta(hours=1)
            print(d1, type(d1))
            date = d1.strftime("%H:%M %d-%m-%Y")
            port_info.append(date)
        if data.split(':')[0] == 'Coupler Loss':
            link_loss = float(data.split(':')[1])
        if data.split(':')[0] == 'Fault Position':
            if data.split(':')[1] == "     -1 ":
                port_info.append("Fault Position: No aplica")
            else:
                port_info.append(data) 
        if data.split(':')[0] == 'Fault Loss':
            fl = float(data.split(':')[1].replace(" ",""))
            if fl > 40: 
                port_info.append("Fault Loss: broken")
                desviation = "No aplica"
                port_info.append(f"Desviation: {desviation}")
            else:
                port_info.append(f"Desviation: {fl}")
            faultloss = float(data.split(':')[1])

    return port_info


def parse_fingerprint(info):
    from datetime import datetime, timedelta

    fingerprint_data = []
    for data in info:
        if data.split('):')[0] == 'Trace Time FP (UTC':
            d = datetime.strptime(data.split('):')[1].strip(" "), "%Y-%m-%d %H:%M:%S")
            d1 = d + timedelta(hours=1)
            date = d1.strftime("%H:%M %d-%m-%Y")
            fingerprint_data.append(date)
        if data.split(':')[0] == 'Link Length':
            fingerprint_data.append(data)
        if data.split(':')[0] == 'Link Loss': 
           fingerprint_data.append(data)
    return fingerprint_data

def parse_events(info):
    fp_event = []
    fa_event = []
    for data in info:
        if data.split(':')[0].startswith('FP_EVENT'):
            h = []
            for x in data.split(':')[1].split( ):
                if x == '""':
                    pass
                else:
                    h.append(x)
            fp_event.append(h)
        if data.split(':')[0].startswith('FA_EVENT'):
            h = []
            for x in data.split(':')[1].split( ):
                if x == '""':
                    pass
                else:
                    h.append(x)
            fa_event.append(h)
    return fp_event, fa_event


        

 