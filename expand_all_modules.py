import os
import shutil

workspace_file = r"d:\Antigravity\Shivam_Staff_Engineer_Mastery_Roadmap.html"
brain_file = r"C:\Users\shiva\.gemini\antigravity\brain\623354e4-df8d-442a-a628-1971c1a87479\Shivam_Staff_Engineer_Mastery_Roadmap.html"

with open(workspace_file, "r", encoding="utf-8") as f:
    html = f.read()

# =========================================================================
# ENRICHED CHAPTER 3 CONTENT
# =========================================================================
ch3_old_theory = """        <div id="ch3-content-theory" class="tab-content space-y-4 text-sm text-slate-300">
          <h3 class="text-base font-bold text-white">The Dual-Write Problem in Microservices</h3>
          <p>
            Writing to a database and publishing an event to Kafka cannot be wrapped in a single distributed transaction without <span class="cloze">Two-Phase Commit (2PC / XA)</span>, which is synchronous, slow, and blocking.
            The solution is the <span class="cloze">Transactional Outbox Pattern</span>: commit business entity mutation and an outbox event in the same local ACID transaction. A CDC connector (<span class="cloze">Debezium reading PostgreSQL WAL via pgoutput</span>) streams outbox events into Kafka.
          </p>
        </div>"""

ch3_new_theory = """        <div id="ch3-content-theory" class="tab-content space-y-5 text-sm text-slate-300">
          <h3 class="text-base font-bold text-white">The Dual-Write Dilemma & Distributed State Inconsistency</h3>
          <p>
            In distributed microservices, state mutations frequently require two distinct actions: <strong>1) Updating relational storage</strong> (PostgreSQL) and <strong>2) Emitting an event</strong> (Apache Kafka). 
            Because network connections are inherently unreliable, executing these as separate network calls creates an impossible race condition:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-rose-300 space-y-1">
            <strong>Dual-Write Failure Modes:</strong><br>
            • Strategy A (DB First): App writes to DB (Success) &rarr; App attempts to publish to Kafka (Network Timeout / OOM Crash) &rarr; <em>Event is permanently lost! Downstream microservices never receive notification.</em><br>
            • Strategy B (Kafka First): App publishes to Kafka (Success) &rarr; App attempts DB commit (Unique Constraint Violation / DB Crash) &rarr; <em>Consumers process phantom events that do not exist in the source of truth!</em>
          </div>

          <h4 class="text-sm font-bold text-white mt-2">Why Two-Phase Commit (2PC / XA) Fails at Scale</h4>
          <p>
            Traditional enterprise distributed transactions rely on 2PC (Prepare &rarr; Commit). However, 2PC is fundamentally unsuited for carrier-grade throughput (45k TPS):
            it holds exclusive database locks across the network during phase 1, scales latency to the slowest participant, and causes cluster-wide deadlocks if the transaction coordinator crashes while holding locks.
          </p>

          <h4 class="text-sm font-bold text-white mt-2">The Architectural Solution: The Transactional Outbox Pattern</h4>
          <p>
            Instead of distributed locking, the application executes both writes inside a <strong>single local PostgreSQL ACID transaction</strong>:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-emerald-300">
            BEGIN TRANSACTION;<br>
            -- 1. Apply business state mutation<br>
            UPDATE managed_objects SET tx_power = 43.5, version = 104 WHERE id = 'cell:eNodeB_104';<br><br>
            -- 2. Append event record to local outbox table<br>
            INSERT INTO outbox_events (event_id, aggregate_type, aggregate_id, event_type, payload, created_at)<br>
            VALUES ('evt_9831', 'CellSector', 'cell:eNodeB_104', 'POWER_RECONFIGURED', '{"txPower": 43.5}', NOW());<br><br>
            COMMIT TRANSACTION; -- Guaranteed 100% atomic! Zero distributed locks.
          </div>
          <p>
            A background Change Data Capture (CDC) worker—specifically <strong>Debezium</strong> tailing the PostgreSQL Write-Ahead Log (WAL) via the low-overhead <code class="text-amber-300 font-mono cloze">pgoutput</code> logical replication plugin—streams commits out of the outbox table directly into Apache Kafka with guaranteed at-least-once delivery.
          </p>

          <h4 class="text-sm font-bold text-white mt-2">Why Kafka Producer Idempotence Does NOT Protect Consumers</h4>
          <p>
            Kafka's <code class="text-amber-300 font-mono cloze">enable.idempotence=true</code> assigns each producer session an internal Producer ID (PID) and monotonic sequence numbers per partition. This strictly deduplicates producer-to-broker network retries.
            However, consumer consumption is strictly <strong>at-least-once</strong>:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-blue-300">
            Consumer Rebalance Storm Hazard:<br>
            1. Consumer Pod 1 polls message 'evt_9831' from Partition 4.<br>
            2. Consumer Pod 1 applies mutation to PostgreSQL (Success).<br>
            3. Before Pod 1 commits offset to __consumer_offsets, Kubernetes terminates Pod 1 (or GC pause exceeds max.poll.interval.ms).<br>
            4. Kafka triggers Consumer Group Rebalance! Partition 4 is reassigned to Consumer Pod 2.<br>
            5. Consumer Pod 2 reads from the last committed offset &rarr; RE-RECEIVES 'evt_9831'!<br>
            &rarr; Without consumer idempotency, cell configuration executes twice!
          </div>

          <h4 class="text-sm font-bold text-white mt-2">The 2-Tier Consumer Defense Architecture</h4>
          <p>
            To guarantee strict single-execution semantics under rebalance storms without adding latency:
          </p>
          <ul class="list-disc pl-5 space-y-1.5 text-xs text-slate-300">
            <li><strong>Tier 1 (L1 In-Memory Fast-Path Filter):</strong> Redis atomic key reservation (<code class="text-amber-300 font-mono">SET idemp:evt:{id} "PENDING" NX EX 86400</code>). Filters out 99.9% of replay duplicates in sub-milliseconds without touching database IOPS.</li>
            <li><strong>Tier 2 (L2 Storage Anchor):</strong> Relational idempotency ledger table (<code class="text-amber-300 font-mono">INSERT INTO processed_events (event_id) VALUES (?) ON CONFLICT (event_id) DO NOTHING</code>) executed within the exact same database transaction as the entity mutation. If Redis evicts early or crashes, the database unique constraint guarantees absolute correctness.</li>
          </ul>
        </div>"""

