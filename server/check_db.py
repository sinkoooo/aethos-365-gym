import chromadb
import json

try:
    client = chromadb.PersistentClient(path="./usm_rag_db")
    collection = client.get_collection("ui_elements")
    
    count = collection.count()
    print(f"\n[RAG DB Status] Total UI elements stored: {count}")
    
    if count > 0:
        results = collection.get(include=["metadatas", "documents"])
        print("\n[DB Contents]")
        for i in range(count):
            print(f"--- Element ID: {results['ids'][i]} ---")
            print(f"Text Context: {results['documents'][i]}")
            meta = results['metadatas'][i]
            print(f"URL Context: {meta.get('url')}")
            locators = meta.get('locators', '[]')
            print(f"Locators generated: {locators}\n")
    else:
        print("The database is currently empty. Make sure you clicked 'Start Mapping Mode' in the extension and then clicked on some buttons or forms on a webpage!")
        
except Exception as e:
    print(f"Could not connect to database or collection not found yet. Error: {e}")
