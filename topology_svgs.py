# topology_svgs.py
# High-Resolution Canonical SVG Architectural Topologies for all 12 Google Staff Modules
# Plus Stencil Layout Data for 1-Click Interactive Whiteboard Loading

def get_svg_topology(ch_id, title, color="cyan"):
    svgs = {
        "ch1": """
<svg viewBox="0 0 920 310" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-cyan-900/50 p-2 shadow-2xl">
  <defs>
    <linearGradient id="g1-edge" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#082f49"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="g1-kafka" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#064e3b"/><stop offset="100%" stop-color="#042f2e" stop-opacity="0.5"/></linearGradient>
    <linearGradient id="g1-sink" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3b0764"/><stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.4"/></linearGradient>
    <marker id="arr-c1" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#00f0ff"/></marker>
    <marker id="arr-g1" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/></marker>
  </defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(20, 35)">
    <rect width="160" height="90" rx="8" fill="url(#g1-edge)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="14" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">EDGE INGRESS</text>
    <text x="14" y="44" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">20M Cell Towers</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10" font-family="sans-serif">eCPRI / IPSec / TLS 1.3</text>
    <text x="14" y="78" fill="#00f0ff" font-size="9" font-family="monospace">45k TPS Wire Rate</text>
  </g>
  <line x1="180" y1="80" x2="230" y2="80" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-c1)"/>
  <text x="185" y="72" fill="#67e8f9" font-size="9" font-family="monospace">gRPC</text>
  <g transform="translate(230, 30)">
    <rect width="190" height="100" rx="8" fill="url(#g1-edge)" stroke="#00f0ff" stroke-width="1.8"/>
    <text x="14" y="22" fill="#00f0ff" font-size="10" font-family="monospace" font-weight="bold">INGRESS GATEWAY</text>
    <text x="14" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Envoy Proxy (48 Pods)</text>
    <text x="14" y="60" fill="#cbd5e1" font-size="10" font-family="sans-serif">Token Bucket Limiter</text>
    <text x="14" y="76" fill="#94a3b8" font-size="9" font-family="sans-serif">Murmur2 Partition Hash</text>
    <text x="14" y="90" fill="#38bdf8" font-size="9" font-family="monospace">Zero-Copy DMA Socket</text>
  </g>
  <line x1="420" y1="80" x2="475" y2="80" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-c1)"/>
  <text x="424" y="72" fill="#67e8f9" font-size="9" font-family="monospace">acks=all</text>
  <g transform="translate(475, 15)">
    <rect width="215" height="130" rx="8" fill="url(#g1-kafka)" stroke="#10b981" stroke-width="1.8"/>
    <text x="14" y="24" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">DISTRIBUTED LOG STREAM</text>
    <text x="14" y="44" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Kafka KRaft Cluster</text>
    <text x="14" y="62" fill="#6ee7b7" font-size="10" font-family="monospace">6 Brokers • 128 Partitions</text>
    <text x="14" y="80" fill="#94a3b8" font-size="10" font-family="sans-serif">Linux PageCache (128GB)</text>
    <text x="14" y="96" fill="#94a3b8" font-size="9" font-family="sans-serif">Zero-Copy sendfile() -&gt; NIC</text>
    <text x="14" y="112" fill="#a7f3d0" font-size="9" font-family="monospace">ISR Quorum: min.insync=2</text>
  </g>
  <line x1="690" y1="50" x2="740" y2="40" stroke="#10b981" stroke-width="1.8" marker-end="url(#arr-g1)"/>
  <line x1="690" y1="80" x2="740" y2="105" stroke="#10b981" stroke-width="1.8" marker-end="url(#arr-g1)"/>
  <line x1="690" y1="110" x2="740" y2="175" stroke="#10b981" stroke-width="1.8" marker-end="url(#arr-g1)"/>
  <g transform="translate(740, 15)">
    <rect width="160" height="55" rx="6" fill="url(#g1-sink)" stroke="#c084fc" stroke-width="1.2"/>
    <text x="10" y="18" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold">INGESTION CONSUMER</text>
    <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Spring Boot 21 Fleet</text>
    <text x="10" y="48" fill="#e9d5ff" font-size="9" font-family="monospace">Cooperative Sticky</text>
  </g>
  <g transform="translate(740, 80)">
    <rect width="160" height="55" rx="6" fill="url(#g1-sink)" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="10" y="18" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">STREAM CEP ENGINE</text>
    <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Apache Flink Cluster</text>
    <text x="10" y="48" fill="#93c5fd" font-size="9" font-family="monospace">SLA Alarms &lt; 100ms</text>
  </g>
  <g transform="translate(740, 145)">
    <rect width="160" height="55" rx="6" fill="url(#g1-sink)" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="10" y="18" fill="#f59e0b" font-size="9" font-family="monospace" font-weight="bold">ANALYTICS SINK</text>
    <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">ClickHouse / ScyllaDB</text>
    <text x="10" y="48" fill="#fcd34d" font-size="9" font-family="monospace">Zero-Copy Batch Load</text>
  </g>
  <g transform="translate(20, 245)">
    <rect width="880" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">GOOGLE L6 SLA GUARANTEES:</text>
    <text x="210" y="25" fill="#00f0ff" font-size="10" font-family="monospace" font-weight="bold">p99 &lt; 42ms Ingress ACK</text>
    <text x="400" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">45,000 TPS Ingestion</text>
    <text x="590" y="25" fill="#f59e0b" font-size="10" font-family="monospace" font-weight="bold">Zero JVM Heap in Hot Path</text>
    <text x="790" y="25" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">0 Lost Records</text>
  </g>
</svg>
""",
        "ch2": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-sky-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-sk" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#7dd3fc" font-size="10" font-family="monospace" font-weight="bold">HARDWARE INGRESS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">100 GbE Fiber NIC</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">ethtool rx-ring 4096</text>
    <text x="14" y="82" fill="#38bdf8" font-size="9" font-family="monospace">14.88 Mpps Wire Rate</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-sk)"/>
  <g transform="translate(270, 30)">
    <rect width="230" height="110" rx="8" fill="#082f49" stroke="#0284c7" stroke-width="1.8"/>
    <text x="14" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">KERNEL DRIVER HOOK</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">eBPF / XDP Driver Layer</text>
    <text x="14" y="66" fill="#f43f5e" font-size="10" font-family="monospace">✕ XDP_DROP (DDoS in 18ns)</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">✔ XDP_REDIRECT (AF_XDP UMEM)</text>
    <text x="14" y="100" fill="#94a3b8" font-size="9" font-family="sans-serif">Bypasses sk_buff allocation</text>
  </g>
  <line x1="500" y1="85" x2="560" y2="85" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-sk)"/>
  <g transform="translate(560, 35)">
    <rect width="220" height="100" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">USERSPACE BYPASS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">DPDK / io_uring Fastpath</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Pinned NUMA Core Polling</text>
    <text x="14" y="84" fill="#38bdf8" font-size="9" font-family="monospace">0 Context Switches / 0 Copy</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">PERFORMANCE BENCHMARK:</text>
    <text x="210" y="25" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">Packet Parse &lt; 850 ns</text>
    <text x="440" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">Zero Kernel Interrupt Overhead</text>
    <text x="730" y="25" fill="#f43f5e" font-size="10" font-family="monospace" font-weight="bold">100% Line-Rate Filter</text>
  </g>
