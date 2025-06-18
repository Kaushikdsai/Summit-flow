let restrictedWebsites = [];

function fetchRestrictedWebsites(){
    fetch("http://127.0.0.1:8000/api/restricted-urls/",{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if(data && Array.isArray(data.restricted_urls)){
                restrictedWebsites=data.restricted_urls
                    .filter((url) => typeof url === "string" && url.trim() !== "")
                    .map((url) => url.replace(/^https?:\/\//, "").replace(/\/$/, ""));
                console.log("Restricted Websites (Sanitized):", restrictedWebsites);
            }
            else{
                console.warn("Invalid data received from API:", data);
            }
        })
        .catch((error) =>
            console.error("Error fetching restricted websites:", error)
        );
}

chrome.tabs.onUpdated.addListener((tabId,changeInfo,tab) => {
    if(changeInfo.status === "loading" && tab.url){
        try{
            const normalizedUrl = new URL(tab.url).hostname;
            const isRestricted = restrictedWebsites.some((site) =>
                normalizedUrl.endsWith(site)
            );
            if(isRestricted){
                console.log("Displaying popup for restricted website:", tab.url);
                chrome.notifications.create({
                    type: "basic",
                    iconUrl: "icons/icon128.png",
                    title: "Restricted Website Alert",
                    message: `You visited a restricted website: ${tab.url}`,
                    priority: 2, 
                });
            }
        }
        catch (error){
            console.error("Error processing tab update:", error);
        }
    }
});

chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed. Fetching restricted websites...");
    fetchRestrictedWebsites();
});

setInterval(fetchRestrictedWebsites, 60000); 

chrome.runtime.onMessage.addListener((message,sender,sendResponse) => {
    if(message.action === "refreshUrls"){
        fetchRestrictedWebsites();
        sendResponse({ status: "success", message: "URLs refreshed!" });
    }
    else if(message.action === "getUrls"){
        sendResponse({ restrictedWebsites });
    }
    else{
        sendResponse({ status: "error", message: "Unknown Action!" });
    }
    return true;
});