# curriculum_stage2_data.py
# Stage 2: Junior to Mid - Horizontal Scalability, Stateless Tiers & Database Indexing

STAGE_2_CHAPTERS = [
    {
        "id": "c-04-scaling-stateless",
        "stageId": "stage-2",
        "stageNum": "STAGE 02",
        "badge": "Junior / Mid",
        "color": "cyan",
        "title": "2.1 Horizontal vs Vertical Scaling & Stateless Web Tiers",
        "difficulty": "Intermediate",
        "readTime": "22 min read",
        "simulatorKey": "finops",
        "summary": "Scaling physical limits: Amdahl's Law, L4 (Maglev) vs L7 (Envoy) load balancing, externalizing session state to Redis clusters, and graceful connection draining.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 text-cyan-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-cyan-400 mb-1">First-Principles Intuition</div>
    Imagine a small restaurant with a single chef. As orders surge from 10 to 500 per hour:
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-cyan-200">
      <li><strong>Vertical Scaling (Scale Up):</strong> Replace the chef with Gordon Ramsay and buy an ultra-expensive industrial 16-burner stove. Eventually, Gordon Ramsay reaches human physical limits; no matter how much money you spend, one person cannot cook 500 steaks simultaneously.</li>
      <li><strong>Horizontal Scaling (Scale Out):</strong> Hire 10 standard chefs, set up an expeditor (<strong>Load Balancer</strong>) at the kitchen entrance to distribute order tickets evenly, and keep all shared ingredients in a central walk-in freezer (<strong>Externalized State / Redis</strong>). Any chef can cook any ticket!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> 1. The Physical Limits of Vertical Scaling (Amdahl's Law)
  </h4>
  <p>
    Vertical scaling hits an economic and physical brick wall. A server with 128 cores and 1TB RAM does not provide 128x the throughput of a single core due to <strong>Amdahl's Law</strong>:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    $$S_{\text{latency}}(s) = \frac{1}{(1 - p) + \frac{p}{s}}$$
    Where $p$ is the parallel fraction of the software and $s$ is the number of cores. If only 5% of your code relies on a shared mutex lock ($p = 0.95$), the maximum theoretical speedup is capped at $20\times$, even if you purchase an infinite number of CPU cores!
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> 2. L4 vs L7 Load Balancing Architecture
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Dimension</th>
          <th class="p-2.5">Layer 4 (Transport / Maglev / IPVS)</th>
          <th class="p-2.5">Layer 7 (Application / Envoy / NGINX)</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Inspection Level</td>
          <td class="p-2.5">TCP/UDP 5-tuple (Src IP, Src Port, Dst IP, Dst Port, Proto)</td>
          <td class="p-2.5 text-emerald-400">HTTP URL paths, Headers, Cookies, JWT claims, gRPC methods</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">TLS Termination</td>
          <td class="p-2.5 text-slate-400">No (Passes raw encrypted TCP packets via Direct Server Return)</td>
          <td class="p-2.5 text-emerald-400">Yes (Terminates TLS, decrypts payload, inspects HTTP content)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Throughput Ceiling</td>
          <td class="p-2.5 text-emerald-400">10M - 50M packets/sec per node (Kernel bypass / DPDK)</td>
          <td class="p-2.5 text-amber-400">50k - 200k req/sec per node (Bounded by CPU crypto &amp; parsing)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> 3. Making Web Tiers Stateless: The Redis Session Engine
  </h4>
  <p>
    If an application server stores user sessions in local server RAM (e.g. <code>app_instance.memory_sessions[user_id]</code>), the load balancer is forced to enable <strong>Sticky Sessions</strong> (pinning a user to that specific server IP).
    When that server crashes or auto-scales down, all active user shopping carts are wiped!
    <br><br>
    In a stateless architecture, application instances hold ZERO session memory. Every request extracts an encrypted token or session ID and fetches data from a sub-millisecond Redis cluster or memcached pool.
  </p>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-l4" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="g-l7" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#059669"/><stop offset="100%" stop-color="#047857"/></linearGradient>
    <linearGradient id="g-app" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient>
    <linearGradient id="g-rd" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#dc2626"/><stop offset="100%" stop-color="#991b1b"/></linearGradient>
    <marker id="arr-c2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-g2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
    <marker id="arr-m2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- TIER 1: L4 MAGLEV ECMP -->
  <g transform="translate(30, 110)">
    <rect width="160" height="130" rx="10" fill="url(#g-l4)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="14" y="26" fill="#ffffff" font-size="11" font-weight="bold">L4 Maglev Fabric</text>
    <text x="14" y="44" fill="#bae6fd" font-size="8" font-family="monospace">BGP Anycast VIP</text>
    <text x="14" y="62" fill="#e0f2fe" font-size="8" font-family="sans-serif">Kernel Bypass (DPDK)</text>
    <rect x="14" y="74" width="132" height="42" rx="4" fill="#0c4a6e"/>
    <text x="20" y="88" fill="#38bdf8" font-size="8" font-family="monospace">Direct Server Return</text>
    <text x="20" y="102" fill="#7dd3fc" font-size="8" font-family="monospace">10M Packets / Sec</text>
  </g>

  <!-- TIER 2: L7 ENVOY PROXIES -->
  <g transform="translate(250, 40)">
    <rect width="180" height="120" rx="10" fill="url(#g-l7)" stroke="#34d399" stroke-width="1.5"/>
    <text x="14" y="26" fill="#ffffff" font-size="11" font-weight="bold">L7 Envoy Proxy 01</text>
    <text x="14" y="44" fill="#a7f3d0" font-size="8" font-family="monospace">TLS 1.3 Termination</text>
    <text x="14" y="62" fill="#d1fae5" font-size="8" font-family="sans-serif">Path: /api/v1/checkout</text>
    <text x="14" y="80" fill="#6ee7b7" font-size="8" font-family="monospace">Rate Limiter &amp; Auth Check</text>
  </g>
  <g transform="translate(250, 190)">
    <rect width="180" height="120" rx="10" fill="url(#g-l7)" stroke="#34d399" stroke-width="1.5"/>
    <text x="14" y="26" fill="#ffffff" font-size="11" font-weight="bold">L7 Envoy Proxy 02</text>
    <text x="14" y="44" fill="#a7f3d0" font-size="8" font-family="monospace">TLS 1.3 Termination</text>
    <text x="14" y="62" fill="#d1fae5" font-size="8" font-family="sans-serif">Path: /api/v1/users</text>
    <text x="14" y="80" fill="#6ee7b7" font-size="8" font-family="monospace">Round-Robin / Least Conn</text>
  </g>

  <!-- TIER 3: STATELESS APP SERVERS -->
  <g transform="translate(490, 40)">
    <rect width="180" height="85" rx="8" fill="url(#g-app)" stroke="#c084fc" stroke-width="1.2"/>
    <text x="14" y="24" fill="#ffffff" font-size="10" font-weight="bold">App Pod #01 (Stateless)</text>
    <text x="14" y="42" fill="#e9d5ff" font-size="8" font-family="monospace">Zero In-Memory Sessions</text>
    <text x="14" y="60" fill="#a7f3d0" font-size="8" font-family="monospace">Auto-scaled to 50 pods</text>
  </g>
  <g transform="translate(490, 140)">
    <rect width="180" height="85" rx="8" fill="url(#g-app)" stroke="#c084fc" stroke-width="1.2"/>
    <text x="14" y="24" fill="#ffffff" font-size="10" font-weight="bold">App Pod #02 (Stateless)</text>
    <text x="14" y="42" fill="#e9d5ff" font-size="8" font-family="monospace">Any pod serves any user</text>
    <text x="14" y="60" fill="#a7f3d0" font-size="8" font-family="monospace">Can be killed anytime</text>
  </g>
  <g transform="translate(490, 240)">
    <rect width="180" height="85" rx="8" fill="url(#g-app)" stroke="#c084fc" stroke-width="1.2"/>
    <text x="14" y="24" fill="#ffffff" font-size="10" font-weight="bold">App Pod #03 (Stateless)</text>
    <text x="14" y="42" fill="#e9d5ff" font-size="8" font-family="monospace">Graceful drain on deploy</text>
  </g>

  <!-- TIER 4: SHARED REDIS SESSION CLUSTER -->
  <g transform="translate(730, 110)">
    <rect width="200" height="130" rx="10" fill="url(#g-rd)" stroke="#f87171" stroke-width="1.5"/>
    <text x="14" y="26" fill="#ffffff" font-size="11" font-weight="bold">Redis Session Cluster</text>
    <text x="14" y="44" fill="#fecaca" font-size="8" font-family="monospace">Master-Replica with Sentinels</text>
    <text x="14" y="62" fill="#fee2e2" font-size="8" font-family="sans-serif">Key: sess:usr_998124</text>
    <rect x="14" y="74" width="172" height="42" rx="4" fill="#7f1d1d"/>
    <text x="20" y="88" fill="#fca5a5" font-size="8" font-family="monospace">Latency: &lt; 0.5 ms</text>
    <text x="20" y="102" fill="#fef08a" font-size="8" font-family="monospace">1M Read Ops / Sec</text>
  </g>

  <!-- CONNECTORS -->
  <path d="M 190 170 L 250 100" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-c2)"/>
  <path d="M 190 180 L 250 250" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-c2)"/>
  <path d="M 430 100 L 490 80" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-g2)"/>
  <path d="M 430 250 L 490 280" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-g2)"/>
  <path d="M 670 80 L 730 160" fill="none" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="3" marker-end="url(#arr-m2)"/>
  <path d="M 670 180 L 730 180" fill="none" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="3" marker-end="url(#arr-m2)"/>
  <path d="M 670 280 L 730 200" fill="none" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="3" marker-end="url(#arr-m2)"/>
