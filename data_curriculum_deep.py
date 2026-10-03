# data_curriculum_deep.py
# Deep, exhaustive, textbook-grade curriculum for Tier 0 through Tier 5

TIERS = [
    {
        "id": "tier-0",
        "num": "TIER 00",
        "title": "Hardware Physics & The Machine Underneath",
        "tagline": "How transistors, CPU caches, memory buses, and NVMe drives dictate distributed systems performance.",
        "badge": "Hardware & Physics",
        "color": "emerald",
        "chapters": [
            {
                "id": "ch-01-hardware-physics",
                "title": "01. CPU Microarchitecture, Memory Hierarchy & The Latency Gap",
                "difficulty": "Foundational Physics",
                "readTime": "20 min read",
                "summary": "Cache lines (64 bytes), L1/L2/L3 caches, NUMA architectures, False Sharing, memory bandwidth ceilings, and mechanical NVMe physics.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/20">
    <div class="flex items-center gap-2 text-emerald-400 font-mono text-xs font-bold uppercase tracking-wider mb-2">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> First Principles Principle
    </div>
    <p class="text-slate-200">
      Software does not execute in the cloud; it executes on silicon chips subject to thermodynamic limits, speed-of-light propagation delays in copper and fiber, and memory bus bandwidth saturation. A Staff Architect who understands CPU cache lines and NUMA topology designs systems that are 100&times; faster and 10&times; cheaper than one who treats the computer as an abstract Turing machine.
    </p>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-emerald-400"></span> 1. The Von Neumann Bottleneck & Memory Hierarchy
  </h4>
  <p>
    Modern CPUs execute multiple instructions per cycle (IPC &gt; 3) at clock speeds exceeding 3.5 GHz (1 cycle &approx; 0.28 nanoseconds). However, fetching a single byte from main memory (DRAM) requires ~100 nanoseconds—a delay of over <strong>350 CPU cycles</strong> where execution units sit completely idle (a "memory stall").
  </p>
  
  <div class="overflow-hidden rounded-xl border border-slate-800 bg-slate-950">
    <table class="w-full text-xs text-left border-collapse">
      <thead>
        <tr class="bg-slate-900/80 text-slate-400 border-b border-slate-800 font-mono">
          <th class="p-3">Level</th>
          <th class="p-3">Capacity</th>
          <th class="p-3">Latency (Cycles)</th>
          <th class="p-3">Latency (Time)</th>
          <th class="p-3">Bandwidth</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 font-mono text-slate-300">
        <tr>
          <td class="p-3 font-bold text-emerald-400">L1 Data Cache</td>
          <td class="p-3">32 - 48 KB / core</td>
          <td class="p-3">4 - 5 cycles</td>
          <td class="p-3">~1.0 ns</td>
          <td class="p-3 text-cyan-400">~2,000 GB/s</td>
        </tr>
        <tr>
          <td class="p-3 font-bold text-emerald-400">L2 Unified Cache</td>
          <td class="p-3">512 KB - 1.25 MB / core</td>
          <td class="p-3">12 - 14 cycles</td>
          <td class="p-3">~3.5 ns</td>
          <td class="p-3 text-cyan-400">~1,000 GB/s</td>
        </tr>
        <tr>
          <td class="p-3 font-bold text-cyan-400">L3 Shared Cache</td>
          <td class="p-3">32 - 96 MB / socket</td>
          <td class="p-3">40 - 60 cycles</td>
          <td class="p-3">~12 - 18 ns</td>
          <td class="p-3 text-cyan-400">~400 GB/s</td>
        </tr>
        <tr>
          <td class="p-3 font-bold text-amber-400">Main Memory (DDR5)</td>
          <td class="p-3">64 GB - 2 TB</td>
          <td class="p-3">200 - 350 cycles</td>
          <td class="p-3">~60 - 100 ns</td>
          <td class="p-3 text-amber-400">~50 - 100 GB/s</td>
        </tr>
        <tr>
          <td class="p-3 font-bold text-rose-400">NVMe SSD (PCIe 4.0)</td>
          <td class="p-3">1 - 30 TB</td>
          <td class="p-3">35,000 - 100,000 cycles</td>
          <td class="p-3">~10 - 30 &mu;s</td>
          <td class="p-3 text-rose-400">~7 GB/s</td>
        </tr>
        <tr>
          <td class="p-3 font-bold text-rose-500">Cross-Datacenter WAN</td>
          <td class="p-3">&infin;</td>
          <td class="p-3">150,000,000 cycles</td>
          <td class="p-3">~50 - 150 ms</td>
          <td class="p-3 text-rose-500">1 - 100 Gbps</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-1.5 h-4 rounded-full bg-emerald-400"></span> 2. Cache Lines & The False Sharing Trap
  </h4>
  <p>
    CPUs never read single bytes from RAM. All memory transfers occur in fixed chunks of <strong>64 bytes</strong> called a <strong>Cache Line</strong>.
  </p>
  <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
    <div class="text-xs font-mono font-bold text-rose-400">THE CONCURRENCY BUG: FALSE SHARING</div>
    <p class="text-xs text-slate-300">
      If Thread 1 on Core 0 modifies variable <code>A</code>, and Thread 2 on Core 1 modifies variable <code>B</code>, but both variables happen to reside within the same 64-byte memory slice, the CPU's cache coherence protocol (MESI/MOESI) forces Core 0 and Core 1 to constantly invalidate each other's L1/L2 caches. Throughput collapses by up to <strong>95%</strong>, despite zero logical locks!
    </p>
    <div class="p-2.5 rounded-lg bg-slate-950 font-mono text-xs text-emerald-400 border border-slate-800">
      // Production Fix in Go / Java / C++: Cache line padding<br/>
      type WorkerCounter struct {<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;count uint64<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;_pad  [56]byte // Pads struct to 64 bytes, preventing cross-core cache invalidation<br/>
      }
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-1.5 h-4 rounded-full bg-emerald-400"></span> 3. NUMA (Non-Uniform Memory Access) in High-Core Servers
  </h4>
  <p>
    Enterprise servers (e.g. AWS <code>c6i.32xlarge</code> or dual-socket AMD EPYC servers) feature 64 to 128 cores divided across multiple physical CPU sockets. Memory attached to Socket 0 is <strong>Local</strong> to Core 0 (60ns latency), but <strong>Remote</strong> to Core 64 on Socket 1 (130ns latency across the Infinity Fabric / UPI interconnect).
  </p>
  <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-300">
    <strong>Production Architecture Rule:</strong> High-performance distributed databases (ScyllaDB, Aerospike) pin worker threads to dedicated CPU cores and bind their memory allocations strictly to local NUMA nodes (<code>numactl --interleave</code> or thread-per-core architecture), eliminating cross-socket bus contention.
  </div>
</div>
"""
            },
            {
                "id": "ch-02-networking-kernel",
                "title": "02. Linux Kernel I/O, Syscalls, eBPF & Kernel Bypass (DPDK/io_uring)",
                "difficulty": "Staff Level Deep Dive",
                "readTime": "22 min read",
                "summary": "Context switching costs, interrupt handling, Epoll vs io_uring, Linux zero-copy (sendfile), eBPF networking, and DPDK kernel bypass.",
                "readTime": "24 min read",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-5 rounded-2xl bg-slate-900 border border-cyan-500/20">
    <p class="text-slate-200">
      At 10,000 requests per second, traditional socket I/O works fine. At <strong>1,000,000 packets per second (Mpps)</strong>, the Linux kernel itself becomes the bottleneck. Every hardware interrupt, system call context switch, and buffer copy burns valuable CPU cycles.
    </p>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-cyan-400"></span> 1. The Anatomy of an I/O System Call & Context Switch
  </h4>
  <p>
    When your application calls <code>read(socket_fd, buf, len)</code>, the CPU transitions from User Mode (Ring 3) to Kernel Mode (Ring 0):
  </p>
  <ol class="list-decimal list-inside space-y-2 text-xs text-slate-300 ml-2">
    <li><strong>Registers Stored:</strong> CPU register state (RIP, RSP, general registers) is saved to the thread's kernel stack.</li>
    <li><strong>Page Table Switch:</strong> The MMU updates Translation Lookaside Buffer (TLB) mappings.</li>
    <li><strong>Data Copy:</strong> The kernel copies bytes from the socket's kernel receive buffer (sk_buff) to your user-space memory buffer.</li>
    <li><strong>Ring Transition:</strong> CPU transitions back to Ring 3. Cost: ~1,500 to 2,000 CPU cycles per syscall!</li>
  </ol>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-1.5 h-4 rounded-full bg-cyan-400"></span> 2. The Evolution of High-Performance Linux I/O
  </h4>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
    <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
      <div class="text-xs font-mono font-bold text-amber-400 mb-1">EPOLL (Level/Edge)</div>
      <p class="text-xs text-slate-400 mb-2">Used by Nginx, Redis, Netty, Node.js</p>
      <div class="text-xs text-slate-300 space-y-1">
        <div>&bull; $O(1)$ event notifications via red-black tree and ready-list.</div>
        <div>&bull; Still requires 1 syscall to poll (<code>epoll_wait</code>) and 1 syscall per read/write.</div>
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-950 border border-cyan-800/40 bg-cyan-950/10">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">IO_URING (Jens Axboe)</div>
      <p class="text-xs text-slate-400 mb-2">Modern Linux 5.1+ Standard</p>
      <div class="text-xs text-slate-300 space-y-1">
        <div>&bull; Two lockless ring buffers shared between kernel and user space.</div>
        <div>&bull; Submit 1,000 I/O operations with <strong>zero syscalls</strong> using kernel polling mode (<code>IORING_SETUP_SQPOLL</code>).</div>
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-950 border border-emerald-800/40 bg-emerald-950/10">
      <div class="text-xs font-mono font-bold text-emerald-400 mb-1">DPDK & eBPF (Bypass)</div>
      <p class="text-xs text-slate-400 mb-2">Cloudflare, Cloud Providers</p>
      <div class="text-xs text-slate-300 space-y-1">
        <div>&bull; <strong>eBPF XDP:</strong> Inspects and drops/routes packets directly in network driver before OS kernel allocates sk_buff.</div>
        <div>&bull; <strong>DPDK:</strong> Unbinds NIC from OS kernel completely. User-space polls NIC queues directly via DMA.</div>
      </div>
    </div>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "tier-1",
        "num": "TIER 01",
        "title": "Protocols, Networking & Traffic Management",
        "tagline": "How bits travel over the wire: BGP Anycast, TCP congestion mechanics, TLS 1.3, and HTTP/3.",
        "badge": "Networking & Edge",
        "color": "cyan",
        "chapters": [
            {
                "id": "ch-03-dns-bgp-anycast",
                "title": "03. Anycast BGP Routing, GeoDNS & Global Traffic Ingestion",
                "difficulty": "Senior to Staff",
                "readTime": "18 min read",
                "summary": "How Cloudflare and AWS route packets to the nearest edge PoP using BGP Anycast, GeoDNS steering, and Edge TLS termination.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-cyan-400"></span> Unicast vs Anycast DNS: How the Internet Routes
  </h4>
  <p>
    In standard <strong>Unicast</strong> routing, an IP address (e.g., <code>198.51.100.1</code>) belongs to exactly one physical server in one datacenter. If a user in Singapore sends a packet to a Unicast IP in Virginia, the packet travels halfway across the globe (~200ms latency).
  </p>
  <p>
    In <strong>Anycast BGP</strong> routing, hundreds of datacenters across the world advertise the <em>exact same IP address</em> into the global BGP routing table. The user's local ISP routes packets to whichever datacenter is topologically closest (lowest autonomous system hop count).
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-amber-400 mb-1">GEODNS (Layer 7 Routing)</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>DNS nameserver inspects the client's recursive resolver IP (or EDNS Client Subnet).</li>
        <li>Returns different IP addresses based on country/continent.</li>
        <li><strong>Limitation:</strong> ISP DNS caching (TTL) delays failover by minutes or hours if a region crashes.</li>
      </ul>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-cyan-800/40 bg-cyan-950/10">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">BGP ANYCAST (Layer 3 Routing)</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>Single IP address announced globally via BGP Autonomous Systems.</li>
        <li>Zero DNS TTL dependency: routers automatically reroute around failed PoPs in seconds.</li>
        <li>DDoS attacks are geographically fragmented and absorbed by local edge nodes without taking down the core.</li>
      </ul>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "ch-04-tcp-quic-http3",
                "title": "04. Transport Protocols: TCP Slow Start, BBR vs Cubic & HTTP/3 QUIC",
                "difficulty": "Staff Level",
                "readTime": "22 min read",
                "summary": "Congestion windows (CWND), TCP Head-of-Line blocking, Google BBR bottleneck bandwidth algorithm, and UDP-based QUIC connection migration.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-cyan-400"></span> The Fundamental Flaw of TCP: Head-of-Line (HoL) Blocking
  </h4>
  <p>
    TCP provides an abstraction of an ordered, reliable byte stream. To guarantee ordering, TCP buffers incoming packets. If packet #3 drops due to Wi-Fi interference, but packets #4, #5, and #6 arrive safely, the operating system <strong>refuses to deliver #4, #5, and #6 to application user space</strong> until packet #3 is retransmitted and acknowledged.
  </p>
  <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
    <div class="text-xs font-mono font-bold text-emerald-400 mb-1">HOW HTTP/3 QUIC ELIMINATES HOL BLOCKING</div>
    <p class="text-xs text-slate-300 leading-relaxed">
      HTTP/3 operates over <strong>QUIC (UDP)</strong>. QUIC introduces independent cryptographic streams inside a single UDP connection. If packet #3 (belonging to Stream A, an image file) drops, Stream B (CSS file) continues processing without a single millisecond of delay!
    </p>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "tier-2",
        "num": "TIER 02",
        "title": "Core Scalability & Caching Architectures",
        "tagline": "Consistent hashing rings, L4/L7 load balancers, multi-tier caching hierarchies, and stampede defenses.",
        "badge": "Scalability & Caching",
        "color": "indigo",
        "chapters": [
            {
                "id": "ch-05-load-balancers-maglev",
                "title": "05. Layer 4 vs Layer 7 Load Balancing: Google Maglev & Envoy Internal Routing",
                "difficulty": "Staff Level Deep Dive",
                "readTime": "24 min read",
                "summary": "Direct Server Return (DSR), Maglev consistent hashing lookup tables, connection tracking tables, and Envoy service mesh routing.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-indigo-400"></span> Direct Server Return (DSR): Scaling to Terabits per Second
  </h4>
  <p>
    In traditional proxy load balancing, all incoming requests AND outgoing responses pass through the load balancer. But web traffic is inherently asymmetric: an HTTP GET request is ~500 bytes, while the response (image, video, JSON payload) is often 500 KB to 5 MB—a <strong>1,000&times; asymmetry</strong>!
  </p>
  <p>
    Under <strong>Direct Server Return (DSR)</strong>, the Layer 4 load balancer inspects the inbound packet, rewrites the destination MAC address to the chosen backend server, and forwards it. The backend server processes the request and <strong>replies directly to the client browser</strong> over the internet, completely bypassing the load balancer! This allows a cluster of L4 boxes to serve 100+ Gbps of egress traffic.
  </p>
</div>
"""
            },
            {
                "id": "ch-06-caching-xfetch-bloom",
                "title": "06. Advanced Caching: Invalidation, Cache Stampede (XFetch) & Multi-Tier Topology",
                "difficulty": "Staff Level Deep Dive",
                "readTime": "22 min read",
                "summary": "Probabilistic early expiration (XFetch mathematical proof), Bloom Filters for cache penetration, Jittered TTLs, and L1 Caffeine + L2 Redis architectures.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-slate-900 border border-indigo-800/40">
    <div class="text-xs font-mono font-bold text-indigo-400 mb-1">THE MATHEMATICS OF XFETCH (PROBABILISTIC EARLY EXPIRATION)</div>
    <p class="text-xs text-slate-300 leading-relaxed mb-3">
      Instead of waiting for a hot key to expire and suffering a 50,000-request DB stampede, the client probabilistically computes whether it should recompute the cache early on read:
    </p>
    <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800 text-center">
      &minus;&beta; &times; &delta; &times; ln(rand()) &gt; (expiry &minus; now)
    </div>
    <div class="text-[11px] text-slate-400 mt-2 space-y-1">
      <div>&bull; <code>&delta;</code>: Duration taken to compute the value from the database (e.g. 50ms).</div>
      <div>&bull; <code>&beta;</code>: Aggressiveness coefficient (&gt; 0, typically set to 1.0).</div>
      <div>&bull; <code>rand()</code>: Uniform random number between 0 and 1.</div>
    </div>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "tier-3",
        "num": "TIER 03",
        "title": "Storage Engines & Data Systems Internals",
        "tagline": "Under the hood of relational and NoSQL databases: B+ Trees, LSM-Trees, WAL, and partitioning keys.",
        "badge": "Storage Engines",
        "color": "fuchsia",
        "chapters": [
            {
                "id": "ch-07-bplus-vs-lsm",
                "title": "07. Storage Engine Internals: B+ Trees vs LSM-Trees (RocksDB / Cassandra)",
                "difficulty": "Principal Level",
                "readTime": "26 min read",
                "summary": "Disk page layouts, write amplification factor (WAF), SSTable bloom filters, leveled vs size-tiered compaction, and WiscKey KV separation.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <p>
    Every database in production uses one of two foundational storage philosophies: <strong>B+ Trees</strong> (in-place updates on fixed-size pages) or <strong>LSM-Trees</strong> (append-only log-structured merge trees). Choosing the wrong engine causes 10&times; write amplification and disk burnout.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">B+ TREE (PostgreSQL / MySQL InnoDB)</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>Optimized for $O(\\log N)$ point queries and sequential range scans.</li>
        <li>Random I/O on writes: Modifying 1 row requires rewriting the entire 8KB/16KB page to disk.</li>
        <li>Requires Doublewrite Buffers to prevent torn pages on power failure.</li>
      </ul>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-fuchsia-400 mb-1">LSM-TREE (RocksDB / Cassandra / ScyllaDB)</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>Optimized for maximum write throughput: appends to WAL + in-memory MemTable (SkipList).</li>
        <li>Flushed sequentially to immutable Sorted String Tables (SSTables).</li>
        <li>Reads check MemTable &rarr; Bloom Filter &rarr; SSTable index. Background compaction merges runs.</li>
      </ul>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "ch-08-sharding-keys",
                "title": "08. Sharding Architecture, Hot Partition Mitigation & Global Secondary Indexes",
                "difficulty": "Staff Level",
                "readTime": "20 min read",
                "summary": "Selecting shard keys, compound keys, salted hash keys for celebrity traffic, cross-shard 2PC avoidance, and change data capture (CDC).",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-fuchsia-400"></span> The Celebrity Hot Shard Disaster & The Salted Key Solution
  </h4>
  <p>
    If you shard by <code>user_id</code>, what happens when a celebrity with 100M followers posts an update? All likes, comments, and reads route to a single database shard, pegging its CPU at 100% while other shards sit idle.
  </p>
  <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
    <div class="text-xs font-mono font-bold text-emerald-400">PRODUCTION FIX: SALTED PARTITION KEYS</div>
    <p class="text-xs text-slate-300 leading-relaxed">
      For high-traffic entities, append a random salt suffix to the partition key on write: <code>partition_key = post_id + "_" + rand(0, 10)</code>. Writes distribute evenly across 10 distinct physical shards! On read, the query orchestrator scatters parallel queries across the 10 shards and aggregates counts in memory in &lt;10ms.
    </p>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "tier-4",
        "num": "TIER 04",
        "title": "Distributed Systems Theory & Consensus",
        "tagline": "PACELC, Strict Serializability, Raft in complete detail, Paxos, and Martin Kleppmann's fencing tokens.",
        "badge": "Consensus & Theory",
        "color": "amber",
        "chapters": [
            {
                "id": "ch-09-raft-consensus-deep",
                "title": "09. Distributed Consensus: Raft Protocol Deconstructed Step-by-Step",
                "difficulty": "Principal Level",
                "readTime": "28 min read",
                "summary": "Leader election safety, term numbers, log matching property, joint consensus configuration changes, and KRaft in Apache Kafka.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-amber-400"></span> The 3 Pillars of Raft Consensus
  </h4>
  <p>
    Raft decomposes consensus into three independent, provable sub-problems:
  </p>
  <div class="space-y-3">
    <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-amber-400 mb-1">1. LEADER ELECTION (Randomized Heartbeat Timeouts)</div>
      <p class="text-xs text-slate-300">Heartbeat intervals (e.g. 50ms) vs randomized election timeouts (150ms-300ms). Randomization prevents split-vote deadlocks when multiple candidates stand simultaneously.</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">2. LOG REPLICATION & QUORUM COMMITS</div>
      <p class="text-xs text-slate-300">Leader writes to its own log, sends <code>AppendEntries</code> RPCs. Once $N/2 + 1$ nodes persist the entry to disk, the leader increments <code>commitIndex</code> and replies to the client.</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-emerald-400 mb-1">3. ELECTION SAFETY INVARIANT</div>
      <p class="text-xs text-slate-300">A follower will vote NO if the candidate's log is less up-to-date than its own: <code>(cand_term, cand_index) &lt; (my_term, my_index)</code>. This guarantees that any elected leader already possesses all committed log entries from prior terms.</p>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "ch-10-fencing-tokens-locks",
                "title": "10. Distributed Concurrency: Fencing Tokens vs Redlock Clock Assumptions",
                "difficulty": "Staff Level",
                "readTime": "20 min read",
                "summary": "Why Redis Redlock is fundamentally unsafe without monotonic tokens, GC pause hazards, and building linearizable locks with etcd/ZooKeeper.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-slate-900 border border-amber-900/50">
    <div class="text-xs font-mono font-bold text-amber-400 mb-1">THE FENCING TOKEN PATTERN (KLEPPMANN'S PROOF)</div>
    <p class="text-xs text-slate-300 leading-relaxed">
      A lock service must generate a strictly increasing 64-bit integer token (e.g. <code>token=102</code>). When Client 1 writes to storage, it passes <code>token=102</code>. If Client 1 freezes for 30s during a GC pause and Client 2 obtains the lock with <code>token=103</code>, the storage engine rejects any subsequent write from Client 1 because $102 &lt; 103$. Lock safety is enforced at the storage boundary!
    </p>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "tier-5",
        "num": "TIER 05",
        "title": "Reliability, Resilience & Observability at Scale",
        "tagline": "Circuit breakers, rate limiters, token buckets, OpenTelemetry distributed tracing, and chaos engineering.",
        "badge": "Resilience & Telemetry",
        "color": "rose",
        "chapters": [
            {
                "id": "ch-11-rate-limiters-circuit-breakers",
                "title": "11. Enterprise Traffic Shaping: Token Bucket, Sliding Window & Circuit Breakers",
                "difficulty": "Senior to Staff",
                "readTime": "24 min read",
                "summary": "Token Bucket vs Leaky Bucket vs Sliding Window Counter in Redis Lua, exponential backoff with Full Jitter, and Hystrix circuit breaker finite state machines.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-1.5 h-4 rounded-full bg-rose-400"></span> The Finite State Machine of a Circuit Breaker
  </h4>
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
    <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-800/40">
      <div class="font-bold text-emerald-400">1. CLOSED (Normal)</div>
      <p class="text-slate-300 mt-1">Traffic flows normally. If error rate exceeds 50% over a 10s sliding window, the breaker trips to OPEN.</p>
    </div>
    <div class="p-3 rounded-lg bg-rose-950/20 border border-rose-800/40">
      <div class="font-bold text-rose-400">2. OPEN (Failing Fast)</div>
      <p class="text-slate-300 mt-1">All incoming requests are immediately rejected locally without calling downstream backend. Protects failing DB from thermal collapse.</p>
    </div>
    <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-800/40">
      <div class="font-bold text-amber-400">3. HALF-OPEN (Testing)</div>
      <p class="text-slate-300 mt-1">After a cooldown period (e.g. 30s), breaker lets 5 trial requests through. If they succeed, trips to CLOSED; if any fail, resets to OPEN.</p>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "ch-12-opentelemetry-tracing",
                "title": "12. Distributed Observability: OpenTelemetry, W3C Trace Context & High-Card Metrics",
                "difficulty": "Staff Level",
                "readTime": "18 min read",
                "summary": "Traceparent headers, distributed span propagation across gRPC/HTTP, Prometheus TSDB chunking, and tail-based trace sampling at scale.",
                "html": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <p>
    In a microservices mesh with 50 hops per request, logs are useless without correlation. <strong>OpenTelemetry</strong> propagates a <code>traceparent</code> header across every network hop:
  </p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ver]-[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;16-byte Trace ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]-[&nbsp;8-byte Parent ID&nbsp;]-[flags]
  </div>
</div>
"""
            }
        ]
    }
]

print(f"Loaded {len(TIERS)} comprehensive tiers.")
