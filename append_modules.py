# append_modules.py
# Appends Modules 3, 4, 5, 6, 7 to modules_tech.py

MODULES_3_TO_7 = [
    {
        "id": "ch3",
        "num": 3,
        "title": "Idempotent Consumer & Transactional Outbox",
        "subtitle": "Dual-Write Dilemma, Debezium WAL Tailing, and 2-Tier Consumer Defense",
        "badge": "Module 3 • Resume Bullet #3",
        "domain": "Reliability & Data Consistency",
        "color": "emerald",
        "theory": """
          <h3 class="text-base font-bold text-white">The Dual-Write Dilemma in Distributed Microservices</h3>
          <p>
            When a business transaction must mutate database state AND emit an event to Kafka, executing them sequentially leads to unavoidable failure states:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs mt-2">
            <div class="p-3 bg-slate-950 rounded-xl border border-rose-900/40">
              <span class="font-bold text-rose-400 block mb-1">Strategy A: DB First, Kafka Second</span>
              <p class="text-slate-400 text-[11px]">Database commits successfully, but network partitions or Kafka broker OOM crashes occur before publish. Result: State is committed, but downstream services are never notified (Event Lost forever).</p>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-rose-900/40">
              <span class="font-bold text-rose-400 block mb-1">Strategy B: Kafka First, DB Second</span>
              <p class="text-slate-400 text-[11px]">Kafka event is published successfully, but database unique constraint violation or timeout causes rollback. Result: Phantom event exists in Kafka; downstream consumers act on ghost state!</p>
            </div>
          </div>

          <h4 class="text-sm font-bold text-white mt-3">Why Distributed Two-Phase Commit (2PC / XA) Fails at 45k TPS</h4>
          <p>
            2PC requires locking resources across the database and message broker while waiting for network acknowledgments. Under 45k TPS, cross-network lock latency spikes transaction hold times by 100x, holding database locks open, exhausting HikariCP connection pools, and cascading into total system gridlock.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">The Architectural Fix: Transactional Outbox with CDC (Debezium)</h4>
          <p>
            The microservice writes its business entity mutation AND appends an event record into an <code class="text-emerald-300 font-mono">outbox_events</code> table within the <strong>exact same local ACID database transaction</strong>:
          </p>
          <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-emerald-300">
            BEGIN TRANSACTION;<br>
            &nbsp; UPDATE managed_objects SET tx_power = 40 WHERE id = 104;<br>
            &nbsp; INSERT INTO outbox_events (event_id, aggregate_type, payload) VALUES ('uuid-104', 'CELL', '{...}');<br>
            COMMIT;
          </div>
          <p class="text-xs text-slate-300">
            A Change Data Capture (CDC) engine like <strong>Debezium</strong> tails PostgreSQL's Write-Ahead Log (WAL) via the <code class="text-emerald-300 font-mono">pgoutput</code> logical replication stream, asynchronously publishing events to Kafka without polling or database locks.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">Why enable.idempotence=true Fails Consumers (At-Least-Once Rebalance Replays)</h4>
          <p>
            Setting <code class="text-emerald-300 font-mono">enable.idempotence=true</code> in Kafka only protects producer-to-broker network retries. Consumers operate under <strong>At-Least-Once delivery</strong>. If a consumer crashes after mutating state but before committing its Kafka offset, Kafka redelivers the message upon partition reassignment.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">The 2-Tier Consumer Defense Architecture</h4>
          <ul class="list-disc pl-5 space-y-1.5 text-xs text-slate-300">
            <li><strong>Tier 1 (In-Memory Redis Fast-Path):</strong> Atomically reserve event UUID: <code class="text-emerald-300 font-mono">SET idemp:evt:{id} "PENDING" NX EX 86400</code>. Filters out 99.9% of rebalance replays in sub-milliseconds without touching database I/O.</li>
            <li><strong>Tier 2 (Relational Storage Anchor):</strong> Relational idempotency table (<code class="text-emerald-300 font-mono">INSERT INTO processed_events (event_id) VALUES (?) ON CONFLICT (event_id) DO NOTHING</code>) executed inside the business transaction. If Redis evicts early, database uniqueness guarantees single-execution correctness.</li>
          </ul>
        """,
        "project": """
          <div class="space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">Production Architecture Blueprint • Samsung USM</span>
              <p class="leading-relaxed">
                <strong>Project:</strong> Cell Reconfiguration Provisioning Bus in Samsung USM.<br>
                <strong>Scale:</strong> 100M+ monthly provisioning commands, 45k TPS burst, multi-pod Kubernetes workers.<br>
                <strong>Your Role:</strong> Staff Architect designing zero-loss transactional event distribution.
              </p>
            </div>

            <h4 class="text-sm font-bold text-white">The Production Crisis (Duplicate Execution Corruption)</h4>
            <p>
              During Kubernetes node autoscaling, consumer pods rebalanced frequently. When a pod was terminated mid-batch, its offset was not yet committed. The replacement pod replayed the last 500 messages, executing cell transmission power increments twice. Over 2,000 cell towers suffered RF distortion due to duplicate configuration execution.
            </p>

            <h4 class="text-sm font-bold text-white">How You Engineered the Solution</h4>
            <ol class="list-decimal pl-5 space-y-1.5">
              <li><strong>Debezium Outbox Pipeline:</strong> Replaced dual-writes with local PostgreSQL outbox tables, streamed to Kafka via Debezium CDC and <code class="text-emerald-300 font-mono">pgoutput</code> WAL decoding, guaranteeing at-least-once zero-loss delivery.</li>
              <li><strong>2-Tier Consumer Defense:</strong> Created a two-tiered filter:
                <br>&bull; Tier 1: Redis <code class="text-emerald-300 font-mono">SET NX EX</code> key reservation dropped duplicates in &lt;1ms.
                <br>&bull; Tier 2: PostgreSQL <code class="text-emerald-300 font-mono">processed_events</code> unique primary key constraint anchored transactional mutations.</li>
              <li><strong>Manual Immediate ACK:</strong> Configured Spring Kafka with <code class="text-emerald-300 font-mono">AckMode.MANUAL_IMMEDIATE</code>, committing offsets only after the database transaction committed.</li>
              <li><strong>Dead Letter Topic (DLT):</strong> Configured exponential backoff with poison pills routed to a DLT with original Kafka headers and error stack traces.</li>
            </ol>

            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-emerald-300">
              Verified Metrics to Quote in Interview:<br>
              • Duplicate Execution Rate: 0 duplicate mutations across 100M+ processed events.<br>
              • Ingestion Overhead: &lt;1.5ms added latency via Redis Tier-1 fast path.<br>
              • Outbox Lag: Under 80ms p99 latency from DB commit to Kafka topic availability.
            </div>
          </div>
        """,
        "code": """
<pre><code class="text-slate-300"><span class="text-slate-400">// Java 21 Spring Boot - 2-Tier Idempotent Kafka Consumer</span>
<span class="text-purple-400">@Service</span>
<span class="text-purple-400">@Slf4j</span>
<span class="text-purple-400">public class</span> <span class="text-blue-400">CellProvisioningConsumer</span> {

    <span class="text-purple-400">@Autowired private</span> StringRedisTemplate redisTemplate;
    <span class="text-purple-400">@Autowired private</span> ProcessedEventRepository processedEventRepo;
    <span class="text-purple-400">@Autowired private</span> ManagedObjectRepository moRepo;

    <span class="text-purple-400">@KafkaListener</span>(
        topics = <span class="text-emerald-300">"cell-reconfiguration-commands"</span>,
        groupId = <span class="text-emerald-300">"usm-provisioning-workers"</span>,
        containerFactory = <span class="text-emerald-300">"manualAckListenerContainerFactory"</span>
    )
    <span class="text-purple-400">public void</span> <span class="text-blue-400">onCellCommand</span>(
            <span class="text-purple-400">@Payload</span> CellCommand cmd,
            <span class="text-purple-400">@Header</span>(KafkaHeaders.RECEIVED_KEY) String cellId,
            Acknowledgment ack) {

        String dedupKey = <span class="text-emerald-300">"idemp:evt:"</span> + cmd.eventId();

        <span class="text-slate-400">// TIER 1: In-Memory Redis Fast-Path Check (&lt;1ms)</span>
        Boolean isFirstArrival = redisTemplate.opsForValue()
                .setIfAbsent(dedupKey, <span class="text-emerald-300">"PROCESSING"</span>, Duration.ofHours(<span class="text-amber-300">24</span>));

        <span class="text-purple-400">if</span> (Boolean.FALSE.equals(isFirstArrival)) {
            log.warn(<span class="text-emerald-300">"Tier-1 Duplicate detected for event {}. Fast ACK and drop."</span>, cmd.eventId());
            ack.acknowledge();
            <span class="text-purple-400">return</span>;
        }

        <span class="text-purple-400">try</span> {
            <span class="text-slate-400">// TIER 2: Atomic Execution within PostgreSQL Transaction</span>
            executeAtomicDatabaseTransaction(cmd);

            redisTemplate.opsForValue().set(dedupKey, <span class="text-emerald-300">"COMMITTED"</span>, Duration.ofHours(<span class="text-amber-300">24</span>));
            ack.acknowledge(); <span class="text-slate-400">// Advance partition offset</span>

        } <span class="text-purple-400">catch</span> (DuplicateEventException ex) {
            log.info(<span class="text-emerald-300">"Tier-2 Duplicate detected in DB uniqueness: {}"</span>, cmd.eventId());
            ack.acknowledge();
        } <span class="text-purple-400">catch</span> (Exception ex) {
            redisTemplate.delete(dedupKey); <span class="text-slate-400">// Allow retry</span>
            <span class="text-purple-400">throw</span> ex; <span class="text-slate-400">// Bubbles to ErrorHandler for exponential backoff & DLT</span>
        }
    }

    <span class="text-purple-400">@Transactional</span>(isolation = Isolation.READ_COMMITTED)
    <span class="text-purple-400">public void</span> <span class="text-blue-400">executeAtomicDatabaseTransaction</span>(CellCommand cmd) {
        <span class="text-purple-400">int</span> inserted = processedEventRepo.insertIgnoreConflict(cmd.eventId(), Instant.now());
        <span class="text-purple-400">if</span> (inserted == <span class="text-amber-300">0</span>) {
            <span class="text-purple-400">throw new</span> DuplicateEventException(<span class="text-emerald-300">"Event already recorded in DB: "</span> + cmd.eventId());
        }
        moRepo.updateTransmitPower(cmd.cellId(), cmd.txPower(), cmd.fencingToken());
    }
}</code></pre>
        """,
        "pitch": """"To eliminate state corruption across 100M consumer rebalance replays, I architected a 2-tier idempotent consumer system paired with the Transactional Outbox pattern. Rather than brittle dual-writes, outbox events commit in the same local ACID transaction as business entities and are captured via Debezium CDC and PostgreSQL WAL tailing. On the consumer side, we enforce strict single-execution semantics: Tier 1 verifies event UUIDs against Redis in sub-milliseconds, filtering 99.9% of replays without database I/O, while Tier 2 anchors commits in PostgreSQL using atomic unique constraints. This guaranteed exact-once business outcomes with zero 2PC lock overhead." """,
        "traps": [
            ("What if a poison pill triggers an unrecoverable exception in your consumer?",
             "We configure Spring Kafka's DefaultErrorHandler with exponential backoff (1s, 2s, 4s). After 3 failed retries, the message is routed to a Dead Letter Topic (DLT) with original partition, offset, and exception stack trace stored in Kafka headers. This prevents partition head-of-line blocking while preserving poison messages for offline forensics."),
            ("Why not just use Kafka's transactional producer (read-process-write)?",
             "Kafka transactions only provide atomicity when reading from Kafka and writing back to another Kafka topic. When the destination is a relational database or external carrier interface, Kafka transactions cannot span across foreign databases without XA, which collapses at 45k TPS. The Outbox pattern + 2-Tier Idempotent consumer is the gold standard for heterogeneous storage boundaries."),
            ("How do you manage disk bloat in the outbox_events table?",
             "We partition outbox_events by day. Once Debezium confirms the LSN has advanced past a partition and messages are acknowledged in Kafka, a lightweight cron script drops old partition segments via ALTER TABLE outbox_events DROP PARTITION in sub-second metadata time, generating zero row-by-row DELETE undo/redo bloat.")
        ],
        "media": [
            ("Chris Richardson: Transactional Outbox Pattern", "https://microservices.io/patterns/data/transactional-outbox.html", "Read Pattern ↗"),
            ("Debezium Architecture & PostgreSQL WAL Tailing", "https://debezium.io/documentation/reference/stable/architecture.html", "Read Debezium Docs ↗"),
            ("Martin Fowler: Idempotent Receiver", "https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html", "Read Fowler Article ↗")
        ]
    },
    {
        "id": "ch4",
        "num": 4,
        "title": "PostgreSQL Recursive CTEs & 3GPP Hierarchy",
        "subtitle": "Slashing Latency from 1,850ms to 45ms across 12-Level Base Station Containment Trees",
        "badge": "Module 4 • Resume Bullet #4",
        "domain": "Relational Graph Optimization",
        "color": "amber",
        "theory": """
          <h3 class="text-base font-bold text-white">The N+1 Disaster in Hierarchical Networks (3GPP Rel-16)</h3>
          <p>
            In carrier-grade 3GPP Element Management Systems (EMS), cellular base stations are modeled as strictly hierarchical trees defined by 3GPP TS 28.622, containing up to 12 levels of containment:
          </p>
          <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-amber-300">
            SubNetwork (Region) &rarr; ManagedElement (gNodeB) &rarr; GNBCUCPFunction &rarr; NRCellCU &rarr; NRCellDU &rarr; NRSectorCarrier &rarr; BWP &rarr; Beamforming &rarr; AntennaArray
          </div>

          <h4 class="text-sm font-bold text-white mt-3">Why Standard ORMs (Spring Data JPA / Hibernate) Fail at Scale</h4>
          <p>
            When an operator opens a 500-cell topology tree, standard JPA entity mappings (<code class="text-amber-300 font-mono">@OneToMany(fetch = FetchType.LAZY)</code>) trigger the <strong>N+1 Query Disaster</strong>:
          </p>
          <ul class="list-disc pl-5 space-y-1 text-xs text-slate-300">
            <li>Query 1 fetches the root <code class="text-amber-300 font-mono">ManagedElement</code>.</li>
            <li>Queries 2 through 501 execute individually across the network as Hibernate navigates child collections level-by-level.</li>
            <li>At an average cross-rack TCP latency of 3.5ms: <span class="font-mono text-rose-400">501 queries &times; 3.5ms = 1,753.5ms network transit latency alone!</span></li>
          </ul>

          <h4 class="text-sm font-bold text-white mt-3">PostgreSQL Recursive CTE Engine Internals & Memory Mechanics</h4>
          <p>
            By migrating to a <strong>Recursive Common Table Expression (<code class="text-amber-300 font-mono">WITH RECURSIVE</code>)</strong>, the entire tree traversal is offloaded from Java memory into PostgreSQL's internal engine:
          </p>
          <ol class="list-decimal pl-5 space-y-1 text-xs text-slate-300">
            <li><strong>Anchor Member:</strong> Evaluates non-recursive term (<code class="text-amber-300 font-mono">WHERE id = :rootId</code>) once, placing rows into the <em>Result Set</em> and internal <strong class="text-amber-300 font-mono">WorkTable</strong>.</li>
            <li><strong>Iterative Recursive Join:</strong> Joins <code class="text-amber-300 font-mono">WorkTable</code> against <code class="text-amber-300 font-mono">managed_objects</code> using an index scan on <code class="text-amber-300 font-mono">parent_id</code>.</li>
            <li><strong>Working Table Swap:</strong> Replaces <code class="text-amber-300 font-mono">WorkTable</code> rows and appends to Result Set until iteration produces 0 rows.</li>
            <li><strong>Single Round-Trip:</strong> Entire 500-node tree returns in <strong>1 single round-trip in 45ms</strong> (a 40x speedup!).</li>
          </ol>

          <h4 class="text-sm font-bold text-white mt-3">Hierarchical Data Model Comparison</h4>
          <div class="overflow-x-auto text-xs mt-2">
            <table class="w-full text-left border-collapse border border-slate-800">
              <thead class="bg-slate-900 text-slate-200">
                <tr><th class="p-2 border border-slate-800">Pattern</th><th class="p-2 border border-slate-800">Read Speed</th><th class="p-2 border border-slate-800">Re-parenting Cost</th><th class="p-2 border border-slate-800">Verdict for Telecom</th></tr>
              </thead>
              <tbody class="divide-y divide-slate-800 text-slate-300">
                <tr><td class="p-2 font-bold text-amber-400">Adjacency List + Recursive CTE (Selected)</td><td class="p-2 text-emerald-400">45ms (In-Memory WorkTable)</td><td class="p-2 text-emerald-400">O(1) Update parent_id</td><td class="p-2">Optimal. Zero write amplification during frequent cell re-parenting.</td></tr>
                <tr><td class="p-2 font-bold text-slate-400">Closure Table</td><td class="p-2 text-emerald-400">O(1) Direct Join</td><td class="p-2 text-rose-400">O(N&sup2;) Write Explosion</td><td class="p-2">Rejected. Re-parenting 1,000 cells locks &gt;100k rows.</td></tr>
                <tr><td class="p-2 font-bold text-slate-400">PostgreSQL ltree</td><td class="p-2 text-emerald-400">O(log N) GiST index</td><td class="p-2 text-rose-400">High String Cascades</td><td class="p-2">Rejected. Materialized path updates lock all downstream descendants.</td></tr>
              </tbody>
            </table>
          </div>
        """,
        "project": """
          <div class="space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-amber-950/20 border border-amber-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">Production Architecture Blueprint • Samsung USM</span>
              <p class="leading-relaxed">
                <strong>Project:</strong> 3GPP Topology Tree Query Service in USM.<br>
                <strong>Scale:</strong> 20M cells nationwide, 12-level hierarchy depth, thousands of concurrent operator queries.<br>
                <strong>Your Role:</strong> Staff Database Architect optimizing relational data access.
              </p>
            </div>

            <h4 class="text-sm font-bold text-white">The Production Crisis (Latency Bottleneck)</h4>
            <p>
              When carrier operators opened base station topology views in the USM console, tree queries took nearly 2 seconds (1,850ms p99 latency). Spring Data JPA executed 501 separate SQL queries sequentially over the network. Database connection pools saturated, query queues backed up, and the frontend web portal froze under concurrent NOC usage.
            </p>

            <h4 class="text-sm font-bold text-white">How You Engineered the Solution</h4>
            <ol class="list-decimal pl-5 space-y-1.5">
              <li><strong>Native Recursive CTE:</strong> Replaced JPA lazy-loading with a single native PostgreSQL <code class="text-amber-300 font-mono">WITH RECURSIVE</code> query that evaluates hierarchy recursion directly inside database memory.</li>
              <li><strong>Composite B-Tree Indexing:</strong> Created a composite index:
                <code class="text-amber-300 font-mono">CREATE INDEX idx_mo_parent_composite ON managed_objects(parent_id, id) INCLUDE (mo_type, administrative_state, operational_state);</code>
                This eliminated table heap lookups during recursive joins.</li>
              <li><strong>Cycle Prevention Guards:</strong> Enforced path tracking via <code class="text-amber-300 font-mono">ARRAY[id]</code> and <code class="text-amber-300 font-mono">WHERE NOT (child.id = ANY(parent.path_tracker))</code> to prevent infinite loops from bad seed scripts.</li>
              <li><strong>Session work_mem Tuning:</strong> Configured dedicated <code class="text-amber-300 font-mono">work_mem = '64MB'</code> for topology read pools, preventing WorkTable disk spills.</li>
            </ol>

            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-emerald-300">
              Verified Metrics to Quote in Interview:<br>
              • Query p99 Latency: Dropped from 1,850ms down to 45ms (a 40x speedup!).<br>
              • Network Round-Trips: Collapsed from 501 network round-trips to exactly 1.<br>
              • Re-parenting Overhead: Remained constant O(1) single-row updates during RAN handovers.
            </div>
          </div>
        """,
        "code": """
<pre><code class="text-slate-300"><span class="text-slate-400">-- PostgreSQL 16 DDL & Indexing + Recursive CTE Query</span>
<span class="text-purple-400">CREATE TABLE</span> managed_objects (
    id <span class="text-purple-400">BIGSERIAL PRIMARY KEY</span>,
    parent_id <span class="text-purple-400">BIGINT REFERENCES</span> managed_objects(id) <span class="text-purple-400">ON DELETE CASCADE</span>,
    distinguished_name <span class="text-purple-400">VARCHAR</span>(<span class="text-amber-300">512</span>) <span class="text-purple-400">NOT NULL</span>,
    mo_type <span class="text-purple-400">VARCHAR</span>(<span class="text-amber-300">64</span>) <span class="text-purple-400">NOT NULL</span>,
    administrative_state <span class="text-purple-400">VARCHAR</span>(<span class="text-amber-300">32</span>) <span class="text-purple-400">NOT NULL DEFAULT</span> <span class="text-emerald-300">'UNLOCKED'</span>,
    operational_state <span class="text-purple-400">VARCHAR</span>(<span class="text-amber-300">32</span>) <span class="text-purple-400">NOT NULL DEFAULT</span> <span class="text-emerald-300">'ENABLED'</span>,
    fencing_token <span class="text-purple-400">BIGINT NOT NULL DEFAULT</span> <span class="text-amber-300">1</span>,
    attributes <span class="text-purple-400">JSONB NOT NULL DEFAULT</span> <span class="text-emerald-300">'{}'</span>,
    updated_at <span class="text-purple-400">TIMESTAMPTZ NOT NULL DEFAULT NOW</span>()
);

<span class="text-slate-400">-- Composite Index: Eliminates heap lookups during recursive join iterations</span>
<span class="text-purple-400">CREATE INDEX</span> idx_mo_parent_composite <span class="text-purple-400">ON</span> managed_objects(parent_id, id)
    <span class="text-purple-400">INCLUDE</span> (mo_type, administrative_state, operational_state);

<span class="text-slate-400">-- High-Performance 1-Round-Trip Recursive CTE Query</span>
<span class="text-purple-400">WITH RECURSIVE</span> mo_hierarchy <span class="text-purple-400">AS</span> (
    <span class="text-slate-400">-- ANCHOR: Seed with target root node</span>
    <span class="text-purple-400">SELECT</span> id, parent_id, distinguished_name, mo_type, administrative_state, operational_state,
           <span class="text-amber-300">1</span> <span class="text-purple-400">AS</span> depth, <span class="text-purple-400">ARRAY</span>[id] <span class="text-purple-400">AS</span> path_tracker
    <span class="text-purple-400">FROM</span> managed_objects 
    <span class="text-purple-400">WHERE</span> id = :targetRootMoId

    <span class="text-purple-400">UNION ALL</span>

    <span class="text-slate-400">-- RECURSIVE MEMBER: Iteratively join children using composite index</span>
    <span class="text-purple-400">SELECT</span> child.id, child.parent_id, child.distinguished_name, child.mo_type,
           child.administrative_state, child.operational_state,
           parent.depth + <span class="text-amber-300">1</span>, parent.path_tracker || child.id
    <span class="text-purple-400">FROM</span> managed_objects child
    <span class="text-purple-400">INNER JOIN</span> mo_hierarchy parent <span class="text-purple-400">ON</span> child.parent_id = parent.id
    <span class="text-purple-400">WHERE</span> parent.depth &lt; <span class="text-amber-300">15</span> 
      <span class="text-purple-400">AND NOT</span> (child.id = <span class="text-purple-400">ANY</span>(parent.path_tracker)) <span class="text-slate-400">-- Cycle Guard</span>
)
<span class="text-purple-400">SELECT</span> * <span class="text-purple-400">FROM</span> mo_hierarchy <span class="text-purple-400">ORDER BY</span> depth <span class="text-purple-400">ASC</span>, id <span class="text-purple-400">ASC</span>;</code></pre>
        """,
        "pitch": """"In Samsung's 4G/5G Element Management System, base stations are modeled as 12-level 3GPP containment hierarchies. Our legacy Spring Data JPA implementation suffered from severe N+1 query degradation, firing 501 separate SQL queries across the network to render a 500-cell topology tree, resulting in an unacceptable 1,850ms p99 latency. I architected our database layer migration to PostgreSQL Recursive Common Table Expressions paired with a composite B-tree index on (parent_id, id). By offloading tree recursion into PostgreSQL's in-memory WorkTable buffer, we collapsed 501 network round-trips into a single round-trip, dropping p99 latency from 1,850ms to 45ms (a 40x speedup) with zero write amplification during cell re-parenting." """,
        "traps": [
            ("What happens if a recursive CTE intermediate result set exceeds PostgreSQL's work_mem?",
             "If the intermediate working table exceeds work_mem, PostgreSQL spills the execution set to on-disk temporary files in base/pgsql_tmp. This converts fast RAM buffer scans into high-latency disk I/O, causing latency to spike from 45ms to >800ms. We prevented disk spills by sizing work_mem = '64MB' for our database connection pool sessions and enforcing an explicit recursion limit of depth < 15."),
            ("Why not use Closure Tables or Postgres ltree extension?",
             "Closure Tables introduce O(N^2) space overhead and severe write amplification during tree re-parenting. In carrier networks, cells frequently move between base station controllers during load balancing. Re-parenting a 1,000-cell branch with Closure Tables requires deleting and re-inserting tens of thousands of closure paths under exclusive locks. ltree requires cascading updates to all descendant materialized paths. Adjacency lists with Recursive CTEs require updating only 1 single parent_id foreign key in O(1) time with zero write lock cascading."),
            ("How do you detect and stop cyclic graphs if bad operator scripts introduce circular parent-child links?",
             "We construct an array of visited IDs in the CTE projection: ARRAY[id] AS path_tracker. In the recursive term, we append child IDs (parent.path_tracker || child.id) and include an explicit guard: WHERE NOT (child.id = ANY(parent.path_tracker)). If a cycle is encountered, the join condition evaluates to false and iteration immediately halts without throwing an error or hanging the database engine.")
        ],
        "media": [
            ("Hussein Nasser: Recursive CTEs in PostgreSQL", "https://www.youtube.com/watch?v=n5y-X818L64", "Watch Video ↗"),
            ("PostgreSQL 16 Official Docs: Common Table Expressions", "https://www.postgresql.org/docs/current/queries-with.html", "Read Docs ↗"),
            ("3GPP TS 28.622 Specification: Generic Network Resource Model", "https://www.3gpp.org/DynaReport/28622.htm", "View 3GPP Spec ↗")
        ]
    },
    {
        "id": "ch5",
        "num": 5,
        "title": "Air-Gapped Zero-GPU Edge RAG & Resilient DOM",
        "subtitle": "4-Bit Quantization (GGUF), AVX-512 VNNI, NUMA Pinning, and Self-Healing Automation",
        "badge": "Module 5 • Resume Bullet #5 & IEEE Paper",
        "domain": "Zero-GPU Edge AI & Resilient Automation",
        "color": "cyan",
        "theory": """
          <h3 class="text-base font-bold text-white">The Memory-Bandwidth Bottleneck of LLM Inference</h3>
          <p>
            In carrier-grade telecommunications, Tier-1 operators (AT&T, Verizon, Jio) operate strictly air-gapped SCADA/EMS data centers. Egress internet access is physically disconnected, and transmitting proprietary network topologies to public cloud LLM APIs is strictly prohibited by federal compliance and national security rules. Furthermore, enterprise GPUs (Nvidia A100/H100) are unavailable on edge telecom servers due to strict power, thermal, and rack footprint budgets.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">Why Autoregressive Generation is Memory-Bandwidth Bound (Not Compute Bound)</h4>
          <p>
            In autoregressive token generation (decode phase, batch size 1), computational intensity is tiny (~1 FLOP/byte). To generate a single output token, the CPU must stream <em>every single parameter</em> of the model from DRAM through CPU cache hierarchies into vector registers:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs font-mono text-cyan-300">
            <div>Inference Speed (tokens/sec) &asymp; DRAM Memory Bandwidth (GB/s) &divide; Model Footprint (GB)</div>
            <div class="text-slate-400 mt-2 font-sans">On a Dual-Channel DDR4-3200 Intel Xeon server (Effective Bandwidth &asymp; 45 GB/s):</div>
            <div class="text-rose-400">• Unquantized FP16 (Qwen2.5-7B): 14.4 GB &divide; 45 GB/s &asymp; 3.1 tok/sec (Laggy, breaks real-time interactive UX).</div>
            <div class="text-emerald-400">• 4-Bit GGUF (Q4_K_M): 4.2 GB &divide; 45 GB/s &asymp; 11.8 - 12.5 tok/sec (Fluid interactive speed, matches natural human reading pace!).</div>
          </div>

          <h4 class="text-sm font-bold text-white mt-3">Affine Block Quantization Mathematics (GGUF Q4_K_M)</h4>
          <p>
            Quantization maps 16-bit floating-point weights ($w \in \mathbb{R}$) into discrete 4-bit integers ($q \in [-8, 7]$):
          </p>
          <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300">
            Quantization: &nbsp; &nbsp;q = round( w / s ) + z<br>
            Dequantization: &nbsp;w&#770; = s &times; ( q - z )<br>
            Where Scale (s) = (w_max - w_min) / (2^b - 1), &nbsp; Zero-Point (z) = round( -w_min / s )
          </div>
          <p class="text-xs text-slate-300">
            GGUF uses <strong>Block Quantization (k-quants)</strong>: weights are partitioned into small blocks of 32 or 256 parameters, each with independent scale factors. W4A16 keeps activations in FP16, preserving 99.2% of full-precision accuracy on specialized telecom acronyms (gNodeB, AMF, UPF, PDCP, RLC).
          </p>

          <h4 class="text-sm font-bold text-white mt-3">Hardware Acceleration & 3-Tier Resilient Self-Healing DOM Locators</h4>
          <ul class="list-disc pl-5 space-y-1.5 text-xs text-slate-300">
            <li><strong>AVX-512 VNNI Vectorization:</strong> Executes four 8-bit integer dot products in a single CPU cycle.</li>
            <li><strong>NUMA Core Pinning:</strong> Pinning worker threads to physical cores on a single NUMA socket via <code class="text-cyan-300 font-mono">taskset</code> eliminates cross-socket UPI interconnect latency and L3 cache thrashing.</li>
            <li><strong>3-Tier Self-Healing DOM Locators:</strong> Tier 1 Semantic Data Attributes &rarr; Tier 2 ARIA & Text Heuristic &rarr; Tier 3 Relative Structural XPath, with automated telemetry emitting self-healing locator patches.</li>
          </ul>
        """,
        "project": """
          <div class="space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-cyan-950/20 border border-cyan-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider block">Production Architecture Blueprint • Samsung & IEEE Publication</span>
              <p class="leading-relaxed">
                <strong>Project:</strong> Air-Gapped AI Network Operator Assistant & Resilient Automation Suite.<br>
                <strong>Constraints:</strong> Zero GPU availability on commodity edge servers, strictly air-gapped data centers, weekly frontend portal UI redesigns.<br>
                <strong>Your Role:</strong> Principal AI/Systems Architect (published in IEEE for novel edge architecture).
              </p>
            </div>

            <h4 class="text-sm font-bold text-white">The Production Crisis (Air-Gap Constraint)</h4>
            <p>
              Telecom operators needed an intelligent natural language assistant to query 3GPP TS 28.622 standards and automate element provisioning. However, cloud LLM APIs were legally forbidden due to national defense and carrier compliance. Running unquantized open-source LLMs on edge Intel Xeon CPUs crawled at 3 tokens per second, making the system unusable. Furthermore, weekly EMS frontend portal updates constantly broke static Selenium test locators.
            </p>

            <h4 class="text-sm font-bold text-white">How You Engineered the Solution</h4>
            <ol class="list-decimal pl-5 space-y-1.5">
              <li><strong>4-Bit GGUF Quantization:</strong> Quantized Qwen2.5-7B to 4-bit GGUF (Q4_K_M), shrinking memory footprint from 14.4GB to 4.2GB and accelerating token generation from 3.1 to 12.5 tok/sec on commodity DDR4 RAM.</li>
              <li><strong>NUMA Thread Affinity & AVX-512:</strong> Configured llama.cpp with AVX-512 VNNI vectorization and pinned 4 inference threads to physical cores on a single NUMA node, cutting inter-token jitter by 93%.</li>
              <li><strong>ONNX Embeddings & Cosine Thresholding:</strong> Deployed quantized <code class="text-cyan-300 font-mono">all-MiniLM-L6-v2</code> (22MB, 8ms CPU latency) with ChromaDB HNSW vector index, rejecting queries with cosine similarity &lt; 0.72 to prevent hallucinations on safety-critical cell power settings.</li>
              <li><strong>3-Tier Resilient Self-Healing DOM Engine:</strong> Implemented a 3-tier cascade (Semantic &rarr; Text Heuristic &rarr; Structural XPath) with telemetry self-healing, slashing test automation maintenance by 90%.</li>
            </ol>

            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-emerald-300">
              Verified Metrics to Quote in Interview:<br>
              • Token Generation Speed: 12.5 tokens/sec on Intel Xeon CPU (zero GPUs used).<br>
              • Hallucination Rate: Dropped to &lt;0.1% via strict 0.72 cosine distance thresholding.<br>
              • Automation Resilience: 90% reduction in weekly broken UI locator incidents.
            </div>
          </div>
        """,
        "code": """
<pre><code class="text-slate-300"><span class="text-slate-400"># Python FastAPI Air-Gapped RAG Server (llama-cpp + ONNX Runtime)</span>
<span class="text-purple-400">import</span> os
<span class="text-purple-400">from</span> fastapi <span class="text-purple-400">import</span> FastAPI
<span class="text-purple-400">from</span> pydantic <span class="text-purple-400">import</span> BaseModel
<span class="text-purple-400">from</span> llama_cpp <span class="text-purple-400">import</span> Llama
<span class="text-purple-400">import</span> chromadb
<span class="text-purple-400">from</span> chromadb.utils <span class="text-purple-400">import</span> embedding_functions

app = FastAPI(title=<span class="text-emerald-300">"Air-Gapped Edge RAG Engine"</span>)

<span class="text-slate-400"># NUMA Pinning & AVX-512 optimization</span>
os.environ[<span class="text-emerald-300">"OMP_NUM_THREADS"</span>] = <span class="text-emerald-300">"4"</span>
os.environ[<span class="text-emerald-300">"KMP_AFFINITY"</span>] = <span class="text-emerald-300">"granularity=fine,compact,1,0"</span>

<span class="text-slate-400"># 4-Bit GGUF Qwen2.5-7B (4.2GB RAM footprint; 12.5 tok/sec on DDR4 Xeon)</span>
llm = Llama(
    model_path=<span class="text-emerald-300">"/opt/models/qwen2.5-7b-instruct-q4_k_m.gguf"</span>,
    n_ctx=<span class="text-amber-300">4096</span>,
    n_threads=<span class="text-amber-300">4</span>,
    use_mmap=<span class="text-purple-400">True</span>,
    use_mlock=<span class="text-purple-400">True</span>  <span class="text-slate-400"># Lock weights in DRAM to prevent OS swapping</span>
)

emb_fn = embedding_functions.ONNXMiniLM_L6_V2(preferred_providers=[<span class="text-emerald-300">"CPUExecutionProvider"</span>])
chroma_client = chromadb.PersistentClient(path=<span class="text-emerald-300">"/opt/chroma_telecom_db"</span>)
collection = chroma_client.get_or_create_collection(
    name=<span class="text-emerald-300">"3gpp_standards_corpus"</span>, embedding_function=emb_fn,
    metadata={<span class="text-emerald-300">"hnsw:space"</span>: <span class="text-emerald-300">"cosine"</span>}
)

<span class="text-purple-400">class</span> <span class="text-blue-400">RAGQuery</span>(BaseModel):
    prompt: str

<span class="text-purple-400">@app.post</span>(<span class="text-emerald-300">"/v1/telecom/rag"</span>)
<span class="text-purple-400">def</span> <span class="text-blue-400">query_rag</span>(query: RAGQuery):
    results = collection.query(query_texts=[query.prompt], n_results=<span class="text-amber-300">3</span>)
    cosine_sim = <span class="text-amber-300">1.0</span> - results[<span class="text-emerald-300">'distances'</span>][<span class="text-amber-300">0</span>][<span class="text-amber-300">0</span>]
    
    <span class="text-slate-400"># Guardrail: Reject low-confidence matches to prevent hallucinations</span>
    <span class="text-purple-400">if</span> cosine_sim &lt; <span class="text-amber-300">0.72</span>:
        <span class="text-purple-400">return</span> {<span class="text-emerald-300">"status"</span>: <span class="text-emerald-300">"REJECTED"</span>, <span class="text-emerald-300">"reason"</span>: <span class="text-emerald-300">"Low confidence similarity (&lt;0.72). Preventing hallucination."</span>}

    retrieved = <span class="text-emerald-300">"\\n"</span>.join(results[<span class="text-emerald-300">'documents'</span>][<span class="text-amber-300">0</span>])
    sys_prompt = f<span class="text-emerald-300">"Strictly answer using context:\\n{retrieved}\\n\\nQuestion: {query.prompt}"</span>
    resp = llm(sys_prompt, max_tokens=<span class="text-amber-300">512</span>, temperature=<span class="text-amber-300">0.1</span>)
    <span class="text-purple-400">return</span> {<span class="text-emerald-300">"status"</span>: <span class="text-emerald-300">"SUCCESS"</span>, <span class="text-emerald-300">"answer"</span>: resp[<span class="text-emerald-300">"choices"</span>][<span class="text-amber-300">0</span>][<span class="text-emerald-300">"text"</span>], <span class="text-emerald-300">"confidence"</span>: cosine_sim}</code></pre>
        """,
        "pitch": """"Because Tier-1 telecom operators operate strictly air-gapped data centers with zero egress internet access and zero GPU infrastructure, commercial cloud LLM APIs were legally forbidden. I designed and deployed an air-gapped, zero-GPU RAG assistant running on commodity Intel Xeon CPUs. By quantizing Qwen2.5-7B to 4-bit GGUF (Q4_K_M) and pinning inference threads to single NUMA sockets with AVX-512 VNNI instructions, we shrank the memory footprint from 14.4GB down to 4.2GB, cutting DRAM transfer latency and accelerating token generation from 3.1 tok/sec to a fluid 12.5 tok/sec conversational assistant. We coupled this with a 3-tier resilient self-healing DOM automation locator engine, reducing automation script breakages by 90% across weekly telecom web portal updates." """,
        "traps": [
            ("Why use W4A16 instead of full W4A4 quantization if memory bandwidth is the primary bottleneck?",
             "In autoregressive generation with batch size 1, model weights account for >99% of total memory traffic per token, while activations contribute <1%. Quantizing activations to 4-bit (W4A4) yields negligible additional throughput gain, but causes catastrophic perplexity degradation on specialized 3GPP acronyms and command syntax. W4A16 retains 99.2% of FP16 accuracy while achieving the exact same memory-bandwidth speedup."),
            ("How do you prevent hallucinations in air-gapped RAG when generating 3GPP cell configuration commands?",
             "We enforce a strict 2-tier guardrail. First, at vector retrieval, we calculate cosine similarity using quantized ONNX embeddings: if the top chunk similarity is below 0.72, the query is rejected immediately with a low-confidence warning rather than hallucinating. Second, the model output is passed through an AST-based JSON/CLI schema validator that verifies generated cell parameters against 3GPP TS 28.622 allowable ranges before presenting them to the network operator."),
            ("Why did you choose GGUF / llama.cpp over vLLM or Ollama for carrier edge deployments?",
             "vLLM is heavily optimized for high-concurrency multi-tenant GPU batching using PagedAttention, but performs poorly on single-batch CPU inference. Ollama bundles background daemon dependencies that violate strict carrier security whitelisting. GGUF with llama.cpp is a standalone, single-binary C/C++ engine with zero external dependencies, native AVX-512 VNNI vectorization, mlock memory locking, and explicit NUMA thread affinity, making it ideal for certified telecom edge environments.")
        ],
        "media": [
            ("Andrej Karpathy: State of LLMs & Inference Physics", "https://www.youtube.com/watch?v=zjkBMFhNj_g", "Watch Video ↗"),
            ("Tim Dettmers: QLoRA & 4-bit Quantization Fundamentals", "https://arxiv.org/abs/2305.14314", "Read Paper ↗"),
            ("llama.cpp GGUF Binary Container Specification", "https://github.com/ggerganov/ggml/blob/master/docs/gguf.md", "View GGUF Spec ↗")
        ]
    },
    {
        "id": "ch6",
        "num": 6,
        "title": "5G Telecom Domain & Google SRE Incident Command",
        "subtitle": "CU/DU/RU Disaggregation, Five Nines Mathematics, and Multi-Window Burn Rates",
        "badge": "Module 6 • Telecom Domain & SRE Production Readiness",
        "domain": "Mission-Critical 99.999% Reliability",
        "color": "rose",
        "theory": """
          <h3 class="text-base font-bold text-white">5G Disaggregated RAN Architecture (3GPP Rel-16)</h3>
          <p>
            In modern 3GPP Release 16/17 telecommunications, traditional monolithic base stations have been completely disaggregated into modular network functions connected over standardized interfaces:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs mt-2">
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <span class="font-bold text-rose-400 block mb-1">Centralized Unit (CU)</span>
              <p class="text-slate-400 text-[11px]">Hosts non-real-time L2/L3 stacks. Split into <strong>CU-CP</strong> (Control Plane: RRC, PDCP-C) and <strong>CU-UP</strong> (User Plane: SDAP, PDCP-U) via the 3GPP <strong>E1 Interface</strong>.</p>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <span class="font-bold text-rose-400 block mb-1">Distributed Unit (DU)</span>
              <p class="text-slate-400 text-[11px]">Hosts real-time latency-critical layers (RLC, MAC, High-PHY). Connected to CU via 3GPP <strong>F1 Interface</strong> (Midhaul latency budget &le; 10ms).</p>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <span class="font-bold text-rose-400 block mb-1">Radio Unit (RU)</span>
              <p class="text-slate-400 text-[11px]">Low-PHY, beamforming, and RF antenna arrays. Connected to DU via <strong>eCPRI</strong> over O-RAN 7.2x split (strict sub-100&mu;s latency budget).</p>
            </div>
          </div>

          <h4 class="text-sm font-bold text-white mt-3">The Mathematical Rigor of "Five Nines" (99.999% Availability)</h4>
          <p>
            Carrier-grade network infrastructure SLA contracts mandate five nines availability across nationwide deployments:
          </p>
          <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-rose-300">
            Annual Allowed Downtime = ( 1.0 - 0.99999 ) &times; 365.2425 days &times; 86,400 sec<br>
            = <span class="font-bold">315.57 seconds &asymp; 5.26 minutes per year</span> across all 20M cell sectors!
          </div>

          <h4 class="text-sm font-bold text-white mt-3">Google SRE Multi-Window Multi-Burn-Rate Alerting Mathematics</h4>
          <p>
            Traditional static threshold alerting creates catastrophic operational failure: false positives cause alert fatigue, while subtle slow leaks consume 50% of the error budget before notification. Google SRE solves this by alerting on <strong>SLO Error Budget Burn Rates</strong>:
          </p>
          <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
            <div class="font-mono text-rose-400 font-bold">Burn Rate Equation: Burn Rate (B) = Observed Error Rate &divide; ( 1 - SLO )</div>
            <ul class="list-disc pl-5 space-y-1 text-slate-300">
              <li><strong>Burn Rate B = 1.0:</strong> Exactly consumes 100% of the budget in 30 days (720 hours).</li>
              <li><strong>Burn Rate B = 14.4:</strong> Consumes 2% of the total monthly error budget in exactly 1 hour.</li>
            </ul>
          </div>

          <h4 class="text-sm font-bold text-white mt-3">The Dual-Window Defense: Eliminating False Positives and Reset Lag</h4>
          <ul class="list-disc pl-5 space-y-1 text-xs text-slate-300">
            <li><strong>Page (Critical On-Call):</strong> 1-hour window burning at 14.4x <strong>AND</strong> 5-minute confirmation window burning at 14.4x. Pages within 2 minutes of a real outage, and auto-resets immediately when healthy traffic resumes.</li>
            <li><strong>Ticket (Subtle Slow Burn):</strong> 6-hour window burning at 6.0x (5% budget consumed) <strong>AND</strong> 30-minute confirmation window burning at 6.0x. Catches slow degradations before budget exhaustion.</li>
          </ul>
        """,
        "project": """
          <div class="space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block">Production Architecture Blueprint • Samsung USM</span>
              <p class="leading-relaxed">
                <strong>Project:</strong> SRE Incident Command & Alarm Correlation Engine in Samsung USM.<br>
                <strong>Scale:</strong> 20M cell towers, 99.999% SLA (5.26 min allowed downtime/year), 100k alarms/sec optical cut bursts.<br>
                <strong>Your Role:</strong> Staff Reliability Architect & Incident Commander.
              </p>
            </div>

            <h4 class="text-sm font-bold text-white">The Production Crisis (Alert Storm & Downtime Threat)</h4>
            <p>
              When a backhaul fiber optic trunk was cut in a major metro market, over 100,000 raw alarms per second flooded into the USM operations console (Loss of Signal, Sync Lost, BGP Flap, Cell Out of Service, NGAP link down). NOC dashboards crashed under the payload, and on-call engineers were bombarded with 5,000 PagerDuty alerts, obscuring the root cause and threatening the 5-minute annual downtime SLA limit.
            </p>

            <h4 class="text-sm font-bold text-white">How You Engineered the Solution</h4>
            <ol class="list-decimal pl-5 space-y-1.5">
              <li><strong>Google SRE Multi-Burn-Rate Rules:</strong> Migrated from naive 5-minute threshold alerts to Prometheus multi-window multi-burn-rate rules (1h 14.4x + 5m confirmation window for pages; 6h 6x + 30m window for tickets).</li>
              <li><strong>Kafka Streams Graph Reduction:</strong> Engineered an in-memory streaming correlator that grouped incoming alarms by ancestor Equipment DN within a 5-second tumbling window, suppressing 99.8% of downstream secondary alarms.</li>
              <li><strong>Root Cause Dispatch:</strong> Collapsed 100,000 secondary leaf alarms into 1 single high-priority dispatch ticket ("FIBER_CUT_BACKHAUL_TRUNK_A"), immediately directing field crews to the exact physical cut location.</li>
              <li><strong>Blameless Post-Mortem Standard:</strong> Established blameless post-mortem protocols analyzing TTDetect, TTAcknowledge, and TTMitigate with automated CI/CD canary gates.</li>
            </ol>

            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-emerald-300">
              Verified Metrics to Quote in Interview:<br>
              • Alarm Reduction: 99.8% noise reduction during major backhaul optical fiber cuts.<br>
              • Incident Detection Latency: Paged on-call command within 2 minutes of active budget burn.<br>
              • SLA Record: Zero nationwide five nines SLA contractual breaches across 20M cells.
            </div>
          </div>
        """,
        "code": """
<pre><code class="text-slate-300"><span class="text-slate-400"># Prometheus Multi-Window Multi-Burn-Rate Alerting (alerting_rules.yml)</span>
groups:
  - name: telecom_sre_slo_alerts
    rules:
      <span class="text-slate-400"># SEVERITY 1 PAGE: 1h window (14.4x) AND 5m window confirms active outage</span>
      - alert: CellProvisioningErrorBudgetBurn_CriticalPage
        expr: |
          (
            (sum(rate(http_requests_total{job="usm-cell-service", status=~"5.."}[1h])) 
             / sum(rate(http_requests_total{job="usm-cell-service"}[1h]))) > (14.4 * (1 - 0.9999))
          )
          AND
          (
            (sum(rate(http_requests_total{job="usm-cell-service", status=~"5.."}[5m])) 
             / sum(rate(http_requests_total{job="usm-cell-service"}[5m]))) > (14.4 * (1 - 0.9999))
          )
        for: 2m
        labels:
          severity: page
          tier: mission_critical
        annotations:
          summary: "Cell Service burning 2% error budget in 1 hour (14.4x rate)"

      <span class="text-slate-400"># SEVERITY 2 TICKET: 6h window (6.0x) AND 30m window confirms slow burn</span>
      - alert: CellProvisioningErrorBudgetBurn_SlowTicket
        expr: |
          (
            (sum(rate(http_requests_total{job="usm-cell-service", status=~"5.."}[6h])) 
             / sum(rate(http_requests_total{job="usm-cell-service"}[6h]))) > (6.0 * (1 - 0.9999))
          )
          AND
          (
            (sum(rate(http_requests_total{job="usm-cell-service", status=~"5.."}[30m])) 
             / sum(rate(http_requests_total{job="usm-cell-service"}[30m]))) > (6.0 * (1 - 0.9999))
          )
        for: 15m
        labels:
          severity: ticket
          tier: mission_critical</code></pre>
        """,
        "pitch": """"In carrier telecommunications, five nines availability means an element management system governing 20 million cell sectors can suffer no more than 5.26 minutes of cumulative downtime per year. To safeguard this SLA without succumbing to alert fatigue, I implemented Google SRE multi-window multi-burn-rate alerting in Prometheus. By mathematically coupling a 1-hour window burning at 14.4x rate with a 5-minute confirmation window, we page on-call engineering in under 2 minutes when 2% of the error budget is consumed, while auto-resolving immediately when traffic recovers. To prevent dashboard collapse during optical fiber cuts, I engineered a Kafka Streams graph reduction engine that collapses 100,000 secondary alarms per second into a single root cause incident within a 5-second tumbling window, maintaining zero nationwide P0 outages." """,
        "traps": [
            ("Why do you need both a 1-hour window AND a 5-minute confirmation window in burn rate alerting?",
             "Using a 1-hour window alone causes alert reset lag: if an outage lasts 5 minutes and recovers, the 1-hour average error rate remains high, keeping the engineer paged for 55 minutes of false alarm. The 5-minute short window confirms that the outage is still actively happening right now. Once the issue is resolved, the 5-minute window immediately clears and automatically resolves the page, eliminating alert fatigue."),
            ("How do you handle 100,000 alarms per second during an optical fiber cut without blowing up Kafka Streams memory?",
             "We use RocksDB-backed state stores with strict memory bounds and in-memory RocksDB block caches. Alarms are re-keyed by ancestor Equipment DN derived from the local 3GPP topological cache. The stream window uses 5-second tumbling windows with no grace period, aggregating secondary alarms into a compact bitmask aggregate. Once the root cause is flagged, downstream leaf alarms within the same window are discarded in-memory, cutting outbound network egress by 99.8%."),
            ("How do you conduct a Blameless Post-Mortem following an L6/L8 infrastructure outage?",
             "We follow Google's SRE Blameless Post-Mortem standard. We focus on process, tooling, and environmental systemic causes rather than human error. We construct an exact second-by-second timeline (Time-to-Detect, Time-to-Acknowledge, Time-to-Mitigate), calculate exact Error Budget burned, perform 5-Whys analysis, and commit actionable preventive work items with assigned owners to CI/CD automated gates, canary analysis, and synthetic probes.")
        ],
        "media": [
            ("Google SRE Workbook: Alerting on SLOs", "https://sre.google/workbook/alerting-on-slos/", "Read SRE Book ↗"),
            ("3GPP TS 38.401: NG-RAN Architecture & CU/DU/F1/E1 Specs", "https://www.3gpp.org/DynaReport/38401.htm", "View 3GPP Spec ↗"),
            ("O-RAN Alliance Fronthaul Working Group 4 Specifications", "https://www.o-ran.org/specifications", "Read O-RAN Specs ↗")
        ]
    },
    {
        "id": "ch7",
        "num": 7,
        "title": "Streaming Data Pipelines & Oracle VLDB (Cognizant)",
        "subtitle": "StAX Pull Cursors, JVM Object Headers, and Oracle 19c Direct-Path Partitioning",
        "badge": "Module 7 • Cognizant Project & Big Data Engineering",
        "domain": "High-Throughput Batch & Stream ETL",
        "color": "teal",
        "theory": """
          <h3 class="text-base font-bold text-white">The DOM OOM Disaster vs StAX O(1) Pull Cursor Architecture</h3>
          <p>
            In enterprise financial clearing and settlement pipelines (Cognizant project domain), large XML/JSON transaction feeds ranging from 2GB to 20GB must be ingested within strict batch maintenance windows. The legacy pipeline relied on standard DOM tree parsers (<code class="text-teal-300 font-mono">DocumentBuilderFactory</code>), which suffered catastrophic <code class="text-rose-400 font-mono">OutOfMemoryError: Java heap space</code> crashes and 6-hour execution times.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">JVM Object Header Anatomy & The 12.5x DOM Expansion Explosion</h4>
          <p>
            On a 64-bit HotSpot JVM, every single object instance incurs mandatory physical memory layout overhead (Java Object Layout / JOL):
          </p>
          <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 font-mono text-xs text-teal-300 space-y-1">
            <div>• Mark Word: 8 bytes (Lock bits, biased locking, identity hash code, 4-bit GC age)</div>
            <div>• Klass Pointer: 4 bytes (under Compressed OOPs <code class="text-amber-300">-XX:+UseCompressedOops</code>) or 8 bytes</div>
            <div>• Padding: 4 bytes (enforces 8-byte boundary alignment)</div>
            <div class="text-rose-400 font-bold">&rarr; Minimum 16 bytes for every single empty Object header on the JVM heap!</div>
          </div>
          <p class="text-xs text-slate-300">
            A DOM parser constructs an in-memory n-ary tree where every XML element instantiates an <code class="text-teal-300 font-mono">ElementImpl</code>, <code class="text-teal-300 font-mono">NodeListImpl</code>, <code class="text-teal-300 font-mono">NamedNodeMapImpl</code>, and multiple <code class="text-teal-300 font-mono">String</code> arrays. A 2GB XML document with 80 million elements expands into <strong>&gt;25GB of live heap memory (a 12.5x memory expansion!)</strong>, causing 15-second Stop-The-World GC pauses and fatal OOM crashes.
          </p>

          <h4 class="text-sm font-bold text-white mt-3">The StAX Pull Cursor Model ($O(1)$ Constant Memory)</h4>
          <p>
            StAX (<code class="text-teal-300 font-mono">XMLStreamReader</code>) operates as an on-demand pull cursor directly over the raw byte stream (<code class="text-teal-300 font-mono">InputStream</code>). As each record finishes parsing, it is mapped into a lightweight Java 21 Record DTO, added to a JDBC batch buffer, and immediately marked eligible for Young Gen garbage collection. Memory consumption remains strictly bounded at <strong>&lt;50MB RAM constant</strong> regardless of file size!
          </p>

          <h4 class="text-sm font-bold text-white mt-3">Oracle 19c Direct-Path Insert (/*+ APPEND */) & TM Mode 6 Locks</h4>
          <p>
            Direct-Path Insert bypasses the SGA Database Buffer Cache completely, formatting data blocks directly in session PGA and writing straight to disk datafiles above the High Water Mark (HWM). By bypassing undo logging for table blocks, write throughput accelerates by 10x-20x.
            Because Direct-Path acquires an exclusive <strong>TM Mode 6 (Table Lock - Exclusive)</strong>, we load into unpartitioned staging tables, then perform a sub-second metadata partition exchange:
            <code class="text-teal-300 font-mono">ALTER TABLE claims EXCHANGE PARTITION p_current WITH TABLE claims_staging INCLUDING INDEXES WITHOUT VALIDATION</code>.
          </p>
        """,
        "project": """
          <div class="space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-teal-950/20 border border-teal-900/40 rounded-xl space-y-2">
              <span class="text-xs font-bold text-teal-400 uppercase tracking-wider block">Production Architecture Blueprint • Cognizant Financial Ingestion</span>
              <p class="leading-relaxed">
                <strong>Project:</strong> High-Throughput Financial Settlement & Claims Ingestion Pipeline.<br>
                <strong>Scale:</strong> Daily 2GB to 20GB XML transaction feeds, strict 2-hour overnight SLA window.<br>
                <strong>Your Role:</strong> Lead Big Data / Java Architect re-engineering the ingestion engine.
              </p>
            </div>

            <h4 class="text-sm font-bold text-white">The Production Crisis (Batch Window Breach & OOM)</h4>
            <p>
              The legacy pipeline parsed daily XML feeds using DOM tree builders. Whenever incoming files exceeded 2GB, the JVM heap exceeded 25GB, triggering prolonged GC pauses and crashing with <code class="text-rose-400 font-mono">OutOfMemoryError: Java heap space</code>. Batch jobs took over 6 hours, routinely breaching financial market open SLAs and incurring financial SLA penalties.
            </p>

            <h4 class="text-sm font-bold text-white">How You Engineered the Solution</h4>
            <ol class="list-decimal pl-5 space-y-1.5">
              <li><strong>StAX Pull Streaming:</strong> Replaced DOM with a StAX pull cursor (<code class="text-teal-300 font-mono">XMLStreamReader</code>), streaming records token-by-token directly from the input stream with a strictly bounded 50MB RAM footprint.</li>
              <li><strong>JDBC Chunked Batching:</strong> Buffered records in batches of 5,000, dispatching to Oracle via <code class="text-teal-300 font-mono">PreparedStatement.addBatch()</code> and periodic transaction commits.</li>
              <li><strong>Oracle Direct-Path Ingestion:</strong> Utilized Direct-Path Insert (<code class="text-teal-300 font-mono">/*+ APPEND */</code>) writing directly above the High Water Mark, bypassing buffer cache contention and undo generation.</li>
              <li><strong>Partition Exchange Architecture:</strong> Loaded into unpartitioned staging tables to isolate TM Mode 6 exclusive table locks, then executed instantaneous sub-second partition exchanges (<code class="text-teal-300 font-mono">ALTER TABLE claims EXCHANGE PARTITION</code>).</li>
              <li><strong>Interval-Range Partitioning:</strong> Configured automatic monthly interval generation (<code class="text-teal-300 font-mono">INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))</code>) with partition pruning.</li>
            </ol>

            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-emerald-300">
              Verified Metrics to Quote in Interview:<br>
              • Ingestion Runtime: Slashed from 6 hours down to 35 minutes (a 10x throughput speedup!).<br>
              • Memory Consumption: Dropped from >25GB live heap down to <50MB constant RAM.<br>
              • Downstream Reporting: Partition pruning dropped financial queries from 45 min to 1.2 sec.
            </div>
          </div>
        """,
        "code": """
<pre><code class="text-slate-300"><span class="text-slate-400">// Java 21 StAX Streaming Ingestor + Oracle 19c DDL</span>
<span class="text-purple-400">package</span> com.cognizant.etl.streaming;

<span class="text-purple-400">import</span> javax.xml.stream.XMLInputFactory;
<span class="text-purple-400">import</span> javax.xml.stream.XMLStreamConstants;
<span class="text-purple-400">import</span> javax.xml.stream.XMLStreamReader;
<span class="text-purple-400">import</span> java.io.InputStream;
<span class="text-purple-400">import</span> java.sql.Connection;
<span class="text-purple-400">import</span> java.sql.PreparedStatement;
<span class="text-purple-400">import</span> java.time.LocalDate;

<span class="text-purple-400">public class</span> <span class="text-blue-400">StaxStreamingClaimIngestor</span> {

    <span class="text-purple-400">private static final int</span> BATCH_SIZE = <span class="text-amber-300">5000</span>;

    <span class="text-purple-400">public void</span> <span class="text-blue-400">streamIngestXml</span>(InputStream xmlStream, Connection conn) <span class="text-purple-400">throws</span> Exception {
        XMLInputFactory factory = XMLInputFactory.newInstance();
        factory.setProperty(XMLInputFactory.SUPPORT_DTD, <span class="text-purple-400">false</span>);
        XMLStreamReader reader = factory.createXMLStreamReader(xmlStream);

        String insertSql = <span class="text-emerald-300">"INSERT /*+ APPEND */ INTO claims_staging (claim_id, policy_num, amount, claim_date) VALUES (?, ?, ?, ?)"</span>;
        conn.setAutoCommit(<span class="text-purple-400">false</span>);

        <span class="text-purple-400">try</span> (PreparedStatement ps = conn.prepareStatement(insertSql)) {
            String currentElement = <span class="text-emerald-300">""</span>, claimId = <span class="text-purple-400">null</span>, policyNum = <span class="text-purple-400">null</span>;
            <span class="text-purple-400">double</span> amount = <span class="text-amber-300">0.0</span>;
            LocalDate claimDate = <span class="text-purple-400">null</span>;
            <span class="text-purple-400">int</span> count = <span class="text-amber-300">0</span>;

            <span class="text-purple-400">while</span> (reader.hasNext()) {
                <span class="text-purple-400">int</span> event = reader.next();
                <span class="text-purple-400">if</span> (event == XMLStreamConstants.START_ELEMENT) {
                    currentElement = reader.getLocalName();
                } <span class="text-purple-400">else if</span> (event == XMLStreamConstants.CHARACTERS) {
                    String txt = reader.getText().trim();
                    <span class="text-purple-400">if</span> (txt.isEmpty()) <span class="text-purple-400">continue</span>;
                    <span class="text-purple-400">if</span> (<span class="text-emerald-300">"claimId"</span>.equals(currentElement)) claimId = txt;
                    <span class="text-purple-400">else if</span> (<span class="text-emerald-300">"policyNumber"</span>.equals(currentElement)) policyNum = txt;
                    <span class="text-purple-400">else if</span> (<span class="text-emerald-300">"amount"</span>.equals(currentElement)) amount = Double.parseDouble(txt);
                    <span class="text-purple-400">else if</span> (<span class="text-emerald-300">"claimDate"</span>.equals(currentElement)) claimDate = LocalDate.parse(txt);
                } <span class="text-purple-400">else if</span> (event == XMLStreamConstants.END_ELEMENT) {
                    <span class="text-purple-400">if</span> (<span class="text-emerald-300">"ClaimRecord"</span>.equals(reader.getLocalName())) {
                        ps.setString(<span class="text-amber-300">1</span>, claimId);
                        ps.setString(<span class="text-amber-300">2</span>, policyNum);
                        ps.setDouble(<span class="text-amber-300">3</span>, amount);
                        ps.setDate(<span class="text-amber-300">4</span>, java.sql.Date.valueOf(claimDate));
                        ps.addBatch();
                        count++;
                        <span class="text-purple-400">if</span> (count % BATCH_SIZE == <span class="text-amber-300">0</span>) {
                            ps.executeBatch();
                            conn.commit();
                        }
                    }
                    currentElement = <span class="text-emerald-300">""</span>;
                }
            }
            ps.executeBatch();
            conn.commit();
        }
    }
}

<span class="text-slate-400">-- Oracle 19c Interval-Range Partitioning & Partition Exchange DDL</span>
<span class="text-purple-400">CREATE TABLE</span> claims_master (
    claim_id <span class="text-purple-400">VARCHAR2</span>(<span class="text-amber-300">64</span>) <span class="text-purple-400">NOT NULL</span>,
    policy_num <span class="text-purple-400">VARCHAR2</span>(<span class="text-amber-300">64</span>) <span class="text-purple-400">NOT NULL</span>,
    amount <span class="text-purple-400">NUMBER</span>(<span class="text-amber-300">12</span>, <span class="text-amber-300">2</span>) <span class="text-purple-400">NOT NULL</span>,
    claim_date <span class="text-purple-400">DATE NOT NULL</span>
)
<span class="text-purple-400">PARTITION BY RANGE</span> (claim_date)
<span class="text-purple-400">INTERVAL</span> (NUMTOYMINTERVAL(<span class="text-amber-300">1</span>, <span class="text-emerald-300">'MONTH'</span>)) (
    <span class="text-purple-400">PARTITION</span> p_initial <span class="text-purple-400">VALUES LESS THAN</span> (TO_DATE(<span class="text-emerald-300">'2026-01-01'</span>, <span class="text-emerald-300">'YYYY-MM-DD'</span>))
);

<span class="text-purple-400">CREATE TABLE</span> claims_staging <span class="text-purple-400">AS SELECT * FROM</span> claims_master <span class="text-purple-400">WHERE</span> <span class="text-amber-300">1</span> = <span class="text-amber-300">0</span>;

<span class="text-purple-400">ALTER TABLE</span> claims_master 
    <span class="text-purple-400">EXCHANGE PARTITION FOR</span> (TO_DATE(<span class="text-emerald-300">'2026-09-01'</span>, <span class="text-emerald-300">'YYYY-MM-DD'</span>))
    <span class="text-purple-400">WITH TABLE</span> claims_staging
    <span class="text-purple-400">INCLUDING INDEXES WITHOUT VALIDATION</span>;</code></pre>
        """,
        "pitch": """"At Cognizant, our financial transaction settlement pipeline was collapsing under multi-gigabyte XML data feeds. Standard DOM parsers expanded 2GB files into 25GB of live heap memory, causing 15-second Stop-The-World GC pauses, frequent OOM crashes, and 6-hour batch runs. I re-architected the ingestion pipeline around Java StAX pull streaming, maintaining a bounded 50MB RAM footprint by processing records as an on-demand cursor. On the storage tier, I paired Oracle 19c Interval-Range Partitioning with Direct-Path Inserts writing directly above the High Water Mark. By isolating exclusive TM Mode 6 table locks in unpartitioned staging tables and performing sub-second partition exchanges, we slashed batch execution from 6 hours to 35 minutes (a 10x throughput gain) with zero JVM heap crashes." """,
        "traps": [
            ("Why choose StAX pull parsing over SAX push parsing if both avoid DOM in-memory trees?",
             "SAX is an asynchronous push parser that streams events to handler callbacks regardless of whether the downstream database can accept them, making consumer backpressure control extremely difficult. If database writes stall, SAX continues parsing and buffers records, leading to out-of-memory errors. StAX is a client-driven pull cursor: the application pulls the next XML token only when the current batch has been dispatched, providing natural backpressure and bounded memory."),
            ("What table lock does Direct-Path Insert place in Oracle, and how does it affect concurrent readers/writers?",
             "Direct-Path Insert places an exclusive TM Mode 6 (Table Lock - Exclusive) on the target table or partition. While concurrent SELECT queries can still read committed data via undo, all concurrent INSERT, UPDATE, and DELETE operations on that table are blocked until the appending transaction commits. We resolved this by loading into dedicated unpartitioned staging tables and performing an instantaneous sub-second metadata partition exchange (ALTER TABLE ... EXCHANGE PARTITION)."),
            ("What is the High Water Mark (HWM) in Oracle, and what happens to space below the HWM during Direct-Path Inserts?",
             "The High Water Mark is the boundary in an Oracle segment above which blocks are unformatted and have never been written. Conventional inserts scan freelists and insert into empty space below the HWM. Direct-Path Insert bypasses freelist lookups and formats fresh blocks strictly above the HWM. If a table has deleted space below the HWM, Direct-Path Insert does not reclaim it, potentially causing table bloat unless tables are truncated or reorganized.")
        ],
        "media": [
            ("Oracle 19c VLDB Guide: Partition Concepts & Pruning", "https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbi/partition-concepts.html", "Read Oracle Docs ↗"),
            ("Ask TOM: Oracle Direct-Path & High Water Mark Physics", "https://asktom.oracle.com/ords/f?p=100:11:0::::P11_QUESTION_ID:9534431800346897258", "Read Ask TOM ↗"),
            ("Oracle Java SE: StAX Pull Parser Specifications", "https://docs.oracle.com/javase/8/docs/technotes/guides/xml/jaxp/stax.html", "View StAX Guide ↗")
        ]
    }
]

with open('d:/Antigravity/modules_tech.py', 'a', encoding='utf-8') as f:
    for mod in MODULES_3_TO_7:
        f.write("\nMODULES.append(" + repr(mod) + ")\n")

print("Successfully appended Modules 3 to 7 into modules_tech.py!")
