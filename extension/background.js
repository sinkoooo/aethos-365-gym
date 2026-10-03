chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "ask_ai") {
        fetch('http://127.0.0.1:8000/api/v1/intent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: request.query })
        })
        .then(response => response.json())
        .then(data => sendResponse(data))
        .catch(error => {
            console.error('Error contacting AI server:', error);
            sendResponse({status: "error", detail: error.toString()});
        });
        return true; // Keep the message channel open for async response
    }
    
    if (request.action === "save_mapped_node") {
        fetch('http://127.0.0.1:8000/api/v1/map', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request.node)
        })
        .then(r => r.json())
        .then(data => console.log('Saved node to RAG:', data))
        .catch(error => console.error('Error saving node to RAG:', error));
    }
});
