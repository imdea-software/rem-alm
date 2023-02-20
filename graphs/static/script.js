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