</svg>
""",
        "codeSnippet": """# Production Python FastAPI Stateless Session Verification Middleware
# Zero Database Calls: Cryptographically Verified RSA-256 JWT with Redis Fallback
import time
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from redis.asyncio import Redis

security = HTTPBearer()

class StatelessSessionManager:
    def __init__(self, public_key_pem: str, redis_client: Redis):
        self.public_key = public_key_pem
        self.redis = redis_client
        self.jwt_algorithm = "RS256"

    async def authenticate_request(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
        token = credentials.credentials
        try:
            # Step 1: In-memory cryptographic signature verification (takes < 0.1ms, 0 network hops!)
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.jwt_algorithm],
                options={"require": ["exp", "iss", "sub", "jti"]}
            )
            
            # Step 2: Check Distributed Token Revocation Blacklist in Redis
            # (Only queried if user clicked "Log Out Everywhere" or password changed)
            jti = payload["jti"]
            is_revoked = await self.redis.exists(f"revoked_token:{jti}")
            if is_revoked:
                raise HTTPException(status_code=401, detail="Token has been explicitly revoked")

            # Step 3: Return stateless user context directly to handler
            return {
                "user_id": payload["sub"],
                "role": payload.get("role", "customer"),
                "tenant_id": payload.get("tenant_id")
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Session expired")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid security token: {str(e)}")
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Knight Capital Group $440 Million Bankruptcy Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: The largest equities market maker in the US lost $440M and went bankrupt in 45 minutes due to an asymmetric horizontal server deployment error.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      On August 1, 2012, Knight Capital manually deployed new trading software across an 8-server horizontal cluster.
      A systems technician mistakenly updated <strong>7 out of the 8 servers</strong>, leaving Server 8 running a legacy codebase where a repurposed software flag was active.
    </p>
    <p>
      When market open arrived, the load balancer forwarded 12.5% of market order requests to Server 8.
      Server 8 interpreted the traffic using the old dead code, triggering a runaway loop of buying high and selling low that executed 4 million unintended share executions across 154 stocks.
      <strong>Because there was zero automated deployment verification or automated canary gating, the company was financially insolvent before engineers identified which server was misconfigured!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Immutable Infrastructure (Golden Images):</strong> Never deploy by updating packages on existing VMs. Bake immutable AMI / container images where all servers are byte-for-byte identical.</li>
      <li><strong class="text-white">Automated Canary Deployments:</strong> Route 1% of live traffic to a single canary node. Continuously monitor error rates and latency SLAs via Prometheus for 10 minutes before progressing to 10%, 50%, and 100%.</li>
      <li><strong class="text-white">Dead-Man Auto-Kill Switches:</strong> Implement automated circuit breakers at the gateway layer that automatically terminate any server instance that deviates by &gt; 3 sigma from fleet behavior.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why are Sticky Sessions considered an architectural anti-pattern, and how do you handle stateful protocols like WebSockets in an auto-scaling environment?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "Sticky Sessions violate the core principle of horizontal scalability by creating <strong>uneven traffic load</strong> and destroying failure recovery. If a power user or web crawler is assigned to Pod A, Pod A overheats while Pod B sits idle. Furthermore, when auto-scaling terminates Pod A or it crashes, all pinned sessions are violently dropped.
      <br><br>
      For stateful persistent connections like <strong>WebSockets</strong>, we decouple connection management from application state using a <strong>Pub/Sub Event Fabric</strong> (e.g. Redis Pub/Sub or Kafka).
      When User X connects to WebSocket Gateway Node 4, Node 4 registers a lightweight routing record in Redis: <code>user_socket:usr_123 &rarr; gateway_node_4</code>.
      When any backend microservice wants to send a notification to User X, it publishes the event to Redis. Node 4 consumes the event and pushes it down the active TCP socket to User X.
      If Node 4 crashes, the client reconnects to any available gateway node in &lt;100ms and re-registers its socket location with zero data loss."
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-05-databases-indexes",
        "stageId": "stage-2",
        "stageNum": "STAGE 02",
        "badge": "Junior / Mid",
        "color": "cyan",
        "title": "2.2 Relational Databases, B+ Trees & Query Indexing",
        "difficulty": "Intermediate",
        "readTime": "24 min read",
        "simulatorKey": "tracer",
        "summary": "Storage engine physics: Why B+ Trees beat Binary Trees for disk blocks. Clustered vs Secondary indexes, Write Amplification, and dissecting EXPLAIN ANALYZE execution plans.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 text-cyan-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-cyan-400 mb-1">First-Principles Intuition</div>
    Imagine searching for a word in a 1,000-page encyclopedia.
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-cyan-200">
      <li><strong>Sequential Full Table Scan:</strong> Start on page 1 and read every single word until you reach page 1,000. If the word is on page 950, you read 950 pages. On disk, this is a full table scan ($O(N)$), thrashing your disk IOPS.</li>
      <li><strong>B+ Tree Index:</strong> Flip to the Index section at the back. It tells you: "Letter 'M' &rarr; Pages 400-550 &rarr; Subheading 'Microservices' &rarr; Page 412". You made 3 quick flips and jumped directly to the exact paragraph ($O(\log_B N)$)!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> 1. The Physics of Disk I/O: Why B+ Trees Win
  </h4>
  <p>
    Operating systems and NVMe SSDs do not read individual bytes from disk; they transfer data in fixed <strong>4KB to 16KB Pages (Blocks)</strong>.
    A standard Binary Search Tree (BST) has a fan-out of 2. For 100,000,000 rows, a BST has a tree depth of $\approx 27$. That requires 27 random disk seeks (at 5ms per seek on HDD or 100μs on SSD = unacceptable!).
    <br><br>
    In contrast, a <strong>B+ Tree</strong> has a massive fan-out ($B \approx 100 \text{ to } 1,000$). For 100,000,000 records, the tree height is only <strong>3 or 4 levels</strong>:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800">
    $$\text{Height} = \lceil \log_{B}(N) \rceil = \lceil \log_{100}(100,000,000) \rceil = 4 \text{ Page Lookups!}$$
    Because root and intermediate pages are cached permanently in OS RAM buffer pools, finding ANY row in a 100-million row database requires exactly <strong>ONE physical disk read</strong>!
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> 2. Clustered vs Secondary Indexes &amp; The Double Lookup
  </h4>
  <ul class="list-disc list-inside space-y-2 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Clustered Index (Primary Key):</strong> The table data ITSELF is physically sorted and stored directly in the leaf pages of the primary B+ Tree. A table can have only ONE clustered index.</li>
    <li><strong class="text-white">Secondary Index (e.g. on `email`):</strong> The leaf pages do NOT contain the full row data. Instead, they store the indexed column (`email`) and the corresponding Primary Key (`id`).</li>
    <li><strong class="text-white">The Penalty (Double Lookup / Bookmark Lookup):</strong> When you query <code>SELECT * FROM users WHERE email = 'ceo@meta.com'</code>, the database engine navigates the secondary index B+ Tree to find the Primary Key `id`, then performs a SECOND B+ Tree traversal on the clustered index to fetch the full row!</li>
    <li><strong class="text-white">The Staff Optimization (Covering Index):</strong> If you index <code>CREATE INDEX idx_email_name ON users(email, full_name)</code>, a query for <code>SELECT full_name WHERE email = ...</code> is satisfied entirely from the secondary index leaf page, eliminating the second disk lookup completely!</li>
  </ul>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-idx" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-leaf" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- ROOT NODE (PAGE 01 - RAM CACHED) -->
  <g transform="translate(360, 30)">
    <rect width="240" height="60" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <text x="120" y="24" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">ROOT PAGE (In Memory Buffer Pool)</text>
    <rect x="20" y="32" width="60" height="20" rx="4" fill="#1e293b"/>
    <text x="50" y="46" fill="#f8fafc" font-size="9" font-family="monospace" text-anchor="middle">ID &lt; 50</text>
    <rect x="90" y="32" width="60" height="20" rx="4" fill="#1e293b"/>
    <text x="120" y="46" fill="#f8fafc" font-size="9" font-family="monospace" text-anchor="middle">50-100</text>
    <rect x="160" y="32" width="60" height="20" rx="4" fill="#1e293b"/>
    <text x="190" y="46" fill="#f8fafc" font-size="9" font-family="monospace" text-anchor="middle">ID &gt; 100</text>
  </g>

  <!-- LEVEL 1: INTERMEDIATE PAGES -->
  <g transform="translate(80, 140)">
    <rect width="220" height="55" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
    <text x="110" y="22" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">Internal Node (Keys 1-49)</text>
    <text x="110" y="42" fill="#cbd5e1" font-size="9" font-family="monospace" text-anchor="middle">[Key 10] [Key 25] [Key 40]</text>
  </g>
  <g transform="translate(370, 140)">
    <rect width="220" height="55" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
    <text x="110" y="22" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">Internal Node (Keys 50-99)</text>
    <text x="110" y="42" fill="#cbd5e1" font-size="9" font-family="monospace" text-anchor="middle">[Key 60] [Key 75] [Key 90]</text>
  </g>
  <g transform="translate(660, 140)">
    <rect width="220" height="55" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
    <text x="110" y="22" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">Internal Node (Keys 100+)</text>
    <text x="110" y="42" fill="#cbd5e1" font-size="9" font-family="monospace" text-anchor="middle">[Key 120] [Key 150] [Key 180]</text>
  </g>

  <!-- LEVEL 2: LEAF DATA PAGES (DOUBLY-LINKED LIST FOR RANGE SCANS) -->
  <g transform="translate(30, 260)">
    <rect width="200" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="22" fill="#34d399" font-size="10" font-weight="bold">Leaf Page A (16KB Block)</text>
    <text x="14" y="40" fill="#a7f3d0" font-size="8" font-family="monospace">Row 1: {id: 1, name: "Alice"}</text>
    <text x="14" y="56" fill="#a7f3d0" font-size="8" font-family="monospace">Row 2: {id: 2, name: "Bob"}</text>
    <text x="14" y="74" fill="#a7f3d0" font-size="8" font-family="monospace">Row 3: {id: 3, name: "Carol"}</text>
  </g>
  <g transform="translate(260, 260)">
    <rect width="200" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="22" fill="#34d399" font-size="10" font-weight="bold">Leaf Page B (16KB Block)</text>
    <text x="14" y="40" fill="#a7f3d0" font-size="8" font-family="monospace">Row 10: {id: 10, name: "Dave"}</text>
    <text x="14" y="56" fill="#a7f3d0" font-size="8" font-family="monospace">Row 11: {id: 11, name: "Eve"}</text>
    <text x="14" y="74" fill="#a7f3d0" font-size="8" font-family="monospace">Row 12: {id: 12, name: "Frank"}</text>
  </g>
  <g transform="translate(490, 260)">
    <rect width="200" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="22" fill="#34d399" font-size="10" font-weight="bold">Leaf Page C (16KB Block)</text>
    <text x="14" y="40" fill="#a7f3d0" font-size="8" font-family="monospace">Row 25: {id: 25, name: "Grace"}</text>
    <text x="14" y="56" fill="#a7f3d0" font-size="8" font-family="monospace">Row 26: {id: 26, name: "Heidi"}</text>
    <text x="14" y="74" fill="#a7f3d0" font-size="8" font-family="monospace">Row 27: {id: 27, name: "Ivan"}</text>
  </g>
  <g transform="translate(720, 260)">
    <rect width="210" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="14" y="22" fill="#34d399" font-size="10" font-weight="bold">Leaf Page D (16KB Block)</text>
    <text x="14" y="40" fill="#a7f3d0" font-size="8" font-family="monospace">Row 50: {id: 50, name: "Judy"}</text>
    <text x="14" y="56" fill="#a7f3d0" font-size="8" font-family="monospace">Row 51: {id: 51, name: "Kevin"}</text>
    <text x="14" y="74" fill="#a7f3d0" font-size="8" font-family="monospace">Row 52: {id: 52, name: "Leo"}</text>
  </g>

  <!-- LEAF SIBLING POINTERS (O(1) RANGE SCAN) -->
  <path d="M 230 305 L 260 305" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-leaf)"/>
  <path d="M 460 305 L 490 305" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-leaf)"/>
  <path d="M 690 305 L 720 305" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-leaf)"/>

  <!-- TRAVERSAL ARROWS -->
  <path d="M 410 90 L 220 140" fill="none" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arr-idx)"/>
  <path d="M 480 90 L 480 140" fill="none" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arr-idx)"/>
  <path d="M 550 90 L 750 140" fill="none" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arr-idx)"/>