</svg>
""",
        "ch3": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-purple-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-pr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#3b0764" stroke="#c084fc" stroke-width="1.5"/>
    <text x="14" y="24" fill="#e9d5ff" font-size="10" font-family="monospace" font-weight="bold">DISTRIBUTED CLIENTS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">500 Worker Pods</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Concurrent Mutation Requests</text>
    <text x="14" y="82" fill="#c084fc" font-size="9" font-family="monospace">Subject to GC Pauses</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#c084fc" stroke-width="2" marker-end="url(#arr-pr)"/>
  <g transform="translate(270, 30)">
    <rect width="240" height="110" rx="8" fill="#2e1065" stroke="#a855f7" stroke-width="1.8"/>
    <text x="14" y="24" fill="#d8b4fe" font-size="10" font-family="monospace" font-weight="bold">ATOMIC LOCK COORDINATOR</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Redis Master / Lua Script</text>
    <text x="14" y="66" fill="#a855f7" font-size="10" font-family="monospace">Key: lock:cell-101 (TTL 10s)</text>
    <text x="14" y="84" fill="#38bdf8" font-size="10" font-family="monospace">INCR token:cell-101 -&gt; #1049281</text>
    <text x="14" y="100" fill="#94a3b8" font-size="9" font-family="sans-serif">64-bit Monotonic Sequence</text>
  </g>
  <line x1="510" y1="85" x2="570" y2="85" stroke="#c084fc" stroke-width="2" marker-end="url(#arr-pr)"/>
  <g transform="translate(570, 30)">
    <rect width="300" height="110" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.8"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">STORAGE VERIFICATION BARRIER</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">PostgreSQL / ScyllaDB Sink</text>
    <text x="14" y="66" fill="#10b981" font-size="10" font-family="monospace">UPDATE cell SET tx_pwr = 45.0</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">WHERE token &gt; last_token;</text>
    <text x="14" y="100" fill="#f43f5e" font-size="9" font-family="monospace">Stale Zombie Writes Replaced (0 Corruptions)</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">GOOGLE L6 INVARIANT:</text>
    <text x="210" y="25" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">No Lock Expiration Ever Corrupts Data</text>
    <text x="560" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">Enforced by Monotonic Fencing Token</text>
  </g>
</svg>
""",
        "ch4": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-indigo-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-in" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#818cf8"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 65)">
    <rect width="160" height="80" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">PROPOSAL CLIENT</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">State Machine Write</text>
    <text x="14" y="66" fill="#94a3b8" font-size="9" font-family="monospace">Linearizable Put(k, v)</text>
  </g>
  <line x1="190" y1="105" x2="250" y2="105" stroke="#818cf8" stroke-width="2" marker-end="url(#arr-in)"/>
  <g transform="translate(250, 30)">
    <rect width="210" height="150" rx="8" fill="#312e81" stroke="#6366f1" stroke-width="2"/>
    <text x="14" y="24" fill="#c7d2fe" font-size="10" font-family="monospace" font-weight="bold">RAFT LEADER (TERM 2)</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Leader Node 1 (AZ-1)</text>
    <text x="14" y="66" fill="#38bdf8" font-size="10" font-family="monospace">WAL Append: index=492</text>
    <text x="14" y="84" fill="#94a3b8" font-size="9" font-family="sans-serif">AppendEntries Heartbeats</text>
    <text x="14" y="102" fill="#10b981" font-size="10" font-family="monospace">CommitIndex &gt; HighWatermark</text>
    <text x="14" y="122" fill="#a5b4fc" font-size="9" font-family="sans-serif">Applies to State Machine</text>
  </g>
  <line x1="460" y1="60" x2="530" y2="35" stroke="#6366f1" stroke-width="1.8" marker-end="url(#arr-in)"/>
  <line x1="460" y1="105" x2="530" y2="105" stroke="#6366f1" stroke-width="1.8" marker-end="url(#arr-in)"/>
  <line x1="460" y1="150" x2="530" y2="175" stroke="#6366f1" stroke-width="1.8" marker-end="url(#arr-in)"/>
  <g transform="translate(530, 15)">
    <rect width="180" height="45" rx="6" fill="#1e1b4b" stroke="#10b981" stroke-width="1.2"/>
    <text x="10" y="18" fill="#10b981" font-size="10" font-family="monospace">Follower 2 (AZ-1) ✔ ACK</text>
    <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Log Matched (Term 2, Idx 492)</text>
  </g>
  <g transform="translate(530, 85)">
    <rect width="180" height="45" rx="6" fill="#1e1b4b" stroke="#10b981" stroke-width="1.2"/>
    <text x="10" y="18" fill="#10b981" font-size="10" font-family="monospace">Follower 3 (AZ-2) ✔ ACK</text>
    <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Log Matched (Term 2, Idx 492)</text>
  </g>
  <g transform="translate(530, 155)">
    <rect width="180" height="45" rx="6" fill="#1e1b4b" stroke="#f43f5e" stroke-width="1.2"/>
    <text x="10" y="18" fill="#f43f5e" font-size="10" font-family="monospace">Follower 4 (AZ-3) ✕ TIMEOUT</text>
    <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Minority Partition (Ignored)</text>
  </g>
  <g transform="translate(30, 225)">
    <rect width="860" height="35" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="23" fill="#64748b" font-size="10" font-family="monospace">CONSENSUS QUORUM:</text>
    <text x="180" y="23" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">3 of 5 Majority Quorum Achieved (Leader + F2 + F3)</text>
    <text x="690" y="23" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">p99 &lt; 3.5ms Commit</text>
  </g>
