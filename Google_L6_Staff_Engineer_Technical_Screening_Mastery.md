# GOOGLE L6 (STAFF) SOFTWARE ENGINEER: TECHNICAL SCREENING & SYSTEM MASTERY COMPENDIUM
**Candidate:** Shivam Agarwal | **Target Level:** Google L6 (Staff Software Engineer) / L7 (Principal)  
**Core Domains:** Distributed Systems, High Concurrency, Carrier-Scale Cloud Infrastructure, Event-Driven Architectures  

---

## 1. Programming Language Mastery: Java
**Selected:** Java (Java 21 / 17 / 11 / 8)

### Human-Grade Staff Defense:
- **Core Depth:** 10+ years of hands-on production engineering using Java to architect carrier-grade, low-latency distributed systems. 
- **Modern Java 21 Capabilities in Production:**
  - **Virtual Threads (Project Loom):** Solved high-density I/O bottlenecks by replacing bound OS thread pools with lightweight virtual threads (`Thread.ofVirtual()`), handling thousands of concurrent network connections without platform thread exhaustion.
  - **Pattern Matching & Records:** Used strongly typed, immutable Java `records` for domain event schemas and sealed interfaces to enforce compile-time exhaustive state-machine transitions across complex telecom workflows.
- **JVM Internals & Performance Tuning:**
  - Deep experience with garbage collection tuning (ZGC and G1GC) to suppress stop-the-world pauses on 64GB+ heaps.
  - Low-level profiling using `async-profiler`, Java Flight Recorder (JFR), and memory leak diagnosis with heap dump analyzers.

---

## 2. Carrier-Grade Microservices Architecture
**Context:** Samsung Unified System Manager (USM) Configuration Management (CM) Platform (3,164+ Java files, 60+ sub-modules).

### Architecture Overview:
The platform orchestrates lifecycle operations, software rollouts, and real-time configuration for 4G LTE, 5G NR (gNB CU/DU split), and O-RAN network elements across 15+ global Tier-1 operators (KDDI, KT, SKT, Comcast, TELUS, Reliance Jio).

```
   [Northbound OSS / CLI / Web UI] 
                 │
                 ▼ (REST / mTLS)
   [USM API Gateway & Request Dispatcher]
                 │
                 ├──► [prjCmGrow: Lifecycle & Growth Engine] ──► [Declarative Validation DAG (200+ Rules)]
                 ├──► [prjCmParameterAudit & Diff Engine]    ──► [Distributed Session Locker (Lease Heartbeats)]
                 ├──► [prjCmSwm: Software Management Daemon] ──► [Multi-Threaded Worker Execution Pools]
                 └──► [prjCmNrm: Resource Model Sync Engine] ──► [NETCONF (RFC 6241/6242) / YANG Handlers]
                                                                          │
                                                                          ▼ (SSH / TLS Southbound)
                                                            [30+ 4G/5G Network Element Types]
```

### Scalability & Fault Tolerance Approaches:
1. **Workload Bulkheading & Worker Pool Isolation:** Handlers maintain segregated thread pools per operator and per Network Element type. A spike in configuration traffic from one operator cannot starve another operator's worker queue.
2. **Key-Partitioned Event Ingestion (Kafka):** Events are partitioned by `NetworkElement_ID`. This guarantees strict per-element FIFO ordering without global locks, enabling linear horizontal scaling across consumer pods.
3. **Stateless Compute & Distributed Session Locking:** Microservices are stateless containers running on Kubernetes. Where multi-step coordination across deep 3GPP containment trees is required, we use distributed lease-based session locks (`EditingPlanLocker`, `SessionLocker`) with heartbeat renewals to eliminate split-brain edits.
4. **Idempotency & Deduplication:** Every incoming transaction carries an `idempotency_key` checked against an in-memory sliding window cache to safely discard duplicate retries caused by flaky radio links.

---

## 3. Resilient Service Failures: Retries, Timeouts, Circuit Breaking & Scale
**Scale Context:** Managing **20M+ cell sectors and 1M+ Network Elements**, sustaining peak bursts of **45,000+ configuration transactions/sec** during metropolitan network reconfigurations and automated Self-Organizing Network (SON) runs.

### Failure Handling Mechanics:
1. **Explicit, Granular Timeouts:** Never rely on default timeouts. 
   - *Connect Timeout:* 1–2 seconds.
   - *Read/Socket Timeout:* 5–8 seconds based on observed p99 latencies.
2. **Retries with Exponential Backoff and Full Jitter:**
   - Retries apply strictly to transient network resets and 5xx errors; 4xx client validation errors fail fast.
   - To avoid the "thundering herd" effect where retrying clients overwhelm recovering downstream dependencies, backoff follows:
     $$\text{Sleep} = \text{random}(0, \, \min(\text{MaxSleep}, \, \text{BaseSleep} \times 2^{\text{attempt}}))$$
