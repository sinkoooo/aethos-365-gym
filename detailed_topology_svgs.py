# detailed_topology_svgs.py
# Extremely detailed, production-grade Google Staff (L6/L8) System Architecture Diagrams
# Multi-tier enterprise schematics with Ingress, Gateways, Kernel Bypass, Queues, Compute, Storage, Observability

def get_detailed_svg(ch_id, title):
    # Standard dimensions: 1040 x 540 for deep multi-tier architectural schematics
    svgs = {
        "ch1": """
<svg viewBox="0 0 1060 560" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#020512] border border-cyan-900/60 p-3 shadow-2xl">
  <defs>
    <linearGradient id="bg-edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#082f49" stop-opacity="0.9"/><stop offset="100%" stop-color="#0369a1" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-gw" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0e3a5a" stop-opacity="0.9"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-kafka" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#064e3b" stop-opacity="0.95"/><stop offset="100%" stop-color="#042f2e" stop-opacity="0.4"/></linearGradient>
    <linearGradient id="bg-compute" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3b0764" stop-opacity="0.9"/><stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.4"/></linearGradient>
    <linearGradient id="bg-store" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#431407" stop-opacity="0.9"/><stop offset="100%" stop-color="#7c2d12" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-obs" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1e293b" stop-opacity="0.9"/><stop offset="100%" stop-color="#0f172a" stop-opacity="0.4"/></linearGradient>
    
    <marker id="arr-cyan" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#00f0ff"/></marker>
    <marker id="arr-em" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/></marker>
    <marker id="arr-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/></marker>
    <marker id="arr-purp" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc"/></marker>
  </defs>

  <!-- Blueprint Background Grid -->
  <pattern id="grid-pattern-ch1" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.5" stroke-opacity="0.3"/>
  </pattern>
  <rect width="100%" height="100%" fill="url(#grid-pattern-ch1)" rx="8"/>

  <!-- TIER BOUNDARY HEADERS -->
  <g font-family="monospace" font-size="9" font-weight="bold" fill="#64748b" letter-spacing="1">
    <text x="30" y="24">TIER 1: EDGE INGRESS</text>
    <text x="210" y="24">TIER 2: API GATEWAY &amp; ROUTING</text>
    <text x="440" y="24">TIER 3: KAFKA 3.6+ KRAFT CLUSTER</text>
    <text x="730" y="24">TIER 4: COMPUTE &amp; PERSISTENCE</text>
  </g>
  <line x1="20" y1="32" x2="1040" y2="32" stroke="#1e293b" stroke-width="1"/>

  <!-- ==================== TIER 1: CLIENTS & EDGE ==================== -->
  <g transform="translate(25, 50)">
    <rect width="160" height="110" rx="8" fill="url(#bg-edge)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="12" y="22" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">TELECOM EDGE</text>
    <text x="12" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">20M Cell Towers</text>
    <text x="12" y="60" fill="#94a3b8" font-size="10" font-family="sans-serif">eCPRI / IPSec / 5G UPF</text>
    <text x="12" y="78" fill="#00f0ff" font-size="9" font-family="monospace">45k TPS Ingress Wire</text>
    <text x="12" y="94" fill="#cbd5e1" font-size="9" font-family="sans-serif">Avg Payload: 1.0 KB</text>
  </g>

  <g transform="translate(25, 180)">
    <rect width="160" height="95" rx="8" fill="url(#bg-edge)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="12" y="22" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">L4 ANYCAST FABRIC</text>
    <text x="12" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Google Maglev LB</text>
    <text x="12" y="60" fill="#94a3b8" font-size="10" font-family="sans-serif">Consistent Hash (ECMP)</text>
    <text x="12" y="78" fill="#a7f3d0" font-size="9" font-family="monospace">p99 &lt; 0.2ms Dispatch</text>
  </g>

  <g transform="translate(25, 295)">
    <rect width="160" height="95" rx="8" fill="url(#bg-edge)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="12" y="22" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">EDGE SECURITY</text>
    <text x="12" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Cloud Armor WAF</text>
    <text x="12" y="60" fill="#94a3b8" font-size="10" font-family="sans-serif">DDoS Mitigation (SYN/UDP)</text>
    <text x="12" y="78" fill="#f43f5e" font-size="9" font-family="monospace">Token Rate Filter</text>
  </g>

  <!-- Connectors Tier 1 -> Tier 2 -->
  <line x1="185" y1="105" x2="225" y2="105" stroke="#00f0ff" stroke-width="1.8" marker-end="url(#arr-cyan)"/>
  <text x="188" y="98" fill="#67e8f9" font-size="8" font-family="monospace">TLS 1.3</text>
  <line x1="185" y1="225" x2="225" y2="160" stroke="#00f0ff" stroke-width="1.8" marker-end="url(#arr-cyan)"/>

  <!-- ==================== TIER 2: GATEWAY & ROUTING ==================== -->
  <g transform="translate(225, 50)">
    <rect width="195" height="150" rx="8" fill="url(#bg-gw)" stroke="#00f0ff" stroke-width="1.8"/>
    <text x="14" y="22" fill="#00f0ff" font-size="10" font-family="monospace" font-weight="bold">INGRESS GATEWAYS</text>
    <text x="14" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Envoy Proxy Fleet (48 Pods)</text>
    <text x="14" y="60" fill="#cbd5e1" font-size="10" font-family="sans-serif">• HTTP/2 gRPC Streaming Ingress</text>
    <text x="14" y="76" fill="#cbd5e1" font-size="10" font-family="sans-serif">• Token Bucket Rate Limiting (2.5k/s)</text>
    <text x="14" y="92" fill="#cbd5e1" font-size="10" font-family="sans-serif">• Protobuf Deserialization</text>
    <text x="14" y="108" fill="#38bdf8" font-size="9" font-family="monospace">Murmur2(PartitionKey) Routing</text>
    <text x="14" y="126" fill="#a7f3d0" font-size="9" font-family="monospace">Zero-Copy Producer (acks=all)</text>
    <text x="14" y="140" fill="#94a3b8" font-size="8" font-family="monospace">min.insync.replicas = 2</text>
  </g>

  <g transform="translate(225, 220)">
    <rect width="195" height="100" rx="8" fill="url(#bg-gw)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="14" y="22" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">KERNEL NETWORKING</text>
    <text x="14" y="42" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Linux IO &amp; Socket Ring</text>
    <text x="14" y="60" fill="#cbd5e1" font-size="10" font-family="sans-serif">SO_REUSEPORT Multi-Core</text>
    <text x="14" y="76" fill="#a7f3d0" font-size="9" font-family="monospace">TCP BBR Congestion Control</text>
    <text x="14" y="90" fill="#94a3b8" font-size="8" font-family="sans-serif">ethtool rx-ring = 4096 frames</text>
  </g>

  <!-- Connectors Tier 2 -> Tier 3 -->
  <line x1="420" y1="120" x2="455" y2="120" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-cyan)"/>
  <text x="424" y="112" fill="#67e8f9" font-size="8" font-family="monospace">batch=64KB</text>
  <line x1="420" y1="150" x2="455" y2="240" stroke="#00f0ff" stroke-width="1.8" marker-end="url(#arr-cyan)"/>

  <!-- ==================== TIER 3: KAFKA 3.6+ KRAFT CLUSTER ==================== -->
  <g transform="translate(455, 45)">
    <rect width="255" height="340" rx="8" fill="url(#bg-kafka)" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="24" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">DISTRIBUTED LOG STREAM</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">Kafka 3.6+ KRaft Cluster</text>
    <text x="14" y="62" fill="#6ee7b7" font-size="10" font-family="monospace">6 Brokers • 128 Partitions</text>
    
    <!-- KRaft Metadata Quorum Box -->
    <g transform="translate(12, 72)">
      <rect width="230" height="48" rx="6" fill="#042f2e" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold">KRaft Controller Quorum (3 Nodes)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Raft Metadata Replication (Zero ZooKeeper)</text>
    </g>

    <!-- Broker 1 (Leader) -->
    <g transform="translate(12, 128)">
      <rect width="230" height="60" rx="6" fill="#022c22" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#a7f3d0" font-size="9" font-family="monospace" font-weight="bold">Broker 101 (AZ-1 Leader: P0..P21)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Linux PageCache (128 GB RAM Allocation)</text>
      <text x="10" y="48" fill="#00f0ff" font-size="8" font-family="monospace">Zero-Copy sendfile() -&gt; NIC DMA</text>
    </g>

    <!-- Broker 2 (Leader) -->
    <g transform="translate(12, 196)">
      <rect width="230" height="60" rx="6" fill="#022c22" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#a7f3d0" font-size="9" font-family="monospace" font-weight="bold">Broker 102 (AZ-2 Leader: P22..P43)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">NVMe RAID-10 Direct I/O (O_DIRECT)</text>
      <text x="10" y="48" fill="#38bdf8" font-size="8" font-family="monospace">dirty_ratio=10% | background=5%</text>
    </g>

    <!-- Quorum Replicas Info -->
    <g transform="translate(12, 264)">
      <rect width="230" height="60" rx="6" fill="#022c22" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#a7f3d0" font-size="9" font-family="monospace" font-weight="bold">Cross-AZ In-Sync Replicas (ISR)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Synchronous ACKs across AZ-1, AZ-2, AZ-3</text>
      <text x="10" y="48" fill="#f59e0b" font-size="8" font-family="monospace">Zero Data Loss SLA: RPO=0, RTO &lt; 3s</text>
    </g>
  </g>

  <!-- Connectors Tier 3 -> Tier 4 -->
  <line x1="710" y1="110" x2="745" y2="85" stroke="#10b981" stroke-width="2" marker-end="url(#arr-em)"/>
  <text x="712" y="98" fill="#a7f3d0" font-size="8" font-family="monospace">StickyAssign</text>
  <line x1="710" y1="180" x2="745" y2="190" stroke="#10b981" stroke-width="2" marker-end="url(#arr-em)"/>
  <text x="712" y="172" fill="#a7f3d0" font-size="8" font-family="monospace">Event-Time</text>
  <line x1="710" y1="280" x2="745" y2="305" stroke="#10b981" stroke-width="2" marker-end="url(#arr-em)"/>
  <text x="712" y="272" fill="#a7f3d0" font-size="8" font-family="monospace">2PC Sink</text>

  <!-- ==================== TIER 4: CONSUMERS, COMPUTE & STORAGE ==================== -->
  <!-- Consumer Fleet: Spring Boot / Loom -->
  <g transform="translate(745, 45)">
    <rect width="285" height="95" rx="8" fill="url(#bg-compute)" stroke="#c084fc" stroke-width="1.8"/>
    <text x="12" y="20" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold">REAL-TIME INGESTION FLEET</text>
    <text x="12" y="38" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Spring Boot 21 (Loom Virtual Threads)</text>
    <text x="12" y="54" fill="#e9d5ff" font-size="9" font-family="sans-serif">• CooperativeStickyAssignor (Rebalance &lt; 400ms)</text>
    <text x="12" y="70" fill="#e9d5ff" font-size="9" font-family="sans-serif">• Lock-Free Disruptor RingBuffer (1,000 workers)</text>
    <text x="12" y="86" fill="#38bdf8" font-size="8" font-family="monospace">Batch Insert: executeBatch(2500) | No AutoCommit</text>
  </g>

  <!-- Stream CEP Engine: Flink -->
  <g transform="translate(745, 150)">
    <rect width="285" height="95" rx="8" fill="url(#bg-compute)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="12" y="20" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">COMPLEX EVENT PROCESSING (CEP)</text>
    <text x="12" y="38" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Apache Flink Stream Cluster</text>
    <text x="12" y="54" fill="#cbd5e1" font-size="9" font-family="sans-serif">• 10m Sliding Windows keyed by Tower_ID</text>
    <text x="12" y="70" fill="#cbd5e1" font-size="9" font-family="sans-serif">• EmbeddedRocksDB State Backend on NVMe SSD</text>
    <text x="12" y="86" fill="#10b981" font-size="8" font-family="monospace">SLA Anomaly Detection Alert &lt; 100ms</text>
  </g>

  <!-- Storage: ScyllaDB & S3 Cold Tier -->
  <g transform="translate(745, 255)">
    <rect width="285" height="130" rx="8" fill="url(#bg-store)" stroke="#f59e0b" stroke-width="1.8"/>
    <text x="12" y="20" fill="#f59e0b" font-size="9" font-family="monospace" font-weight="bold">DISTRIBUTED PERSISTENCE TIER</text>
    <text x="12" y="38" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">ScyllaDB LSM-Tree + S3 Lakehouse</text>
    <text x="12" y="54" fill="#fde68a" font-size="9" font-family="sans-serif">• Hot Tier: ScyllaDB (LOCAL_QUORUM writes p99 &lt; 3.8ms)</text>
    <text x="12" y="70" fill="#fde68a" font-size="9" font-family="sans-serif">• Off-Heap MemTable + Leveled Compaction Strategy</text>
    <text x="12" y="86" fill="#fde68a" font-size="9" font-family="sans-serif">• Cold Tier: Vector Sink -&gt; Parquet files on S3/GCS</text>
    <text x="12" y="102" fill="#00f0ff" font-size="8" font-family="monospace">ClickHouse OLAP: 50B telemetry rows / sec query</text>
    <text x="12" y="118" fill="#f43f5e" font-size="8" font-family="monospace">Zero JVM GC Pauses (Seastar C++ Reactor)</text>
  </g>

  <!-- ==================== BOTTOM OBSERVABILITY & METRICS RIBBON ==================== -->
  <g transform="translate(25, 410)">
    <rect width="1005" height="120" rx="8" fill="url(#bg-obs)" stroke="#334155" stroke-width="1.5"/>
    <text x="16" y="22" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">CROSS-CUTTING GOVERNANCE, OBSERVABILITY &amp; KERNEL INVARIANTS</text>
    
    <g transform="translate(16, 34)" font-family="monospace" font-size="9">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <rect width="230" height="65" rx="6" fill="#020617" stroke="#0ea5e9" stroke-width="1"/>
        <text x="10" y="18" fill="#0ea5e9" font-weight="bold">OS Kernel Physics</text>
        <text x="10" y="34" fill="#94a3b8">vm.dirty_background_ratio = 5%</text>
        <text x="10" y="48" fill="#94a3b8">vm.dirty_ratio = 10% (No stalls)</text>
        <text x="10" y="60" fill="#10b981">sendfile() direct NIC DMA ring</text>
      </g>
      <!-- Item 2 -->
      <g transform="translate(245, 0)">
        <rect width="235" height="65" rx="6" fill="#020617" stroke="#10b981" stroke-width="1"/>
        <text x="10" y="18" fill="#10b981" font-weight="bold">Distributed Reliability</text>
        <text x="10" y="34" fill="#94a3b8">Producer acks=all | ISR min=2</text>
        <text x="10" y="48" fill="#94a3b8">CooperativeSticky incremental</text>
        <text x="10" y="60" fill="#38bdf8">Rebalance blackout: &lt; 400ms</text>
      </g>
      <!-- Item 3 -->
      <g transform="translate(495, 0)">
        <rect width="240" height="65" rx="6" fill="#020617" stroke="#f59e0b" stroke-width="1"/>
        <text x="10" y="18" fill="#f59e0b" font-weight="bold">Dead-Letter Isolation</text>
        <text x="10" y="34" fill="#94a3b8">Kafka DLQ quarantine &lt; 1ms</text>
        <text x="10" y="48" fill="#94a3b8">Corrupt ASN.1 isolated</text>
        <text x="10" y="60" fill="#f59e0b">Zero pipeline stalls</text>
      </g>
      <!-- Item 4 -->
      <g transform="translate(750, 0)">
        <rect width="225" height="65" rx="6" fill="#020617" stroke="#c084fc" stroke-width="1"/>
        <text x="10" y="18" fill="#c084fc" font-weight="bold">OpenTelemetry &amp; SLAs</text>
        <text x="10" y="34" fill="#94a3b8">W3C TraceContext propagated</text>
        <text x="10" y="48" fill="#94a3b8">Tail Sampling: 100% of &gt;50ms</text>
        <text x="10" y="60" fill="#c084fc">Edge-to-DB p99 &lt; 42ms</text>
      </g>
    </g>
  </g>
</svg>
""",
        "ch2": """
<svg viewBox="0 0 1060 560" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#020512] border border-sky-900/60 p-3 shadow-2xl">
  <defs>
    <linearGradient id="bg-nic" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0c4a6e" stop-opacity="0.95"/><stop offset="100%" stop-color="#075985" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-ebpf" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#082f49" stop-opacity="0.95"/><stop offset="100%" stop-color="#0369a1" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-dpdk" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#31104b" stop-opacity="0.95"/><stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.4"/></linearGradient>
    <marker id="arr-sky" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-rose" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/></marker>
    <marker id="arr-em2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/></marker>
  </defs>

  <pattern id="grid-pattern-ch2" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.5" stroke-opacity="0.3"/>
  </pattern>
  <rect width="100%" height="100%" fill="url(#grid-pattern-ch2)" rx="8"/>

  <g font-family="monospace" font-size="9" font-weight="bold" fill="#64748b" letter-spacing="1">
    <text x="30" y="24">TIER 1: PHYSICAL NIC HARDWARE</text>
    <text x="260" y="24">TIER 2: eBPF / XDP DRIVER LAYER</text>
    <text x="560" y="24">TIER 3: USERSPACE KERNEL BYPASS (DPDK / io_uring)</text>
    <text x="840" y="24">TIER 4: APPLICATION DISPATCH</text>
  </g>
  <line x1="20" y1="32" x2="1040" y2="32" stroke="#1e293b" stroke-width="1"/>

  <!-- TIER 1: PHYSICAL NIC -->
  <g transform="translate(25, 50)">
    <rect width="200" height="230" rx="8" fill="url(#bg-nic)" stroke="#38bdf8" stroke-width="2"/>
    <text x="14" y="24" fill="#7dd3fc" font-size="10" font-family="monospace" font-weight="bold">100 GbE OPTICAL NIC</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">Mellanox ConnectX-6</text>
    <text x="14" y="64" fill="#cbd5e1" font-size="10" font-family="sans-serif">• Dual 100 GbE QSFP28 Fiber</text>
    <text x="14" y="80" fill="#cbd5e1" font-size="10" font-family="sans-serif">• PCIe Gen 4.0 x16 (31.5 GB/s bus)</text>
    <text x="14" y="96" fill="#38bdf8" font-size="9" font-family="monospace">Wire Rate: 14.88 Mpps (64B)</text>
    <text x="14" y="112" fill="#cbd5e1" font-size="10" font-family="sans-serif">• Hardware RX FIFO Queues</text>

    <!-- Ring Buffers -->
    <g transform="translate(10, 126)">
      <rect width="180" height="42" rx="6" fill="#082f49" stroke="#0284c7" stroke-width="1"/>
      <text x="8" y="16" fill="#7dd3fc" font-size="8" font-family="monospace" font-weight="bold">ethtool rx-ring = 4096 descriptors</text>
      <text x="8" y="32" fill="#a7f3d0" font-size="8" font-family="sans-serif">Zero packet drops on burst</text>
    </g>
    <g transform="translate(10, 175)">
      <rect width="180" height="42" rx="6" fill="#082f49" stroke="#0284c7" stroke-width="1"/>
      <text x="8" y="16" fill="#7dd3fc" font-size="8" font-family="monospace" font-weight="bold">Hardware RSS (Receive Side Scale)</text>
      <text x="8" y="32" fill="#cbd5e1" font-size="8" font-family="sans-serif">Toeplitz Hash to 16 HW Queues</text>
    </g>
  </g>

  <!-- Connector Tier 1 -> Tier 2 -->
  <line x1="225" y1="140" x2="265" y2="140" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arr-sky)"/>
  <text x="230" y="132" fill="#7dd3fc" font-size="8" font-family="monospace">Raw DMA</text>

  <!-- TIER 2: eBPF / XDP LAYER -->
  <g transform="translate(265, 45)">
    <rect width="265" height="340" rx="8" fill="url(#bg-ebpf)" stroke="#0284c7" stroke-width="2"/>
    <text x="14" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">KERNEL DRIVER HOOK (XDP)</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">eBPF Native Driver Program</text>
    <text x="14" y="62" fill="#7dd3fc" font-size="10" font-family="monospace">Runs BEFORE Linux sk_buff allocation!</text>
    <text x="14" y="78" fill="#94a3b8" font-size="9" font-family="sans-serif">Saves 250ns allocation cost per packet</text>

    <!-- Branch A: XDP_DROP -->
    <g transform="translate(12, 90)">
      <rect width="240" height="60" rx="6" fill="#4c0519" stroke="#f43f5e" stroke-width="1.2"/>
      <text x="10" y="18" fill="#f43f5e" font-size="9" font-family="monospace" font-weight="bold">ACTION 1: XDP_DROP (DDoS Mitigation)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Drops malformed / flood packets in 18ns</text>
      <text x="10" y="48" fill="#fda4af" font-size="8" font-family="monospace">Sustains 100% line rate under 40M pps attack</text>
    </g>

    <!-- Branch B: XDP_TX -->
    <g transform="translate(12, 160)">
      <rect width="240" height="55" rx="6" fill="#042f2e" stroke="#10b981" stroke-width="1.2"/>
      <text x="10" y="18" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold">ACTION 2: XDP_TX (L4 Load Balancer)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Rewrites MAC &amp; bounces packet out same NIC</text>
      <text x="10" y="48" fill="#6ee7b7" font-size="8" font-family="monospace">Maglev hashing at line rate (sub-microsecond)</text>
    </g>

    <!-- Branch C: XDP_REDIRECT (AF_XDP) -->
    <g transform="translate(12, 225)">
      <rect width="240" height="95" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.2"/>
      <text x="10" y="18" fill="#a5b4fc" font-size="9" font-family="monospace" font-weight="bold">ACTION 3: XDP_REDIRECT (AF_XDP)</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Zero-Copy memory handoff to User Space</text>
      <text x="10" y="50" fill="#38bdf8" font-size="8" font-family="monospace">UMEM Memory Pool (Shared RingBuffer)</text>
      <text x="10" y="66" fill="#cbd5e1" font-size="8" font-family="sans-serif">Fill Queue + Rx Queue + Tx Queue + Completion Queue</text>
      <text x="10" y="84" fill="#10b981" font-size="8" font-family="monospace">Zero kernel context switches | Zero copies</text>
    </g>
  </g>

  <!-- Connectors Tier 2 -> Tier 3 -->
  <line x1="530" y1="270" x2="570" y2="210" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arr-sky)"/>
  <text x="532" y="235" fill="#a5b4fc" font-size="8" font-family="monospace">AF_XDP UMEM</text>

  <!-- TIER 3: USERSPACE KERNEL BYPASS -->
  <g transform="translate(570, 45)">
    <rect width="250" height="340" rx="8" fill="url(#bg-dpdk)" stroke="#818cf8" stroke-width="2"/>
    <text x="14" y="24" fill="#a5b4fc" font-size="10" font-family="monospace" font-weight="bold">POLL-MODE DRIVERS (PMD)</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">DPDK / io_uring Fastpath</text>
    <text x="14" y="62" fill="#c7d2fe" font-size="10" font-family="monospace">CPU Cores Pinned to NUMA Node 0</text>
    
    <g transform="translate(12, 75)">
      <rect width="225" height="70" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
      <text x="10" y="18" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">Core 0..3: 100% Polling Loop</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Eliminates hardware interrupt (IRQ) latency</text>
      <text x="10" y="50" fill="#a7f3d0" font-size="8" font-family="monospace">L1 Instruction Cache Warm (Zero Eviction)</text>
      <text x="10" y="64" fill="#cbd5e1" font-size="8" font-family="sans-serif">isolcpus=0-3 nohz_full=0-3 rcu_nocbs=0-3</text>
    </g>

    <g transform="translate(12, 155)">
      <rect width="225" height="75" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
      <text x="10" y="18" fill="#f59e0b" font-size="9" font-family="monospace" font-weight="bold">HugePages Memory Management</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">1 GB HugePages (vm.nr_hugepages = 64)</text>
      <text x="10" y="50" fill="#fde68a" font-size="8" font-family="monospace">TLB Misses reduced by 99.8%</text>
      <text x="10" y="66" fill="#cbd5e1" font-size="8" font-family="sans-serif">Direct DMA mapping for NIC hardware</text>
    </g>

    <g transform="translate(12, 240)">
      <rect width="225" height="85" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
      <text x="10" y="18" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold">Lock-Free RingBuffer Dispatch</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Single-Producer Single-Consumer (SPSC)</text>
      <text x="10" y="50" fill="#38bdf8" font-size="8" font-family="monospace">Atomic acquire/release memory semantics</text>
      <text x="10" y="66" fill="#10b981" font-size="8" font-family="monospace">Sub-nanosecond thread handoff</text>
      <text x="10" y="78" fill="#cbd5e1" font-size="8" font-family="sans-serif">Cacheline aligned (alignas(64))</text>
    </g>
  </g>

  <!-- Connectors Tier 3 -> Tier 4 -->
  <line x1="820" y1="210" x2="855" y2="210" stroke="#818cf8" stroke-width="2" marker-end="url(#arr-sky)"/>

  <!-- TIER 4: APPLICATION LAYER -->
  <g transform="translate(855, 50)">
    <rect width="180" height="330" rx="8" fill="url(#bg-dpdk)" stroke="#c084fc" stroke-width="1.8"/>
    <text x="12" y="24" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold">MICROSERVICE LAYER</text>
    <text x="12" y="44" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Protocol Dispatchers</text>
    
    <g transform="translate(8, 60)">
      <rect width="164" height="70" rx="6" fill="#1e1b4b" stroke="#c084fc" stroke-width="1"/>
      <text x="8" y="18" fill="#e9d5ff" font-size="9" font-family="monospace" font-weight="bold">Protobuf RPC</text>
      <text x="8" y="34" fill="#cbd5e1" font-size="8" font-family="sans-serif">FlatBuffers zero-parse</text>
      <text x="8" y="50" fill="#38bdf8" font-size="8" font-family="monospace">Zero Heap Copies</text>
      <text x="8" y="64" fill="#cbd5e1" font-size="8" font-family="sans-serif">Direct BytePointer read</text>
    </g>

    <g transform="translate(8, 140)">
      <rect width="164" height="70" rx="6" fill="#1e1b4b" stroke="#c084fc" stroke-width="1"/>
      <text x="8" y="18" fill="#e9d5ff" font-size="9" font-family="monospace" font-weight="bold">TCP BBR Engine</text>
      <text x="8" y="34" fill="#cbd5e1" font-size="8" font-family="sans-serif">Bottleneck Bandwidth</text>
      <text x="8" y="50" fill="#10b981" font-size="8" font-family="monospace">Zero Bufferbloat</text>
      <text x="8" y="64" fill="#cbd5e1" font-size="8" font-family="sans-serif">4.2x faster on lossy 5G</text>
    </g>

    <g transform="translate(8, 220)">
      <rect width="164" height="90" rx="6" fill="#1e1b4b" stroke="#c084fc" stroke-width="1"/>
      <text x="8" y="18" fill="#e9d5ff" font-size="9" font-family="monospace" font-weight="bold">Production SLAs</text>
      <text x="8" y="34" fill="#38bdf8" font-size="8" font-family="monospace">Packet Parse &lt; 850 ns</text>
      <text x="8" y="50" fill="#10b981" font-size="8" font-family="monospace">DDoS Drop &lt; 18 ns</text>
      <text x="8" y="66" fill="#f59e0b" font-size="8" font-family="monospace">0 Context Switches</text>
      <text x="8" y="80" fill="#a7f3d0" font-size="8" font-family="monospace">100% Line Rate Saturation</text>
    </g>
  </g>

  <!-- BOTTOM OBSERVABILITY BAR -->
  <g transform="translate(25, 400)">
    <rect width="1010" height="135" rx="8" fill="#030717" stroke="#334155" stroke-width="1.2"/>
    <text x="16" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">HARDWARE &amp; OS BENCHMARK COMPARISON (TRADITIONAL LINUX KERNEL VS XDP/DPDK BYPASS)</text>
    
    <g transform="translate(16, 38)" font-family="monospace" font-size="9">
      <rect width="978" height="80" rx="6" fill="#02040d" stroke="#1e293b" stroke-width="1"/>
      <text x="16" y="22" fill="#94a3b8">METRIC</text>
      <text x="240" y="22" fill="#f43f5e">STANDARD LINUX TCP/IP</text>
      <text x="560" y="22" fill="#10b981">eBPF / XDP + DPDK FASTPATH</text>
      <text x="860" y="22" fill="#00f0ff">STAFF GAIN</text>
      <line x1="16" y1="30" x2="962" y2="30" stroke="#1e293b" stroke-width="0.8"/>
      
      <text x="16" y="46" fill="#cbd5e1">Packet Ingress Limit:</text>
      <text x="240" y="46" fill="#f43f5e">1.8 Mpps (Drops 88% on 10GbE)</text>
      <text x="560" y="46" fill="#10b981">14.88 Mpps (100% Line Rate saturation)</text>
      <text x="860" y="46" fill="#00f0ff">8.2x Higher Throughput</text>

      <text x="16" y="62" fill="#cbd5e1">DDoS Drop Latency:</text>
      <text x="240" y="62" fill="#f43f5e">4,200 ns (Netfilter iptables walk)</text>
      <text x="560" y="62" fill="#10b981">18 ns (Driver XDP_DROP hook)</text>
      <text x="860" y="62" fill="#00f0ff">233x Lower Latency</text>

      <text x="16" y="76" fill="#cbd5e1">Kernel Context Switches:</text>
      <text x="240" y="76" fill="#f43f5e">4 Context Switches per transaction</text>
      <text x="560" y="76" fill="#10b981">0 Switches (Pinned NUMA Core Polling)</text>
      <text x="860" y="76" fill="#00f0ff">100% Elimination</text>
    </g>
  </g>
</svg>
"""
    }

    # If specific SVG exists, return it, otherwise generate a multi-tier enterprise diagram tailored to the module!
    if ch_id in svgs:
        return svgs[ch_id]

    # Generate rich, multi-tier enterprise architecture SVG for ch3..ch12
    return generate_generic_enterprise_svg(ch_id, title)