</svg>
""",
        "ch5": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-emerald-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-em" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="14" y="24" fill="#6ee7b7" font-size="10" font-family="monospace" font-weight="bold">RAW DATA LAKE</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">ASN.1 CDR Files (2GB)</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Memory-Mapped FileChannel</text>
    <text x="14" y="82" fill="#10b981" font-size="9" font-family="monospace">Zero Heap Copies</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#10b981" stroke-width="2" marker-end="url(#arr-em)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#042f2e" stroke="#14b8a6" stroke-width="1.8"/>
    <text x="14" y="24" fill="#5eead4" font-size="10" font-family="monospace" font-weight="bold">VIRTUAL THREAD ENGINE</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Java 21 Loom Workers</text>
    <text x="14" y="66" fill="#a7f3d0" font-size="10" font-family="monospace">1,000 Concurrent Virtual Workers</text>
    <text x="14" y="84" fill="#94a3b8" font-size="9" font-family="sans-serif">Chunk Size: 2,500 records</text>
    <text x="14" y="100" fill="#f43f5e" font-size="9" font-family="monospace">Corrupt? -&gt; Kafka DLQ (&lt;1ms)</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#10b981" stroke-width="2" marker-end="url(#arr-em)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">BATCH STORAGE SINK</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">ScyllaDB / PostgreSQL</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Batched JDBC executeBatch()</text>
    <text x="14" y="84" fill="#10b981" font-size="9" font-family="monospace">Auto-Commit: DISABLED</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">BATCH SLA:</text>
    <text x="160" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">50,000 CDR/s Sustained</text>
    <text x="420" y="25" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">&lt; 1.5 GB Heap Memory Footprint</text>
    <text x="730" y="25" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">Zero Job Restarts</text>
  </g>
</svg>
""",
        "ch6": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-teal-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-te" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#14b8a6"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#134e4a" stroke="#14b8a6" stroke-width="1.5"/>
    <text x="14" y="24" fill="#5eead4" font-size="10" font-family="monospace" font-weight="bold">INGRESS STREAM</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Kafka Telemetry Topic</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Event-Time Watermarks</text>
    <text x="14" y="82" fill="#14b8a6" font-size="9" font-family="monospace">BoundedOutOfOrderness(5s)</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#14b8a6" stroke-width="2" marker-end="url(#arr-te)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#042f2e" stroke="#0d9488" stroke-width="1.8"/>
    <text x="14" y="24" fill="#2dd4bf" font-size="10" font-family="monospace" font-weight="bold">FLINK CEP ENGINE</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">KeyBy(tower_id) • 10m Window</text>
    <text x="14" y="66" fill="#99f6e4" font-size="10" font-family="monospace">State: EmbeddedRocksDB (NVMe)</text>
    <text x="14" y="84" fill="#94a3b8" font-size="9" font-family="sans-serif">Chandy-Lamport Checkpoints</text>
    <text x="14" y="100" fill="#38bdf8" font-size="9" font-family="monospace">Exactly-Once Semantics</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#14b8a6" stroke-width="2" marker-end="url(#arr-te)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#31104b" stroke="#c084fc" stroke-width="1.5"/>
    <text x="14" y="24" fill="#e9d5ff" font-size="10" font-family="monospace" font-weight="bold">TWO-PHASE SINK</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Kafka 2PC / ClickHouse</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Real-Time Anomaly Alarms</text>
    <text x="14" y="84" fill="#14b8a6" font-size="9" font-family="monospace">SLA: Alert &lt; 100ms</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">STREAM SLA:</text>
    <text x="160" y="25" fill="#14b8a6" font-size="10" font-family="monospace" font-weight="bold">Sub-100ms End-to-End Latency</text>
    <text x="440" y="25" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">Off-Heap RocksDB State (Zero GC)</text>
    <text x="740" y="25" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">Zero Lost Events</text>
  </g>
