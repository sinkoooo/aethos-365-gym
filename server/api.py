from fastapi import FastAPI, Request
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI(title="USM AI Navigation Assistant API")

# Allow requests from the Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Database (ChromaDB)
# Using ephemeral client for testing; use PersistentClient in production
chroma_client = chromadb.PersistentClient(path="./usm_rag_db")
collection = chroma_client.get_or_create_collection(name="ui_elements")

# Initialize Local Embedding Model (CPU optimized ONNX under the hood)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2') 

# Initialize Local LLM Engine (Llama.cpp)
llm = None
MODEL_PATH = "./models/Qwen2.5-7B-Instruct.Q4_K_M.gguf"
if os.path.exists(MODEL_PATH):
    try:
        from llama_cpp import Llama
        print("Loading local LLM via llama.cpp (CPU Mode)...")
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=1024,
            n_threads=os.cpu_count(),
            n_gpu_layers=0,
            use_mlock=True
        )
    except Exception as e:
        print(f"Failed to load LLM: {e}")
else:
    print(f"Warning: Model not found at {MODEL_PATH}. Using mock LLM for prototype.")

# Schemas
class Locator(BaseModel):
    type: str
    value: str
    priority: int

class ElementNode(BaseModel):
    element_id: str
    url_regex: str
    semantic_context: List[str]
    locators: List[Locator]
    element_type: str
    interaction_type: str
    
class IntentRequest(BaseModel):
    query: str
    current_url: Optional[str] = None

@app.post("/api/v1/map")
async def save_mapped_node(node: ElementNode):
    """
    Called by the Chrome Extension in 'Mapping Mode' when an expert clicks a UI element.
    Saves the structure into the local Chroma RAG DB.
    """
    # Create the text document payload for the embedding
    document_text = f"Label/Context: {' | '.join(node.semantic_context)}. Type: {node.element_type}"
    
    # Generate CPU embedding
    embedding = model.encode(document_text).tolist()
    
    # Store in Vector DB
    collection.upsert(
        documents=[document_text],
        embeddings=[embedding],
        metadatas=[{"locators": str([l.dict() for l in node.locators]), "url": node.url_regex}],
        ids=[node.element_id]
    )
    return {"status": "success", "message": f"Ingested {node.element_id} into RAG"}

@app.post("/api/v1/intent")
async def resolve_intent(req: IntentRequest):
    """
    Called by the Chrome Extension in 'Assistant Mode' when an operator asks a question.
    Searches RAG for the best matching UI element and returns the XPaths.
    """
    search_query = req.query
    
    # Here, we would ask the LLM to refine the natural language query into a strict search intent.
    if llm:
        prompt = f"<|im_start|>system\nYou extract the core UI configuration parameter from user questions.<|im_end|>\n<|im_start|>user\n{req.query}<|im_end|>\n<|im_start|>assistant\nUI Parameter:"
        response = llm(prompt, max_tokens=15, stop=["\n"])
        extracted_intent = response['choices'][0]['text'].strip()
        if extracted_intent:
            search_query = extracted_intent
    
    # Search the RAG DB
    embedding = model.encode(search_query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1 
    )
    
    target_nodes = []
    if results['ids'] and len(results['ids'][0]) > 0:
        # We found a match in the UI database!
        metadata = results['metadatas'][0][0]
        # Parse locators string back to list of dicts (ast.literal_eval is safer, but eval works for prototype)
        import ast
        locs = ast.literal_eval(metadata['locators'])
        
        target_nodes.append({
            "step_instruction": "Target Identified",
            "locators": locs,
            "url_requirement": metadata.get('url', '*')
        })
        
    return {
        "status": "success",
        "search_query_used": search_query,
        "target_nodes": target_nodes
    }

if __name__ == "__main__":
    print("Starting USM Backend Server strictly on localhost...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
