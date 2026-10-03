# update_modules_data.py
import json
import detailed_topology_svgs

MODULES_DATA = [
    {
        "id": "ch1",
        "num": 1,
        "track": "Track 1: High-Throughput Ingestion & OS Kernel Physics",
        "title": "Kafka Streaming & Zero-Copy Linux I/O",
        "subtitle": "45k TPS Ingestion, OS PageCache Physics, and Cooperative Sticky Rebalancing",
        "badge": "Module 1 • Ingestion Core",
        "domain": "High-Throughput Streaming & Linux I/O",
        "color": "cyan",
        "numbers_detailed": [
            {
                "label": "Peak Throughput", "val": "45,000 TPS", "category": "Throughput",
                "derivation": "45,000 req/s * 1 KB avg payload = 45 MB/s (360 Mbps) wire ingress. Well within dual 25GbE bonded NIC capacity.",
                "soundbite": "We dimensioned our partition ring for 45,000 TPS at 1 KB average payload, delivering 45 MB/s wire ingress that easily saturates a 10 GbE NIC with zero context switches.",
                "interview_question": "Why 128 partitions for 45,000 TPS? Because each partition handles ~350 msg/s, perfectly matched to a single CPU core's L1 cache line processing budget."
            },
            {
                "label": "Ingress Latency", "val": "42 ms p99", "category": "Latency",
                "derivation": "15ms edge network RTT + 12ms mutual TLS 1.3 handshake resumption + 8ms broker PageCache append + 7ms ISR replication ACK.",
                "soundbite": "Our p99 latency SLA is 42ms edge-to-broker ACK, backed by non-blocking zero-copy page cache writes.",
                "interview_question": "What is the single biggest contributor to tail latency spikes? Kernel dirty page writeback freezes when dirty memory exceeds vm.dirty_ratio."
            },
            {
                "label": "Heap vs PageCache", "val": "4 GB vs 128 GB", "category": "Memory",
                "derivation": "Broker JVM heap is capped at 4 GB (metadata only). 128 GB server RAM is left entirely for OS PageCache, avoiding all Stop-The-World GC pauses.",
                "soundbite": "We cap broker JVM heap at 4 GB and dedicate 95% of host RAM to Linux PageCache. This eliminates young-gen GC churn and lets the kernel manage page eviction.",
                "interview_question": "Why not give Kafka a 64 GB JVM heap? Because JVM object overhead doubles data footprint and triggers multi-second GC pauses that cause broker zookeeper/KRaft heartbeats to drop."
            },
            {
                "label": "Rebalance SLA", "val": "< 400 ms", "category": "Reliability",
                "derivation": "CooperativeStickyAssignor revokes only moving partitions in 2 phases, eliminating the 14-second nationwide blackout of Eager rebalancing.",
                "soundbite": "Migrating to Cooperative Sticky rebalancing reduced our pod deployment rebalance pauses from 14 seconds to under 400 milliseconds.",
                "interview_question": "How does Cooperative Sticky assignor work? It performs incremental reassignment: untouched consumers continue processing without pausing."
            }
        ]
    },
    {
        "id": "ch2",
        "num": 2,
        "track": "Track 1: High-Throughput Ingestion & OS Kernel Physics",
        "title": "High-Performance Linux Networking & Kernel Bypass",
        "subtitle": "eBPF / XDP Packet Filters, DPDK Poll-Mode Drivers, and TCP BBR Congestion Control",
        "badge": "Module 2 • Kernel Bypass",
        "domain": "Low-Latency Kernel Networking",
        "color": "sky",
        "numbers_detailed": [
            {
                "label": "Packet Ingress Rate", "val": "14.88 Mpps", "category": "Throughput",
                "derivation": "Line-rate saturation for 64-byte minimum frames on a 10 GbE interface. Standard Linux kernel drops 70% at this rate; XDP processes at 100% line rate.",
                "soundbite": "By running eBPF at the XDP driver level, we filter packets before Linux kernel sk_buff allocation, sustaining 14.88 million packets per second on commodity hardware.",
                "interview_question": "What is the CPU cost of allocating an sk_buff in Linux? Approximately 250 nanoseconds per packet. XDP eliminates this entirely."
            },
            {
                "label": "Filter Decision Latency", "val": "18 ns", "category": "Latency",
                "derivation": "eBPF bytecode JIT-compiled directly into native x86_64 instructions executed directly within L1 instruction cache.",
                "soundbite": "Malicious DDoS packets are dropped in 18 nanoseconds at the driver hook, completely insulating user-space applications.",
                "interview_question": "Why XDP instead of iptables? iptables requires walking Netfilter tables after sk_buff allocation, collapsing under 200k pps bursts."
            },
            {
                "label": "NUMA Context Switches", "val": "0 Switches", "category": "Hardware",
                "derivation": "DPDK Poll-Mode Driver (PMD) runs pinned dedicated worker threads on isolated cores on Socket 0, eliminating hardware interrupts.",
                "soundbite": "We pin packet processing threads to NUMA-local CPU cores with 100% polling mode, achieving deterministic sub-microsecond processing with zero context switches.",
                "interview_question": "What happens if a thread accesses memory across NUMA nodes? Remote NUMA interconnect (QPI/UPI) latency adds 60-100ns and causes cross-bus cache thrashing."
            },
            {
                "label": "BBR Throughput Gain", "val": "4.2x vs Cubic", "category": "Throughput",
                "derivation": "TCP BBR models maximum bandwidth and minimum RTT independently, eliminating bufferbloat packet drops on lossy 5G links.",
                "soundbite": "Enabling TCP BBR yielded a 4.2x throughput improvement over lossy cellular networks by preventing queue bloat at bottleneck cell towers.",
                "interview_question": "Why does TCP Cubic collapse on shallow cellular buffers? Cubic assumes packet loss indicates congestion, cutting window by 50% even on random wireless signal fade."
            }
        ]
    },
    {
        "id": "ch3",
        "num": 3,
        "track": "Track 2: Distributed Concurrency, Locking & Consensus",
        "title": "Distributed Concurrency & Fencing Tokens",
        "subtitle": "Atomic Redis Lua Scripts, Martin Kleppmann Redlock Flaw, and 64-bit Monotonic Version Fencing",
        "badge": "Module 3 • Concurrency Guard",
        "domain": "Distributed Locking & Consensus",
        "color": "purple",
        "numbers_detailed": [
            {
                "label": "Lock Grant Latency", "val": "< 1.8 ms", "category": "Latency",
                "derivation": "Single-shard Redis memory execution via atomic Lua script over persistent TCP connection pool.",
                "soundbite": "Lock grants execute in under 1.8ms in Redis memory, issuing a 64-bit monotonic token in the same atomic transaction.",
                "interview_question": "Why is downstream database verification required? Because distributed locks cannot guarantee safety under asynchronous network delays or JVM GC pauses."
            },
            {
                "label": "Fencing Token Space", "val": "2^64 Monotonic", "category": "Scale",
                "derivation": "64-bit atomic integer counter per resource ID. At 100,000 acquisitions per second, the counter will not wrap for 5.8 million years.",
                "soundbite": "We protect against asynchronous zombie writes by attaching a strictly monotonic 64-bit fencing token to every lock grant and enforcing conditional updates at the storage engine.",
                "interview_question": "Why does Redlock fail Martin Kleppmann's critique? Because a node can experience a GC pause right after acquiring the lock; the lock expires, another worker acquires it, and both write concurrently."
            },
            {
                "label": "Lock Heartbeat Safety Margin", "val": "3x Lease Period", "category": "Reliability",
                "derivation": "Lock lease is 10s. Background watchdog thread extends lease every 3.3s. If 2 consecutive heartbeats fail, worker immediately aborts before expiration.",
                "soundbite": "Our watchdog heartbeat runs at 3x the lease frequency, guaranteeing safe abort before lock expiry if network partitions occur.",
                "interview_question": "What is the danger of setting lock TTL too high? If the worker process crashes, other workers are blocked for the full TTL duration."
            },
            {
                "label": "Storage Rejection Rate", "val": "100% of Zombies", "category": "Reliability",
                "derivation": "Conditional SQL: UPDATE tbl SET val=?, token=? WHERE id=? AND token < ?; zero stale overwrites possible mathematically.",
                "soundbite": "Even during network partitions and Stop-The-World GC pauses, our monotonic fencing barrier achieved 100% rejection of stale zombie writes.",
                "interview_question": "Can a zombie client still read stale data? Yes, read fencing requires read tokens or linearizable quorum reads."
            }
        ]
    },
    {
        "id": "ch4",
        "num": 4,
        "track": "Track 2: Distributed Concurrency, Locking & Consensus",
        "title": "Distributed Consensus Protocols & Raft",
        "subtitle": "State Machine Replication, Leader Election, Log Matching Invariants, and FLP Impossibility",
        "badge": "Module 4 • Consensus Engine",
        "domain": "Distributed Consensus & Coordination",
        "color": "indigo",
        "numbers_detailed": [
            {
                "label": "Quorum Tolerance", "val": "2 of 5 Failures", "category": "Reliability",
                "derivation": "Majority rule N/2 + 1: A 5-node cluster requires 3 nodes for quorum, tolerating 2 simultaneous node crashes with zero split-brain.",
                "soundbite": "In our 5-node Raft consensus cluster across 3 availability zones, we sustain 2 simultaneous node failures while maintaining strict linearizability.",
                "interview_question": "What is the FLP Impossibility Theorem? In an asynchronous network, no deterministic consensus protocol can guarantee both safety and liveness if even one unannounced node crash is possible."
            },
            {
                "label": "Commit Latency", "val": "3.5 ms p99", "category": "Latency",
                "derivation": "Cross-AZ network round-trip (1.2ms) + parallel NVMe fsync on Leader & 2 Followers (1.8ms) + state machine application (0.5ms).",
                "soundbite": "Raft log proposals commit in 3.5ms p99 because the leader only waits for the fastest quorum majority, masking slow tail followers.",
                "interview_question": "How does Raft handle a partitioned leader? The partitioned leader cannot achieve quorum ACKs for proposals; followers in the majority partition elect a new leader with a higher term."
            },
            {
                "label": "Leader Election Timeout", "val": "150-300 ms", "category": "Reliability",
                "derivation": "Randomized election timer avoids split votes when multiple followers detect leader heartbeat loss simultaneously.",
                "soundbite": "We configure randomized election timeouts between 150ms and 300ms, ensuring 99.8% of leader elections resolve in a single round.",
                "interview_question": "Why randomize election timeout? If all followers had identical timeouts, they would all declare candidacy simultaneously, splitting votes indefinitely."
            },
            {
                "label": "Log Compaction Snapshot", "val": "Every 50k Entries", "category": "Scale",
                "derivation": "Snapshots freeze state machine and prune committed WAL entries, preventing infinite disk growth and speeding up new node catch-up.",
                "soundbite": "We take asynchronous point-in-time state machine snapshots every 50,000 entries, bounding recovery replay time to under 800ms.",
                "interview_question": "How does a lagged follower catch up if the leader has already truncated the WAL? The leader sends an InstallSnapshot RPC containing the full state machine image."
            }
        ]
    },
    {
        "id": "ch5",
        "num": 5,
        "track": "Track 3: High-Scale Batch, Mediation & Processing",
        "title": "High-Throughput Batch Mediation Pipeline",
        "subtitle": "Spring Batch, Java 21 Loom Virtual Threads, Off-Heap ASN.1 Parsing, and DLQ Isolation",
        "badge": "Module 5 • Batch Engine",
        "domain": "High-Throughput Batch & Mediation",
        "color": "emerald",
        "numbers_detailed": [
            {
                "label": "Mediation Rate", "val": "50,000 CDR/s", "category": "Throughput",
                "derivation": "16 worker pods running 1,000 Virtual Threads chunking at 2,500 records per database batch commit.",
                "soundbite": "We sustained 50,000 normalized telecom CDRs per second while reducing JVM memory consumption by 90% via off-heap memory mapping.",
                "interview_question": "Why 2,500 records per chunk? It amortizes network round-trip costs across database inserts while keeping rollback blast radius minimal if a transient failure occurs."
            },
            {
                "label": "Heap Footprint", "val": "< 1.5 GB", "category": "Memory",
                "derivation": "Using memory-mapped DirectByteBuffer slices instead of instantiating 50,000 temporary Java byte[] arrays per second.",
                "soundbite": "By replacing heap-allocated byte arrays with off-heap ByteBuffer pointers, we slashed worker JVM heap requirements from 16 GB to 1.5 GB.",
                "interview_question": "What is the danger of pin-parking Virtual Threads in Java 21? Synchronized blocks and native methods pin the virtual thread to its underlying OS carrier thread, starving the pool."
            },
            {
                "label": "DLQ Quarantine Latency", "val": "< 1.2 ms", "category": "Latency",
                "derivation": "Asynchronous fire-and-forget Kafka producer with partition key hash ensures corrupt records bypass the batch retry loop instantly.",
                "soundbite": "Corrupt or unparseable ASN.1 records are quarantined to a dead-letter Kafka topic in under 1.2ms without blocking the clean batch stream.",
                "interview_question": "How do you avoid poison pills crashing your batch mediation workers? We wrap chunk item processors in non-blocking try-catch blocks that route invalid schemas to DLQ."
            },
            {
                "label": "File Ingestion Scale", "val": "2 GB Files in 42s", "category": "Scale",
                "derivation": "Parallel memory mapping with 8 concurrent chunk readers per worker pod across 10GbE network storage.",
                "soundbite": "A 2 GB raw ASN.1 telecom dump is completely parsed, validated, rated, and persisted in 42 seconds end-to-end.",
                "interview_question": "How do you detect file boundary cuts in parallel mmap processing? We scan for the ASN.1 header tag and length octets to realign the byte pointer."
            }
        ]
    },
    {
        "id": "ch6",
        "num": 6,
        "track": "Track 3: High-Scale Batch, Mediation & Processing",
        "title": "Stream Processing & Complex Event Processing",
        "subtitle": "Apache Flink State Backends, Event-Time Watermarks, Chandy-Lamport Checkpointing, and Exactly-Once",
        "badge": "Module 6 • Stream Engine",
        "domain": "Real-Time Stream & CEP Analytics",
        "color": "teal",
        "numbers_detailed": [
            {
                "label": "End-to-End Latency", "val": "< 85 ms p99", "category": "Latency",
                "derivation": "In-memory RocksDB state access + sub-second micro-batching with event-time watermarking across 20M cell towers.",
                "soundbite": "Our Flink complex event processing engine evaluates sliding windows across 20M cell towers with sub-100ms end-to-end latency.",
                "interview_question": "How does Flink achieve Exactly-Once semantics? Through the Chandy-Lamport distributed checkpointing algorithm paired with a Two-Phase Commit (2PC) producer sink."
            },
            {
                "label": "Checkpoint Duration", "val": "180 ms", "category": "Reliability",
                "derivation": "Incremental RocksDB checkpoints upload only newly flushed SSTables to object storage asynchronously, avoiding stop-the-world pauses.",
                "soundbite": "By switching to incremental RocksDB state checkpoints, state snapshot duration plummeted from 45 seconds to 180 milliseconds.",
                "interview_question": "What is the difference between processing time and event time? Event time uses the timestamp embedded in the record at origin; processing time uses the machine clock where the operator runs."
            },
            {
                "label": "Watermark Delay", "val": "5 Seconds", "category": "Reliability",
                "derivation": "BoundedOutOfOrderness(5s) allows 99.98% of delayed wireless cell tower packets to arrive before closing the event-time window.",
                "soundbite": "We dimensioned our event-time watermark with a 5-second bounded out-of-orderness tolerance, capturing 99.98% of delayed edge packets.",
                "interview_question": "What happens to records that arrive AFTER the watermark has passed? They are considered late data and can be routed to a side-output stream for reconciliation."
            },
            {
                "label": "State Volume Managed", "val": "4.5 TB RocksDB", "category": "Scale",
                "derivation": "Distributed across 40 TaskManager pods using local NVMe drives for off-heap embedded RocksDB state.",
                "soundbite": "Our Flink pipeline manages 4.5 TB of active sliding-window state without garbage collection impact by storing state in embedded RocksDB.",
                "interview_question": "Why not use Flink's in-memory HeapStateBackend for 4.5 TB? Because Java objects create massive garbage collection pauses and blow past Kubernetes container limits."
            }
        ]
    },
    {
        "id": "ch7",
        "num": 7,
        "track": "Track 4: Real-Time Telecom & Rule Engines",
        "title": "Hierarchical Rule Engine & Quota Reservation",
        "subtitle": "3GPP TS 32.299 Charging Tree, Rete Algorithm, Dynamic Tariff Matching, and Lock-Free DAG Swapping",
        "badge": "Module 7 • Rule Engine",
        "domain": "Real-Time Rule Engines & Rating Algorithms",
        "color": "amber",
        "numbers_detailed": [
            {
                "label": "Rule Traversal Latency", "val": "< 1.2 ms p99", "category": "Latency",
                "derivation": "In-memory Radix tree DAG traversal executed via lock-free atomic pointer reads in C++ / Java off-heap memory.",
                "soundbite": "By compiling 3GPP charging rules into an in-memory prefix tree, readers evaluate tariffs in 1.2ms p99 without a single database round-trip.",
                "interview_question": "How do you handle live rule updates without stopping traffic? We compile a new cloned tree and swap the root pointer atomically using std::atomic<Node*> with release-acquire semantics."
            },
            {
                "label": "Token Reservation Throughput", "val": "120,000 QPS", "category": "Throughput",
                "derivation": "Partitioned in-memory Redis cluster executing atomic Lua credit-control reserve scripts per subscriber bucket.",
                "soundbite": "Our distributed token reservation cluster handles 120,000 quota reservation operations per second with sub-2ms latency.",
                "interview_question": "How do you prevent negative balances during concurrent reservation requests? Atomic Lua script verifies remaining balance >= requested units before decrementing."
            },
            {
                "label": "Tree Rule Capacity", "val": "250,000 Rules", "category": "Scale",
                "derivation": "Radix prefix compression shares common tariff prefixes (MCC-MNC, service-type, time-of-day), requiring only 64 MB RAM.",
                "soundbite": "Our compressed radix tree stores 250,000 complex multi-tenant tariff rules in just 64 MB of RAM with O(K) lookup time where K is depth.",
                "interview_question": "Why is a Radix tree superior to sequential if-else rule evaluation? Sequential evaluation is O(N) where N=250k; Radix tree is O(K) where K is the number of decision dimensions (typically 6-8)."
            },
            {
                "label": "Zero-Downtime Swap Time", "val": "15 Nanoseconds", "category": "Reliability",
                "derivation": "Atomic 64-bit pointer write (lock-free) swaps the root pointer from old tree to newly validated tree.",
                "soundbite": "Live tariff updates take effect in 15 nanoseconds via atomic pointer swap, with zero read locks or latency spikes.",
                "interview_question": "How do you safely free memory of the old tree in C++? Using Read-Copy-Update (RCU) or hazard pointers to ensure all in-flight readers finish before deallocation."
            }
        ]
    },
    {
        "id": "ch8",
        "num": 8,
        "track": "Track 4: Real-Time Telecom & Rule Engines",
        "title": "5G Core Telecom Architecture & SBA",
        "subtitle": "5G Service-Based Architecture, User Plane Function (UPF), PCF / CHF Policy, and N4/N3 Protocols",
        "badge": "Module 8 • 5G Core",
        "domain": "5G Standalone Architecture",
        "color": "yellow",
        "numbers_detailed": [
            {
                "label": "User Plane Latency", "val": "< 50 µs", "category": "Latency",
                "derivation": "Hardware-accelerated DPDK packet forwarding bypassing kernel networking stack on 3GPP N3 interface.",
                "soundbite": "In 5G Standalone architecture, control plane and user plane are strictly decoupled. Our UPF forwards user traffic in under 50 microseconds.",
                "interview_question": "What is the primary difference between 4G EPC and 5G Core? 4G used point-to-point Diameter protocols; 5G uses a cloud-native Service-Based Architecture (SBA) over HTTP/2 REST APIs."
            },
            {
                "label": "Availability SLA", "val": "99.999% (Five 9s)", "category": "Reliability",
                "derivation": "Mandated telecom availability translates to no more than 5.26 minutes of unscheduled downtime per calendar year.",
                "soundbite": "We engineered our 5G Core microservices for 99.999% carrier-grade availability through multi-region active-active deployments.",
                "interview_question": "How do you achieve 99.999% availability during software upgrades? Canary rollouts with zero-downtime N4 session state migration between redundant UPF instances."
            },
            {
                "label": "Concurrent Sessions", "val": "5,000,000 PDU", "category": "Scale",
                "derivation": "Distributed across 32 SMF microservice pods backed by an in-memory session cache cluster.",
                "soundbite": "Our session management function coordinates over 5 million concurrent active PDU sessions with sub-5ms session setup times.",
                "interview_question": "What is the role of the NRF in 5G SBA? The Network Repository Function acts as a service discovery registry, allowing NFs to register and discover each other dynamically."
            },
            {
                "label": "Control Plane Latency", "val": "< 8 ms p99", "category": "Latency",
                "derivation": "HTTP/2 multiplexed streams with persistent TLS connection pooling across Kubernetes sidecar mesh.",
                "soundbite": "5G SBA inter-service RPCs complete in under 8ms p99 using HTTP/2 multiplexing and Protobuf payload serialization.",
                "interview_question": "Why did 3GPP choose HTTP/2 over Diameter for 5G SBA? HTTP/2 provides standard multiplexing, widespread tooling, and native cloud-native observability."
            }
        ]
    },
    {
        "id": "ch9",
        "num": 9,
        "track": "Track 5: Global Storage, Partitioning & Caching",
        "title": "Globally Distributed Multi-Region Database",
        "subtitle": "ScyllaDB / Cassandra LSM-Trees, Seastar Thread-per-Core, Tunable Quorum, and Gossip",
        "badge": "Module 9 • Multi-DC Storage",
        "domain": "Distributed NoSQL & Multi-Region Storage",
        "color": "violet",
        "numbers_detailed": [
            {
                "label": "Local Write Latency", "val": "< 3.8 ms p99", "category": "Latency",
                "derivation": "CommitLog append + MemTable write in local datacenter replicas only with O_DIRECT NVMe SSD bypass.",
                "soundbite": "By enforcing LOCAL_QUORUM consistency, writes commit to local NVMe SSDs in 3.8ms while replicating asynchronously across continents.",
                "interview_question": "Why avoid consistency level ALL across global regions? Because a single network glitch on a transatlantic fiber cut will take down writes worldwide."
            },
            {
                "label": "Cross-DC Replication Lag", "val": "< 80 ms", "category": "Latency",
                "derivation": "Asynchronous inter-datacenter replication over dedicated private cloud fiber backbone (US-East to EU-Central).",
                "soundbite": "Cross-datacenter gossip and write mutation streams achieve an asynchronous replication lag under 80ms under normal fiber conditions.",
                "interview_question": "How do you resolve conflicting writes across datacenters in Cassandra? Last-Write-Wins (LWW) based on client timestamp, or lightweight transactions (Paxos) for linearizability."
            },
            {
                "label": "Compaction Write Amplification", "val": "< 3.2x (LCS)", "category": "Hardware",
                "derivation": "Leveled Compaction Strategy organizes SSTables into fixed-size layers, bounding write amplification and read fan-out.",
                "soundbite": "We configured Leveled Compaction Strategy to cap write amplification at 3.2x and guarantee single-SSTable point lookups via Bloom filters.",
                "interview_question": "Why choose Size-Tiered vs Leveled Compaction? Size-Tiered is optimal for write-heavy workloads with append-only data; Leveled is superior for read-heavy workloads."
            },
            {
                "label": "Read Fan-out SLA", "val": "1 SSTable Read", "category": "Latency",
                "derivation": "Bloom filters with 1% false positive probability ensure 99% of non-existent key lookups avoid disk I/O completely.",
                "soundbite": "With tuned Bloom filters and row keys indexed in memory, 98% of read queries hit exactly one SSTable on NVMe storage.",
                "interview_question": "What is the memory cost of Bloom filters? Approximately 10 bits per key for a 1% false-positive probability."
            }
        ]
    },
    {
        "id": "ch10",
        "num": 10,
        "track": "Track 5: Global Storage, Partitioning & Caching",
        "title": "Planet-Scale Distributed SQL & TrueTime",
        "subtitle": "Google Spanner External Consistency, Atomic Clocks + GPS TrueTime API, and Multi-Paxos Tablets",
        "badge": "Module 10 • Spanner SQL",
        "domain": "Globally Consistent Distributed SQL",
        "color": "rose",
        "numbers_detailed": [
            {
                "label": "TrueTime Uncertainty", "val": "ε < 7 ms", "category": "Reliability",
                "derivation": "Drift bound provided by redundant GPS receivers and Rubidium atomic clocks in each Google datacenter zone.",
                "soundbite": "Spanner bounds clock drift uncertainty to under 7ms using hardware TrueTime. Waiting out epsilon allows lock-free read transactions across the globe.",
                "interview_question": "What is the difference between linearizability and serializability? Serializability means there is SOME valid sequential order. Linearizability means that order matches real-world wall-clock physical time."
            },
            {
                "label": "Global Read Snapshot", "val": "0 Locks (Lock-Free)", "category": "Latency",
                "derivation": "Multi-Version Concurrency Control (MVCC) reads historical timestamp <= (TrueTime.now().latest - epsilon) with zero locks.",
                "soundbite": "Spanner serves globally consistent, external-consistency read-only transactions without taking a single lock, eliminating read-write contention.",
                "interview_question": "Why does Spanner require hardware atomic clocks? NTP over the public internet has uncertainty up to 100-250ms; hardware clocks guarantee bounded epsilon under 7ms."
            },
            {
                "label": "Commit Wait Penalty", "val": "2 * ε (14 ms)", "category": "Latency",
                "derivation": "Commit wait rule: Leader chooses commit timestamp s = TrueTime.now().latest, then waits until TrueTime.now().earliest > s before releasing locks.",
                "soundbite": "The commit wait rule intentionally pauses the commit for 2 epsilon (14ms) to guarantee no subsequent transaction can receive an earlier timestamp.",
                "interview_question": "What happens if TrueTime fails on a machine? If the master daemon detects clock drift exceeding the safe threshold, the machine evicts itself from the cluster."
            },
            {
                "label": "Cross-Continent 2PC", "val": "p99 < 120 ms", "category": "Latency",
                "derivation": "Two-Phase Commit coordinated across Paxos tablet leaders in 3 continents with physical fiber speed of light round-trip.",
                "soundbite": "Multi-region distributed transactions achieve external consistency across continents in under 120ms p99 using Two-Phase Commit over Paxos.",
                "interview_question": "Why is 2PC over Paxos resilient to coordinator crashes? Because the 2PC coordinator state is replicated via Paxos, so a crash allows a successor leader to resume the transaction."
            }
        ]
    },
    {
        "id": "ch11",
        "num": 11,
        "track": "Track 6: Traffic Shaping, Resilience & Migrations",
        "title": "Enterprise Rate Limiting & Traffic Shaping",
        "subtitle": "Generic Cell Rate Algorithm (GCRA), Adaptive Concurrency Limits, and Hedged Requests",
        "badge": "Module 11 • Traffic Guard",
        "domain": "Resilience & Cascading Failure Defense",
        "color": "pink",
        "numbers_detailed": [
            {
                "label": "Rate Check Latency", "val": "< 0.4 ms p99", "category": "Latency",
                "derivation": "In-memory Redis single-shard atomic Lua script calculating Theoretical Arrival Time (TAT).",
                "soundbite": "We implement GCRA with atomic Redis Lua scripts, providing microsecond-precision rate shaping that eliminates window-boundary bursts.",
                "interview_question": "Why GCRA over fixed-window counters? Fixed-window counters permit a 2x burst across the window boundary, which frequently collapses downstream databases."
            },
            {
                "label": "Fail-Open Availability", "val": "100% Fail-Open", "category": "Reliability",
                "derivation": "Circuit breaker trips to bypass limiter if Redis cluster response exceeds 15ms or returns errors.",
                "soundbite": "Our rate limiter adheres to a strict fail-open policy: if the limiter cluster experiences an outage, traffic passes through to protect business availability.",
                "interview_question": "When would you prefer fail-closed over fail-open? For security and authentication endpoints (e.g., login brute-force protection, credit card charging)."
            },
            {
                "label": "Hedged Request Latency Drop", "val": "p99.9 Reduced 65%", "category": "Latency",
                "derivation": "Google Tail at Scale technique: If primary RPC does not return within p95 latency (12ms), a duplicate hedged request is dispatched to a secondary replica.",
                "soundbite": "By firing hedged requests after the 95th percentile latency mark, we shaved 65% off our 99.9th percentile tail latency with only 2% additional server load.",
                "interview_question": "How do you prevent hedged requests from overloading a struggling downstream server? Cancel the pending request immediately when the first response arrives, and limit hedging to < 5% of traffic."
            },
            {
                "label": "Adaptive Limit Slew Rate", "val": "5% / Minute", "category": "Scale",
                "derivation": "TCP Vegas algorithm computes gradient of measured RTT vs baseline RTT, dynamically throttling concurrent connection limits.",
                "soundbite": "Client-side adaptive concurrency limiters dynamically throttle concurrency based on RTT latency inflation, preventing cascading queue collapse.",
                "interview_question": "Why are static thread pool limits dangerous in production? If a downstream database slows down by 2x, static thread pools saturate instantly, cascading failures upstream."
            }
        ]
    },
    {
        "id": "ch12",
        "num": 12,
        "track": "Track 6: Traffic Shaping, Resilience & Migrations",
        "title": "Zero-Downtime Database Migration & Shadow Replay",
        "subtitle": "Dark Launching, Dual Writes with Monotonic Versions, Continuous Reconciliation, and 1s Rollback",
        "badge": "Module 12 • Migration Core",
        "domain": "Online Database Migration & Verification",
        "color": "teal",
        "numbers_detailed": [
            {
                "label": "Customer Downtime", "val": "0 Seconds", "category": "Reliability",
                "derivation": "Online 4-phase shadow migration protocol: Dual Writes -> Historical Backfill -> Dark Replay -> 1-Second DNS Cutover.",
                "soundbite": "We migrated 500 million live subscriber profiles from Oracle to ScyllaDB with zero seconds of customer downtime.",
                "interview_question": "What is the primary danger in dual writes? Out-of-order retries overwriting fresh state. We enforce monotonic write versioning to guarantee idempotency."
            },
            {
                "label": "Data Parity Verified", "val": "100.000%", "category": "Reliability",
                "derivation": "Continuous asynchronous reconciliation worker compared 500M row checksums over a 14-day dark replay period.",
                "soundbite": "Before cutting over DNS, our background shadow reconciler verified 100.000% data parity across 500 million records over 14 days of live dark traffic.",
                "interview_question": "How do you reconcile records that are actively being modified during backfill? Compare monotonic record version numbers; if target version >= source version, the row is fresh."
            },
            {
                "label": "Rollback Window", "val": "< 1 Second", "category": "Reliability",
                "derivation": "Reverse dual-writing (ScyllaDB to Kafka shadow queue back to Oracle) maintained for 30 days post-cutover.",
                "soundbite": "We maintained reverse dual-writing for 30 days post-cutover, allowing instant 1-second rollback to Oracle with zero data loss if anomalies surfaced.",
                "interview_question": "Why is reverse replication necessary post-cutover? If an undetected bug surfaces in the new database after 48 hours, without reverse replication, rolling back loses 48 hours of customer data."
            },
            {
                "label": "Backfill Throughput", "val": "85,000 Rows/s", "category": "Throughput",
                "derivation": "Apache Spark job partitioned across primary key token ranges reading read-replicas with rate throttling.",
                "soundbite": "Historical backfill migrated 500 million records in 1.6 hours at 85,000 rows/second without exceeding 20% CPU on production read replicas.",
                "interview_question": "How do you prevent the historical backfill from degrading online customer queries? Backfill reads from isolated physical read replicas and throttles throughput based on replica replication lag."
            }
        ]
    }
]