</svg>
""",
        "ch7": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-amber-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-am" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#451a03" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="14" y="24" fill="#fcd34d" font-size="10" font-family="monospace" font-weight="bold">3GPP DIAMETER INGRESS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">CCR-Initial / Update</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Rating Group &amp; MSISDN</text>
    <text x="14" y="82" fill="#f59e0b" font-size="9" font-family="monospace">Quota Reservation Req</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#f59e0b" stroke-width="2" marker-end="url(#arr-am)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#291402" stroke="#d97706" stroke-width="1.8"/>
    <text x="14" y="24" fill="#fbbf24" font-size="10" font-family="monospace" font-weight="bold">LOCK-FREE RADIX TREE</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Tariff Charging Tree (CTE)</text>
    <text x="14" y="66" fill="#fde68a" font-size="10" font-family="monospace">Tenant Root -&gt; RatingGroup</text>
    <text x="14" y="84" fill="#94a3b8" font-size="9" font-family="sans-serif">Atomic Pointer Swap root_.load()</text>
    <text x="14" y="100" fill="#10b981" font-size="9" font-family="monospace">0 DB Round-Trips in Hot Path</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#f59e0b" stroke-width="2" marker-end="url(#arr-am)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">RESERVATION BUCKET</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Redis Token Bucket Cluster</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Decrement Quota Reserve</text>
    <text x="14" y="84" fill="#f59e0b" font-size="9" font-family="monospace">CCA Answer with GSU</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">3GPP SLA:</text>
    <text x="160" y="25" fill="#f59e0b" font-size="10" font-family="monospace" font-weight="bold">Rating Evaluation p99 &lt; 1.2ms</text>
    <text x="440" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">Sub-millisecond Quota Reserve</text>
    <text x="740" y="25" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">Lock-Free Reads</text>
  </g>
</svg>
""",
        "ch8": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-yellow-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-ye" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#eab308"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#422006" stroke="#eab308" stroke-width="1.5"/>
    <text x="14" y="24" fill="#fef08a" font-size="10" font-family="monospace" font-weight="bold">5G RADIO ACCESS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">gNodeB Cell Base</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">N3 GTP-U User Plane</text>
    <text x="14" y="82" fill="#eab308" font-size="9" font-family="monospace">N2 NGAP Control Plane</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#eab308" stroke-width="2" marker-end="url(#arr-ye)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#2d1a04" stroke="#ca8a04" stroke-width="1.8"/>
    <text x="14" y="24" fill="#fef08a" font-size="10" font-family="monospace" font-weight="bold">USER PLANE FUNCTION (UPF)</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">DPDK Fastpath Forwarding</text>
    <text x="14" y="66" fill="#fef9c3" font-size="10" font-family="monospace">N4 PFCP Session Mgmt</text>
    <text x="14" y="84" fill="#94a3b8" font-size="9" font-family="sans-serif">Decoupled from SBA Control</text>
    <text x="14" y="100" fill="#10b981" font-size="9" font-family="monospace">Forwarding Latency &lt; 50 µs</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#eab308" stroke-width="2" marker-end="url(#arr-ye)"/>
  <g transform="translate(580, 20)">
    <rect width="230" height="130" rx="8" fill="#082f49" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="14" y="22" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">5G SBA CONTROL PLANE</text>
    <text x="14" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">HTTP/2 JSON Mesh</text>
    <text x="14" y="62" fill="#7dd3fc" font-size="10" font-family="monospace">SMF (Session Management)</text>
    <text x="14" y="80" fill="#cbd5e1" font-size="9" font-family="sans-serif">CHF (Charging Function)</text>
    <text x="14" y="98" fill="#cbd5e1" font-size="9" font-family="sans-serif">PCF (Policy Control Function)</text>
    <text x="14" y="116" fill="#cbd5e1" font-size="9" font-family="sans-serif">UDM (Unified Data Mgmt)</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">5G CORE SLA:</text>
    <text x="160" y="25" fill="#eab308" font-size="10" font-family="monospace" font-weight="bold">User Plane &lt; 50 µs</text>
    <text x="360" y="25" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">99.999% Telecom Availability</text>
    <text x="640" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">Cloud-Native SBA Microservices</text>
  </g>
