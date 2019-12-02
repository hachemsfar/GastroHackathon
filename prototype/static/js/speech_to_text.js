var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = function() {
    recognizing = true;
    start_img.src = "/static/img/mic-animate.gif";
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_img.src = "/static/img/mic.gif";
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = "/static/img/mic.gif";
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      ignore_onend = true;
    }
  };

    recognition.onresult = function(event) {  
      var interim_transcript = '';
      for (var i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          final_transcript += event.results[i][0].transcript;
        } else {
          interim_transcript += event.results[i][0].transcript;
        }
      }
    final_span = document.getElementById('final_span');
    interim_span = document.getElementById('interim_span')
    final_span.textContent = final_transcript;
    interim_span.textContent = interim_transcript;
    };

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_img.src = "/static/img/mic.gif";
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }
    // get the value of CSRF token
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();

    var data = final_transcript;
    console.log(data);

   // $.get('/confirm_order/?data='+data);
   $(location).attr('href','/confirm_order/?data='+data);

  };
}


function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.start();
  ignore_onend = false;
    final_span = document.getElementById('final_span');
  interim_span = document.getElementById('interim_span')
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_img.src = '/static/img/mic-slash.gif';
  start_timestamp = event.timeStamp;
}
