# USM AI Navigation Assistant: Comprehensive Implementation Plan

## 1. Executive Summary
This document provides a comprehensive implementation plan for an AI-driven navigation assistant tailored for the Samsung Unified System Manager (USM). The solution addresses the steep learning curve of the USM platform by providing operators with a natural language interface that guides them through complex Configuration, Fault, and Performance Management tasks. The entire system is designed to operate securely within an air-gapped environment on standard CPU-based server architecture, leveraging open-source technologies.

## 2. Problem Statement
The Samsung USM manages multiple network elements (2G, 4G, 5G, BSC, eNB, DU, CU, etc.) and exposes thousands of configuration parameters and operations. The immense complexity makes it difficult for new or non-expert users to locate specific functionalities. Furthermore, deployment constraints within operator networks strictly prohibit internet access (air-gapped) and lack GPU acceleration, rendering cloud-based AI solutions or heavy local visual models unviable.

## 3. Proposed Solution
The core design principle avoids passing the massive USM DOM to a local LLM in real-time. Instead, we use a hybrid approach: building a structured **UI Element Database** via expert human-guided crawling, which is then utilized by a RAG-powered AI to translate user intents into exact UI locators. This enables natural language to UI navigation mapping with minimal computational overhead.

---

## 4. Architectural Workflow: The Two Phases

### Phase 1: Guided UI Mapping & Ingestion (The "Explorer")
Because USM is a complex, heavily dynamic web application (SPA), traditional automated web crawlers cannot easily discover all deep configuration menus and parameters. We solve this by using Domain Experts to map the UI visually.

1. **Mapping Mode**: A USM Domain Expert enables "Mapping Mode" in the Chrome extension and navigates through all the different pages and tabs of USM. No natural language prompts or specific tasks are entered during this phase.
2. **UI Extraction**: As the expert clicks through the application, the extension automatically extracts the visible UI elements on the current screen—buttons, menus, form fields, table headers, and their associated labels.
3. **Structured Storage (Navigation JSON)**: The extension builds a structural map of the USM interface. It links semantic labels (e.g., "Tx Power", "FCAPS Config") directly to their exact technical DOM locators (XPath or CSS Selectors), creating a massive "Navigation JSON" database of the application surface.
4. **Vectorization (RAG)**: This UI Map JSON is chunked and embedded into the local Vector Database. The RAG system now contains a perfect mapping of *human-readable parameter names* to *exact spatial UI elements*.

### Phase 2: User Intent & Navigation (The "Assistant")
When a standard operator uses the system, they interact with the AI using normal language.
1. **Semantic Intent**: The user types, "I need to configure Tx Power on an eNodeB."
2. **Fast RAG Retrieval**: The local CPU-bound AI converts this intent into a semantic search query. The Vector DB instantly returns the corresponding UI elements from the *Navigation JSON* that match "Tx Power" and "eNodeB".
3. **Deterministic UI Targeting**: The LLM determines the correct sequence of UI elements retrieved from RAG. 
4. **Visual Guidance**: The Chrome Extension receives the exact XPaths/CSS Selectors for the target elements. It highlights these elements on the operator's screen (e.g., highlighting the 'Radio Config' tab, then the 'Tx Power' input field), physically guiding them to the correct section without the LLM ever needing to read their live DOM.

---

## 5. Technology Stack

### 5.1 Frontend: Navigation Chrome Extension (Manifest V3)
- **Framework**: Vanilla JavaScript / HTML / CSS (to maintain lightweight footprint).
- **Mode Toggle**: Switches between Operator (Assistant) and Expert (Mapping) profiles.
- **Mapping Script**: Recursively parses the localized DOM fragments over new views, extracting elements into a schema.
- **DOM Manipulator**: Fast, native browser execution of bounding boxes and highlights based on retrieved locators.

### 5.2 Backend Engine (Operator CPU Servers)
- **Language**: Python 3.10+
- **API Server Layer**: `FastAPI` with `Uvicorn`, managing concurrent communication with the Chrome Extension.
- **Local RAG Pipeline (CPU Optimized)**:
  - **Vector DB**: `ChromaDB` or `FAISS` (extremely fast for CPU environments).
  - **Embeddings**: `all-MiniLM-L6-v2` via ONNX Runtime to create the dense index of the UI labels quickly on CPU.
- **NLP Engine**: `llama.cpp` serving a highly quantized model (e.g., 4-bit Llama-3 or Qwen2.5). Capable of running at 5-15 tokens/sec on standard server CPUs (such as Intel Xeon or AMD EPYC), ensuring smooth responsiveness.

---

## 6. Critical Design Strategies

### 6.1 Handling Dynamic UI Elements
USM utilizes dynamically generated CSS classes (e.g., `class="css-1x2y3z"`), making CSS selectors brittle. The "Mapping Mode" script generates a **Resilient Locator Fallback Array** for every element instead of a single selector:

1. **Semantic Attributes (Primary)**: Stable identifiers: `data-testid`, `aria-label`, `name`, or static `id`s.
2. **Text-Based XPath (Secondary)**: Target the exact visible text: `//button[normalize-space(text())='Apply Config']`.
3. **Hierarchical XPath (Tertiary)**: Structural relative targeting: `//label[contains(text(), 'Tx Power')]/following-sibling::input`.

During playback, the Extension tries locator #1. If it fails due to a UI update, it instantly falls back to #2 and #3, making the navigation system extremely robust.

### 6.2 System Updates & RAG Synchronization
- **Continuous Alignment**: When USM receives software updates, Domain Experts can re-trigger Mapping Mode on changed views to patch the vector database without full redeployment.
- **Centralized Local Hosting**: The backend components run on the operator's existing server infra. Operators seamlessly inherit the latest semantic maps.

---

## 7. Implementation Roadmap

### Phase 1: Core System & Prototyping (Weeks 1-4)
- **Objectives:** Establish base Chrome Extension infrastructure and backend skeleton.
- **Key Deliverables:** Extension that can successfully dump a normalized JSON map of a screen; basic Python API with ChromaDB initialization.

### Phase 2: Knowledge Ingestion & Integration (Weeks 5-8)
- **Objectives:** Operationalize the RAG pipeline and integrate quantized LLMs.
- **Key Deliverables:** `llama.cpp` serving a local 4-bit LLM; End-to-end connection mapping natural language to XPath retrieval.

### Phase 3: UAT & Optimization (Weeks 9-11)
- **Objectives:** Optimize queries for CPU constraints, harden locator robustness, test with actual USM environments.
- **Key Deliverables:** Real-world testing with USM domain experts creating mappings. Refinement of locator array accuracy (target: 95%+).

### Phase 4: Full Deployment & Training (Week 12)
- **Objectives:** Air-gapped rollout and operator familiarization.
- **Key Deliverables:** Security audit completion, installation scripts for Operator CPU Servers, and user training manuals.

---

## 8. Verification Plan & Testing Criteria
- **Milestone 1**: Successful JSON map extraction from a complex, dynamic SPA test instance holding 500+ DOM nodes.
- **Milestone 2**: Ingest JSON into ChromaDB and execute query ("Where is the alarm configuration?") verifying system correctly returns the XPath for that exact item.
- **Milestone 3**: Successful execution of a full "Search -> Target Element Highlight" workflow within < 2 seconds response time running exclusively on standard non-GPU local hardware.