3. **Circuit Breaking (Resilience4j / Envoy):**
   - Tracks error rates within a sliding execution window (e.g., 50 calls).
   - If error rate exceeds 50%, the circuit transitions to `OPEN`, immediately returning fallback data or fast-failing to preserve thread pools.
   - Automatically probes recovery with a `HALF_OPEN` state after a cool-down window (e.g., 15s).
4. **Dead Letter Queues (DLQ) & Audit Replay:** Failed transactions that exhaust retries are routed to persistent DLQ topics with telemetry alerts for asynchronous recovery without stalling production traffic.

---

## 4. System Design: Real-Time Retail Inventory Visibility (Thousands of Stores)

### Functional & Scale Requirements:
- Thousands of retail stores, millions of SKUs.
- Real-time stock visibility queries (read p99 < 20ms).
- High write volume: in-store POS checkouts, returns, warehouse restocks, and online cart reservations.

### Architecture Diagram:
```
[In-Store POS / Web Carts]
            │
            ▼ (HTTPS / Token Bucket Rate Limiting)
     [Envoy API Gateway]
            │
            ▼ (Partitioned by store_id:sku_id)
     [Apache Kafka Topic: inventory-events]
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
[Stream Processor (Flink/Java 21)]       [Async Persistence Consumer]
            │                                         │
   (Atomic In-Memory Lua)                     (Append-Only Ledger)
            ▼                                         ▼
[Redis Cluster: store_inventory:{id}]     [Sharded PostgreSQL / ScyllaDB]
            ▲
            │ (Sub-5ms p99 Reads)
    [Read Query API] ◄── [Mobile App / Web Storefront]
```

### Detailed Subsystems:
1. **Partitioned Ingestion:** Updates are published to Kafka keyed by `hash(store_id:sku_id)`. All inventory deltas for a specific product at a specific store land on the exact same broker partition, guaranteeing ordered sequential processing.
2. **Real-Time In-Memory Serving Cache (Redis Cluster):**
   - Stock balances are cached in Redis Hashes: `HSET store_inventory:{store_id} {sku_id} {available_qty}`.
   - Atomic conditional deductions are executed via Lua scripts:
     ```lua
     local current = tonumber(redis.call('HGET', KEYS[1], ARGV[1]) or '0')
     local requested = tonumber(ARGV[2])
     if current >= requested then
         redis.call('HINCRBY', KEYS[1], ARGV[1], -requested)
         return 1 -- SUCCESS
     else
         return 0 -- OUT OF STOCK
     end
     ```
3. **Immutable Event-Sourced Storage:** Every transaction is written to an append-only ledger (`inventory_transactions`) in sharded PostgreSQL/ScyllaDB. Current balances in the database are reconciled asynchronously via Change Data Capture (Debezium/Kafka Connect).
4. **Offline Store Edge Resilience:** Each physical store runs an edge daemon with local SQLite cache. If WAN connectivity fails, POS checkouts proceed against locally allocated quotas, syncing upstream via vector clocks when the link restores.

---

## 5. High Availability (HA) & Horizontal Scaling
### High Availability Strategy:
1. **Multi-AZ Active-Active Redundancy:** Stateless application services deploy across $\ge 3$ Availability Zones behind geo-distributed load balancers. A failure of an entire AZ shifts traffic instantly without user impact.
2. **Stateless Application Tier:** No in-memory session pinning. Tokens are signed stateless JWTs or backed by Redis, enabling immediate pod replacement.
3. **Graceful Degradation:** If the real-time exact inventory service degrades, checkout falls back to optimistic reservation with asynchronous confirmation rather than failing hard with HTTP 500.
4. **Storage HA:** Primary-replica database topologies with automated failover (Patroni for PostgreSQL; ScyllaDB with Replication Factor of 3 and `LOCAL_QUORUM` reads/writes).

### Horizontal Scaling Strategy:
1. **Domain-Driven Sharding:** Shard compute and database tiers by `store_id`. Because operations at Store 101 do not touch Store 502, scaling is linearly additive.
2. **Autoscaling on Custom Lag Metrics:** Kubernetes HPA autoscales pods based on Kafka consumer group lag (via KEDA) and p99 request latency rather than raw CPU.
3. **CQRS (Command Query Responsibility Segregation):** Decouple heavy read traffic (hitting Redis clusters and database read replicas) from the transactional write path.

---

## 6. Systematic Re-Architecture of Legacy Bottlenecked Systems

