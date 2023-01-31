from graphs.settings import *
from statistics import *

def get_graphs_info(port,address,petition):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import re
    
    url = (f"https://{address}/trace/{port}/{petition}/r")
    r = requests.get(url=url, params={}, auth=(ZBX_USER,ZBX_PWD), verify=False)
    
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
        graph_values.update({value[0]: [value[1],value[2]]})
    
    
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

    try:
        exp = float(list(graph_values.keys())[-1])
        if (exp / 1000) < 50:
            for key in graph_values:
                if i == 0 or i == 50 : 
                    value1.append(graph_values[key][0])
                    value2.append(graph_values[key][1])
                    keys.append(key)
                    i = 0
                i += 1
        else:
            for key in graph_values:
                ma_v1.append(float(graph_values[key][0]))
                ma_v2.append(float(graph_values[key][1]))
                if s == 10:
                    value1.append(mean(ma_v1))
                    value2.append(mean(ma_v2))
                    keys.append(key)

                    ma_v1 = []
                    ma_v2 = []
                    s = 0
                
                s += 1
                """ if i == 0 or i == 800 :
                        value1.append(graph_values[key][0])
                        value2.append(graph_values[key][1])
                        keys.append(key)
                        i = 0 """
        return port_info, value1, value2, keys
    except Exception as e:
        return None, None, None, None 





def parse_portinfo(info):
    trace_time = info[4]
    port_name = info[23]
    return info
