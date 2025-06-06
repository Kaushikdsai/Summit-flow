const startElement=document.getElementById('start');
const restartElement=document.getElementById('restart');
const fastForwardElement=document.getElementById('fast-forward');
const timerElement=document.getElementById('timer');
const percentageElement=document.getElementById('percentage');
const img=document.getElementById('start-stop');
const bikeImg=document.getElementById('svg-image');
const playImage=img.dataset.playSrc;
const pauseImage=img.dataset.pauseSrc;

let totalSeconds;
let temp;
let interval;
let isFirst=true;
let totalBreakSeconds;
let breakTime;
let isOnBreak=false;

function startTimer(){
    if(isFirst){
        isFirst=false;
        const time=focusDuration;
        if(!time){
            alert("Enter valid time!");
            return;
        }
        img.src=pauseImage;
        let [focusHours,focusMinutes,focusSeconds]=time.split(":").map(Number);
        totalSeconds=(focusHours*3600)+(focusMinutes*60)+focusSeconds;
        temp=totalSeconds;
        breakTime=Math.floor(totalSeconds/2);
        let [breakHours,breakMinutes,breakSeconds]=breakDuration.split(":").map(Number);
        totalBreakSeconds=(breakHours*3600)+(breakMinutes*60)+breakSeconds;
        isOnBreak=false;
        clearInterval(interval);
        interval=setInterval(tick,1000);
        startMoving(totalSeconds);
    }
}

function tick(){
    if(!isOnBreak){
        if(totalSeconds>0){
            totalSeconds--;
            updateTimer(totalSeconds);
            if(totalSeconds===breakTime){
                isOnBreak=true;
            }
        }else{
            clearInterval(interval);
            isFirst=true;
            alert("The session is done! Congratulations for successfully completing it!");
            sendSessionData(temp);
        }
    }else{
        if(totalBreakSeconds>0){
            bikeImg.style.animationPlayState='paused';
            totalBreakSeconds--;
        }else{
            isOnBreak=false;
            bikeImg.style.animationPlayState='running';
            totalSeconds--;
            updateTimer(totalSeconds);
        }
    }
}

function updateTimer(seconds){
    const hours=Math.floor(seconds/3600);
    const minutes=Math.floor((seconds%3600)/60);
    const secs=seconds%60;
    const newTime=[
        String(hours).padStart(2,'0'),
        String(minutes).padStart(2,'0'),
        String(secs).padStart(2,'0')
    ].join(":");
    timerElement.textContent=newTime;
    percentageElement.textContent=Math.floor(((temp-seconds)/temp)*100);
}

function restartTimer(){
    bikeImg.style.animation='none';
    img.src=playImage;
    clearInterval(interval);
    isFirst=true;
    isOnBreak=false;
    const time=focusDuration;
    let [hours,minutes,seconds]=time.split(":").map(Number);
    totalSeconds=(hours*3600)+(minutes*60)+seconds;
    timerElement.textContent=focusDuration;
    percentageElement.textContent=0;
}

function fastForwardTimer(){
    let allowedTime=((87/100)*temp);
    if((temp-totalSeconds)>allowedTime){
        clearInterval(interval);
        interval=setInterval(tick,500);
    }else{
        alert("You need to pass through atleast 87% of the time");
    }
}

function toggle(){
    if(img.src.includes("play.png")){
        img.src=pauseImage;
        if(totalSeconds<=0&&!isOnBreak){
            startTimer();
        }else{
            bikeImg.style.animationPlayState='running';
            clearInterval(interval);
            interval=setInterval(tick,1000);
        }
    }else{
        img.src=playImage;
        bikeImg.style.animationPlayState='paused';
        clearInterval(interval);
    }
}

function startMoving(seconds){
    bikeImg.style.animation='none';
    void bikeImg.offsetWidth;
    bikeImg.style.animation=`move ${seconds}s linear`;
}

function sendSessionData(session_seconds){
    console.log('Sending session data:',session_seconds);
    fetch('/update-metrics/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':getCookie('csrftoken'),
        },
        body:JSON.stringify({session_seconds}),
        credentials:'include'
    })
    .then(response=>response.json())
    .then(data=>{
        console.log(data);
    })
    .catch(error=>{
        console.error('Error sending session data:',error);
    });
}

function getCookie(name){
    let cookieValue=null;
    if(document.cookie&&document.cookie!==""){
        const cookies=document.cookie.split(";");
        for(let cookie of cookies){
            cookie=cookie.trim();
            if(cookie.startsWith(name+"=")){
                cookieValue=decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}

startElement.addEventListener("click",()=>{
    if(isFirst){
        startTimer();
    }else{
        toggle();
    }
});
restartElement.addEventListener("click",restartTimer);
fastForwardElement.addEventListener("click",fastForwardTimer);
