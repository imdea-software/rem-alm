$(document).ready(function(){
    var ports_data = {
        "172.20.237.90":[
            {"1" : "CIEMAT-URJC-IMDEA NETWORK - F1"},
            {"2" : "CIEMAT-URJC-IMDEA NETWORK - F2"},
            {"3" : "Imdea Software F1"},
            {"4" : "Imdea Software F2"},
            {"5" : "UCM F1"},
            {"6" : "UCM F2"},
            {"7" : "CIB F1"},
            {"8" : "CIB F2"},
            {"9" : "UNED F1"},
            {"10" : "UNED F2"},
            {"11" : "Casa Velázquez F1"},
            {"12" : "Casa Velázquez F2"},
            {"13" : "UPM F1"},
            {"14" : "UPM F2"},
            {"15" : "UAM F1"},
            {"16" : "UAM F2"}
                       
    ],
        "172.20.237.86":[
            {"1" : "CSIC - UC3M - IMDEA NETWORK - F1"},
            {"2" : "CSIC - UC3M - IMDEA NETWORK - F2"},
            {"3" : "CSICJO F1"},
            {"4" : "CSICJO F2"},
            {"5" : "UCM F1"},
            {"6" : "UCM F2"}
    ]  
    }

const selectElement = document.getElementById('address')

  selectElement.addEventListener('change', function() {
  var min = 1
  var address = selectElement.value;
  var select = document.getElementById('port'); 


  for (var i=0; i<=17; i++) {
      $('#port').children('option[value="'+i+'"]').remove();
  }
  for (var i=0;i<ports_data[address].length; i++, min++){
        var opt = document.createElement('option');
        opt.value = min;
        opt.innerHTML = ports_data[address][i][min];

        select.appendChild(opt);
        var instances = M.FormSelect.init(select, opt);
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


 $("#portForm").on('submit', function(event){
      document.getElementById('applybutton').disabled=true; 
      /* document.getElementById('applybutton').innerHTML='Recibiendo información...'; */
      var url = "{% url 'ajax-alm' %}";
      var form = document.querySelector("[name='portForm']")
      var port = form.elements.port.value;
      var address = form.elements.address.value;
      var type = form.elements.type.value;
      var csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
}
  });
  $.ajax({
      url : url,
      data : {
        "port": port,
        "address":address,
        "type" : type
      },
      type : "POST",
      dataType:"json",
      success: function(response){  
          if(response['keys'] && response['value1'] && response['value2']){
            var keys = response['keys'];
            var value1 = response['value1'];
            var value2 = response['value2'];
            var faultanalysis = response['faultanalysis'];
            var fingerprint = response['fingerprint'];
            var fa_events = response['fa_event'];
            var fp_events = response['fp_event'];
            var portname = response['portname'];
            var options = {
                chart: {
                  height: 550,
                  width: 1200,
                  type: "line",
                  stacked: false
                },
                colors: ["#424242","#00b8d4"],
                series: [
                  {
                    name: "Finger Print",
                    data: value1
                  },
                  {
                    name: "Fault analysis",
                    data: value2
                  }
                ],
                events: {
                  mounted: (chart) => {
                    chart.windowResizeHandler();
                  }
                },
                plotOptions: {
                  bar: {
                    columnWidth: "20%"
                  }
                },
                responsive: [
                    {
                      breakpoint: 700,
                      options: {
                        plotOptions: {
                          line: {
                            height:565,
                            width:760,
                          }
                        },
                        legend: {
                          position: "bottom"
                        }
                      }
                    }
                  ],
                xaxis: {
                  categories: keys,
                  type: 'numeric',
                  title:{
                    text:'KM',
                    position: "bottom",
                    style:{
                      color: "#424242",
                    }
                  },
                },
                yaxis: [
                  {
                    axisTicks: {
                      show: true
                    },
                    axisBorder: {
                      show: true,
                      color: ""
                    },
                    labels: {
                      style: {
                        colors: ""
                      }
                    },
                    title: {
                      text: "Finger Print",
                      style: {
                        color: "#424242",
                      }
                    }
                  },
                  {
                    opposite: true,
                    axisTicks: {
                      show: true
                    },
                    axisBorder: {
                      show: true,
                      color: "#00b8d4"
                    },
                    labels: {
                      style: {
                        colors: "#00b8d4"
                      }
                    },
                    title: {
                      text: "Fault analysis",
                      style: {
                        color: "#00b8d4"
                      }
                    }
                  }
                ],
                legend: {
                  horizontalAlign: "left",
                  offsetX: 40
                }
            };
            document.getElementById('fault-analysis').innerHTML='';
            document.getElementById('finger-print').innerHTML='';
            document.getElementById('fp-events').innerHTML='';
            document.getElementById('fa-events').innerHTML='';
            document.getElementById('chart').innerHTML='';
            document.getElementById('portname').innerHTML='';
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
            document.getElementById('applybutton').innerHTML='Aceptar';
            document.getElementById('applybutton').disabled=false;
            var name = faultanalysis[23] 
            var tfa = faultanalysis[4]
            if (response['value1'] == null | !response['value1'] == null){
              document.getElementById('fault-analysis').innerHTML='No hay información disponible...';
              document.getElementById('chart').innerHTML='';

            }else {
              document.getElementById('portname').innerHTML=portname+"  ";
              createFaultAnalysisTable(faultanalysis);
              createFingerprintTable(fingerprint);
              createEventsFPTable(fp_events);
              createEventsFATable(fa_events);
            }
            
          }else{
            if (response['value1'] == null | !response['value1'] == null){
            document.getElementById('fault-analysis').innerHTML='No hay información disponible...';
            document.getElementById('finger-print').innerHTML='';
            document.getElementById('chart').innerHTML='';
            $('#applybutton').removeAttr('disabled');
          }  
          }
        },
        error: function(){
          document.getElementById('fault-analysis').innerHTML='';
            document.getElementById('finger-print').innerHTML='';
            document.getElementById('fp-events').innerHTML='';
            document.getElementById('fa-events').innerHTML='';
            document.getElementById('chart').innerHTML='';
            document.getElementById('portname').innerHTML='';
          document.getElementById('chart').innerHTML="Ahora mismo no hay información disponible sobre esta gráfica...";
          document.getElementById('applybutton').disabled=false;
            }
          });
        event.preventDefault();
});


function createFaultAnalysisTable(faultanalysis){
  var ul = document.createElement("ul");
  document.getElementById('fault-analysis').appendChild(ul);
  ul.setAttribute( "class", "collection with-header left-align");
  var header = document.createElement("li");
  header.className = "collection-header";
  header.innerHTML = "<p> Fault Analysis Results </p>";
  ul.appendChild(header);
  for (let i = 0; i < faultanalysis.length; i++){
        var li = document.createElement("li");  
        li.className = "collection-item";
        li.innerHTML = faultanalysis[i]
        ul.appendChild(li);
    };
};



function createFingerprintTable(fingerprint){
  document.getElementById('fp-events').innerHTML='';
  document.getElementById('fa-events').innerHTML='';
  var ul = document.createElement("ul");
  document.getElementById('finger-print').appendChild(ul);
  ul.setAttribute( "class", "collection with-header left-align");
  var header = document.createElement("li");
  header.className = "collection-header";
  header.innerHTML = "<p>Fingerprint Results </p>";
  ul.appendChild(header);
  for (let i = 0; i < fingerprint.length; i++){
        var li = document.createElement("li");
        li.className = "collection-item";
        li.innerHTML = fingerprint[i]
        ul.appendChild(li);
    };
}

function createEventsFPTable(fp_events){
  /* console.log(fp_events); */
  var title = document.createElement("p");
  title.setAttribute("class","left-align cyan-text darken-4");
  title.innerHTML = "Fingerprint";
  document.getElementById('fp-events').appendChild(title);
  var fp_table = document.createElement("table");
  fp_table.setAttribute("class", "responsive-table  highlight left-align");
  document.getElementById('fp-events').appendChild(fp_table);
  var fp_header1 = document.createElement("thead");
  fp_table.append(fp_header1);
  var hrow = document.createElement("tr");
  hrow.setAttribute("class", "left-align");
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
  title.setAttribute("class","right-align cyan-text darken-4");
  title.innerHTML = "Fault Analysis";
  document.getElementById('fa-events').appendChild(title);
  /* document.getElementById('fa-events').setAttribute("class","right-align"); */
  var fa_table = document.createElement("table");
  fa_table.setAttribute("class", "responsive-table highlight left-align");
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