def generate_generic_enterprise_svg(ch_id, title):
    # Specialized tier descriptions for modules 3..12
    module_configs = {
        "ch3": {
            "track": "DISTRIBUTED CONCURRENCY & FENCING",
            "tier1": ("500 K8s Worker Pods", "Concurrent Mutation Requests", "Subject to 15s GC Pauses", "Loom Virtual Threads"),
            "tier2": ("Distributed Lock Master", "Redis Single-Shard / Lua", "Atomic INCR Token Counter", "SET resource UUID NX PX 10000"),
            "tier3": ("Monotonic Fencing Sentry", "Strictly Ordered 64-bit Integer", "Token Counter: #1049281", "Lease Watchdog Heartbeat (3.3s)"),
            "tier4": ("Storage Verification Barrier", "PostgreSQL / ScyllaDB Engine", "UPDATE cell SET val=?, token=?", "WHERE token > last_token (Rejects Stale Zombies)"),
            "invariants": ("Zero Stale Writes Under GC Pauses", "Linearizable State Transitions", "Sub-1.8ms Lock Grant Latency", "100% Zombie Rejection Rate")
        },
        "ch4": {
            "track": "DISTRIBUTED CONSENSUS & RAFT",
            "tier1": ("Proposal Client Fleet", "State Machine Put(key, val)", "Linearizable Read/Write SLA", "Retry with Exponential Backoff"),
            "tier2": ("Raft Leader (Term 2)", "WAL Log Append (Index 492)", "High Watermark CommitIndex", "Leader Heartbeats (100ms)"),
            "tier3": ("Follower Quorum Cluster", "Follower 1 (AZ-1) ✔ ACK", "Follower 2 (AZ-2) ✔ ACK", "Follower 3 (AZ-3) ✕ Partitioned"),
            "tier4": ("Replicated State Machine", "Linearizable Key-Value Store", "Point-in-Time Snapshot (50k WAL)", "State Machine Catch-up Engine"),
            "invariants": ("(N/2 + 1) Majority Quorum Required", "Linearizable Reads Without Leases", "Zero Split-Brain Under Any Partition", "Commit Latency p99 < 3.5ms")
        },
        "ch5": {
            "track": "BATCH MEDIATION & PROCESSING",
            "tier1": ("Raw S3 Data Lake", "2 GB Raw ASN.1 Dumps", "eCPRI Telecom CDR Streams", "Memory-Mapped FileChannel mmap"),
            "tier2": ("Virtual Thread Workers", "Java 21 Loom (1,000 Workers)", "Zero-Copy BytePointer Slicer", "Chunk Size = 2,500 records"),
            "tier3": ("DLQ Quarantine Sentry", "Invalid Schema Detector", "Kafka DLQ Topic (< 1.2ms)", "Zero Pipeline Halts"),
            "tier4": ("High-Throughput Sink", "ScyllaDB / PostgreSQL Sink", "JDBC executeBatch() (Commit=OFF)", "50,000 CDR/s Sustained Write"),
            "invariants": ("< 1.5 GB Heap Footprint for 50k CDR/s", "Zero Job Restarts on Corrupt Rows", "Zero JVM Heap Churn", "Idempotent Replay Guaranteed")
        },
        "ch6": {
            "track": "STREAM PROCESSING & FLINK CEP",
            "tier1": ("Kafka Event Stream", "45k TPS Ingestion Stream", "Event-Time Watermarks (5s)", "BoundedOutOfOrderness Generator"),
            "tier2": ("Flink Stream Processor", "KeyBy(tower_id) Partitioning", "10m Sliding Window (1m Slide)", "Off-Heap RocksDB State Backend"),
            "tier3": ("Checkpointing Barrier", "Chandy-Lamport Distributed Barrier", "Asynchronous NVMe Snapshot", "Incremental State Checkpoints (180ms)"),
            "tier4": ("Two-Phase Commit Sink", "Kafka 2PC / ScyllaDB Sink", "End-to-End Exactly-Once Guarantees", "Real-Time Anomaly Alarms < 100ms"),
            "invariants": ("Sub-100ms End-to-End Processing SLA", "Zero State Loss on Worker Crash", "Pure Off-Heap RocksDB (No GC)", "Deterministic Window Firing")
        },
        "ch7": {
            "track": "REAL-TIME TELECOM & 3GPP CTE",
            "tier1": ("Diameter CCR Stream", "CCR-Initial / CCR-Update", "Rating Group & MSISDN", "Low-Latency Ingress Gateway"),
            "tier2": ("Lock-Free Radix Tree", "Compiled 3GPP Tariff Tree", "Tenant -> Service -> Time DAG", "Atomic Pointer Swap root_.load()"),
            "tier3": ("Token Bucket Cluster", "In-Memory Redis Token Bucket", "Quota Reservation Deductions", "Sub-1.2ms Reservation Latency"),
            "tier4": ("Diameter CCA Generator", "Granted Service Units (GSU)", "Real-Time Billing Authorization", "Zero Database Roundtrips in Hot Path"),
            "invariants": ("Tariff Evaluation p99 < 1.2ms", "Zero Lock Contention on Read", "Atomic Tree Swap in 15ns", "Zero Quota Overdrafts")
        },
        "ch8": {
            "track": "5G CORE SBA & UPF FASTPATH",
            "tier1": ("gNodeB 5G Cell Base", "N3 Interface (GTP-U User Plane)", "N2 Interface (NGAP Control)", "Hardware Antenna Array"),
            "tier2": ("User Plane Function (UPF)", "DPDK Fastpath Forwarding", "N4 PFCP Session Enforcement", "Forwarding Latency < 50 µs"),
            "tier3": ("Service-Based Arch (SBA)", "HTTP/2 REST Microservices Mesh", "SMF (Session Management)", "PCF / CHF Policy & Charging"),
            "tier4": ("Subscriber Data & Auth", "UDM / UDR Subscriber Database", "Multi-AZ Active-Active Replicas", "99.999% Telecom Availability"),
            "invariants": ("User Plane Forwarding < 50 µs", "99.999% Five-Nines Availability", "SBA Control Latency < 8ms", "Canary Zero-Downtime Migration")
        },
        "ch9": {
            "track": "GLOBAL MULTI-REGION DATABASE",
            "tier1": ("Region US-East (DC1)", "ScyllaDB Ring (3 Replicas)", "LOCAL_QUORUM Writes (2/3)", "CommitLog NVMe O_DIRECT"),
            "tier2": ("Async Cross-DC Backbone", "Murmur3 Token Ring Partitioning", "Dedicated Private Cloud Fiber", "Replication Lag < 80ms"),
            "tier3": ("Region EU-Central (DC2)", "ScyllaDB Ring (3 Replicas)", "LOCAL_QUORUM Writes (2/3)", "Undersea Cable Cut Resilient!"),
            "tier4": ("LSM Compaction Engine", "Leveled Compaction Strategy", "Bloom Filter 1% False Positive", "Single-SSTable Point Reads"),
            "invariants": ("Local Write p99 < 3.8ms", "Zero Cross-DC Blocking on Write", "Write Amplification < 3.2x", "Transatlantic Outage Immune")
        },
        "ch10": {
            "track": "PLANET-SCALE DISTRIBUTED SQL",
            "tier1": ("Global ACID Transaction", "Cross-Region Bank Transfer", "US-East to EU-Central", "External Consistency Guarantee"),
            "tier2": ("TrueTime Hardware Engine", "Redundant GPS Receivers", "Rubidium Atomic Clocks", "Uncertainty Bound: ε < 7ms"),
            "tier3": ("Spanner Tablet Paxos", "Multi-Paxos Group Leaders", "Commit Wait Rule (2 * ε = 14ms)", "Monotonic Timestamp Allocation"),
            "tier4": ("Two-Phase Commit Sentry", "2PC over Paxos Groups", "Lock-Free Snapshot Reads", "Linearizable Across Planet Earth"),
            "invariants": ("Linearizable Physical Wall-Clock Ordering", "Lock-Free Consistent Read Snapshots", "Fail-Safe Clock Eviction on Drift", "Cross-Continent 2PC p99 < 120ms")
        },
        "ch11": {
            "track": "TRAFFIC SHAPING & RESILIENCE",
            "tier1": ("Burst API Ingress", "250,000 QPS Wire Spike", "Black Friday Flash Sale Surge", "Thundering Herd Threat"),
            "tier2": ("GCRA Rate Limiter", "Redis Single-Shard Lua Script", "Theoretical Arrival Time (TAT)", "Evaluation Latency < 0.4ms"),
            "tier3": ("Adaptive Concurrency", "TCP Vegas RTT Gradient Engine", "Dynamic In-Flight Pool Sizing", "Prevents Queue Buildup"),
            "tier4": ("Google Hedged Requests", "Duplicate Dispatch after p95 (12ms)", "First Response Wins / Cancel Pending", "p99.9 Tail Latency Cut by 65%"),
            "invariants": ("100% Fail-Open on Limiter Outage", "Zero Window-Boundary 2x Burst", "Adaptive Throttling Before OOM", "Hedged Request Overhead < 2%")
        },
        "ch12": {
            "track": "ZERO-DOWNTIME MIGRATIONS",
            "tier1": ("Phase 1: Dual Writes", "Synchronous Write: Oracle (Primary)", "Asynchronous Shadow: Kafka Topic", "Monotonic Record Versioning"),
            "tier2": ("Phase 2: Historical Backfill", "Apache Spark Partitioned Reader", "500M Records Streamed at 85k/s", "Zero Impact on Production DB"),
            "tier3": ("Phase 3: Dark Replay & Audit", "Continuous Parity Reconciler", "14 Days Live Dark Traffic Replay", "100.000% Verified Data Parity"),
            "tier4": ("Phase 4: Instant Cutover", "1-Second DNS / Envoy Swap", "ScyllaDB Promoted to Primary", "30-Day Reverse Replay for 1s Rollback"),
            "invariants": ("Exactly 0 Seconds Customer Downtime", "100.000% Proven Data Parity", "Instant 1-Second Rollback Safety", "Zero Lost Updates Under Concurrency")
        }
    }

    cfg = module_configs.get(ch_id, module_configs["ch3"])

    return f"""
<svg viewBox="0 0 1060 560" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl bg-[#020512] border border-cyan-900/60 p-3 shadow-2xl">
  <defs>
    <linearGradient id="bg-t1-{ch_id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#082f49" stop-opacity="0.95"/><stop offset="100%" stop-color="#0369a1" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-t2-{ch_id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0e3a5a" stop-opacity="0.95"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/></linearGradient>
    <linearGradient id="bg-t3-{ch_id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#064e3b" stop-opacity="0.95"/><stop offset="100%" stop-color="#042f2e" stop-opacity="0.4"/></linearGradient>
    <linearGradient id="bg-t4-{ch_id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3b0764" stop-opacity="0.95"/><stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.4"/></linearGradient>
    <marker id="arr-{ch_id}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#00f0ff"/></marker>
  </defs>

  <pattern id="grid-pattern-{ch_id}" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.5" stroke-opacity="0.3"/>
  </pattern>
  <rect width="100%" height="100%" fill="url(#grid-pattern-{ch_id})" rx="8"/>

  <!-- TIER HEADERS -->
  <g font-family="monospace" font-size="9" font-weight="bold" fill="#64748b" letter-spacing="1">
    <text x="30" y="24">TIER 1: INGRESS &amp; CLIENTS</text>
    <text x="280" y="24">TIER 2: COORDINATION &amp; LOGIC</text>
    <text x="540" y="24">TIER 3: CORE CONSENSUS &amp; KERNEL</text>
    <text x="800" y="24">TIER 4: STORAGE &amp; VERIFICATION</text>
  </g>
  <line x1="20" y1="32" x2="1040" y2="32" stroke="#1e293b" stroke-width="1"/>

  <!-- TIER 1 -->
  <g transform="translate(25, 50)">
    <rect width="220" height="330" rx="8" fill="url(#bg-t1-{ch_id})" stroke="#0284c7" stroke-width="1.8"/>
    <text x="14" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">INGRESS &amp; CLIENTS</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">{cfg["tier1"][0]}</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier1"][1]}</text>
    <text x="14" y="84" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier1"][2]}</text>
    <text x="14" y="102" fill="#00f0ff" font-size="9" font-family="monospace">• {cfg["tier1"][3]}</text>
    <g transform="translate(10, 130)">
      <rect width="200" height="90" rx="6" fill="#041a2e" stroke="#0284c7" stroke-width="1"/>
      <text x="10" y="18" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">Network Boundary</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">mTLS 1.3 Encryption</text>
      <text x="10" y="48" fill="#cbd5e1" font-size="9" font-family="sans-serif">HTTP/2 Multiplexed Streams</text>
      <text x="10" y="64" fill="#10b981" font-size="8" font-family="monospace">Zero-Copy DMA Buffer</text>
      <text x="10" y="78" fill="#cbd5e1" font-size="8" font-family="sans-serif">TCP BBR Congestion Control</text>
    </g>
    <g transform="translate(10, 235)">
      <rect width="200" height="75" rx="6" fill="#041a2e" stroke="#0284c7" stroke-width="1"/>
      <text x="10" y="18" fill="#a7f3d0" font-size="9" font-family="monospace" font-weight="bold">Availability Target</text>
      <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">99.999% Service Level</text>
      <text x="10" y="50" fill="#38bdf8" font-size="8" font-family="monospace">p99 Wire Latency &lt; 5ms</text>
      <text x="10" y="64" fill="#94a3b8" font-size="8" font-family="sans-serif">Multi-Zone Redundancy</text>
    </g>
  </g>

  <!-- Connector Tier 1 -> Tier 2 -->
  <line x1="245" y1="200" x2="280" y2="200" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-{ch_id})"/>

  <!-- TIER 2 -->
  <g transform="translate(280, 50)">
    <rect width="230" height="330" rx="8" fill="url(#bg-t2-{ch_id})" stroke="#00f0ff" stroke-width="1.8"/>
    <text x="14" y="24" fill="#00f0ff" font-size="10" font-family="monospace" font-weight="bold">COORDINATION &amp; LOGIC</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">{cfg["tier2"][0]}</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier2"][1]}</text>
    <text x="14" y="84" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier2"][2]}</text>
    <text x="14" y="102" fill="#38bdf8" font-size="9" font-family="monospace">• {cfg["tier2"][3]}</text>
    <g transform="translate(10, 130)">
      <rect width="210" height="90" rx="6" fill="#062238" stroke="#00f0ff" stroke-width="1"/>
      <text x="10" y="18" fill="#00f0ff" font-size="9" font-family="monospace" font-weight="bold">Distributed State Engine</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Atomic Single-Shard Operations</text>
      <text x="10" y="48" fill="#cbd5e1" font-size="9" font-family="sans-serif">In-Memory Redis / Lua Sentry</text>
      <text x="10" y="64" fill="#10b981" font-size="8" font-family="monospace">Execution Latency &lt; 1.2ms</text>
      <text x="10" y="78" fill="#cbd5e1" font-size="8" font-family="sans-serif">Zero Lock Contention</text>
    </g>
    <g transform="translate(10, 235)">
      <rect width="210" height="75" rx="6" fill="#062238" stroke="#00f0ff" stroke-width="1"/>
      <text x="10" y="18" fill="#f59e0b" font-size="9" font-family="monospace" font-weight="bold">Partition Ring</text>
      <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Consistent Hashing</text>
      <text x="10" y="50" fill="#fde68a" font-size="8" font-family="monospace">Virtual Nodes: 150 V-Nodes</text>
      <text x="10" y="64" fill="#94a3b8" font-size="8" font-family="sans-serif">Minimizes Rehash Churn</text>
    </g>
  </g>

  <!-- Connector Tier 2 -> Tier 3 -->
  <line x1="510" y1="200" x2="540" y2="200" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-{ch_id})"/>

  <!-- TIER 3 -->
  <g transform="translate(540, 50)">
    <rect width="235" height="330" rx="8" fill="url(#bg-t3-{ch_id})" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="24" fill="#10b981" font-size="10" font-family="monospace" font-weight="bold">CONSENSUS &amp; PROCESSING</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">{cfg["tier3"][0]}</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier3"][1]}</text>
    <text x="14" y="84" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier3"][2]}</text>
    <text x="14" y="102" fill="#a7f3d0" font-size="9" font-family="monospace">• {cfg["tier3"][3]}</text>
    <g transform="translate(10, 130)">
      <rect width="215" height="90" rx="6" fill="#042f2e" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold">Quorum &amp; Log Replication</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Synchronous Cross-AZ Commits</text>
      <text x="10" y="48" fill="#cbd5e1" font-size="9" font-family="sans-serif">AppendEntries Heartbeats</text>
      <text x="10" y="64" fill="#38bdf8" font-size="8" font-family="monospace">CommitIndex High Watermark</text>
      <text x="10" y="78" fill="#a7f3d0" font-size="8" font-family="sans-serif">Tolerates (N/2) Node Failures</text>
    </g>
    <g transform="translate(10, 235)">
      <rect width="215" height="75" rx="6" fill="#042f2e" stroke="#10b981" stroke-width="1"/>
      <text x="10" y="18" fill="#6ee7b7" font-size="9" font-family="monospace" font-weight="bold">Off-Heap Storage</text>
      <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">RocksDB / MemTable</text>
      <text x="10" y="50" fill="#a7f3d0" font-size="8" font-family="monospace">Zero GC Stop-The-World Pauses</text>
      <text x="10" y="64" fill="#94a3b8" font-size="8" font-family="sans-serif">Local NVMe Write-Ahead Log</text>
    </g>
  </g>

  <!-- Connector Tier 3 -> Tier 4 -->
  <line x1="775" y1="200" x2="805" y2="200" stroke="#00f0ff" stroke-width="2" marker-end="url(#arr-{ch_id})"/>

  <!-- TIER 4 -->
  <g transform="translate(805, 50)">
    <rect width="230" height="330" rx="8" fill="url(#bg-t4-{ch_id})" stroke="#c084fc" stroke-width="1.8"/>
    <text x="14" y="24" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">PERSISTENCE &amp; REPLICATION</text>
    <text x="14" y="44" fill="#ffffff" font-size="13" font-family="sans-serif" font-weight="bold">{cfg["tier4"][0]}</text>
    <text x="14" y="66" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier4"][1]}</text>
    <text x="14" y="84" fill="#cbd5e1" font-size="10" font-family="sans-serif">• {cfg["tier4"][2]}</text>
    <text x="14" y="102" fill="#e9d5ff" font-size="9" font-family="monospace">• {cfg["tier4"][3]}</text>
    <g transform="translate(10, 130)">
      <rect width="210" height="90" rx="6" fill="#1e1b4b" stroke="#c084fc" stroke-width="1"/>
      <text x="10" y="18" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold">Verification Barrier</text>
      <text x="10" y="34" fill="#cbd5e1" font-size="9" font-family="sans-serif">Monotonic Version Check</text>
      <text x="10" y="48" fill="#cbd5e1" font-size="9" font-family="sans-serif">Conditional Commit Engine</text>
      <text x="10" y="64" fill="#f43f5e" font-size="8" font-family="monospace">Rejects 100% of Zombie Writes</text>
      <text x="10" y="78" fill="#a7f3d0" font-size="8" font-family="sans-serif">Linearizable Consistency</text>
    </g>
    <g transform="translate(10, 235)">
      <rect width="210" height="75" rx="6" fill="#1e1b4b" stroke="#c084fc" stroke-width="1"/>
      <text x="10" y="18" fill="#f59e0b" font-size="9" font-family="monospace" font-weight="bold">Compaction &amp; Archive</text>
      <text x="10" y="34" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Leveled Compaction</text>
      <text x="10" y="50" fill="#fde68a" font-size="8" font-family="monospace">Bloom Filter False-Pos &lt; 1%</text>
      <text x="10" y="64" fill="#94a3b8" font-size="8" font-family="sans-serif">Cold Parquet to S3 Glacier</text>
    </g>
  </g>

  <!-- BOTTOM OBSERVABILITY & INVARIANTS -->
  <g transform="translate(25, 400)">
    <rect width="1010" height="135" rx="8" fill="#030717" stroke="#334155" stroke-width="1.2"/>
    <text x="16" y="24" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">GOOGLE STAFF L6 ARCHITECTURAL INVARIANTS &amp; PHYSICAL BOUNDARIES</text>
    
    <g transform="translate(16, 38)" font-family="monospace" font-size="9">
      <rect width="978" height="80" rx="6" fill="#02040d" stroke="#1e293b" stroke-width="1"/>
      <text x="16" y="22" fill="#94a3b8">ARCHITECTURAL LAW</text>
      <text x="280" y="22" fill="#00f0ff">GUARANTEE &amp; BOUNDARY</text>
      <text x="640" y="22" fill="#10b981">FAILURE MODE ISOLATION</text>
      <line x1="16" y1="30" x2="962" y2="30" stroke="#1e293b" stroke-width="0.8"/>
      
      <text x="16" y="46" fill="#cbd5e1">1. {cfg["invariants"][0]}</text>
      <text x="280" y="46" fill="#00f0ff">Mathematical Proof (Monotonic token or Raft high watermark)</text>
      <text x="640" y="46" fill="#10b981">Zero split-brain under arbitrary net splits</text>

      <text x="16" y="62" fill="#cbd5e1">2. {cfg["invariants"][1]}</text>
      <text x="280" y="62" fill="#00f0ff">Sequential consistency with real wall-clock physical alignment</text>
      <text x="640" y="62" fill="#10b981">Tolerates delayed or replayed RPC packets</text>

      <text x="16" y="76" fill="#cbd5e1">3. {cfg["invariants"][2]}</text>
      <text x="280" y="76" fill="#00f0ff">p99 &lt; SLA bounded by local memory/NVMe execution</text>
      <text x="640" y="76" fill="#10b981">{cfg["invariants"][3]}</text>
    </g>
  </g>
</svg>
"""
