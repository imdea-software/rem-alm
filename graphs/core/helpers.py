from graphs.settings import *
from statistics import *

def get_graphs_info(port,address,petition):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import re
    
    url = (f"https://{address}/trace/{port}/{petition}/f")
    r = requests.get(url=url, params={}, auth=(ZBX_USER,ZBX_PWD), verify=False)
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

        # mirar a ver si hay 4 valores por index coger solo los dos ultimos

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
            portname = port_info[23]
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
    events = []
    port_info = []
    link_loss = ''
    desviation = ''
    faultloss = ''
    for data in info:
        if data.split('):')[0] == 'Trace Time FA (UTC':
            port_info.append(data.split('):')[1])
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
                port_info.append(data)
            faultloss = float(data.split(':')[1])
            """ print(type(faultloss), type(link_loss))
            desviation = round(float(link_loss) - float(faultloss),3)
            print(type(faultloss), type(link_loss))
            port_info.append(f"Desviation: {desviation}(dB)") """

    return port_info


def parse_fingerprint(info):
    fingerprint_data = []
    for data in info:
        if data.split('):')[0] == 'Trace Time FP (UTC':
            fingerprint_data.append(data.split('):')[1])
        if data.split(':')[0] == 'Link Length':
            fingerprint_data.append(data)
        if data.split(':')[0] == 'Link Loss': 
           fingerprint_data.append(data)
        if data.split(':')[0] == 'Fault Loss':
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




""" sep=  
Type: FA 
Trace Count: 2 
Trace Time FP (UTC): 2020-01-29 16:07:12 
Trace Time FA (UTC): 2021-10-29 05:36:32 
 
Device Info: 14 
Release Number:               3.3.1 
Shelf Unit Name:              64ALM/#1650D/AC 
Shelf Name:                   CIEMAT-AL-AD-04 
Inventory Type:               64ALM-1650D 
CLEI Code:                    WOMSJ00BRA 
Vendor ID:                    ADVA 
Universal Serial Identifier:  LBADVA72183500308 
Serial Number:                FA72183500308 
Part Number:                  1043709846-01 
FPGA Revision:                6.03.01 
Firmware Revision:            2.56 
Hardware Revision:            1.01 
Software Revision:            30301_201912051528 
Measurement Wavelength:       1650 
 
Link: 10 
Port Name:        "UCM F1" 
Link Length:      1014.8 
External Offset:  5 
Link Loss:        1.13 
Fault Loss:       0.67 
Coupler Loss:     0.70 
Max Laser Power:  16.96 
Link Latency:     5.0 
Fault Position:     -1 
Remark:           "" 
 
Events: 4 
FP_EVENT_1: 0.0 >-53.8 2.2 "" 
FP_EVENT_2: 1014.8 0.0 term "" 
FA_EVENT_1: 0.0 >-53.7 1.7 
FA_EVENT_2: 998.4 0.0 term 
 
Trace Settings: 12 
Trace Name:         FP_1 FA_1 
pulsewidth:         300 300 
average:            16384 16384 
sampling mode:      160 160 
port:               5 5 
start:              0.0 0.0 
end:                3897.4 3897.4 
length:             19999.5 19999.5 
offset:             434.3 434.3 
refractive index:   1.468900 1.468900 
board temperature:  43.2 45.8 
norm value:         657767509.476562 646414647.004390 
 
Trace Data: 2388 

        #añadir Link Length
        
        #parse en dos tablas fault analysis & finger print
Loss Fast Deviation High CLEAR	Deviation: 0.8 dB - Threshold: 1.0 dB
            Timestamp:	2022-08-26 19:04:46
            Link Loss [dB]:	23.7
            Mean Fast/Medium/Slow [dB]:	22.9/23.8/23.5
            Fault Position [m]: """

        # add Fault Loss:       21.55 
        # add Fault Position:     -1  (si es negativo poner: 'No aplica')
        #desviation : link loss - fault loss
        

 