</svg>
""",
        "codeSnippet": """-- Production PostgreSQL DDL: Advanced Indexing Patterns & Execution Analysis
-- Demonstrating Covering Indexes, Partial Indexes, and EXPLAIN ANALYZE

-- Scenario: High-volume financial transactions table (100M+ rows)
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    amount_cents BIGINT NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL, -- 'PENDING', 'SETTLED', 'FAILED'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Optimization 1: High-Performance Composite Covering Index
-- Eliminates table heap lookups for typical account statement query
CREATE INDEX idx_account_stmt ON transactions (account_id, created_at DESC)
INCLUDE (amount_cents, currency, status);

-- Optimization 2: Partial Index for High-Velocity Queue Worker
-- 99% of transactions are SETTLED. Only 1% are PENDING.
-- Instead of indexing all 100M rows, this partial index contains only ~10,000 rows!
-- Index size drops from 4.5 GB to 1.2 MB!
CREATE INDEX idx_pending_txs ON transactions (created_at ASC)
WHERE status = 'PENDING';

-- Staff Execution Plan Verification Query:
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT amount_cents, currency, status
FROM transactions
WHERE account_id = 'c4d6a1b2-8c9e-4f1a-b3d5-e7f8a9b0c1d2'
  AND created_at >= NOW() - INTERVAL '30 days'
