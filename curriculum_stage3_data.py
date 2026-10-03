# curriculum_stage3_data.py
# Stage 3: Senior Engineer - Distributed Sharding, Caching & Event Streaming

STAGE_3_CHAPTERS = [
    {
        "id": "c-06-replication-sharding",
        "stageId": "stage-3",
        "stageNum": "STAGE 03",
        "badge": "Senior Engineer",
        "color": "indigo",
        "title": "3.1 Database Sharding, Consistent Hash Partitioning & Replication Lag",
        "difficulty": "Senior",
        "readTime": "25 min read",
        "simulatorKey": "ring",
        "summary": "Partitioning physical data: Range vs Hash vs Consistent Hashing with virtual nodes. Dealing with celebrity hot keys, cross-shard scatter-gather, and replication lag anomalies.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/20 text-indigo-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-indigo-400 mb-1">First-Principles Intuition</div>
    Imagine you have a phone book with 1 billion names. It is too heavy for any single bookshelf to hold ($IOPS / Disk limit$).
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-indigo-200">
      <li><strong>Range Sharding:</strong> Volume 1 has names A-C, Volume 2 has D-F, etc. The catastrophic flaw: Letter "S" has 150 million names, while letter "X" has 2,000 names. Volume S bursts while Volume X collects dust (Data &amp; Query Skew).</li>
      <li><strong>Modulus Hash Sharding:</strong> Compute <code>hash(name) % N</code>. If you have 4 servers, records are distributed evenly. But the moment you add Server 5, <code>hash(name) % 5</code> re-hashes and moves 80% of all data across the network!</li>
      <li><strong>Consistent Hashing:</strong> Map servers and data keys to a $2^{32}-1$ integer ring. Adding a server only moves $1/N$ fraction of keys from its immediate clockwise neighbor. Zero global rebalancing!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-indigo-400"></span> 1. The Mathematics of Consistent Hashing with Virtual Nodes
  </h4>
  <p>
    In a standard hash ring with only 3 physical nodes, non-uniform distribution can cause one server to own 60% of the ring circumference.
    To achieve near-perfect mathematical balance, each physical server is assigned $V$ <strong>Virtual Nodes (vnodes)</strong> (typically $V = 256$ to $1,024$ points along the ring):
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    $$\text{Standard Deviation of Key Distribution: } \sigma \propto \frac{1}{\sqrt{V}}$$
    With $V = 256$ virtual nodes per physical machine, the variance between the most loaded and least loaded node drops to under <strong>3.5%</strong>!
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-indigo-400"></span> 2. Replication Lag &amp; The "Read-After-Write" Trap
  </h4>
  <p>
    To scale read throughput, databases deploy 1 Primary (accepts writes) and $N$ Read Replicas (serve reads).
    Replication is asynchronous to keep write latency low. If a network blip causes 500ms replication lag:
  </p>
  <ol class="list-decimal list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li>User posts a comment: <code>POST /comment</code> &rarr; Writes to Primary DB at $T=0$. Primary returns HTTP 200.</li>
    <li>Browser immediately reloads feed: <code>GET /feed</code> &rarr; Load balancer routes read to Replica B at $T=50\,\text{ms}$.</li>
    <li>Replica B has not yet received the WAL replication segment. The comment is invisible!</li>
    <li>User assumes the comment failed, posts it again, creating duplicate data.</li>
  </ol>
  <p class="text-xs text-emerald-400 font-mono">
    Staff Fix: <strong>Read-Your-Own-Writes Consistency</strong>. When a user writes, set a cookie <code>write_ts=1719230192</code>. For the next 5 seconds, route that user's read requests exclusively to the Primary, or to a replica whose replication watermark &ge; <code>write_ts</code>!
  </p>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>
    <marker id="arr-h3" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- CONSISTENT HASH RING (CIRCULAR TOPOLOGY) -->
  <g transform="translate(180, 190)">
    <!-- Outer Ring -->
    <circle cx="0" cy="0" r="140" fill="none" stroke="#334155" stroke-width="4" stroke-dasharray="6"/>
    <text x="0" y="-150" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">0 (2^32 - 1)</text>

    <!-- Node A (Cyan) and vnodes -->
    <circle cx="0" cy="-140" r="12" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
    <text x="0" y="-120" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">Shard A (v1)</text>

    <circle cx="-135" cy="40" r="10" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="-140" y="65" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Shard A (v2)</text>

    <!-- Node B (Emerald) and vnodes -->
    <circle cx="120" cy="-70" r="12" fill="#059669" stroke="#34d399" stroke-width="2"/>
    <text x="145" y="-55" fill="#34d399" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">Shard B (v1)</text>

    <circle cx="-50" cy="130" r="10" fill="#059669" stroke="#34d399" stroke-width="1.5"/>
    <text x="-50" y="155" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">Shard B (v2)</text>

    <!-- Node C (Fuchsia) and vnodes -->
    <circle cx="70" cy="120" r="12" fill="#7c3aed" stroke="#c084fc" stroke-width="2"/>
    <text x="95" y="135" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">Shard C (v1)</text>

    <!-- Incoming Key Lookup Walk -->
    <circle cx="80" cy="-20" r="6" fill="#facc15"/>
    <text x="80" y="-30" fill="#facc15" font-size="8" font-family="monospace" text-anchor="middle">key: user_948</text>
    <path d="M 80 -14 A 140 140 0 0 1 70 120" fill="none" stroke="#facc15" stroke-width="2" stroke-dasharray="3"/>
    <text x="130" y="40" fill="#facc15" font-size="8" font-family="monospace">Clockwise Walk &rarr; Shard C</text>
  </g>

  <!-- SHARD ARCHITECTURE DETAILS (RIGHT PANEL) -->
  <g transform="translate(480, 40)">
    <rect width="440" height="300" rx="10" fill="#0f172a" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="12" font-family="sans-serif" font-weight="bold">Vitess / Citus Distributed Shard Router</text>
    <text x="20" y="50" fill="#94a3b8" font-size="9" font-family="monospace">Transparent SQL Query Partitioning Engine</text>

    <!-- Shard 1 Box -->
    <g transform="translate(20, 70)">
      <rect width="190" height="95" rx="6" fill="#1e293b" stroke="#0284c7" stroke-width="1.2"/>
      <text x="12" y="22" fill="#38bdf8" font-size="10" font-weight="bold">Shard Cluster A</text>
      <text x="12" y="38" fill="#bae6fd" font-size="8" font-family="monospace">Primary: Write Master</text>
      <text x="12" y="52" fill="#94a3b8" font-size="8" font-family="monospace">Replica 1 &bull; Replica 2 (Read)</text>
      <text x="12" y="70" fill="#34d399" font-size="8" font-family="monospace">Keys: 0x0000 - 0x5555</text>
      <text x="12" y="84" fill="#a7f3d0" font-size="8" font-family="monospace">Throughput: 15k QPS</text>
    </g>

    <!-- Shard 2 Box -->
    <g transform="translate(230, 70)">
      <rect width="190" height="95" rx="6" fill="#1e293b" stroke="#059669" stroke-width="1.2"/>
      <text x="12" y="22" fill="#34d399" font-size="10" font-weight="bold">Shard Cluster B</text>
      <text x="12" y="38" fill="#a7f3d0" font-size="8" font-family="monospace">Primary: Write Master</text>
      <text x="12" y="52" fill="#94a3b8" font-size="8" font-family="monospace">Replica 1 &bull; Replica 2 (Read)</text>
      <text x="12" y="70" fill="#34d399" font-size="8" font-family="monospace">Keys: 0x5556 - 0xAAAA</text>
      <text x="12" y="84" fill="#a7f3d0" font-size="8" font-family="monospace">Throughput: 15k QPS</text>
    </g>

    <!-- Shard 3 Box -->
    <g transform="translate(20, 180)">
      <rect width="400" height="100" rx="6" fill="#1e1b4b" stroke="#7c3aed" stroke-width="1.2"/>
      <text x="14" y="24" fill="#c084fc" font-size="11" font-weight="bold">Celebrity Key Mitigation: Salted Hashing</text>
      <text x="14" y="44" fill="#e9d5ff" font-size="8" font-family="sans-serif">
        If Elon Musk posts a tweet, 100M users read from user_id: 44. Shard A would melt!
      </text>
      <rect x="14" y="55" width="372" height="32" rx="4" fill="#312e81"/>
      <text x="24" y="75" fill="#facc15" font-size="8" font-family="monospace">
        Shard Key: user_id + "_" + rand(0, 16) &rarr; Distributes reads across 16 shards!
      </text>
    </g>
  </g>
</svg>
""",
        "codeSnippet": """// Production Consistent Hash Ring Implementation in Go
// Demonstrating Murmur3 Hashing, Virtual Nodes & Binary Search Ring Traversal
package sharding

import (
	"fmt"
	"sort"
	"strconv"
	"sync"

	"github.com/spaolacci/murmur3"
)

type ConsistentHashRing struct {
	mu           sync.RWMutex
	vnodes       int               // Number of virtual nodes per physical node (e.g. 256)
	ring         []uint32          // Sorted list of token hashes along the ring
	nodeMap      map[uint32]string // Token hash -> Physical Node Address
	nodes        map[string]bool   // Set of registered physical nodes
}

func NewConsistentHashRing(vnodes int) *ConsistentHashRing {
	return &ConsistentHashRing{
		vnodes:  vnodes,
		ring:    make([]uint32, 0),
		nodeMap: make(map[uint32]string),
		nodes:   make(map[string]bool),
	}
}

// AddNode registers a physical server and hashes its virtual points
func (h *ConsistentHashRing) AddNode(node string) {
	h.mu.Lock()
	defer h.mu.Unlock()

	if h.nodes[node] {
		return
	}
	h.nodes[node] = true

	for i := 0; i < h.vnodes; i++ {
		// Example: "db-shard-1#vnode-42"
		vnodeKey := node + "#" + strconv.Itoa(i)
		hash := murmur3.Sum32([]byte(vnodeKey))
		h.ring = append(h.ring, hash)
		h.nodeMap[hash] = node
	}

	sort.Slice(h.ring, func(i, j int) bool {
		return h.ring[i] < h.ring[j]
	})
}

// GetNode routes a partition key to the closest clockwise physical server
func (h *ConsistentHashRing) GetNode(key string) (string, error) {
	h.mu.RLock()
	defer h.mu.RUnlock()

	if len(h.ring) == 0 {
		return "", fmt.Errorf("hash ring is empty; no shards registered")
	}

	hash := murmur3.Sum32([]byte(key))

	// Binary search in sorted ring for the first token >= key hash
	idx := sort.Search(len(h.ring), func(i int) bool {
		return h.ring[i] >= hash
	})

	// Wrap around to the start of the ring if key hash exceeds all tokens
	if idx == len(h.ring) {
		idx = 0
	}

	return h.nodeMap[h.ring[idx]], nil
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The 2018 GitHub 24-Hour Network Split &amp; MySQL Corruption Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: GitHub entered emergency read-only maintenance for 24 hours after a 43-second transatlantic optical network partition triggered MySQL split-brain.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      On October 21, 2018, maintenance on a 100G transatlantic fiber optic link caused a 43-second network blip between GitHub's primary US East data center and secondary US West data center.
      Automated orchestrators in US West detected missing heartbeats and promoted local MySQL read replicas to primaries.
    </p>
    <p>
      When the network link healed 43 seconds later, <strong>both data centers had independent primary databases accepting concurrent writes</strong>.
      Because replication was asynchronous and lacked fencing tokens, thousands of conflicting database writes were committed in both regions, corrupting pull requests, merge statuses, and user accounts.
      Engineers spent 24 hours manually reconciling binary transaction logs to prevent permanent data loss!
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Raft-Governed Failover (Github Orchestrator):</strong> Never allow a single region to promote a database replica without obtaining a majority quorum consensus ($N/2 + 1$) across an odd number of regions (e.g. 3 data centers).</li>
      <li><strong class="text-white">Strict Read-Only Fencing:</strong> When a network partition is detected, demote all disconnected replicas to <code>read_only=ON</code> instantly to prevent rogue split-brain writes.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "How do you execute a cross-shard transaction or query (e.g. JOIN across 2 sharded databases) without bringing down your system?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "The primary rule of database sharding is: <strong>Design your sharding key so that 99% of queries are single-shard</strong>. If you are joining tables across shards on every request, your partition key is wrong.
      <br><br>
      When a cross-shard query is unavoidable, there are two production patterns:
      <br><br>
      1. <strong>Scatter-Gather with Query Federation:</strong> The shard proxy dispatches $N$ parallel queries across all shards, then aggregates, sorts, and limits the results in memory. This is acceptable for analytical queries, but dangerous at high TPS because a single slow shard inflates the entire query latency to the P99.9 slowest node.
      <br><br>
      2. <strong>Denormalization via Event Streaming (The Staff Solution):</strong> Instead of runtime cross-shard joins, use Change Data Capture (Debezium + Kafka) to asynchronously project joined data into a dedicated read-optimized table or Elasticsearch cluster. Writes remain strictly partitioned by entity ID, while reads hit a pre-computed materialized view with zero cross-shard coordination."
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-07-message-queues",
        "stageId": "stage-3",
        "stageNum": "STAGE 03",
        "badge": "Senior Engineer",
        "color": "indigo",
        "title": "3.2 Message Brokers vs Event Logs: RabbitMQ vs Apache Kafka",
        "difficulty": "Senior",
        "readTime": "24 min read",
        "simulatorKey": "tracer",
        "summary": "Smart Broker / Dumb Consumer vs Dumb Broker / Smart Consumer. Append-only commit logs, Linux zero-copy sendfile(2), and exactly-once processing semantics.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/20 text-indigo-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-indigo-400 mb-1">First-Principles Intuition</div>
    <ul class="list-disc list-inside space-y-1 text-xs text-indigo-200">
      <li><strong>Traditional Message Queue (RabbitMQ / AMQP):</strong> Like a post office with PO boxes. When you pick up a package from your PO box, it is deleted forever. The post office tracks which messages were picked up. If 1,000 consumers connect, the post office does 1,000x the state management.</li>
      <li><strong>Distributed Append-Only Commit Log (Apache Kafka):</strong> Like an immutable ledger etched into stone. Messages are appended in sequential order with an offset (0, 1, 2, 3...). Consumers simply bring their own bookmarks (<strong>Consumer Offsets</strong>). If 10,000 consumers read the ledger, the broker doesn't care; it does zero state tracking, and consumers can replay history from any point in time!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-indigo-400"></span> 1. Architectural Comparison Matrix
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Feature</th>
          <th class="p-2.5">RabbitMQ (AMQP)</th>
          <th class="p-2.5">Apache Kafka (Commit Log)</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Data Storage Model</td>
          <td class="p-2.5">Transient queue (Deleted upon consumer ACK)</td>
          <td class="p-2.5 text-emerald-400">Persistent disk log (Retained for 7 days / forever)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Consumer Model</td>
          <td class="p-2.5">Push (Broker pushes to consumer)</td>
          <td class="p-2.5 text-emerald-400">Pull (Consumer polls at its own pace)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Replayability</td>
          <td class="p-2.5 text-rose-400">Impossible once ACKed</td>
          <td class="p-2.5 text-emerald-400">Trivial: Reset consumer group offset to 0</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Throughput Ceiling</td>
          <td class="p-2.5 text-amber-400">20k - 50k msgs/sec (RAM bound)</td>
          <td class="p-2.5 text-emerald-400">1,000,000+ msgs/sec per broker (Zero-Copy)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-indigo-400"></span> 2. Why Kafka Can Write 1 Million Messages/Sec on Hard Drives
  </h4>
  <p>
    Spinning hard disks are notoriously slow for random I/O (100 IOPS), but blisteringly fast for <strong>Sequential I/O (600 MB/s)</strong>—faster than random writes to RAM!
    Kafka achieves super-human speed through two Linux kernel physics optimizations:
  </p>
  <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Sequential Disk Append:</strong> Kafka never modifies existing files. It strictly appends to the tail of the segment file. Disk write heads never seek randomly.</li>
    <li><strong class="text-white">Linux Zero-Copy (`sendfile(2)` system call):</strong> Traditional brokers copy data: Disk &rarr; OS Page Cache &rarr; User Space JVM Buffer &rarr; Socket Buffer &rarr; NIC Buffer (4 context switches, 3 CPU copies). Kafka invokes <code>sendfile()</code>: data streams directly from the OS Page Cache to the NIC buffer with <strong>ZERO CPU memory copies</strong>!</li>
  </ul>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-p" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="g-k" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#059669"/><stop offset="100%" stop-color="#047857"/></linearGradient>
    <linearGradient id="g-c3" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient>
    <marker id="arr-kf" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- PRODUCERS -->
  <g transform="translate(30, 80)">
    <rect width="160" height="220" rx="10" fill="url(#g-p)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="14" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Producers</text>
    <text x="14" y="48" fill="#bae6fd" font-size="9" font-family="monospace">Idempotent (acks=all)</text>

    <rect x="14" y="65" width="132" height="40" rx="4" fill="#0c4a6e"/>
    <text x="20" y="82" fill="#38bdf8" font-size="8" font-family="monospace">App Pod A (Orders)</text>
    <text x="20" y="96" fill="#7dd3fc" font-size="8" font-family="monospace">MurmurHash2(key)</text>

    <rect x="14" y="115" width="132" height="40" rx="4" fill="#0c4a6e"/>
    <text x="20" y="132" fill="#38bdf8" font-size="8" font-family="monospace">App Pod B (Payments)</text>
    <text x="20" y="146" fill="#7dd3fc" font-size="8" font-family="monospace">Batching 64KB buffers</text>

    <rect x="14" y="165" width="132" height="40" rx="4" fill="#0c4a6e"/>
    <text x="20" y="182" fill="#38bdf8" font-size="8" font-family="monospace">App Pod C (Events)</text>
    <text x="20" y="196" fill="#7dd3fc" font-size="8" font-family="monospace">LZ4 Compression</text>
  </g>

  <!-- KAFKA BROKER CLUSTER & PARTITIONS -->
  <g transform="translate(240, 40)">
    <rect width="420" height="300" rx="12" fill="#0f172a" stroke="#059669" stroke-width="2"/>
    <text x="20" y="32" fill="#34d399" font-size="13" font-family="sans-serif" font-weight="bold">Kafka 3.6+ KRaft Cluster (Topic: order_events)</text>
    <text x="20" y="50" fill="#94a3b8" font-size="9" font-family="monospace">Append-Only Commit Logs &bull; Linux Zero-Copy sendfile()</text>

    <!-- Partition 0 -->
    <g transform="translate(20, 65)">
      <rect width="380" height="60" rx="6" fill="#064e3b" stroke="#10b981"/>
      <text x="12" y="20" fill="#34d399" font-size="10" font-weight="bold">Partition 0 (Leader: Broker 1)</text>
      <!-- Log segments -->
      <g transform="translate(12, 28)" font-family="monospace" font-size="8">
        <rect x="0" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="17" y="15" fill="#a7f3d0" text-anchor="middle">0</text>
        <rect x="40" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="57" y="15" fill="#a7f3d0" text-anchor="middle">1</text>
        <rect x="80" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="97" y="15" fill="#a7f3d0" text-anchor="middle">2</text>
        <rect x="120" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="137" y="15" fill="#a7f3d0" text-anchor="middle">3</text>
        <rect x="160" y="0" width="45" height="22" fill="#065f46" stroke="#34d399"/>
        <text x="182" y="15" fill="#ffffff" text-anchor="middle">4 [HWM]</text>
        <text x="220" y="15" fill="#94a3b8">Offset pointer</text>
      </g>
    </g>

    <!-- Partition 1 -->
    <g transform="translate(20, 140)">
      <rect width="380" height="60" rx="6" fill="#064e3b" stroke="#10b981"/>
      <text x="12" y="20" fill="#34d399" font-size="10" font-weight="bold">Partition 1 (Leader: Broker 2)</text>
      <g transform="translate(12, 28)" font-family="monospace" font-size="8">
        <rect x="0" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="17" y="15" fill="#a7f3d0" text-anchor="middle">0</text>
        <rect x="40" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="57" y="15" fill="#a7f3d0" text-anchor="middle">1</text>
        <rect x="80" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="97" y="15" fill="#a7f3d0" text-anchor="middle">2</text>
        <rect x="120" y="0" width="45" height="22" fill="#065f46" stroke="#34d399"/>
        <text x="142" y="15" fill="#ffffff" text-anchor="middle">3 [HWM]</text>
      </g>
    </g>

    <!-- Partition 2 -->
    <g transform="translate(20, 215)">
      <rect width="380" height="60" rx="6" fill="#064e3b" stroke="#10b981"/>
      <text x="12" y="20" fill="#34d399" font-size="10" font-weight="bold">Partition 2 (Leader: Broker 3)</text>
      <g transform="translate(12, 28)" font-family="monospace" font-size="8">
        <rect x="0" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="17" y="15" fill="#a7f3d0" text-anchor="middle">0</text>
        <rect x="40" y="0" width="35" height="22" fill="#042f2e" stroke="#10b981"/>
        <text x="57" y="15" fill="#a7f3d0" text-anchor="middle">1</text>
        <rect x="80" y="0" width="45" height="22" fill="#065f46" stroke="#34d399"/>
        <text x="102" y="15" fill="#ffffff" text-anchor="middle">2 [HWM]</text>
      </g>
    </g>
  </g>

  <!-- CONSUMER GROUPS -->
  <g transform="translate(710, 80)">
    <rect width="210" height="220" rx="10" fill="url(#g-c3)" stroke="#c084fc" stroke-width="1.5"/>
    <text x="14" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Consumer Groups</text>
    <text x="14" y="48" fill="#e9d5ff" font-size="8" font-family="monospace">Pull Architecture (Poll Loop)</text>

    <rect x="14" y="65" width="180" height="40" rx="4" fill="#312e81"/>
    <text x="20" y="82" fill="#c084fc" font-size="8" font-family="monospace">Group: "fraud_detector"</text>
    <text x="20" y="96" fill="#a7f3d0" font-size="8" font-family="monospace">Real-time latency &lt; 2ms</text>

    <rect x="14" y="115" width="180" height="40" rx="4" fill="#312e81"/>
    <text x="20" y="132" fill="#c084fc" font-size="8" font-family="monospace">Group: "search_indexer"</text>
    <text x="20" y="146" fill="#a7f3d0" font-size="8" font-family="monospace">Elasticsearch indexing</text>

    <rect x="14" y="165" width="180" height="40" rx="4" fill="#312e81"/>
    <text x="20" y="182" fill="#c084fc" font-size="8" font-family="monospace">Group: "data_lake_s3"</text>
    <text x="20" y="196" fill="#a7f3d0" font-size="8" font-family="monospace">Micro-batch to Iceberg</text>
  </g>

  <!-- FLOW ARROWS -->
  <path d="M 190 190 L 240 190" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-kf)"/>
  <path d="M 660 190 L 710 190" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-kf)"/>
</svg>
""",
        "codeSnippet": """// Production Kafka Producer in Go with Idempotency & Guaranteed Delivery
package main

import (
	"context"
	"fmt"
	"time"

	"github.com/segmentio/kafka-go"
)

func NewIdempotentProducer(brokers []string, topic string) *kafka.Writer {
	return &kafka.Writer{
		Addr:         kafka.TCP(brokers...),
		Topic:        topic,
		Balancer:     &kafka.Murmur2Balancer{}, // Consistent hash partitioner
		MaxAttempts:  5,
		BatchSize:    1000,                     // Micro-batch up to 1000 messages
		BatchBytes:   1048576,                  // Or 1 MB
		BatchTimeout: 10 * time.Millisecond,    // Or every 10ms
		RequiredAcks: kafka.RequireAll,         // acks=all: Wait for all in-sync replicas (ISR)
		Async:        false,                    // Synchronous flush confirmation
		Compression:  kafka.Lz4,                // High throughput compression
	}
}

func PublishOrderEvent(writer *kafka.Writer, orderID string, payload []byte) error {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Using OrderID as Key guarantees all events for this specific order
	// land in the exact same partition in strictly monotonic chronological sequence!
	msg := kafka.Message{
		Key:   []byte(orderID),
		Value: payload,
		Headers: []kafka.Header{
			{Key: "producer_version", Value: []byte("2.4.0")},
			{Key: "sent_at", Value: []byte(time.Now().UTC().Format(time.RFC3339Nano))},
		},
	}

	err := writer.WriteMessages(ctx, msg)
	if err != nil {
		return fmt.Errorf("kafka write failure after retries: %w", err)
	}

	return nil
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The LinkedIn Kafka Global Rebalance Storm Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 500 downstream microservices stopped consuming events, causing massive data pipelines to stall for 3 hours.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      A Java garbage collection pause of 35 seconds on a single consumer pod exceeded the configured <code>max.poll.interval.ms</code> (30 seconds).
      The Kafka Group Coordinator assumed that consumer was dead and initiated a <strong>Full Stop-the-World Consumer Group Rebalance</strong>.
    </p>
    <p>
      During the rebalance, all 200 consumer instances revoked their partition assignments.
      Because consumer startup took 40 seconds to initialize local state, multiple consumers timed out consecutively.
      <strong>This created an infinite cascade: Rebalance &rarr; Timeout &rarr; Rebalance &rarr; Timeout! Zero messages were processed for 3 hours!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Static Membership (KIP-345):</strong> Configure <code>group.instance.id</code> so rolling restarts or transient GC pauses do not trigger rebalances. The broker preserves partition ownership for up to 5 minutes.</li>
      <li><strong class="text-white">Cooperative Sticky Assignor (KIP-429):</strong> Replaces eager rebalancing. Only partitions that need to move are revoked; unaffected consumers continue processing messages without interruption.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "How does Apache Kafka guarantee Exactly-Once Semantics (EOS), and what happens when an upstream producer crashes midway through a transaction?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "Kafka achieves Exactly-Once Processing (EOS) through three tightly coupled primitives:
      <br><br>
      1. <strong>Idempotent Producer:</strong> The broker assigns each producer a unique 64-bit <code>Producer ID (PID)</code>. Every batch includes a monotonically incrementing <code>Sequence Number</code>. If network retries resend a batch, the broker recognizes <code>PID + SeqNum</code> and drops duplicates with zero overhead.
      <br><br>
      2. <strong>Transactional Coordinator &amp; WAL Markers:</strong> In a read-process-write pipeline (consume from Topic A &rarr; write to Topic B &rarr; commit offset to <code>__consumer_offsets</code>), the producer writes all outputs within a two-phase transaction.
      The Transaction Coordinator writes a <code>COMMIT</code> marker to the log.
      <br><br>
      3. <strong>Read-Committed Isolation:</strong> Downstream consumers configured with <code>isolation.level=read_committed</code> buffer uncommitted messages and only release them to the application when the <code>COMMIT</code> marker appears. If the producer crashes, the transaction times out, an <code>ABORT</code> marker is written, and consumers transparently discard the uncommitted batch!"
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 3 loaded with {len(STAGE_3_CHAPTERS)} comprehensive chapters.")
