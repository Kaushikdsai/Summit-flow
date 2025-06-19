let restrictedWebsites = [];

function fetchRestrictedWebsites() {
    fetch("http://127.0.0.1:8000/api/restricted-urls/", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })
    .then((response) => response.json())
    .then((data) => {
        if(data && Array.isArray(data.restricted_urls)){
            restrictedWebsites=data.restricted_urls
            .filter((url) => typeof url==="string" && url.trim()!=="")
            .map((url) => url.replace(/^https?:\/\//, "").replace(/\/$/, ""));
            console.log("Restricted Websites:", restrictedWebsites);
            updateBlockingRules();
        }
        else{
            console.warn("Invalid data received from API:", data);
        }
    })
    .catch((error) => console.error("Error fetching restricted websites:", error));
}

function updateBlockingRules(){
    const rules=restrictedWebsites.map((site, index) => ({
        id: index + 1,
        priority: 1,
        action: { type: "block" },
        condition: { urlFilter: `*://${site}/*`, resourceTypes: ["main_frame"] },
    }));

    chrome.declarativeNetRequest.updateDynamicRules(
    {
        removeRuleIds: Array.from({ length: 1000 }, (_, i) => i + 1),
        addRules: rules,
    },
    () => console.log("Blocking rules updated:", rules)
  );
}

chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed. Fetching restricted websites...");
    fetchRestrictedWebsites();
});

setInterval(fetchRestrictedWebsites, 60000);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action==="refreshUrls"){
        fetchRestrictedWebsites();
        sendResponse({ status: "success", message: "URLs refreshed!" });
    }
    else if(message.action==="getUrls"){
        sendResponse({ restrictedWebsites });
    }
    else if(message.action==="clearUrls"){
        restrictedWebsites=[];
        updateBlockingRules();
        sendResponse({ status: "success", message: "URLs cleared!" });
    }
    else{
        sendResponse({ status: "error", message: "Unknown Action!" });
    }
    return true;
});
