document.getElementById('btn-record').addEventListener('click', () => {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "start_mapping"});
        document.getElementById('status-text').innerText = "Status: Mapping active on page.";
        document.getElementById('chat-container').style.display = "none";
    });
});

document.getElementById('btn-play').addEventListener('click', () => {
    document.getElementById('status-text').innerText = "Status: AI Mode Active";
    document.getElementById('chat-container').style.display = "block";
});

document.getElementById('btn-send').addEventListener('click', () => {
    const query = document.getElementById('chat-input').value;
    if(!query) return;
    
    document.getElementById('status-text').innerText = "Status: Thinking...";
    
    chrome.runtime.sendMessage({ action: "ask_ai", query: query }, (response) => {
        if(response && response.status === "success" && response.target_nodes.length > 0) {
           document.getElementById('status-text').innerText = "Status: Highlighting target!";
           chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: "highlight_nodes", 
                    nodes: response.target_nodes
                });
            });
        } else {
            document.getElementById('status-text').innerText = "Status: " + (response ? response.detail || "Not found" : "Error connecting to server.");
        }
    });
});