</svg>
""",
        "ch9": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-violet-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-vi" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#a78bfa"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 30)">
    <rect width="250" height="120" rx="8" fill="#2e1065" stroke="#a78bfa" stroke-width="1.8"/>
    <text x="14" y="24" fill="#c4b5fd" font-size="10" font-family="monospace" font-weight="bold">DATACENTER 1: US-EAST</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">ScyllaDB Ring (3 Replicas)</text>
    <text x="14" y="66" fill="#a78bfa" font-size="10" font-family="monospace">LOCAL_QUORUM Writes (2/3)</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">Local p99 Write &lt; 3.8ms</text>
    <text x="14" y="102" fill="#94a3b8" font-size="9" font-family="sans-serif">CommitLog NVMe O_DIRECT</text>
  </g>
  <line x1="280" y1="90" x2="350" y2="90" stroke="#a78bfa" stroke-width="2" marker-end="url(#arr-vi)"/>
  <line x1="350" y1="90" x2="280" y2="90" stroke="#a78bfa" stroke-width="2" marker-end="url(#arr-vi)"/>
  <g transform="translate(350, 45)">
    <rect width="200" height="90" rx="8" fill="#090d24" stroke="#6d28d9" stroke-width="1.5"/>
    <text x="14" y="24" fill="#c4b5fd" font-size="10" font-family="monospace" font-weight="bold">GOSSIP &amp; REPLICATION</text>
    <text x="14" y="44" fill="#ffffff" font-size="11" font-family="sans-serif">Murmur3 Token Ring</text>
    <text x="14" y="62" fill="#38bdf8" font-size="9" font-family="monospace">Async Cross-DC Sync</text>
    <text x="14" y="76" fill="#f43f5e" font-size="9" font-family="monospace">Cable Cut Immune!</text>
  </g>
  <line x1="550" y1="90" x2="620" y2="90" stroke="#a78bfa" stroke-width="2" marker-end="url(#arr-vi)"/>
  <g transform="translate(620, 30)">
    <rect width="250" height="120" rx="8" fill="#2e1065" stroke="#a78bfa" stroke-width="1.8"/>
    <text x="14" y="24" fill="#c4b5fd" font-size="10" font-family="monospace" font-weight="bold">DATACENTER 2: EU-CENTRAL</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">ScyllaDB Ring (3 Replicas)</text>
    <text x="14" y="66" fill="#a78bfa" font-size="10" font-family="monospace">LOCAL_QUORUM Writes (2/3)</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">Local p99 Write &lt; 4.1ms</text>
    <text x="14" y="102" fill="#94a3b8" font-size="9" font-family="sans-serif">Independent Availability</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">STORAGE INVARIANT:</text>
    <text x="210" y="25" fill="#a78bfa" font-size="10" font-family="monospace" font-weight="bold">Zero Cross-DC Blocking on Write</text>
    <text x="520" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">LOCAL_QUORUM Prevents Global Blackouts</text>
  </g>
</svg>
""",
        "ch10": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-rose-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-ro" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
    <text x="14" y="24" fill="#fda4af" font-size="10" font-family="monospace" font-weight="bold">GLOBAL ACID TX</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Cross-Region Transfer</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">US-East -&gt; EU-Central</text>
    <text x="14" y="82" fill="#f43f5e" font-size="9" font-family="monospace">External Consistency</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#f43f5e" stroke-width="2" marker-end="url(#arr-ro)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#2a0815" stroke="#e11d48" stroke-width="1.8"/>
    <text x="14" y="24" fill="#fb7185" font-size="10" font-family="monospace" font-weight="bold">TRUETIME API (HARDWARE)</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">GPS + Rubidium Clocks</text>
    <text x="14" y="66" fill="#fecdd3" font-size="10" font-family="monospace">TrueTime.now() -&gt; [earliest, latest]</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">Uncertainty Bound: ε &lt; 7ms</text>
    <text x="14" y="100" fill="#94a3b8" font-size="9" font-family="sans-serif">Wait Out Epsilon Before Commit</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#f43f5e" stroke-width="2" marker-end="url(#arr-ro)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">SPANNER TABLET 2PC</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Multi-Paxos Groups</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Two-Phase Commit Coord</text>
    <text x="14" y="84" fill="#f43f5e" font-size="9" font-family="monospace">Monotonic TrueTime TS</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">SPANNER INVARIANT:</text>
    <text x="210" y="25" fill="#f43f5e" font-size="10" font-family="monospace" font-weight="bold">Linearizable External Consistency Worldwide</text>
    <text x="620" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">Lock-Free Consistent Read Snapshots</text>
  </g>