### Phase 1: Observability & Bottleneck Profiling (Zero Assumptions)
- Profile end-to-end latency with distributed tracing (OpenTelemetry/Jaeger).
- Triage the root cause:
  - *Database:* Slow queries, missing indexes, table lock contention, unpartitioned multi-terabyte tables, N+1 query loops.
  - *Application:* Synchronous blocking I/O, heavy lock contention, stop-the-world GC pauses (profiled via `async-profiler` / JFR).
  - *Network/Protocol:* Serial RPC head-of-line blocking (e.g., RFC 6241 serial device-side locks).

### Phase 2: Incremental Transformation (Strangler Fig Pattern)
- Avoid catastrophic big-bang rewrites.
- Place a routing proxy (Envoy / API Gateway) in front of the legacy system.
- Decouple synchronous blocking interactions into asynchronous event streams (Kafka/RabbitMQ).
- Introduce a caching layer (Redis) to offload hot read paths.
- Carve out bounded contexts one service at a time.

### Phase 3: Shadow Traffic & Dark Launch Verification
- Deploy the new service in parallel without user-facing impact.
- Mirror live production traffic (shadow requests) to both legacy and new systems.
- Compare outputs, error rates, and p99 latency percentiles to verify 100% parity before initiating a canary traffic rollout (1% $\rightarrow$ 10% $\rightarrow$ 100%).

---

## 7. Multi-Threading, Concurrency & Race Condition Elimination

### Real-World Production Problem:
In Samsung USM, executing firmware upgrades and configuration verifications sequentially across 5,000 base stations required **14+ hours**. 
We re-architected this into an asynchronous worker daemon leveraging Java 21 Virtual Threads (`Loom`):
- Each network element upgrade is heavily I/O-bound (SFTP image download, MD5 verification, candidate configuration lock, activation RPC).
- Virtual threads allowed thousands of concurrent worker tasks without exhausting underlying OS platform threads, slashing the batch window from 14 hours down to **22 minutes**.

### What is a Race Condition?
A race condition occurs when concurrent threads access and mutate shared state without synchronization, causing non-deterministic execution where the final state depends on thread scheduling order. 
*Example:* Two threads simultaneously executing `counter++`. Both read `10`, compute `11`, and write `11`, silently losing one increment.

### Prevention Techniques:
1. **Immutability:** Use Java `records` and unmodifiable collections. Immutable state is inherently thread-safe.
2. **Lock-Free Atomic Primitives:** Use hardware Compare-And-Swap (CAS) operations (`AtomicLong`, `AtomicReference`, `LongAdder`) for high-throughput counters.
3. **Concurrent Data Structures:** Use `ConcurrentHashMap` (segment-level locking) and `ConcurrentSkipListMap` instead of synchronized wrapper collections.
4. **Explicit Lock Scoping with Timeouts:** Use `ReentrantLock.tryLock(timeout)` to eliminate deadlock potential.
5. **Distributed Fencing Tokens:** For distributed locking, issue monotonic 64-bit integer tokens (`INCR`) validated at the database layer (`WHERE version < token`) to discard stale writes caused by JVM GC pauses.

---

## 8. Stream Coding: Efficiently Finding the Latest State per SKU

### Problem Context:
Incoming stream: `UpdateEvent(sku_id, quantity, timestamp, sequence_num)`. Events arrive out-of-order due to network delays.

### Optimal Real-Time Stream Processor (Java / Flink / Kafka Streams):
```java
public class SkuLatestStateProcessor {
    // In production, backed by an in-memory RocksDB StateStore
    private final Map<String, SkuState> stateStore = new ConcurrentHashMap<>();

    public void processEvent(UpdateEvent incoming) {
        stateStore.compute(incoming.getSkuId(), (sku, current) -> {
            if (current == null) {
                return new SkuState(incoming.getQuantity(), incoming.getTimestamp(), incoming.getSequenceNum());
            }
            // Strict sequence & timestamp check to reject out-of-order arrivals
            boolean isNewer = incoming.getSequenceNum() > current.getSequenceNum()
                || (incoming.getSequenceNum() == current.getSequenceNum() 
                    && incoming.getTimestamp() > current.getTimestamp());

            return isNewer 
                ? new SkuState(incoming.getQuantity(), incoming.getTimestamp(), incoming.getSequenceNum()) 
                : current; // Discard stale update
        });
    }
}
```

### Production Architectural Guarantees:
- **Kafka Log Compaction:** Configure the topic with `cleanup.policy=compact`. Kafka's background cleaner automatically deletes older records with the same SKU key, retaining only the latest record indefinitely.
- **SQL Batch Equivalent:**
  ```sql
  SELECT sku_id, quantity, event_timestamp
  FROM (
      SELECT sku_id, quantity, event_timestamp,
             ROW_NUMBER() OVER (PARTITION BY sku_id ORDER BY sequence_num DESC, event_timestamp DESC) as rn
      FROM inventory_stream
  ) ranked
  WHERE rn = 1;
  ```

