# USM AI Navigation Assistant - UML Architecture Diagram

This diagram outlines the detailed workflow and component architecture of the USM Navigation Assistant, matching the two phases specified in your original plan.

```mermaid
flowchart TD
    %% User Personas
    User((User / Operator))
    Expert((Domain Expert))
    
    %% Frontend Components
    subgraph Frontend [Client - Web Browser]
        USM_Web[USM Web Application \n SPA Dashboard]
        Extension[Chrome Extension \n Manifest V3]
    end
    
    %% Backend/Server Components
    subgraph Backend [Local Operator Server CPU-Only]
        FastAPI_Server[FastAPI Server Engine]
        LLM[Local LLM Engine \n llama.cpp / 4-bit Quantized]
        VectorDB[(Vector Database \n ChromaDB / FAISS)]
    end
    
    %% MAPPING PHASE (Phase 1)
    Expert -- 1. Enables 'Mapping Mode' \n & Navigates --> USM_Web
    USM_Web -- 2. Exposes DOM Fragments --> Extension
    Extension -- 3. Extracts elements to \n Navigation JSON --> FastAPI_Server
    FastAPI_Server -- 4. Embeds semantic names & \n locators --> VectorDB
    
    %% ASSISTANT PHASE (Phase 2)
    User -- 5. Asks for Help \n Natural Language --> Extension
    Extension -- 6. Forwards Intent --> FastAPI_Server
    FastAPI_Server -- 7. Semantic Search Query --> VectorDB
    VectorDB -- 8. Returns Relevant \n XPath/Locators --> FastAPI_Server
    FastAPI_Server -- 9. Prompt + UI Context --> LLM
    LLM -- 10. Computes Deterministic \n Target Element --> FastAPI_Server
    FastAPI_Server -- 11. Dispatch Selected \n Locators --> Extension
    Extension -- 12. Executes Resilient \n XPath/CSS Targeting --> USM_Web
    USM_Web -- 13. Visually Highlights Tab/Input \n Bounding Boxes --> User

    %% Styling Elements
    classDef server fill:#e2e2e2,stroke:#333,stroke-width:2px;
    classDef frontend fill:#d4ebf2,stroke:#333,stroke-width:2px;
    classDef database fill:#f9e79f,stroke:#333,stroke-width:2px;
    classDef llm fill:#a9dfbf,stroke:#333,stroke-width:2px;
    classDef persona fill:#fcf3cf,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    
    class FastAPI_Server server;
    class USM_Web,Extension frontend;
    class VectorDB database;
    class LLM llm;
    class User,Expert persona;
```
