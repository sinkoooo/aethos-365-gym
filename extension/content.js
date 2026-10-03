let mappingActive = false;

// 1. Map Generation Logic
document.addEventListener('click', function(e) {
    if(!mappingActive) return;
    
    // Extractor Logic: Generate Locator Fallback Array
    const locators = [];
    const target = e.target;
    
    // Priority 1: Semantic Attributes
    if(target.id) locators.push({ type: "attribute", value: `//*[@id='${target.id}']`, priority: 1 });
    if(target.getAttribute('data-testid')) locators.push({ type: "attribute", value: `//*[@data-testid='${target.getAttribute('data-testid')}']`, priority: 1 });
    if(target.name) locators.push({ type: "attribute", value: `//*[@name='${target.name}']`, priority: 1 });
    
    // Priority 2: Text-based
    const textContext = target.innerText || target.textContent;
    if(textContext && textContext.trim() !== '') {
        const cleanText = textContext.replace(/'/g, "\\'").trim();
        locators.push({ type: "xpath_text", value: `//*[normalize-space(text())='${cleanText}']`, priority: 2 });
    }
    
    // Prepare Data
    const nodeData = {
        element_id: `usm_node_${Date.now()}`,
        url_regex: window.location.pathname,
        semantic_context: textContext ? [textContext.trim(), document.title] : [document.title],
        locators: locators,
        element_type: target.tagName.toLowerCase(),
        interaction_type: "click"
    };
    
    // Avoid sending useless clicks like clicking strictly on the body/html
    if(['html', 'body'].includes(nodeData.element_type)) return;
    
    // Send to background to save in RAG
    chrome.runtime.sendMessage({ action: "save_mapped_node", node: nodeData });
    
    // Visual feedback for expert
    drawHighlight(target, "red");
});

// 2. Playback / Highlight Logic
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if(request.action === "start_mapping") {
        mappingActive = true;
        alert('Mapping Mode Active: Click around to map UI elements to RAG.');
    }
    
    if(request.action === "highlight_nodes" && request.nodes) {
        request.nodes.forEach(node => {
            let foundElement = null;
            
            // Try locators by priority
            const sortedLocators = node.locators.sort((a,b) => a.priority - b.priority);
            for(let loc of sortedLocators) {
                try {
                    let evaluation = document.evaluate(loc.value, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    if(evaluation.singleNodeValue) {
                        foundElement = evaluation.singleNodeValue;
                        break;
                    }
                } catch(e) {
                    console.log("Invalid XPath:", loc.value);
                }
            }
            
            if(foundElement) {
                drawHighlight(foundElement, "#2ed573"); // green for success
            }
        });
    }
});

// Helper: Visual Overlays (Resilient against CSS frameworks)
function drawHighlight(element, color) {
    const rect = element.getBoundingClientRect();
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = `${rect.top}px`;
    overlay.style.left = `${rect.left}px`;
    overlay.style.width = `${rect.width}px`;
    overlay.style.height = `${rect.height}px`;
    overlay.style.zIndex = '999999';
    overlay.style.pointerEvents = 'none'; // Don't block clicks
    overlay.style.boxShadow = `0 0 10px 4px ${color}, inset 0 0 5px 2px ${color}`;
    overlay.style.borderRadius = '3px';
    overlay.style.transition = 'opacity 0.5s ease-out';
    
    document.documentElement.appendChild(overlay);
    
    // Fade out after 3 seconds
    setTimeout(() => {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 500);
    }, 3000);
}
