document.getElementById("refresh").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "refreshUrls" }, (response) => {
        if(response.status==="success"){
            alert(response.message);
        }
        else{
            alert("Error: "+response.message);
        }
    });
});

chrome.runtime.sendMessage({ action: "getUrls" }, (response) => {
    const listElement=document.getElementById("restricted-websites");
    if(response.restrictedWebsites && response.restrictedWebsites.length>0){
        response.restrictedWebsites.forEach((site) => {
            const li=document.createElement("li");
            li.textContent=site;
            listElement.appendChild(li);
        });
    } else {
        listElement.textContent = "No restricted websites.";
    }
});