if ch3_old_theory in html:
    html = html.replace(ch3_old_theory, ch3_new_theory)
    print("Replaced Chapter 3 Theory.")
else:
    print("Warning: Chapter 3 old theory not matched exactly.")

# =========================================================================
# ENRICHED CHAPTER 3 CODE
# =========================================================================
ch3_old_code = """        <div id="ch3-content-code" class="tab-content hidden space-y-4 text-sm text-slate-300">
          <div class="code-block" id="code-ch3">
<pre><code class="text-slate-300"><span class="text-purple-400">@KafkaListener</span>(topics = <span class="text-emerald-300">"cell-config-events"</span>)
<span class="text-purple-400">public void</span> <span class="text-blue-400">onMessage</span>(CellConfigEvent event, Acknowledgment ack) {
    String dedupKey = <span class="text-emerald-300">"dedup:evt:"</span> + event.getEventId();
    <span class="text-slate-400">// Tier 1: Fast Redis Dedup Check</span>
    Boolean isNew = redisTemplate.opsForValue().setIfAbsent(dedupKey, <span class="text-emerald-300">"PENDING"</span>, Duration.ofHours(<span class="text-amber-300">24</span>));
    <span class="text-purple-400">if</span> (Boolean.FALSE.equals(isNew)) { ack.acknowledge(); <span class="text-purple-400">return</span>; }

    <span class="text-slate-400">// Tier 2: DB Commit with ON CONFLICT DO NOTHING</span>
    executeAtomicDatabaseTransaction(event);
    ack.acknowledge();
}</code></pre>
          </div>
        </div>"""