---

## 9. Large-Scale Duplicate Transaction Detection

### Duplicate Definition:
Identical `account_id`, `amount`, `merchant_id` occurring within a $\Delta t \le 5\text{-minute}$ window, or identical cryptographic transaction hashes.

### Approach 1: Real-Time Stream Deduplication (Bloom Filter + Redis Window)
1. **Fingerprint Hash:** `hash = SHA256(account_id + ":" + amount + ":" + merchant_id)`.
2. **Tier 1 (Fast-Path Bloom Filter):** Check distributed in-memory Bloom filter. If negative, transaction is definitely unique $\rightarrow$ add to filter and process.
3. **Tier 2 (Exact Verification):** If Bloom filter returns positive, query a Redis Sorted Set (`ZADD` with timestamp as score, TTL = 10 minutes) for that account to verify whether an exact matching amount occurred within $\pm 300\text{ seconds}$.

### Approach 2: Terabyte-Scale Batch Processing (Distributed MapReduce / Spark)
```
[500M Transactions] 
        │
        ▼ (Hash-Partition by account_id: O(N) Network Shuffle)
[Worker Nodes] ──► Local In-Memory Sort by timestamp: O(M log M) per worker
        │
        ▼ (Linear 1-Pass Sliding Window Scan: O(M))
[Flag Duplicates where tx[i].amount == tx[i-1].amount AND Δt <= 300s]
```
- **Why this beats $O(N^2)$ cross-joins:** Partitioning ensures that all transactions for an account land on the exact same worker. Sorting locally requires $O(M \log M)$ time, followed by a single-pass linear comparison against adjacent records within the 5-minute window.

---

## 10. Object-Oriented Principles: Composition vs. Inheritance

### Architectural Differences:
- **Inheritance (`is-a`):** Compile-time white-box reuse. Subclasses inherit internal state and methods, creating tight coupling. Changes in parent classes frequently break subclass invariants (Fragile Base Class problem).
- **Composition (`has-a`):** Runtime black-box reuse. Classes contain references to interfaces and delegate behavior, resulting in loose coupling.

### Why Staff Engineers Favor Composition:
1. **Dynamic Runtime Behavior:** Capabilities can be swapped dynamically at runtime (Strategy Pattern) without class explosion.
2. **Testability & Mocking:** Classes depending on injected interfaces are trivially mockable in unit tests without complex parent instantiations.
3. **Encapsulation Protection:** Prevents exposing unnecessary parent methods to public consumers.

---

## 11. Production Design Patterns & SOLID Architecture

### Production Design Patterns:
1. **Strategy Pattern:** Network Element Grow engine selects `ProvisioningStrategy` implementations (NETCONF vs. REST vs. SNMP) dynamically at runtime based on NE hardware profile.
2. **Builder Pattern:** Fluent builders for complex 3GPP telemetry requests with 40+ optional fields, enforcing validation and immutability.
3. **Template Method Pattern:** Firmware upgrade framework defines standard invariant lifecycles (`preFlight() -> download() -> verifyChecksum() -> flash() -> rollbackOnFailure()`), while hardware-specific subclasses implement flashing primitives.
4. **Observer / Pub-Sub Pattern:** Asynchronous dispatch of YANG Network Resource Model change events to logging and alarm listeners.

### End-to-End SOLID Architecture Design (Order Processing Service):
```
                       ┌──────────────────────┐
                       │   OrderController    │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │     OrderService     │
                       └──────────┬───────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ «interface»      │    │ «interface»      │    │ «interface»      │
│ PaymentGateway   │    │ InventoryService │    │ NotificationSvc  │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
 ┌───────┴───────┐               │               ┌───────┴───────┐
 ▼               ▼               ▼               ▼               ▼
[StripeGW]   [PayPalGW]    [WarehouseSync]   [EmailNotifier] [SmsNotifier]
```

- **S - Single Responsibility:** `OrderService` coordinates business logic; separate classes handle payment (`PaymentGateway`), inventory reservation (`InventoryService`), and notification (`NotificationService`).
- **O - Open/Closed:** New payment providers (e.g. Apple Pay) are added by implementing `PaymentGateway` without modifying existing `OrderService` code.
- **L - Liskov Substitution:** Any `PaymentGateway` implementation can be substituted without throwing unexpected `UnsupportedOperationException`.
- **I - Interface Segregation:** Segregated focused contracts (`OrderCreator`, `OrderCanceller`, `InvoiceGenerator`) rather than one bloated 30-method interface.
- **D - Dependency Inversion:** `OrderService` depends on abstract interfaces injected via Spring constructor injection, never on concrete database or HTTP client implementations.
