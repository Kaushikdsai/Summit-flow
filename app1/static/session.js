const startElement=document.getElementById('start');
const restartElement=document.getElementById('restart');
const fastForwardElement=document.getElementById('fast-forward');
const timerElement=document.getElementById('timer');
const percentageElement=document.getElementById('percentage');
const img=document.getElementById('start-stop');
const bikeImg=document.getElementById('svg-image');
const playImage=img.dataset.playSrc;
const pauseImage=img.dataset.pauseSrc;

let totalMilliSeconds;
let temp;
let interval;
let isFirst=true;
let totalBreakMilliSeconds;
let breakTime;
let isOnBreak=false;

function startTimer(){
    if(isFirst){
        isFirst=false;
        console.log("time: "+focusDuration);
        const time=focusDuration;
        if(!time){
            alert("Enter valid time!");
            return;
        }
        img.src=pauseImage;
        let [focusHours,focusMinutes,focusSeconds]=time.split(":").map(Number);
        totalMilliSeconds=((focusHours*3600)+(focusMinutes*60)+focusSeconds)*1000;
        temp=totalMilliSeconds;
        breakTime=Math.floor(totalMilliSeconds/2);
        let [breakHours,breakMinutes,breakSeconds]=breakDuration.split(":").map(Number);
        totalBreakMilliSeconds=((breakHours*3600)+(breakMinutes*60)+breakSeconds)*1000;
        isOnBreak=false;
        clearInterval(interval);
        interval=setInterval(tick,100);
        startMoving(totalMilliSeconds+1);
    }
}

function tick(){
    if(!isOnBreak){
        if(totalMilliSeconds>0){
            totalMilliSeconds=Math.max(0,totalMilliSeconds-100);
            updateTimer(totalMilliSeconds);
            if(totalMilliSeconds<=breakTime){
                isOnBreak=true;
            }
        }
        else{
            clearInterval(interval);
            isFirst=true;
            totalMilliSeconds = 0;
            updateTimer(totalMilliSeconds);
            alert("The session is done! Congratulations for successfully completing it!");
            sendSessionData(temp/1000);
        }
    }
    else{
        if(totalBreakMilliSeconds>0){
            bikeImg.style.animationPlayState='paused';
            totalBreakMilliSeconds-=100;
        }
        else{
            isOnBreak=false;
            bikeImg.style.animationPlayState='running';
            totalMilliSeconds=Math.max(0,totalMilliSeconds-100);
            updateTimer(totalMilliSeconds);
        }
    }
}

function updateTimer(milliSeconds){
    const totalMilliSeconds=Math.floor(milliSeconds/1000);
    const hours=Math.floor(totalMilliSeconds/3600);
    const minutes=Math.floor((totalMilliSeconds%3600)/60);
    const secs=totalMilliSeconds%60;
    const newTime=[
        String(hours).padStart(2,'0'),
        String(minutes).padStart(2,'0'),
        String(secs).padStart(2,'0')
    ].join(":");
    timerElement.textContent=newTime;
    percentageElement.textContent=Math.floor(((temp-milliSeconds)/temp)*100);
}

function restartTimer(){
    bikeImg.style.animation='none';
    img.src=playImage;
    clearInterval(interval);
    isFirst=true;
    isOnBreak=false;
    const time=focusDuration;
    let [hours,minutes,seconds]=time.split(":").map(Number);
    totalMilliSeconds=((hours*3600)+(minutes*60)+seconds)*1000;
    timerElement.textContent=focusDuration;
    percentageElement.textContent=0;
}

function fastForwardTimer(){
    let allowedTime=((87/100)*temp);
    if((temp-totalMilliSeconds)>allowedTime){
        clearInterval(interval);
        interval=setInterval(tick,50);
    }
    else{
        alert("You need to pass through atleast 87% of the time");
    }
}

function toggle(){
    if(img.src.includes("play.png")){
        img.src=pauseImage;
        if(totalMilliSeconds<=0 && !isOnBreak){
            startTimer();
        }
        else{
            bikeImg.style.animationPlayState='running';
            clearInterval(interval);
            interval=setInterval(tick,100);
        }
    }
    else{
        img.src=playImage;
        bikeImg.style.animationPlayState='paused';
        clearInterval(interval);
    }
}

function startMoving(milliSeconds){
    bikeImg.style.animation='none';
    void bikeImg.offsetWidth;
    bikeImg.style.animation=`move ${milliSeconds/1000}s linear`;
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
    if(document.cookie && document.cookie!==""){
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