ch3_new_code = """        <div id="ch3-content-code" class="tab-content hidden space-y-4 text-sm text-slate-300">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">Java 21 Spring Boot Production 2-Tier Idempotent Consumer</span>
            <button onclick="copyCode('code-ch3')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded border border-slate-700 transition-all flex items-center gap-1">
              <span>📋</span> Copy Code
            </button>
          </div>
          <div class="code-block" id="code-ch3">
<pre><code class="text-slate-300"><span class="text-purple-400">@Service</span>
<span class="text-purple-400">@Slf4j</span>
<span class="text-purple-400">public class</span> <span class="text-blue-400">CellReconfigurationConsumer</span> {

    <span class="text-purple-400">@Autowired private</span> StringRedisTemplate redisTemplate;
    <span class="text-purple-400">@Autowired private</span> ManagedObjectRepository moRepository;
    <span class="text-purple-400">@Autowired private</span> ProcessedEventRepository processedEventRepository;

    <span class="text-slate-400">// Manual Immediate ACK mode: Offset commits ONLY after successful business transaction</span>
    <span class="text-purple-400">@KafkaListener</span>(
        topics = <span class="text-emerald-300">"cell-reconfiguration-commands"</span>,
        groupId = <span class="text-emerald-300">"usm-provisioning-workers"</span>,
        containerFactory = <span class="text-emerald-300">"kafkaManualAckListenerContainerFactory"</span>
    )
    <span class="text-purple-400">public void</span> <span class="text-blue-400">onCellConfigMessage</span>(
            <span class="text-purple-400">@Payload</span> CellConfigCommand command,
            <span class="text-purple-400">@Header</span>(KafkaHeaders.RECEIVED_KEY) String networkElementId,
            Acknowledgment ack) {

        String dedupKey = <span class="text-emerald-300">"idemp:evt:"</span> + command.eventId();

        <span class="text-slate-400">// -------------------------------------------------------------</span>
        <span class="text-slate-400">// TIER 1: In-Memory Redis Fast Deduplication Check (Sub-millisecond)</span>
        <span class="text-slate-400">// -------------------------------------------------------------</span>
        Boolean isFirstArrival = redisTemplate.opsForValue()
                .setIfAbsent(dedupKey, <span class="text-emerald-300">"PROCESSING"</span>, Duration.ofHours(<span class="text-amber-300">24</span>));

        <span class="text-purple-400">if</span> (Boolean.FALSE.equals(isFirstArrival)) {
            log.warn(<span class="text-emerald-300">"Tier-1 Duplicate detected in Redis for Event: {}. Fast-path ACK and drop."</span>, command.eventId());
            ack.acknowledge(); <span class="text-slate-400">// Discard replay safely</span>
            <span class="text-purple-400">return</span>;
        }

        <span class="text-purple-400">try</span> {
            <span class="text-slate-400">// -------------------------------------------------------------</span>
            <span class="text-slate-400">// TIER 2: Atomic Execution within PostgreSQL Transaction</span>
            <span class="text-slate-400">// -------------------------------------------------------------</span>
            executeAtomicDatabaseTransaction(command);

            <span class="text-slate-400">// Mark completed in Redis</span>
            redisTemplate.opsForValue().set(dedupKey, <span class="text-emerald-300">"COMMITTED"</span>, Duration.ofHours(<span class="text-amber-300">24</span>));
            ack.acknowledge();

        } <span class="text-purple-400">catch</span> (DuplicateEventException ex) {
            log.info(<span class="text-emerald-300">"Tier-2 Duplicate detected in DB constraint: {}. Acknowledging offset."</span>, command.eventId());
            ack.acknowledge(); <span class="text-slate-400">// Idempotency guaranteed by DB uniqueness</span>
        } <span class="text-purple-400">catch</span> (Exception ex) {
            <span class="text-slate-400">// Evict transient Redis key so retries can re-attempt</span>
            redisTemplate.delete(dedupKey);
            log.error(<span class="text-emerald-300">"Processing failed for Event: {}. Bubbling to Spring Kafka ErrorHandler."</span>, command.eventId(), ex);
            <span class="text-purple-400">throw</span> ex; <span class="text-slate-400">// Triggers exponential backoff & DLT routing</span>
        }
    }

    <span class="text-purple-400">@Transactional</span>(isolation = Isolation.READ_COMMITTED, rollbackFor = Exception.<span class="text-purple-400">class</span>)
    <span class="text-purple-400">public void</span> <span class="text-blue-400">executeAtomicDatabaseTransaction</span>(CellConfigCommand cmd) {
        <span class="text-slate-400">// 1. Atomic insert into unique idempotency ledger table</span>
        <span class="text-purple-400">int</span> rows = processedEventRepository.insertIgnoreConflict(cmd.eventId(), Instant.now());
        <span class="text-purple-400">if</span> (rows == <span class="text-amber-300">0</span>) {
            <span class="text-purple-400">throw new</span> DuplicateEventException(<span class="text-emerald-300">"Event already recorded in PostgreSQL: "</span> + cmd.eventId());
        }

        <span class="text-slate-400">// 2. Apply business Managed Object mutation</span>
        moRepository.updateTransmitPower(cmd.cellId(), cmd.txPower(), cmd.fencingToken());
    }
}</code></pre>
          </div>
        </div>"""

