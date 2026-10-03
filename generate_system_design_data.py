# generate_system_design_data.py
# Generates comprehensive Google L6/L8 System Design Blueprints for Modules 1 to 7

import sys

content = '''# system_design_data.py
# Comprehensive Google L6/L8 System Design Blueprints for Modules 1 to 7
# Each blueprint follows the Google Principal System Design Interview framework:
# 1. Scope, Functional Requirements & Non-Functional SLAs
# 2. End-to-End Component Architecture & Microservices Topology
# 3. API Contracts & Protobuf Wire Schema Definitions
# 4. Storage Architecture, Data Modeling & Partitioning
# 5. End-to-End Packet & Request Flow (Step-by-step 8-stage lifecycle)
# 6. Failure Domains, Split-Brain & Disaster Recovery
# 7. Observability, SLIs/SLOs & Tail Latency Mitigation

SYSTEM_DESIGNS = {
    "ch1": {
        "title": "Design a Distributed Telemetry & Configuration Ingestion Pipeline (45k TPS)",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            
            <!-- SECTION 1: SCOPE, FUNCTIONAL & NON-FUNCTIONAL SLAS -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Non-Functional SLAs (Google L6/L8 Standards)
                </span>
                <span class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-mono text-[10px]">Tier-0 Critical Path</span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <span class="font-bold text-white block">Functional Requirements:</span>
                  <ul class="list-disc pl-4 space-y-1.5 text-slate-400">
                    <li><strong class="text-slate-200">High-Fanout Ingestion:</strong> Ingest real-time antenna tilt, transmit power, and cell state mutations from 20M nationwide 4G/5G cell sectors.</li>
                    <li><strong class="text-slate-200">Strict FIFO Ordering:</strong> Guarantee strict per-cell FIFO order (antenna tilt change #2 must never be processed before #1).</li>
                    <li><strong class="text-slate-200">Multi-Consumer Fan-Out:</strong> Asynchronously stream events to Billing (exact-once), Real-time Alarm Engine (&lt;100ms SLA), and Long-term Analytics Sink (S3/ClickHouse).</li>
                    <li><strong class="text-slate-200">Zero Ingestion Blocking:</strong> Ingress must never block or shed traffic during rolling deployments of downstream microservices.</li>
                  </ul>
                </div>
                <div class="space-y-2">
                  <span class="font-bold text-white block">Non-Functional SLAs & Budgets:</span>
                  <ul class="list-disc pl-4 space-y-1.5 text-slate-400">
                    <li><strong class="text-slate-200">Throughput:</strong> 45,000 TPS sustained peak during nationwide cell activation; burst capacity to 100,000 TPS.</li>
                    <li><strong class="text-slate-200">Latency Budget:</strong> p50 &lt; 5ms, p99 &lt; 42ms edge-to-broker ACK. Total end-to-end downstream processing p99 &lt; 200ms.</li>
                    <li><strong class="text-slate-200">Availability:</strong> 99.999% (Five Nines, &lt; 5.26 minutes annual downtime).</li>
                    <li><strong class="text-slate-200">Durability & Data Loss:</strong> RPO = 0 (Zero data loss allowed; all commits require <code class="text-cyan-300 font-mono">acks=all</code> with <code class="text-cyan-300 font-mono">min.insync.replicas=2</code>).</li>
                    <li><strong class="text-slate-200">Disaster Recovery:</strong> RTO &lt; 3 seconds on single broker crash; RTO &lt; 30 seconds on regional failover.</li>
                  </ul>
                </div>
              </div>

              <!-- Capacity Sizing Table -->
              <div class="mt-3 p-3 bg-slate-900/90 rounded-lg border border-slate-800 text-[11px] font-mono space-y-1">
                <span class="text-cyan-300 font-bold block mb-1 font-sans text-xs">Capacity Sizing & Hardware Derivations:</span>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-slate-300">
                  <div>• Payload Size: <strong class="text-white">1 KB avg</strong></div>
                  <div>• Ingress Bandwidth: <strong class="text-white">45 MB/s (360 Mbps)</strong></div>
                  <div>• Daily Ingestion: <strong class="text-white">11.6 TB / day (3x rep)</strong></div>
                  <div>• 7-Day Storage: <strong class="text-white">81.2 TB NVMe RAID-10</strong></div>
                </div>
              </div>
            </div>

            <!-- SECTION 2: COMPONENT TOPOLOGY -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>2.</span> High-Level Component Topology & Network Boundaries
              </span>
              <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] leading-relaxed text-slate-300 overflow-x-auto">
[Edge Cell Towers (20M Sectors)]
       │ (eCPRI / IPSec Tunnel / TLS 1.3)
       ▼
[Edge Envoy Load Balancer Fleet] ───► Token Bucket Rate Limiter & TLS Offload
       │ (HTTP/2 gRPC Stream)
       ▼
[Ingress Gateway Pods (Go / C++)] ───► Protobuf Validation & Murmur2 Key Partitioning
       │ (Zero-Copy Producer acks=all)
       ▼
[Distributed Ingestion Cluster (Kafka 3.6+ / KRaft Quorum)]
   ├── Broker 1 (Leader P0..P21, NVMe WAL, Linux PageCache dirty_ratio=5%)
   ├── Broker 2 (Leader P22..P43, PageCache Zero-Copy sendfile)
   ├── Broker 3 (Leader P44..P64, min.insync.replicas=2)
   ├── Broker 4..6 (Followers / Cross-AZ Replica Quorum)
       │
       ├──► [Cooperative Sticky Consumer Fleet (Spring Boot / Java 21 Loom)]
       │        └──► Lock-free Ring Buffer Ingestion ──► PostgreSQL / ScyllaDB
       ├──► [Real-Time CEP Engine (Flink)] ──► SLA Alarm Detection (&lt;100ms)
       └──► [Long-Term Cold Sink (Vector/Kafka Connect)] ──► ClickHouse / Parquet S3
              </div>
            </div>

            <!-- SECTION 3: API & PROTOBUF WIRE CONTRACT -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>3.</span> API Contracts & Binary Protobuf Schema
              </span>
              <div class="bg-slate-900 rounded-lg p-3 font-mono text-[11px] text-cyan-300 overflow-x-auto">
syntax = "proto3";
package telecom.telemetry.v1;

message IngestionRequest {
  string idempotency_key = 1;      // UUIDv4: deduplication window 24h
  string network_element_id = 2;    // Partition Key: e.g. "eNodeB-40912-Sector-3"
  int64 timestamp_ns = 3;           // Nanosecond timestamp at edge sensor
  uint64 sequence_number = 4;       // Monotonically increasing sequence per tower
  
  enum EventType {
    EVENT_TYPE_UNSPECIFIED = 0;
    ANTENNA_TILT_CHANGED = 1;
    TRANSMIT_POWER_DBM = 2;
    CARRIER_FREQUENCY_HOP = 3;
    ALARM_CRITICAL_HIGH_TEMP = 4;
  }
  EventType event_type = 5;
  bytes payload_wire_format = 6;    // Zero-copy binary payload (no JSON parsing!)
}

message IngestionResponse {
  enum StatusCode { SUCCESS = 0; DEGRADED = 1; RATE_LIMITED = 2; ERROR = 3; }
  StatusCode status = 1;
  int64 committed_offset = 2;
  int32 assigned_partition = 3;
}
              </div>
            </div>

            <!-- SECTION 4: STORAGE & PARTITIONING -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>4.</span> Storage Architecture, Partitioning & Linux I/O Physics
              </span>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
                <div class="p-3 bg-slate-900/80 rounded-lg space-y-1.5">
                  <strong class="text-white block">Partitioning & Ordering Invariant:</strong>
                  <p>Partitions are mapped via <code class="text-cyan-300 font-mono">hash(NetworkElement_ID) % 128</code>. By choosing the cell tower ID as the partition key, all mutations for a specific physical radio sector land in the exact same partition, enforcing strict linear order without global locks.</p>
                </div>
                <div class="p-3 bg-slate-900/80 rounded-lg space-y-1.5">
                  <strong class="text-white block">Zero-Copy PageCache Mechanics:</strong>
                  <p>Brokers write segment files sequentially (NVMe writes: 3,500 MB/s). Read requests from consumers use Linux <code class="text-cyan-300 font-mono">sendfile()</code>: data moves from PageCache to NIC DMA ring without copying into JVM heap, avoiding GC pauses completely.</p>
                </div>
              </div>
            </div>

            <!-- SECTION 5: STEP-BY-STEP DATA FLOW -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>5.</span> End-to-End Request Lifecycle (8-Stage Pipeline)
              </span>
              <div class="space-y-2 text-slate-300">
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">1</span>
                  <div><strong class="text-white">Edge Emission:</strong> Cell tower sensor captures antenna tilt change, encodes into binary Protobuf, and opens persistent HTTP/2 gRPC stream to Envoy ingress.</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">2</span>
                  <div><strong class="text-white">Ingress & Token Bucket Check:</strong> Envoy validates TLS 1.3 cert, checks token bucket rate limiter (max 2,500 req/s per cell cluster), and forwards to Gateway worker.</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">3</span>
                  <div><strong class="text-white">Murmur2 Partition Assignment:</strong> Ingress Gateway computes <code class="text-cyan-300 font-mono">murmur2(NetworkElement_ID) & 0x7FFFFFFF % 128</code> and batches record into produce accumulator.</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">4</span>
                  <div><strong class="text-white">Broker Append:</strong> Broker leader receives batch, appends directly to active log segment in OS PageCache, and emits write to follower ISR replicas.</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">5</span>
                  <div><strong class="text-white">Quorum Replicate & Commit:</strong> Follower in separate Availability Zone fetches data via zero-copy. Once replica ACK is received (<code class="text-cyan-300 font-mono">min.insync.replicas=2</code>), leader advances High Watermark (HW).</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">6</span>
                  <div><strong class="text-white">Client ACK:</strong> Broker returns success response with committed partition offset to producer (Latency: 4.8ms p50, 38ms p99).</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">7</span>
                  <div><strong class="text-white">Cooperative Consumer Consumption:</strong> Spring Boot consumer fleet polls batch. CooperativeStickyAssignor ensures 0-pause rebalance during pod rollouts.</div>
                </div>
                <div class="flex items-start gap-2.5">
                  <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">8</span>
                  <div><strong class="text-white">Virtual Thread Offload:</strong> Java 21 Loom virtual threads process database UPSERT off-heap. High-watermark offset committed asynchronously.</div>
                </div>
              </div>
            </div>

            <!-- SECTION 6: FAILURE MODES & DISASTER RECOVERY -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>6.</span> Failure Domains, Split-Brain & Disaster Recovery
              </span>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div class="p-3 bg-rose-950/20 border border-rose-900/40 rounded-lg space-y-1">
                  <strong class="text-rose-300 block font-bold">Broker Crash / Failover:</strong>
                  <p class="text-slate-400 text-[11px]">KRaft controller detects heartbeat timeout (&lt;3s), promotes in-sync replica (ISR) to new partition leader. Producer retries with exponential jitter; zero dropped records.</p>
                </div>
                <div class="p-3 bg-rose-950/20 border border-rose-900/40 rounded-lg space-y-1">
                  <strong class="text-rose-300 block font-bold">Consumer Rebalance Storm:</strong>
                  <p class="text-slate-400 text-[11px]">Mitigated by Cooperative Sticky Assignor. Only migrating partitions pause; remaining 95% of consumers continue streaming traffic without stutter.</p>
                </div>
                <div class="p-3 bg-rose-950/20 border border-rose-900/40 rounded-lg space-y-1">
                  <strong class="text-rose-300 block font-bold">OS PageCache Write Stall:</strong>
                  <p class="text-slate-400 text-[11px]">Linux default <code class="text-rose-200 font-mono">dirty_ratio=20%</code> causes synchronous blocking during write bursts. Tuned to <code class="text-cyan-300 font-mono">vm.dirty_background_ratio=5</code> to force continuous background flushes.</p>
                </div>
              </div>
            </div>

            <!-- SECTION 7: OBSERVABILITY & MITIGATION -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>7.</span> Observability, SLIs/SLOs & Tail Latency Mitigation
              </span>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
                <div class="space-y-1">
                  <strong class="text-white block">SLIs & Golden Signals:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400 text-[11px]">
                    <li><strong class="text-slate-200">Consumer Lag (Records):</strong> Alert threshold &gt; 5,000 records for &gt; 60 seconds.</li>
                    <li><strong class="text-slate-200">Under-Replicated Partitions (URP):</strong> PagerDuty trigger if URP &gt; 0 for &gt; 30 seconds.</li>
                    <li><strong class="text-slate-200">JVM GC Pause Time:</strong> Alert if STW pause &gt; 25ms (indicates heap leak).</li>
                  </ul>
                </div>
                <div class="space-y-1">
                  <strong class="text-white block">Tail Latency Mitigations:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400 text-[11px]">
                    <li><strong class="text-slate-200">TCP Corking & Socket Buffers:</strong> Tune <code class="text-cyan-300 font-mono">wmem_max=16MB</code> and <code class="text-cyan-300 font-mono">tcp_nodelay=true</code> to eliminate Nagle packet batching delays.</li>
                    <li><strong class="text-slate-200">Hedged Ingress Requests:</strong> If edge cell sees broker response latency &gt; 35ms, immediately emit parallel hedged request to secondary gateway.</li>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        """
    },
    
    "ch2": {
        "title": "Design a Distributed Concurrency Coordinator & Fencing Lock Service",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            
            <!-- SECTION 1: SCOPE & SLAS -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Non-Functional SLAs (Google L6/L8 Standards)
                </span>
                <span class="px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 font-mono text-[10px]">Tier-0 Data Integrity</span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <span class="font-bold text-white block">Functional Requirements:</span>
                  <ul class="list-disc pl-4 space-y-1.5 text-slate-400">
                    <li><strong class="text-slate-200">Distributed Mutual Exclusion:</strong> Ensure that exactly one worker pod mutates a given Managed Object ID (MO-ID) at any instant.</li>
                    <li><strong class="text-slate-200">Strictly Monotonic Fencing Tokens:</strong> Every lock grant generates an incrementing 64-bit integer token to defeat delayed network packets and JVM GC pauses.</li>
                    <li><strong class="text-slate-200">Automatic Dead-Lock Recovery:</strong> If a holding node crashes, the lease must expire safely within 10 seconds without corrupting state.</li>
                  </ul>
                </div>
                <div class="space-y-2">
                  <span class="font-bold text-white block">Non-Functional SLAs & Budgets:</span>
                  <ul class="list-disc pl-4 space-y-1.5 text-slate-400">
                    <li><strong class="text-slate-200">Throughput:</strong> 25,000 lock acquisitions/releases per second across 500 microservice pods.</li>
                    <li><strong class="text-slate-200">Lock Grant Latency:</strong> p50 &lt; 0.8ms, p99 &lt; 2.5ms (in-memory execution).</li>
                    <li><strong class="text-slate-200">Split-Brain Escape Rate:</strong> Exactly 0 incidents. Fencing token verification at downstream database layer is mathematically infallible.</li>
                    <li><strong class="text-slate-200">Availability:</strong> 99.999% across 3 Availability Zones.</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- SECTION 2: TOPOLOGY -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>2.</span> High-Level Component Topology
              </span>
              <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] leading-relaxed text-slate-300 overflow-x-auto">
[500 Kubernetes Worker Pods]
       │
       ├──► [Distributed Lock Client Library (C++ / Java SDK)]
       │        ├── Heartbeat Watchdog Thread (renews TTL every 3.3s)
       │        └── Monotonic Fencing Token Injector
       │
       ▼ (gRPC / Redis RESP3 Protocol over Mutual TLS)
[Distributed Lock Coordinator Cluster]
   ├── Node 1 (Raft Leader / Redis Shard Master, In-Memory Lease Table)
   ├── Node 2 (Raft Quorum Follower, AZ-1)
   ├── Node 3 (Raft Quorum Follower, AZ-2)
       │
       ▼ (Acquisition returns token e.g. token=1049281)
[Downstream Storage Mutation: PostgreSQL / CockroachDB]
   └── UPDATE cell_config 
          SET tx_power = 45.0, last_fencing_token = 1049281
        WHERE mo_id = 'cell-101' 
          AND last_fencing_token &lt; 1049281;  -- Enforces Fencing!
              </div>
            </div>

            <!-- SECTION 3: API & LUA CONTRACTS -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
              <span class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>3.</span> Atomic Coordinator Lua Scripts & Protobuf Contract
              </span>
              <div class="bg-slate-900 rounded-lg p-3 font-mono text-[11px] text-purple-300 overflow-x-auto">
-- ATOMIC ACQUISITION WITH MONOTONIC FENCING TOKEN
-- KEYS[1] = lock_key ("lock:mo:cell-101")
-- KEYS[2] = token_key ("token:mo:cell-101")
-- ARGV[1] = client_uuid ("pod-a-thread-14-uuid")
-- ARGV[2] = ttl_seconds (10)
if redis.call('set', KEYS[1], ARGV[1], 'NX', 'EX', ARGV[2]) then
    local fencing_token = redis.call('incr', KEYS[2])
    return {1, fencing_token}  -- SUCCESS: acquired, returns token
else
    return {0, 0}              -- FAILED: already held
end
              </div>
            </div>

            <!-- SECTION 4: FAILURE MODES & JEPSEN ANALYSIS -->
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>4.</span> The Martin Kleppmann Redlock Flaw & Downstream Fencing Defense
              </span>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
                <div class="p-3 bg-rose-950/20 border border-rose-900/40 rounded-lg space-y-1.5">
                  <strong class="text-rose-300 block font-bold">The Asynchronous Pause Hazard:</strong>
                  <p class="text-[11px] text-slate-400">Worker 1 acquires lock with 10s TTL. Worker 1 enters a 15-second Stop-The-World (STW) JVM Garbage Collection pause. Lock expires. Worker 2 acquires lock and updates DB. Worker 1 wakes up, unaware its lock expired, and blindly overwrites Worker 2's update!</p>
                </div>
                <div class="p-3 bg-emerald-950/20 border border-emerald-900/40 rounded-lg space-y-1.5">
                  <strong class="text-emerald-300 block font-bold">The Staff L8 Architectural Mitigation:</strong>
                  <p class="text-[11px] text-slate-400">Locks cannot guarantee mutual exclusion in asynchronous networks without downstream storage verification. Worker 1 has token=101; Worker 2 gets token=102. When Worker 1 wakes up, its SQL update fails because <code class="text-emerald-300 font-mono">last_fencing_token &lt; 101</code> evaluates to false!</p>
                </div>
              </div>
            </div>

          </div>
        """
    },

    "ch3": {
        "title": "Design a High-Throughput Batch Mediation Pipeline (50k TPS)",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Non-Functional SLAs (Batch Mediation)
                </span>
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono text-[10px]">Telecom Ingestion Engine</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong class="text-white block mb-1">Functional Scope:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li>Batch normalize, validate, and enrich 50,000 Call Detail Records (CDRs) per second.</li>
                    <li>Handle heterogeneous schemas from legacy ASN.1 BER, 3GPP Diameter, and JSON.</li>
                    <li>Implement transactional chunking with automatic dead-letter queue (DLQ) isolation.</li>
                  </ul>
                </div>
                <div>
                  <strong class="text-white block mb-1">Non-Functional SLAs:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li><strong>Throughput:</strong> 50,000 records/sec sustained across 16 worker pods.</li>
                    <li><strong>Memory Overhead:</strong> &lt; 1.5 GB JVM heap per worker by streaming ASN.1 streams off-heap.</li>
                    <li><strong>Failure Tolerance:</strong> Poison pill records isolate to DLQ in &lt; 1ms without rolling back the entire batch.</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">2. High-Performance Chunking Architecture</span>
              <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-slate-300 leading-relaxed overflow-x-auto">
[Raw Telecom CDR Stream / S3 Bucket]
       │ (Off-Heap Memory Mapped File Channel)
       ▼
[ASN.1 BER Parser (Zero-Copy Byte Pointer Slicing)]
       │ (Chunk Size: 2,500 records)
       ▼
[Java 21 Loom Virtual Thread Dispatcher] ──► 1,000 Concurrent Virtual Workers
       │
       ├── Worker 1..N ──► In-Memory Rating Engine (Local L3 Cache Hash Table)
       │
       ▼ (Batch JDBC Prepared Statement / COPY INTO)
[High-Performance Storage Sink: ScyllaDB / PostgreSQL Partition]
              </div>
            </div>
          </div>
        """
    },

    "ch4": {
        "title": "Design a Real-Time Hierarchical Charging Tree Engine (3GPP CTE)",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & 3GPP Technical Specifications
                </span>
                <span class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 font-mono text-[10px]">3GPP TS 32.299 / TS 29.512</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong class="text-white block mb-1">Functional Scope:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li>Evaluate multi-tier rating hierarchies: Subscriber Tier &rarr; Rating Group &rarr; Service ID &rarr; Tariff Table.</li>
                    <li>Handle Diameter Credit-Control-Request (CCR-Initial, CCR-Update, CCR-Terminate) with real-time balance reservations.</li>
                    <li>Perform dynamic fallback to alternate rating trees when quota units are exhausted.</li>
                  </ul>
                </div>
                <div>
                  <strong class="text-white block mb-1">Non-Functional SLAs:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li><strong>Evaluation Latency:</strong> Tree traversal p99 &lt; 1.2ms (pure in-memory graph).</li>
                    <li><strong>Rule Space:</strong> Support 50,000 active enterprise charging rule branches.</li>
                    <li><strong>Concurrency:</strong> Lock-free reader evaluation via copy-on-write atomic pointer swapping.</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">2. Lock-Free Tree Memory Topology</span>
              <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-slate-300 leading-relaxed overflow-x-auto">
Root Node (Tenant ID: "Verizon-5G")
  ├── Service Node (Rating Group: 100 - Video Streaming)
  │     ├── Rule Branch A (Peak Hours 08:00-20:00 & QoS &gt; 5) &rarr; Tariff: $0.05 / MB
  │     └── Rule Branch B (Off-Peak Hours & QoS &lt;= 5) &rarr; Tariff: $0.01 / MB
  └── Service Node (Rating Group: 200 - VoNR HD Voice)
        └── Rule Branch C &rarr; Tariff: $0.002 / Second
              </div>
            </div>
          </div>
        """
    },

    "ch5": {
        "title": "Design a Globally Distributed Multi-Region Database (ScyllaDB / Spanner)",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Global Consistency Model
                </span>
                <span class="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 font-mono text-[10px]">Multi-DC Distributed Storage</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong class="text-white block mb-1">Functional Scope:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li>Active-Active multi-region deployment across 3 geographic zones (US-East, US-West, EU-Central).</li>
                    <li>Support low-latency reads and writes without waiting for speed-of-light cross-Atlantic round-trips.</li>
                    <li>Guarantee tunable consistency: <code class="text-indigo-300 font-mono">LOCAL_QUORUM</code> for financial ledger writes, <code class="text-indigo-300 font-mono">ONE</code> for metrics.</li>
                  </ul>
                </div>
                <div>
                  <strong class="text-white block mb-1">Non-Functional SLAs:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li><strong>Write Latency:</strong> p99 &lt; 4ms locally (async gossip replication to remote DCs).</li>
                    <li><strong>Partition Tolerance:</strong> Tolerate total undersea cable severance without taking down local reads/writes.</li>
                    <li><strong>Read Latency:</strong> p99 &lt; 2ms from local bloom filters and memory-mapped page cache.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        """
    },

    "ch6": {
        "title": "Design an Enterprise Distributed Rate Limiter & Concurrency Limiter",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Rate Limiting Mathematics
                </span>
                <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-mono text-[10px]">DDoS & Noisy Neighbor Guard</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong class="text-white block mb-1">Functional Scope:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li>Protect internal services from cascading collapses and noisy-neighbor tenant abuse.</li>
                    <li>Support multi-dimensional limits: IP address, API Key, Tenant ID, and Route Endpoint.</li>
                    <li>Implement Generic Cell Rate Algorithm (GCRA) and Sliding Window Log with sub-millisecond precision.</li>
                  </ul>
                </div>
                <div>
                  <strong class="text-white block mb-1">Non-Functional SLAs:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li><strong>Check Latency:</strong> Admission check p99 &lt; 0.5ms (local memory filter + async Redis sync).</li>
                    <li><strong>Throughput:</strong> 250,000 evaluations per second per ingress gateway instance.</li>
                    <li><strong>Fail-Open Policy:</strong> If the rate-limiter cluster fails, gracefully fail OPEN with metrics alert.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        """
    },

    "ch7": {
        "title": "Design a Zero-Downtime Database Migration & Traffic Replay Engine",
        "requirements": """
          <div class="space-y-6 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                <span class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>1.</span> System Scope & Migration Invariants
                </span>
                <span class="px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800 font-mono text-[10px]">Zero Customer Impact</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong class="text-white block mb-1">Functional Scope:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li>Migrate 500M live subscriber records from legacy Oracle RDBMS to modern ScyllaDB cluster.</li>
                    <li>Perform dual-writes with asynchronous shadow traffic replay and continuous reconciliation.</li>
                    <li>Enable 1-second instant rollback at any phase without data loss or corruption.</li>
                  </ul>
                </div>
                <div>
                  <strong class="text-white block mb-1">Non-Functional SLAs:</strong>
                  <ul class="list-disc pl-4 space-y-1 text-slate-400">
                    <li><strong>Customer Downtime:</strong> Exactly 0 seconds (Zero Downtime).</li>
                    <li><strong>Shadow Latency Impact:</strong> Production p99 latency must not degrade by &gt; 1.5ms during shadow writes.</li>
                    <li><strong>Data Divergence:</strong> Continuous reconciler verifies 100.000% parity across both databases before cutover.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        """
    }
}
'''

with open("d:/Antigravity/system_design_data.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated system_design_data.py successfully!")
