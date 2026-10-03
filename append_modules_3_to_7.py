# append_modules_3_to_7.py
# Generates complete, comprehensive modules 1 to 7 for modules_tech.py

import json

def get_all_modules():
    # Load ch1 and ch2 from previous build or define all 7 cleanly
    from build_full_modules_tech import ch1, ch2
    modules = [ch1, ch2]

    ch3 = {
        "id": "ch3",
        "num": 3,
        "title": "Batch Processing & Mediation Pipeline",
        "subtitle": "Spring Batch, Java 21 Loom Virtual Threads, and ASN.1 Zero-Copy Decoding",
        "badge": "Module 3 • Resume Bullet #3",
        "domain": "High-Throughput Batch Processing & Telecom Mediation",
        "color": "emerald",
        "theory": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-3">
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">High-Throughput Batch Mediation Physics</span>
              <p>
                Processing 50,000 Call Detail Records (CDRs) per second from raw telecom network probes involves handling massive binary ASN.1 files, normalizing heterogeneous schemas, and performing transactional persistence without saturating JVM memory or database connection pools.
              </p>
            </div>
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
              <h4 class="text-sm font-bold text-white">1. ASN.1 BER Binary Off-Heap Zero-Copy Decoding</h4>
              <p>
                Standard JVM ASN.1 decoders allocate objects for every Tag-Length-Value (TLV) field. For a 2 GB CDR file containing 10M records, this generates over 250M short-lived Java objects, triggering catastrophic Young Generation GC pauses. By utilizing memory-mapped buffers (<code class="text-emerald-300 font-mono">FileChannel.map()</code>) and decoding via off-heap byte pointer offsets, object allocation is reduced by 92%.
              </p>
            </div>
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
              <h4 class="text-sm font-bold text-white">2. Java 21 Project Loom Virtual Threads</h4>
              <p>
                Platform threads in Linux consume ~1 MB of stack memory and incur expensive kernel context switches (~1-2 microseconds). Java 21 Virtual Threads are lightweight user-mode threads scheduled by the JVM onto a small carrier thread pool (matching physical CPU cores). Over 10,000 concurrent Virtual Threads can execute I/O without exhausting operating system memory.
              </p>
            </div>
          </div>
        """,
        "project": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">Production Architecture Blueprint • Telecom CDR Mediation Engine</span>
              <p class="leading-relaxed">
                <strong>Scale:</strong> Processing 50,000 CDRs/sec sustained, peak 120,000 CDRs/sec.<br>
                <strong>Architecture:</strong> Spring Batch chunking with 2,500 records per transaction, offloaded to Project Loom virtual thread pools with non-blocking JDBC batching.
              </p>
            </div>
          </div>
        """,
        "code": """
          <div class="space-y-3">
            <div class="flex items-center gap-1 border-b border-slate-800 pb-2 text-xs">
              <button onclick="switchCodeTab('ch3', 'header')" id="ch3-btn-code-header" class="code-tab-btn active px-3 py-1 rounded bg-slate-800 text-emerald-400 border border-slate-700 font-mono font-semibold">CdrBatchConfig.java</button>
              <button onclick="switchCodeTab('ch3', 'impl')" id="ch3-btn-code-impl" class="code-tab-btn px-3 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 font-mono hover:text-white">ZeroCopyAsn1Parser.java</button>
            </div>

            <div id="ch3-file-header" class="code-file-view block font-mono text-[11px] leading-relaxed">
              <pre><code class="language-java">// ============================================================================
// FILE: CdrBatchConfig.java (Spring Batch + Java 21 Loom Virtual Threads)
// ============================================================================
@Configuration
@EnableBatchProcessing
public class CdrBatchConfig {
    @Bean
    public Step mediationStep(JobRepository jobRepo, PlatformTransactionManager txManager) {
        return new StepBuilder("cdr-mediation-step", jobRepo)
            .&lt;ByteBuffer, CdrNormalized&gt;chunk(2500, txManager) // Optimal chunk size
            .reader(new MemoryMappedCdrReader())
            .processor(new Asn1ZeroCopyProcessor())
            .writer(new ScyllaBatchWriter())
            .taskExecutor(Executors.newVirtualThreadPerTaskExecutor()) // Loom Virtual Threads
            .faultTolerant()
            .skip(CorruptRecordException.class).skipLimit(1000)
            .listener(new DeadLetterQueueSkipListener())
            .build();
    }
}</code></pre>
            </div>

            <div id="ch3-file-impl" class="code-file-view hidden font-mono text-[11px] leading-relaxed">
              <pre><code class="language-java">// ============================================================================
// FILE: ZeroCopyAsn1Parser.java (Off-Heap Byte Pointer Slicing)
// ============================================================================
public class ZeroCopyAsn1Parser {
    public static void parseRecord(MappedByteBuffer buffer, CdrRecord outRecord) {
        int tag = buffer.get() & 0xFF;
        int length = decodeLength(buffer);
        int valueOffset = buffer.position();
        
        // Zero-copy extraction: read directly without creating intermediate byte arrays
        outRecord.msisdn = buffer.getLong(valueOffset);
        outRecord.durationSec = buffer.getInt(valueOffset + 8);
        buffer.position(valueOffset + length);
    }
}</code></pre>
            </div>
          </div>
        """,
        "pitch": """
          At Samsung, I architected the high-throughput batch mediation engine for telecom Call Detail Records (CDRs), processing 50,000 records per second. Standard batch frameworks fail due to memory blowups when parsing multi-gigabyte files and thread starvation during database batch inserts.

          We resolved this by replacing traditional object-based ASN.1 decoders with off-heap memory-mapped buffers and pointer arithmetic, slashing heap allocation by 92%. We paired this with Java 21 Project Loom virtual threads, allowing thousands of concurrent batch chunks to execute non-blocking database inserts without context-switch overhead, reducing daily mediation runtimes from 6 hours to under 45 minutes.
        """,
        "traps": [
            {
                "title": "The Poison Pill Batch Rollback Death Loop",
                "scenario": "Interviewer: 'A batch file contains 100,000 records processed in chunks of 2,500. Record #4,821 has a corrupt format. The batch job retries infinitely and never finishes. How do you design fault tolerance?'",
                "junior_fallacy": "Candidates suggest wrapping each individual record in its own try/catch and single-row database commit, destroying batch throughput.",
                "root_cause": "When a corrupt record throws an unhandled exception inside a 2,500-record chunk, the entire database transaction rolls back. On retry, the worker hits the exact same record, creating an infinite rollback loop.",
                "l8_mitigation": "Configure Spring Batch fault tolerance with a SkipPolicy. When a corrupt record is detected, isolate the corrupt record to a Kafka Dead Letter Queue (DLQ) with error metadata, commit the remaining 2,499 valid records, and trigger Prometheus alerts.",
                "defense_script": "This is the poison pill chunk rollback hazard. In high-throughput batch engines, we never commit record-by-record due to network round trips. We use chunk transactions paired with a SkipListener that quarantines malformed records to a Dead Letter Queue while committing valid records atomically."
            },
            {
                "title": "Database Connection Pool Starvation Under Virtual Threads",
                "scenario": "Interviewer: 'You upgrade to Java 21 Virtual Threads and spawn 10,000 concurrent workers for batch processing. The database crashes immediately. Why?'",
                "junior_fallacy": "Candidates assume Virtual Threads automatically scale database connections.",
                "root_cause": "Virtual Threads make thread creation practically free, but database connections are physically bounded by database CPU, memory, and lock contention. 10,000 virtual threads concurrently opening database connections will exhaust HikariCP and crash the database with connection refused errors.",
                "l8_mitigation": "Decouple virtual thread concurrency from database connection limits using a bounded Semaphore (e.g. max 64 concurrent database operations) or a dedicated database connection queue.",
                "defense_script": "Virtual threads eliminate thread overhead, but they do not eliminate downstream resource bounds. I would decouple virtual thread dispatch from database access by throttling DB calls with a bounded Semaphore matching the database connection pool size."
            }
        ]
    }
    modules.append(ch3)

    ch4 = {
        "id": "ch4",
        "num": 4,
        "title": "Hierarchical Rule Engine & Quota Reservation",
        "subtitle": "3GPP TS 32.299 Charging Tree, Rete Algorithm, and Lock-Free Pointer Swapping",
        "badge": "Module 4 • Resume Bullet #4",
        "domain": "Real-Time Rule Engines & Rating Algorithms",
        "color": "amber",
        "theory": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-amber-950/20 border border-amber-900/40 rounded-xl space-y-3">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">3GPP Telecom Rating Physics</span>
              <p>
                In 4G/5G telecommunications (3GPP TS 32.299), every packet or voice call requires sub-millisecond credit rating and quota reservation via Diameter Credit-Control-Request (CCR) messages. Evaluating multi-tiered rule hierarchies at 50,000 TPS requires lock-free in-memory DAG evaluation.
              </p>
            </div>
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
              <h4 class="text-sm font-bold text-white">1. Lock-Free Atomic Pointer Swapping</h4>
              <p>
                Rule modifications occur continuously while traffic is active. Traditional mutex locking creates severe reader contention. By compiling rules into an immutable prefix tree (Radix DAG) and publishing updates via a single 64-bit atomic CAS pointer swap (<code class="text-amber-300 font-mono">std::atomic&lt;Node*&gt;</code>), reader threads evaluate rules with zero locks and zero latency spikes.
              </p>
            </div>
          </div>
        """,
        "project": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-amber-950/20 border border-amber-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">Production Architecture Blueprint • 3GPP CTE Charging Engine</span>
              <p class="leading-relaxed">
                <strong>Scale:</strong> 50,000 charging evaluations per second, p99 latency &lt; 1.2ms.<br>
                <strong>Outcome:</strong> Replaced recursive SQL CTE evaluation with in-memory lock-free Directed Acyclic Graphs, cutting rating latency by 90%.
              </p>
            </div>
          </div>
        """,
        "code": """
          <div class="space-y-3">
            <div class="flex items-center gap-1 border-b border-slate-800 pb-2 text-xs">
              <button onclick="switchCodeTab('ch4', 'header')" id="ch4-btn-code-header" class="code-tab-btn active px-3 py-1 rounded bg-slate-800 text-amber-400 border border-slate-700 font-mono font-semibold">ChargingTree.hpp</button>
            </div>
            <div id="ch4-file-header" class="code-file-view block font-mono text-[11px] leading-relaxed">
              <pre><code class="language-cpp">// ============================================================================
// FILE: ChargingTree.hpp (Lock-Free Prefix Tree Rule Evaluator)
// ============================================================================
#pragma once
#include &lt;atomic&gt;
#include &lt;string&gt;
#include &lt;memory&gt;

struct RuleNode {
    uint32_t rating_group;
    uint32_t service_id;
    double tariff_rate;
    RuleNode* next_branch;
};

class ChargingTreeEvaluator {
public:
    double evaluate_tariff(uint32_t group, uint32_t service) {
        RuleNode* root = root_.load(std::memory_order_acquire); // Lock-free read
        while (root) {
            if (root-&gt;rating_group == group && root-&gt;service_id == service) {
                return root-&gt;tariff_rate;
            }
            root = root-&gt;next_branch;
        }
        return 0.05; // Fallback default tariff
    }

    void publish_new_rules(RuleNode* new_root) {
        root_.store(new_root, std::memory_order_release); // Atomic publication
    }

private:
    std::atomic&lt;RuleNode*&gt; root_{nullptr};
};</code></pre>
            </div>
          </div>
        """,
        "pitch": """
          In 5G telecom networks, every data session must be rated and credited in real time under 2ms SLAs. At Samsung, we encountered massive database lock contention when querying hierarchical rating trees via recursive SQL CTEs.

          I re-architected the charging engine by compiling rating rules into an immutable in-memory Directed Acyclic Graph evaluated via lock-free atomic pointer swapping. Reader threads traverse rating paths with zero locks in under 1.2ms p99, while rule catalog updates publish atomically without taking down active data sessions, reducing evaluation latencies by 90%.
        """,
        "traps": [
            {
                "title": "The Memory Leak in Atomic Pointer Swapping (ABA & Reclamation)",
                "scenario": "Interviewer: 'You swap the rule tree pointer atomically using std::atomic. When do you free the memory of the old tree that was replaced?'",
                "junior_fallacy": "Candidates say 'Immediately delete the old pointer after swapping.'",
                "root_cause": "Deleting the old tree immediately causes catastrophic segmentation faults! Reader threads that loaded the old pointer right before the swap are still actively traversing its nodes in memory.",
                "l8_mitigation": "Use Epoch-Based Reclamation (EBR) or Read-Copy-Update (RCU). The old memory is only freed once all threads that started before the swap have completed their read epoch.",
                "defense_script": "Immediate deletion causes use-after-free crashes for concurrent readers. We employ Epoch-Based Reclamation (EBR) or Hazard Pointers: old tree versions are queued and only reclaimed once the thread epoch counter advances past all concurrent reader lifetimes."
            }
        ]
    }
    modules.append(ch4)

    ch5 = {
        "id": "ch5",
        "num": 5,
        "title": "Globally Distributed Multi-Region Database",
        "subtitle": "ScyllaDB / Cassandra LSM-Trees, Tunable Quorum, and Thread-per-Core Seastar",
        "badge": "Module 5 • Resume Bullet #5",
        "domain": "Distributed NoSQL & Multi-Region Storage",
        "color": "indigo",
        "theory": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-indigo-950/20 border border-indigo-900/40 rounded-xl space-y-3">
              <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider block">Multi-Region Distributed Database Physics</span>
              <p>
                Synchronous multi-region ACID transactions across transoceanic distances violate the speed of light (~80ms RTT between New York and London). ScyllaDB and Cassandra achieve sub-4ms writes by utilizing Log-Structured Merge (LSM) trees and tunable quorum consistency (LOCAL_QUORUM).
              </p>
            </div>
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
              <h4 class="text-sm font-bold text-white">1. LSM Tree Storage Mechanics (MemTable & SSTables)</h4>
              <p>
                Writes append to an on-disk CommitLog sequentially, then write to an in-memory MemTable (SkipList). Writes return immediately without seeking disk. When the MemTable fills, it flushes to an immutable Sorted String Table (SSTable) on disk. Background compaction merges SSTables and purges tombstones.
              </p>
            </div>
          </div>
        """,
        "project": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-indigo-950/20 border border-indigo-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider block">Production Architecture Blueprint • Multi-Region ScyllaDB Cluster</span>
              <p class="leading-relaxed">
                <strong>Scale:</strong> 100M managed objects replicated across US-East, US-West, and EU-Central with LOCAL_QUORUM consistency.
              </p>
            </div>
          </div>
        """,
        "code": """
          <div class="space-y-3">
            <div class="flex items-center gap-1 border-b border-slate-800 pb-2 text-xs">
              <button onclick="switchCodeTab('ch5', 'header')" id="ch5-btn-code-header" class="code-tab-btn active px-3 py-1 rounded bg-slate-800 text-indigo-400 border border-slate-700 font-mono font-semibold">schema.cql</button>
            </div>
            <div id="ch5-file-header" class="code-file-view block font-mono text-[11px] leading-relaxed">
              <pre><code class="language-sql">-- ============================================================================
-- FILE: schema.cql (ScyllaDB Multi-Region Keyspace & Table)
-- ============================================================================
CREATE KEYSPACE telecom_telemetry
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'us-east': 3,
    'us-west': 3,
    'eu-central': 3
};

CREATE TABLE telecom_telemetry.cell_metrics (
    tower_id text,
    sector_id int,
    bucket_hour timestamp,
    event_timestamp timestamp,
    antenna_tilt double,
    tx_power double,
    PRIMARY KEY ((tower_id, bucket_hour), sector_id, event_timestamp)
) WITH CLUSTERING ORDER BY (sector_id ASC, event_timestamp DESC)
AND compaction = {'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS'};</code></pre>
            </div>
          </div>
        """,
        "pitch": """
          In building multi-region telecom management systems, enforcing synchronous global ACID transactions creates severe latency degradation due to transoceanic latency. I architected our storage layer on ScyllaDB utilizing NetworkTopologyStrategy across 3 geographic regions.

          By enforcing LOCAL_QUORUM consistency, writes commit to local NVMe CommitLogs and MemTables in under 3.8ms p99, while background gossip protocols replicate state asynchronously across continents. During an undersea fiber severance, our cluster operated with 100% availability and zero customer impact.
        """,
        "traps": [
            {
                "title": "The Tombstone Read Latency Explosion",
                "scenario": "Interviewer: 'Your Cassandra/ScyllaDB cluster has 4ms write latency, but read latency suddenly explodes to 15,000ms on specific customer keys. Why?'",
                "junior_fallacy": "Candidates assume missing database indices or hardware degradation.",
                "root_cause": "In LSM databases, DELETE statements do not erase data immediately; they append a 'Tombstone' marker. If an application executes bulk deletions, subsequent reads must scan and discard thousands of tombstones across SSTables, triggering tombstone warning thresholds and read timeouts.",
                "l8_mitigation": "1) Lower gc_grace_seconds for write-heavy ephemeral data. 2) Avoid mass individual row deletions; delete by partition or use Time-To-Live (TTL). 3) Schedule proactive major compactions.",
                "defense_script": "This is tombstone accumulation in LSM SSTables. Deletions create tombstone markers that must be scanned until compaction purges them. I would inspect tombstone_warn_threshold metrics, transition bulk deletions to partition-level drops, and tune gc_grace_seconds."
            }
        ]
    }
    modules.append(ch5)

    ch6 = {
        "id": "ch6",
        "num": 6,
        "title": "Enterprise Rate Limiting & Concurrency Control",
        "subtitle": "Generic Cell Rate Algorithm (GCRA), Sliding Window Log, and Hedged Requests",
        "badge": "Module 6 • Resume Bullet #6",
        "domain": "Traffic Shaping & Resilience",
        "color": "rose",
        "theory": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-3">
              <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block">Traffic Shaping Mathematics</span>
              <p>
                Fixed-window rate limiters permit 2x burst limits across window boundaries. The Generic Cell Rate Algorithm (GCRA / Leaky Bucket as a Meter) eliminates boundary bursts by calculating Theoretical Arrival Times (TAT) with sub-millisecond precision.
              </p>
            </div>
          </div>
        """,
        "project": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block">Production Architecture Blueprint • Distributed Envoy Rate Limiter</span>
              <p class="leading-relaxed">
                <strong>Scale:</strong> Protecting internal microservices across 250,000 QPS with sub-0.5ms evaluation latency and fail-open resilience.
              </p>
            </div>
          </div>
        """,
        "code": """
          <div class="space-y-3">
            <div class="flex items-center gap-1 border-b border-slate-800 pb-2 text-xs">
              <button onclick="switchCodeTab('ch6', 'header')" id="ch6-btn-code-header" class="code-tab-btn active px-3 py-1 rounded bg-slate-800 text-rose-400 border border-slate-700 font-mono font-semibold">gcra_limiter.lua</button>
            </div>
            <div id="ch6-file-header" class="code-file-view block font-mono text-[11px] leading-relaxed">
              <pre><code class="language-lua">-- ============================================================================
-- FILE: gcra_limiter.lua (Generic Cell Rate Algorithm)
-- ============================================================================
local key = KEYS[1]
local now = tonumber(ARGV[1])
local emission_interval = tonumber(ARGV[2]) -- e.g. 10000 microseconds (100 req/sec)
local burst_offset = tonumber(ARGV[3])      -- e.g. 50000 microseconds (5 bursts)

local tat = tonumber(redis.call('get', key)) or now
local new_tat = math.max(now, tat) + emission_interval

if new_tat - now <= burst_offset then
    redis.call('set', key, new_tat, 'PX', math.ceil((new_tat - now) / 1000) + 1000)
    return 1 -- ALLOWED
else
    return 0 -- RATE LIMITED (429)
end</code></pre>
            </div>
          </div>
        """,
        "pitch": """
          Protecting distributed microservices from cascading collapses requires intelligent rate shaping, not naive fixed-window counters that allow double-burst traffic spikes. I designed our enterprise gateway rate-limiting tier using the Generic Cell Rate Algorithm (GCRA) executed via atomic Redis Lua scripts.

          By tracking theoretical arrival times, we eliminated boundary burst spikes, maintained sub-0.5ms check latency, and instituted a fail-open circuit breaker ensuring that internal caching blips never degrade client traffic.
        """,
        "traps": [
            {
                "title": "The Fail-Closed Gateway Outage",
                "scenario": "Interviewer: 'Your Redis rate limiter cluster experiences a 30-second network partition. What happens to incoming user traffic?'",
                "junior_fallacy": "Candidates state that traffic is safely blocked to protect backend servers.",
                "root_cause": "Failing closed converts a non-critical infrastructure cache outage into a 100% total outage for all paying end customers.",
                "l8_mitigation": "Design rate limiters with explicit Fail-Open semantics. If the limiter cluster times out or errors, bypass rate checking, emit a high-priority PagerDuty metric, and allow traffic to pass.",
                "defense_script": "Rate limiters must always fail open. An internal limiter outage must never take down user traffic. We wrap rate check RPCs in a circuit breaker that fails open after 25ms, alerting SREs while keeping services available."
            }
        ]
    }
    modules.append(ch6)

    ch7 = {
        "id": "ch7",
        "num": 7,
        "title": "Zero-Downtime Migration & Shadow Traffic",
        "subtitle": "Dark Traffic Replay, Continuous Parity Reconciliation, and Instant 1-Second Rollback",
        "badge": "Module 7 • Resume Bullet #7",
        "domain": "Online Database Migration & Verification",
        "color": "teal",
        "theory": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-teal-950/20 border border-teal-900/40 rounded-xl space-y-3">
              <span class="text-xs font-bold text-teal-400 uppercase tracking-wider block">Zero-Downtime Migration Physics</span>
              <p>
                Migrating petabyte-scale production databases live without downtime is a distributed consensus problem. The 4-phase migration pattern (Dual Writes &rarr; Historical Backfill &rarr; Shadow Verification &rarr; Live Cutover) guarantees zero data loss and sub-second rollback.
              </p>
            </div>
          </div>
        """,
        "project": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-teal-950/20 border border-teal-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-teal-400 uppercase tracking-wider block">Production Architecture Blueprint • Oracle to ScyllaDB Migration</span>
              <p class="leading-relaxed">
                <strong>Scale:</strong> Migrated 500M live subscriber profiles from Oracle RDBMS to ScyllaDB with 0 seconds of downtime and 100% data parity.
              </p>
            </div>
          </div>
        """,
        "code": """
          <div class="space-y-3">
            <div class="flex items-center gap-1 border-b border-slate-800 pb-2 text-xs">
              <button onclick="switchCodeTab('ch7', 'header')" id="ch7-btn-code-header" class="code-tab-btn active px-3 py-1 rounded bg-slate-800 text-teal-400 border border-slate-700 font-mono font-semibold">DualWriteService.java</button>
            </div>
            <div id="ch7-file-header" class="code-file-view block font-mono text-[11px] leading-relaxed">
              <pre><code class="language-java">// ============================================================================
// FILE: DualWriteService.java (Synchronous Primary + Asynchronous Shadow)
// ============================================================================
@Service
public class DualWriteService {
    public void saveSubscriber(Subscriber record) {
        // 1. Primary write is source of truth
        legacyOracleRepo.save(record);

        // 2. Async shadow write to Kafka with monotonic version
        kafkaTemplate.send("migration.shadow.topic", record.getId(), 
            new ShadowPayload(record, System.currentTimeMillis()));
    }
}</code></pre>
            </div>
          </div>
        """,
        "pitch": """
          In Tier-0 telecommunications, scheduling maintenance windows to migrate databases is unacceptable. I led the zero-downtime migration of 500M subscriber profiles from legacy Oracle databases to ScyllaDB.

          We executed a 4-phase rollout: establishing asynchronous dual writes with monotonic versioning, backfilling 10 years of historical data via distributed batch workers, and replaying production shadow traffic against both databases for 14 continuous days to prove 100.000% parity before executing a 1-second DNS cutover with zero downtime.
        """,
        "traps": [
            {
                "title": "The Stale Shadow Overwrite Race Condition",
                "scenario": "Interviewer: 'During dual-writes, an update at 10:00:00 fails over network and retries at 10:00:05. Meanwhile, a fresh update at 10:00:03 wrote successfully. The retry overwrites the fresh update. How do you prevent this?'",
                "junior_fallacy": "Junior candidates suggest serializing all requests globally through a single thread.",
                "root_cause": "Network retries arrive out of chronological order, allowing an older state to overwrite newer state on the shadow database.",
                "l8_mitigation": "Enforce monotonic version timestamps on every write. The shadow database update statement includes a conditional check: UPDATE ... WHERE version &lt; incoming_version.",
                "defense_script": "This is out-of-order shadow mutation. We enforce monotonic write versioning. Every write carries a monotonic timestamp, and the secondary database enforces conditional updates, rejecting any delayed retry with an older timestamp."
            }
        ]
    }
    modules.append(ch7)

    return modules

if __name__ == "__main__":
    mods = get_all_modules()
    with open("d:/Antigravity/modules_tech.py", "w", encoding="utf-8") as f:
        f.write("# modules_tech.py\n# Deep technical content for Modules 1 to 7 of NEXUS ARCHITECT platform\n\nMODULES = " + repr(mods) + "\n")
    print(f"Updated modules_tech.py with all {len(mods)} modules successfully!")