if ch3_old_code in html:
    html = html.replace(ch3_old_code, ch3_new_code)
    print("Replaced Chapter 3 Code.")

# =========================================================================
# ENRICHED CHAPTER 5 CONTENT
# =========================================================================
ch5_old_theory = """        <div id="ch5-content-theory" class="tab-content space-y-4 text-sm text-slate-300">
          <h3 class="text-base font-bold text-white">The Memory-Bandwidth Bottleneck of LLM Inference</h3>
          <p>
            In autoregressive decoding (batch size 1), LLM token generation is <strong class="cloze">strictly memory-bandwidth bound</strong>, not arithmetic bound. Generating a single token requires reading every parameter from RAM into CPU caches.
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300">
            Inference Speed &asymp; Memory Bandwidth (GB/s) &divide; Model Footprint (GB)<br>
            • FP16 7B: 14GB &divide; 50 GB/s DDR4 = 3.5 tok/sec (Unusable).<br>
            • INT4 7B (GGUF): <span class="cloze">4.2GB &divide; 50 GB/s DDR4 = 12 tok/sec</span> (Fluid interactive speed!).
          </div>
        </div>"""

ch5_new_theory = """        <div id="ch5-content-theory" class="tab-content space-y-5 text-sm text-slate-300">
          <h3 class="text-base font-bold text-white">The Physics of Air-Gapped Zero-GPU LLM Inference</h3>
          <p>
            In carrier telecom data centers, network configurations and topology maps represent sovereign national infrastructure. 
            Regulatory compliance strictly forbids transmitting network state to external cloud LLM APIs (OpenAI, Anthropic, Gemini). 
            Furthermore, telecom edge management nodes run on commodity dual-socket Intel Xeon servers with <strong>zero dedicated GPUs</strong>.
          </p>

          <h4 class="text-sm font-bold text-white mt-2">The Memory-Bandwidth Bottleneck in Autoregressive Generation</h4>
          <p>
            A common misconception is that LLM token generation is compute-bound (FLOPs-bound). In training or large-batch serving, matrix-matrix multiplications ($GEMM$) dominate arithmetic intensity.
            However, during single-user interactive assistant generation (batch size = 1), generation operates as a <strong>matrix-vector multiplication ($GEMV$)</strong>.
            Every single token generated requires streaming <em>every single parameter in the model</em> from system RAM into CPU L3 caches and SIMD registers:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300">
            Theoretical Maximum Token Generation Speed Formula:<br>
            $$\\text{Tokens per Second} \\approx \\frac{\\text{Memory Bus Bandwidth (GB/s)}}{\\text{Total Model Footprint (GB)}}$$<br>
            Let's evaluate on a standard dual-channel DDR4 server (~50 GB/s memory bandwidth):<br>
            • FP16 (16-bit) Qwen2.5-7B: Footprint = 7 &times; 10^9 &times; 2 bytes &asymp; 14.0 GB.<br>
            &rarr; Speed = 50 GB/s &divide; 14.0 GB &asymp; <strong>3.5 tokens/sec</strong> (Sluggish, unusable for real-time user interaction).<br><br>
            • INT4 (4-bit Q4_K_M GGUF) Qwen2.5-7B: Footprint = 7 &times; 10^9 &times; 0.5 bytes + scales &asymp; 4.2 GB.<br>
            &rarr; Speed = 50 GB/s &divide; 4.2 GB &asymp; <strong>11.9 &asymp; 12.0 tokens/sec</strong> (Fluid, natural conversational speed!).
          </div>

          <h4 class="text-sm font-bold text-white mt-2">The Mathematics of Affine Quantization (GGUF Q4_K_M)</h4>
          <p>
            Affine quantization maps 16-bit continuous floating-point weights $w \\in [w_{\\min}, w_{\\max}]$ onto discrete 4-bit integer values $q \\in [0, 15]$:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-amber-300">
            Forward Quantization:<br>
            $$q = \\text{clamp}\\left(\\text{round}\\left(\\frac{w}{s}\\right) + z, \\ 0, \\ 2^b - 1\\right)$$<br>
            Scale Factor: $s = \\frac{w_{\\max} - w_{\\min}}{2^b - 1}, \\quad$ Zero-Point: $z = \\text{round}\\left(-\\frac{w_{\\min}}{s}\\right)$<br><br>
            Dequantization in CPU SIMD Registers during GEMV:<br>
            $$\\hat{w} = s \\cdot (q - z)$$
          </div>
          <p>
            In <code class="text-cyan-300 font-mono">llama.cpp</code>, AVX-512 vector registers process 16 separate 32-bit floats or 64 8-bit integers simultaneously in a single CPU cycle, completely bypassing GPU requirements.
          </p>

          <h4 class="text-sm font-bold text-white mt-2">The 3-Tier Resilient DOM Fallback Engine</h4>
          <p>
            Automating actions across 400+ Samsung USM screens via a Chrome extension failed using standard CSS selectors because enterprise Single Page Apps (Angular/React) dynamically obfuscate class names on every build (e.g. <code class="text-rose-400 font-mono">.btn_x829fa</code>).
            We engineered a resilient 3-tier fallback resolution array:
          </p>
          <ul class="list-disc pl-5 space-y-1.5 text-xs text-slate-300">
            <li><strong>Tier 1 (Semantic ARIA Attributes):</strong> Query by accessibility roles and labels (<code class="text-cyan-300 font-mono">[role="button"][aria-label="Save Sector"]</code>). Resilient to 100% of CSS restylings.</li>
            <li><strong>Tier 2 (XPath Normalized Text Matching):</strong> Query element by normalized inner text (<code class="text-cyan-300 font-mono">//*[self::button or self::a][contains(normalize-space(text()), "Save Sector")]</code>). Survives DOM hierarchy reshuffling.</li>
            <li><strong>Tier 3 (Relative Hierarchical Proximity):</strong> Traverse relative to stable adjacent labels or form field headers.</li>
          </ul>
        </div>"""