ORDER BY created_at DESC;

-- EXPECTED STAFF OUTPUT:
-- Index Only Scan using idx_account_stmt on public.transactions
-- Heap Fetches: 0  (Proof that zero physical table blocks were touched!)
-- Buffers: shared hit=4 read=0 (Served 100% from RAM buffer pool)
-- Execution Time: 0.082 ms
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The GitLab 2017 Live Database Outage (300GB Production Data Loss)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: GitLab.com was offline for 18 hours after a PostgreSQL replication lag incident led to accidental deletion of the production primary directory.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      GitLab experienced a severe replication lag crisis on a secondary database node caused by an unexpected spike in database writes (a spammer attack creating millions of fake issues).
      The replica was unable to catch up using streaming WAL (Write-Ahead Logging).
    </p>
    <p>
      An engineer attempting to clear a lock file and resynchronize the replica manually executed <code>rm -rf /var/opt/gitlab/postgresql/data</code>.
      <strong>Tragically, the engineer was connected to the PRODUCTION PRIMARY database server instead of the replica!</strong>
      300GB of customer repositories, comments, and issue data vanished instantly. 5 separate automated backup mechanisms (LVM snapshots, S3 wal-e, Azure storage) all failed due to silent configuration bugs!
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Role-Based Terminal Color Guards:</strong> SSH sessions to production database primaries must display bright red shell prompts, require hardware MFA confirmation, and revoke destructive shell permissions (<code>rm</code>, <code>dropdb</code>).</li>
      <li><strong class="text-white">Continuous Backup Restore Testing:</strong> Backups are only valid if an automated test restores them into a staging database daily. Never assume backups work without continuous verification.</li>
      <li><strong class="text-white">Continuous Point-in-Time Recovery (PITR):</strong> Ship PostgreSQL WAL segments directly to immutable S3 Object Lock buckets with 30-day retention policies so accidental deletion can be rolled back to the exact second.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why can't we just add an index to every single column in our database table to guarantee that all queries run at maximum speed?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "Indexes are not free; they are separate physical B+ Tree structures stored on disk. Adding an index to every column introduces three severe architectural penalties:
      <br><br>
      1. <strong>Massive Write Amplification:</strong> Every <code>INSERT</code>, <code>UPDATE</code>, or <code>DELETE</code> must update the primary clustered table AND synchronously rebalance every single secondary B+ Tree index. If you have 15 indexes on a table, 1 insert translates into 16 separate disk write operations and frequent B+ Tree page splits!
      <br><br>
      2. <strong>Buffer Pool Eviction:</strong> Index pages compete with hot table data for space in the RAM database buffer pool. Excess indexes evict frequently accessed table rows from memory, triggering expensive NVMe disk I/O.
      <br><br>
      3. <strong>Optimizer Confusion:</strong> The query planner must evaluate dozens of combinatorial index paths, inflating query parse and planning latency.
      <br><br>
      The Staff approach is surgical: create <strong>Composite Covering Indexes</strong> tailored to exact query patterns, utilize <strong>Partial Indexes</strong> for low-cardinality status flags, and continuously monitor <code>pg_stat_user_indexes</code> to drop any index with zero scan hits."
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 2 loaded with {len(STAGE_2_CHAPTERS)} comprehensive chapters.")
