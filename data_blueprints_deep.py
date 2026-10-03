# data_blueprints_deep.py
# The 12 Complete Production Blueprints for Staff & Principal Systems Architects

BLUEPRINTS = [
    {
        "id": "bp-stripe",
        "num": "01",
        "title": "Stripe: Financial Payment Gateway & Immutable Double-Entry Ledger",
        "tagline": "How to process $1+ Trillion with 99.999% SLA, strict idempotency, and zero financial data loss.",
        "badge": "Fintech & Ledgers",
        "stats": {
            "uptime": "99.999% SLA (Five Nines)",
            "annualVolume": "$1+ Trillion / Year",
            "consistency": "Strict Serializability",
            "dataLossTolerance": "$0.00 (Zero Tolerance)"
        },
        "svg": """
<svg viewBox="0 0 760 300" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="70" width="110" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="75" y="98" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Merchant Client</text>
  <text x="75" y="112" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Idempotency-Key</text>

  <rect x="170" y="60" width="150" height="75" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="245" y="88" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Idempotency Gate</text>
  <text x="245" y="104" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Atomic Redis Lock</text>
  <text x="245" y="118" fill="#fbbf24" font-size="7" font-family="monospace" text-anchor="middle">Cached replay in &lt;5ms</text>

  <rect x="360" y="60" width="160" height="75" rx="10" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="440" y="88" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Payment Core</text>
  <text x="440" y="104" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Tokenize &amp; Fraud Score</text>
  <text x="440" y="118" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">2PC with Card Networks</text>

  <rect x="560" y="65" width="170" height="65" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="645" y="95" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Visa / Mastercard / Banks</text>
  <text x="645" y="110" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">ISO 8583 Protocol</text>

  <rect x="220" y="180" width="300" height="85" rx="10" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="370" y="208" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Immutable Double-Entry Ledger DB</text>
  <text x="370" y="225" fill="#34d399" font-size="9" font-family="monospace" text-anchor="middle">SUM(Debits) == SUM(Credits) &equiv; 0</text>
  <text x="370" y="240" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">PostgreSQL / Spanner Multi-AZ &bull; Append-Only</text>

  <path d="M 130 98 L 170 98" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 320 98 L 360 98" stroke="#10b981" stroke-width="2"/>
  <path d="M 520 98 L 560 98" stroke="#f59e0b" stroke-width="2"/>
  <path d="M 440 135 L 440 180" stroke="#ec4899" stroke-width="2"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">The Double-Entry Accounting Invariant</h5>
  <p>In financial engineering, balance is not a column; <strong>balance is a computed view</strong> derived from an immutable stream of ledger postings. Every transaction contains at least two entries: one debit and one credit.</p>
  <div class="p-3 rounded-lg bg-slate-950 font-mono text-[11px] text-cyan-300 border border-slate-800">
    -- The Fundamental Ledger Transaction Invariant<br/>
    INSERT INTO ledger_postings (entry_id, tx_id, account_id, amount_cents, direction)<br/>
    VALUES <br/>
    &nbsp;&nbsp;('ent_01', 'tx_991', 'user_checking_act', -10000, 'DEBIT'),<br/>
    &nbsp;&nbsp;('ent_02', 'tx_991', 'merchant_settlement_act', +9710, 'CREDIT'),<br/>
    &nbsp;&nbsp;('ent_03', 'tx_991', 'stripe_revenue_fee', +290, 'CREDIT');<br/>
    -- Balance Check: (-10000) + 9710 + 290 = 0.00
  </div>
</div>
"""
    },
    {
        "id": "bp-twitter",
        "num": "02",
        "title": "X / Twitter: Planet-Scale Real-Time Social Graph & Timeline Feed",
        "tagline": "Solving the 100M celebrity fanout problem with hybrid push-pull timeline materialization.",
        "badge": "Social Graph",
        "stats": {
            "dau": "500 Million DAU",
            "readQps": "350,000 QPS (Home Timelines)",
            "writeQps": "15,000 Tweets / Sec",
            "p99Latency": "< 30ms Timeline Load"
        },
        "svg": """
<svg viewBox="0 0 760 300" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="120" width="100" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="148" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Client App</text>
  <text x="70" y="162" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">GET /timeline</text>

  <rect x="160" y="115" width="100" height="65" rx="8" fill="#0f172a" stroke="#6366f1" stroke-width="1.5"/>
  <text x="210" y="145" fill="#818cf8" font-size="11" font-weight="bold" text-anchor="middle">Envoy Proxy</text>
  <text x="210" y="160" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Auth &amp; RateLimit</text>

  <rect x="300" y="45" width="140" height="65" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="370" y="75" fill="#22d3ee" font-size="11" font-weight="bold" text-anchor="middle">Push Fanout Engine</text>
  <text x="370" y="90" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Followers &lt; 25k (Redis List)</text>

  <rect x="300" y="180" width="140" height="65" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="370" y="210" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Timeline Aggregator</text>
  <text x="370" y="225" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Celebrities &gt; 25k (Pull Merge)</text>

  <rect x="490" y="35" width="130" height="55" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="555" y="62" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Redis Clusters</text>
  <text x="555" y="78" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Pre-computed Lists</text>

  <rect x="490" y="120" width="130" height="55" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="555" y="148" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">FlockDB Graph</text>
  <text x="555" y="162" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Follower Edges</text>

  <rect x="490" y="200" width="130" height="55" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="1.5"/>
  <text x="555" y="228" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Manhattan DB</text>
  <text x="555" y="242" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Tweet RocksDB</text>

  <path d="M 120 148 L 160 148" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 260 140 L 300 80" stroke="#06b6d4" stroke-width="1.5"/>
  <path d="M 260 155 L 300 210" stroke="#a855f7" stroke-width="1.5"/>
  <path d="M 440 80 L 490 65" stroke="#10b981" stroke-width="1.5"/>
  <path d="M 440 90 L 490 140" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 440 215 L 490 150" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 440 230 L 490 230" stroke="#ec4899" stroke-width="1.5"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Hybrid Timeline Materialization Strategy</h5>
  <p>Standard users (&lt;25,000 followers) use <strong>Fanout-on-Write (Push)</strong>, inserting tweet IDs into followers' Redis lists for instant O(1) reads. Celebrities (&gt;25,000 followers) use <strong>Fanout-on-Read (Pull)</strong>, merging dynamically on feed scroll to avoid blowing up write IOPS.</p>
</div>
"""
    },
    {
        "id": "bp-whatsapp",
        "num": "03",
        "title": "WhatsApp: Ultra-Low Latency Messaging & Erlang BEAM Broker",
        "tagline": "How 2 Billion users exchange 100 Billion messages daily with ephemeral storage.",
        "badge": "Real-Time Sockets",
        "stats": {
            "dau": "2+ Billion DAU",
            "dailyMessages": "100+ Billion Messages / Day",
            "concurrentSockets": "100 Million Active WebSockets",
            "p99Latency": "< 40ms Delivery"
        },
        "svg": """
<svg viewBox="0 0 760 280" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="100" height="50" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="85" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Alice (Sender)</text>
  <text x="70" y="98" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">Signal Protocol</text>

  <rect x="20" y="170" width="100" height="50" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="195" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Bob (Receiver)</text>
  <text x="70" y="208" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">Signal Protocol</text>

  <rect x="170" y="45" width="180" height="190" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="260" y="72" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">Erlang BEAM Gateways</text>
  <text x="260" y="86" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">2M Conns / Node</text>

  <rect x="190" y="100" width="140" height="32" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="260" y="120" fill="#f8fafc" font-size="8" font-family="monospace" text-anchor="middle">Alice Session Actor</text>

  <rect x="190" y="150" width="140" height="32" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="260" y="170" fill="#f8fafc" font-size="8" font-family="monospace" text-anchor="middle">Bob Session Actor</text>

  <rect x="400" y="55" width="150" height="65" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="475" y="82" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Session Router (Mnesia)</text>
  <text x="475" y="98" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">UserID &rarr; Gateway IP</text>

  <rect x="400" y="165" width="150" height="65" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="475" y="192" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Offline Queue (Spanner)</text>
  <text x="475" y="208" fill="#ef4444" font-size="8" font-family="monospace" text-anchor="middle">Auto-purged on Delivery</text>

  <path d="M 120 85 L 190 115" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 330 115 L 400 85" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 330 165 L 120 195" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 330 165 L 400 195" stroke="#ec4899" stroke-width="1.5"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Ephemeral Broker Architecture</h5>
  <p>WhatsApp stores zero message text permanently on disk. The instant Bob's client sends an ACK receipt, the message is permanently expunged from the database.</p>
</div>
"""
    },
    {
        "id": "bp-uber",
        "num": "04",
        "title": "Uber: Real-Time Geospatial Driver Dispatch & Hexagonal H3 Indexing",
        "tagline": "How to ingest 1.25M GPS pings per second and calculate optimal supply matching in &lt; 500ms.",
        "badge": "Geospatial Indexing",
        "stats": {
            "activeDrivers": "5 Million Concurrent Drivers",
            "pingRate": "Every 4 Seconds per Driver",
            "ingestThroughput": "1,250,000 GPS Pings / Sec",
            "matchingLatency": "< 500ms P99"
        },
        "svg": """
<svg viewBox="0 0 760 280" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="55" width="110" height="50" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="75" y="80" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Driver App</text>
  <text x="75" y="94" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">gRPC Ping (Lat, Lng)</text>

  <rect x="170" y="50" width="130" height="60" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="235" y="78" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">H3 Indexer</text>
  <text x="235" y="94" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Lat/Lng &rarr; H3 Hex Cell</text>

  <rect x="340" y="50" width="140" height="60" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="410" y="78" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Kafka H3 Stream</text>
  <text x="410" y="94" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Partitioned by City/Cell</text>

  <rect x="520" y="40" width="220" height="80" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="630" y="70" fill="#22d3ee" font-size="12" font-weight="bold" text-anchor="middle">In-Memory Location Service</text>
  <text x="630" y="88" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">H3 Cell &rarr; Set&lt;DriverID&gt;</text>
  <text x="630" y="102" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Sub-ms Concentric K-Ring Search</text>

  <rect x="20" y="165" width="110" height="50" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="75" y="190" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Rider App</text>
  <text x="75" y="204" fill="#c084fc" font-size="7" font-family="monospace" text-anchor="middle">Request Ride</text>

  <rect x="240" y="160" width="240" height="60" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="188" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Dispatch &amp; Dynamic Matcher</text>
  <text x="360" y="204" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Queries K-Rings &bull; ETA &bull; Surge Pricing</text>

  <path d="M 130 80 L 170 80" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 300 80 L 340 80" stroke="#10b981" stroke-width="2"/>
  <path d="M 480 80 L 520 80" stroke="#ec4899" stroke-width="2"/>
  <path d="M 130 190 L 240 190" stroke="#a855f7" stroke-width="2"/>
  <path d="M 480 190 L 630 120" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Hexagons vs Squares & Geohash</h5>
  <p>In a hexagonal grid (Uber H3), all 6 neighbors share identical edge lengths and center-to-center distances, allowing clean O(1) concentric K-ring radius expansions without spherical distortion.</p>
</div>
"""
    },
    {
        "id": "bp-netflix",
        "num": "05",
        "title": "Netflix: Video Transcoding DAG & Open Connect CDN Appliances",
        "tagline": "How Netflix delivers 15%+ of downstream Internet traffic with 98% ISP cache hits.",
        "badge": "Video & CDN Edge",
        "stats": {
            "traffic": "15%+ Global Internet Downstream",
            "edgeServers": "18,000+ Open Connect Appliances",
            "protocols": "HLS & MPEG-DASH Adaptive Bitrate",
            "cacheHit": "98.5% Edge ISP Cache Hit"
        },
        "svg": """
<svg viewBox="0 0 760 280" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="100" height="50" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="70" y="85" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Studio Master</text>
  <text x="70" y="98" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">ProRes 4K (500GB)</text>

  <rect x="160" y="55" width="140" height="60" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="230" y="82" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Chunking DAG</text>
  <text x="230" y="98" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">2s - 6s Independent Segments</text>

  <rect x="340" y="30" width="130" height="35" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="405" y="52" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">Worker 1: AV1 / 4K / 60fps</text>

  <rect x="340" y="75" width="130" height="35" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="405" y="97" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">Worker 2: HEVC / 1080p</text>

  <rect x="340" y="120" width="130" height="35" rx="4" fill="#1e293b" stroke="#34d399"/>
  <text x="405" y="142" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">Worker N: H.264 / 720p</text>

  <rect x="510" y="45" width="220" height="80" rx="10" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="620" y="75" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Open Connect CDN Edge</text>
  <text x="620" y="92" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Hardware deployed directly inside ISP</text>
  <text x="620" y="106" fill="#34d399" font-size="7" font-family="monospace" text-anchor="middle">Zero transit cost &bull; 98.5% cache hit</text>

  <rect x="550" y="180" width="140" height="50" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="620" y="205" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Smart TV Client</text>
  <text x="620" y="220" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Adaptive Bitrate (ABR)</text>

  <path d="M 120 85 L 160 85" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 300 75 L 340 48" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 300 85 L 340 92" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 300 95 L 340 138" stroke="#34d399" stroke-width="1.5"/>
  <path d="M 470 85 L 510 85" stroke="#ec4899" stroke-width="2"/>
  <path d="M 620 125 L 620 180" stroke="#38bdf8" stroke-width="2"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Adaptive Bitrate Streaming (ABR)</h5>
  <p>The client fetches a <code>manifest.m3u8</code> describing chunk options. Every 2 seconds, the client measures buffer health and throughput, seamlessly upgrading from 720p to 4K without pausing video.</p>
</div>
"""
    },
    {
        "id": "bp-spanner",
        "num": "06",
        "title": "Google Spanner: TrueTime & Planet-Scale Distributed SQL",
        "tagline": "How atomic clocks and GPS enable globally linearizable ACID transactions across continents.",
        "badge": "Distributed SQL",
        "stats": {
            "consistency": "Strict Serializability",
            "timeSync": "TrueTime Atomic Clocks + GPS",
            "uncertaintyBound": "&epsilon; &le; 7 ms",
            "readLocks": "Zero Read Locks (Snapshot MVCC)"
        },
        "svg": """
<svg viewBox="0 0 760 260" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="45" width="200" height="170" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="130" y="75" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Region: US-East</text>
  <rect x="50" y="90" width="160" height="40" rx="6" fill="#1e293b" stroke="#f59e0b"/>
  <text x="130" y="115" fill="#fbbf24" font-size="9" font-weight="bold" text-anchor="middle">TrueTime Master (GPS + Rubidium)</text>
  <rect x="50" y="145" width="160" height="50" rx="6" fill="#1e293b" stroke="#34d399"/>
  <text x="130" y="170" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">Paxos Group Leader</text>
  <text x="130" y="185" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Range: [User_000, User_500)</text>

  <rect x="270" y="45" width="200" height="170" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="370" y="75" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Region: Europe-West</text>
  <rect x="290" y="90" width="160" height="40" rx="6" fill="#1e293b" stroke="#f59e0b"/>
  <text x="370" y="115" fill="#fbbf24" font-size="9" font-weight="bold" text-anchor="middle">TrueTime Master (GPS + Rubidium)</text>
  <rect x="290" y="145" width="160" height="50" rx="6" fill="#1e293b" stroke="#a855f7"/>
  <text x="370" y="170" fill="#c084fc" font-size="10" font-weight="bold" text-anchor="middle">Paxos Follower Replica</text>
  <text x="370" y="185" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Replicates via Paxos Log</text>

  <rect x="510" y="45" width="220" height="170" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="620" y="75" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">TrueTime Commit-Wait Rule</text>
  <foreignObject x="525" y="90" width="190" height="115">
    <div xmlns="http://www.w3.org/1999/xhtml" class="text-[10px] text-slate-300 space-y-2">
      <p>TrueTime returns interval <code>[t.earliest, t.latest]</code> where uncertainty $\epsilon \le 7\text{ ms}$.</p>
      <p><strong>Commit-Wait:</strong> The write transaction leader assigns timestamp $s = \text{latest}$ and waits until absolute time has passed $s$, guaranteeing global external consistency across continents without locking reads!</p>
    </div>
  </foreignObject>

  <path d="M 210 170 L 290 170" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why NTP Fails for Planet-Scale SQL</h5>
  <p>Standard NTP drifts by 100ms-500ms over the internet. Google installed atomic rubidium clocks and GPS receivers in every datacenter rack to guarantee $\epsilon \le 7\text{ ms}$, creating the world's first globally linearizable SQL database.</p>
</div>
"""
    },
    {
        "id": "bp-tinyurl",
        "num": "07",
        "title": "TinyURL / Bitly: Global URL Shortener & Analytics Ingestion",
        "tagline": "Base62 pre-computed Key Generation Service (KGS) eliminating database lock contention.",
        "badge": "Base62 & KGS",
        "stats": {
            "capacity": "3.5 Trillion URLs (7-Char Base62)",
            "readWriteRatio": "100 : 1 Read Heavy",
            "redirectLatency": "< 5 ms Edge P99",
            "httpCode": "302 Found vs 301 Permanent"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="100" height="50" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="85" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Browser Client</text>
  <text x="70" y="98" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">GET /x8A9k1</text>

  <rect x="160" y="50" width="130" height="65" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="225" y="78" fill="#22d3ee" font-size="11" font-weight="bold" text-anchor="middle">Cloudflare CDN Edge</text>
  <text x="225" y="94" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">95% Cached &bull; &lt;5ms</text>

  <rect x="330" y="50" width="130" height="65" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="395" y="78" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Redirect Service</text>
  <text x="395" y="94" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Stateless Go Workers</text>

  <rect x="500" y="30" width="140" height="50" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="570" y="55" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">Redis L2 Cache</text>
  <text x="570" y="68" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Top 20% Active URLs</text>

  <rect x="500" y="95" width="140" height="55" rx="6" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="570" y="122" fill="#f472b6" font-size="10" font-weight="bold" text-anchor="middle">DynamoDB Store</text>
  <text x="570" y="136" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Key: short_hash</text>

  <rect x="330" y="150" width="130" height="65" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <text x="395" y="178" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Key Gen Service (KGS)</text>
  <text x="395" y="194" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Pre-computes Base62</text>

  <path d="M 120 85 L 160 85" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 290 85 L 330 85" stroke="#06b6d4" stroke-width="1.5"/>
  <path d="M 460 70 L 500 55" stroke="#10b981" stroke-width="1.5"/>
  <path d="M 460 95 L 500 120" stroke="#ec4899" stroke-width="1.5"/>
  <path d="M 395 150 L 395 115" stroke="#f59e0b" stroke-width="1.5"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why Hash At Runtime Causes Write Lock Contention</h5>
  <p>Calculating MD5 or MurmurHash and checking for collisions at write time requires looping and database locks. <strong>KGS (Key Generation Service)</strong> pre-generates billions of unique 7-character Base62 keys in a background batch worker. When a user requests a short URL, KGS simply assigns the next available key in O(1) time without collisions!</p>
</div>
"""
    },
    {
        "id": "bp-dynamo",
        "num": "08",
        "title": "Amazon DynamoDB: Sloppy Quorums & Merkle Anti-Entropy",
        "tagline": "How Amazon guarantees an always-writable shopping cart with sloppy quorums ($R + W > N$).",
        "badge": "NoSQL Quorums",
        "stats": {
            "p99Latency": "< 10 ms SLA Globally",
            "availability": "100% Always-Writable",
            "quorumFormula": "R + W > N",
            "antiEntropy": "Hierarchical Merkle Trees"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <circle cx="180" cy="125" r="85" fill="none" stroke="#334155" stroke-width="4" stroke-dasharray="5"/>
  <circle cx="180" cy="40" r="12" fill="#38bdf8"/>
  <text x="180" y="44" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">N1</text>
  <circle cx="265" cy="125" r="12" fill="#10b981"/>
  <text x="265" y="129" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">N2</text>
  <circle cx="180" cy="210" r="12" fill="#f59e0b"/>
  <text x="180" y="214" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">N3</text>
  <circle cx="95" cy="125" r="12" fill="#ec4899"/>
  <text x="95" y="129" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">N4</text>

  <rect x="330" y="30" width="390" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="345" y="52" fill="#38bdf8" font-size="11" font-weight="bold">Quorum Consensus Formula: R + W &gt; N</text>
  <text x="345" y="68" fill="#94a3b8" font-size="8">N=3 replicas. If W=2 and R=2, read and write quorums must overlap by at least 1 node.</text>

  <rect x="330" y="95" width="390" height="55" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="345" y="117" fill="#fbbf24" font-size="11" font-weight="bold">Hinted Handoff: The Always-Writable Design</text>
  <text x="345" y="133" fill="#94a3b8" font-size="8">If Node N2 is unreachable, Node N4 accepts the write with a hint and replays it when N2 reboots.</text>

  <rect x="330" y="160" width="390" height="55" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="1.5"/>
  <text x="345" y="182" fill="#f472b6" font-size="11" font-weight="bold">Anti-Entropy via Merkle Trees</text>
  <text x="345" y="198" fill="#94a3b8" font-size="8">Compares hierarchical hash trees in O(log N) to synchronize diverging partitions without full scans.</text>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Shopping Cart High Availability</h5>
  <p>If network partitions isolate nodes, DynamoDB prefers availability over strong consistency. Multiple conflicting writes are captured via <strong>Vector Clocks</strong> and resolved at read time by taking the union of added items.</p>
</div>
"""
    },
    {
        "id": "bp-search",
        "num": "09",
        "title": "Google Search: Distributed Web Spider & Inverted Index",
        "tagline": "How to crawl 100+ Billion web pages, deduplicate with SimHash, and rank results in &lt; 200ms.",
        "badge": "Search & Crawling",
        "stats": {
            "indexedPages": "100+ Billion Pages",
            "crawlThroughput": "Millions of Pages / Sec",
            "searchQps": "100,000+ Queries / Sec",
            "queryLatency": "< 200ms Complete SERP"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="45" width="120" height="65" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="80" y="72" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">URL Frontier</text>
  <text x="80" y="88" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Politeness &amp; Priority</text>

  <rect x="180" y="45" width="130" height="65" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="245" y="72" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Crawler Workers</text>
  <text x="245" y="88" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Async DNS + SimHash</text>

  <rect x="350" y="45" width="140" height="65" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="420" y="72" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Parser &amp; Tokenizer</text>
  <text x="420" y="88" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">HTML Clean &bull; Stemming</text>

  <rect x="530" y="35" width="190" height="85" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="625" y="62" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Distributed Inverted Index</text>
  <text x="625" y="78" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Word &rarr; [DocID Posting List]</text>
  <text x="625" y="92" fill="#34d399" font-size="7" font-family="monospace" text-anchor="middle">Two-pointer SIMD Intersection</text>

  <rect x="200" y="150" width="520" height="60" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="460" y="178" fill="#22d3ee" font-size="12" font-weight="bold" text-anchor="middle">Search Serving Tier (PageRank &bull; BM25 &bull; RankBrain)</text>
  <text x="460" y="195" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Scattered across 10,000 query nodes; Gathers top-k results in parallel in &lt;50ms</text>

  <path d="M 140 78 L 180 78" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 310 78 L 350 78" stroke="#10b981" stroke-width="2"/>
  <path d="M 490 78 L 530 78" stroke="#a855f7" stroke-width="2"/>
  <path d="M 625 120 L 625 150" stroke="#ec4899" stroke-width="2"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Posting List Intersection</h5>
  <p>An inverted index maps keywords to sorted lists of Document IDs. When querying <code>"distributed systems"</code>, query servers execute vectorized SIMD leapfrog joins across posting lists in microseconds.</p>
</div>
"""
    },
    {
        "id": "bp-hft",
        "num": "10",
        "title": "High-Frequency Trading: Order Book Matching Engine (LMAX Disruptor)",
        "tagline": "How to match 6 Million orders per second with sub-microsecond latency and zero GC pauses.",
        "badge": "Sub-Microsecond Systems",
        "stats": {
            "throughput": "6,000,000 Orders / Sec",
            "latency": "< 800 Nanoseconds P99",
            "concurrency": "Lock-Free Ring Buffer (Disruptor)",
            "memory": "Off-Heap Pinned Memory"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="55" width="110" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="75" y="82" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Trader Gateway</text>
  <text x="75" y="96" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">FIX / ITCH Protocol</text>

  <rect x="170" y="45" width="220" height="75" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="280" y="75" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">LMAX Ring Buffer (Disruptor)</text>
  <text x="280" y="92" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Lock-Free Circular Array (2^N size)</text>
  <text x="280" y="106" fill="#fbbf24" font-size="7" font-family="monospace" text-anchor="middle">Atomic CAS Sequence Number &bull; Zero Locks</text>

  <rect x="430" y="45" width="180" height="75" rx="10" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="520" y="75" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Single-Threaded Engine</text>
  <text x="520" y="92" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Pinned to Isolated CPU Core</text>
  <text x="520" y="106" fill="#10b981" font-size="7" font-family="monospace" text-anchor="middle">Sub-microsecond Price-Time Priority</text>

  <rect x="230" y="150" width="380" height="60" rx="8" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>
  <text x="420" y="178" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Replication &amp; Non-Blocking Journaler</text>
  <text x="420" y="195" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Secondary consumer logs orders asynchronously without blocking the matching thread</text>

  <path d="M 130 82 L 170 82" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 390 82 L 430 82" stroke="#10b981" stroke-width="2"/>
  <path d="M 280 120 L 280 150" stroke="#64748b" stroke-width="1.5"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Why Single-Threaded Beats Multi-Threaded Locking</h5>
  <p>Traditional multi-threaded matching engines suffer from thread context switching (1,500ns) and mutex lock contention (25ns). The <strong>LMAX Disruptor</strong> pins a single thread to an isolated CPU core (<code>isolcpus</code>), reading from a lock-free pre-allocated ring buffer. Because there are zero thread switches and zero locks, it matches orders in <strong>under 800 nanoseconds</strong>.</p>
</div>
"""
    },
    {
        "id": "bp-s3",
        "num": "11",
        "title": "AWS S3 Architecture: Distributed Object Store & Erasure Coding",
        "tagline": "How S3 achieves 99.999999999% (11 Nines) durability using Reed-Solomon (8+4) Erasure Coding.",
        "badge": "Object Storage",
        "stats": {
            "durability": "99.999999999% (11 Nines)",
            "volume": "Exabytes of Data",
            "erasureCoding": "Reed-Solomon (8 Data + 4 Parity)",
            "storageSavings": "50% Savings vs 3x Replication"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="110" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="75" y="88" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">Client PUT</text>
  <text x="75" y="102" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">Multipart S3 API</text>

  <rect x="170" y="55" width="140" height="65" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="240" y="82" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">S3 Ingress Gateway</text>
  <text x="240" y="98" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Slices Object into Chunks</text>

  <rect x="350" y="45" width="170" height="85" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="435" y="72" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Reed-Solomon Erasure Coder</text>
  <text x="435" y="90" fill="#fbbf24" font-size="8" font-family="monospace" text-anchor="middle">8 Data Chunks + 4 Parity Chunks</text>
  <text x="435" y="104" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">Survives 4 Concurrent Drive Failures!</text>

  <rect x="560" y="45" width="170" height="85" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="645" y="72" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Storage Fleet (12 Racks)</text>
  <text x="645" y="90" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">1 Chunk per physical rack</text>
  <text x="645" y="104" fill="#10b981" font-size="7" font-family="monospace" text-anchor="middle">Survives entire datacenter loss</text>

  <path d="M 130 88 L 170 88" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 310 88 L 350 88" stroke="#10b981" stroke-width="2"/>
  <path d="M 520 88 L 560 88" stroke="#ec4899" stroke-width="2"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">Erasure Coding vs 3x Replication</h5>
  <p>Standard 3x replication has a <strong>200% storage overhead</strong> (1 TB requires 3 TB disk). <strong>Reed-Solomon (8+4) Erasure Coding</strong> splits an object into 8 data chunks and computes 4 mathematical parity chunks. Overhead is only <strong>50%</strong> (1 TB requires 1.5 TB disk), yet the object can withstand the loss of <strong>any 4 concurrent disks or racks</strong> without losing a single bit!</p>
</div>
"""
    },
    {
        "id": "bp-vector-rag",
        "num": "12",
        "title": "Modern AI Infrastructure: Vector Search (HNSW) & vLLM PagedAttention",
        "tagline": "How to serve 100M+ vector embeddings and achieve 8x LLM serving throughput with continuous batching.",
        "badge": "GenAI Infrastructure",
        "stats": {
            "vectorDimensions": "1,536 (Gemini / OpenAI)",
            "vectorCount": "100 Million+ Embeddings",
            "searchLatency": "< 15 ms ANN (HNSW)",
            "gpuUtilization": "8x Higher Throughput via PagedAttention"
        },
        "svg": """
<svg viewBox="0 0 760 250" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="100" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="88" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle">User Prompt</text>
  <text x="70" y="102" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">RAG Query</text>

  <rect x="160" y="60" width="120" height="55" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <text x="220" y="85" fill="#c084fc" font-size="11" font-weight="bold" text-anchor="middle">Embedding API</text>
  <text x="220" y="100" fill="#94a3b8" font-size="7" font-family="monospace" text-anchor="middle">Float32[1536]</text>

  <rect x="320" y="45" width="180" height="85" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="410" y="72" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Vector DB (Milvus / Pinecone)</text>
  <text x="410" y="90" fill="#fbbf24" font-size="8" font-family="monospace" text-anchor="middle">HNSW Hierarchical Graph</text>
  <text x="410" y="104" fill="#38bdf8" font-size="7" font-family="monospace" text-anchor="middle">Top-K Context Chunks retrieved in &lt;15ms</text>

  <rect x="540" y="45" width="190" height="85" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="635" y="72" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">vLLM Inference Cluster</text>
  <text x="635" y="90" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">PagedAttention KV-Cache</text>
  <text x="635" y="104" fill="#34d399" font-size="7" font-family="monospace" text-anchor="middle">Continuous Batching Streaming</text>

  <path d="M 120 88 L 160 88" stroke="#38bdf8" stroke-width="1.5"/>
  <path d="M 280 88 L 320 88" stroke="#a855f7" stroke-width="2"/>
  <path d="M 500 88 L 540 88" stroke="#10b981" stroke-width="2"/>
</svg>
""",
        "deepDive": """
<div class="space-y-4 text-xs text-slate-300">
  <h5 class="text-sm font-bold text-white">How PagedAttention Solves GPU HBM Fragmentation</h5>
  <p>Traditional LLM inference reserves static memory for worst-case token lengths (e.g. 4096 tokens), leaving up to <strong>80% of GPU High Bandwidth Memory (HBM) wasted</strong>. <strong>PagedAttention</strong> introduces OS virtual memory paging to LLM KV-caches, packing non-contiguous memory blocks and boosting serving throughput by <strong>4x to 8x</strong> on NVIDIA H100 GPUs.</p>
</div>
"""
    }
]

print(f"Loaded all {len(BLUEPRINTS)} Master Blueprints.")