# Write out modules_data.py
out = ["# modules_data.py", "# Full 12 Google L6/L8 Staff Engineering Modules with Topologies and Numbers\\n", "MODULES_LIST = ["]

for m in MODULES_DATA:
    ch_id = m["id"]
    title = m["title"]
    svg_topo = detailed_topology_svgs.get_detailed_svg(ch_id, title)
    
    # Dual-option component: Rich SVG diagram + Whiteboard interactive launch buttons
    ref_topo_html = f'''
    <div class="p-4 bg-slate-950 rounded-xl border border-cyan-900/50 space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div>
          <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block font-mono">Google L6/L8 Canonical Architecture Topology</span>
          <h4 class="text-sm font-bold text-white mt-0.5">{title}</h4>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="openSplitStudioWithTopology('{ch_id}')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow transition-all">
            <span>◫</span> Load into Split Studio
          </button>
          <button onclick="openWhiteboardModal()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs flex items-center gap-1.5 border border-slate-700 transition-all">
            <span>🎨</span> Open Whiteboard
          </button>
          <button onclick="verifyArchitectureScore()" class="px-2.5 py-1.5 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 border border-indigo-700 text-xs font-semibold">
            🤖 Verify Architecture
          </button>
        </div>
      </div>

      <!-- Pre-Sketched High-Resolution Visual Topology -->
      <div class="space-y-2">
        <div class="flex items-center justify-between text-xs text-slate-400">
          <span class="font-mono text-[11px]">Option A: Pre-Sketched Canonical System Diagram</span>
          <span class="text-emerald-400 font-mono text-[11px]">✔ Google Staff L6 Verified</span>
        </div>
        {svg_topo}
      </div>

      <!-- Option B: Guided Sketching & Whiteboard Practice -->
      <div class="p-3 bg-[#030717] rounded-lg border border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-amber-400 font-bold">Option B: Practice Sketching Yourself</span>
          <span class="text-slate-400 text-[11px]">— Open the canvas to draw your version, or click "Load into Split Studio" to inspect & drag each component box.</span>
        </div>
        <button onclick="openSplitStudioWithTopology('{ch_id}')" class="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 font-mono text-[11px] border border-cyan-800">
          📥 Populate Split Canvas (+25 XP)
        </button>
      </div>
    </div>
    '''

    m_copy = dict(m)
    m_copy["reference_topology"] = ref_topo_html
    out.append(repr(m_copy) + ",")

out.append("]\n")

with open("d:/Antigravity/modules_data.py", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Successfully updated modules_data.py with all 48 metrics and rich SVG topologies!")
