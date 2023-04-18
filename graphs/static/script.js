$(document).ready(function(){

  var port_data = {
      "172.20.237.90":[
          {"1" : "CIEMAT-URJC-IMDEA NETWORK - F1 - (1)"},
          {"2" : "CIEMAT-URJC-IMDEA NETWORK - F2 - (2)"},
          {"3" : "Imdea Software F1 - (3)"},
          {"4" : "Imdea Software F2 - (4)"},
          {"5" : "UCM F1 - (5)"},
          {"6" : "UCM F2 - (6)"},
          {"7" : "CIB F1 - (7)"},
          {"8" : "CIB F2 - (8)"},
          {"9" : "UNED F1 - (9)"},
          {"10" : "UNED F2 - (10)"},
          {"11" : "Casa Velázquez F1 - (11)"},
          {"12" : "Casa Velázquez F2 - (12)"},
          {"13" : "UPM F1 - (13)"},
          {"14" : "UPM F2 - (14)"},
          {"15" : "UAM F1 - (15)"},
          {"16" : "UAM F2 - (16)"}
                     
  ],
      "172.20.237.86":[
          {"1" : "CSIC-UC3M-2017-06-F/UC3M-IMDEANET-2017-05-F1 (1)"},
          {"2" : "CSIC - UC3M - IMDEA NETWORK - F2 (2)"},
          {"3" : "CSICJO F1 - (3)"},
          {"4" : "CSICJO F2 - (4)"},
          {"5" : "UCM F1 - (5)"},
          {"6" : "UCM F2 - (6)"}
  ]  
  }

    var vista_telefonica = {
              "172.20.237.90":[
                  {"1" : "CIEMAT-URJC-IMDEA NETWORK - F1"},
                  {"2" : "CIEMAT-URJC-IMDEA NETWORK - F2"},
                  {"3" : "Imdea Software F1 - (3)"},
                  {"4" : "Imdea Software F2 - (4)"},
                  {"15" : "UAM F1 - (15)"},
                  {"16" : "UAM F2 - (16)"}
                          
          ],
              "172.20.237.86":[
                  {"1" : "CSIC-UC3M-2017-06-F/UC3M-IMDEANET-2017-05-F1 (1)"},
                  {"2" : "CSIC - UC3M - IMDEA NETWORK - F2 (2)"},
                  {"3" : "CSICJO F1 - (3)"},
                  {"4" : "CSICJO F2 - (4)"},
          ]  
          }
        
        
          var vista_correos = {
              "172.20.237.86":[
                  {"5" : "UCM F1 - (5)"},
                  {"6" : "UCM F2 - (6)"}
          ]  
          }
          var indefinida_1 = {
            "172.20.237.86":[
              {"5" : "UCM F1 - (5)"},
              {"6" : "UCM F2 - (6)"}
            ]  
          }
          var indefinida_2 = {}
          var indefinida_3 = {}


var ports = document.getElementById("address").value;
var views = document.getElementById("vista").value;
const selectElement = document.getElementById('address');
selectElement.addEventListener('change', function() {
for (var i=0; i<=17; i++) {
  $('#port').children('option[value="'+i+'"]').remove();
}
var min = 1
var address = selectElement.value;
var select = document.getElementById('port'); 

if (views == 'noc' || views == 'ops'){
  for (var i=0;i<port_data[address].length; i++, min++){
      for (const [key, value] of Object.entries(port_data[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }else if (views == 'telefonica'){
    for (var i=0;i<vista_telefonica[address].length; i++, min++){
      for (const [key, value] of Object.entries(vista_telefonica[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }else if (views == 'correos'){
    for (var i=0;i<vista_correos[address].length; i++, min++){
      for (const [key, value] of Object.entries(vista_correos[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }else if (views == 'indefinida_1'){
    for (var i=0;i<indefinida_1[address].length; i++, min++){
      for (const [key, value] of Object.entries(indefinida_1[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }else if (views == 'indefinida_2'){
    for (var i=0;i<indefinida_2[address].length; i++, min++){
      for (const [key, value] of Object.entries(indefinida_2[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }else if (views == 'indefinida_3'){
    for (var i=0;i<indefinida_3[address].length; i++, min++){
      for (const [key, value] of Object.entries(indefinida_3[address][i])) {
      var opt = document.createElement('option');
      opt.value = key;
      opt.innerHTML = value;
      select.appendChild(opt);
      var instances = M.FormSelect.init(select, opt);
      };
    };
  }
})

});


function sameOrigin(url) {
  // test that a given url is a same-origin URL
  // url could be relative or scheme relative or absolute
  var host = document.location.host; // host + port
  var protocol = document.location.protocol;
  var sr_origin = '//' + host;
  var origin = protocol + sr_origin;
  // Allow absolute or scheme relative URLs to same origin
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
      !(/^(\/\/|http:|https:).*/.test(url));
};

// usando jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
};
function csrfSafeMethod(method) {
      // estos métodos no requieren CSRF
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };


function createFaultAnalysisTable(faultanalysis){
var table = document.createElement("table");
table.setAttribute("class", "table striped responsive-table");
/* table.setAttribute("style","border: 1px solid !important;"); */
document.getElementById('fault-analysis').appendChild(table);
var header = document.createElement("th");
var theader = document.createElement("thead");
header.innerHTML = "Fault Analysis Results";
var thr = document.createElement("tr");
thr.appendChild(header);
theader.appendChild(thr);
/* theader.setAttribute("style","border: 1px solid #9e9e9e !important;"); */
table.appendChild(theader);
var body = document.createElement("tbody");
table.appendChild(body)
for (let i = 0; i < faultanalysis.length; i++){
      var li = document.createElement("td");  
      li.innerHTML = faultanalysis[i]
      var tr = document.createElement("tr");
      tr.setAttribute("style","border: 1px solid #9e9e9e !important;")
      tr.appendChild(li);
      body.appendChild(tr);
  };
};

function createFingerprintTable(fingerprint){
var table = document.createElement("table");
/* table.setAttribute("style","border: 1px solid !important;"); */
table.setAttribute("class", "table striped responsive-table");
document.getElementById('finger-print').appendChild(table);
var header = document.createElement("th");
header.innerHTML = "Fingerprint Results";
var thr = document.createElement("tr");
var theader = document.createElement("thead");
thr.appendChild(header);
theader.appendChild(thr);
/* theader.setAttribute("style","border: 1px solid #9e9e9e !important;"); */
table.appendChild(theader);
tbody = document.createElement("tbody");
table.appendChild(tbody);
for (let i = 0; i < fingerprint.length; i++){
      var td = document.createElement("td");
      td.innerHTML = fingerprint[i]
      tr = document.createElement("tr");
      tr.appendChild(td);
      tr.setAttribute("style","border: 1px solid #9e9e9e !important;");
      tbody.appendChild(tr);
  };
};

function createEventsFPTable(fp_events){
var title = document.createElement("p");
title.setAttribute("class","left-align");
title.innerHTML = " <h6>Fingerprint</h6>";
document.getElementById('fp-events').appendChild(title);
var fp_table = document.createElement("table");
fp_table.setAttribute("class", "responsive-table  striped right-align");
document.getElementById('fp-events').appendChild(fp_table);
var fp_header1 = document.createElement("thead");
fp_table.append(fp_header1);
var hrow = document.createElement("tr");
hrow.setAttribute("class", "right-align");
fp_header1.append(hrow);
var theader1 = document.createElement("th");
theader1.innerHTML = "Position(m)";
hrow.append(theader1);
var theader2 = document.createElement("th");
theader2.innerHTML = "Reflectance(md)";
hrow.append(theader2);
var theader3 = document.createElement("th");
theader3.innerHTML = "Attenuation(dB)";
hrow.append(theader3);
var tbody = document.createElement("tbody");
fp_table.append(tbody)
for(let j = 0; j < fp_events.length; j++){
    var trow = document.createElement("tr");
    var data = String(""+fp_events[j]).split(",");
    for(x = 0; x < data.length; x++){
      var td_events = document.createElement("td");
      td_events.innerHTML = data[x];
      trow.appendChild(td_events);
    
    }
    tbody.append(trow);
  };

};  

function createEventsFATable(fa_events){
var title = document.createElement("p");
title.setAttribute("class","right-align");
title.innerHTML = "<h6>Fault Analysis</h6>";
document.getElementById('fa-events').appendChild(title);
/* document.getElementById('fa-events').setAttribute("class","right-align"); */
var fa_table = document.createElement("table");
fa_table.setAttribute("class", "responsive-table striped left-align");
document.getElementById('fa-events').appendChild(fa_table);
var fa_header1 = document.createElement("thead");
fa_table.append(fa_header1);
var hrow = document.createElement("tr");
hrow.setAttribute("class", "left-align");
fa_header1.append(hrow);
var theader1 = document.createElement("th");
theader1.innerHTML = "Position(m)";
hrow.append(theader1);
var theader2 = document.createElement("th");
theader2.innerHTML = "Reflectance(md)";
hrow.append(theader2);
var theader3 = document.createElement("th");
theader3.innerHTML = "Attenuation(dB)";
hrow.append(theader3);
var tbody = document.createElement("tbody");
fa_table.append(tbody)
for(let j = 0; j < fa_events.length; j++){
    var trow = document.createElement("tr");
    var data = String(""+fa_events[j]).split(",");
    for(x = 0; x < data.length; x++){
      var td_events = document.createElement("td");
      td_events.innerHTML = data[x];
      trow.appendChild(td_events);
    
    }
    tbody.append(trow);
  };
};