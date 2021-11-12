const searchForm = document.querySelector("#search-form");
var speakButton=document.getElementById("speakbutton");
var speakIcon=speakButton.firstElementChild;
const searchFormInput = searchForm.querySelector("input"); // <=> document.querySelector("#search-form input");
function getLocalStream() {
    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then( stream => {
        window.localStream = stream; // A
        window.localAudio.srcObject = stream; // B
        window.localAudio.autoplay = true; // C
    }).catch( err => {
        console.log("u got an error:" + err)
    });
}
var inp=document.getElementById("inp");
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition; // if none exists -> undefined
if(SpeechRecognition) {
  console.log("Your Browser supports speech Recognition");
  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  

  searchForm.insertAdjacentHTML("beforeend", '<button type="button" id="micbutton"><i class="fas fa-microphone-slash"></i></button>');
  searchFormInput.style.paddingRight = "50px";

  const micBtn = document.getElementById("micbutton");
  const micIcon = micBtn.firstElementChild;

  micBtn.addEventListener("click", micBtnClick);
  function micBtnClick() {
      getLocalStream();
    if(micIcon.classList.contains("fa-microphone-slash")) { // Start Voice Recognition

      recognition.start(); // First time you have to allow access to mic!
    }
    else {
      recognition.stop();
    }
  }

  recognition.addEventListener("start", startSpeechRecognition); // <=> recognition.onstart = function() {...}
  function startSpeechRecognition() {
    micIcon.classList.remove("fa-microphone-slash");
    micIcon.classList.add("fa-microphone");
    searchFormInput.focus();
    console.log("Voice activated, SPEAK");
  }

  recognition.addEventListener("end", endSpeechRecognition); // <=> recognition.onend = function() {...}
  function endSpeechRecognition() {
    micIcon.classList.remove("fa-microphone");
    micIcon.classList.add("fa-microphone-slash");
    searchFormInput.focus();
    console.log("Speech recognition service disconnected");
  }

  recognition.addEventListener("result", resultOfSpeechRecognition); // <=> recognition.onresult = function(event) {...} - Fires when you stop talking
  function resultOfSpeechRecognition(event) {
    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    if(transcript.toLowerCase().trim()==="stop recording") {
      recognition.stop();
    }
    else if(!searchFormInput.value) {
      searchFormInput.value = transcript;
    }
    else {
        if(transcript.toLowerCase().trim()==="reset") {
        searchFormInput.value = "";
      }
      else {
        if(transcript.toLowerCase().trim()==="go"){
          var inpu=inp.value;
          if(speakIcon.classList.contains("fa-volume-down")){
            sendReq(inpu,true);
          }else{
            sendReq(inpu,false);
          }
            inp.value="";
        }
        else{
        searchFormInput.value = transcript;
        }
      }
    }
    // searchFormInput.value = transcript;
    // searchFormInput.focus();
    // setTimeout(() => {
    //   searchForm.submit();
    // }, 500);
  }
  
  //Reset,Go,Stop recording
}
else {
  console.log("Your Browser does not support speech Recognition");
  
}