let speech = new SpeechSynthesisUtterance();
speech.lang = "en";
var speakButton=document.getElementById("speakbutton");
var speakIcon=speakButton.firstElementChild;
speakButton.addEventListener("click",()=>{
  
  if(speakIcon.classList.contains("fa-volume-mute")){
    speakIcon.classList.remove("fa-volume-mute");
    speakIcon.classList.add("fa-volume-down");
  
  }
  else{
    speakIcon.classList.add("fa-volume-mute");
    speakIcon.classList.remove("fa-volume-down");
  
  }
});
function openForm() {
    document.getElementById("myForm").style.display = "block";
  }
  

  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }
  closeForm();

const autoscroll=()=>{
  const $messages = document.querySelector('#chatwin');
  $messages.scrollTop=$messages.scrollHeight;
}
function sendReq(ques,a1){
  $.ajax({
    type: "POST",
    url: "/chatbot",
    data: {
        question: ques
    },
    success: function(result) {
        console.log("shrey dangayach123");
        var p1 =document.createElement("p");
        p1.innerHTML = '<i class="far fa-user use"></i>';
        var text=document.createTextNode(ques+"  ");
        p1.appendChild(text);
        p1.classList.add("p11");
        p1.classList.add("user");
        chatWin.appendChild(p1);

        var p1 =document.createElement("p");
        p1.innerHTML='<i class="fas fa-laptop lap"></i>'
        var a=result.response
        var arr=a.split("\n");
        var i=0;
        while(i!=arr.length){
          var text=document.createTextNode(arr[i]);
          p1.appendChild(text);
          var br1=document.createElement("br");
          p1.appendChild(br1);
          i=i+1;
        }
        if(a1){
          speech.text=result.response;
          speech.rate = 1;
          speech.volume = 10;
          speech.pitch = 1;
          let voices=[];
          window.speechSynthesis.onvoiceschanged = () => {
          voices = window.speechSynthesis.getVoices();
          speech.voice = voices[0];
        };
        window.speechSynthesis.speak(speech);
        }
        p1.classList.add("p11");
        chatWin.appendChild(p1);
        autoscroll();

    },
    error: function(result) {
        alert('result');
    }
});
}

var send = document.getElementById("sendButton");
var chatWin=document.getElementById("chatwin");
var p1 =document.createElement("p");
p1.innerHTML = '<i class="fas fa-laptop lap"></i>';
var text=document.createTextNode("Hello ! Welcome to Me..Guide . I am Helper Bot . How can i help you ?");
p1.appendChild(text);
p1.classList.add("p11");
chatWin.appendChild(p1);
        
        
var inp=document.getElementById("inp");
send.addEventListener("click",()=>{
  var inpu=inp.value;

  if(inpu===""){
    alert("Enter Query To Be Asked !!");
  }
  else{
      if(speakIcon.classList.contains("fa-volume-down")){
        sendReq(inpu,true);
      }else{
        sendReq(inpu,false);
      }
      
      inp.value="";
  }
})