</svg>
""",
        "ch11": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-pink-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-pi" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f472b6"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 40)">
    <rect width="180" height="90" rx="8" fill="#500724" stroke="#f472b6" stroke-width="1.5"/>
    <text x="14" y="24" fill="#fbcfe8" font-size="10" font-family="monospace" font-weight="bold">BURST INGRESS</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">250,000 QPS Spike</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Black Friday Flash Sale</text>
    <text x="14" y="82" fill="#f472b6" font-size="9" font-family="monospace">Thundering Herd Risk</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#f472b6" stroke-width="2" marker-end="url(#arr-pi)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#330a1c" stroke="#db2777" stroke-width="1.8"/>
    <text x="14" y="24" fill="#f472b6" font-size="10" font-family="monospace" font-weight="bold">GCRA RATE LIMITER</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Redis Single-Shard Lua</text>
    <text x="14" y="66" fill="#fbcfe8" font-size="10" font-family="monospace">TAT (Theoretical Arrival Time)</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">Eval Latency &lt; 0.4 ms</text>
    <text x="14" y="100" fill="#94a3b8" font-size="9" font-family="sans-serif">Eliminates 2x Window Boundary Burst</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#f472b6" stroke-width="2" marker-end="url(#arr-pi)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">ADAPTIVE CONCURRENCY</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">TCP Vegas Limiter</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">Measures Live RTT Gradient</text>
    <text x="14" y="84" fill="#f472b6" font-size="9" font-family="monospace">Prevents Queue Buildup</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">RESILIENCE INVARIANT:</text>
    <text x="210" y="25" fill="#f472b6" font-size="10" font-family="monospace" font-weight="bold">Microsecond Traffic Shaping</text>
    <text x="480" y="25" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">100% Fail-Open on Limiter Cluster Outage</text>
  </g>
</svg>
""",
        "ch12": """
<svg viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#030612] border border-cyan-900/50 p-2 shadow-2xl">
  <defs><marker id="arr-cy" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#00f0ff"/></marker></defs>
  <rect width="100%" height="100%" fill="#030612" rx="8"/>
  <g transform="translate(30, 30)">
    <rect width="180" height="110" rx="8" fill="#082f49" stroke="#0284c7" stroke-width="1.5"/>
    <text x="14" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">PHASE 1 &amp; 2</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Dual Writes &amp; Backfill</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="9" font-family="sans-serif">Sync: Primary DB (Oracle)</text>
    <text x="14" y="80" fill="#00f0ff" font-size="9" font-family="sans-serif">Async: Kafka Shadow Topic</text>
    <text x="14" y="96" fill="#94a3b8" font-size="9" font-family="monospace">500M Records Backfilled</text>
  </g>
  <line x1="210" y1="85" x2="270" y2="85" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-cy)"/>
  <g transform="translate(270, 30)">
    <rect width="250" height="110" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.8"/>
    <text x="14" y="24" fill="#6ee7b7" font-size="10" font-family="monospace" font-weight="bold">PHASE 3: CONTINUOUS PARITY</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Reconciler &amp; Shadow Read</text>
    <text x="14" y="66" fill="#a7f3d0" font-size="10" font-family="monospace">Dark Traffic Replay (14 Days)</text>
    <text x="14" y="84" fill="#10b981" font-size="10" font-family="monospace">100.000% Data Parity Verified</text>
    <text x="14" y="100" fill="#94a3b8" font-size="9" font-family="sans-serif">Monotonic Version Invariant</text>
  </g>
  <line x1="520" y1="85" x2="580" y2="85" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-cy)"/>
  <g transform="translate(580, 35)">
    <rect width="220" height="100" rx="8" fill="#31104b" stroke="#c084fc" stroke-width="1.5"/>
    <text x="14" y="24" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">PHASE 4: INSTANT CUTOVER</text>
    <text x="14" y="46" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">1-Second DNS / Envoy Swap</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">ScyllaDB Promoted Primary</text>
    <text x="14" y="84" fill="#10b981" font-size="9" font-family="monospace">0 Seconds Customer Downtime</text>
  </g>
  <g transform="translate(30, 215)">
    <rect width="860" height="40" rx="6" fill="#050a1f" stroke="#1e293b" stroke-width="1"/>
    <text x="20" y="25" fill="#64748b" font-size="10" font-family="monospace">MIGRATION INVARIANT:</text>
    <text x="210" y="25" fill="#00f0ff" font-size="10" font-family="monospace" font-weight="bold">Zero Lost Updates • Instant Rollback Safety • 100% Proven Parity</text>
  </g>
</svg>
"""
    }
    return svgs.get(ch_id, svgs["ch1"])