if ch5_old_theory in html:
    html = html.replace(ch5_old_theory, ch5_new_theory)
    print("Replaced Chapter 5 Theory.")

# =========================================================================
# ENRICHED CHAPTER 5 CODE
# =========================================================================
ch5_old_code = """        <div id="ch5-content-code" class="tab-content hidden space-y-4 text-sm text-slate-300">
          <div class="code-block" id="code-ch5">
<pre><code class="text-slate-300"><span class="text-slate-400"># Pinned to 4 physical cores to eliminate hyperthreading cache thrashing</span>
llm = Llama(model_path=<span class="text-emerald-300">"qwen2.5-7b-q4_k_m.gguf"</span>, n_ctx=<span class="text-amber-300">2048</span>, n_threads=<span class="text-amber-300">4</span>, use_mmap=<span class="text-purple-400">True</span>)</code></pre>
          </div>
        </div>"""

ch5_new_code = """        <div id="ch5-content-code" class="tab-content hidden space-y-4 text-sm text-slate-300">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-cyan-400">Python FastAPI Zero-GPU Edge Engine & Chrome Extension Content Script</span>
            <button onclick="copyCode('code-ch5')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded border border-slate-700 transition-all flex items-center gap-1">
              <span>📋</span> Copy Code
            </button>
          </div>
          <div class="code-block" id="code-ch5">
<pre><code class="text-slate-300"><span class="text-slate-400"># =====================================================================</span>
<span class="text-slate-400"># 1. Python FastAPI Edge RAG Backend (server/api.py)</span>
<span class="text-slate-400"># =====================================================================</span>
<span class="text-purple-400">from</span> fastapi <span class="text-purple-400">import</span> FastAPI, HTTPException
<span class="text-purple-400">from</span> pydantic <span class="text-purple-400">import</span> BaseModel
<span class="text-purple-400">from</span> llama_cpp <span class="text-purple-400">import</span> Llama
<span class="text-purple-400">import</span> chromadb
<span class="text-purple-400">import</span> os

app = FastAPI(title=<span class="text-emerald-300">"Samsung USM Edge AI Engine"</span>)

<span class="text-slate-400"># Pinned to 4 dedicated physical CPU cores to eliminate hyper-threading cache thrashing</span>
llm = Llama(
    model_path=<span class="text-emerald-300">"./models/qwen2.5-7b-instruct-q4_k_m.gguf"</span>,
    n_ctx=<span class="text-amber-300">2048</span>,
    n_threads=<span class="text-amber-300">4</span>,             <span class="text-slate-400"># 4 physical cores</span>
    n_batch=<span class="text-amber-300">512</span>,
    use_mmap=<span class="text-purple-400">True</span>,           <span class="text-slate-400"># Memory-mapped directly from OS page cache</span>
    verbose=<span class="text-purple-400">False</span>
)

<span class="text-slate-400"># Local ChromaDB Vector Store running all-MiniLM-L6-v2 ONNX embeddings</span>
chroma_client = chromadb.PersistentClient(path=<span class="text-emerald-300">"./chroma_db"</span>)
docs_collection = chroma_client.get_or_create_collection(
    name=<span class="text-emerald-300">"usm_telecom_manuals"</span>,
    metadata={<span class="text-emerald-300">"hnsw:space"</span>: <span class="text-emerald-300">"cosine"</span>}
)

<span class="text-purple-400">class</span> <span class="text-blue-400">QueryRequest</span>(BaseModel):
    query: str

<span class="text-purple-400">@app.post</span>(<span class="text-emerald-300">"/api/v1/assist"</span>)
<span class="text-purple-400">def</span> <span class="text-blue-400">assist_operator</span>(req: QueryRequest):
    <span class="text-slate-400"># 1. Retrieve top-2 relevant technical manual chunks with cosine similarity threshold</span>
    results = docs_collection.query(query_texts=[req.query], n_results=<span class="text-amber-300">2</span>)
    context_chunks = results[<span class="text-emerald-300">"documents"</span>][<span class="text-amber-300">0</span>] <span class="text-purple-400">if</span> results[<span class="text-emerald-300">"documents"</span>] <span class="text-purple-400">else</span> []
    context_str = <span class="text-emerald-300">"\n---\n"</span>.join(context_chunks)

    <span class="text-slate-400"># 2. Construct grounded intent-to-action prompt</span>
    prompt = f<span class="text-emerald-300">"""&lt;|im_start|&gt;system
