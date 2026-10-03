# modules_scratch_to_god.py
# Contains in-depth curriculum modules for Level 0, Level 1, Level 2, and Level 3.

LEVELS_DATA = [
    {
        "id": "level-0",
        "levelNum": "00",
        "badge": "Scratch / Level 0",
        "badgeColor": "emerald",
        "title": "The Absolute Foundations (Scratch)",
        "subtitle": "How the Internet actually works under the hood, basic physics of computers, and back-of-the-envelope math.",
        "icon": "zap",
        "topics": [
            {
                "id": "l0-anatomy-request",
                "title": "0.1 Anatomy of a Web Request: From Browser to Socket",
                "summary": "Step-by-step breakdown of DNS resolution, TCP 3-way handshake, TLS 1.3 negotiation, and HTTP/1.1 vs HTTP/2 vs HTTP/3.",
                "readTime": "12 min read",
                "difficulty": "Beginner",
                "content": """
<div class="space-y-6">
  <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-sm leading-relaxed text-slate-300">
    <p class="font-semibold text-emerald-400 mb-2">What happens when you type <code>https://api.example.com/v1/users</code> and press Enter?</p>
    Before a single byte of your application code executes, a complex cascade of low-level networking, cryptography, and operating system events occurs. Understanding this lifecycle is the cornerstone of diagnosing P99 latency spikes and connection bottlenecks.
  </div>

  <h4 class="text-lg font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. DNS Resolution: The Global Phonebook
  </h4>
  <p class="text-slate-300 leading-relaxed">
    The browser checks multiple caches in order before querying the network:
  </p>
  <ul class="list-disc list-inside space-y-2 text-slate-300 ml-2">
    <li><strong class="text-white">Browser DNS Cache:</strong> Chrome caches for 60s (view at <code>chrome://net-internals/#dns</code>).</li>
    <li><strong class="text-white">OS DNS Cache:</strong> Maintained by <code>systemd-resolved</code> on Linux or DNS Client service on Windows.</li>
    <li><strong class="text-white">Router & Local ISP Resolver (Recursive DNS):</strong> E.g. Cloudflare (<code>1.1.1.1</code>) or Google (<code>8.8.8.8</code>).</li>
  </ul>
  <p class="text-slate-300 leading-relaxed">
    If cache misses, the Recursive Resolver queries the hierarchy: <strong>Root DNS Servers (.)</strong> &rarr; <strong>TLD DNS Servers (.com)</strong> &rarr; <strong>Authoritative DNS Server (example.com)</strong>. Modern production systems leverage <strong>Anycast DNS</strong> so that the recursive query routes via BGP to the geographically nearest authoritative nameserver, dropping resolution latency from 150ms to &lt;15ms.
  </p>

  <h4 class="text-lg font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. Transport Layer: TCP 3-Way Handshake & TLS 1.3
  </h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-2">LEGACY: TCP + TLS 1.2 (3 RTTs)</div>
      <div class="text-xs font-mono text-slate-400 space-y-1">
        <div>1. Client &rarr; Server: SYN (1/2 RTT)</div>
        <div>2. Server &rarr; Client: SYN-ACK (1 RTT)</div>
        <div>3. Client &rarr; Server: ACK + ClientHello (1.5 RTT)</div>
        <div>4. Server &rarr; Client: ServerHello + Cert (2 RTT)</div>
        <div>5. Client &rarr; Server: KeyExchange + Finished (2.5 RTT)</div>
        <div>6. Data transmission begins at 3 RTT (~150ms on mobile!)</div>
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-emerald-800/60 bg-emerald-950/10">
      <div class="text-xs font-mono font-bold text-emerald-400 mb-2">MODERN: TLS 1.3 & HTTP/3 QUIC (0 to 1 RTT)</div>
      <div class="text-xs font-mono text-slate-400 space-y-1">
        <div>1. Client sends cryptographic keys with ClientHello immediately.</div>
        <div>2. TLS 1.3 finishes in <strong>1 single RTT</strong> for fresh connections.</div>
        <div>3. <strong>0-RTT Resumption:</strong> Pre-shared key (PSK) allows application payload to be sent in the very first packet.</div>
        <div>4. <strong>HTTP/3 (QUIC):</strong> Uses UDP instead of TCP, eliminating Head-of-Line (HoL) blocking on packet drop.</div>
      </div>
    </div>
  </div>

  <h4 class="text-lg font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 3. HTTP Evolution Matrix
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border-collapse">
      <thead>
        <tr class="border-b border-slate-800 text-slate-400 bg-slate-900/50">
          <th class="p-3">Protocol</th>
          <th class="p-3">Transport</th>
          <th class="p-3">Multiplexing</th>
          <th class="p-3">Header Compression</th>
          <th class="p-3">HoL Blocking</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300">
        <tr>
          <td class="p-3 font-semibold text-amber-400">HTTP/1.1</td>
          <td class="p-3">TCP</td>
          <td class="p-3 text-red-400">No (Pipelining flawed, 6 conns/domain)</td>
          <td class="p-3 text-red-400">None (Plaintext overhead)</td>
          <td class="p-3 text-red-400">Severe (App-level HoL)</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-cyan-400">HTTP/2</td>
          <td class="p-3">TCP</td>
          <td class="p-3 text-emerald-400">Yes (Binary frames & streams)</td>
          <td class="p-3 text-emerald-400">HPACK (Dynamic table)</td>
          <td class="p-3 text-amber-400">TCP-level HoL (1 lost packet stalls all streams)</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-emerald-400">HTTP/3</td>
          <td class="p-3">UDP (QUIC)</td>
          <td class="p-3 text-emerald-400">Yes (Independent stream recovery)</td>
          <td class="p-3 text-emerald-400">QPACK (Out-of-order header decoding)</td>
          <td class="p-3 text-emerald-400">Zero (Packet drop only pauses its own stream)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""
            },
            {
                "id": "l0-back-of-envelope",
                "title": "0.2 Back-of-the-Envelope Math: The Mental Calculator",
                "summary": "Master powers of two, QPS to storage conversions, and the golden rules of capacity planning in 30 seconds.",
                "readTime": "15 min read",
                "difficulty": "Beginner",
                "content": """
<div class="space-y-6">
  <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 text-sm text-slate-300">
    <p class="font-semibold text-cyan-400 mb-1">The Golden Rule of Back-of-the-Envelope Math:</p>
    In System Design interviews and Staff-level RFCs, precision is the enemy of clarity. You do not calculate <code>86,400 * 365</code> on paper. You round up: <strong>1 day &approx; 100,000 seconds ($10^5$)</strong>, and you think in orders of magnitude (Powers of 10 and Powers of 2).
  </div>

  <h4 class="text-base font-bold text-white">1. Powers of Two Memory Table</h4>
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
    <div class="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
      <div class="text-slate-400">2^10 (1,024)</div>
      <div class="text-emerald-400 font-bold text-sm">1 KB (Kilobyte)</div>
      <div class="text-slate-500">Short text document</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
      <div class="text-slate-400">2^20 (1,048,576)</div>
      <div class="text-cyan-400 font-bold text-sm">1 MB (Megabyte)</div>
      <div class="text-slate-500">Compressed HD image</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
      <div class="text-slate-400">2^30 (1,073,741,824)</div>
      <div class="text-indigo-400 font-bold text-sm">1 GB (Gigabyte)</div>
      <div class="text-slate-500">1 hour 1080p video</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
      <div class="text-slate-400">2^40 (1,099,511,627,776)</div>
      <div class="text-fuchsia-400 font-bold text-sm">1 TB (Terabyte)</div>
      <div class="text-slate-500">Hard drive / Database volume</div>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">2. The 86,400 Formula (Daily Requests &rarr; QPS)</h4>
  <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-2">
    <div>Exact seconds in a day: <span class="text-amber-300 font-bold">86,400</span> (approximate as <span class="text-emerald-400 font-bold">100,000</span> or 10^5)</div>
    <div class="pt-2 border-t border-slate-800">
      <div class="text-cyan-400 font-bold">&bull; 1 Million requests / day:</div>
      <div class="text-slate-400">1,000,000 / 86,400 &approx; <strong>12 QPS</strong> (Queries Per Second)</div>
    </div>
    <div>
      <div class="text-cyan-400 font-bold">&bull; 100 Million requests / day:</div>
      <div class="text-slate-400">100,000,000 / 86,400 &approx; <strong>1,200 QPS</strong> (Peak &times; 2 &approx; 2,400 QPS)</div>
    </div>
    <div>
      <div class="text-cyan-400 font-bold">&bull; 1 Billion requests / day:</div>
      <div class="text-slate-400">1,000,000,000 / 86,400 &approx; <strong>12,000 QPS</strong> (Peak &times; 2 &approx; 25,000 QPS)</div>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">3. The 80/20 Caching Rule (Pareto Principle)</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    In 95% of real-world production systems, <strong>20% of the content generates 80% of the traffic</strong>. Therefore, sizing your in-memory cache (Redis/Memcached) to store 20% of your daily working dataset guarantees an ~80% cache hit ratio, protecting your disk-bound databases from thermal collapse.
  </p>
  <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-300">
    <strong>Example Calculation:</strong> If daily read payload is 5 TB, your Redis cluster memory footprint must be: <code>5 TB &times; 0.20 = 1 TB RAM</code>.
  </div>
</div>
"""
            },
            {
                "id": "l0-scale-up-vs-scale-out",
                "title": "0.3 Scaling Foundations: Scale-Up vs Scale-Out & Statelessness",
                "summary": "When vertical scaling hits a wall, stateless app tiers, and externalizing session state into Redis and JWTs.",
                "readTime": "10 min read",
                "difficulty": "Beginner",
                "content": """
<div class="space-y-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="flex items-center gap-2 mb-2 text-amber-400 font-bold text-sm">
        <span>Vertical Scaling (Scale-Up)</span>
      </div>
      <p class="text-xs text-slate-300 leading-relaxed mb-3">
        Adding more CPU, RAM, and NVMe drives to a single box (e.g. AWS <code>u-24tb1.112xlarge</code> with 24TB RAM).
      </p>
      <div class="text-xs space-y-1 text-slate-400">
        <div><strong class="text-emerald-400">+</strong> Simple, zero network partitions, ACID transactions trivial.</div>
        <div><strong class="text-rose-400">-</strong> Hardware ceiling exists; costs scale exponentially.</div>
        <div><strong class="text-rose-400">-</strong> Single Point of Failure (SPOF) - downtime during maintenance.</div>
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="flex items-center gap-2 mb-2 text-emerald-400 font-bold text-sm">
        <span>Horizontal Scaling (Scale-Out)</span>
      </div>
      <p class="text-xs text-slate-300 leading-relaxed mb-3">
        Adding more commodity servers behind an L4/L7 load balancer.
      </p>
      <div class="text-xs space-y-1 text-slate-400">
        <div><strong class="text-emerald-400">+</strong> Theoretically infinite scale; linear cost curve.</div>
        <div><strong class="text-emerald-400">+</strong> High availability (N+1 redundancy; kill any node freely).</div>
        <div><strong class="text-rose-400">-</strong> Requires stateless services, distributed consensus, network partitions.</div>
      </div>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">Stateless Architecture: The Golden Rule</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    For horizontal autoscaling (Kubernetes HPA or AWS Auto Scaling Groups) to work, <strong>Application servers must never store client state in local process memory</strong>. If request #1 lands on Server A and request #2 lands on Server B, the user experience must be identical.
  </p>
  <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
    <div class="text-xs font-mono text-cyan-400 mb-2">WHERE STATE BELONGS:</div>
    <ul class="text-xs text-slate-300 space-y-2">
      <li><strong class="text-white">Session State:</strong> Centralized Redis Cluster or Signed Stateless JWTs (JSON Web Tokens).</li>
      <li><strong class="text-white">Uploaded Files:</strong> Object Storage (AWS S3, Google Cloud Storage, MinIO) with CDN fronting.</li>
      <li><strong class="text-white">Relational Data:</strong> Database clusters with Read Replicas and Connection Poolers (PgBouncer).</li>
    </ul>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "level-1",
        "levelNum": "01",
        "badge": "Core / Level 1",
        "badgeColor": "cyan",
        "title": "The Core Building Blocks (Mid-Level)",
        "subtitle": "Load balancers, caching hierarchies, database classification, and horizontal sharding.",
        "icon": "layers",
        "topics": [
            {
                "id": "l1-load-balancers",
                "title": "1.1 Load Balancing: L4 vs L7, Algorithms & Consistent Hashing",
                "summary": "Deep dive into Layer 4 vs Layer 7 routing, Power of Two Choices (P2C), and consistent hashing rings.",
                "readTime": "16 min read",
                "difficulty": "Intermediate",
                "content": """
<div class="space-y-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">LAYER 4 (L4) LOAD BALANCER</div>
      <div class="text-xs text-slate-400 mb-2">Operates at Transport Layer (TCP/UDP IP:Port)</div>
      <p class="text-xs text-slate-300 leading-relaxed">
        Does not look inside HTTP packets or decrypt TLS. Uses Linux IPVS, Maglev, or HAProxy in TCP mode. Routes packets by modifying IP packet headers via Direct Server Return (DSR). Can handle <strong>millions of packets per second (Mpps)</strong> with sub-microsecond overhead.
      </p>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-indigo-400 mb-1">LAYER 7 (L7) LOAD BALANCER</div>
      <div class="text-xs text-slate-400 mb-2">Operates at Application Layer (HTTP/gRPC/WebSocket)</div>
      <p class="text-xs text-slate-300 leading-relaxed">
        Terminates TLS, inspects HTTP headers, cookies, URL paths (e.g. <code>/api/v1/checkout</code> &rarr; Checkout Cluster, <code>/static/*</code> &rarr; CDN). Envoy, Nginx, AWS ALB. Higher CPU usage, but enables smart routing, circuit breaking, and rate limiting.
      </p>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">Load Balancing Algorithms Compared</h4>
  <ul class="space-y-3 text-xs text-slate-300">
    <li class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <span class="text-white font-bold">Round Robin & Weighted Round Robin:</span> Distributes sequentially. Flawed when requests have wildly varying processing durations (e.g., report generation vs health check).
    </li>
    <li class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <span class="text-white font-bold">Least Connections:</span> Routes to the backend with fewest active TCP sockets. Highly effective for long-lived connections (WebSockets, SSE).
    </li>
    <li class="p-3 rounded-lg bg-slate-900 border border-cyan-800/50 bg-cyan-950/10">
      <span class="text-cyan-400 font-bold">Power of Two Random Choices (P2C):</span> Picks two random backends and routes to the one with lower load/latency. Mitigates the "herd effect" of Least Connections and approaches optimal balance with O(1) computational overhead. Used by Envoy, Twitter, and Finagle.
    </li>
    <li class="p-3 rounded-lg bg-slate-900 border border-emerald-800/50 bg-emerald-950/10">
      <span class="text-emerald-400 font-bold">Consistent Hashing with Virtual Nodes:</span> Hashes keys and servers onto a circular ring ($0$ to $2^{32}-1$). Adding or removing a server reshuffles only $K/N$ keys instead of $100\%$! Essential for distributed caches and stateful databases.
    </li>
  </ul>
</div>
"""
            },
            {
                "id": "l1-caching-patterns",
                "title": "1.2 Caching Architectures, Invalidation & The 4 Nightmares",
                "summary": "Cache-aside vs write-through, LRU/LFU, cache stampede (XFetch), cache penetration with Bloom filters, and cache avalanche.",
                "readTime": "18 min read",
                "difficulty": "Intermediate",
                "content": """
<div class="space-y-6">
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border-collapse">
      <thead>
        <tr class="border-b border-slate-800 text-slate-400 bg-slate-900/50">
          <th class="p-3">Pattern</th>
          <th class="p-3">How it Works</th>
          <th class="p-3">Pros</th>
          <th class="p-3">Cons</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300">
        <tr>
          <td class="p-3 font-semibold text-cyan-400">Cache-Aside (Lazy)</td>
          <td class="p-3">App checks cache. On miss, reads DB, populates cache, returns.</td>
          <td class="p-3 text-emerald-400">Only requested data is cached. Cache failure doesn't halt writes.</td>
          <td class="p-3 text-rose-400">Cache miss penalty (3 network hops). Stale data if DB updated directly.</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-emerald-400">Write-Through</td>
          <td class="p-3">App writes to Cache; Cache synchronously writes to DB before ACK.</td>
          <td class="p-3 text-emerald-400">Data in cache is never stale; reads are always hot.</td>
          <td class="p-3 text-rose-400">Higher write latency (must wait for DB). Caches data never read.</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-amber-400">Write-Behind (Write-Back)</td>
          <td class="p-3">App writes to Cache immediately. Cache asynchronously flushes to DB.</td>
          <td class="p-3 text-emerald-400">Insane write throughput; absorbs massive traffic spikes.</td>
          <td class="p-3 text-rose-400">Data loss risk if cache crashes before flushing to durable DB.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white mt-6">The 4 Production Cache Nightmares & Their Staff-Level Fixes</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-rose-900/40">
      <div class="text-xs font-mono font-bold text-rose-400 mb-1">1. CACHE STAMPEDE (DOGPILING)</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        A super-hot key (e.g. world cup score) expires. 100,000 concurrent requests miss simultaneously and crush the database.
      </p>
      <div class="p-2 rounded bg-slate-950 text-xs text-emerald-400 font-mono">
        Solution: Mutex locking (Redis SETNX) or Probabilistic Early Expiration (XFetch algorithm).
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-amber-900/40">
      <div class="text-xs font-mono font-bold text-amber-400 mb-1">2. CACHE PENETRATION</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        Attacker queries for non-existent IDs (e.g. <code>id=-9999</code>). Cache misses every time, passing every request directly to the DB.
      </p>
      <div class="p-2 rounded bg-slate-950 text-xs text-emerald-400 font-mono">
        Solution: Bloom Filter fronting the cache (O(1) probabilistic set membership) OR caching empty/null results with short TTL.
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-indigo-900/40">
      <div class="text-xs font-mono font-bold text-indigo-400 mb-1">3. CACHE AVALANCHE</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        Huge batch of cached items set with identical 24-hour TTL all expire at the exact same second, nuking the database.
      </p>
      <div class="p-2 rounded bg-slate-950 text-xs text-emerald-400 font-mono">
        Solution: Add Random Jitter: <code>TTL = base_ttl + rand(0, 300)</code> so expirations smoothly distribute over time.
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-cyan-900/40">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">4. CACHE BREAKDOWN</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        A single celebrity profile key experiences 500,000 QPS, exhausting the single Redis node's NIC/CPU bandwidth.
      </p>
      <div class="p-2 rounded bg-slate-950 text-xs text-emerald-400 font-mono">
        Solution: Two-Tier Caching (L1 Local in-memory Caffeine/Go-cache + L2 Distributed Redis) with pub/sub invalidation.
      </div>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "l1-databases-sharding",
                "title": "1.3 Databases, Indexing Internals & Horizontal Sharding",
                "summary": "B+ Trees vs LSM-Trees, Read Replicas vs Sharding, selecting the right shard key, and handling cross-shard joins.",
                "readTime": "20 min read",
                "difficulty": "Intermediate",
                "content": """
<div class="space-y-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">B+ TREE STORAGE ENGINE</div>
      <div class="text-xs text-slate-400 mb-2">PostgreSQL, MySQL InnoDB, SQLite</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>Optimized for fast reads ($O(\\log N)$ point and range scans).</li>
        <li>Fixed-size disk pages (typically 8KB or 16KB).</li>
        <li>Random I/O on writes: In-place page updates require Write-Ahead Logging (WAL) for durability.</li>
        <li>Read-heavy workloads with complex secondary indexes.</li>
      </ul>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-emerald-400 mb-1">LSM-TREE (Log-Structured Merge)</div>
      <div class="text-xs text-slate-400 mb-2">Cassandra, RocksDB, ScyllaDB, Bigtable</div>
      <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
        <li>Optimized for maximum write throughput ($O(1)$ append).</li>
        <li>Writes buffer in-memory (MemTable) + append to commit log.</li>
        <li>Flushed sequentially to immutable disk files (SSTables).</li>
        <li>Background compaction cleans tombstones and merges sorted runs. Reads require Bloom filters.</li>
      </ul>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">Database Sharding: Strategies & Pitfalls</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    When your dataset exceeds single-box storage (e.g. &gt; 4 TB) or write IOPS exceed SSD bandwidth, you shard horizontally across independent database instances.
  </p>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border-collapse">
      <thead>
        <tr class="border-b border-slate-800 text-slate-400 bg-slate-900/50">
          <th class="p-3">Strategy</th>
          <th class="p-3">Mechanics</th>
          <th class="p-3">Pros</th>
          <th class="p-3">Critical Risks</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300">
        <tr>
          <td class="p-3 font-semibold text-white">Range-Based</td>
          <td class="p-3">IDs 1-1M &rarr; Shard 1; IDs 1M-2M &rarr; Shard 2.</td>
          <td class="p-3 text-emerald-400">Simple, range queries stay within one shard.</td>
          <td class="p-3 text-rose-400">Hotspot disaster: sequential IDs route 100% of new writes to the newest shard.</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-cyan-400">Hash-Based</td>
          <td class="p-3"><code>shard = hash(user_id) % N</code></td>
          <td class="p-3 text-emerald-400">Uniform distribution of writes and reads.</td>
          <td class="p-3 text-rose-400">Adding a shard requires massive re-sharding (solved via Consistent Hashing).</td>
        </tr>
        <tr>
          <td class="p-3 font-semibold text-emerald-400">Directory-Based</td>
          <td class="p-3">Lookup service maps Entity ID &rarr; Shard ID.</td>
          <td class="p-3 text-emerald-400">Ultimate flexibility; rebalance shards by updating lookup table.</td>
          <td class="p-3 text-rose-400">Lookup service becomes single point of failure and extra latency hop.</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "level-2",
        "levelNum": "02",
        "badge": "Distributed / Level 2",
        "badgeColor": "indigo",
        "title": "Distributed Systems Principles & Trade-offs (Senior Engineer)",
        "subtitle": "The CAP/PACELC theorems, consistency spectrum, Kafka internals, and microservice sagas.",
        "icon": "cpu",
        "topics": [
            {
                "id": "l2-cap-pacelc",
                "title": "2.1 The CAP & PACELC Theorems: Beyond the Textbook Lie",
                "summary": "Why 'pick two' is misleading, network partitions are inevitable, and how PACELC governs normal system operations.",
                "readTime": "15 min read",
                "difficulty": "Advanced",
                "content": """
<div class="space-y-6">
  <div class="p-4 rounded-xl bg-slate-900 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
    <strong class="text-indigo-400 font-bold">The Senior Engineer Reality Check:</strong> You CANNOT choose "CA" (Consistency + Availability without Partition Tolerance) in any distributed network. Network cables get cut, switches reboot, and GC pauses occur. <strong>Partitions (P) are a physical fact of life</strong>. The real decision is: <em>When a network partition strikes, do you choose Consistency (fail the request) or Availability (accept stale writes)?</em>
  </div>

  <h4 class="text-base font-bold text-white mt-4">The PACELC Theorem (Abadi's Formula)</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    What happens 99.9% of the time when there is NO partition? That's what PACELC answers:
  </p>
  <div class="p-4 rounded-xl bg-slate-950 font-mono text-xs border border-slate-800 text-center">
    If <span class="text-amber-400 font-bold">Partition (P)</span>: choose <span class="text-cyan-400 font-bold">Availability (A)</span> OR <span class="text-rose-400 font-bold">Consistency (C)</span>;<br/>
    <span class="text-emerald-400 font-bold">Else (E)</span>: choose <span class="text-fuchsia-400 font-bold">Latency (L)</span> OR <span class="text-indigo-400 font-bold">Consistency (C)</span>.
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-cyan-400">PA/EL</div>
      <div class="text-slate-400 mt-1">Cassandra, DynamoDB (eventual)</div>
      <div class="text-slate-500 mt-2 text-[11px]">During partition: Available.<br/>Normal: Optimized for low latency over strong consistency.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-indigo-400">PC/EC</div>
      <div class="text-slate-400 mt-1">Google Spanner, CockroachDB</div>
      <div class="text-slate-500 mt-2 text-[11px]">During partition: Consistent.<br/>Normal: Sacrifices latency to guarantee strict serializability.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-emerald-400">PC/EL</div>
      <div class="text-slate-400 mt-1">MongoDB, Redis Sentinel</div>
      <div class="text-slate-500 mt-2 text-[11px]">During partition: Refuses writes if primary isolated.<br/>Normal: Fast async replication to secondaries.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-amber-400">PA/EC</div>
      <div class="text-slate-400 mt-1">Rare / Theoretical</div>
      <div class="text-slate-500 mt-2 text-[11px]">Available during partition, but pays heavy latency penalty during normal mode.</div>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "l2-kafka-streaming",
                "title": "2.2 Event Streaming & Kafka: Partitions, Offsets & Zero-Copy",
                "summary": "Why Kafka achieves millions of msgs/sec: sequential disk I/O, Linux page cache, sendfile zero-copy, and consumer group rebalancing.",
                "readTime": "20 min read",
                "difficulty": "Advanced",
                "content": """
<div class="space-y-6">
  <p class="text-slate-300 text-xs leading-relaxed">
    Traditional message queues (RabbitMQ, SQS) maintain an in-memory index of messages and delete messages immediately upon consumer ACK. Kafka inverted this paradigm: it is an <strong>append-only, immutable commit log</strong> partitioned across disks.
  </p>

  <h4 class="text-base font-bold text-white mt-4">Why Kafka Is So Blazing Fast (The 3 Secrets)</h4>
  <div class="space-y-3 text-xs text-slate-300">
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-emerald-400 mb-1">1. Sequential Disk I/O Beats Random RAM</div>
      <p>Sequential disk throughput on modern NVMe SSDs reaches 3,500+ MB/s. Because Kafka partitions only append to the tail, OS disk read-ahead and write-behind optimizations work at 100% efficiency.</p>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-cyan-400 mb-1">2. OS Page Cache & No JVM GC Overhead</div>
      <p>Kafka does not cache messages in the JVM heap (avoiding GC pauses and 2x memory bloat). It relies directly on the Linux kernel Page Cache. If a consumer is reading recent data, it reads straight from kernel RAM without hitting physical disk.</p>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-indigo-400/50 bg-indigo-950/10">
      <div class="font-bold text-indigo-400 mb-1">3. Linux Zero-Copy (<code>sendfile</code> syscall)</div>
      <p>Traditional data transfer copies bytes 4 times: Disk &rarr; Kernel Buffer &rarr; User Space &rarr; Socket Buffer &rarr; NIC. Kafka uses the <code>sendfile()</code> syscall, transferring bytes directly from <strong>Kernel Page Cache &rarr; NIC buffer via DMA</strong>, bypassing user memory entirely.</p>
    </div>
  </div>

  <h4 class="text-base font-bold text-white mt-4">Partitioning & Scaling Model</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    The <strong>Partition</strong> is Kafka's fundamental unit of parallelism. A single consumer within a Consumer Group can read from multiple partitions, but <strong>a partition can only be read by ONE consumer instance at a time</strong>. To scale your consumption throughput to 50 concurrent workers, you must have at least 50 partitions!
  </p>
</div>
"""
            },
            {
                "id": "l2-sagas-distributed-tx",
                "title": "2.3 Distributed Transactions: 2PC vs Saga Pattern",
                "summary": "Why Two-Phase Commit fails at scale, Choreography vs Orchestration Sagas, and compensating transactions.",
                "readTime": "16 min read",
                "difficulty": "Advanced",
                "content": """
<div class="space-y-6">
  <div class="p-4 rounded-xl bg-slate-900 border border-rose-900/40 text-xs text-slate-300 leading-relaxed">
    <strong class="text-rose-400 font-bold">The Microservice Dilemma:</strong> In a monolithic system, checking inventory, charging a credit card, and creating an order happen in a single local ACID database transaction. In microservices with separated databases, a single ACID transaction requires a <strong>Two-Phase Commit (2PC)</strong>, which holds locks across network boundaries, crushes throughput, and deadlocks if a coordinator crashes.
  </div>

  <h4 class="text-base font-bold text-white mt-4">The Saga Pattern: Eventual Consistency for Workflows</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    A Saga is a sequence of local transactions. Each transaction updates data within a single service. If a step fails, the Saga executes <strong>Compensating Transactions</strong> in reverse order to undo changes.
  </p>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-cyan-400 mb-1">CHOREOGRAPHY SAGA (Decentralized)</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        Services publish and listen to domain events via Kafka/RabbitMQ. Order Service emits <code>OrderCreated</code> &rarr; Payment Service listens and charges &rarr; emits <code>PaymentSuccess</code> &rarr; Inventory reserves.
      </p>
      <div class="text-xs text-slate-400">
        <strong>Best for:</strong> Simple flows (2-4 steps).<br/>
        <strong>Drawback:</strong> Complex dependency spaghetti; hard to track workflow state.
      </div>
    </div>
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
      <div class="text-xs font-mono font-bold text-emerald-400 mb-1">ORCHESTRATION SAGA (Centralized)</div>
      <p class="text-xs text-slate-300 leading-relaxed mb-2">
        A central Orchestrator (e.g. Temporal, Cadence, AWS Step Functions) coordinates steps, tracks state machines, and explicitly issues commands and compensating rollbacks.
      </p>
      <div class="text-xs text-slate-400">
        <strong>Best for:</strong> Enterprise flows (financial payments, multi-step checkouts).<br/>
        <strong>Drawback:</strong> Central orchestrator logic must be maintained.
      </div>
    </div>
  </div>
</div>
"""
            }
        ]
    },
    {
        "id": "level-3",
        "levelNum": "03",
        "badge": "Staff / Level 3",
        "badgeColor": "fuchsia",
        "title": "Advanced Reliability & Planet-Scale (Staff Engineer)",
        "subtitle": "Raft consensus, distributed locking with fencing tokens, Twitter Snowflake ID generation, and multi-region routing.",
        "icon": "shield-check",
        "topics": [
            {
                "id": "l3-raft-consensus",
                "title": "3.1 Distributed Consensus: The Raft Protocol Deconstructed",
                "summary": "How etcd, CockroachDB, and Kafka KRaft maintain a single source of truth across Byzantine failure domains.",
                "readTime": "22 min read",
                "difficulty": "Staff Level",
                "content": """
<div class="space-y-6">
  <p class="text-slate-300 text-xs leading-relaxed">
    Consensus means getting multiple distributed nodes to agree on a sequence of state values, even when nodes crash or messages are delayed. Paxos was the theoretical pioneer, but <strong>Raft</strong> was created specifically to be understandable and implementable.
  </p>

  <h4 class="text-base font-bold text-white mt-4">The 3 Sub-Problems Solved by Raft</h4>
  <div class="space-y-3 text-xs text-slate-300">
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-cyan-400 mb-1">1. Leader Election</div>
      <p>Nodes exist in one of three states: <strong>Follower</strong>, <strong>Candidate</strong>, or <strong>Leader</strong>. If a follower misses heartbeats (randomized election timeout 150-300ms), it increments its Term and requests votes. A candidate needs a Quorum of votes ($N/2 + 1$) to become Leader.</p>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="font-bold text-emerald-400 mb-1">2. Log Replication</div>
      <p>Clients send writes ONLY to the Leader. The Leader appends the entry to its log and broadcasts <code>AppendEntries</code> RPCs. Once the entry is safely replicated on a majority of nodes, the Leader commits it and applies it to its local State Machine, then replies to the client.</p>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-fuchsia-400/50 bg-fuchsia-950/10">
      <div class="font-bold text-fuchsia-400 mb-1">3. Safety Invariant</div>
      <p>If a leader commits a log entry at a given index and term, no other leader can ever commit a different entry for that index. A node will refuse to vote for a candidate whose log is less up-to-date than its own.</p>
    </div>
  </div>
</div>
"""
            },
            {
                "id": "l3-distributed-locks",
                "title": "3.2 Distributed Locks & Concurrency: Why Redlock is Flawed",
                "summary": "Martin Kleppmann's critique of Redis Redlock, GC pause hazards, and how Fencing Tokens solve data corruption.",
                "readTime": "18 min read",
                "difficulty": "Staff Level",
                "content": """
<div class="space-y-6">
  <div class="p-4 rounded-xl bg-slate-900 border border-rose-900/50 text-xs text-slate-300 leading-relaxed">
    <strong class="text-rose-400 font-bold">The Dangerous Assumption:</strong> Many engineers use Redis <code>SET resource_name my_random_token NX PX 30000</code> and assume their critical section is safe. In distributed systems with asynchronous networks and Stop-The-World garbage collection pauses, this assumption will silently corrupt data.
  </div>

  <h4 class="text-base font-bold text-white mt-4">The GC Pause Attack Scenario</h4>
  <ol class="list-decimal list-inside space-y-2 text-xs text-slate-300">
    <li><strong>Client 1</strong> acquires lock on resource for 10 seconds.</li>
    <li><strong>Client 1</strong> experiences a sudden 15-second Stop-The-World GC pause or disk page fault.</li>
    <li>While Client 1 is frozen, the lock TTL expires in Redis.</li>
    <li><strong>Client 2</strong> acquires the now-free lock and updates the database.</li>
    <li><strong>Client 1</strong> wakes up from GC pause, believes it still holds the lock, and overwrites Client 2's data!</li>
  </ol>

  <h4 class="text-base font-bold text-white mt-4">The Solution: Fencing Tokens</h4>
  <p class="text-slate-300 text-xs leading-relaxed">
    Every time a lock is granted by a consensus service (etcd, ZooKeeper), it issues a strictly monotonically increasing <strong>Fencing Token</strong> (e.g. <code>token = 34</code>). When writing to the storage layer, the storage rejects any write containing a token lower than the highest token it has already processed.
  </p>
</div>
"""
            },
            {
                "id": "l3-snowflake-id",
                "title": "3.3 Distributed ID Generation: Twitter Snowflake & ULID",
                "summary": "Generating 64-bit sortable unique IDs without database bottlenecks at 100,000 IDs/sec per machine.",
                "readTime": "14 min read",
                "difficulty": "Staff Level",
                "content": """
<div class="space-y-6">
  <p class="text-slate-300 text-xs leading-relaxed">
    Why not use UUIDv4? UUIDs are 128-bit strings (heavy storage footprint) and completely random, which causes severe B+ Tree index page fragmentation in relational databases. Twitter solved this with <strong>Snowflake</strong>: a 64-bit integer that fits into a standard <code>BIGINT</code> and is roughly time-sortable.
  </p>

  <h4 class="text-base font-bold text-white mt-4">Twitter Snowflake 64-Bit Allocation</h4>
  <div class="grid grid-cols-4 gap-2 text-center text-xs font-mono">
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="text-slate-500">1 bit</div>
      <div class="text-amber-400 font-bold">Sign (0)</div>
      <div class="text-slate-500 text-[10px]">Unused</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="text-slate-500">41 bits</div>
      <div class="text-cyan-400 font-bold">Timestamp (ms)</div>
      <div class="text-slate-500 text-[10px]">69 years lifetime</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="text-slate-500">10 bits</div>
      <div class="text-emerald-400 font-bold">Machine ID</div>
      <div class="text-slate-500 text-[10px]">1,024 nodes</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
      <div class="text-slate-500">12 bits</div>
      <div class="text-indigo-400 font-bold">Sequence</div>
      <div class="text-slate-500 text-[10px]">4,096 IDs / ms / node</div>
    </div>
  </div>
  <div class="p-3 rounded-lg bg-slate-900 text-xs text-slate-400 font-mono">
    Throughput per machine: <code>4,096 IDs &times; 1,000 ms = 4,096,000 unique IDs / second</code> without coordination!
  </div>
</div>
"""
            }
        ]
    }
]

print(f"Loaded {len(LEVELS_DATA)} foundation levels.")
