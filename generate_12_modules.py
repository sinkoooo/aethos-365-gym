# generate_12_modules.py
# Generates 12 comprehensive Google L6/L8 Staff Engineering Modules for modules_data.py

import json

modules = [
    # -------------------------------------------------------------------------
    # MODULE 1: Kafka Streaming & Zero-Copy Linux I/O
    # -------------------------------------------------------------------------
    {
        "id": "ch1",
        "num": 1,
        "track": "Track 1: High-Throughput Ingestion & OS Kernel Physics",
        "title": "Kafka Streaming & Zero-Copy Linux I/O",
        "subtitle": "45k TPS Ingestion, OS PageCache Physics, and Cooperative Sticky Rebalancing",
        "badge": "Module 1 • Ingestion Core",
        "domain": "High-Throughput Streaming & Linux I/O",
        "color": "cyan",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-cyan-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-cyan-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 1</span>
              <span class="text-[10px] bg-cyan-950 px-2 py-0.5 rounded text-cyan-300 border border-cyan-800">Verified Architecture</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-cyan-300 leading-relaxed overflow-x-auto">
[20M Cell Towers / Edge Probes]
       │ (eCPRI / IPSec / TLS 1.3)
       ▼
[Edge Envoy Ingress Gateways (48 Pods)] ──► Token Bucket Rate Limiting (2.5k req/s per tower)
       │ (HTTP/2 gRPC Stream)
       ▼
[Ingress Gateway Dispatchers (C++ / Go)] ──► Murmur2 Partition Hashing on NetworkElement_ID
       │ (Zero-Copy Producer acks=all, min.insync.replicas=2)
       ▼
[Kafka 3.6+ KRaft Cluster (6 Brokers, NVMe RAID-10, 128 Partitions)]
   ├── Leader P0..P21 (Linux PageCache dirty_background_ratio=5%, dirty_ratio=10%)
   ├── Leader P22..P43 (Zero-Copy sendfile() -> NIC DMA Ring)
   └── Followers (Cross-AZ Synchronous Quorum Replicas)
       │
       ├──► [Cooperative Sticky Consumer Fleet (Spring Boot / Java 21 Loom)]
       │        └──► Lock-free Ring Buffer Ingestion ──► ScyllaDB / PostgreSQL
       ├──► [Real-Time CEP Engine (Apache Flink)] ──► SLA Alarm Detection (&lt;100ms)
       └──► [Cold Storage Sink (Vector / S3)] ──► ClickHouse Analytics Engine
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: p99 &lt; 42ms edge-to-broker ACK | Zero JVM Heap allocation in transit</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch1')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Peak Throughput",
                "val": "45,000 TPS",
                "category": "Throughput",
                "derivation": "45,000 req/s * 1 KB avg payload = 45 MB/s (360 Mbps) wire ingress. Well within dual 25GbE bonded NIC capacity.",
                "soundbite": "We dimensioned our partition ring for 45,000 TPS at 1 KB average payload, delivering 45 MB/s wire ingress that easily saturates a 10 GbE NIC with zero context switches.",
                "interview_question": "Why 128 partitions for 45,000 TPS? Because each partition handles ~350 msg/s, perfectly matched to a single CPU core's L1 cache line processing budget."
            },
            {
                "label": "Ingress Latency",
                "val": "42 ms p99",
                "category": "Latency",
                "derivation": "15ms edge network RTT + 12ms mutual TLS 1.3 handshake resumption + 8ms broker PageCache append + 7ms ISR replication ACK.",
                "soundbite": "Our p99 latency SLA is 42ms edge-to-broker ACK, backed by non-blocking zero-copy page cache writes.",
                "interview_question": "What is the single biggest contributor to tail latency spikes? Kernel dirty page writeback freezes when dirty memory exceeds vm.dirty_ratio."
            },
            {
                "label": "Heap vs PageCache",
                "val": "4 GB vs 128 GB",
                "category": "Memory",
                "derivation": "Broker JVM heap is capped at 4 GB (metadata only). 128 GB server RAM is left entirely for OS PageCache, avoiding all Stop-The-World GC pauses.",
                "soundbite": "We cap broker JVM heap at 4 GB and dedicate 95% of host RAM to Linux PageCache. This eliminates young-gen GC churn and lets the kernel manage page eviction.",
                "interview_question": "Why not give Kafka a 64 GB JVM heap? Because JVM object overhead doubles data footprint and triggers multi-second GC pauses that cause broker zookeeper/KRaft heartbeats to drop."
            },
            {
                "label": "Rebalance SLA",
                "val": "< 400 ms",
                "category": "Reliability",
                "derivation": "CooperativeStickyAssignor revokes only moving partitions in 2 phases, eliminating the 14-second nationwide blackout of Eager rebalancing.",
                "soundbite": "Migrating to Cooperative Sticky rebalancing reduced our pod deployment rebalance pauses from 14 seconds to under 400 milliseconds.",
                "interview_question": "How does Cooperative Sticky assignor work? It performs incremental reassignment: untouched consumers continue processing without pausing."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 2: High-Performance Linux Networking (eBPF, XDP, DPDK)
    # -------------------------------------------------------------------------
    {
        "id": "ch2",
        "num": 2,
        "track": "Track 1: High-Throughput Ingestion & OS Kernel Physics",
        "title": "High-Performance Linux Networking & Kernel Bypass",
        "subtitle": "eBPF / XDP Packet Filters, DPDK Poll-Mode Drivers, and TCP BBR Congestion Control",
        "badge": "Module 2 • Kernel Bypass",
        "domain": "Low-Latency Kernel Networking",
        "color": "sky",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-sky-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-sky-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 2</span>
              <span class="text-[10px] bg-sky-950 px-2 py-0.5 rounded text-sky-300 border border-sky-800">Kernel Bypass</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-sky-300 leading-relaxed overflow-x-auto">
[Incoming 100 GbE Fiber Ingress (40M packets/sec)]
       │
       ▼
[NIC Hardware RX Ring Buffer (ethtool rx-ring 4096)]
       │
       ├──► [eBPF / XDP Driver Hook (Runs inside NIC Driver before sk_buff allocation!)]
       │        ├── Drop Malicious / DDOS Traffic in 15 nanoseconds (XDP_DROP)
       │        └── Forward Valid Packets via AF_XDP Zero-Copy Socket (XDP_REDIRECT)
       │
       ▼ (Bypasses entire Linux TCP/IP Kernel Stack!)
[User-Space Packet Parser (DPDK / io_uring Poll-Mode Driver)]
   ├── Core 0-3 (Pinned to NUMA Socket 0, 100% CPU polling, zero interrupt overhead)
   └── Lockless Circular Queue ──► Microservice Protocol Dispatcher
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Packet processing &lt; 850 nanoseconds | 0 kernel context switches</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch2')" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Packet Rate",
                "val": "14.88 Mpps",
                "category": "Throughput",
                "derivation": "Line-rate saturation for 64-byte packets on 10 GbE interface. Standard Linux kernel drops 70% at this rate; XDP processes at 100% line rate.",
                "soundbite": "By running eBPF at the XDP driver level, we filter packets before Linux kernel sk_buff allocation, sustaining 14.88 million packets per second on commodity hardware.",
                "interview_question": "What is the CPU cost of allocating an sk_buff in Linux? Approximately 250 nanoseconds per packet. XDP eliminates this entirely."
            },
            {
                "label": "Filter Latency",
                "val": "18 ns",
                "category": "Latency",
                "derivation": "eBPF bytecode JIT-compiled directly into native x86_64 instructions executed in L1 instruction cache.",
                "soundbite": "Malicious DDoS packets are dropped in 18 nanoseconds at the driver hook, completely insulating user-space applications.",
                "interview_question": "Why XDP instead of iptables? iptables requires walking Netfilter tables after sk_buff allocation, collapsing under 200k pps bursts."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 3: Distributed Concurrency & Monotonic Fencing Tokens
    # -------------------------------------------------------------------------
    {
        "id": "ch3",
        "num": 3,
        "track": "Track 2: Distributed Concurrency, Locking & Consensus",
        "title": "Distributed Concurrency & Fencing Tokens",
        "subtitle": "Atomic Redis Lua Scripts, Martin Kleppmann Redlock Flaw, and 64-bit Monotonic Version Fencing",
        "badge": "Module 3 • Concurrency Guard",
        "domain": "Distributed Locking & Consensus",
        "color": "purple",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-purple-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-purple-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 3</span>
              <span class="text-[10px] bg-purple-950 px-2 py-0.5 rounded text-purple-300 border border-purple-800">Fencing Defense</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-purple-300 leading-relaxed overflow-x-auto">
[500 Kubernetes Worker Pods]
       │ (Acquire Lock via Atomic Lua Script)
       ▼
[Redis Master / etcd Raft Coordinator Cluster]
   ├── Key: "lock:mo:cell-101" (TTL = 10s, Value = client_uuid)
   └── Token Counter: "token:mo:cell-101" (Atomically INCR -> e.g. token=1049281)
       │
       ▼ (Worker A gets Token 101, Worker B gets Token 102)
[Downstream Database Storage Engine (PostgreSQL / ScyllaDB)]
   └── Atomic Conditional Commit Barrier:
          UPDATE cell_config 
             SET tx_power = 45.0, last_token = 1049281
           WHERE mo_id = 'cell-101' 
             AND last_token &lt; 1049281;  -- Rejects Stale Zombie Writes!
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: 0 split-brain incidents across 500 pods | Mathematical mutual exclusion</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch3')" class="px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Grant Latency",
                "val": "< 1.8 ms",
                "category": "Latency",
                "derivation": "Single-shard Redis memory execution via atomic Lua script over persistent connection pool.",
                "soundbite": "Lock grants execute in under 1.8ms in Redis memory, issuing a 64-bit monotonic token in the same atomic transaction.",
                "interview_question": "Why is downstream database verification required? Because distributed locks cannot guarantee safety under asynchronous network delays or JVM GC pauses."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 4: Distributed Consensus Protocols (Raft, Multi-Paxos)
    # -------------------------------------------------------------------------
    {
        "id": "ch4",
        "num": 4,
        "track": "Track 2: Distributed Concurrency, Locking & Consensus",
        "title": "Distributed Consensus Protocols & Raft",
        "subtitle": "State Machine Replication, Leader Election, Log Matching Invariants, and FLP Impossibility",
        "badge": "Module 4 • Consensus Engine",
        "domain": "Distributed Consensus & Coordination",
        "color": "indigo",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-indigo-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-indigo-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 4</span>
              <span class="text-[10px] bg-indigo-950 px-2 py-0.5 rounded text-indigo-300 border border-indigo-800">Raft Consensus</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-indigo-300 leading-relaxed overflow-x-auto">
[Client Proposal Write Request]
       │
       ▼
[Node 1: Raft Cluster Leader (Term 2)] ──► Appends entry to uncommitted local WAL
       │
       ├── AppendEntries RPC ──► [Node 2: Follower (AZ-1)] ──► ACK
       ├── AppendEntries RPC ──► [Node 3: Follower (AZ-2)] ──► ACK
       ├── AppendEntries RPC ──► [Node 4: Follower (AZ-3)] ──► Partitioned / Slow
       └── AppendEntries RPC ──► [Node 5: Follower (AZ-3)] ──► Offline
       │
       ▼ (Majority Quorum Reached: 3/5 Nodes ACK)
[Leader Advances CommitIndex (High Watermark)]
       │
       ├──► Applies command to State Machine
       └──► Returns Success to Client (p99 &lt; 3.5ms)
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Linearizable reads/writes | Quorum tolerance: (N/2 + 1) majority</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch4')" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Quorum Commit",
                "val": "3 of 5 Nodes",
                "category": "Reliability",
                "derivation": "Majority rule N/2 + 1 guarantees overlapping node in any two successive majorities, preventing split-brain.",
                "soundbite": "In a 5-node cluster, we tolerate 2 simultaneous node crashes while maintaining linearizable commits.",
                "interview_question": "What is the FLP Impossibility Theorem? In an asynchronous network, no deterministic consensus protocol can guarantee both safety and liveness if even a single unannounced process crash is possible."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 5: High-Throughput Batch Mediation Pipeline
    # -------------------------------------------------------------------------
    {
        "id": "ch5",
        "num": 5,
        "track": "Track 3: High-Scale Batch, Mediation & Processing",
        "title": "High-Throughput Batch Mediation Pipeline",
        "subtitle": "Spring Batch, Java 21 Loom Virtual Threads, Off-Heap ASN.1 Parsing, and DLQ Isolation",
        "badge": "Module 5 • Batch Engine",
        "domain": "High-Throughput Batch & Mediation",
        "color": "emerald",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-emerald-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-emerald-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 5</span>
              <span class="text-[10px] bg-emerald-950 px-2 py-0.5 rounded text-emerald-300 border border-emerald-800">Batch Mediation</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-emerald-300 leading-relaxed overflow-x-auto">
[Raw 2GB ASN.1 CDR Files / S3 Data Lake]
       │
       ▼ (Memory Mapped FileChannel mmap - Zero Heap Copies)
[Zero-Copy ASN.1 Byte Pointer Slicer]
       │
       ▼ (Chunk Size = 2,500 records)
[Java 21 Loom Virtual Thread Pool (1,000 Concurrent Virtual Workers)]
   ├── Worker 1..N ──► In-Memory Normalization & Rating Lookups
   │        └──► Corrupt Record Detected? ──► Immediate Kafka DLQ Quarantine (&lt;1ms)
   │
   ▼ (Batched JDBC executeBatch() with Auto-Commit DISABLED)
[High-Scale Database Sink: ScyllaDB / PostgreSQL Partition]
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: 50,000 CDR/s sustained | &lt; 1.5 GB JVM Heap footprint</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch5')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Mediation Rate",
                "val": "50,000 CDR/s",
                "category": "Throughput",
                "derivation": "16 worker pods running 1,000 Virtual Threads chunking at 2,500 records per transaction.",
                "soundbite": "We sustained 50,000 normalized telecom CDRs per second while reducing JVM memory consumption by 90% via off-heap memory mapping.",
                "interview_question": "Why 2,500 records per chunk? It amortizes network round-trip costs across database inserts while keeping rollback blast radius minimal if a transient failure occurs."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 6: Stream Processing & Complex Event Processing (Flink)
    # -------------------------------------------------------------------------
    {
        "id": "ch6",
        "num": 6,
        "track": "Track 3: High-Scale Batch, Mediation & Processing",
        "title": "Stream Processing & Complex Event Processing",
        "subtitle": "Apache Flink State Backends, Event-Time Watermarks, Chandy-Lamport Checkpointing, and Exactly-Once",
        "badge": "Module 6 • Stream Engine",
        "domain": "Real-Time Stream & CEP Analytics",
        "color": "teal",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-teal-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-teal-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 6</span>
              <span class="text-[10px] bg-teal-950 px-2 py-0.5 rounded text-teal-300 border border-teal-800">Flink CEP</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-teal-300 leading-relaxed overflow-x-auto">
[Kafka Event Stream: 45k TPS Telemetry]
       │
       ▼ (Event-Time Watermark Generator: BoundedOutOfOrderness(5s))
[Flink Stateful Stream Processor]
   ├── Operator 1: KeyBy(tower_id) ──► Window: SlidingEventTimeWindow(10m, 1m)
   ├── State Backend: EmbeddedRocksDBStateBackend (Off-Heap NVMe SSD, zero GC)
   └── Asynchronous Checkpointing: Chandy-Lamport Distributed Barrier Algorithm
       │
       ▼ (Two-Phase Commit Sink: Kafka / ClickHouse)
[Downstream Real-Time Billing & Network Anomaly Detection (&lt;100ms SLA)]
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: End-to-end processing &lt; 100ms | Exactly-Once state guarantees</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch6')" class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Window Latency",
                "val": "< 85 ms",
                "category": "Latency",
                "derivation": "In-memory RocksDB state access with Bloom filters and block cache hits.",
                "soundbite": "Our Flink complex event processing engine evaluates sliding windows across 20M cell towers with sub-100ms end-to-end latency.",
                "interview_question": "How does Flink achieve Exactly-Once semantics? Through the Chandy-Lamport distributed checkpointing algorithm paired with a Two-Phase Commit (2PC) producer sink."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 7: Hierarchical Rule Engine & Quota Reservation (3GPP CTE)
    # -------------------------------------------------------------------------
    {
        "id": "ch7",
        "num": 7,
        "track": "Track 4: Real-Time Telecom & Rule Engines",
        "title": "Hierarchical Rule Engine & Quota Reservation",
        "subtitle": "3GPP TS 32.299 Charging Tree, Rete Algorithm, Dynamic Tariff Matching, and Lock-Free DAG Swapping",
        "badge": "Module 7 • Rule Engine",
        "domain": "Real-Time Rule Engines & Rating Algorithms",
        "color": "amber",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-amber-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-amber-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 7</span>
              <span class="text-[10px] bg-amber-950 px-2 py-0.5 rounded text-amber-300 border border-amber-800">3GPP CTE</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-amber-300 leading-relaxed overflow-x-auto">
[Diameter CCR-Initial / CCR-Update Packet]
       │
       ▼ (Sub-millisecond Rating Evaluation)
[Lock-Free In-Memory Radix Tree (Atomic Pointer Swap root_.load(acquire))]
   ├── Tenant Root Node ("Verizon-5G")
   │     ├── Rating Group: 100 (Video Streaming) ──► Peak Hour Match ──► $0.05 / MB
   │     └── Rating Group: 200 (VoNR HD Voice) ──► Off-Peak Match ──► $0.002 / Sec
   │
   ▼ (Atomic Credit Reservation)
[In-Memory Redis Token Bucket Cluster] ──► Decrement Quota Reserve (p99 &lt; 1.2ms)
   └── Return Diameter Credit-Control-Answer (CCA) with Granted Service Units (GSU)
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Traversal p99 &lt; 1.2ms | 0 database round-trips in hot path</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch7')" class="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Evaluation Latency",
                "val": "< 1.2 ms",
                "category": "Latency",
                "derivation": "In-memory Radix tree DAG traversal executed via lock-free atomic pointer reads.",
                "soundbite": "By compiling 3GPP charging rules into an in-memory prefix tree, readers evaluate tariffs in 1.2ms p99 without a single database round-trip.",
                "interview_question": "How do you handle live rule updates without stopping traffic? We compile a new cloned tree and swap the root pointer atomically using std::atomic<Node*> with release-acquire semantics."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 8: 5G Core Telecom Architecture (SBA, UPF, PCF)
    # -------------------------------------------------------------------------
    {
        "id": "ch8",
        "num": 8,
        "track": "Track 4: Real-Time Telecom & Rule Engines",
        "title": "5G Core Telecom Architecture & SBA",
        "subtitle": "5G Service-Based Architecture, User Plane Function (UPF), PCF / CHF Policy, and N4/N3 Protocols",
        "badge": "Module 8 • 5G Core",
        "domain": "5G Standalone Architecture",
        "color": "yellow",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-yellow-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-yellow-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 8</span>
              <span class="text-[10px] bg-yellow-950 px-2 py-0.5 rounded text-yellow-300 border border-yellow-800">5G SBA Core</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-yellow-300 leading-relaxed overflow-x-auto">
[gNodeB 5G Radio Base Station]
       │ (N3 GTP-U Tunnel - User Plane)
       ▼
[User Plane Function (UPF) - DPDK Fastpath] ──► Direct Hardware Forwarding
       │ (N4 PFCP Protocol)
       ▲
[Session Management Function (SMF)] ──► Service-Based Architecture (HTTP/2 JSON)
       ├── Nchf ──► [Charging Function (CHF)] ──► Real-Time Quota Allocation
       ├── Npcf ──► [Policy Control Function (PCF)] ──► QoS Bandwidth Enforcement
       └── Nudm ──► [Unified Data Management (UDM)] ──► Subscriber Authentication
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: User-plane forwarding latency &lt; 50 microseconds | Control plane 99.999%</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch8')" class="px-3 py-1.5 rounded-lg bg-yellow-600 hover:bg-yellow-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "User Plane Latency",
                "val": "< 50 µs",
                "category": "Latency",
                "derivation": "Hardware-accelerated DPDK packet processing bypassing kernel networking stack on N3 interface.",
                "soundbite": "In 5G Standalone architecture, control plane and user plane are strictly decoupled. Our UPF forwards user traffic in under 50 microseconds.",
                "interview_question": "What is the primary difference between 4G EPC and 5G Core? 4G used point-to-point Diameter protocols; 5G uses a cloud-native Service-Based Architecture (SBA) over HTTP/2 REST APIs."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 9: Globally Distributed Multi-Region Database (ScyllaDB)
    # -------------------------------------------------------------------------
    {
        "id": "ch9",
        "num": 9,
        "track": "Track 5: Global Storage, Partitioning & Caching",
        "title": "Globally Distributed Multi-Region Database",
        "subtitle": "ScyllaDB / Cassandra LSM-Trees, Seastar Thread-per-Core, Tunable Quorum, and Gossip",
        "badge": "Module 9 • Multi-DC Storage",
        "domain": "Distributed NoSQL & Multi-Region Storage",
        "color": "violet",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-violet-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-violet-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 9</span>
              <span class="text-[10px] bg-violet-950 px-2 py-0.5 rounded text-violet-300 border border-violet-800">Multi-DC Quorum</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-violet-300 leading-relaxed overflow-x-auto">
[Datacenter US-East (Virginia)]               [Datacenter EU-Central (Frankfurt)]
   ├── Coordinator Node (LOCAL_QUORUM)            ├── Read/Write Coordinator
   ├── Node 1 (Token Range 0..25)                 ├── Node 4 (Token Range 0..25)
   ├── Node 2 (Token Range 26..50)                ├── Node 5 (Token Range 26..50)
   └── Node 3 (Token Range 51..100)               └── Node 6 (Token Range 51..100)
       │                                              │
       └───► Background Gossip & Async Cross-DC Replication (Murmur3 Token Ring) ◄───┘
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Local write p99 &lt; 3.8ms | Complete tolerance of undersea cable cuts</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch9')" class="px-3 py-1.5 rounded-lg bg-violet-600 hover:bg-violet-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Local Write p99",
                "val": "< 3.8 ms",
                "category": "Latency",
                "derivation": "CommitLog append + MemTable write in local datacenter replicas only.",
                "soundbite": "By enforcing LOCAL_QUORUM consistency, writes commit to local NVMe SSDs in 3.8ms while replicating asynchronously across continents.",
                "interview_question": "Why avoid consistency level ALL across global regions? Because a single network glitch on a transatlantic fiber cut will take down writes worldwide."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 10: Planet-Scale Distributed SQL (Spanner & TrueTime)
    # -------------------------------------------------------------------------
    {
        "id": "ch10",
        "num": 10,
        "track": "Track 5: Global Storage, Partitioning & Caching",
        "title": "Planet-Scale Distributed SQL & TrueTime",
        "subtitle": "Google Spanner External Consistency, Atomic Clocks + GPS TrueTime API, and Multi-Paxos Tablets",
        "badge": "Module 10 • Spanner SQL",
        "domain": "Globally Consistent Distributed SQL",
        "color": "rose",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-rose-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-rose-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 10</span>
              <span class="text-[10px] bg-rose-950 px-2 py-0.5 rounded text-rose-300 border border-rose-800">Spanner TrueTime</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-rose-300 leading-relaxed overflow-x-auto">
[Global ACID Transaction: Transfer $500 US to EU]
       │
       ▼
[Spanner Zone Master (US-East)] ──► TrueTime.now() -> Interval: [t_earliest, t_latest]
       │ (Wait out clock uncertainty bound epsilon &lt; 7ms)
       ▼
[Paxos Group Leader for Tablet US-Accounts] ──► 2-Phase Commit Coordinator
       │
       ├── Paxos Replication ──► US-East Replica, US-Central Replica, US-West Replica
       └── Two-Phase Commit ──► Tablet EU-Accounts Paxos Group
       │
       ▼ (Linearizable external consistency guaranteed across the planet!)
[Transaction Committed with Globally Unique Monotonic TrueTime Timestamp]
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: External consistency (linearizability) across global datacenters</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch10')" class="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "TrueTime Bound",
                "val": "ε < 7 ms",
                "category": "Reliability",
                "derivation": "Drift bound provided by redundant GPS receivers and Rubidium atomic clocks in each Google datacenter.",
                "soundbite": "Spanner bounds clock drift uncertainty to under 7ms using hardware TrueTime. Waiting out epsilon allows lock-free read transactions across the globe.",
                "interview_question": "What is the difference between linearizability and serializability? Serializability means there is SOME valid sequential order. Linearizability means that order matches real-world wall-clock physical time."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 11: Enterprise Rate Limiting & Traffic Shaping
    # -------------------------------------------------------------------------
    {
        "id": "ch11",
        "num": 11,
        "track": "Track 6: Traffic Shaping, Resilience & Migrations",
        "title": "Enterprise Rate Limiting & Traffic Shaping",
        "subtitle": "Generic Cell Rate Algorithm (GCRA), Adaptive Concurrency Limits, and Hedged Requests",
        "badge": "Module 11 • Traffic Guard",
        "domain": "Resilience & Cascading Failure Defense",
        "color": "pink",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-pink-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-pink-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 11</span>
              <span class="text-[10px] bg-pink-950 px-2 py-0.5 rounded text-pink-300 border border-pink-800">GCRA Limiter</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-pink-300 leading-relaxed overflow-x-auto">
[Incoming API Ingress (250,000 QPS)]
       │
       ▼ (Sub-0.4ms Rate Check via Redis Lua Script)
[Generic Cell Rate Algorithm (GCRA / Leaky Bucket as a Meter)]
   ├── Check: New_TAT - Now &lt;= Burst_Offset
   ├── Passed? ──► Update TAT, Forward Request to Backend Microservice
   └── Exceeded? ──► Return HTTP 429 with Retry-After header
       │
       ▼ (Backend Protection)
[Client-Side Adaptive Concurrency Limiter (TCP Vegas Algorithm)]
   └── Dynamically adjusts in-flight concurrency limit based on measured RTT latency!
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Evaluation p99 &lt; 0.4ms | 100% Fail-Open policy on limiter outage</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch11')" class="px-3 py-1.5 rounded-lg bg-pink-600 hover:bg-pink-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Check Latency",
                "val": "< 0.4 ms",
                "category": "Latency",
                "derivation": "In-memory Redis single-shard atomic Lua script execution.",
                "soundbite": "We implement GCRA with atomic Redis Lua scripts, providing microsecond-precision rate shaping that eliminates window-boundary bursts.",
                "interview_question": "Why GCRA over fixed-window counters? Fixed-window counters permit a 2x burst across the window boundary, which frequently collapses downstream databases."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MODULE 12: Zero-Downtime Database Migration & Traffic Replay
    # -------------------------------------------------------------------------
    {
        "id": "ch12",
        "num": 12,
        "track": "Track 6: Traffic Shaping, Resilience & Migrations",
        "title": "Zero-Downtime Database Migration & Shadow Replay",
        "subtitle": "Dark Launching, Dual Writes with Monotonic Versions, Continuous Reconciliation, and 1s Rollback",
        "badge": "Module 12 • Migration Core",
        "domain": "Online Database Migration & Verification",
        "color": "teal",
        "reference_topology": """
          <div class="p-4 bg-slate-950 rounded-xl border border-teal-900/50 space-y-3 font-mono text-[11px] text-slate-300">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-teal-400 font-bold uppercase tracking-wider font-sans text-xs">Canonical Google Staff Reference Topology • Module 12</span>
              <span class="text-[10px] bg-teal-950 px-2 py-0.5 rounded text-teal-300 border border-teal-800">Zero Downtime</span>
            </div>
            <div class="p-3 bg-[#030712] rounded-lg border border-slate-800 text-teal-300 leading-relaxed overflow-x-auto">
Phase 1: Dual Writes (Sync to Oracle, Async to Kafka Shadow Queue)
Phase 2: Historical Backfill (500M records migrated via Spark/Flink)
Phase 3: Dark Traffic Replay & Continuous Parity Reconciler (14 days, 100% parity verified)
Phase 4: Instant 1-Second DNS Cutover (Zero Customer Downtime)
            </div>
            <div class="flex items-center justify-between pt-1 text-slate-400 font-sans text-xs">
              <span>SLA Invariant: Exactly 0 seconds customer downtime | 100.000% proven data parity</span>
              <button onclick="loadReferenceTopologyToWhiteboard('ch12')" class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                <span>🎨</span> Load into Whiteboard to Edit
              </button>
            </div>
          </div>
        """,
        "numbers_detailed": [
            {
                "label": "Customer Downtime",
                "val": "0 Seconds",
                "category": "Reliability",
                "derivation": "Online 4-phase shadow migration protocol.",
                "soundbite": "We migrated 500 million live subscriber profiles from Oracle to ScyllaDB with zero seconds of customer downtime.",
                "interview_question": "What is the primary danger in dual writes? Out-of-order retries overwriting fresh state. We enforce monotonic write versioning to guarantee idempotency."
            }
        ]
    }
]

with open("d:/Antigravity/modules_data.py", "w", encoding="utf-8") as f:
    f.write("# modules_data.py\n# Full 12 Google L6/L8 Staff Engineering Modules\n\nMODULES_LIST = " + repr(modules) + "\n")

print(f"Generated modules_data.py with all {len(modules)} modules successfully!")