You are Samsung USM Element Manager Assistant. Output valid JSON only with keys: 'explanation', 'target_action', and 'selectors'.
Context:
{context_str}
&lt;|im_end|&gt;
&lt;|im_start|&gt;user
{req.query}
&lt;|im_end|&gt;
&lt;|im_start|&gt;assistant
"""</span>
    output = llm(prompt, max_tokens=<span class="text-amber-300">256</span>, temperature=<span class="text-amber-300">0.1</span>, stop=[<span class="text-emerald-300">"&lt;|im_end|&gt;"</span>])
    <span class="text-purple-400">return</span> {<span class="text-emerald-300">"response"</span>: output[<span class="text-emerald-300">"choices"</span>][<span class="text-amber-300">0</span>][<span class="text-emerald-300">"text"</span>]}

<span class="text-slate-400">// =====================================================================</span>
<span class="text-slate-400">// 2. Chrome Extension 3-Tier Resilient Locator Engine (content.js)</span>
<span class="text-slate-400">// =====================================================================</span>
<span class="text-purple-400">function</span> <span class="text-blue-400">resolveResilientElement</span>(locatorPlan) {
    <span class="text-slate-400">// TIER 1: Semantic ARIA Accessibility Selectors</span>
    <span class="text-purple-400">if</span> (locatorPlan.ariaSelector) {
        <span class="text-purple-400">const</span> el = document.querySelector(locatorPlan.ariaSelector);
        <span class="text-purple-400">if</span> (el &amp;&amp; el.offsetParent !== <span class="text-purple-400">null</span>) <span class="text-purple-400">return</span> el;
    }

    <span class="text-slate-400">// TIER 2: XPath Normalized Text Matching</span>
    <span class="text-purple-400">if</span> (locatorPlan.targetText) {
        <span class="text-purple-400">const</span> xpath = <span class="text-emerald-300">`//*[self::button or self::a or self::span][contains(normalize-space(text()), '${locatorPlan.targetText}')]`</span>;
        <span class="text-purple-400">const</span> res = document.evaluate(xpath, document, <span class="text-purple-400">null</span>, XPathResult.FIRST_ORDERED_NODE_TYPE, <span class="text-purple-400">null</span>);
        <span class="text-purple-400">if</span> (res.singleNodeValue &amp;&amp; res.singleNodeValue.offsetParent !== <span class="text-purple-400">null</span>) {
            <span class="text-purple-400">return</span> res.singleNodeValue;
        }
    }

    <span class="text-slate-400">// TIER 3: Relative Hierarchical Proximity Fallback</span>
    <span class="text-purple-400">if</span> (locatorPlan.parentContainer &amp;&amp; locatorPlan.childTag) {
        <span class="text-purple-400">const</span> container = document.querySelector(locatorPlan.parentContainer);
        <span class="text-purple-400">if</span> (container) {
            <span class="text-purple-400">const</span> el = container.querySelector(locatorPlan.childTag);
            <span class="text-purple-400">if</span> (el &amp;&amp; el.offsetParent !== <span class="text-purple-400">null</span>) <span class="text-purple-400">return</span> el;
        }
    }

    <span class="text-purple-400">return null</span>;
}</code></pre>
          </div>
        </div>"""

if ch5_old_code in html:
    html = html.replace(ch5_old_code, ch5_new_code)
    print("Replaced Chapter 5 Code.")

# =========================================================================
# WRITE OUTPUT
# =========================================================================
with open(workspace_file, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated {workspace_file} (Bytes: {len(html)})")

shutil.copy2(workspace_file, brain_file)
print(f"Mirrored to {brain_file}")
