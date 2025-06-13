let restrictedWebsites=[];
function fetchRestrictedWebsites(){
    fetch("http://127.0.0.1:8000/api/restricted-urls/")
    .then((response) => response.json())
    .then((data) => {
        restrictedWebsites=data.restricted_urls || [];
        console.log("Restricted Websites: ", restrictedWebsites);
    })
    .catch((error) => {
        console.error(error);
    })
}

chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
        const url=new URL(details.url);
        if(restrictedWebsites.some((site) => url.hostname.includes(site))){
            alert(`Access to ${url.href} is restricted!`);
        }
        return { cancel: true};
    },
    {urls: ["<all_urls>"]},
    ["blocking"]
)

chrome.runtime.onInstalled.addListener(() => {
    fetchRestrictedWebsites();
})

setInterval(fetchRestrictedWebsites, 60000);

chrome.runtime.onMessage.addListener((message,sender,sendResponse) => {
    if(message.action==="refreshUrls"){
        fetchRestrictedWebsites();
        sendResponse({ status: "success", message: "URLs refreshed!" });
    }
    else if(message.action==="getUrls"){
        sendResponse({ restrictedWebsites });
    }
    else{
        sendResponse({ status: "success", message: "Unknown Action!" });
    }
    return true;
})