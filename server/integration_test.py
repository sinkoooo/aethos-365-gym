import requests
import json
import time

API_URL = "http://127.0.0.1:8000/api/v1"

print("--- TESTING AI RAG PIPELINE (Simulating Chrome Extension) ---")

# 1. Simulating the Chrome Extension extracting the "Frequency Band" element
mapped_node = {
    "element_id": "usm_mock_freq_band_123",
    "url_regex": "/sample_usm.html",
    "semantic_context": ["Frequency Band Indicator", "Radio Configuration - eNodeB 8820", "Samsung USM"],
    "locators": [
        {"type": "xpath_text", "value": "//*[normalize-space(text())='Frequency Band Indicator']/following-sibling::input", "priority": 1}
    ],
    "element_type": "input",
    "interaction_type": "click"
}

print("\n1. EXTENSION 'RECORD MODE': Pushing mapped UI element to Local AI Backend...")
try:
    res_map = requests.post(f"{API_URL}/map", json=mapped_node)
    print("   [Success] RAG Database Ingestion Response:", res_map.json())
except Exception as e:
    print("   [ERROR] Could not connect to API:", e)
    exit()

# 2. Add slight semantic delay for ChromaDB flattening
time.sleep(1)

# 3. Simulate the User asking a question
query_text = "How do I configure the frequency band for this cell?"
print(f"\n2. USER INTENT IN CHAT: '{query_text}'")

intent_query = {
    "query": query_text,
    "current_url": "/sample_usm.html"
}

print("\n3. EXTENSION 'ASSISTANT MODE': Asking AI to find the UI locators...")
res_intent = requests.post(f"{API_URL}/intent", json=intent_query)

print("\n   [Success] AI Response sent back to Chrome Extension:")
print(json.dumps(res_intent.json(), indent=2))