# Stencils for 1-click loading into Split Studio or Whiteboard
STENCIL_PRESETS = {
    "ch1": [
        {"type": "gateway", "x": 40, "y": 70, "title": "Envoy Gateway", "desc": "48 Pods • Rate Limited"},
        {"type": "kafka", "x": 190, "y": 70, "title": "Kafka KRaft", "desc": "6 Brokers • 128 Partitions"},
        {"type": "pod", "x": 340, "y": 30, "title": "Spring Consumer", "desc": "Cooperative Sticky"},
        {"type": "scylla", "x": 340, "y": 130, "title": "ScyllaDB Tier", "desc": "LSM Engine • NVMe"},
    ],
    "ch2": [
        {"type": "gateway", "x": 40, "y": 70, "title": "100 GbE NIC", "desc": "14.88 Mpps Wire Rate"},
        {"type": "pod", "x": 190, "y": 70, "title": "eBPF / XDP Hook", "desc": "Drop 18ns / AF_XDP"},
        {"type": "pod", "x": 340, "y": 70, "title": "DPDK Polling", "desc": "Pinned NUMA Fastpath"},
    ],
    "ch3": [
        {"type": "pod", "x": 40, "y": 70, "title": "Worker Pods", "desc": "500 K8s Workers"},
        {"type": "redis", "x": 190, "y": 70, "title": "Redis Master", "desc": "Atomic Lua + Token"},
        {"type": "postgres", "x": 340, "y": 70, "title": "PostgreSQL Sink", "desc": "WHERE token > last"},
    ],
    "ch4": [
        {"type": "pod", "x": 40, "y": 70, "title": "Proposal Client", "desc": "Linearizable Write"},
        {"type": "pod", "x": 190, "y": 70, "title": "Raft Leader", "desc": "Term 2 • High Watermark"},
        {"type": "pod", "x": 340, "y": 30, "title": "Follower 1 (AZ1)", "desc": "Quorum ACK"},
        {"type": "pod", "x": 340, "y": 130, "title": "Follower 2 (AZ2)", "desc": "Quorum ACK"},
    ],
    "ch5": [
        {"type": "gateway", "x": 40, "y": 70, "title": "Raw ASN.1 Lake", "desc": "2GB Memory-Mapped"},
        {"type": "pod", "x": 190, "y": 70, "title": "Virtual Threads", "desc": "1,000 Loom Workers"},
        {"type": "scylla", "x": 340, "y": 70, "title": "Database Sink", "desc": "50k CDR/s Batched"},
    ],
    "ch6": [
        {"type": "kafka", "x": 40, "y": 70, "title": "Kafka Ingress", "desc": "45k TPS Telemetry"},
        {"type": "pod", "x": 190, "y": 70, "title": "Flink CEP", "desc": "RocksDB State NVMe"},
        {"type": "scylla", "x": 340, "y": 70, "title": "2PC Sink", "desc": "Alerts < 100ms"},
    ],
    "ch7": [
        {"type": "gateway", "x": 40, "y": 70, "title": "Diameter CCR", "desc": "Rating Group Ingress"},
        {"type": "pod", "x": 190, "y": 70, "title": "Radix Tree DAG", "desc": "Lock-Free Radix Tree"},
        {"type": "redis", "x": 340, "y": 70, "title": "Token Bucket", "desc": "Reserve Quota < 1.2ms"},
    ],
    "ch8": [
        {"type": "pod", "x": 40, "y": 70, "title": "gNodeB Base", "desc": "N3 GTP-U Radio"},
        {"type": "gateway", "x": 190, "y": 70, "title": "UPF Fastpath", "desc": "DPDK Forward < 50µs"},
        {"type": "pod", "x": 340, "y": 70, "title": "5G SBA SMF/CHF", "desc": "HTTP/2 JSON Mesh"},
    ],
    "ch9": [
        {"type": "scylla", "x": 40, "y": 70, "title": "DC1: US-East", "desc": "LOCAL_QUORUM (2/3)"},
        {"type": "pod", "x": 190, "y": 70, "title": "Gossip Ring", "desc": "Murmur3 Cross-DC"},
        {"type": "scylla", "x": 340, "y": 70, "title": "DC2: EU-Central", "desc": "LOCAL_QUORUM (2/3)"},
    ],
    "ch10": [
        {"type": "pod", "x": 40, "y": 70, "title": "Global ACID Tx", "desc": "External Consistency"},
        {"type": "pod", "x": 190, "y": 70, "title": "TrueTime Engine", "desc": "GPS + Atomic ε < 7ms"},
        {"type": "postgres", "x": 340, "y": 70, "title": "Spanner 2PC", "desc": "Multi-Paxos Tablets"},
    ],
    "ch11": [
        {"type": "gateway", "x": 40, "y": 70, "title": "Burst Ingress", "desc": "250k QPS Wire Spike"},
        {"type": "redis", "x": 190, "y": 70, "title": "GCRA Lua Sentry", "desc": "TAT Microsecond Rate"},
        {"type": "pod", "x": 340, "y": 70, "title": "Vegas Limiter", "desc": "Adaptive Concurrency"},
    ],
    "ch12": [
        {"type": "pod", "x": 40, "y": 70, "title": "Dual Writer", "desc": "Oracle Sync + Kafka"},
        {"type": "pod", "x": 190, "y": 70, "title": "Parity Sentry", "desc": "14-Day Dark Replay"},
        {"type": "scylla", "x": 340, "y": 70, "title": "Promoted Primary", "desc": "1-Sec DNS Cutover"},
    ],
}
