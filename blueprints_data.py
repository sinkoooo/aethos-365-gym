# blueprints_data.py
# Contains the 10 God-Level Real-World System Design Blueprints with architectures, scale math, failure modes, and SVG diagrams.

BLUEPRINTS = [
    {
        "id": "blueprint-twitter",
        "title": "Blueprint 1: Planet-Scale Distributed Social Feed (Twitter / X)",
        "badge": "Social Graph & Timeline",
        "scaleStats": {
            "dau": "500 Million DAU",
            "readQps": "350,000 Read QPS",
            "writeQps": "15,000 Write QPS (Tweets)",
            "storage": "120 TB / Day (Media + Metadata)"
        },
        "description": "How Twitter handles the celebrity fanout problem (Lady Gaga / Elon Musk with 100M+ followers) using a hybrid push-pull timeline architecture.",
        "architectureSvg": """
<svg viewBox="0 0 800 380" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ec4899" stop-opacity="0.8"/>
    </linearGradient>
  </defs>

  <!-- Title & Legend -->
  <text x="20" y="30" fill="#94a3b8" font-family="monospace" font-size="12" font-weight="bold">TWITTER HYBRID TIMELINE TOPOLOGY</text>

  <!-- Client -->
  <rect x="30" y="160" width="110" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="85" y="195" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">User App</text>
  <text x="85" y="210" fill="#94a3b8" font-size="9" text-anchor="middle">iOS / Web</text>

  <!-- API Gateway / L7 -->
  <rect x="180" y="145" width="110" height="90" rx="8" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>
  <text x="235" y="180" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">API Gateway</text>
  <text x="235" y="198" fill="#38bdf8" font-size="9" text-anchor="middle">Envoy Proxy</text>
  <text x="235" y="215" fill="#94a3b8" font-size="8" text-anchor="middle">Auth &amp; RateLimit</text>

  <!-- Fanout Service -->
  <rect x="340" y="80" width="130" height="70" rx="8" fill="url(#cyanGrad)" stroke="#06b6d4" stroke-width="2"/>
  <text x="405" y="112" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">Fanout Worker</text>
  <text x="405" y="128" fill="#e0f2fe" font-size="9" text-anchor="middle">Normal Users (&lt;25k)</text>
  <text x="405" y="140" fill="#e0f2fe" font-size="8" text-anchor="middle">Push to Redis Timelines</text>

  <!-- Timeline Service -->
  <rect x="340" y="230" width="130" height="70" rx="8" fill="url(#purpleGrad)" stroke="#a855f7" stroke-width="2"/>
  <text x="405" y="262" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">Timeline Aggregator</text>
  <text x="405" y="278" fill="#f3e8ff" font-size="9" text-anchor="middle">Celebrity Fanout-on-Read</text>
  <text x="405" y="290" fill="#f3e8ff" font-size="8" text-anchor="middle">Merge @ Request Time</text>

  <!-- Redis Timeline Cache -->
  <rect x="530" y="60" width="120" height="60" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="590" y="90" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Redis Clusters</text>
  <text x="590" y="106" fill="#94a3b8" font-size="9" text-anchor="middle">User Timelines (Lists)</text>

  <!-- Social Graph Service (FlockDB) -->
  <rect x="530" y="160" width="120" height="60" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="590" y="190" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Social Graph</text>
  <text x="590" y="206" fill="#94a3b8" font-size="9" text-anchor="middle">Follower Edges DB</text>

  <!-- Primary Tweet Store (Manhattan / Cassandra) -->
  <rect x="530" y="260" width="120" height="60" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="1.5"/>
  <text x="590" y="290" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Tweet Store</text>
  <text x="590" y="306" fill="#94a3b8" font-size="9" text-anchor="middle">Cassandra / Manhattan</text>

  <!-- Connections -->
  <path d="M 140 190 L 180 190" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 290 170 L 340 120" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="4"/>
  <path d="M 290 210 L 340 260" stroke="#a855f7" stroke-width="1.5"/>
  <path d="M 470 115 L 530 95" stroke="#10b981" stroke-width="1.5"/>
  <path d="M 470 125 L 530 180" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 470 265 L 530 200" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 470 280 L 530 285" stroke="#ec4899" stroke-width="1.5"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">The Celebrity Fanout Dilemma</h5>
  <p>If Justin Bieber has 100M followers and posts a tweet:</p>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>Pure Push (Fanout-on-Write):</strong> Inserting Bieber's tweet into 100,000,000 user timeline lists in Redis takes ~5 minutes, creating unacceptable lag and burning billions of write IOPS.</li>
    <li><strong>Pure Pull (Fanout-on-Read):</strong> Querying every single account a user follows when loading the home feed requires hundreds of DB queries per scroll, crippling read latency.</li>
  </ul>
  <h5 class="text-sm font-bold text-white mt-4">The Production Hybrid Solution</h5>
  <ol class="list-decimal list-inside space-y-2 ml-2">
    <li>Users with &lt; 25,000 followers use <strong>Fanout-on-Write (Push)</strong>. Their tweets are immediately inserted into followers' Redis timeline lists (O(1) read).</li>
    <li>Celebrity accounts (&gt; 25,000 followers) use <strong>Fanout-on-Read (Pull)</strong>. When a user requests their home feed, the timeline aggregator fetches their pre-computed Redis timeline AND dynamically pulls recent tweets from celebrities they follow, performing an in-memory K-way merge in &lt;15ms.</li>
  </ol>
</div>
"""
    },
    {
        "id": "blueprint-whatsapp",
        "title": "Blueprint 2: Ultra-Low Latency Messaging & Presence (WhatsApp)",
        "badge": "Real-Time Sockets & Erlang",
        "scaleStats": {
            "dau": "2+ Billion DAU",
            "messages": "100 Billion Messages / Day",
            "peakConnections": "100 Million Concurrent WebSockets",
            "latency": "< 50ms Delivery P99"
        },
        "description": "2 Billion users served by minimal infrastructure using FreeBSD kernel tuning, Erlang BEAM actor model, and ephemeral message store.",
        "architectureSvg": """
<svg viewBox="0 0 800 360" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- Clients -->
  <rect x="30" y="70" width="100" height="50" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="80" y="95" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Alice (Sender)</text>
  <text x="80" y="110" fill="#94a3b8" font-size="8" text-anchor="middle">Noise Protocol</text>

  <rect x="30" y="240" width="100" height="50" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="80" y="265" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Bob (Receiver)</text>
  <text x="80" y="280" fill="#94a3b8" font-size="8" text-anchor="middle">Noise Protocol</text>

  <!-- Gateway Erlang Cluster -->
  <rect x="200" y="50" width="160" height="260" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="280" y="80" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">Erlang Gateway Cluster</text>
  <text x="280" y="96" fill="#94a3b8" font-size="8" text-anchor="middle">2M Persistent Conns/Node</text>

  <rect x="220" y="115" width="120" height="40" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="280" y="140" fill="#f8fafc" font-size="9" text-anchor="middle">Alice's Actor Process</text>

  <rect x="220" y="205" width="120" height="40" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="280" y="230" fill="#f8fafc" font-size="9" text-anchor="middle">Bob's Actor Process</text>

  <!-- Session & Presence Registry (Mnesia / Redis) -->
  <rect x="440" y="60" width="140" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="510" y="90" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">User Session Router</text>
  <text x="510" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">UserID &rarr; Gateway Node IP</text>
  <text x="510" y="118" fill="#94a3b8" font-size="7" text-anchor="middle">Distributed Hash Table (DHT)</text>

  <!-- Transient Offline Queue (Cassandra/Spanner) -->
  <rect x="440" y="220" width="140" height="70" rx="8" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
  <text x="510" y="250" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Ephemeral Offline DB</text>
  <text x="510" y="265" fill="#94a3b8" font-size="8" text-anchor="middle">Stores ONLY until delivered</text>
  <text x="510" y="278" fill="#ef4444" font-size="7" text-anchor="middle">Auto-delete on ACK!</text>

  <!-- Push Notification Service -->
  <rect x="650" y="220" width="120" height="70" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="1.5"/>
  <text x="710" y="250" fill="#f472b6" font-size="10" font-weight="bold" text-anchor="middle">APNs / FCM Push</text>
  <text x="710" y="266" fill="#94a3b8" font-size="8" text-anchor="middle">Wakeup asleep devices</text>

  <!-- Connecting Lines -->
  <path d="M 130 95 L 220 135" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 340 135 L 440 95" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 340 145 L 340 215" stroke="#10b981" stroke-width="2" stroke-dasharray="4"/>
  <path d="M 220 225 L 130 265" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 340 225 L 440 255" stroke="#a855f7" stroke-width="1.5"/>
  <path d="M 580 255 L 650 255" stroke="#ec4899" stroke-width="1.5"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why WhatsApp Achieves 2M Connections per Server</h5>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>Erlang BEAM Virtual Machine:</strong> Erlang processes are lightweight user-space green threads consuming only ~2KB of RAM each (compared to a 1MB OS thread in Java/Go). A single box with 64GB RAM comfortably handles 2,000,000 concurrent socket connections.</li>
    <li><strong>Ephemeral Message Architecture:</strong> WhatsApp does NOT store message history on servers. The server is simply a routing broker. Once Bob's client sends back an ACK receipt (double blue check), the message is instantly purged from disk/RAM.</li>
    <li><strong>Presence Throttling:</strong> User "Online" / "Typing..." indicators are NOT broadcast to all phone contacts (which would generate $O(N^2)$ traffic). Presence is pushed ONLY to contacts who are currently actively viewing Alice's conversation screen.</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-uber",
        "title": "Blueprint 3: Real-Time Geospatial Driver Dispatch (Uber / Lyft)",
        "badge": "Geohash & Uber H3 Hexagons",
        "scaleStats": {
            "activeDrivers": "5 Million Concurrent Drivers",
            "pingInterval": "Every 4 Seconds",
            "ingestQps": "1.25 Million Location Updates / Sec",
            "dispatchLatency": "< 500ms for Nearest Match"
        },
        "description": "Sub-second geospatial radius queries and driver matching at planetary scale using Uber's open-source H3 Hexagonal Hierarchical Spatial Index.",
        "architectureSvg": """
<svg viewBox="0 0 800 360" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- Driver App -->
  <rect x="30" y="80" width="120" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="90" y="110" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Driver GPS Ping</text>
  <text x="90" y="125" fill="#38bdf8" font-size="8" text-anchor="middle">Lat, Lng every 4s (gRPC)</text>

  <!-- Location Ingestion Gateway -->
  <rect x="200" y="75" width="130" height="70" rx="8" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>
  <text x="265" y="105" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Ingest Gateway</text>
  <text x="265" y="122" fill="#10b981" font-size="8" text-anchor="middle">Computes H3 Hex Index</text>
  <text x="265" y="134" fill="#94a3b8" font-size="7" text-anchor="middle">Resolution 8 (~460m)</text>

  <!-- Kafka Stream -->
  <rect x="380" y="85" width="120" height="50" rx="6" fill="#1e293b" stroke="#ec4899" stroke-width="1.5"/>
  <text x="440" y="110" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Kafka Log</text>
  <text x="440" y="125" fill="#94a3b8" font-size="8" text-anchor="middle">Partitioned by City/H3</text>

  <!-- In-Memory Geospatial Service (Ringpop / Redis) -->
  <rect x="550" y="60" width="190" height="100" rx="10" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="645" y="90" fill="#22d3ee" font-size="12" font-weight="bold" text-anchor="middle">Location Shard (In-Memory)</text>
  <text x="645" y="106" fill="#94a3b8" font-size="8" text-anchor="middle">Hexagon Cell &rarr; Set of Driver IDs</text>
  <text x="645" y="120" fill="#34d399" font-size="8" text-anchor="middle">Sub-millisecond K-Ring Lookup</text>
  <text x="645" y="145" fill="#f59e0b" font-size="7" text-anchor="middle">Ringpop Gossip Protocol</text>

  <!-- Rider Request -->
  <rect x="30" y="240" width="120" height="60" rx="8" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
  <text x="90" y="270" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Rider App</text>
  <text x="90" y="285" fill="#c084fc" font-size="8" text-anchor="middle">"Request Ride" (Lat, Lng)</text>

  <!-- Dispatch / Matching Engine -->
  <rect x="250" y="235" width="220" height="70" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="262" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Dispatch &amp; Supply Matcher</text>
  <text x="360" y="278" fill="#94a3b8" font-size="8" text-anchor="middle">Queries K-Ring Neighbor Cells in H3</text>
  <text x="360" y="292" fill="#38bdf8" font-size="8" text-anchor="middle">ETA Calculation &amp; Dynamic Pricing</text>

  <!-- Trip State DB -->
  <rect x="550" y="235" width="190" height="70" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
  <text x="645" y="265" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Trip State (MySQL / Docstore)</text>
  <text x="645" y="282" fill="#94a3b8" font-size="8" text-anchor="middle">ACID Lock on Ride Acceptance</text>

  <!-- Connecting Lines -->
  <path d="M 150 110 L 200 110" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 330 110 L 380 110" stroke="#10b981" stroke-width="2"/>
  <path d="M 500 110 L 550 110" stroke="#ec4899" stroke-width="2"/>
  <path d="M 150 270 L 250 270" stroke="#a855f7" stroke-width="2"/>
  <path d="M 470 270 L 550 270" stroke="#10b981" stroke-width="2"/>
  <path d="M 360 235 L 600 160" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="3"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why Uber Built H3 Hexagons Instead of Squares or Geohash</h5>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>Equal Neighbor Distances:</strong> In a rectangular grid or Geohash, diagonal neighbors are $\\sqrt{2} \\times d$ away, distorting radius queries. In a hexagon, all 6 neighbors share identical edge lengths and center-to-center distances!</li>
    <li><strong>H3 K-Ring Queries:</strong> To find drivers within 2 km of a rider, Uber takes the rider's H3 cell and executes <code>h3.gridDisk(cell, k=2)</code> to get the concentric hexagon ring in O(1) time.</li>
    <li><strong>Partitioning:</strong> Shards are partitioned geographically by city (e.g., San Francisco vs London). A driver in SF never contends for memory with a driver in Tokyo.</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-netflix",
        "title": "Blueprint 4: High-Throughput Video Streaming DAG (Netflix / YouTube)",
        "badge": "Transcoding & CDN Edge",
        "scaleStats": {
            "streamingTraffic": "15%+ of Global Internet Downstream",
            "videoHours": "500 Hours Uploaded / Min (YouTube)",
            "edgeAppliances": "18,000+ Open Connect Servers",
            "protocols": "HLS & MPEG-DASH Adaptive Bitrate"
        },
        "description": "Parallel chunked video transcoding DAG pipelines, Adaptive Bitrate Streaming (ABR), and Open Connect edge hardware.",
        "architectureSvg": """
<svg viewBox="0 0 800 340" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- Creator Upload -->
  <rect x="20" y="80" width="100" height="50" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="70" y="105" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Creator Upload</text>
  <text x="70" y="118" fill="#94a3b8" font-size="7" text-anchor="middle">Raw 4K ProRes (100GB)</text>

  <!-- S3 Raw Store -->
  <rect x="160" y="80" width="100" height="50" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="210" y="105" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">S3 Raw Bucket</text>
  <text x="210" y="118" fill="#94a3b8" font-size="7" text-anchor="middle">Multipart S3 Upload</text>

  <!-- DAG Orchestrator (Meson / Temporal) -->
  <rect x="300" y="60" width="140" height="90" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="370" y="88" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Transcoding DAG</text>
  <text x="370" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">Splits video into 5s chunks</text>
  <text x="370" y="120" fill="#38bdf8" font-size="7" text-anchor="middle">1000s parallel worker jobs</text>
  <text x="370" y="135" fill="#94a3b8" font-size="7" text-anchor="middle">Temporal / Netflix Meson</text>

  <!-- Worker Farm -->
  <rect x="480" y="30" width="130" height="40" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="545" y="55" fill="#34d399" font-size="8" text-anchor="middle">Worker 1: AV1 / 4K / 60fps</text>

  <rect x="480" y="85" width="130" height="40" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="545" y="110" fill="#34d399" font-size="8" text-anchor="middle">Worker 2: HEVC / 1080p</text>

  <rect x="480" y="140" width="130" height="40" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="545" y="165" fill="#34d399" font-size="8" text-anchor="middle">Worker N: H.264 / 720p / 360p</text>

  <!-- CDN & Open Connect Edge -->
  <rect x="650" y="60" width="130" height="90" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="715" y="88" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Open Connect CDN</text>
  <text x="715" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">Edge Cache inside ISP</text>
  <text x="715" y="120" fill="#38bdf8" font-size="7" text-anchor="middle">HLS .m3u8 Master Manifest</text>
  <text x="715" y="135" fill="#34d399" font-size="7" text-anchor="middle">98%+ Edge Cache Hit!</text>

  <!-- Client Playback -->
  <rect x="650" y="230" width="130" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="715" y="260" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Smart TV / Phone</text>
  <text x="715" y="275" fill="#38bdf8" font-size="8" text-anchor="middle">ABR dynamically switches bitrates</text>

  <!-- Connections -->
  <path d="M 120 105 L 160 105" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 260 105 L 300 105" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 440 90 L 480 50" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 440 105 L 480 105" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 440 120 L 480 160" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 610 105 L 650 105" stroke="#ec4899" stroke-width="2"/>
  <path d="M 715 150 L 715 230" stroke="#38bdf8" stroke-width="2"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Adaptive Bitrate Streaming (ABR) Mechanics</h5>
  <p>A 2-hour 4K movie is never sent as a single giant MP4 file. It is sliced into <strong>tens of thousands of 2-second to 6-second independent <code>.ts</code> or <code>.m4s</code> chunk files</strong> across 15+ different bitrates and codec combinations (H.264, AV1, VP9).</p>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li>The client player downloads the <code>master.m3u8</code> manifest file containing available bitrate streams.</li>
    <li>Every 2 seconds, the client inspects its buffer health and current Wi-Fi throughput. If Wi-Fi degrades, it requests the next 2-second chunk at 720p instead of 4K without pausing playback!</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-stripe",
        "title": "Blueprint 5: Financial Payment Gateway & Ledger (Stripe)",
        "badge": "Double-Entry Ledger & Idempotency",
        "scaleStats": {
            "uptime": "99.999% SLA (Five Nines)",
            "volume": "$1+ Trillion Processed Annually",
            "consistency": "Strict Serializability",
            "dataLossTolerance": "Absolute Zero ($0.00)"
        },
        "description": "Double-entry accounting, distributed idempotency keys with atomic reservation, and reconciliation engines.",
        "architectureSvg": """
<svg viewBox="0 0 800 320" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- Client Merchant -->
  <rect x="20" y="80" width="120" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="80" y="110" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Merchant Client</text>
  <text x="80" y="125" fill="#38bdf8" font-size="8" text-anchor="middle">Header: Idempotency-Key</text>

  <!-- API Gateway & Idempotency Layer -->
  <rect x="180" y="70" width="160" height="80" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="260" y="98" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Idempotency Interceptor</text>
  <text x="260" y="115" fill="#94a3b8" font-size="8" text-anchor="middle">Atomic Redis Lock on Key</text>
  <text x="260" y="130" fill="#f59e0b" font-size="7" text-anchor="middle">Returns cached response on replay</text>

  <!-- Payment Orchestrator -->
  <rect x="380" y="70" width="150" height="80" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="455" y="98" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Payment Core</text>
  <text x="455" y="115" fill="#94a3b8" font-size="8" text-anchor="middle">Card Tokenization &amp; Fraud</text>
  <text x="455" y="130" fill="#38bdf8" font-size="7" text-anchor="middle">Two-Phase Commit with Visa/Mastercard</text>

  <!-- Double Entry Ledger DB -->
  <rect x="580" y="50" width="190" height="110" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="675" y="80" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Double-Entry Immutable Ledger</text>
  <text x="675" y="98" fill="#94a3b8" font-size="8" text-anchor="middle">Sum(Debits) == Sum(Credits) &equiv; 0</text>
  <text x="675" y="112" fill="#34d399" font-size="8" text-anchor="middle">Append-Only / Never UPDATE</text>
  <text x="675" y="135" fill="#fbbf24" font-size="7" text-anchor="middle">PostgreSQL / Spanner Multi-Region</text>

  <!-- Daily Reconciliation Engine -->
  <rect x="380" y="210" width="390" height="70" rx="8" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>
  <text x="575" y="240" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Daily Automated Bank Reconciliation Batch Engine</text>
  <text x="575" y="258" fill="#94a3b8" font-size="8" text-anchor="middle">Matches internal ledger records against external bank clearing files (NACHA, SWIFT, SEPA)</text>

  <!-- Connections -->
  <path d="M 140 110 L 180 110" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 340 110 L 380 110" stroke="#10b981" stroke-width="2"/>
  <path d="M 530 110 L 580 110" stroke="#ec4899" stroke-width="2"/>
  <path d="M 675 160 L 675 210" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Double-Entry Bookkeeping Invariant</h5>
  <p>In financial systems, you NEVER write <code>UPDATE accounts SET balance = balance - 100</code>. That is an amateur anti-pattern that creates race conditions and impossible audit trails.</p>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>Every financial movement is an immutable pair of entries:</strong> 1 Debit and 1 Credit.</li>
    <li>When User A pays User B $100: User A's asset account is credited -$100, and User B's asset account is debited +$100.</li>
    <li>At any millisecond in time, the sum of all debits and credits across the entire platform must equal exactly 0. If it deviates by $0.00001, automated circuit breakers immediately freeze transactions and page on-call Staff engineers.</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-tinyurl",
        "title": "Blueprint 6: Planet-Scale URL Shortener (TinyURL / Bitly)",
        "badge": "Base62 & Key Generation",
        "scaleStats": {
            "writeQps": "1,000 New URLs / Sec",
            "readQps": "100,000 Redirects / Sec (100:1 Ratio)",
            "storage": "3.5 Trillion URLs (7-Char Base62)",
            "latency": "< 10ms Redirect P99"
        },
        "description": "Base62 encoding, pre-computed Key Generation Service (KGS) eliminating database write lock contention, and 301 vs 302 HTTP redirect trade-offs.",
        "architectureSvg": """
<svg viewBox="0 0 800 320" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="80" width="110" height="50" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="85" y="105" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Client Browser</text>
  <text x="85" y="118" fill="#94a3b8" font-size="7" text-anchor="middle">GET /x8A9k1</text>

  <!-- GeoDNS / Cloudflare CDN Edge -->
  <rect x="180" y="70" width="140" height="70" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="250" y="98" fill="#22d3ee" font-size="11" font-weight="bold" text-anchor="middle">Cloudflare CDN Edge</text>
  <text x="250" y="115" fill="#94a3b8" font-size="8" text-anchor="middle">95%+ Hot Redirects Cached</text>
  <text x="250" y="128" fill="#10b981" font-size="7" text-anchor="middle">Returns 301/302 in &lt;5ms</text>

  <!-- Application Web Cluster -->
  <rect x="370" y="70" width="140" height="70" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="440" y="98" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Redirect Service</text>
  <text x="440" y="115" fill="#94a3b8" font-size="8" text-anchor="middle">Stateless Go/Rust Workers</text>

  <!-- Redis Cache -->
  <rect x="560" y="40" width="160" height="60" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="640" y="68" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Redis L2 Cache</text>
  <text x="640" y="85" fill="#94a3b8" font-size="8" text-anchor="middle">Stores Top 20% Active URLs</text>

  <!-- Key Generation Service (KGS) -->
  <rect x="370" y="190" width="140" height="80" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <text x="440" y="218" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Key Gen Service (KGS)</text>
  <text x="440" y="235" fill="#94a3b8" font-size="8" text-anchor="middle">Pre-generates 7-char keys</text>
  <text x="440" y="250" fill="#38bdf8" font-size="7" text-anchor="middle">Zero runtime collision overhead</text>

  <!-- Primary DB (DynamoDB / Cassandra) -->
  <rect x="560" y="150" width="160" height="80" rx="6" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="640" y="180" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">DynamoDB / NoSQL</text>
  <text x="640" y="198" fill="#94a3b8" font-size="8" text-anchor="middle">Key: short_hash (Partition)</text>
  <text x="640" y="212" fill="#94a3b8" font-size="7" text-anchor="middle">Value: original_url, created_at</text>

  <!-- Connections -->
  <path d="M 140 105 L 180 105" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 320 105 L 370 105" stroke="#06b6d4" stroke-width="1.5"/>
  <path d="M 510 90 L 560 70" stroke="#10b981" stroke-width="1.5"/>
  <path d="M 510 115 L 560 170" stroke="#ec4899" stroke-width="1.5"/>
  <path d="M 440 190 L 440 140" stroke="#f59e0b" stroke-width="1.5"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">HTTP 301 vs 302: The Interview Trap</h5>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>301 Moved Permanently:</strong> The browser caches the redirect forever. Subsequent clicks NEVER hit your servers. <em>Pros:</em> Zero server load. <em>Cons:</em> You cannot track click analytics or revoke the URL!</li>
    <li><strong>302 Found (or 307 Temporary):</strong> The browser always hits your server first before redirecting. <em>Pros:</em> Real-time click analytics, geolocation tracking, device routing. <em>Cons:</em> Higher server load. Production standard is 302 with short CDN edge caching.</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-dynamo",
        "title": "Blueprint 7: Distributed Key-Value Store (Amazon Dynamo Architecture)",
        "badge": "Sloppy Quorum & Merkle Trees",
        "scaleStats": {
            "p999Latency": "< 10ms SLA for Amazon Shopping Cart",
            "availability": "100% Always-Writable Shopping Cart",
            "partitionTolerance": "Multi-Rack Split Survival",
            "consensus": "Vector Clocks + Merkle Anti-Entropy"
        },
        "description": "The seminal Amazon Dynamo paper decomposed: Consistent hashing rings, Sloppy Quorums ($R + W > N$), Hinted Handoff, and Merkle tree sync.",
        "architectureSvg": """
<svg viewBox="0 0 800 320" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <circle cx="220" cy="160" r="110" fill="none" stroke="#334155" stroke-width="4" stroke-dasharray="6"/>
  <circle cx="220" cy="50" r="14" fill="#38bdf8"/>
  <text x="220" y="54" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">N1</text>

  <circle cx="330" cy="160" r="14" fill="#10b981"/>
  <text x="330" y="164" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">N2</text>

  <circle cx="220" cy="270" r="14" fill="#f59e0b"/>
  <text x="220" y="274" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">N3</text>

  <circle cx="110" cy="160" r="14" fill="#ec4899"/>
  <text x="110" y="164" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">N4</text>

  <text x="220" y="155" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Consistent Hash Ring</text>
  <text x="220" y="172" fill="#94a3b8" font-size="9" text-anchor="middle">Preference List (N=3)</text>

  <!-- Right Details -->
  <rect x="420" y="40" width="350" height="70" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="435" y="65" fill="#38bdf8" font-size="11" font-weight="bold">Quorum Consensus Formula: R + W &gt; N</text>
  <text x="435" y="82" fill="#94a3b8" font-size="9">If N=3 replicas, set W=2 (writes ACKed by 2) and R=2 (reads query 2).</text>
  <text x="435" y="96" fill="#34d399" font-size="8 font-mono">Guarantees read and write quorums overlap by at least 1 node!</text>

  <rect x="420" y="125" width="350" height="75" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="435" y="150" fill="#fbbf24" font-size="11" font-weight="bold">Hinted Handoff: Always-Writable Design</text>
  <text x="435" y="167" fill="#94a3b8" font-size="9">If Node N2 is down, write is accepted by healthy Node N4 with a "hint".</text>
  <text x="435" y="182" fill="#94a3b8" font-size="8">Once N2 recovers, N4 forwards the buffered write back to N2.</text>

  <rect x="420" y="215" width="350" height="75" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="1.5"/>
  <text x="435" y="240" fill="#f472b6" font-size="11" font-weight="bold">Anti-Entropy via Merkle Trees</text>
  <text x="435" y="257" fill="#94a3b8" font-size="9">Replicas synchronize key ranges using hierarchical hash trees.</text>
  <text x="435" y="272" fill="#94a3b8" font-size="8">Detects out-of-sync key ranges in O(log N) without transferring entire dataset.</text>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why Amazon Sacrificed Consistency for the Shopping Cart</h5>
  <p>In Amazon's early days, losing an item from a shopping cart meant lost revenue. Amazon's founders declared: <em>The shopping cart must always accept writes, even if datacenters are disconnected from each other.</em></p>
  <p>If two disconnected nodes accept concurrent updates to the same cart (e.g. adding socks vs adding a book), Dynamo uses <strong>Vector Clocks</strong> to capture causal relationships. On read, if concurrent branches exist, Dynamo preserves both and lets the client application reconcile the union (you see both items rather than losing one!).</p>
</div>
"""
    },
    {
        "id": "blueprint-spanner",
        "title": "Blueprint 8: Planet-Scale Distributed SQL (Google Spanner / CockroachDB)",
        "badge": "TrueTime & External Consistency",
        "scaleStats": {
            "scope": "Global Multi-Continent Sharding",
            "consistency": "Strict Serializability",
            "transactionEngine": "2PC + Multi-Paxos per Range",
            "timeSync": "TrueTime Atomic Clocks + GPS (< 7ms error)"
        },
        "description": "How Google solved cross-datacenter ACID transactions without locks on reads using atomic clocks and the TrueTime API.",
        "architectureSvg": """
<svg viewBox="0 0 800 320" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- Datacenter A -->
  <rect x="40" y="60" width="200" height="220" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="140" y="90" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Region: US-East</text>
  
  <rect x="60" y="110" width="160" height="50" rx="6" fill="#1e293b" stroke="#f59e0b"/>
  <text x="140" y="132" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">TrueTime Master</text>
  <text x="140" y="147" fill="#94a3b8" font-size="7" text-anchor="middle">GPS Receiver + Rubidium Clock</text>

  <rect x="60" y="180" width="160" height="70" rx="6" fill="#1e293b" stroke="#34d399"/>
  <text x="140" y="205" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">Paxos Group Leader</text>
  <text x="140" y="222" fill="#94a3b8" font-size="8" text-anchor="middle">Range: [User_000, User_500)</text>

  <!-- Datacenter B -->
  <rect x="300" y="60" width="200" height="220" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="400" y="90" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Region: Europe-West</text>

  <rect x="320" y="110" width="160" height="50" rx="6" fill="#1e293b" stroke="#f59e0b"/>
  <text x="400" y="132" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">TrueTime Master</text>
  <text x="400" y="147" fill="#94a3b8" font-size="7" text-anchor="middle">GPS Receiver + Rubidium Clock</text>

  <rect x="320" y="180" width="160" height="70" rx="6" fill="#1e293b" stroke="#a855f7"/>
  <text x="400" y="205" fill="#c084fc" font-size="10" font-weight="bold" text-anchor="middle">Paxos Replica</text>
  <text x="400" y="222" fill="#94a3b8" font-size="8" text-anchor="middle">Replicates via Paxos Log</text>

  <!-- Right Explanation Card -->
  <rect x="540" y="60" width="230" height="220" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
  <text x="655" y="90" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">TrueTime Commit Wait Rule</text>
  <foreignObject x="555" y="105" width="200" height="160">
    <div xmlns="http://www.w3.org/1999/xhtml" class="text-[10px] text-slate-300 space-y-2">
      <p>TrueTime API returns a time interval <code>[earliest, latest]</code> where error bound $\epsilon \le 7\text{ ms}$.</p>
      <p><strong>Commit Wait:</strong> When writing, the leader picks timestamp $s = \text{latest}$. It pauses the commit until TrueTime guarantees that absolute real time has passed $s$ ($2 \times \epsilon$).</p>
      <p class="text-emerald-400 font-bold">Result: Globally linearizable ACID transactions across continents without locking reads!</p>
    </div>
  </foreignObject>

  <!-- Connections -->
  <path d="M 220 215 L 320 215" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why NTP Is Broken for Distributed Transactions</h5>
  <p>Standard Network Time Protocol (NTP) over the public internet experiences 100ms to 500ms of clock drift and asymmetric network delays. You cannot know if event A happened before event B across datacenters. Google installed GPS antennas and atomic rubidium clocks in every single datacenter rack, bounding time uncertainty to $\pm 1-7\text{ ms}$, creating the world's first globally consistent distributed SQL database.</p>
</div>
"""
    },
    {
        "id": "blueprint-search",
        "title": "Blueprint 9: Web Crawler & Search Inverted Index (Google Search)",
        "badge": "Inverted Index & PageRank",
        "scaleStats": {
            "indexedPages": "100+ Billion Web Pages",
            "crawlThroughput": "Millions of Pages / Sec",
            "searchQps": "100,000+ Queries / Sec",
            "queryLatency": "< 200ms Complete SERP"
        },
        "description": "Distributed URL frontier, politeness queues, SimHash near-duplicate detection, and distributed inverted index posting lists.",
        "architectureSvg": """
<svg viewBox="0 0 800 300" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- URL Frontier -->
  <rect x="30" y="60" width="130" height="80" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="95" y="88" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">URL Frontier</text>
  <text x="95" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">Politeness &amp; Priority</text>
  <text x="95" y="120" fill="#94a3b8" font-size="7" text-anchor="middle">1 host per worker queue</text>

  <!-- Distributed Crawler Workers -->
  <rect x="220" y="60" width="130" height="80" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="285" y="88" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Crawler Workers</text>
  <text x="285" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">Async DNS + HTTP Fetch</text>
  <text x="285" y="120" fill="#fbbf24" font-size="7" text-anchor="middle">SimHash Deduplication</text>

  <!-- Document Processing & Parser -->
  <rect x="410" y="60" width="140" height="80" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="480" y="88" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Content Extractor</text>
  <text x="480" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">HTML Clean, Tokenization</text>
  <text x="480" y="120" fill="#38bdf8" font-size="7" text-anchor="middle">Stemming &amp; Stopwords</text>

  <!-- Distributed Inverted Index -->
  <rect x="610" y="40" width="160" height="120" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="690" y="68" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Inverted Index</text>
  <text x="690" y="85" fill="#94a3b8" font-size="8" text-anchor="middle">"system" &rarr; [Doc1, Doc8...]</text>
  <text x="690" y="98" fill="#94a3b8" font-size="8" text-anchor="middle">"design" &rarr; [Doc1, Doc14...]</text>
  <text x="690" y="125" fill="#10b981" font-size="8" text-anchor="middle">Intersect Posting Lists</text>

  <!-- Search Serving Cluster -->
  <rect x="410" y="190" width="360" height="70" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="590" y="218" fill="#22d3ee" font-size="11" font-weight="bold" text-anchor="middle">Search Serving Tier &amp; Ranker (PageRank + RankBrain ML)</text>
  <text x="590" y="235" fill="#94a3b8" font-size="8" text-anchor="middle">Scattered across 10,000 query nodes; Gathers top-k results in parallel in &lt;50ms</text>

  <!-- Connections -->
  <path d="M 160 100 L 220 100" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 350 100 L 410 100" stroke="#10b981" stroke-width="2"/>
  <path d="M 550 100 L 610 100" stroke="#a855f7" stroke-width="2"/>
  <path d="M 690 160 L 690 190" stroke="#ec4899" stroke-width="2"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Posting List Intersection at Microsecond Latency</h5>
  <p>An Inverted Index maps each word to a sorted list of Document IDs where it appears (a <strong>Posting List</strong>). When a user searches for <code>"system design"</code>:</p>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li>The query node fetches the posting list for <code>"system"</code> and <code>"design"</code>.</li>
    <li>It performs a fast two-pointer intersection or vectorized SIMD leapfrog join to find documents containing both words.</li>
    <li>Results are ranked using BM25 relevance score combined with global PageRank authority scores.</li>
  </ul>
</div>
"""
    },
    {
        "id": "blueprint-vector-rag",
        "title": "Blueprint 10: Vector Search & AI RAG Engine (Milvus / Pinecone / vLLM)",
        "badge": "Vector DB & LLM Serving",
        "scaleStats": {
            "embeddingDimensions": "1,536 (OpenAI / Gemini)",
            "vectorCount": "100 Million+ Embeddings",
            "searchLatency": "< 15ms ANN Search",
            "indexingAlgorithm": "HNSW (Hierarchical Small World)"
        },
        "description": "Modern generative AI infrastructure: Approximate Nearest Neighbor (ANN) vector search, HNSW graphs, and high-throughput vLLM PagedAttention KV cache serving.",
        "architectureSvg": """
<svg viewBox="0 0 800 320" class="w-full h-auto bg-slate-950 rounded-xl p-4 border border-slate-800" xmlns="http://www.w3.org/2000/svg">
  <!-- User Query -->
  <rect x="20" y="80" width="110" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="75" y="110" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">User Prompt</text>
  <text x="75" y="125" fill="#38bdf8" font-size="8" text-anchor="middle">"How does Raft work?"</text>

  <!-- Embedding Model -->
  <rect x="170" y="80" width="130" height="60" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="235" y="105" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Embedding Model</text>
  <text x="235" y="122" fill="#94a3b8" font-size="8" text-anchor="middle">Float32[1536] Vector</text>

  <!-- Vector Database (Milvus / Pinecone) -->
  <rect x="350" y="60" width="180" height="100" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="440" y="88" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Vector DB (HNSW Index)</text>
  <text x="440" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">Multi-layer Skip-list Graph</text>
  <text x="440" y="120" fill="#fbbf24" font-size="8" text-anchor="middle">Cosine Distance / Dot Product</text>
  <text x="440" y="138" fill="#38bdf8" font-size="7" text-anchor="middle">Top-K Most Relevant Context Chunks</text>

  <!-- LLM Serving Cluster (vLLM) -->
  <rect x="580" y="60" width="190" height="100" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="675" y="88" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">vLLM Inference Cluster</text>
  <text x="675" y="105" fill="#94a3b8" font-size="8" text-anchor="middle">PagedAttention (Zero Waste)</text>
  <text x="675" y="120" fill="#38bdf8" font-size="8" text-anchor="middle">Continuous Batching</text>
  <text x="675" y="138" fill="#34d399" font-size="7" text-anchor="middle">Streams Tokens via SSE to Client</text>

  <!-- Hybrid Search Filter -->
  <rect x="350" y="190" width="420" height="80" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
  <text x="560" y="218" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Enterprise Hybrid Search: Dense Vector + Sparse BM25 + Metadata Filters</text>
  <text x="560" y="235" fill="#94a3b8" font-size="8" text-anchor="middle">Combines semantic meaning (embeddings) with exact keyword matching and tenant/ACL security filtering</text>
  <text x="560" y="252" fill="#a855f7" font-size="7 font-mono" text-anchor="middle">WHERE tenant_id = 'org_992' AND published_year &gt;= 2024</text>

  <!-- Connections -->
  <path d="M 130 110 L 170 110" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 300 110 L 350 110" stroke="#a855f7" stroke-width="2"/>
  <path d="M 530 110 L 580 110" stroke="#10b981" stroke-width="2"/>
</svg>
""",
        "technicalDeepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why vLLM PagedAttention Changed LLM Serving</h5>
  <p>In traditional LLM serving, GPU High Bandwidth Memory (HBM) is fragmented and wasted because key-value (KV) caches are pre-allocated for worst-case sequence lengths (e.g. 4,096 tokens), leaving up to <strong>60-80% of GPU memory unused</strong>.</p>
  <ul class="list-disc list-inside space-y-1 ml-2">
    <li><strong>PagedAttention</strong> borrows the virtual memory paging concept from operating systems. It stores KV caches in non-contiguous memory blocks.</li>
    <li>This allows dynamic allocation of token memory with virtually 0% internal fragmentation, enabling <strong>4x to 8x higher batch sizes and throughput</strong> on NVIDIA H100 GPUs!</li>
  </ul>
</div>
"""
    }
]

print(f"Loaded {len(BLUEPRINTS)} God-Level Blueprints.")
