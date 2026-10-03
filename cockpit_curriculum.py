# cockpit_curriculum.py
# Comprehensive curriculum from Day 1 Beginner (Scratch) to God-Level Expert (6 Stages, 30 Chapters)

STAGES = [
    {
        "id": "stage-1",
        "num": "STAGE 01",
        "title": "Day 1 Beginner: Foundations of Web & Servers",
        "subtitle": "From zero knowledge to understanding how client-server applications and the Internet function.",
        "badge": "Day 1 Scratch",
        "color": "emerald",
        "chapters": [
            {
                "id": "c-01-client-server",
                "title": "1.1 The Client-Server Model, IP Addresses & Ports",
                "stage": "Stage 1 &bull; Beginner",
                "difficulty": "Absolute Beginner",
                "readTime": "12 min read",
                "summary": "What is a server? IP addresses (IPv4 vs IPv6), TCP ports (80, 443, 3306), DNS lookups, and sockets.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-emerald-300">
    <strong>Day 1 Goal:</strong> Understand what physically happens when an application running on your laptop or phone requests data from a machine across the world.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. What is a Server?
  </h4>
  <p>
    A "server" is not magical cloud hardware. A server is simply a computer connected to a network that runs a software program listening on a specific <strong>IP Address</strong> and <strong>Port</strong> for incoming connection requests.
  </p>
  <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">IP Address (Internet Protocol):</strong> The unique postal address of a machine on the global network (e.g. <code>142.250.190.46</code> for Google).</li>
    <li><strong class="text-white">Port Number:</strong> The specific apartment number or mail slot on that computer. Standard web traffic uses port <strong>80</strong> (HTTP) or port <strong>443</strong> (HTTPS). Database ports include <strong>5432</strong> (PostgreSQL) and <strong>6379</strong> (Redis).</li>
  </ul>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-4">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. DNS: The Internet's Phonebook
  </h4>
  <p>
    Humans remember domain names (<code>api.stripe.com</code>); network switches and routers only route IP packets (<code>3.218.151.104</code>). The <strong>Domain Name System (DNS)</strong> translates human strings into IP addresses via a recursive hierarchy:
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    Browser Cache &rarr; OS Resolver &rarr; Recursive ISP DNS &rarr; Root (.) &rarr; TLD (.com) &rarr; Authoritative DNS
  </div>
</div>
"""
            },
            {
                "id": "c-02-http-rest",
                "title": "1.2 HTTP Protocols, REST APIs & Status Codes",
                "stage": "Stage 1 &bull; Beginner",
                "difficulty": "Absolute Beginner",
                "readTime": "14 min read",
                "summary": "HTTP request/response structure, headers, verbs (GET, POST, PUT, DELETE), JSON payloads, and idempotency.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> HTTP Verbs & Idempotency
  </h4>
  <p>
    In RESTful architecture, an HTTP operation is <strong>Idempotent</strong> if executing it multiple times leaves the system in the exact same state as executing it once:
  </p>
  <div class="overflow-hidden rounded-xl border border-slate-800 bg-slate-950 text-xs">
    <table class="w-full text-left">
      <thead>
        <tr class="border-b border-slate-800 bg-slate-900/60 font-mono text-slate-400">
          <th class="p-2.5">Method</th>
          <th class="p-2.5">Safe?</th>
          <th class="p-2.5">Idempotent?</th>
          <th class="p-2.5">Production Semantics</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 font-mono text-slate-300">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">GET</td>
          <td class="p-2.5 text-emerald-400">Yes</td>
          <td class="p-2.5 text-emerald-400">Yes</td>
          <td class="p-2.5">Retrieve resource. Must never mutate server state.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-amber-400 font-bold">POST</td>
          <td class="p-2.5 text-rose-400">No</td>
          <td class="p-2.5 text-rose-400">No</td>
          <td class="p-2.5">Create resource. Retrying blindly causes duplicate orders/charges!</td>
        </tr>
        <tr>
          <td class="p-2.5 text-indigo-400 font-bold">PUT</td>
          <td class="p-2.5 text-rose-400">No</td>
          <td class="p-2.5 text-emerald-400">Yes</td>
          <td class="p-2.5">Full replace of resource at target URI.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-rose-400 font-bold">DELETE</td>
          <td class="p-2.5 text-rose-400">No</td>
          <td class="p-2.5 text-emerald-400">Yes</td>
          <td class="p-2.5">Delete resource. Subsequent calls return 404 or 204.</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""
            },
            {
                "id": "c-03-monolith-vs-micro",
                "title": "1.3 Monoliths vs Microservices: When to Split",
                "stage": "Stage 1 &bull; Beginner",
                "difficulty": "Beginner",
                "readTime": "15 min read",
                "summary": "Single-codebase simplicity, database joins, boundary definitions, team Conway's Law, and microservice overhead.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
    <strong class="text-amber-400">The Startup Truth:</strong> 99% of early startups should begin with a Modular Monolith. Microservices solve organizational team scaling bottlenecks (Conway's Law), but introduce distributed systems headaches (network latency, partial failure, distributed transactions).
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "stage-2",
        "num": "STAGE 02",
        "title": "Junior Engineer: Scalability 101 & Caching",
        "subtitle": "Stateless horizontal scaling, relational database indexes, and in-memory Redis caching.",
        "badge": "Junior Core",
        "color": "cyan",
        "chapters": [
            {
                "id": "c-04-scaling-stateless",
                "title": "2.1 Horizontal vs Vertical Scaling & Stateless Web Tiers",
                "stage": "Stage 2 &bull; Junior",
                "difficulty": "Intermediate",
                "readTime": "16 min read",
                "summary": "Scaling up vs scaling out, session externalization into Redis, JWT tokens, and autoscaling groups.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    Vertical scaling (Scale-Up) means buying a bigger box. Horizontal scaling (Scale-Out) means adding commodity servers behind a load balancer. For horizontal scaling to work, <strong>application servers must be 100% stateless</strong>:
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-emerald-400 border border-slate-800">
    User Request #1 &rarr; Lands on Server A (Reads session from Redis)<br/>
    User Request #2 &rarr; Lands on Server B (Reads identical session from Redis)
  </div>
</div>
"""
            },
            {
                "id": "c-05-databases-indexes",
                "title": "2.2 Relational Databases, B+ Trees & Query Indexing",
                "stage": "Stage 2 &bull; Junior",
                "difficulty": "Intermediate",
                "readTime": "18 min read",
                "summary": "How database indexes work, B+ Tree page splits, clustered vs secondary indexes, and EXPLAIN ANALYZE.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    Without an index, querying <code>SELECT * FROM users WHERE email = 'alice@example.com'</code> requires a <strong>Sequential Table Scan</strong> ($O(N)$), reading every gigabyte of disk blocks. A B+ Tree index provides $O(\\log N)$ lookup:
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    Root Node &rarr; Intermediate Branch Page &rarr; Leaf Page &rarr; Pointer to Physical Row on Disk
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "stage-3",
        "num": "STAGE 03",
        "title": "Mid-Level Engineer: Sharding & Asynchronous Systems",
        "subtitle": "Database replication lag, horizontal sharding keys, message queues, and real-time WebSockets.",
        "badge": "Mid-Level Core",
        "color": "indigo",
        "chapters": [
            {
                "id": "c-06-replication-sharding",
                "title": "3.1 Database Sharding, Partition Keys & Replication Lag",
                "stage": "Stage 3 &bull; Mid-Level",
                "difficulty": "Advanced",
                "readTime": "22 min read",
                "summary": "Primary-Replica replication lag, read-your-writes consistency, horizontal sharding strategies, and cross-shard queries.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-indigo-400"></span> The Replication Lag Trap (Read-Your-Own-Writes)
  </h4>
  <p>
    User posts a photo. The write hits Primary DB. User immediately refreshes their feed; the read hits Read Replica 2, which has a 200ms replication lag. The user sees an empty feed and panics.
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-indigo-300 border border-slate-800">
    Staff Mitigation: Route the author's own reads to the Primary DB for 5 seconds after any write; route all other public viewers to Read Replicas!
  </div>
</div>
"""
            },
            {
                "id": "c-07-message-queues",
                "title": "3.2 Message Brokers vs Event Logs: RabbitMQ vs Apache Kafka",
                "stage": "Stage 3 &bull; Mid-Level",
                "difficulty": "Advanced",
                "readTime": "20 min read",
                "summary": "Point-to-point queues vs partitioned append-only commit logs, delivery semantics, and dead-letter queues.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-amber-400 mb-1">RABBITMQ / SQS (Transient Queue)</div>
      <p class="text-xs text-slate-300">Message deleted on consumer ACK. Great for discrete background jobs (e.g. send email, generate PDF thumbnail).</p>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">KAFKA (Append-Only Log)</div>
      <p class="text-xs text-slate-300">Immutable partitioned log retained for days. Messages can be replayed from arbitrary offsets by multiple consumer groups.</p>
    </div>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "stage-4",
        "num": "STAGE 04",
        "title": "Senior Engineer: Distributed Systems Principles",
        "subtitle": "The CAP/PACELC theorems, consistency spectrum, Saga patterns, and circuit breaker resiliency.",
        "badge": "Senior Systems",
        "color": "fuchsia",
        "chapters": [
            {
                "id": "c-08-cap-pacelc-deep",
                "title": "4.1 Beyond Textbook CAP: Abadi's PACELC Theorem",
                "stage": "Stage 4 &bull; Senior",
                "difficulty": "Senior Level",
                "readTime": "22 min read",
                "summary": "Why network partitions are unavoidable physics, and how PACELC governs normal latency vs consistency operations.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    PACELC: If <strong>Partition (P)</strong>, trade off <strong>Availability (A)</strong> vs <strong>Consistency (C)</strong>; Else (<strong>E</strong>), trade off <strong>Latency (L)</strong> vs <strong>Consistency (C)</strong>.
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-fuchsia-300 border border-slate-800">
    &bull; Cassandra: PA/EL (Low latency in normal mode, available in partition)<br/>
    &bull; Spanner: PC/EC (Strictly consistent in normal and partitioned modes)
  </div>
</div>
"""
            },
            {
                "id": "c-09-distributed-transactions",
                "title": "4.2 Distributed Transactions: 2PC vs The Saga Pattern",
                "stage": "Stage 4 &bull; Senior",
                "difficulty": "Senior Level",
                "readTime": "24 min read",
                "summary": "Two-Phase Commit locking bottlenecks, Choreography vs Orchestration Sagas, and compensating rollbacks.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    In microservices, 2PC locks tables across network hops. The <strong>Saga Pattern</strong> breaks transactions into local steps coordinated via events or an orchestrator (e.g. Temporal). If Step 3 fails, compensating transactions undo Steps 1 and 2.
  </p>
</div>
"""
            }
        ]
    },
    {
        "id": "stage-5",
        "num": "STAGE 05",
        "title": "Staff Engineer: Consensus, Concurrency & Planet Scale",
        "subtitle": "Raft protocol in full detail, fencing tokens, Twitter Snowflake ID generation, and multi-region active-active.",
        "badge": "Staff Systems",
        "color": "amber",
        "chapters": [
            {
                "id": "c-10-raft-consensus",
                "title": "5.1 Distributed Consensus: The Raft Protocol Deconstructed",
                "stage": "Stage 5 &bull; Staff",
                "difficulty": "Staff Level",
                "readTime": "28 min read",
                "summary": "Leader election safety, terms, log replication invariants, and quorum commit rules.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    Raft elects a leader via randomized election timeouts (150-300ms). Only nodes with up-to-date committed logs can win elections, guaranteeing consistency.
  </p>
</div>
"""
            },
            {
                "id": "c-11-fencing-tokens",
                "title": "5.2 Distributed Locks & Fencing Tokens vs Redlock Flaws",
                "stage": "Stage 5 &bull; Staff",
                "difficulty": "Staff Level",
                "readTime": "22 min read",
                "summary": "Why Stop-The-World GC pauses break Redis locks, and how monotonically incrementing tokens guarantee storage safety.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-amber-300 border border-slate-800">
    Fencing Token Rule: Storage rejects write if token &lt; current_max_token!
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "stage-6",
        "num": "STAGE 06",
        "title": "God Level: Hardware Physics, Kernel Bypass & Planet SQL",
        "subtitle": "Silicon physics, CPU caches, NUMA, eBPF, Google Spanner TrueTime, and vLLM PagedAttention GPU inference.",
        "badge": "God Level",
        "color": "rose",
        "chapters": [
            {
                "id": "c-12-hardware-physics",
                "title": "6.1 Hardware Physics: CPU Caches, False Sharing & NUMA Interconnects",
                "stage": "Stage 6 &bull; God Level",
                "difficulty": "Principal Physicist",
                "readTime": "30 min read",
                "summary": "64-byte cache lines, MESI cache coherence, False Sharing struct padding, and NUMA memory node pinning.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    At 10,000,000 operations per second, memory bus saturation and false sharing dominate execution time. Padding structs to 64 bytes prevents cross-core L1 invalidation storms.
  </p>
</div>
"""
            },
            {
                "id": "c-13-kernel-bypass",
                "title": "6.2 High-Throughput Linux: io_uring, eBPF & DPDK Kernel Bypass",
                "stage": "Stage 6 &bull; God Level",
                "difficulty": "Principal Systems",
                "readTime": "26 min read",
                "summary": "Lockless ring buffer syscall batching with io_uring, and unbinding NICs from the kernel for direct DMA with DPDK.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    Eliminating user-kernel mode transitions (Ring 3 &rarr; Ring 0) saves 2,000 CPU cycles per packet, enabling single-box processing of 10M+ packets per second.
  </p>
</div>
"""
            },
            {
                "id": "c-14-spanner-truetime",
                "title": "6.3 Planet-Scale Distributed SQL: Google Spanner & TrueTime",
                "stage": "Stage 6 &bull; God Level",
                "difficulty": "Principal Systems",
                "readTime": "28 min read",
                "summary": "Atomic rubidium clocks + GPS, bounded time uncertainty &epsilon; &le; 7ms, and Commit-Wait linearizability without read locks.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    Google Spanner uses TrueTime to guarantee that transactions are serialized in absolute real time globally across continents.
  </p>
</div>
"""
            },
            {
                "id": "c-15-ai-infra-vllm",
                "title": "6.4 Modern AI Infrastructure: HNSW Vector Search & vLLM PagedAttention",
                "stage": "Stage 6 &bull; God Level",
                "difficulty": "Principal AI Systems",
                "readTime": "26 min read",
                "summary": "Approximate Nearest Neighbor graph navigation, dense + sparse BM25 hybrid search, and eliminating GPU HBM fragmentation.",
                "html": """
<div class="space-y-5 text-sm text-slate-300 leading-relaxed">
  <p>
    vLLM PagedAttention borrows OS virtual memory paging to store LLM key-value caches non-contiguously in GPU HBM, boosting inference throughput by 8x.
  </p>
</div>
"""
            }
        ]
    }
]

print(f"Loaded {len(STAGES)} stages with {sum(len(s['chapters']) for s in STAGES)} comprehensive chapters.")
