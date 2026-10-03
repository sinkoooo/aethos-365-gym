# data_interactive_tools.py
# Modular, robust interactive tools for Packet Tracer, AWS FinOps, Hash Ring, Rate Limiter, and Interview Studio.

TRACER_HTML = """
<div class="space-y-6">
  <!-- Top Header & Scenario Switcher Bar -->
  <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
        <h3 class="text-lg font-bold text-white font-mono tracking-tight">DISTRIBUTED ARCHITECTURE PACKET TRACER &amp; PROTOCOL INSPECTOR</h3>
      </div>
      <p class="text-xs text-slate-400 mt-1 max-w-3xl">
        Step through simulated production traffic: Anycast Edge CDN caching, mTLS mutations with 2PC Paxos &amp; Kafka CDC, Cache Stampede SingleFlight guards, and Circuit Breaker failovers.
      </p>
    </div>

    <!-- Stepper Controls & Speed Toggle -->
    <div class="flex items-center gap-2 flex-wrap">
      <button onclick="prevTracerStep()" id="btn-tracer-prev" title="Step Back" class="px-2.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-all flex items-center gap-1 cursor-pointer">
        <i data-lucide="chevron-left" class="w-3.5 h-3.5"></i> Prev
      </button>
      <button onclick="toggleTracerAutoPlay()" id="btn-tracer-play" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-1.5 cursor-pointer">
        <i data-lucide="play" id="icon-tracer-play" class="w-3.5 h-3.5 fill-current"></i> <span id="text-tracer-play">Auto Play</span>
      </button>
      <button onclick="nextTracerStep()" id="btn-tracer-next" title="Step Forward" class="px-2.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-all flex items-center gap-1 cursor-pointer">
        Next <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
      </button>
      <button onclick="resetTracer()" title="Reset Trace" class="p-1.5 rounded-xl text-slate-400 hover:text-white bg-slate-950 border border-slate-800 transition-all cursor-pointer">
        <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
      </button>
      <button onclick="toggleTracerSpeed()" id="btn-tracer-speed" class="px-2.5 py-1.5 rounded-xl text-[11px] font-mono font-bold text-cyan-400 bg-cyan-950/40 border border-cyan-800/50 hover:bg-cyan-900/40 transition-all cursor-pointer">
        1x Speed
      </button>
    </div>
  </div>

  <!-- Scenario Selector Buttons -->
  <div class="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar text-xs font-mono">
    <button onclick="switchTracerScenario('scenario-edge-hit')" id="btn-scen-scenario-edge-hit" class="tracer-scen-btn px-3 py-1.5 rounded-xl bg-cyan-500 text-slate-950 font-bold transition-all shrink-0 flex items-center gap-1.5 shadow-lg shadow-cyan-500/20">
      <i data-lucide="zap" class="w-3.5 h-3.5"></i> 1. Edge CDN Hit (8ms)
    </button>
    <button onclick="switchTracerScenario('scenario-write-cdc')" id="btn-scen-scenario-write-cdc" class="tracer-scen-btn px-3 py-1.5 rounded-xl bg-slate-900 text-slate-400 hover:text-white font-medium transition-all shrink-0 flex items-center gap-1.5 border border-slate-800">
      <i data-lucide="database" class="w-3.5 h-3.5"></i> 2. Dist Write + Paxos 2PC + Kafka CDC (42ms)
    </button>
    <button onclick="switchTracerScenario('scenario-stampede')" id="btn-scen-scenario-stampede" class="tracer-scen-btn px-3 py-1.5 rounded-xl bg-slate-900 text-slate-400 hover:text-white font-medium transition-all shrink-0 flex items-center gap-1.5 border border-slate-800">
      <i data-lucide="shield" class="w-3.5 h-3.5"></i> 3. Stampede SingleFlight (18ms)
    </button>
    <button onclick="switchTracerScenario('scenario-breaker')" id="btn-scen-scenario-breaker" class="tracer-scen-btn px-3 py-1.5 rounded-xl bg-slate-900 text-slate-400 hover:text-white font-medium transition-all shrink-0 flex items-center gap-1.5 border border-slate-800">
      <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> 4. Circuit Breaker Trip (1ms)
    </button>
  </div>

  <!-- Real-time Step Timeline Banner -->
  <div class="bg-slate-950/80 p-3 rounded-2xl border border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
    <div class="flex items-center gap-2">
      <span id="tracer-step-badge" class="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/30">Step 1 of 3</span>
      <span id="tracer-step-desc" class="text-slate-200 font-medium">Client dispatches HTTP/3 0-RTT request to Cloudflare Anycast Edge.</span>
    </div>
    <div class="flex items-center gap-3 shrink-0">
      <span class="text-slate-500">Latency: <span id="tracer-step-latency" class="text-emerald-400 font-bold">0.0 ms</span></span>
      <div class="w-32 bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-800">
        <div id="tracer-progress-bar" class="bg-gradient-to-r from-cyan-500 to-emerald-400 h-full w-1/3 transition-all duration-300"></div>
      </div>
    </div>
  </div>

  <!-- SVG Architecture Topology & Deep Packet Inspector -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- SVG Canvas (Col 8) -->
    <div class="lg:col-span-8 bg-slate-950 rounded-2xl border border-white/[0.08] p-4 relative overflow-hidden">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,#06b6d405_0%,transparent_70%)] pointer-events-none"></div>

      <svg id="architecture-tracer-svg" viewBox="0 0 680 340" class="w-full h-auto relative z-10" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="traceGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#10b981"/>
            <stop offset="50%" stop-color="#06b6d4"/>
            <stop offset="100%" stop-color="#8b5cf6"/>
          </linearGradient>
          <filter id="traceGlow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          <filter id="nodeGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#06b6d4" flood-opacity="0.6"/>
          </filter>
        </defs>

        <!-- Base Conduits Wireframe -->
        <!-- Row 1: Ingress (Client -> CDN -> L4 Maglev -> Envoy L7) -->
        <line x1="82" y1="76" x2="252" y2="76" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>
        <line x1="252" y1="76" x2="427" y2="76" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>
        <line x1="427" y1="76" x2="597" y2="76" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>

        <!-- Ingress to Service Core (Envoy L7 down to App Microservice) -->
        <line x1="597" y1="76" x2="597" y2="246" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>

        <!-- Row 2: Service & Storage Core (App -> Redis Cache -> Spanner DB -> Kafka KRaft) -->
        <line x1="597" y1="246" x2="427" y2="246" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>
        <line x1="427" y1="246" x2="252" y2="246" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>
        <line x1="252" y1="246" x2="82" y2="246" stroke="#1e293b" stroke-width="3" stroke-dasharray="4,4"/>

        <!-- Active Illuminated Path -->
        <path id="tracer-active-path" d="M 82 76 L 252 76" fill="none" stroke="url(#traceGrad)" stroke-width="4" stroke-linecap="round" stroke-dasharray="800" stroke-dashoffset="0" class="transition-all duration-500"/>

        <!-- Animated Traveling Packet Particles -->
        <circle id="trace-packet-dot" cx="82" cy="76" r="7" fill="#00f0ff" filter="url(#traceGlow)" opacity="0" class="transition-all duration-300"></circle>
        <circle id="trace-ack-dot" cx="252" cy="76" r="6" fill="#10b981" filter="url(#traceGlow)" opacity="0" class="transition-all duration-300"></circle>

        <!-- =================== 8 TOPOLOGY NODES =================== -->
        <!-- NODE 1: CLIENT (x: 20, y: 40) -->
        <g id="node-box-client" class="cursor-pointer group" onclick="inspectNode('client')">
          <rect x="20" y="40" width="125" height="72" rx="10" fill="#0b0f19" stroke="#38bdf8" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="82" y="66" fill="#f8fafc" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">User Client</text>
          <text x="82" y="82" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Browser / iOS / App</text>
          <text x="82" y="98" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">HTTP/3 QUIC (0-RTT)</text>
        </g>

        <!-- NODE 2: CLOUDFLARE EDGE (x: 185, y: 40) -->
        <g id="node-box-cdn" class="cursor-pointer group" onclick="inspectNode('cdn')">
          <rect x="185" y="40" width="135" height="72" rx="10" fill="#0b0f19" stroke="#06b6d4" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="252" y="66" fill="#22d3ee" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">Cloudflare Edge</text>
          <text x="252" y="82" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Anycast BGP &bull; WAF</text>
          <text x="252" y="98" fill="#10b981" font-size="8" font-family="monospace" text-anchor="middle">95% RAM Cache Hit</text>
        </g>

        <!-- NODE 3: L4 MAGLEV LOAD BALANCER (x: 360, y: 40) -->
        <g id="node-box-l4" class="cursor-pointer group" onclick="inspectNode('l4')">
          <rect x="360" y="40" width="135" height="72" rx="10" fill="#0b0f19" stroke="#6366f1" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="427" y="66" fill="#818cf8" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">L4 Maglev / IPVS</text>
          <text x="427" y="82" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Kernel Bypass (DPDK)</text>
          <text x="427" y="98" fill="#e2e8f0" font-size="8" font-family="monospace" text-anchor="middle">Direct Server Return</text>
        </g>

        <!-- NODE 4: ENVOY API GATEWAY (x: 535, y: 40) -->
        <g id="node-box-l7" class="cursor-pointer group" onclick="inspectNode('l7')">
          <rect x="535" y="40" width="125" height="72" rx="10" fill="#0b0f19" stroke="#a855f7" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="597" y="66" fill="#c084fc" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">Envoy Gateway</text>
          <text x="597" y="82" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">mTLS Ingress &bull; Auth</text>
          <text x="597" y="98" fill="#fbbf24" font-size="8" font-family="monospace" text-anchor="middle">Token Bucket RateLimit</text>
        </g>

        <!-- NODE 5: APP MICROSERVICES PODS (x: 535, y: 210) -->
        <g id="node-box-app" class="cursor-pointer group" onclick="inspectNode('app')">
          <rect x="535" y="210" width="125" height="72" rx="10" fill="#0b0f19" stroke="#3b82f6" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="597" y="236" fill="#60a5fa" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">App Services</text>
          <text x="597" y="252" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Go / Rust Pods (K8s)</text>
          <text x="597" y="268" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">SingleFlight Barrier</text>
        </g>

        <!-- NODE 6: REDIS CACHE CLUSTER (x: 360, y: 210) -->
        <g id="node-box-cache" class="cursor-pointer group" onclick="inspectNode('cache')">
          <rect x="360" y="210" width="135" height="72" rx="10" fill="#0b0f19" stroke="#10b981" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="427" y="236" fill="#34d399" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">Redis Cluster</text>
          <text x="427" y="252" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">16,384 Hash Slots</text>
          <text x="427" y="268" fill="#34d399" font-size="8" font-family="monospace" text-anchor="middle">&lt; 0.8 ms RAM Read</text>
        </g>

        <!-- NODE 7: SPANNER MULTI-AZ DB (x: 185, y: 210) -->
        <g id="node-box-db" class="cursor-pointer group" onclick="inspectNode('db')">
          <rect x="185" y="210" width="135" height="72" rx="10" fill="#0b0f19" stroke="#ec4899" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="252" y="236" fill="#f472b6" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">Google Spanner</text>
          <text x="252" y="252" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Multi-AZ Paxos 2PC</text>
          <text x="252" y="268" fill="#f59e0b" font-size="8" font-family="monospace" text-anchor="middle">TrueTime Consensus</text>
        </g>

        <!-- NODE 8: KAFKA KRAFT & CLICKHOUSE (x: 20, y: 210) -->
        <g id="node-box-kafka" class="cursor-pointer group" onclick="inspectNode('kafka')">
          <rect x="20" y="210" width="125" height="72" rx="10" fill="#0b0f19" stroke="#f59e0b" stroke-width="2" class="group-hover:stroke-cyan-400 transition-all"/>
          <text x="82" y="236" fill="#fbbf24" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">Kafka KRaft</text>
          <text x="82" y="252" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Commit Log CDC</text>
          <text x="82" y="268" fill="#10b981" font-size="8" font-family="monospace" text-anchor="middle">ClickHouse OLAP</text>
        </g>
      </svg>
    </div>

    <!-- Live Deep Packet Inspector Drawer (Col 4) -->
    <div id="tracer-inspector" class="lg:col-span-4 bg-slate-950 rounded-2xl border border-white/[0.08] p-5 space-y-4">
      <!-- Title & Color Tag -->
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span id="inspect-color-dot" class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
          <h4 id="inspect-title" class="text-sm font-bold text-white font-mono">Cloudflare Anycast CDN</h4>
        </div>
        <span id="inspect-badge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-bold">Edge Network PoP</span>
      </div>

      <!-- OSI Layer & Latency SLA -->
      <div class="grid grid-cols-2 gap-2 text-xs font-mono">
        <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-[9px] text-slate-500 uppercase">OSI PROTOCOL LAYER</div>
          <div id="inspect-layer" class="text-xs font-bold text-cyan-300 mt-0.5">Layer 7 Application</div>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-[9px] text-slate-500 uppercase">P99 LATENCY SLA</div>
          <div id="inspect-latency" class="text-xs font-bold text-emerald-400 mt-0.5">&lt; 8 ms edge</div>
        </div>
      </div>

      <!-- Raw Wire Packet Hex / Frame Terminal -->
      <div class="space-y-1.5 font-mono">
        <div class="flex items-center justify-between text-[10px] text-slate-400">
          <span class="flex items-center gap-1.5"><i data-lucide="terminal" class="w-3 h-3 text-cyan-400"></i> LIVE WIRE PACKET FRAME</span>
          <span id="inspect-protocol" class="text-emerald-400 font-bold">HTTP/3 QUIC (UDP 443)</span>
        </div>
        <pre id="inspect-packet-terminal" class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-[10.5px] font-mono text-cyan-200 overflow-x-auto custom-scroll leading-relaxed whitespace-pre font-normal"></pre>
      </div>

      <!-- Architectural Responsibility & Failure Mode -->
      <div class="space-y-3 text-xs">
        <div>
          <div class="text-[10px] font-mono uppercase text-slate-500 font-bold">CORE RESPONSIBILITY</div>
          <p id="inspect-desc" class="text-slate-300 mt-0.5 leading-relaxed">Terminates client TLS 1.3, absorbs volumetric DDoS, and serves 95% of static assets and cacheable API GET requests directly from RAM edge nodes.</p>
        </div>

        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="text-[10px] font-mono uppercase text-cyan-400 font-bold">FAILURE RECOVERY &amp; RESILIENCE</div>
          <div id="inspect-failure" class="text-slate-300 text-[11px] leading-relaxed">BGP Route Withdraw redirects ingress traffic to neighbor PoP in &lt; 2s.</div>
        </div>

        <div class="p-3 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-1">
          <div class="text-[10px] font-mono font-bold text-amber-400 flex items-center gap-1">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> STAFF ARCHITECT PRO-TIP
          </div>
          <p id="inspect-tip" class="text-[11px] text-slate-400 leading-relaxed">Use Cache-Control: s-maxage=3600, stale-while-revalidate=60 to decouple edge response latency from origin DB load.</p>
        </div>
      </div>
    </div>
  </div>
</div>
"""

FINOPS_HTML = """
<div class="space-y-6">
  <!-- Top Header & Preset Bar -->
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <h3 class="text-lg font-bold text-white font-mono tracking-tight">AWS FINOPS &amp; CAPACITY SIZING CALCULATOR</h3>
      </div>
      <p class="text-xs text-slate-400 mt-1 max-w-3xl">
        Model real-world cloud economics: calculate server sizing, Graviton3 ARM savings (-20%), Aurora Serverless v2, ElastiCache Redis, S3 Intelligent-Tiering, and the notorious NAT Gateway egress trap.
      </p>
    </div>
    <select id="cost-preset-selector" onchange="applyCostPreset(this.value)" class="bg-slate-950 text-slate-200 text-xs px-3 py-2 rounded-xl border border-slate-800 outline-none font-mono focus:border-emerald-400 transition-all cursor-pointer">
      <option value="twitter">X / Twitter Scale (500M DAU)</option>
      <option value="whatsapp">WhatsApp Messaging (2B DAU)</option>
      <option value="fintech">Fintech Payment Gateway (50M DAU)</option>
      <option value="ecommerce">E-Commerce Prime Day (100M DAU)</option>
      <option value="iot">IoT Telemetry Fleet (100M Devices)</option>
      <option value="custom">-- Custom Enterprise Scale --</option>
    </select>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- Left Column: Sizing Sliders & Architecture Toggles (5 Cols) -->
    <div class="lg:col-span-5 space-y-4">
      <!-- Scale Sliders Card -->
      <div class="bg-slate-950 rounded-2xl border border-slate-800 p-5 space-y-4">
        <div class="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center justify-between">
          <span>TRAFFIC &amp; WORKLOAD SCALE</span>
          <i data-lucide="sliders" class="w-3.5 h-3.5 text-slate-500"></i>
        </div>

        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Daily Active Users (DAU)</span>
            <span id="cost-lbl-dau" class="font-mono text-emerald-400 font-bold">500,000,000</span>
          </div>
          <input type="range" id="cost-dau" min="100000" max="1000000000" step="500000" value="500000000" oninput="recomputeCost()" class="w-full accent-emerald-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Requests / User / Day</span>
            <span id="cost-lbl-reqs" class="font-mono text-cyan-400 font-bold">35</span>
          </div>
          <input type="range" id="cost-reqs" min="1" max="200" step="1" value="35" oninput="recomputeCost()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Read : Write Ratio</span>
            <span id="cost-lbl-ratio" class="font-mono text-indigo-400 font-bold">20 : 1 (95% Reads)</span>
          </div>
          <input type="range" id="cost-ratio" min="1" max="50" step="1" value="20" oninput="recomputeCost()" class="w-full accent-indigo-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Avg Request Payload (KB)</span>
            <span id="cost-lbl-payload" class="font-mono text-amber-400 font-bold">2.0 KB</span>
          </div>
          <input type="range" id="cost-payload" min="0.5" max="50" step="0.5" value="2.0" oninput="recomputeCost()" class="w-full accent-amber-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Peak Traffic Headroom Multiplier</span>
            <span id="cost-lbl-peak" class="font-mono text-rose-400 font-bold">3.0&times; (Spike Safety)</span>
          </div>
          <input type="range" id="cost-peak" min="1.5" max="6.0" step="0.5" value="3.0" oninput="recomputeCost()" class="w-full accent-rose-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>
      </div>

      <!-- Cloud Architecture & FinOps Toggles Card -->
      <div class="bg-slate-950 rounded-2xl border border-slate-800 p-5 space-y-4">
        <div class="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center justify-between">
          <span>HARDWARE &amp; ARCHITECTURE TOGGLES</span>
          <span class="text-[10px] text-cyan-400 font-normal">Live Bill Impact</span>
        </div>

        <!-- 1. CPU Architecture -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-mono text-slate-400 font-bold">COMPUTE PROCESSOR</label>
          <div class="grid grid-cols-2 gap-2 text-xs font-mono">
            <button onclick="setArchToggle('cpu', 'graviton')" id="toggle-cpu-graviton" class="p-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold text-left transition-all cursor-pointer">
              <div>Graviton3 ARM64</div>
              <div class="text-[10px] text-emerald-400/80 font-normal">c7g.4xlarge (-20% $)</div>
            </button>
            <button onclick="setArchToggle('cpu', 'intel')" id="toggle-cpu-intel" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer">
              <div>Intel x86-64</div>
              <div class="text-[10px] text-slate-500 font-normal">c6i.4xlarge (Standard)</div>
            </button>
          </div>
        </div>

        <!-- 2. Database Tier -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-mono text-slate-400 font-bold">DATABASE TIER</label>
          <div class="grid grid-cols-2 gap-2 text-xs font-mono">
            <button onclick="setArchToggle('db', 'aurora')" id="toggle-db-aurora" class="p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-left transition-all cursor-pointer">
              <div>Aurora Serverless v2</div>
              <div class="text-[10px] text-cyan-400/80 font-normal">Auto-scaling ACUs</div>
            </button>
            <button onclick="setArchToggle('db', 'rds')" id="toggle-db-rds" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer">
              <div>Self-Hosted Multi-AZ</div>
              <div class="text-[10px] text-slate-500 font-normal">PostgreSQL + gp3 IOPS</div>
            </button>
          </div>
        </div>

        <!-- 3. S3 Storage Tiering -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-mono text-slate-400 font-bold">S3 OBJECT STORAGE TIER</label>
          <div class="grid grid-cols-2 gap-2 text-xs font-mono">
            <button onclick="setArchToggle('s3', 'intelligent')" id="toggle-s3-intelligent" class="p-2 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-bold text-left transition-all cursor-pointer">
              <div>Intelligent-Tiering</div>
              <div class="text-[10px] text-indigo-400/80 font-normal">Auto Deep Archive (-40%)</div>
            </button>
            <button onclick="setArchToggle('s3', 'standard')" id="toggle-s3-standard" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer">
              <div>Standard S3 Tier</div>
              <div class="text-[10px] text-slate-500 font-normal">$0.023 per GB/mo</div>
            </button>
          </div>
        </div>

        <!-- 4. NAT Gateway Egress Trap -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label class="text-[11px] font-mono text-slate-400 font-bold">NAT GATEWAY &amp; VPC ROUTING</label>
            <span class="text-[9px] font-mono text-rose-400 bg-rose-950/40 px-1.5 py-0.5 rounded border border-rose-800/40">Trap Alert</span>
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs font-mono">
            <button onclick="setArchToggle('nat', 'endpoint')" id="toggle-nat-endpoint" class="p-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold text-left transition-all cursor-pointer">
              <div>VPC Gateway Endpoints</div>
              <div class="text-[10px] text-emerald-400/80 font-normal">FREE S3/Dynamo Egress ($0)</div>
            </button>
            <button onclick="setArchToggle('nat', 'trap')" id="toggle-nat-trap" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer">
              <div>Default NAT Gateway</div>
              <div class="text-[10px] text-rose-400 font-normal">Charges $0.045/GB Fee!</div>
            </button>
          </div>
        </div>

        <!-- 5. Commitment Plan -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-mono text-slate-400 font-bold">AWS PRICING COMMITMENT</label>
          <div class="grid grid-cols-3 gap-1.5 text-xs font-mono">
            <button onclick="setArchToggle('plan', 'ondemand')" id="toggle-plan-ondemand" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-center transition-all cursor-pointer">
              <div>On-Demand</div>
              <div class="text-[9px] text-slate-500">0% Discount</div>
            </button>
            <button onclick="setArchToggle('plan', '1yr')" id="toggle-plan-1yr" class="p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-center transition-all cursor-pointer">
              <div>1-Yr Savings</div>
              <div class="text-[9px] text-cyan-400">38% Discount</div>
            </button>
            <button onclick="setArchToggle('plan', '3yr')" id="toggle-plan-3yr" class="p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-center transition-all cursor-pointer">
              <div>3-Yr Reserved</div>
              <div class="text-[9px] text-slate-500">54% Discount</div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Telemetry KPI Cards & Live Itemized Cloud Bill (7 Cols) -->
    <div class="lg:col-span-7 space-y-4">
      <!-- 4 Top KPI Sizing Telemetry Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
          <div class="text-[10px] font-mono text-slate-500 uppercase">Avg Read QPS</div>
          <div id="cost-res-readqps" class="text-base font-mono font-bold text-cyan-400 mt-0.5">192,708</div>
          <div class="text-[9px] font-mono text-slate-500 mt-1">95% Cache Hit Potential</div>
        </div>
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
          <div class="text-[10px] font-mono text-slate-500 uppercase">Peak QPS (3&times;)</div>
          <div id="cost-res-peakqps" class="text-base font-mono font-bold text-amber-400 mt-0.5">607,638</div>
          <div class="text-[9px] font-mono text-slate-500 mt-1">Sized for 3&sigma; spikes</div>
        </div>
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
          <div class="text-[10px] font-mono text-slate-500 uppercase">Egress Bandwidth</div>
          <div id="cost-res-egress" class="text-base font-mono font-bold text-indigo-400 mt-0.5">3.08 Gbps</div>
          <div class="text-[9px] font-mono text-slate-500 mt-1">Direct wire bandwidth</div>
        </div>
        <div class="p-3.5 rounded-xl bg-slate-950 border border-emerald-900/40 bg-emerald-950/10">
          <div class="text-[10px] font-mono text-emerald-400 uppercase">80/20 RAM Cache</div>
          <div id="cost-res-cache-ram" class="text-base font-mono font-bold text-emerald-400 mt-0.5">350.0 GB</div>
          <div class="text-[9px] font-mono text-emerald-400/80 mt-1">Hot working set</div>
        </div>
      </div>

      <!-- Itemized Monthly Bill Breakdown -->
      <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <span class="text-xs font-mono font-bold text-white uppercase tracking-wider">ESTIMATED AWS MONTHLY INFRASTRUCTURE BILL</span>
            <div id="cost-res-tco" class="text-[10px] text-slate-500 font-mono mt-0.5">Year 1 TCO: $218,400</div>
          </div>
          <div class="text-right">
            <span class="text-[10px] text-slate-500 font-mono uppercase">Total Monthly Spend</span>
            <div id="cost-res-total-bill" class="text-xl font-mono font-black text-emerald-400">$18,200 / mo</div>
          </div>
        </div>

        <div class="space-y-2 text-xs font-mono">
          <!-- 1. Compute -->
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div>
              <span class="text-white font-bold">1. App Tier Compute</span>
              <span id="cost-res-instances" class="text-slate-400 ml-2">(152x c7g.4xlarge Graviton3)</span>
            </div>
            <span id="cost-res-compute-bill" class="text-slate-200 font-bold">$10,480 / mo</span>
          </div>

          <!-- 2. Redis Cluster -->
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div>
              <span class="text-white font-bold">2. ElastiCache Redis / Valkey</span>
              <span id="cost-res-redis-nodes" class="text-slate-400 ml-2">(14x r7g.xlarge nodes)</span>
            </div>
            <span id="cost-res-redis-bill" class="text-slate-200 font-bold">$2,860 / mo</span>
          </div>

          <!-- 3. Database Tier -->
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div>
              <span class="text-white font-bold">3. Database Tier (Aurora v2 / gp3)</span>
              <span id="cost-res-db-details" class="text-slate-400 ml-2">(64 ACUs + 12K IOPS)</span>
            </div>
            <span id="cost-res-db-bill" class="text-slate-200 font-bold">$3,120 / mo</span>
          </div>

          <!-- 4. Storage S3 -->
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div>
              <span class="text-white font-bold">4. S3 Object Storage</span>
              <span id="cost-res-storage-tb" class="text-slate-400 ml-2">(63.9 TB / year)</span>
            </div>
            <span id="cost-res-storage-bill" class="text-slate-200 font-bold">$798 / mo</span>
          </div>

          <!-- 5. Egress Bandwidth -->
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div>
              <span class="text-white font-bold">5. Internet Data Egress</span>
              <span class="text-slate-400 ml-2">($0.05 / GB direct)</span>
            </div>
            <span id="cost-res-egress-bill" class="text-slate-200 font-bold">$942 / mo</span>
          </div>

          <!-- 6. NAT Gateway Trap -->
          <div id="cost-row-nat" class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div class="flex items-center gap-1.5">
              <span class="text-white font-bold">6. AWS NAT Gateway Processing</span>
              <span id="cost-res-nat-badge" class="text-[9px] px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">Bypassed ($0)</span>
            </div>
            <span id="cost-res-nat-bill" class="text-emerald-400 font-bold">$0 / mo</span>
          </div>
        </div>

        <!-- Staff+ Architecture Optimization Levers Card -->
        <div class="p-4 rounded-xl bg-slate-900/90 border border-cyan-500/20 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-mono font-bold text-cyan-400 flex items-center gap-1.5">
              <i data-lucide="zap" class="w-3.5 h-3.5"></i> STAFF+ ARCHITECTURE OPTIMIZATION LEVERS
            </span>
            <button onclick="applyStaffOptimizations()" class="px-2.5 py-1 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30 text-[11px] font-mono font-bold transition-all cursor-pointer">
              Apply All Levers
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 space-y-0.5">
              <div class="text-[10px] text-slate-400 font-bold">Graviton3 ARM Migration</div>
              <div id="finops-sav-graviton" class="text-emerald-400 font-bold">Saves ~$2,620 / mo (-20%)</div>
              <div class="text-[9px] text-slate-500">Zero code change for Go/Node/Python</div>
            </div>

            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 space-y-0.5">
              <div class="text-[10px] text-slate-400 font-bold">VPC S3 Gateway Endpoint</div>
              <div id="finops-sav-nat" class="text-emerald-400 font-bold">Saves ~$1,850 / mo ($0.045/GB)</div>
              <div class="text-[9px] text-slate-500">Route internal traffic away from NAT</div>
            </div>

            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 space-y-0.5">
              <div class="text-[10px] text-slate-400 font-bold">S3 Intelligent-Tiering</div>
              <div id="finops-sav-s3" class="text-emerald-400 font-bold">Saves ~$320 / mo (Auto Archive)</div>
              <div class="text-[9px] text-slate-500">Moves inactive objects to Glacier</div>
            </div>

            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 space-y-0.5">
              <div class="text-[10px] text-slate-400 font-bold">Cloudflare Edge &amp; Brotli</div>
              <div id="finops-sav-edge" class="text-emerald-400 font-bold">Saves ~$610 / mo (-65% Egress)</div>
              <div class="text-[9px] text-slate-500">Terminates 95% of reads at Edge PoP</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
"""

RING_HTML = """
<div class="space-y-6">
  <!-- Header Bar with Sub-Tab Switcher -->
  <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
        <h3 class="text-lg font-bold text-white font-mono tracking-tight">DISTRIBUTED SERVER DISTRIBUTION &amp; LOAD BALANCING ENGINE</h3>
      </div>
      <p class="text-xs text-slate-400 mt-1 max-w-3xl">
        Master two core architectural paradigms: <strong>Consistent Hash Ring</strong> (stateful storage/cache partitioning with &sigma; &prop; 1/&radic;V) and <strong>L4/L7 Traffic Balancer</strong> (stateless application request routing).
      </p>
    </div>

    <!-- Mode Selector: Hash Ring vs L4/L7 Balancer -->
    <div class="flex items-center gap-1.5 bg-slate-950 p-1 rounded-xl border border-white/[0.08] shrink-0">
      <button onclick="switchDistSubTab('ring')" id="btn-subtab-ring" class="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-1.5">
        <i data-lucide="circle-dot" class="w-3.5 h-3.5"></i> Consistent Hash Ring
      </button>
      <button onclick="switchDistSubTab('balancer')" id="btn-subtab-balancer" class="px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5">
        <i data-lucide="network" class="w-3.5 h-3.5"></i> L4/L7 Traffic Balancer
      </button>
    </div>
  </div>

  <!-- VIEW 1: CONSISTENT HASH RING (DYNAMO / CASSANDRA / REDIS) -->
  <div id="dist-view-ring" class="space-y-6">
    <!-- Action Bar -->
    <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950/70 p-3 rounded-2xl border border-white/[0.06]">
      <div class="flex items-center gap-2">
        <button onclick="addHashNodeLive()" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/25 transition-all flex items-center gap-1.5">
          <i data-lucide="server" class="w-3.5 h-3.5"></i> + Add Server Node
        </button>
        <button onclick="killRandomNodeLive()" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30 hover:bg-rose-500/25 transition-all flex items-center gap-1.5">
          <i data-lucide="flame" class="w-3.5 h-3.5"></i> Simulate Node Crash
        </button>
        <button onclick="scatterKeysLive(120)" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all">
          Scatter 120 Keys
        </button>
        <button onclick="resetHashCluster()" class="px-3 py-1.5 rounded-xl text-xs font-mono text-slate-400 hover:text-white border border-slate-800 transition-all">
          Reset Cluster
        </button>
      </div>

      <!-- Live Quality Indicator -->
      <div id="live-quality-badge" class="flex items-center gap-2 px-3 py-1 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 text-xs font-mono">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="live-quality-text">Uniform Distribution (&sigma; = 2.4%)</span>
      </div>
    </div>

    <!-- Main Grid: SVG Ring + Server Distribution Table -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Left Column: SVG Ring & Key Probe (Col 7) -->
      <div class="lg:col-span-7 space-y-4">
        <div class="bg-slate-950 rounded-2xl border border-white/[0.08] p-4 flex flex-col items-center justify-center relative overflow-hidden">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,#06b6d408_0%,transparent_70%)]"></div>
          
          <svg id="live-hash-ring-svg" viewBox="0 0 460 460" class="w-full max-w-[420px] h-auto relative z-10">
            <!-- Dynamic SVG injected by renderLiveHashRing() -->
          </svg>

          <!-- Ring Legend -->
          <div class="flex flex-wrap items-center justify-center gap-4 text-[10px] font-mono text-slate-400 mt-2 z-10">
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full border-2 border-white bg-slate-900"></span>
              <span>Physical Server</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
              <span>Virtual Node (vnode)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>Partitioned Key Dot</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-0.5 bg-rose-400"></span>
              <span>Clockwise Routing Arc</span>
            </div>
          </div>
        </div>

        <!-- Interactive Key Routing Probe Card -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-3">
          <div class="flex items-center justify-between text-xs font-mono font-bold text-slate-300">
            <span class="flex items-center gap-2">
              <i data-lucide="crosshair" class="w-3.5 h-3.5 text-cyan-400"></i> INTERACTIVE KEY ROUTING PROBE
            </span>
            <span class="text-[10px] text-slate-500 font-normal">Deterministic FNV-1a Hash Space</span>
          </div>

          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <input type="text" id="probe-key-input" value="user_profile:94821" placeholder="Enter key (e.g. user:109, cart:441)..." 
                class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-mono text-white focus:outline-none focus:border-cyan-400 transition-all">
            </div>
            <button onclick="probeSpecificKey()" class="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-all flex items-center gap-1.5 shrink-0">
              <i data-lucide="search" class="w-3.5 h-3.5"></i> Route Key
            </button>
            <button onclick="probeRandomKey()" class="px-3 py-2 rounded-xl text-xs font-mono bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-all shrink-0">
              Random Probe
            </button>
          </div>

          <!-- Probe Diagnostic Telemetry Result -->
          <div id="probe-result-box" class="p-3 rounded-xl bg-slate-900/90 border border-cyan-500/20 text-xs font-mono space-y-1 text-slate-300">
            <div class="text-cyan-400 font-bold flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
              <span id="probe-res-status">Probe ready. Click "Route Key" to trace hash coordinate.</span>
            </div>
            <div id="probe-res-details" class="text-[11px] text-slate-400 flex flex-wrap gap-x-4 gap-y-1"></div>
          </div>
        </div>
      </div>

      <!-- Right Column: Distribution Table & Control Sliders (Col 5) -->
      <div class="lg:col-span-5 space-y-4">
        <!-- Vnodes Slider -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
          <div class="flex justify-between items-center text-xs">
            <span class="text-slate-300 font-mono font-bold">Virtual Nodes (vnodes / server)</span>
            <span id="live-lbl-vnodes" class="font-mono text-cyan-400 font-bold px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20">15 vnodes</span>
          </div>
          <input type="range" id="live-input-vnodes" min="1" max="40" step="1" value="15" oninput="changeLiveVNodes(this.value)" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
          <div class="flex justify-between text-[10px] font-mono text-slate-500">
            <span>1 vnode (Severe Skew)</span>
            <span>15 (Balanced)</span>
            <span>40 (&sigma; &rarr; 0)</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-snug pt-1">
            <strong>First Principles:</strong> Higher virtual nodes interleave shard coordinates across the 360&deg; circle, eliminating hot spots without physical server over-provisioning.
          </p>
        </div>

        <!-- SERVER DISTRIBUTION Table -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-3">
          <div class="flex justify-between items-center text-xs font-mono font-bold text-white border-b border-slate-800 pb-2">
            <span class="flex items-center gap-2">
              <i data-lucide="layers" class="w-3.5 h-3.5 text-emerald-400"></i> SERVER DISTRIBUTION
            </span>
            <span id="live-lbl-keycount" class="text-emerald-400 font-bold">120 Keys Distributed</span>
          </div>

          <!-- Dynamic Server Rows -->
          <div id="live-hash-nodes-list" class="space-y-2.5 max-h-80 overflow-y-auto custom-scroll pr-1">
            <!-- Dynamically populated by renderLiveHashRing() -->
          </div>
        </div>

        <!-- Cluster Event Migration Log -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
          <div class="flex justify-between items-center text-xs font-mono text-slate-400 border-b border-slate-800/80 pb-1.5">
            <span>CLUSTER REBALANCING LOG</span>
            <span class="text-[10px] text-cyan-400">Minimal K/N Rehash</span>
          </div>
          <div id="live-cluster-event-log" class="text-[11px] font-mono space-y-1 text-slate-400 max-h-32 overflow-y-auto custom-scroll">
            <div class="text-emerald-400">[READY] Cluster initialized with 4 primary nodes &amp; 60 virtual partitions.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- VIEW 2: L4/L7 APPLICATION TRAFFIC BALANCER (ENVOY / IPVS) -->
  <div id="dist-view-balancer" class="hidden space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950/70 p-3 rounded-2xl border border-white/[0.06]">
      <div class="flex items-center gap-3">
        <span class="text-xs font-mono text-slate-400">Balancing Algorithm:</span>
        <select id="lb-algo-select" onchange="changeLbAlgo(this.value)" class="bg-slate-900 text-cyan-300 text-xs px-3 py-1.5 rounded-xl border border-slate-700 outline-none font-mono">
          <option value="round-robin">Round Robin (Uniform Sequential)</option>
          <option value="weighted">Weighted Round Robin (Capacity 4:2:1:1)</option>
          <option value="least-conn">Least Connections (Dynamic Concurrency)</option>
          <option value="power-of-two">Power of Two Random Choices (P2C - Lowest Queue)</option>
          <option value="ip-hash">IP Hash / Consistent Session Affinity</option>
        </select>
      </div>

      <div class="flex items-center gap-2">
        <button onclick="sendLbRequest(1)" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-all">
          Send 1 Request
        </button>
        <button onclick="sendLbRequest(20)" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-indigo-500 hover:bg-indigo-400 text-white transition-all">
          Fire 20 Burst
        </button>
        <button onclick="sendLbRequest(100)" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all">
          100 QPS Spike
        </button>
        <button onclick="toggleLbLag()" id="btn-toggle-lag" class="px-3 py-1.5 rounded-xl text-xs font-mono text-amber-300 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 transition-all">
          Inject Slowdown on Node 3
        </button>
      </div>
    </div>

    <!-- Backend Web Tier Servers Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- App Server 1 -->
      <div id="lb-srv-0" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3 transition-all">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            <span class="text-xs font-mono font-bold text-white">app-pod-01</span>
          </div>
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">Weight 4x</span>
        </div>
        <div class="text-slate-400 text-[11px] font-mono">10.0.2.11:8080 &bull; c6i.2xlarge</div>
        <div class="space-y-1">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Active Conns:</span>
            <span id="lb-conn-0" class="text-white font-bold">0</span>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div id="lb-bar-0" class="h-full bg-cyan-400 rounded-full transition-all duration-300" style="width: 0%;"></div>
          </div>
        </div>
        <div class="flex justify-between items-center text-xs font-mono pt-1 border-t border-slate-800/80">
          <span class="text-slate-400">Total Served:</span>
          <span id="lb-total-0" class="text-cyan-400 font-bold">0 reqs</span>
        </div>
      </div>

      <!-- App Server 2 -->
      <div id="lb-srv-1" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3 transition-all">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            <span class="text-xs font-mono font-bold text-white">app-pod-02</span>
          </div>
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Weight 2x</span>
        </div>
        <div class="text-slate-400 text-[11px] font-mono">10.0.2.12:8080 &bull; c6i.xlarge</div>
        <div class="space-y-1">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Active Conns:</span>
            <span id="lb-conn-1" class="text-white font-bold">0</span>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div id="lb-bar-1" class="h-full bg-emerald-400 rounded-full transition-all duration-300" style="width: 0%;"></div>
          </div>
        </div>
        <div class="flex justify-between items-center text-xs font-mono pt-1 border-t border-slate-800/80">
          <span class="text-slate-400">Total Served:</span>
          <span id="lb-total-1" class="text-emerald-400 font-bold">0 reqs</span>
        </div>
      </div>

      <!-- App Server 3 (Can have lag injected) -->
      <div id="lb-srv-2" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3 transition-all">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span id="lb-dot-2" class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
            <span class="text-xs font-mono font-bold text-white">app-pod-03</span>
          </div>
          <span id="lb-badge-2" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">Weight 1x</span>
        </div>
        <div class="text-slate-400 text-[11px] font-mono">10.0.2.13:8080 &bull; c6i.large</div>
        <div class="space-y-1">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Active Conns:</span>
            <span id="lb-conn-2" class="text-white font-bold">0</span>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div id="lb-bar-2" class="h-full bg-amber-400 rounded-full transition-all duration-300" style="width: 0%;"></div>
          </div>
        </div>
        <div class="flex justify-between items-center text-xs font-mono pt-1 border-t border-slate-800/80">
          <span class="text-slate-400">Total Served:</span>
          <span id="lb-total-2" class="text-amber-400 font-bold">0 reqs</span>
        </div>
      </div>

      <!-- App Server 4 -->
      <div id="lb-srv-3" class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3 transition-all">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-fuchsia-400"></span>
            <span class="text-xs font-mono font-bold text-white">app-pod-04</span>
          </div>
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-fuchsia-500/10 text-fuchsia-400 border border-fuchsia-500/20">Weight 1x</span>
        </div>
        <div class="text-slate-400 text-[11px] font-mono">10.0.2.14:8080 &bull; c6i.large</div>
        <div class="space-y-1">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Active Conns:</span>
            <span id="lb-conn-3" class="text-white font-bold">0</span>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div id="lb-bar-3" class="h-full bg-fuchsia-400 rounded-full transition-all duration-300" style="width: 0%;"></div>
          </div>
        </div>
        <div class="flex justify-between items-center text-xs font-mono pt-1 border-t border-slate-800/80">
          <span class="text-slate-400">Total Served:</span>
          <span id="lb-total-3" class="text-fuchsia-400 font-bold">0 reqs</span>
        </div>
      </div>
    </div>

    <!-- Live Traffic Dispatch Terminal -->
    <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
      <div class="flex justify-between items-center text-xs font-mono text-slate-400 border-b border-slate-800/80 pb-2">
        <span class="text-white font-bold flex items-center gap-2">
          <i data-lucide="terminal" class="w-3.5 h-3.5 text-cyan-400"></i> ENVOY PROXY ACCESS LOG
        </span>
        <button onclick="clearLbLogs()" class="text-[10px] text-slate-500 hover:text-slate-300 transition-all">Clear Terminal</button>
      </div>
      <div id="lb-terminal-log" class="text-[11px] font-mono space-y-1 text-slate-400 max-h-40 overflow-y-auto custom-scroll">
        <div class="text-slate-600">[READY] Envoy proxy listening on VIP 192.168.1.100:443 (HTTP/2 &bull; TLS 1.3)</div>
      </div>
    </div>
  </div>
</div>
"""

LIMITER_HTML = """
<div class="space-y-6">
  <!-- Header Bar with Algorithm & Tier Selectors -->
  <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-rose-400 animate-pulse"></span>
        <h3 class="text-lg font-bold text-white font-mono tracking-tight">DISTRIBUTED RATE LIMITER &amp; QUOTA MANAGEMENT STUDIO</h3>
      </div>
      <p class="text-xs text-slate-400 mt-1 max-w-3xl">
        High-scale distributed throttling architecture: Token Bucket physics, Leaky Bucket traffic shaping, Sliding Window counter mathematics, atomic Redis Lua script execution, and RFC 6585 HTTP header contracts.
      </p>
    </div>

    <!-- Algorithm and Tenant Controls -->
    <div class="flex flex-wrap items-center gap-2 shrink-0">
      <!-- Tenant Selector -->
      <div class="flex items-center gap-1.5 bg-slate-950 px-2.5 py-1 rounded-xl border border-white/[0.08]">
        <span class="text-[10px] font-mono text-slate-500 uppercase">Tenant:</span>
        <select id="rl-tenant-select" onchange="switchRlTenant(this.value)" class="bg-transparent text-xs font-mono font-bold text-cyan-400 outline-none cursor-pointer">
          <option value="free" class="bg-slate-950 text-cyan-400">Free Tier (15 burst &bull; 2/s)</option>
          <option value="pro" selected class="bg-slate-950 text-emerald-400">Pro Tier (60 burst &bull; 10/s)</option>
          <option value="enterprise" class="bg-slate-950 text-purple-400">Enterprise Tier (200 burst &bull; 40/s)</option>
          <option value="ddos" class="bg-slate-950 text-rose-400">Quarantined Botnet (0 burst &bull; 0/s)</option>
        </select>
      </div>

      <!-- Algorithm Selector -->
      <div class="flex items-center gap-1.5 bg-slate-950 px-2.5 py-1 rounded-xl border border-white/[0.08]">
        <span class="text-[10px] font-mono text-slate-500 uppercase">Algo:</span>
        <select id="live-rl-algo" onchange="switchRlAlgo(this.value)" class="bg-transparent text-xs font-mono font-bold text-amber-400 outline-none cursor-pointer">
          <option value="token-bucket" selected class="bg-slate-950 text-white">Token Bucket (Stripe / AWS / GitHub)</option>
          <option value="leaky-bucket" class="bg-slate-950 text-white">Leaky Bucket (Traffic Shaping / NGINX)</option>
          <option value="sliding-window" class="bg-slate-950 text-white">Sliding Window Counter (Cloudflare / Twitter)</option>
          <option value="fixed-window" class="bg-slate-950 text-white">Fixed Window Counter (Memcached INCR)</option>
        </select>
      </div>
    </div>
  </div>

  <!-- Real-Time Metrics & Control Bar -->
  <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950/70 p-3 rounded-2xl border border-white/[0.06]">
    <div class="flex flex-wrap items-center gap-2">
      <button onclick="sendLiveRlReq(1)" class="px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/25 transition-all flex items-center gap-1.5">
        <i data-lucide="play" class="w-3.5 h-3.5"></i> Send 1 Req
      </button>
      <button onclick="sendLiveRlReq(5)" class="px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/25 transition-all flex items-center gap-1.5">
        <i data-lucide="zap" class="w-3.5 h-3.5"></i> Fire 5 Burst
      </button>
      <button onclick="sendLiveRlReq(25)" class="px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30 hover:bg-amber-500/25 transition-all flex items-center gap-1.5">
        <i data-lucide="flame" class="w-3.5 h-3.5"></i> 25 Req Spike
      </button>
      <button onclick="toggleContinuousTraffic()" id="btn-continuous-traffic" class="px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-indigo-500/15 text-indigo-400 border border-indigo-500/30 hover:bg-indigo-500/25 transition-all flex items-center gap-1.5">
        <i data-lucide="activity" class="w-3.5 h-3.5"></i> <span id="lbl-continuous-traffic">Auto 15 QPS</span>
      </button>
      <button onclick="triggerDdosAttack()" class="px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30 hover:bg-rose-500/25 transition-all flex items-center gap-1.5">
        <i data-lucide="shield-alert" class="w-3.5 h-3.5"></i> 100-Req DDoS Surge
      </button>
      <button onclick="resetRlState()" class="px-2.5 py-1.5 rounded-xl text-xs font-mono text-slate-400 hover:text-white border border-slate-800 transition-all">
        Reset
      </button>
    </div>

    <!-- Live Telemetry Counts -->
    <div class="flex items-center gap-3 text-xs font-mono">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span class="text-slate-400">200 OK:</span>
        <span id="rl-stat-ok" class="text-emerald-400 font-bold">0</span>
      </div>
      <div class="h-3 w-px bg-slate-800"></div>
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-rose-400"></span>
        <span class="text-slate-400">429 Throttled:</span>
        <span id="rl-stat-throttled" class="text-rose-400 font-bold">0</span>
      </div>
      <div class="h-3 w-px bg-slate-800"></div>
      <div class="flex items-center gap-1.5">
        <span class="text-slate-400">Total QPS:</span>
        <span id="rl-stat-qps" class="text-cyan-400 font-bold">0.0 req/s</span>
      </div>
    </div>
  </div>

  <!-- Primary Working Grid -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- Left Column: Physics Simulator SVG & Algorithm Explanation (Col 7) -->
    <div class="lg:col-span-7 space-y-4">
      <!-- Animated Visualizer Box -->
      <div class="bg-slate-950 rounded-2xl border border-white/[0.08] p-4 flex flex-col items-center justify-center relative overflow-hidden">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,#f43f5e08_0%,transparent_70%)]"></div>
        
        <svg id="live-rl-physics-svg" viewBox="0 0 520 280" class="w-full max-w-[500px] h-auto relative z-10">
          <!-- Dynamic physics animation injected by renderRlPhysicsSVG() -->
        </svg>

        <!-- Capacity & Refill Status Banner below SVG -->
        <div class="w-full flex items-center justify-between pt-3 border-t border-slate-800/80 text-xs font-mono z-10 mt-1">
          <div class="flex items-center gap-2">
            <span class="text-slate-400" id="rl-algo-capacity-label">Bucket Capacity:</span>
            <span id="rl-stat-capacity" class="font-bold text-white">60 Tokens</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-slate-400" id="rl-algo-refill-label">Refill Rate:</span>
            <span id="rl-stat-refill" class="font-bold text-cyan-400">10.0 / sec</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-slate-400">Current Level:</span>
            <span id="live-rl-meter-text" class="font-bold text-emerald-400">60.0 / 60</span>
          </div>
        </div>
      </div>

      <!-- Real-Time Throughput / 429 Rolling Chart -->
      <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
        <div class="flex items-center justify-between text-xs font-mono font-bold text-slate-300">
          <span class="flex items-center gap-2">
            <i data-lucide="bar-chart-2" class="w-3.5 h-3.5 text-cyan-400"></i> ROLLING 20-SECOND THROUGHPUT SPECTRUM
          </span>
          <span class="text-[10px] text-slate-500 font-normal">
            <span class="text-emerald-400 font-bold">&#9632; 200 OK</span> &bull; 
            <span class="text-rose-400 font-bold">&#9632; 429 Throttled</span>
          </span>
        </div>
        <svg id="rl-rolling-chart-svg" viewBox="0 0 500 70" class="w-full h-16 bg-slate-900/60 rounded-xl border border-slate-800 p-1">
          <!-- Populated dynamically by updateRollingChart() -->
        </svg>
      </div>

      <!-- Algorithm Deep Dive & Mathematical Formula -->
      <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
        <div class="flex items-center justify-between text-xs font-mono font-bold text-white border-b border-slate-800 pb-2">
          <span id="rl-algo-title" class="text-cyan-400">TOKEN BUCKET ARCHITECTURAL MATHEMATICS</span>
          <span id="rl-algo-standard" class="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">Stripe / Amazon Standard</span>
        </div>
        <div id="rl-algo-formula-box" class="p-2.5 rounded-xl bg-slate-900 border border-slate-800/80 font-mono text-xs text-amber-300">
          <!-- Formula text -->
        </div>
        <p id="rl-algo-explanation" class="text-xs text-slate-300 leading-relaxed pt-1">
          <!-- Explanation text -->
        </p>
      </div>
    </div>

    <!-- Right Column: RFC 6585 Headers & Redis Lua Execution (Col 5) -->
    <div class="lg:col-span-5 space-y-4">
      <!-- Live RFC 6585 / draft-ietf-httpapi-ratelimit HTTP Response Inspector -->
      <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2.5">
        <div class="flex items-center justify-between text-xs font-mono font-bold text-white border-b border-slate-800 pb-2">
          <span class="flex items-center gap-1.5">
            <i data-lucide="globe" class="w-3.5 h-3.5 text-cyan-400"></i> LIVE HTTP GATEWAY RESPONSE
          </span>
          <span id="rl-http-status-pill" class="text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
            HTTP 200 OK
          </span>
        </div>

        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 font-mono text-xs space-y-1.5 text-slate-300">
          <div class="flex justify-between border-b border-slate-800/60 pb-1 text-[11px]">
            <span class="text-slate-500">Status Code:</span>
            <span id="rl-res-code" class="text-emerald-400 font-bold">200 OK (Allowed)</span>
          </div>
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">X-RateLimit-Limit:</span>
            <span id="rl-res-limit" class="text-white font-bold">60</span>
          </div>
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">X-RateLimit-Remaining:</span>
            <span id="rl-res-remaining" class="text-cyan-400 font-bold">59</span>
          </div>
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">X-RateLimit-Reset:</span>
            <span id="rl-res-reset" class="text-slate-300">1727439600 (in 60s)</span>
          </div>
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">Retry-After:</span>
            <span id="rl-res-retry" class="text-slate-500">0s (Quota Available)</span>
          </div>
          <div class="flex justify-between text-[11px] pt-1 border-t border-slate-800/60">
            <span class="text-slate-400">RateLimit-Policy:</span>
            <span id="rl-res-policy" class="text-amber-400 text-[10px]">"60;w=60;burst=60"</span>
          </div>
        </div>
      </div>

      <!-- Redis Cluster State & Atomic Lua Inspector -->
      <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2.5">
        <div class="flex items-center justify-between text-xs font-mono font-bold text-white border-b border-slate-800 pb-2">
          <span class="flex items-center gap-1.5">
            <i data-lucide="database" class="w-3.5 h-3.5 text-rose-400"></i> REDIS IN-MEMORY STATE
          </span>
          <button onclick="toggleLuaScriptModal()" id="btn-toggle-lua" class="text-[10px] px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 hover:bg-rose-500/20 border border-rose-500/30 transition-all">
            View Lua Script
          </button>
        </div>

        <!-- Redis Key Telemetry Box -->
        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 font-mono text-[11px] space-y-1 text-slate-300">
          <div class="flex justify-between">
            <span class="text-slate-500">Redis Hash Key:</span>
            <span id="rl-redis-key" class="text-rose-400 font-bold truncate max-w-[200px]">ratelimit:pro_team9</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">HGET tokens:</span>
            <span id="rl-redis-tokens" class="text-emerald-400 font-bold">59.00</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">HGET last_refilled:</span>
            <span id="rl-redis-last" class="text-white">1727439540.100</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">TTL Remaining:</span>
            <span id="rl-redis-ttl" class="text-cyan-400">59s</span>
          </div>
        </div>

        <!-- Collapsible Lua Script Code -->
        <div id="rl-lua-code-container" class="hidden p-3 rounded-xl bg-black border border-slate-800 font-mono text-[10px] space-y-1 overflow-x-auto text-emerald-300 max-h-48 custom-scroll">
<pre>-- Atomic Token Bucket Lua Script
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local state = redis.call('HMGET', key, 'tokens', 'last_updated')
local tokens = tonumber(state[1])
local last_updated = tonumber(state[2])

if not tokens then
  tokens = capacity
  last_updated = now
else
  local elapsed = math.max(0, now - last_updated)
  tokens = math.min(capacity, tokens + (elapsed * refill_rate))
  last_updated = now
end

if tokens >= requested then
  tokens = tokens - requested
  redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
  redis.call('EXPIRE', key, math.ceil(capacity / refill_rate))
  return {1, tokens} -- ALLOWED (1)
else
  redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
  return {0, tokens} -- THROTTLED (0)
end</pre>
        </div>
      </div>

      <!-- Real-time Gateway Terminal Logs -->
      <div class="p-4 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-2">
        <div class="flex items-center justify-between text-xs font-mono text-slate-400 border-b border-slate-800/80 pb-2">
          <span class="text-white font-bold flex items-center gap-1.5">
            <i data-lucide="terminal" class="w-3.5 h-3.5 text-cyan-400"></i> ENVOY &amp; API GATEWAY AUDIT LOG
          </span>
          <button onclick="clearLiveRlLogs()" class="text-[10px] text-slate-500 hover:text-slate-300 transition-all">Clear</button>
        </div>
        <div id="live-rl-terminal" class="text-[11px] font-mono space-y-1 text-slate-400 max-h-36 overflow-y-auto custom-scroll">
          <div class="text-slate-500">[System Ready] Rate limiter initialized. Algorithm: Token Bucket (Redis Lua).</div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

INTERVIEW_HTML = """
<div class="space-y-6">
  <!-- Top Header with Problem Selector & 45-Min Timer -->
  <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span>
        <h3 class="text-lg font-bold text-white font-mono tracking-tight">STAFF+ SYSTEM DESIGN INTERVIEW SIMULATOR (FAANG L6/L7 &amp; Principal)</h3>
      </div>
      <p class="text-xs text-slate-400 mt-1 max-w-3xl">
        Elite 45-minute simulation environment: 8 FAANG prompt archetypes, interactive 5-phase framework, real-time capacity calculator, interviewer curveball challenges, and official FAANG L6/L7 evaluation rubrics.
      </p>
    </div>

    <!-- Right Controls: Problem Picker & Clock -->
    <div class="flex flex-wrap items-center gap-3 shrink-0">
      <!-- Problem Dropdown -->
      <div class="flex items-center gap-1.5 bg-slate-950 px-3 py-1.5 rounded-xl border border-white/[0.08]">
        <span class="text-[10px] font-mono text-slate-500 uppercase">Prompt:</span>
        <select id="interview-problem-select" onchange="switchInterviewProblem(this.value)" class="bg-transparent text-xs font-mono font-bold text-amber-400 outline-none cursor-pointer max-w-[220px]">
          <option value="stripe" selected class="bg-slate-950 text-white">Stripe: Global Payment Engine</option>
          <option value="tiktok" class="bg-slate-950 text-white">TikTok: 50M Live Stream Chat</option>
          <option value="s3" class="bg-slate-950 text-white">AWS S3: Exabyte Object Store</option>
          <option value="uber" class="bg-slate-950 text-white">Uber: Geospatial Driver Matching</option>
          <option value="tinyurl" class="bg-slate-950 text-white">TinyURL: Global URL Shortener</option>
          <option value="docs" class="bg-slate-950 text-white">Google Docs: Real-Time CRDT</option>
          <option value="crawler" class="bg-slate-950 text-white">Googlebot: Distributed Web Crawler</option>
          <option value="temporal" class="bg-slate-950 text-white">Temporal: Distributed Workflow Engine</option>
        </select>
      </div>

      <!-- 45-Min Timer Display & Controller -->
      <div class="flex items-center gap-2 bg-slate-950 px-3 py-1 rounded-xl border border-white/[0.08]">
        <div id="studio-timer-display" class="font-mono text-xl font-black text-emerald-400 tracking-wider">45:00</div>
        <button onclick="toggleStudioTimer()" id="btn-studio-timer" class="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all">
          Start
        </button>
        <button onclick="resetStudioTimer()" class="px-2.5 py-1.5 rounded-lg text-xs font-mono text-slate-400 hover:text-white border border-slate-800 transition-all">
          Reset
        </button>
      </div>
    </div>
  </div>

  <!-- Studio Sub-Navigation Tabs -->
  <div class="flex items-center justify-between gap-2 border-b border-slate-800 pb-3 overflow-x-auto no-scrollbar">
    <div class="flex items-center gap-1.5 shrink-0">
      <button onclick="switchStudioSubTab('framework')" id="tab-studio-framework" class="studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-amber-500 text-slate-950 transition-all flex items-center gap-1.5 shadow-lg shadow-amber-500/10">
        <i data-lucide="compass" class="w-3.5 h-3.5"></i> <span>5-Phase Master Framework</span>
      </button>
      <button onclick="switchStudioSubTab('calculator')" id="tab-studio-calculator" class="studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5">
        <i data-lucide="calculator" class="w-3.5 h-3.5"></i> <span>Capacity Math Engine</span>
      </button>
      <button onclick="switchStudioSubTab('curveballs')" id="tab-studio-curveballs" class="studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5">
        <i data-lucide="zap" class="w-3.5 h-3.5"></i> <span>Interviewer Grilling &amp; Curveballs</span>
      </button>
      <button onclick="switchStudioSubTab('rubric')" id="tab-studio-rubric" class="studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5">
        <i data-lucide="award" class="w-3.5 h-3.5"></i> <span>FAANG L6/L7 Rubric &amp; Level Predictor</span>
      </button>
      <button onclick="switchStudioSubTab('notes')" id="tab-studio-notes" class="studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5">
        <i data-lucide="edit-3" class="w-3.5 h-3.5"></i> <span>Candidate Solution Scratchpad</span>
      </button>
    </div>

    <!-- Active Phase Badge -->
    <div id="studio-active-phase-pill" class="text-[11px] font-mono font-bold px-3 py-1 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shrink-0">
      PHASE 1: SCOPE &amp; BOUNDARIES (0-5m)
    </div>
  </div>

  <!-- SUB-VIEW 1: 5-PHASE MASTER FRAMEWORK -->
  <div id="subview-studio-framework" class="space-y-6">
    <!-- 5 Phase Stepper Header -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-2.5">
      <div onclick="jumpToPhase(1)" id="phase-card-1" class="phase-step-btn p-3 rounded-xl border bg-cyan-500/10 border-cyan-500/40 text-cyan-300 cursor-pointer transition-all space-y-1">
        <div class="flex items-center justify-between text-[10px] font-mono font-bold">
          <span>PHASE 1</span>
          <span>00:00 - 05:00</span>
        </div>
        <div class="text-xs font-bold text-white">Clarify &amp; Scope</div>
        <div class="text-[10px] text-slate-400 truncate">Functional &amp; Non-Functional</div>
      </div>

      <div onclick="jumpToPhase(2)" id="phase-card-2" class="phase-step-btn p-3 rounded-xl border bg-slate-950 border-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all space-y-1">
        <div class="flex items-center justify-between text-[10px] font-mono font-bold">
          <span>PHASE 2</span>
          <span>05:00 - 12:00</span>
        </div>
        <div class="text-xs font-bold text-white">Capacity &amp; APIs</div>
        <div class="text-[10px] text-slate-400 truncate">QPS, Storage, REST/gRPC</div>
      </div>

      <div onclick="jumpToPhase(3)" id="phase-card-3" class="phase-step-btn p-3 rounded-xl border bg-slate-950 border-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all space-y-1">
        <div class="flex items-center justify-between text-[10px] font-mono font-bold">
          <span>PHASE 3</span>
          <span>12:00 - 25:00</span>
        </div>
        <div class="text-xs font-bold text-white">High-Level Design</div>
        <div class="text-[10px] text-slate-400 truncate">End-to-End Topology &amp; DB</div>
      </div>

      <div onclick="jumpToPhase(4)" id="phase-card-4" class="phase-step-btn p-3 rounded-xl border bg-slate-950 border-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all space-y-1">
        <div class="flex items-center justify-between text-[10px] font-mono font-bold">
          <span>PHASE 4</span>
          <span>25:00 - 40:00</span>
        </div>
        <div class="text-xs font-bold text-white">Deep-Dive &amp; Scale</div>
        <div class="text-[10px] text-slate-400 truncate">Bottlenecks &amp; Concurrency</div>
      </div>

      <div onclick="jumpToPhase(5)" id="phase-card-5" class="phase-step-btn p-3 rounded-xl border bg-slate-950 border-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all space-y-1">
        <div class="flex items-center justify-between text-[10px] font-mono font-bold">
          <span>PHASE 5</span>
          <span>40:00 - 45:00</span>
        </div>
        <div class="text-xs font-bold text-white">Trade-offs &amp; Wrap</div>
        <div class="text-[10px] text-slate-400 truncate">RPO/RTO, SLIs &amp; Defense</div>
      </div>
    </div>

    <!-- Active Problem Blueprint Specification Banner -->
    <div class="p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div>
          <span id="interview-active-tag" class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">
            FAANG ARCHETYPE: GLOBAL PAYMENTS
          </span>
          <h3 id="interview-problem-title" class="text-base font-bold text-white font-mono mt-1">Design a Distributed Global Payment Engine (Stripe / Adyen)</h3>
        </div>
        <div class="flex items-center gap-2">
          <span id="interview-problem-target" class="text-xs font-mono text-cyan-400 font-bold bg-cyan-950/30 px-3 py-1 rounded-xl border border-cyan-500/20">
            Target Scale: 10,000 TPS &bull; 99.999% SLA
          </span>
        </div>
      </div>

      <!-- Problem Phase Content Dynamic Container -->
      <div id="interview-phase-dynamic-body" class="space-y-4 text-xs font-mono text-slate-300">
        <!-- Dynamically injected by renderInterviewPhaseContent() -->
      </div>
    </div>
  </div>

  <!-- SUB-VIEW 2: BACK-OF-THE-ENVELOPE CAPACITY CALCULATOR -->
  <div id="subview-studio-calculator" class="hidden space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Input Sliders (Col 6) -->
      <div class="lg:col-span-6 p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2 text-xs font-mono font-bold text-white">
          <span class="flex items-center gap-1.5"><i data-lucide="sliders" class="w-3.5 h-3.5 text-cyan-400"></i> TRAFFIC &amp; STORAGE ASSUMPTIONS</span>
          <button onclick="applyInterviewCalcPreset()" class="text-[10px] text-cyan-400 hover:text-cyan-300">Load Problem Defaults</button>
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Daily Active Users (DAU):</span>
            <span id="calc-val-dau" class="text-white font-bold">100,000,000</span>
          </div>
          <input type="range" id="calc-in-dau" min="1000000" max="1000000000" step="1000000" value="100000000" oninput="recalcInterviewMath()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Actions per User per Day:</span>
            <span id="calc-val-actions" class="text-white font-bold">20</span>
          </div>
          <input type="range" id="calc-in-actions" min="1" max="100" step="1" value="20" oninput="recalcInterviewMath()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Read / Write Ratio:</span>
            <span id="calc-val-ratio" class="text-cyan-400 font-bold">10 : 1 (91% Reads)</span>
          </div>
          <input type="range" id="calc-in-ratio" min="1" max="100" step="1" value="10" oninput="recalcInterviewMath()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Payload Size per Record:</span>
            <span id="calc-val-payload" class="text-white font-bold">2.0 KB</span>
          </div>
          <input type="range" id="calc-in-payload" min="0.1" max="50" step="0.5" value="2.0" oninput="recalcInterviewMath()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-400">Peak Traffic Multiplier:</span>
            <span id="calc-val-peak" class="text-rose-400 font-bold">3.0x</span>
          </div>
          <input type="range" id="calc-in-peak" min="1.5" max="6.0" step="0.5" value="3.0" oninput="recalcInterviewMath()" class="w-full accent-rose-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>
      </div>

      <!-- Computed Results Grid (Col 6) -->
      <div class="lg:col-span-6 p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2 text-xs font-mono font-bold text-white">
          <span class="flex items-center gap-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-400"></i> DERIVED FAANG INFRASTRUCTURE SIZING</span>
          <button onclick="copyCalcSummaryToNotes()" class="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 hover:bg-cyan-500/20">
            Copy to Notes
          </button>
        </div>

        <div class="grid grid-cols-2 gap-3 text-xs font-mono">
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <div class="text-slate-500 text-[10px]">AVG WRITE QPS</div>
            <div id="calc-res-write-qps" class="text-base font-bold text-white">2,108 req/s</div>
            <div id="calc-res-peak-write" class="text-[10px] text-rose-400 font-bold">Peak: 6,324 req/s</div>
          </div>

          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <div class="text-slate-500 text-[10px]">AVG READ QPS</div>
            <div id="calc-res-read-qps" class="text-base font-bold text-white">21,080 req/s</div>
            <div id="calc-res-peak-read" class="text-[10px] text-cyan-400 font-bold">Peak: 63,240 req/s</div>
          </div>

          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <div class="text-slate-500 text-[10px]">STORAGE (1 YEAR / 5 YEARS)</div>
            <div id="calc-res-storage-1yr" class="text-base font-bold text-amber-400">133.0 TB / yr</div>
            <div id="calc-res-storage-5yr" class="text-[10px] text-slate-400">5 Years: 665.0 TB</div>
          </div>

          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <div class="text-slate-500 text-[10px]">CACHE RAM REQUIRED (20% RULE)</div>
            <div id="calc-res-cache-ram" class="text-base font-bold text-emerald-400">72.9 GB RAM</div>
            <div id="calc-res-redis-nodes" class="text-[10px] text-slate-400">2x r6g.xlarge nodes</div>
          </div>
        </div>

        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800/80 font-mono text-[11px] space-y-1 text-slate-300">
          <div class="text-cyan-400 font-bold">NETWORK INGRESS &amp; EGRESS BANDWIDTH:</div>
          <div id="calc-res-network" class="text-slate-300">Ingress: 33.7 MB/s (0.27 Gbps) &bull; Egress: 337.3 MB/s (2.70 Gbps)</div>
          <div class="text-[10px] text-slate-500 pt-1">Rule of Thumb: At > 10 Gbps egress, terminate TLS at Anycast CDN edges to protect origin cloud egress bills.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SUB-VIEW 3: INTERVIEWER GRILLING & CURVEBALL SIMULATOR -->
  <div id="subview-studio-curveballs" class="hidden space-y-6">
    <div class="p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div>
          <h4 class="text-base font-bold text-white font-mono flex items-center gap-2">
            <i data-lucide="zap" class="w-4 h-4 text-rose-400"></i> STAFF/PRINCIPAL INTERVIEWER GRILLING CHALLENGES
          </h4>
          <p class="text-xs text-slate-400 mt-0.5">Simulates high-pressure edge cases, split-brain scenarios, and concurrency traps thrown by FAANG bar-raisers.</p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="drawRandomCurveball()" class="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-rose-500 hover:bg-rose-400 text-white transition-all flex items-center gap-1.5 shadow-lg shadow-rose-500/20">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Draw Random Curveball
          </button>
        </div>
      </div>

      <!-- Curveball Display Card -->
      <div id="curveball-card-container" class="space-y-4">
        <!-- Dynamically injected by renderCurveball() -->
      </div>
    </div>
  </div>

  <!-- SUB-VIEW 4: FAANG L6/L7 RUBRIC & LEVEL PREDICTOR -->
  <div id="subview-studio-rubric" class="hidden space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- 4 Pillars Evaluation Form (Col 8) -->
      <div class="lg:col-span-8 p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2 text-xs font-mono font-bold text-white">
          <span class="flex items-center gap-1.5"><i data-lucide="check-square" class="w-3.5 h-3.5 text-cyan-400"></i> OFFICIAL FAANG SYSTEM DESIGN 4-PILLAR RUBRIC</span>
          <span class="text-[10px] text-slate-500">Score each pillar from 1 to 4</span>
        </div>

        <!-- Pillar 1 -->
        <div class="space-y-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold">1. Problem Navigation &amp; Scope Scaffolding</span>
            <span id="rubric-lbl-1" class="text-cyan-400 font-bold">Score: 3 / 4 (Solid Senior)</span>
          </div>
          <input type="range" id="rubric-in-1" min="1" max="4" step="1" value="3" oninput="updateRubricLevel()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
          <p class="text-[11px] text-slate-400">Did you drive the ambiguity? Identify 3 critical use cases, calculate bounds, and declare non-goals cleanly?</p>
        </div>

        <!-- Pillar 2 -->
        <div class="space-y-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold">2. Architecture Completeness &amp; Data Model</span>
            <span id="rubric-lbl-2" class="text-emerald-400 font-bold">Score: 3 / 4 (Solid Senior)</span>
          </div>
          <input type="range" id="rubric-in-2" min="1" max="4" step="1" value="3" oninput="updateRubricLevel()" class="w-full accent-emerald-400 bg-slate-800 rounded-lg cursor-pointer">
          <p class="text-[11px] text-slate-400">End-to-end data flow correctness, primary/shard keys, database selection justification (LSM vs B-Tree vs Columnar).</p>
        </div>

        <!-- Pillar 3 -->
        <div class="space-y-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold">3. Resilience, Concurrency &amp; Edge Cases</span>
            <span id="rubric-lbl-3" class="text-amber-400 font-bold">Score: 3 / 4 (Solid Senior)</span>
          </div>
          <input type="range" id="rubric-in-3" min="1" max="4" step="1" value="3" oninput="updateRubricLevel()" class="w-full accent-amber-400 bg-slate-800 rounded-lg cursor-pointer">
          <p class="text-[11px] text-slate-400">Race condition prevention, distributed locking (fencing tokens), idempotent retries, backpressure, and zero single points of failure.</p>
        </div>

        <!-- Pillar 4 -->
        <div class="space-y-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold">4. Staff+ Trade-offs &amp; Principal Judgement</span>
            <span id="rubric-lbl-4" class="text-fuchsia-400 font-bold">Score: 3 / 4 (Solid Senior)</span>
          </div>
          <input type="range" id="rubric-in-4" min="1" max="4" step="1" value="3" oninput="updateRubricLevel()" class="w-full accent-fuchsia-400 bg-slate-800 rounded-lg cursor-pointer">
          <p class="text-[11px] text-slate-400">Explaining CAP/PACELC trade-offs objectively, acknowledging engineering downsides, and designing for operability (SLIs/SLOs).</p>
        </div>
      </div>

      <!-- Level Predictor Outcome Badge (Col 4) -->
      <div class="lg:col-span-4 p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-4">
        <div class="border-b border-slate-800 pb-2 text-xs font-mono font-bold text-white">
          <span>PROJECTED FAANG LEVEL OUTCOME</span>
        </div>

        <div id="rubric-level-card" class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-center space-y-2">
          <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wider">PROJECTED HIRING BAR</div>
          <div id="rubric-level-title" class="text-2xl font-black font-mono text-emerald-400">L6 / STAFF ARCHITECT</div>
          <div id="rubric-level-score" class="text-xs font-mono text-slate-300">Composite Score: 12 / 16 (75%)</div>
        </div>

        <div id="rubric-level-critique" class="text-xs font-mono text-slate-300 leading-relaxed space-y-2">
          <!-- Dynamically populated by updateRubricLevel() -->
        </div>
      </div>
    </div>
  </div>

  <!-- SUB-VIEW 5: CANDIDATE INTERACTIVE SCRATCHPAD -->
  <div id="subview-studio-notes" class="hidden space-y-4">
    <div class="p-5 rounded-2xl bg-slate-950 border border-white/[0.08] space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <i data-lucide="edit-3" class="w-4 h-4 text-cyan-400"></i>
          <span class="text-xs font-mono font-bold text-white">CANDIDATE INTERVIEW SCRATCHPAD &amp; SYSTEM PROPOSAL</span>
        </div>
        <div class="flex items-center gap-2 text-xs font-mono">
          <span id="scratchpad-word-count" class="text-slate-500">0 words</span>
          <button onclick="copyScratchpadToClipboard()" id="btn-copy-scratchpad" class="px-3 py-1 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/20 transition-all">
            Copy Markdown
          </button>
          <button onclick="resetScratchpadTemplate()" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white border border-slate-800 transition-all">
            Reset Template
          </button>
        </div>
      </div>

      <textarea id="interview-scratchpad-input" oninput="saveScratchpadNotes()" rows="18" 
        class="w-full p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400 leading-relaxed custom-scroll"
        placeholder="Draft your solution here..."></textarea>
      
      <div class="text-[10px] font-mono text-slate-500 flex justify-between">
        <span>Auto-saved to local browser storage</span>
        <span>Standard Markdown formatting supported</span>
      </div>
    </div>
  </div>
</div>
"""

TOOLS_JS = """
// ========================================================
// INTERACTIVE LAB CONTROLLERS (100% NULL-SAFE)
// ========================================================


// ========================================================
// 1. GOD-LEVEL DISTRIBUTED ARCHITECTURE PACKET TRACER
// ========================================================

const nodeTelemetry = {
  client: {
    title: "User Client (Mobile & Web)",
    badge: "Layer 7 Endpoint",
    layer: "Layer 7 Application",
    color: "#38bdf8",
    desc: "End-user client communicating over HTTP/3 (QUIC / UDP 443) with 0-RTT TLS 1.3 session resumption and client-side optimistic caching.",
    latency: "< 5 ms local",
    failure: "Exponential Backoff with Full Jitter",
    tip: "Always enforce client-side idempotency keys (UUIDv4) in request headers to guarantee safe automated retries during network flapping."
  },
  cdn: {
    title: "Cloudflare Anycast CDN",
    badge: "Edge Network PoP",
    layer: "Layer 3 / 7 Edge",
    color: "#06b6d4",
    desc: "300+ global datacenters advertising identical BGP Anycast IP. Terminates client TLS within 15ms and caches static assets and API GET payloads in RAM.",
    latency: "< 8 ms edge",
    failure: "BGP Route Withdraw (< 2s)",
    tip: "Use Cache-Control: s-maxage=3600, stale-while-revalidate=60 to decouple edge response latency from origin DB load."
  },
  l4: {
    title: "L4 Maglev / IPVS Load Balancer",
    badge: "Transport Layer Routing",
    layer: "Layer 4 Transport",
    color: "#6366f1",
    desc: "Kernel-bypass packet scheduler (DPDK) operating via Direct Server Return (DSR). Performs consistent 5-tuple hashing to distribute millions of packets/sec.",
    latency: "< 10 microseconds",
    failure: "ECMP Equal-Cost Multi-Path Failover",
    tip: "Direct Server Return allows backend application servers to reply directly to clients, bypassing L4 egress bandwidth bottlenecks."
  },
  l7: {
    title: "Envoy Proxy API Gateway",
    badge: "Application Ingress",
    layer: "Layer 7 Ingress",
    color: "#a855f7",
    desc: "Terminates mTLS, validates JWT signatures against JWKS, enforces distributed Token Bucket rate limits, and manages circuit breaker trip thresholds.",
    latency: "< 1.5 ms gateway",
    failure: "Outlier Detection & Degraded Fallback",
    tip: "Configure local token buckets on Envoy edge sidecars to shed abusive crawlers before their requests ever touch backend CPU threads."
  },
  app: {
    title: "App Microservices Pods",
    badge: "Service Layer (K8s)",
    layer: "Layer 7 Microservice",
    color: "#3b82f6",
    desc: "Stateless application containers (Go / Rust) executing business logic, distributed locks, and SingleFlight mutex barriers to defeat cache stampedes.",
    latency: "< 3.0 ms compute",
    failure: "Horizontal Pod Autoscaler (HPA)",
    tip: "Wrap database queries in singleflight.Group to ensure that 1,000 concurrent requests for an expired key trigger exactly ONE database query."
  },
  cache: {
    title: "Redis Cluster (In-Memory)",
    badge: "L2 Caching Tier",
    layer: "In-Memory Store",
    color: "#10b981",
    desc: "Distributed in-memory key-value store partitioned across 16,384 hash slots. Stores the top 20% hot working set with sub-millisecond read latency.",
    latency: "< 0.8 ms RAM",
    failure: "Sentinel Automatic Master Failover",
    tip: "Implement XFetch probabilistic early expiration (gap = -beta * delta * ln(rand())) to eliminate stampedes on celebrity cache items."
  },
  db: {
    title: "Google Spanner / Multi-AZ SQL",
    badge: "Durable System of Record",
    layer: "Multi-AZ Consensus",
    color: "#ec4899",
    desc: "Globally distributed ACID database leveraging Paxos consensus and TrueTime atomic GPS/rubidium clocks for strict serializability across multiple AZs.",
    latency: "< 12 ms Paxos quorum",
    failure: "Automatic Raft / Paxos Leader Re-election",
    tip: "Never use monotonically increasing primary keys (auto-increment integers) to avoid scorching a single physical partition split."
  },
  kafka: {
    title: "Apache Kafka KRaft & ClickHouse",
    badge: "Distributed Commit Log",
    layer: "Streaming / OLAP",
    color: "#f59e0b",
    desc: "Sequential append-only log with Linux page cache zero-copy reads, serving 1M+ events/sec, feeding ClickHouse for real-time vectorized OLAP analytics.",
    latency: "< 3 ms produce ACK",
    failure: "In-Sync Replica (ISR) Promotion",
    tip: "Partition count dictates maximum consumer concurrency. Pre-scale topic partitions based on peak expected worker count."
  }
};

const tracerScenarios = {
  "scenario-edge-hit": {
    id: "scenario-edge-hit",
    title: "1. Edge CDN Cache Hit (8ms)",
    steps: [
      {
        node: "client",
        x: 82, y: 76,
        desc: "Client issues GET /api/v1/products/4921 over HTTP/3 (QUIC) with 0-RTT TLS session resumption.",
        protocol: "HTTP/3 QUIC (UDP 443)",
        latencyHop: "0.0 ms",
        headers: `GET /api/v1/products/4921 HTTP/3\nHost: api.nexus.io\nUser-Agent: NexusClient/2.4 (iOS 18.1)\nAccept: application/json\n0-RTT: 1`
      },
      {
        node: "cdn",
        x: 252, y: 76,
        desc: "Cloudflare Edge PoP receives request, checks WAF, finds hot key in RAM -> CACHE HIT (Age: 42s)!",
        protocol: "TLS 1.3 / RAM Cache",
        latencyHop: "+7.2 ms",
        headers: `HTTP/3 200 OK\nCF-Cache-Status: HIT\nAge: 42\nContent-Type: application/json\nContent-Encoding: br\nServer: cloudflare`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Edge streams compressed Brotli JSON payload back to client. Origin servers are 100% bypassed!",
        protocol: "HTTP/3 200 OK",
        latencyHop: "+1.0 ms",
        headers: `Response Payload: { "product_id": 4921, "title": "Ultra Cluster X", "price": 499.00 }\nTotal SLA Latency: 8.2 ms`
      }
    ]
  },
  "scenario-write-cdc": {
    id: "scenario-write-cdc",
    title: "2. Dist Write + Paxos 2PC + Kafka CDC (42ms)",
    steps: [
      {
        node: "client",
        x: 82, y: 76,
        desc: "Mobile client submits POST /v1/orders with idempotency key and JWT token.",
        protocol: "HTTP/3 QUIC (POST)",
        latencyHop: "0.0 ms",
        headers: `POST /v1/orders HTTP/3\nHost: api.nexus.io\nAuthorization: Bearer eyJhbGciOi...\nIdempotency-Key: idem_94812a\nContent-Type: application/json`
      },
      {
        node: "cdn",
        x: 252, y: 76,
        desc: "Cloudflare Edge terminates TLS 1.3, verifies WAF DDoS rules, and proxies to origin backbone.",
        protocol: "Edge TLS Termination",
        latencyHop: "+6.8 ms",
        headers: `TCP Connection Re-used (Keep-Alive)\nOrigin Backbone Route: US-East-1\nX-Forwarded-For: 203.0.113.195`
      },
      {
        node: "l4",
        x: 427, y: 76,
        desc: "L4 Maglev LB hashes 5-tuple and forwards raw TCP frame to Envoy Gateway via Direct Server Return.",
        protocol: "IPVS / DSR (Kernel Bypass)",
        latencyHop: "+0.01 ms",
        headers: `Ethernet Frame: DSR Encapsulation\nTarget MAC: Envoy-Node-04\nSource IP Preserved: 203.0.113.195`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy API Gateway validates JWT, checks Token Bucket rate limit (84/100 tokens left), and routes to App pod.",
        protocol: "mTLS 1.3 X.509",
        latencyHop: "+1.2 ms",
        headers: `JWT Claims Verified: user_id=94821\nRateLimit: OK (remaining=84)\nUpstream Cluster: order-service.prod`
      },
      {
        node: "app",
        x: 597, y: 246,
        desc: "Order Service acquires distributed lock in Redis Cluster (Redlock) to ensure exactly-once execution.",
        protocol: "RESP3 Redis Lock",
        latencyHop: "+0.9 ms",
        headers: `SET lock:order:idem_94812a "token_uuid" NX PX 5000\nRedis Status: +OK (Lock Acquired)`
      },
      {
        node: "db",
        x: 252, y: 246,
        desc: "Spanner executes 2PC transaction: Paxos consensus across 3 AZs with TrueTime (eps <= 4ms). Commit persisted!",
        protocol: "Paxos Consensus / 2PC",
        latencyHop: "+28.4 ms",
        headers: `BEGIN TRANSACTION\nINSERT INTO orders (id, user_id, amount) VALUES ('ord_710', 94821, 149.00);\nCOMMIT (TrueTime CommitTimestamp=1774892184912)`
      },
      {
        node: "kafka",
        x: 82, y: 246,
        desc: "Debezium CDC streams order_created event to Kafka KRaft; ClickHouse updates real-time analytics.",
        protocol: "Kafka KRaft / CDC",
        latencyHop: "+3.2 ms",
        headers: `Kafka Produce ACK (topic=order-events, partition=4, offset=891042)\nClickHouse Consumer: Ingested Batch`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Envoy relays HTTP 201 Created back to client with order receipt. Total latency: 42.1 ms.",
        protocol: "HTTP/3 201 Created",
        latencyHop: "+1.6 ms",
        headers: `HTTP/3 201 Created\nContent-Type: application/json\nPayload: { "order_id": "ord_710", "status": "CONFIRMED" }`
      }
    ]
  },
  "scenario-stampede": {
    id: "scenario-stampede",
    title: "3. Stampede SingleFlight (18ms)",
    steps: [
      {
        node: "client",
        x: 82, y: 76,
        desc: "1,000 concurrent clients request expired trending topic (GET /v1/trends/tech).",
        protocol: "HTTP/3 (1,000 Burst)",
        latencyHop: "0.0 ms",
        headers: `GET /v1/trends/tech HTTP/3\nConcurrent Conns: 1,000\nCache TTL on CDN: Expired (0s remaining)`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy routes the 1,000 concurrent requests into the Go Order/Feed service pods.",
        protocol: "Envoy Forwarding",
        latencyHop: "+3.2 ms",
        headers: `Active HTTP/2 Streams: 1,000\nUpstream: feed-service`
      },
      {
        node: "cache",
        x: 427, y: 246,
        desc: "App checks Redis Cluster -> CACHE MISS! 1,000 threads simultaneously need fresh data.",
        protocol: "Redis GET (MISS)",
        latencyHop: "+0.8 ms",
        headers: `GET trend:tech\nRedis Response: (nil) [Key Expired]`
      },
      {
        node: "app",
        x: 597, y: 246,
        desc: "Go singleflight.Group activates! Mutex barrier locks out 999 requests; exactly ONE thread queries the DB.",
        protocol: "Go singleflight.Group",
        latencyHop: "+0.2 ms",
        headers: `group.Do("trend:tech", fetchFn)\nThread 1: Executing fetchFn()\nThreads 2..1000: Suspended on sync.WaitGroup`
      },
      {
        node: "db",
        x: 252, y: 246,
        desc: "Database handles ONE single query instead of melting down under 1,000 concurrent queries!",
        protocol: "Spanner Single Read",
        latencyHop: "+11.8 ms",
        headers: `SELECT * FROM trends WHERE topic = 'tech'\nReturned 1 row in 11.8 ms. Database load: 1 QPS (meltdown prevented!)`
      },
      {
        node: "cache",
        x: 427, y: 246,
        desc: "Single thread repopulates Redis with fresh 5-minute TTL and probabilistic early expiration (XFetch).",
        protocol: "Redis SETEX",
        latencyHop: "+0.9 ms",
        headers: `SETEX trend:tech 300 "{...}"\nStatus: +OK`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "SingleFlight broadcasts result to all 999 waiting callers; all 1,000 clients receive HTTP 200 OK!",
        protocol: "HTTP/3 200 OK",
        latencyHop: "+1.5 ms",
        headers: `HTTP/3 200 OK (Served to 1,000 callers)\nTotal Latency: 18.4 ms (DB Saved!)`
      }
    ]
  },
  "scenario-breaker": {
    id: "scenario-breaker",
    title: "4. Circuit Breaker Trip (1ms)",
    steps: [
      {
        node: "client",
        x: 82, y: 76,
        desc: "Client submits POST /v1/checkout/external-payment.",
        protocol: "HTTP/3 QUIC (POST)",
        latencyHop: "0.0 ms",
        headers: `POST /v1/checkout/external-payment HTTP/3\nHost: api.nexus.io`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy Gateway forwards request to Payment Service.",
        protocol: "Envoy Routing",
        latencyHop: "+1.1 ms",
        headers: `Cluster: payment-partner-service`
      },
      {
        node: "app",
        x: 597, y: 246,
        desc: "Downstream third-party payment partner fails: consecutive 504 Gateway Timeouts & 500 errors surge.",
        protocol: "Downstream Timeout",
        latencyHop: "+5000 ms (Timeout)",
        headers: `HTTP 504 Gateway Timeout\nDownstream Partner Unresponsive`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy Outlier Detection observes >50% failure rate: Circuit Breaker trips from CLOSED -> OPEN!",
        protocol: "Circuit Breaker OPEN",
        latencyHop: "+0.1 ms",
        headers: `Circuit Breaker: STATE_OPEN\nConsecutive 5xx Count: 5 / 5\nAll downstream calls short-circuited!`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Gateway intercepts request instantly, returning degraded async fallback in 1.2ms without consuming worker threads!",
        protocol: "HTTP 200 (Degraded)",
        latencyHop: "+0.1 ms",
        headers: `HTTP/3 200 OK\nPayload: { "status": "QUEUED_ASYNC_RETRY", "fallback": true }\nSLA: 1.2 ms (No origin thread starvation!)`
      }
    ]
  }
};

let currentTracerScenarioKey = "scenario-edge-hit";
let currentTracerStepIdx = 0;
let tracerAutoPlayTimer = null;
let tracerSpeedMultiplier = 1;

function inspectNode(key) {
  const data = nodeTelemetry[key];
  if (!data) return;
  const t = document.getElementById('inspect-title'); if (t) t.innerText = data.title;
  const b = document.getElementById('inspect-badge'); if (b) b.innerText = data.badge;
  const l = document.getElementById('inspect-layer'); if (l) l.innerText = data.layer || "Layer 7";
  const lat = document.getElementById('inspect-latency'); if (lat) lat.innerText = data.latency;
  const f = document.getElementById('inspect-failure'); if (f) f.innerText = data.failure;
  const tp = document.getElementById('inspect-tip'); if (tp) tp.innerText = data.tip;
  const d = document.getElementById('inspect-desc'); if (d) d.innerText = data.desc;
  const dot = document.getElementById('inspect-color-dot'); if (dot) dot.style.backgroundColor = data.color;

  // Highlight active node box in SVG
  document.querySelectorAll('[id^="node-box-"]').forEach(el => {
    const rect = el.querySelector('rect');
    if (rect) {
      rect.setAttribute('stroke-width', '2');
      rect.removeAttribute('filter');
    }
  });
  const activeBox = document.getElementById('node-box-' + key);
  if (activeBox) {
    const rect = activeBox.querySelector('rect');
    if (rect) {
      rect.setAttribute('stroke-width', '3');
      rect.setAttribute('filter', 'url(#nodeGlow)');
    }
  }
}

function renderTracerStep() {
  const scen = tracerScenarios[currentTracerScenarioKey];
  if (!scen || !scen.steps) return;
  const step = scen.steps[currentTracerStepIdx];
  if (!step) return;

  // Step Counter & Desc
  const stepBadge = document.getElementById('tracer-step-badge');
  if (stepBadge) stepBadge.innerText = `Step ${currentTracerStepIdx + 1} of ${scen.steps.length}`;

  const stepDesc = document.getElementById('tracer-step-desc');
  if (stepDesc) stepDesc.innerText = step.desc;

  const stepLat = document.getElementById('tracer-step-latency');
  if (stepLat) stepLat.innerText = step.latencyHop;

  const pBar = document.getElementById('tracer-progress-bar');
  if (pBar) {
    const pct = Math.round(((currentTracerStepIdx + 1) / scen.steps.length) * 100);
    pBar.style.width = pct + '%';
  }

  // Animate dot to coordinates
  const dot = document.getElementById('trace-packet-dot');
  if (dot) {
    dot.style.opacity = '1';
    dot.setAttribute('cx', step.x);
    dot.setAttribute('cy', step.y);
  }

  // Update Raw Wire Terminal
  const term = document.getElementById('inspect-packet-terminal');
  if (term) term.innerText = step.headers;

  const proto = document.getElementById('inspect-protocol');
  if (proto) proto.innerText = step.protocol;

  // Inspect the current node
  inspectNode(step.node);
}

function switchTracerScenario(scenKey) {
  if (tracerAutoPlayTimer) {
    clearInterval(tracerAutoPlayTimer);
    tracerAutoPlayTimer = null;
    const playText = document.getElementById('text-tracer-play');
    if (playText) playText.innerText = "Auto Play";
  }

  currentTracerScenarioKey = scenKey;
  currentTracerStepIdx = 0;

  document.querySelectorAll('.tracer-scen-btn').forEach(btn => {
    btn.className = "tracer-scen-btn px-3 py-1.5 rounded-xl bg-slate-900 text-slate-400 hover:text-white font-medium transition-all shrink-0 flex items-center gap-1.5 border border-slate-800 cursor-pointer";
  });
  const target = document.getElementById('btn-scen-' + scenKey);
  if (target) {
    target.className = "tracer-scen-btn px-3 py-1.5 rounded-xl bg-cyan-500 text-slate-950 font-bold transition-all shrink-0 flex items-center gap-1.5 shadow-lg shadow-cyan-500/20 cursor-pointer";
  }

  renderTracerStep();
}

function nextTracerStep() {
  const scen = tracerScenarios[currentTracerScenarioKey];
  if (!scen) return;
  if (currentTracerStepIdx < scen.steps.length - 1) {
    currentTracerStepIdx++;
    renderTracerStep();
  } else {
    currentTracerStepIdx = 0;
    renderTracerStep();
  }
}

function prevTracerStep() {
  if (currentTracerStepIdx > 0) {
    currentTracerStepIdx--;
    renderTracerStep();
  }
}

function resetTracer() {
  if (tracerAutoPlayTimer) {
    clearInterval(tracerAutoPlayTimer);
    tracerAutoPlayTimer = null;
    const playText = document.getElementById('text-tracer-play');
    if (playText) playText.innerText = "Auto Play";
  }
  currentTracerStepIdx = 0;
  renderTracerStep();
}

function toggleTracerAutoPlay() {
  const playText = document.getElementById('text-tracer-play');
  if (tracerAutoPlayTimer) {
    clearInterval(tracerAutoPlayTimer);
    tracerAutoPlayTimer = null;
    if (playText) playText.innerText = "Auto Play";
  } else {
    if (playText) playText.innerText = "Pause";
    const interval = Math.max(400, 1400 / tracerSpeedMultiplier);
    tracerAutoPlayTimer = setInterval(() => {
      const scen = tracerScenarios[currentTracerScenarioKey];
      if (currentTracerStepIdx < scen.steps.length - 1) {
        currentTracerStepIdx++;
        renderTracerStep();
      } else {
        currentTracerStepIdx = 0;
        renderTracerStep();
      }
    }, interval);
  }
}

function toggleTracerSpeed() {
  tracerSpeedMultiplier = (tracerSpeedMultiplier === 1) ? 2 : 1;
  const btn = document.getElementById('btn-tracer-speed');
  if (btn) btn.innerText = tracerSpeedMultiplier + 'x Speed';
  if (tracerAutoPlayTimer) {
    clearInterval(tracerAutoPlayTimer);
    tracerAutoPlayTimer = null;
    toggleTracerAutoPlay();
  }
}


// ========================================================
// 2. GOD-LEVEL AWS FINOPS & CAPACITY SIZING CALCULATOR
// ========================================================

const costPresets = {
  twitter:   { dau: 500000000, reqs: 35, ratio: 20, payload: 2.0, peak: 3.0 },
  whatsapp:  { dau: 2000000000, reqs: 80, ratio: 1,  payload: 0.8, peak: 2.5 },
  fintech:   { dau: 50000000,  reqs: 20, ratio: 4,  payload: 4.0, peak: 4.0 },
  ecommerce: { dau: 100000000, reqs: 50, ratio: 15, payload: 5.0, peak: 3.5 },
  iot:       { dau: 100000000, reqs: 120, ratio: 0.05, payload: 1.2, peak: 3.0 }
};

let finopsConfig = {
  cpu: 'graviton',    // 'graviton' (-20%) vs 'intel'
  db: 'aurora',       // 'aurora' vs 'rds'
  s3: 'intelligent',  // 'intelligent' (-40%) vs 'standard'
  nat: 'endpoint',    // 'endpoint' ($0) vs 'trap' ($0.045/GB)
  plan: '1yr'         // 'ondemand' (0%), '1yr' (38%), '3yr' (54%)
};

function setArchToggle(category, val) {
  finopsConfig[category] = val;

  // Update button active states
  if (category === 'cpu') {
    const bg = document.getElementById('toggle-cpu-graviton');
    const bi = document.getElementById('toggle-cpu-intel');
    if (bg && bi) {
      bg.className = (val === 'graviton')
        ? 'p-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
      bi.className = (val === 'intel')
        ? 'p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
    }
  } else if (category === 'db') {
    const ba = document.getElementById('toggle-db-aurora');
    const br = document.getElementById('toggle-db-rds');
    if (ba && br) {
      ba.className = (val === 'aurora')
        ? 'p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
      br.className = (val === 'rds')
        ? 'p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
    }
  } else if (category === 's3') {
    const bsi = document.getElementById('toggle-s3-intelligent');
    const bss = document.getElementById('toggle-s3-standard');
    if (bsi && bss) {
      bsi.className = (val === 'intelligent')
        ? 'p-2 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
      bss.className = (val === 'standard')
        ? 'p-2 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
    }
  } else if (category === 'nat') {
    const bne = document.getElementById('toggle-nat-endpoint');
    const bnt = document.getElementById('toggle-nat-trap');
    if (bne && bnt) {
      bne.className = (val === 'endpoint')
        ? 'p-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
      bnt.className = (val === 'trap')
        ? 'p-2 rounded-xl bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold text-left transition-all cursor-pointer'
        : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-left transition-all cursor-pointer';
    }
  } else if (category === 'plan') {
    ['ondemand', '1yr', '3yr'].forEach(p => {
      const btn = document.getElementById('toggle-plan-' + p);
      if (btn) {
        btn.className = (val === p)
          ? 'p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold text-center transition-all cursor-pointer'
          : 'p-2 rounded-xl bg-slate-900 text-slate-400 border border-slate-800 text-center transition-all cursor-pointer';
      }
    });
  }

  recomputeCost();
}

function applyStaffOptimizations() {
  finopsConfig.cpu = 'graviton';
  finopsConfig.db = 'aurora';
  finopsConfig.s3 = 'intelligent';
  finopsConfig.nat = 'endpoint';
  finopsConfig.plan = '1yr';

  setArchToggle('cpu', 'graviton');
  setArchToggle('db', 'aurora');
  setArchToggle('s3', 'intelligent');
  setArchToggle('nat', 'endpoint');
  setArchToggle('plan', '1yr');
}

function applyCostPreset(val) {
  if (!costPresets[val]) return;
  const p = costPresets[val];
  const eDau = document.getElementById('cost-dau'); if (eDau) eDau.value = p.dau;
  const eReqs = document.getElementById('cost-reqs'); if (eReqs) eReqs.value = p.reqs;
  const eRatio = document.getElementById('cost-ratio'); if (eRatio) eRatio.value = p.ratio;
  const ePay = document.getElementById('cost-payload'); if (ePay) ePay.value = p.payload;
  const ePeak = document.getElementById('cost-peak'); if (ePeak) ePeak.value = p.peak;
  recomputeCost();
}

function recomputeCost() {
  const eDau = document.getElementById('cost-dau');
  if (!eDau) return;
  const eReqs = document.getElementById('cost-reqs');
  const eRatio = document.getElementById('cost-ratio');
  const ePayload = document.getElementById('cost-payload');
  const ePeak = document.getElementById('cost-peak');

  const dau = parseFloat(eDau.value);
  const reqs = parseFloat(eReqs.value);
  const ratio = parseFloat(eRatio.value);
  const payloadKb = parseFloat(ePayload.value);
  const peak = parseFloat(ePeak.value);

  // Update slider labels
  const lDau = document.getElementById('cost-lbl-dau'); if (lDau) lDau.innerText = dau.toLocaleString();
  const lReqs = document.getElementById('cost-lbl-reqs'); if (lReqs) lReqs.innerText = reqs;
  const readPct = Math.round((ratio / (ratio + 1)) * 100);
  const lRatio = document.getElementById('cost-lbl-ratio'); if (lRatio) lRatio.innerText = `${ratio} : 1 (${readPct}% Reads)`;
  const lPayload = document.getElementById('cost-lbl-payload'); if (lPayload) lPayload.innerText = `${payloadKb.toFixed(1)} KB`;
  const lPeak = document.getElementById('cost-lbl-peak'); if (lPeak) lPeak.innerText = `${peak.toFixed(1)}x (Spike Safety)`;

  // Math sizing
  const totalDailyReqs = dau * reqs;
  const avgQps = totalDailyReqs / 86400;
  const readQps = Math.round(avgQps * (ratio / (ratio + 1)));
  const peakQps = Math.round(avgQps * peak);

  const egressBps = readQps * (payloadKb * 1024) * 8;
  const dailyStorageBytes = totalDailyReqs * (1 / (ratio + 1)) * (payloadKb * 1024);
  const cacheRamBytes = dailyStorageBytes * 0.20;

  // Plan Discount Factor
  let planDiscount = 1.0;
  if (finopsConfig.plan === '1yr') planDiscount = 0.62; // 38% off
  else if (finopsConfig.plan === '3yr') planDiscount = 0.46; // 54% off

  // 1. Compute
  const instanceCapacity = 4000; // QPS per 4xlarge instance
  const instanceCount = Math.max(2, Math.ceil(peakQps / instanceCapacity));
  const hourlyBaseRate = (finopsConfig.cpu === 'graviton') ? 0.544 : 0.680; // Graviton is $0.544/hr vs Intel $0.680/hr
  const computeMonthly = instanceCount * (hourlyBaseRate * 24 * 30.5) * planDiscount;

  // 2. Redis Cluster
  const redisNodeCount = Math.max(3, Math.ceil((cacheRamBytes / 1e9) / 26));
  const redisMonthly = redisNodeCount * (0.336 * 24 * 30.5) * planDiscount;

  // 3. Database
  const annualStorageGb = (dailyStorageBytes * 365) / 1e9;
  let dbMonthly = 0;
  if (finopsConfig.db === 'aurora') {
    const acus = Math.max(4, Math.ceil(peakQps / 5000) * 2);
    dbMonthly = (acus * 0.12 * 24 * 30.5 * 0.70) + (annualStorageGb * 0.10);
  } else {
    dbMonthly = (instanceCount * 0.45 * 24 * 30.5) + (annualStorageGb * 0.115);
  }

  // 4. S3 Storage
  const s3RatePerGb = (finopsConfig.s3 === 'intelligent') ? 0.0125 : 0.023;
  const s3Monthly = annualStorageGb * s3RatePerGb;

  // 5. Internet Egress Bandwidth
  const monthlyEgressGb = ((egressBps / 8) * 86400 * 30.5) / 1e9;
  const egressMonthly = monthlyEgressGb * 0.05;

  // 6. NAT Gateway Egress Trap ($0.045/GB processing)
  let natMonthly = 0;
  if (finopsConfig.nat === 'trap') {
    natMonthly = monthlyEgressGb * 0.045 + (3 * 0.045 * 24 * 30.5); // 3 NAT GWs + data fee
  }

  const totalBill = computeMonthly + redisMonthly + dbMonthly + s3Monthly + egressMonthly + natMonthly;
  const year1Tco = totalBill * 12;

  // Update UI Elements
  const rRead = document.getElementById('cost-res-readqps'); if (rRead) rRead.innerText = readQps.toLocaleString();
  const rPeak = document.getElementById('cost-res-peakqps'); if (rPeak) rPeak.innerText = peakQps.toLocaleString();
  const rEgress = document.getElementById('cost-res-egress'); if (rEgress) rEgress.innerText = `${(egressBps / 1e9).toFixed(2)} Gbps`;
  const rCache = document.getElementById('cost-res-cache-ram'); if (rCache) rCache.innerText = `${(cacheRamBytes / 1e9).toFixed(1)} GB`;

  const rInst = document.getElementById('cost-res-instances'); 
  if (rInst) rInst.innerText = `(${instanceCount}x ${(finopsConfig.cpu === 'graviton') ? 'c7g.4xlarge Graviton3' : 'c6i.4xlarge Intel'})`;
  const rCompB = document.getElementById('cost-res-compute-bill'); if (rCompB) rCompB.innerText = `$${Math.round(computeMonthly).toLocaleString()} / mo`;

  const rRedN = document.getElementById('cost-res-redis-nodes'); if (rRedN) rRedN.innerText = `(${redisNodeCount}x r7g.xlarge nodes, 80/20 RAM)`;
  const rRedB = document.getElementById('cost-res-redis-bill'); if (rRedB) rRedB.innerText = `$${Math.round(redisMonthly).toLocaleString()} / mo`;

  const rDbB = document.getElementById('cost-res-db-bill'); if (rDbB) rDbB.innerText = `$${Math.round(dbMonthly).toLocaleString()} / mo`;

  const rStorTb = document.getElementById('cost-res-storage-tb'); if (rStorTb) rStorTb.innerText = `(${(annualStorageGb / 1000).toFixed(1)} TB / year)`;
  const rStorB = document.getElementById('cost-res-storage-bill'); if (rStorB) rStorB.innerText = `$${Math.round(s3Monthly).toLocaleString()} / mo`;

  const rEgB = document.getElementById('cost-res-egress-bill'); if (rEgB) rEgB.innerText = `$${Math.round(egressMonthly).toLocaleString()} / mo`;

  const rNatB = document.getElementById('cost-res-nat-bill'); 
  const rNatBadge = document.getElementById('cost-res-nat-badge');
  if (rNatB && rNatBadge) {
    if (finopsConfig.nat === 'trap') {
      rNatB.innerText = `$${Math.round(natMonthly).toLocaleString()} / mo`;
      rNatB.className = "text-rose-400 font-bold";
      rNatBadge.className = "text-[9px] px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800";
      rNatBadge.innerText = "NAT Trap Active!";
    } else {
      rNatB.innerText = "$0 / mo";
      rNatB.className = "text-emerald-400 font-bold";
      rNatBadge.className = "text-[9px] px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800";
      rNatBadge.innerText = "Bypassed ($0)";
    }
  }

  const rTotB = document.getElementById('cost-res-total-bill'); if (rTotB) rTotB.innerText = `$${Math.round(totalBill).toLocaleString()} / mo`;
  const rTco = document.getElementById('cost-res-tco'); if (rTco) rTco.innerText = `Year 1 TCO: $${Math.round(year1Tco).toLocaleString()}`;

  // Update Savings Levers
  const savGraviton = computeMonthly * 0.20;
  const savNat = (monthlyEgressGb * 0.045);
  const savS3 = (annualStorageGb * 0.0105);
  const savEdge = egressMonthly * 0.65;

  const elG = document.getElementById('finops-sav-graviton'); if (elG) elG.innerText = `Saves ~$${Math.round(savGraviton).toLocaleString()} / mo (-20%)`;
  const elN = document.getElementById('finops-sav-nat'); if (elN) elN.innerText = `Saves ~$${Math.round(savNat).toLocaleString()} / mo ($0.045/GB)`;
  const elS = document.getElementById('finops-sav-s3'); if (elS) elS.innerText = `Saves ~$${Math.round(savS3).toLocaleString()} / mo (Auto Archive)`;
  const elE = document.getElementById('finops-sav-edge'); if (elE) elE.innerText = `Saves ~$${Math.round(savEdge).toLocaleString()} / mo (-65% Egress)`;
}


/* =========================================================================
   GOD-LEVEL DISTRIBUTED SERVER DISTRIBUTION & LOAD BALANCING ENGINE
   ========================================================================= */

// 1. DETERMINISTIC CRYPTOGRAPHIC HASH (FNV-1a 32-bit)
function fnv1aHash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0); // 32-bit unsigned integer
}

function hashToAngle(str) {
  return (fnv1aHash(str) % 36000) / 100.0; // 0.00 to 359.99 degrees
}

// 2. CLUSTER STATE & POOL DEFINITIONS
let liveHashNodes = [
  { id: "Server-Alpha", ip: "10.0.1.10", port: 8081, color: "#06b6d4", active: true },
  { id: "Server-Beta",  ip: "10.0.1.20", port: 8082, color: "#10b981", active: true },
  { id: "Server-Gamma", ip: "10.0.1.30", port: 8083, color: "#f59e0b", active: true },
  { id: "Server-Delta", ip: "10.0.1.40", port: 8084, color: "#ec4899", active: true }
];

const candidateServers = [
  { id: "Server-Epsilon", ip: "10.0.1.50", port: 8085, color: "#8b5cf6" },
  { id: "Server-Zeta",    ip: "10.0.1.60", port: 8086, color: "#3b82f6" },
  { id: "Server-Eta",     ip: "10.0.1.70", port: 8087, color: "#14b8a6" },
  { id: "Server-Theta",   ip: "10.0.1.80", port: 8088, color: "#f97316" }
];

let liveKeys = [];
let liveVnodes = 15;
let activeHighlightNodeId = null;
let lastProbe = null;

// Seed realistic keys on boot
function seedInitialHashKeys(count = 120) {
  const prefixes = ["user_profile", "order_tx", "session_jwt", "cart_item", "payment_vault", "device_telemetry", "chat_msg", "token_refresh"];
  liveKeys = [];
  for (let i = 1; i <= count; i++) {
    const keyName = `${prefixes[i % prefixes.length]}:${(i * 137 + 42) % 9999 + 1000}`;
    const angle = hashToAngle(keyName);
    liveKeys.push({ id: keyName, angle: angle });
  }
}

// 3. LOGGING CLUSTER EVENTS
function logClusterEvent(msg, type = 'info') {
  const logEl = document.getElementById('live-cluster-event-log');
  if (!logEl) return;
  const time = new Date().toISOString().substring(11, 19);
  const color = type === 'alert' ? 'text-rose-400 font-bold' : (type === 'success' ? 'text-emerald-400 font-bold' : 'text-slate-400');
  const row = document.createElement('div');
  row.className = color;
  row.innerHTML = `<span class="text-slate-600">[${time}]</span> ${msg}`;
  logEl.prepend(row);
}

// 4. SUB-TAB SWITCHER (Consistent Hash Ring vs L4/L7 Balancer)
function switchDistSubTab(tab) {
  if (typeof playClickTone === 'function') playClickTone(700, 0.02);
  const vRing = document.getElementById('dist-view-ring');
  const vBal = document.getElementById('dist-view-balancer');
  const bRing = document.getElementById('btn-subtab-ring');
  const bBal = document.getElementById('btn-subtab-balancer');

  if (tab === 'ring') {
    if (vRing) vRing.classList.remove('hidden');
    if (vBal) vBal.classList.add('hidden');
    if (bRing) bRing.className = 'px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-1.5';
    if (bBal) bBal.className = 'px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5';
    renderLiveHashRing();
  } else {
    if (vRing) vRing.classList.add('hidden');
    if (vBal) vBal.classList.remove('hidden');
    if (bBal) bBal.className = 'px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-1.5';
    if (bRing) bRing.className = 'px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5';
    renderLbUI();
  }
  if (typeof safeCreateIcons === 'function') safeCreateIcons();
}

// 5. VIRTUAL NODES FACTOR CHANGE
function changeLiveVNodes(val) {
  liveVnodes = parseInt(val) || 15;
  const l = document.getElementById('live-lbl-vnodes');
  if (l) l.innerText = `${liveVnodes} vnodes (${liveHashNodes.length * liveVnodes} total)`;
  logClusterEvent(`Virtual node factor adjusted to ${liveVnodes} vnodes/server (recalculating ring partitions).`, 'info');
  renderLiveHashRing();
}

// 6. ADD SERVER NODE (+ Scale Out)
function addHashNodeLive() {
  if (liveHashNodes.length >= 8) {
    logClusterEvent('Maximum 8 servers allowed in live interactive lab.', 'alert');
    return;
  }
  const nextNode = candidateServers[liveHashNodes.length - 4];
  if (nextNode) {
    liveHashNodes.push({ ...nextNode, active: true });
    logClusterEvent(`SCALE-OUT: Added ${nextNode.id} (${nextNode.ip}:${nextNode.port}). Minimal K/N keys migrated without cluster invalidation!`, 'success');
  } else {
    const idx = liveHashNodes.length + 1;
    liveHashNodes.push({ id: `Server-${idx}`, ip: `10.0.1.${idx}0`, port: 8080 + idx, color: '#38bdf8', active: true });
    logClusterEvent(`SCALE-OUT: Added Server-${idx}. Minimal K/N keys rebalanced!`, 'success');
  }
  renderLiveHashRing();
}

// 7. SIMULATE RANDOM NODE CRASH
function killRandomNodeLive() {
  const activeNodes = liveHashNodes.filter(n => n.active);
  if (activeNodes.length <= 2) {
    logClusterEvent('Minimum 2 active nodes required to sustain consistent quorum.', 'alert');
    return;
  }
  const victim = activeNodes[activeNodes.length - 1];
  victim.active = false;
  logClusterEvent(`CRASH EVENT: ${victim.id} (${victim.ip}) went offline! Its keys seamlessly remapped clockwise. Zero cache avalanche!`, 'alert');
  renderLiveHashRing();
}

// 8. TOGGLE INDIVIDUAL NODE HEALTH
function toggleSpecificNodeHealth(nodeId) {
  const node = liveHashNodes.find(n => n.id === nodeId);
  if (!node) return;
  const activeCount = liveHashNodes.filter(n => n.active).length;
  if (node.active && activeCount <= 2) {
    logClusterEvent('Cannot disable: minimum 2 active nodes required for ring replication.', 'alert');
    return;
  }
  node.active = !node.active;
  if (node.active) {
    logClusterEvent(`RECOVERY: ${node.id} is back online! Clockwise partitions reclaimed.`, 'success');
  } else {
    logClusterEvent(`FAILURE: ${node.id} marked OFFLINE! Partitions forwarded to next clockwise neighbor.`, 'alert');
  }
  renderLiveHashRing();
}

// 9. SCATTER KEYS
function scatterKeysLive(count) {
  seedInitialHashKeys(count);
  logClusterEvent(`Scattered ${count} deterministic keys across hash ring.`, 'info');
  renderLiveHashRing();
}

function resetHashCluster() {
  liveHashNodes = [
    { id: "Server-Alpha", ip: "10.0.1.10", port: 8081, color: "#06b6d4", active: true },
    { id: "Server-Beta",  ip: "10.0.1.20", port: 8082, color: "#10b981", active: true },
    { id: "Server-Gamma", ip: "10.0.1.30", port: 8083, color: "#f59e0b", active: true },
    { id: "Server-Delta", ip: "10.0.1.40", port: 8084, color: "#ec4899", active: true }
  ];
  liveVnodes = 15;
  const slider = document.getElementById('live-input-vnodes'); if (slider) slider.value = 15;
  const l = document.getElementById('live-lbl-vnodes'); if (l) l.innerText = '15 vnodes';
  activeHighlightNodeId = null;
  lastProbe = null;
  seedInitialHashKeys(120);
  logClusterEvent('Cluster reset to default 4-node production baseline.', 'info');
  renderLiveHashRing();
}

// 10. HIGHLIGHT NODE SELECTION
function setHighlightNode(nodeId) {
  if (activeHighlightNodeId === nodeId) {
    activeHighlightNodeId = null;
  } else {
    activeHighlightNodeId = nodeId;
  }
  renderLiveHashRing();
}

// 11. KEY PROBE LOOKUP
function probeSpecificKey() {
  const inp = document.getElementById('probe-key-input');
  if (!inp) return;
  const key = inp.value.trim() || 'user_profile:94821';
  executeKeyProbe(key);
}

function probeRandomKey() {
  const randNum = Math.floor(Math.random() * 90000 + 10000);
  const key = `user_session:${randNum}`;
  const inp = document.getElementById('probe-key-input');
  if (inp) inp.value = key;
  executeKeyProbe(key);
}

function executeKeyProbe(key) {
  const hash = fnv1aHash(key);
  const angle = (hash % 36000) / 100.0;

  const activeNodes = liveHashNodes.filter(n => n.active);
  if (activeNodes.length === 0) return;

  let allVPoints = [];
  activeNodes.forEach(node => {
    for (let v = 0; v < liveVnodes; v++) {
      const vAngle = (fnv1aHash(node.id + ":vnode:" + v) % 36000) / 100.0;
      allVPoints.push({ nodeId: node.id, color: node.color, angle: vAngle, vIndex: v, nodeObj: node });
    }
  });
  allVPoints.sort((a, b) => a.angle - b.angle);

  let target = allVPoints.find(p => p.angle >= angle);
  if (!target) target = allVPoints[0];

  lastProbe = {
    key: key,
    hash: hash,
    hexHash: '0x' + hash.toString(16).toUpperCase(),
    angle: angle,
    target: target
  };

  const statusEl = document.getElementById('probe-res-status');
  if (statusEl) {
    statusEl.innerHTML = `Key <strong>"${key}"</strong> mapped to <strong style="color: ${target.color};">${target.nodeId}</strong>`;
  }
  const detailsEl = document.getElementById('probe-res-details');
  if (detailsEl) {
    detailsEl.innerHTML = `
      <span>Hash: <strong class="text-white">${lastProbe.hexHash}</strong></span>
      <span>Coordinate: <strong class="text-cyan-400">${angle.toFixed(1)}&deg;</strong></span>
      <span>Clockwise Successor: <strong style="color: ${target.color};">${target.nodeObj.ip}:${target.nodeObj.port}</strong> (vnode #${target.vIndex} at ${target.angle.toFixed(1)}&deg;)</span>
    `;
  }

  logClusterEvent(`PROBE: "${key}" (Hash ${lastProbe.hexHash} &bull; ${angle.toFixed(1)}&deg;) &rarr; ${target.nodeId} (${target.nodeObj.ip})`, 'info');
  renderLiveHashRing();
}

// 12. RENDER CONSISTENT HASH RING & SERVER DISTRIBUTION
function renderLiveHashRing() {
  const svg = document.getElementById('live-hash-ring-svg');
  if (!svg) return;

  if (liveKeys.length === 0) {
    seedInitialHashKeys(120);
  }

  const cx = 230, cy = 230, r = 160;
  const activeNodes = liveHashNodes.filter(n => n.active);

  // Collect all virtual node coordinates
  let allVPoints = [];
  activeNodes.forEach((node, nIdx) => {
    // Primary anchor position
    const primaryAngle = (nIdx * (360 / activeNodes.length)) % 360;
    allVPoints.push({ nodeId: node.id, color: node.color, angle: primaryAngle, isPrimary: true, vIndex: 0, nodeObj: node });

    // Interleaved virtual nodes
    for (let v = 1; v < liveVnodes; v++) {
      const vAngle = (fnv1aHash(node.id + ":vnode:" + v) % 36000) / 100.0;
      allVPoints.push({ nodeId: node.id, color: node.color, angle: vAngle, isPrimary: false, vIndex: v, nodeObj: node });
    }
  });
  allVPoints.sort((a, b) => a.angle - b.angle);

  // Distribute keys to clockwise successor
  let distribution = {};
  liveHashNodes.forEach(n => distribution[n.id] = 0);

  let keyColorMap = [];
  liveKeys.forEach(k => {
    let target = allVPoints.find(p => p.angle >= k.angle);
    if (!target) target = allVPoints[0];
    if (target) {
      distribution[target.nodeId]++;
      keyColorMap.push({ ...k, targetNodeId: target.nodeId, color: target.color });
    }
  });

  // Calculate Mathematical Uniformity (Standard Deviation & CV)
  const N = activeNodes.length || 1;
  const K = liveKeys.length || 1;
  const mean = K / N;
  let varianceSum = 0;
  activeNodes.forEach(n => {
    const count = distribution[n.id] || 0;
    varianceSum += Math.pow(count - mean, 2);
  });
  const stdDev = Math.sqrt(varianceSum / N);
  const cvPct = Math.round((stdDev / mean) * 100);

  // Update Quality Badge
  const qBadge = document.getElementById('live-quality-badge');
  const qText = document.getElementById('live-quality-text');
  if (qBadge && qText) {
    if (cvPct > 25) {
      qBadge.className = 'flex items-center gap-2 px-3 py-1 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs font-mono';
      qText.innerHTML = `Severe Hotspot Skew (&sigma; = ${stdDev.toFixed(1)} &bull; ${cvPct}% CV)`;
    } else if (cvPct > 10) {
      qBadge.className = 'flex items-center gap-2 px-3 py-1 rounded-xl bg-amber-950/40 border border-amber-500/40 text-amber-300 text-xs font-mono';
      qText.innerHTML = `Moderate Balance (&sigma; = ${stdDev.toFixed(1)} &bull; ${cvPct}% CV)`;
    } else {
      qBadge.className = 'flex items-center gap-2 px-3 py-1 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs font-mono';
      qText.innerHTML = `Near-Perfect Uniformity (&sigma; = ${stdDev.toFixed(1)} &bull; ${cvPct}% CV)`;
    }
  }

  // Build SVG Content
  let svgHtml = `
    <!-- Definitions -->
    <defs>
      <filter id="glow-ring" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="4" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    </defs>

    <!-- Outer Hash Space Orbit (0 to 2^32 - 1) -->
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#1e293b" stroke-width="4" stroke-dasharray="6 4"/>
    <circle cx="${cx}" cy="${cy}" r="${r + 28}" fill="none" stroke="#0f172a" stroke-width="1"/>

    <!-- Coordinate Cardinal Markers -->
    <text x="${cx}" y="${cy - r - 12}" fill="#64748b" font-size="8" font-family="monospace" text-anchor="middle">0&deg; / 2^32</text>
    <text x="${cx + r + 18}" y="${cy + 3}" fill="#64748b" font-size="8" font-family="monospace" text-anchor="start">90&deg;</text>
    <text x="${cx}" y="${cy + r + 20}" fill="#64748b" font-size="8" font-family="monospace" text-anchor="middle">180&deg;</text>
    <text x="${cx - r - 18}" y="${cy + 3}" fill="#64748b" font-size="8" font-family="monospace" text-anchor="end">270&deg;</text>

    <!-- Center Hub Info -->
    <circle cx="${cx}" cy="${cy}" r="45" fill="#090d16" stroke="#1e293b" stroke-width="2"/>
    <text x="${cx}" y="${cy - 8}" fill="#f8fafc" font-size="12" font-weight="bold" font-family="monospace" text-anchor="middle">HASH RING</text>
    <text x="${cx}" y="${cy + 8}" fill="#06b6d4" font-size="10" font-weight="bold" font-family="monospace" text-anchor="middle">${allVPoints.length} VNODES</text>
    <text x="${cx}" y="${cy + 22}" fill="#64748b" font-size="8" font-family="monospace" text-anchor="middle">&sigma; &plusmn;${stdDev.toFixed(1)} keys</text>
  `;

  // Draw Key Particles on Ring Perimeter (Color-coded to owner!)
  keyColorMap.forEach(k => {
    const isHighlighted = !activeHighlightNodeId || activeHighlightNodeId === k.targetNodeId;
    const rad = (k.angle * Math.PI) / 180;
    const kx = cx + (r - 18) * Math.cos(rad);
    const ky = cy + (r - 18) * Math.sin(rad);
    const opacity = isHighlighted ? 0.85 : 0.15;
    svgHtml += `<circle cx="${kx}" cy="${ky}" r="3" fill="${k.color}" opacity="${opacity}">
      <title>${k.id} &bull; ${k.angle.toFixed(1)}&deg; &rarr; ${k.targetNodeId}</title>
    </circle>`;
  });

  // Draw Virtual Nodes
  allVPoints.forEach(p => {
    const isHighlighted = !activeHighlightNodeId || activeHighlightNodeId === p.nodeId;
    const rad = (p.angle * Math.PI) / 180;
    const nx = cx + r * Math.cos(rad);
    const ny = cy + r * Math.sin(rad);
    const radius = p.isPrimary ? 8 : 4;
    const stroke = p.isPrimary ? '#ffffff' : '#0f172a';
    const opacity = isHighlighted ? 1.0 : 0.25;

    svgHtml += `<circle cx="${nx}" cy="${ny}" r="${radius}" fill="${p.color}" stroke="${stroke}" stroke-width="${p.isPrimary ? 2 : 1}" opacity="${opacity}">
      <title>${p.nodeId} (vnode #${p.vIndex}) at ${p.angle.toFixed(1)}&deg;</title>
    </circle>`;

    if (p.isPrimary && isHighlighted) {
      const tx = cx + (r + 18) * Math.cos(rad);
      const ty = cy + (r + 18) * Math.sin(rad) + 4;
      const label = p.nodeId.replace('Server-', 'S-');
      svgHtml += `<text x="${tx}" y="${ty}" fill="${p.color}" font-size="9" font-weight="bold" font-family="monospace" text-anchor="middle">${label}</text>`;
    }
  });

  // Draw Active Key Probe Laser & Arc if probe exists
  if (lastProbe) {
    const pRad = (lastProbe.angle * Math.PI) / 180;
    const px = cx + (r - 18) * Math.cos(pRad);
    const py = cy + (r - 18) * Math.sin(pRad);

    // Laser beam from center hub to key coordinate
    svgHtml += `
      <line x1="${cx}" y1="${cy}" x2="${px}" y2="${py}" stroke="#00f0ff" stroke-width="2" stroke-dasharray="4 2" opacity="0.9"/>
      <circle cx="${px}" cy="${py}" r="6" fill="#00f0ff" filter="url(#glow-ring)"/>
      <circle cx="${px}" cy="${py}" r="3" fill="#ffffff"/>
    `;
  }

  svg.innerHTML = svgHtml;

  // Render SERVER DISTRIBUTION Table
  const listEl = document.getElementById('live-hash-nodes-list');
  if (listEl) {
    listEl.innerHTML = liveHashNodes.map(n => {
      const count = distribution[n.id] || 0;
      const pct = liveKeys.length > 0 ? ((count / liveKeys.length) * 100).toFixed(1) : '0.0';
      const isSelected = activeHighlightNodeId === n.id;
      const bgClass = isSelected ? 'bg-slate-900 border-cyan-500/50 shadow-lg' : 'bg-slate-900/60 border-slate-800';
      const opacityClass = n.active ? '' : 'opacity-40 grayscale';

      return `
        <div onclick="setHighlightNode('${n.id}')" class="p-3 rounded-xl border ${bgClass} ${opacityClass} cursor-pointer transition-all space-y-2 hover:border-slate-700">
          <div class="flex items-center justify-between text-xs font-mono">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full shrink-0" style="background-color: ${n.color};"></span>
              <span class="text-white font-bold">${n.id}</span>
              <span class="text-[10px] text-slate-500">${n.ip}:${n.port}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold font-mono text-white">${count} keys</span>
              <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-cyan-400 font-bold">${pct}%</span>
              <button onclick="event.stopPropagation(); toggleSpecificNodeHealth('${n.id}')" title="${n.active ? 'Simulate Crash' : 'Recover Node'}" 
                class="px-2 py-0.5 text-[9px] rounded font-bold font-mono ${n.active ? 'bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 border border-rose-500/30' : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30'}">
                ${n.active ? 'CRASH' : 'REVIVE'}
              </button>
            </div>
          </div>

          <!-- Capacity Bar -->
          <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all duration-300" style="width: ${pct}%; background-color: ${n.color};"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  const countEl = document.getElementById('live-lbl-keycount');
  if (countEl) countEl.innerText = `${liveKeys.length} Keys Distributed`;
}

// 13. L4/L7 TRAFFIC LOAD BALANCER ENGINE
let lbServers = [
  { id: 'app-pod-01', weight: 4, activeConns: 0, totalServed: 0, maxConns: 50 },
  { id: 'app-pod-02', weight: 2, activeConns: 0, totalServed: 0, maxConns: 50 },
  { id: 'app-pod-03', weight: 1, activeConns: 0, totalServed: 0, maxConns: 50, hasLag: false },
  { id: 'app-pod-04', weight: 1, activeConns: 0, totalServed: 0, maxConns: 50 }
];

let lbAlgo = 'round-robin';
let lbRoundRobinIdx = 0;
let lbWeightedSequence = [0, 0, 0, 0, 1, 1, 2, 3];
let lbWeightedIdx = 0;

function changeLbAlgo(algo) {
  lbAlgo = algo;
  logLbTerminal(`Load balancing algorithm set to: ${algo.toUpperCase()}`, 'info');
}

function toggleLbLag() {
  lbServers[2].hasLag = !lbServers[2].hasLag;
  const btn = document.getElementById('btn-toggle-lag');
  const dot = document.getElementById('lb-dot-2');
  const badge = document.getElementById('lb-badge-2');
  if (lbServers[2].hasLag) {
    if (btn) btn.innerText = 'Clear Lag from Node 3';
    if (dot) dot.className = 'w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping';
    if (badge) badge.innerText = '300ms Lag Spike!';
    logLbTerminal('[CHAOS INJECT] Injected 300ms thread stall into app-pod-03 (Observing Least-Conn / P2C avoidance)...', 'alert');
  } else {
    if (btn) btn.innerText = 'Inject Slowdown on Node 3';
    if (dot) dot.className = 'w-2.5 h-2.5 rounded-full bg-amber-400';
    if (badge) badge.innerText = 'Weight 1x';
    logLbTerminal('[RECOVER] Cleared thread stall on app-pod-03.', 'info');
  }
}

function logLbTerminal(msg, type = 'info') {
  const term = document.getElementById('lb-terminal-log');
  if (!term) return;
  const time = new Date().toISOString().substring(11, 19);
  const color = type === 'alert' ? 'text-rose-400 font-bold' : (type === 'hit' ? 'text-emerald-400 font-mono' : 'text-slate-400');
  const row = document.createElement('div');
  row.className = color;
  row.innerHTML = `<span class="text-slate-600">[${time}]</span> ${msg}`;
  term.prepend(row);
}

function clearLbLogs() {
  const term = document.getElementById('lb-terminal-log');
  if (term) term.innerHTML = '<div class="text-slate-600">[READY] Access logs cleared.</div>';
}

function sendLbRequest(count = 1) {
  for (let i = 0; i < count; i++) {
    let chosenIdx = 0;

    if (lbAlgo === 'round-robin') {
      chosenIdx = lbRoundRobinIdx % lbServers.length;
      lbRoundRobinIdx++;
    } else if (lbAlgo === 'weighted') {
      chosenIdx = lbWeightedSequence[lbWeightedIdx % lbWeightedSequence.length];
      lbWeightedIdx++;
    } else if (lbAlgo === 'least-conn') {
      let minConns = Infinity;
      lbServers.forEach((srv, idx) => {
        if (srv.activeConns < minConns) {
          minConns = srv.activeConns;
          chosenIdx = idx;
        }
      });
    } else if (lbAlgo === 'power-of-two') {
      // Pick 2 random servers, route to lowest active conns
      const idxA = Math.floor(Math.random() * lbServers.length);
      let idxB = Math.floor(Math.random() * lbServers.length);
      while (idxB === idxA) idxB = Math.floor(Math.random() * lbServers.length);
      chosenIdx = lbServers[idxA].activeConns <= lbServers[idxB].activeConns ? idxA : idxB;
    } else if (lbAlgo === 'ip-hash') {
      const mockIp = `192.168.${Math.floor(Math.random() * 5 + 1)}.${Math.floor(Math.random() * 250 + 1)}`;
      chosenIdx = fnv1aHash(mockIp) % lbServers.length;
    }

    const srv = lbServers[chosenIdx];
    srv.activeConns++;
    srv.totalServed++;

    const latency = srv.hasLag ? Math.floor(Math.random() * 150 + 250) : Math.floor(Math.random() * 15 + 5);
    setTimeout(() => {
      if (srv.activeConns > 0) srv.activeConns--;
      renderLbUI();
    }, latency * 12);
  }

  logLbTerminal(`Dispatched ${count} request(s) via [${lbAlgo.toUpperCase()}] algorithm.`, 'hit');
  renderLbUI();
}

function renderLbUI() {
  lbServers.forEach((srv, idx) => {
    const connEl = document.getElementById(`lb-conn-${idx}`);
    const barEl = document.getElementById(`lb-bar-${idx}`);
    const totEl = document.getElementById(`lb-total-${idx}`);
    const pct = Math.min(100, Math.round((srv.activeConns / srv.maxConns) * 100));

    if (connEl) connEl.innerText = `${srv.activeConns} active`;
    if (barEl) barEl.style.width = `${pct}%`;
    if (totEl) totEl.innerText = `${srv.totalServed.toLocaleString()} reqs`;
  });
}

// 14. INITIALIZE SERVER DISTRIBUTION ENGINE
function initServerDistribution() {
  seedInitialHashKeys(120);
  renderLiveHashRing();
  renderLbUI();
}

// Run immediately on script load
try {
  initServerDistribution();
} catch(e) {}



/* =========================================================================
   GOD-LEVEL DISTRIBUTED RATE LIMITER & QUOTA MANAGEMENT ENGINE (RateLimit OS 3.0)
   ========================================================================= */

// Multi-Tenant Configurations
const RL_TENANTS = {
  free: { name: "Free Tier", key: "tenant:free_491", capacity: 15, refillRate: 2.0, burst: 15, color: "#06b6d4" },
  pro: { name: "Pro Tier", key: "tenant:pro_team9", capacity: 60, refillRate: 10.0, burst: 60, color: "#10b981" },
  enterprise: { name: "Enterprise Tier", key: "tenant:ent_stripe", capacity: 200, refillRate: 40.0, burst: 200, color: "#a855f7" },
  ddos: { name: "Malicious Botnet", key: "tenant:bot_ddos", capacity: 0, refillRate: 0.0, burst: 0, color: "#f43f5e" }
};

let currentTenant = 'pro';
let currentAlgo = 'token-bucket';

// Rate Limiter Engine Internal State
let rlState = {
  // Token Bucket State
  tokens: 60,
  capacity: 60,
  refillRate: 10.0, // tokens per second
  lastRefillTime: performance.now(),

  // Leaky Bucket State
  queue: 0,
  queueCapacity: 30,
  leakRate: 8.0, // reqs leaked per second
  lastLeakTime: performance.now(),

  // Sliding Window Counter State (60-second window, 6 sub-buckets)
  windowDuration: 60, // seconds
  prevWindowCount: 42,
  currWindowCount: 18,
  currWindowStart: Date.now(),
  windowLimit: 60,

  // Fixed Window State
  fixedWindowCount: 15,
  fixedWindowStart: Math.floor(Date.now() / 60000),
  fixedLimit: 60,

  // Global Telemetry Counters
  totalOk: 0,
  totalThrottled: 0,
  rollingHistory: Array(20).fill({ ok: 0, throttled: 0 })
};

let rlEngineInterval = null;
let continuousTrafficInterval = null;
let isContinuousRunning = false;

// Initialize Engine Lifecycle
function startLiveRlEngine() {
  if (rlEngineInterval) clearInterval(rlEngineInterval);
  syncTenantParams();
  
  rlEngineInterval = setInterval(() => {
    stepRateLimiterPhysics();
    updateLiveRlUI();
    renderRlPhysicsSVG();
  }, 100);

  // Every second: advance the rolling throughput chart
  setInterval(() => {
    shiftRollingChart();
  }, 1000);
}

// Synchronize Tenant Parameters
function syncTenantParams() {
  const t = RL_TENANTS[currentTenant] || RL_TENANTS.pro;
  rlState.capacity = t.capacity;
  rlState.refillRate = t.refillRate;
  rlState.tokens = Math.min(rlState.capacity, rlState.tokens || t.capacity);
  rlState.queueCapacity = Math.max(10, Math.round(t.capacity / 2));
  rlState.leakRate = Math.max(2, Math.round(t.refillRate * 0.8));
  rlState.windowLimit = t.capacity;
  rlState.fixedLimit = t.capacity;
}

// Switch Tenant Tier
function switchRlTenant(tenant) {
  currentTenant = tenant;
  syncTenantParams();
  const t = RL_TENANTS[tenant];
  logLiveRl(`[TENANT SWITCH] Active client identity: ${t.name} (Key: ${t.key} &bull; Capacity: ${t.capacity} &bull; Rate: ${t.refillRate}/s)`, 'info');
  updateLiveRlUI();
}

// Switch Algorithm
function switchRlAlgo(algo) {
  currentAlgo = algo;
  syncTenantParams();
  const names = {
    'token-bucket': 'Token Bucket (Amazon / Stripe)',
    'leaky-bucket': 'Leaky Bucket (Traffic Shaping / NGINX)',
    'sliding-window': 'Sliding Window Counter (Cloudflare / Twitter)',
    'fixed-window': 'Fixed Window Counter (Memcached INCR)'
  };
  logLiveRl(`[ALGORITHM SWITCH] Active engine set to: ${names[algo]}`, 'info');
  updateAlgoDeepDiveText();
  updateLiveRlUI();
}

// Step Physics Simulator (Continuous Time Math)
function stepRateLimiterPhysics() {
  const now = performance.now();

  // 1. Token Bucket Physics (Continuous Refill)
  const dtTokens = (now - rlState.lastRefillTime) / 1000.0;
  if (dtTokens > 0) {
    if (rlState.tokens < rlState.capacity) {
      rlState.tokens = Math.min(rlState.capacity, rlState.tokens + (dtTokens * rlState.refillRate));
    }
    rlState.lastRefillTime = now;
  }

  // 2. Leaky Bucket Physics (Constant Drain)
  const dtQueue = (now - rlState.lastLeakTime) / 1000.0;
  if (dtQueue > 0) {
    if (rlState.queue > 0) {
      rlState.queue = Math.max(0, rlState.queue - (dtQueue * rlState.leakRate));
    }
    rlState.lastLeakTime = now;
  }
}

// Dispatch Live Request
function sendLiveRlReq(count = 1) {
  let okCount = 0;
  let throttleCount = 0;
  let lastStatus = 200;

  for (let i = 0; i < count; i++) {
    let allowed = false;

    if (currentAlgo === 'token-bucket') {
      if (rlState.tokens >= 1.0) {
        rlState.tokens -= 1.0;
        allowed = true;
      }
    } else if (currentAlgo === 'leaky-bucket') {
      if (rlState.queue + 1.0 <= rlState.queueCapacity) {
        rlState.queue += 1.0;
        allowed = true;
      }
    } else if (currentAlgo === 'sliding-window') {
      // Calculate sliding window weighted count
      const nowSec = Date.now() / 1000.0;
      const windowProgress = (nowSec % rlState.windowDuration) / rlState.windowDuration;
      const estimatedCount = (rlState.prevWindowCount * (1 - windowProgress)) + rlState.currWindowCount;
      if (estimatedCount + 1 <= rlState.windowLimit) {
        rlState.currWindowCount++;
        allowed = true;
      }
    } else if (currentAlgo === 'fixed-window') {
      const currentMinute = Math.floor(Date.now() / 60000);
      if (currentMinute !== rlState.fixedWindowStart) {
        rlState.fixedWindowStart = currentMinute;
        rlState.fixedWindowCount = 0;
      }
      if (rlState.fixedWindowCount + 1 <= rlState.fixedLimit) {
        rlState.fixedWindowCount++;
        allowed = true;
      }
    }

    if (allowed) {
      okCount++;
      rlState.totalOk++;
      lastStatus = 200;
    } else {
      throttleCount++;
      rlState.totalThrottled++;
      lastStatus = 429;
    }
  }

  // Record into rolling history
  const lastIdx = rlState.rollingHistory.length - 1;
  rlState.rollingHistory[lastIdx] = {
    ok: rlState.rollingHistory[lastIdx].ok + okCount,
    throttled: rlState.rollingHistory[lastIdx].throttled + throttleCount
  };

  // Log to Gateway Terminal
  if (okCount > 0) {
    logLiveRl(`HTTP/1.1 200 OK &bull; [${currentAlgo.toUpperCase()}] Passed ${okCount} req(s). (Remaining quota: ${getRemainingQuota().toFixed(1)})`, 'ok');
  }
  if (throttleCount > 0) {
    logLiveRl(`HTTP/1.1 429 Too Many Requests &bull; [${currentAlgo.toUpperCase()}] Throttled ${throttleCount} req(s)! Retry-After: ${getRetryAfter()}s`, 'err');
  }

  updateHttpTelemetry(lastStatus);
  updateLiveRlUI();
}

function getRemainingQuota() {
  if (currentAlgo === 'token-bucket') return rlState.tokens;
  if (currentAlgo === 'leaky-bucket') return Math.max(0, rlState.queueCapacity - rlState.queue);
  if (currentAlgo === 'sliding-window') {
    const nowSec = Date.now() / 1000.0;
    const windowProgress = (nowSec % rlState.windowDuration) / rlState.windowDuration;
    const est = (rlState.prevWindowCount * (1 - windowProgress)) + rlState.currWindowCount;
    return Math.max(0, rlState.windowLimit - est);
  }
  return Math.max(0, rlState.fixedLimit - rlState.fixedWindowCount);
}

function getRetryAfter() {
  if (currentAlgo === 'token-bucket') {
    if (rlState.refillRate <= 0) return 999;
    return Math.ceil((1.0 - rlState.tokens) / rlState.refillRate) || 1;
  }
  if (currentAlgo === 'leaky-bucket') {
    return Math.ceil(rlState.queue / rlState.leakRate) || 1;
  }
  return 12;
}

// Continuous Traffic Generator
function toggleContinuousTraffic() {
  isContinuousRunning = !isContinuousRunning;
  const btn = document.getElementById('btn-continuous-traffic');
  const lbl = document.getElementById('lbl-continuous-traffic');

  if (isContinuousRunning) {
    if (btn) btn.className = 'px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-amber-500 text-slate-950 transition-all flex items-center gap-1.5 shadow-lg shadow-amber-500/20';
    if (lbl) lbl.innerText = 'Stop Traffic';
    continuousTrafficInterval = setInterval(() => {
      sendLiveRlReq(2); // 100ms * 10 = 20 req/sec
    }, 100);
    logLiveRl('[TRAFFIC GEN] Sustained 20 QPS background request generator started.', 'info');
  } else {
    clearInterval(continuousTrafficInterval);
    if (btn) btn.className = 'px-3 py-1.5 rounded-xl text-xs font-mono font-bold bg-indigo-500/15 text-indigo-400 border border-indigo-500/30 hover:bg-indigo-500/25 transition-all flex items-center gap-1.5';
    if (lbl) lbl.innerText = 'Auto 15 QPS';
    logLiveRl('[TRAFFIC GEN] Background traffic generator stopped.', 'info');
  }
}

// 100-Req DDoS Surge
function triggerDdosAttack() {
  logLiveRl('[SECURITY ALERT] Inbound 100-request DDoS burst detected across single subnet!', 'err');
  sendLiveRlReq(100);
}

function resetRlState() {
  syncTenantParams();
  rlState.tokens = rlState.capacity;
  rlState.queue = 0;
  rlState.currWindowCount = 0;
  rlState.prevWindowCount = 20;
  rlState.fixedWindowCount = 0;
  rlState.totalOk = 0;
  rlState.totalThrottled = 0;
  logLiveRl('[SYSTEM RESET] Rate limiter metrics and tokens reset to default baseline.', 'info');
  updateLiveRlUI();
}

function toggleLuaScriptModal() {
  const c = document.getElementById('rl-lua-code-container');
  const btn = document.getElementById('btn-toggle-lua');
  if (!c) return;
  if (c.classList.contains('hidden')) {
    c.classList.remove('hidden');
    if (btn) btn.innerText = 'Hide Lua Script';
  } else {
    c.classList.add('hidden');
    if (btn) btn.innerText = 'View Lua Script';
  }
}

// Update HTTP RFC 6585 Telemetry
function updateHttpTelemetry(status) {
  const pill = document.getElementById('rl-http-status-pill');
  const codeEl = document.getElementById('rl-res-code');
  const limitEl = document.getElementById('rl-res-limit');
  const remEl = document.getElementById('rl-res-remaining');
  const resetEl = document.getElementById('rl-res-reset');
  const retryEl = document.getElementById('rl-res-retry');
  const policyEl = document.getElementById('rl-res-policy');

  const rem = Math.max(0, Math.floor(getRemainingQuota()));
  const retry = getRetryAfter();
  const resetTimestamp = Math.floor(Date.now() / 1000) + 60;

  if (status === 200) {
    if (pill) { pill.innerText = 'HTTP 200 OK'; pill.className = 'text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'; }
    if (codeEl) { codeEl.innerText = '200 OK (Allowed)'; codeEl.className = 'text-emerald-400 font-bold'; }
    if (retryEl) { retryEl.innerText = '0s (Quota Available)'; retryEl.className = 'text-slate-500'; }
  } else {
    if (pill) { pill.innerText = 'HTTP 429 TOO MANY REQUESTS'; pill.className = 'text-[10px] px-2 py-0.5 rounded font-bold bg-rose-500/20 text-rose-400 border border-rose-500/40 animate-pulse'; }
    if (codeEl) { codeEl.innerText = '429 Too Many Requests'; codeEl.className = 'text-rose-400 font-bold'; }
    if (retryEl) { retryEl.innerText = `${retry}s (Retry-After header active)`; retryEl.className = 'text-rose-400 font-bold'; }
  }

  if (limitEl) limitEl.innerText = rlState.capacity;
  if (remEl) remEl.innerText = rem;
  if (resetEl) resetEl.innerText = `${resetTimestamp} (in 60s)`;
  if (policyEl) policyEl.innerText = `"${rlState.capacity};w=60;burst=${rlState.capacity}"`;
}

// Update UI Telemetry & Counters
function updateLiveRlUI() {
  const t = RL_TENANTS[currentTenant] || RL_TENANTS.pro;

  // Counter Badges
  const sOk = document.getElementById('rl-stat-ok'); if (sOk) sOk.innerText = rlState.totalOk.toLocaleString();
  const sThr = document.getElementById('rl-stat-throttled'); if (sThr) sThr.innerText = rlState.totalThrottled.toLocaleString();
  
  // QPS Meter (sum of ok + throttled in last 2 seconds / 2)
  const recent = rlState.rollingHistory.slice(-2);
  const qps = ((recent[0].ok + recent[0].throttled + recent[1].ok + recent[1].throttled) / 2.0).toFixed(1);
  const sQps = document.getElementById('rl-stat-qps'); if (sQps) sQps.innerText = `${qps} req/s`;

  // Capacity Labels
  const capVal = document.getElementById('rl-stat-capacity');
  const refVal = document.getElementById('rl-stat-refill');
  const levelText = document.getElementById('live-rl-meter-text');

  if (currentAlgo === 'token-bucket') {
    if (capVal) capVal.innerText = `${rlState.capacity} Tokens`;
    if (refVal) refVal.innerText = `${rlState.refillRate.toFixed(1)} / sec`;
    if (levelText) {
      levelText.innerText = `${rlState.tokens.toFixed(1)} / ${rlState.capacity}`;
      levelText.className = rlState.tokens > (rlState.capacity * 0.3) ? 'font-bold text-emerald-400' : (rlState.tokens > 0 ? 'font-bold text-amber-400' : 'font-bold text-rose-400');
    }
  } else if (currentAlgo === 'leaky-bucket') {
    if (capVal) capVal.innerText = `${rlState.queueCapacity} Buffer Slots`;
    if (refVal) refVal.innerText = `Drain: ${rlState.leakRate.toFixed(1)} / s`;
    if (levelText) {
      levelText.innerText = `Queue: ${rlState.queue.toFixed(1)} / ${rlState.queueCapacity}`;
      levelText.className = rlState.queue < (rlState.queueCapacity * 0.7) ? 'font-bold text-emerald-400' : 'font-bold text-rose-400';
    }
  } else {
    if (capVal) capVal.innerText = `${rlState.windowLimit} Req / Min`;
    if (refVal) refVal.innerText = `Sliding Window`;
    if (levelText) {
      const quota = getRemainingQuota();
      levelText.innerText = `Remaining: ${quota.toFixed(0)} / ${rlState.windowLimit}`;
      levelText.className = quota > 10 ? 'font-bold text-emerald-400' : 'font-bold text-rose-400';
    }
  }

  // Update Redis In-Memory State Display
  const rKey = document.getElementById('rl-redis-key'); if (rKey) rKey.innerText = `rl:${t.key}`;
  const rTok = document.getElementById('rl-redis-tokens'); if (rTok) rTok.innerText = rlState.tokens.toFixed(2);
  const rLast = document.getElementById('rl-redis-last'); if (rLast) rLast.innerText = (Date.now() / 1000).toFixed(3);
}

// Render Animated SVG Physics View (Visual mechanism of the chosen algorithm)
function renderRlPhysicsSVG() {
  const svg = document.getElementById('live-rl-physics-svg');
  if (!svg) return;

  const width = 520, height = 280;

  if (currentAlgo === 'token-bucket') {
    // RENDER TOKEN BUCKET CYLINDER WITH LIQUID FILL & PARTICLES
    const pct = Math.max(0, Math.min(100, (rlState.tokens / rlState.capacity) * 100));
    const fillHeight = (pct / 100) * 130;
    const fillY = 200 - fillHeight;
    const color = pct > 30 ? '#10b981' : (pct > 5 ? '#f59e0b' : '#f43f5e');

    svg.innerHTML = `
      <defs>
        <linearGradient id="tokenFluid" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="${color}" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="${color}" stop-opacity="0.2"/>
        </linearGradient>
      </defs>

      <!-- Grid Backdrop -->
      <line x1="40" y1="210" x2="480" y2="210" stroke="#1e293b" stroke-width="1" stroke-dasharray="4"/>

      <!-- Refill Pipe (Left/Top) -->
      <path d="M 120 20 L 120 60 L 190 60" fill="none" stroke="#334155" stroke-width="8" stroke-linecap="round"/>
      <text x="120" y="15" fill="#06b6d4" font-size="9" font-family="monospace" text-anchor="middle">+${rlState.refillRate}/s Refill Nozzle</text>
      
      <!-- Falling Refill Droplet -->
      <circle cx="200" cy="60" r="4" fill="#00f0ff" opacity="0.8">
        <animate attributeName="cy" values="60;100" dur="0.8s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;0" dur="0.8s" repeatCount="indefinite"/>
      </circle>

      <!-- Token Bucket Tank Container -->
      <rect x="180" y="70" width="160" height="130" rx="8" fill="#0b0f19" stroke="#334155" stroke-width="2"/>
      
      <!-- Liquid / Token Fill Level -->
      <rect x="182" y="${fillY}" width="156" height="${fillHeight}" rx="4" fill="url(#tokenFluid)"/>
      <line x1="182" y1="${fillY}" x2="338" y2="${fillY}" stroke="${color}" stroke-width="2"/>

      <!-- Gauge Markers -->
      <text x="345" y="75" fill="#64748b" font-size="8" font-family="monospace">100% (${rlState.capacity})</text>
      <text x="345" y="135" fill="#64748b" font-size="8" font-family="monospace">50%</text>
      <text x="345" y="198" fill="#64748b" font-size="8" font-family="monospace">0% (Empty)</text>

      <!-- Drain Valve Pipe -->
      <rect x="250" y="200" width="20" height="30" fill="#1e293b"/>
      
      <!-- Gateway Filter Gate (Bottom) -->
      <g transform="translate(180, 230)">
        <rect width="160" height="35" rx="8" fill="#0f172a" stroke="${pct > 0 ? '#10b981' : '#f43f5e'}" stroke-width="2"/>
        <text x="80" y="18" fill="#f8fafc" font-size="10" font-weight="bold" font-family="monospace" text-anchor="middle">
          ${pct > 0 ? 'GATEWAY: 200 ALLOWED' : 'GATEWAY: 429 BLOCKED'}
        </text>
        <text x="80" y="28" fill="${pct > 0 ? '#34d399' : '#fb7185'}" font-size="8" font-family="monospace" text-anchor="middle">
          ${pct > 0 ? 'Token deducted &bull; Passed to backend' : 'Zero tokens &bull; Client quarantined'}
        </text>
      </g>
    `;
  } else if (currentAlgo === 'leaky-bucket') {
    // RENDER LEAKY BUCKET FUNNEL WITH WATER DROPS
    const queuePct = Math.min(100, (rlState.queue / rlState.queueCapacity) * 100);
    const qColor = queuePct > 80 ? '#f43f5e' : (queuePct > 40 ? '#f59e0b' : '#38bdf8');

    svg.innerHTML = `
      <!-- Funnel Outer Contour -->
      <polygon points="170,40 350,40 280,180 240,180" fill="#0b0f19" stroke="#334155" stroke-width="2"/>
      
      <!-- Funnel Buffer Queue Fill -->
      <polygon points="190,70 330,70 270,175 250,175" fill="${qColor}" opacity="0.3"/>

      <!-- Funnel Tube -->
      <rect x="245" y="180" width="30" height="35" fill="#1e293b" stroke="#334155"/>

      <!-- Labels -->
      <text x="260" y="25" fill="#f8fafc" font-size="10" font-weight="bold" font-family="monospace" text-anchor="middle">FIFO BUFFER QUEUE (${rlState.queue.toFixed(0)} / ${rlState.queueCapacity})</text>
      <text x="360" y="110" fill="#64748b" font-size="9" font-family="monospace">Burst Buffer</text>
      
      <!-- Constant Leak Droplets -->
      <circle cx="260" cy="225" r="4" fill="#38bdf8">
        <animate attributeName="cy" values="220;260" dur="0.6s" repeatCount="indefinite"/>
      </circle>

      <!-- Smooth Egress Destination Box -->
      <rect x="180" y="240" width="160" height="30" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="260" y="258" fill="#38bdf8" font-size="9" font-weight="bold" font-family="monospace" text-anchor="middle">
        SMOOTH EGRESS (${rlState.leakRate}/sec)
      </text>
    `;
  } else {
    // RENDER SLIDING WINDOW TIMELINE RULER
    const progress = (Math.floor(Date.now() / 1000) % 60) / 60.0;
    const prevWeight = ((1 - progress) * 100).toFixed(0);
    const currWeight = (progress * 100).toFixed(0);

    svg.innerHTML = `
      <!-- Time axis -->
      <line x1="50" y1="140" x2="470" y2="140" stroke="#334155" stroke-width="3"/>
      
      <!-- Window t-1 (Previous) -->
      <rect x="60" y="70" width="190" height="90" rx="8" fill="#1e293b" opacity="0.4" stroke="#475569" stroke-width="1"/>
      <text x="155" y="95" fill="#94a3b8" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">PREVIOUS WINDOW [t-1]</text>
      <text x="155" y="115" fill="#cbd5e1" font-size="12" font-family="monospace" text-anchor="middle">${rlState.prevWindowCount} requests</text>
      <text x="155" y="135" fill="#06b6d4" font-size="9" font-family="monospace" text-anchor="middle">Weighted: ${prevWeight}%</text>

      <!-- Window t (Current) -->
      <rect x="270" y="70" width="190" height="90" rx="8" fill="#064e3b" opacity="0.4" stroke="#10b981" stroke-width="1.5"/>
      <text x="365" y="95" fill="#34d399" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">CURRENT WINDOW [t]</text>
      <text x="365" y="115" fill="#ffffff" font-size="12" font-family="monospace" text-anchor="middle">${rlState.currWindowCount} requests</text>
      <text x="365" y="135" fill="#34d399" font-size="9" font-family="monospace" text-anchor="middle">Weighted: ${currWeight}%</text>

      <!-- Sliding Indicator -->
      <line x1="${160 + (progress * 180)}" y1="40" x2="${160 + (progress * 180)}" y2="180" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4"/>
      <circle cx="${160 + (progress * 180)}" cy="40" r="5" fill="#f43f5e"/>
      <text x="${160 + (progress * 180)}" y="30" fill="#f43f5e" font-size="8" font-family="monospace" text-anchor="middle">NOW: ${(progress * 60).toFixed(0)}s</text>

      <!-- Formula output banner -->
      <rect x="80" y="210" width="360" height="40" rx="8" fill="#0f172a" stroke="#334155"/>
      <text x="260" y="235" fill="#f8fafc" font-size="10" font-family="monospace" text-anchor="middle">
        Estimated Window Load: ${Math.round((rlState.prevWindowCount * (1 - progress)) + rlState.currWindowCount)} / ${rlState.windowLimit} req/min
      </text>
    `;
  }
}

// Shift Rolling 20-Second Chart
function shiftRollingChart() {
  rlState.rollingHistory.shift();
  rlState.rollingHistory.push({ ok: 0, throttled: 0 });
  renderRollingChart();
}

function renderRollingChart() {
  const chartSvg = document.getElementById('rl-rolling-chart-svg');
  if (!chartSvg) return;

  const barWidth = 20;
  const gap = 5;
  const maxHeight = 50;

  // Find max value in history for scaling
  let maxVal = 10;
  rlState.rollingHistory.forEach(d => {
    if (d.ok + d.throttled > maxVal) maxVal = d.ok + d.throttled;
  });

  let svgHtml = '';
  rlState.rollingHistory.forEach((d, i) => {
    const x = i * (barWidth + gap) + 10;
    const okH = Math.round((d.ok / maxVal) * maxHeight);
    const thrH = Math.round((d.throttled / maxVal) * maxHeight);

    const okY = 60 - okH;
    const thrY = okY - thrH;

    if (okH > 0) {
      svgHtml += `<rect x="${x}" y="${okY}" width="${barWidth}" height="${okH}" rx="2" fill="#10b981"/>`;
    }
    if (thrH > 0) {
      svgHtml += `<rect x="${x}" y="${thrY}" width="${barWidth}" height="${thrH}" rx="2" fill="#f43f5e"/>`;
    }
    if (okH === 0 && thrH === 0) {
      svgHtml += `<line x1="${x}" y1="59" x2="${x + barWidth}" y2="59" stroke="#1e293b" stroke-width="2"/>`;
    }
  });

  chartSvg.innerHTML = svgHtml;
}

// Update Algorithm Deep Dive Description Text & Formula
function updateAlgoDeepDiveText() {
  const tEl = document.getElementById('rl-algo-title');
  const fBox = document.getElementById('rl-algo-formula-box');
  const exp = document.getElementById('rl-algo-explanation');
  const std = document.getElementById('rl-algo-standard');

  if (currentAlgo === 'token-bucket') {
    if (tEl) tEl.innerText = 'TOKEN BUCKET ARCHITECTURAL MATHEMATICS';
    if (std) std.innerText = 'Stripe / AWS / GitHub Standard';
    if (fBox) fBox.innerHTML = '$$\\text{tokens}_{\\text{new}} = \\min\\Big(B,\\; \\text{tokens}_{\\text{old}} + \\Delta t \\times R\\Big) - 1$$';
    if (exp) exp.innerHTML = '<strong>How it works:</strong> A bucket holds up to $B$ tokens. Every second, $R$ tokens are deposited into the bucket. Each HTTP request consumes 1 token. If the bucket is empty, the request is instantly rejected with HTTP 429. Allows short bursts up to $B$ while guaranteeing average throughput never exceeds $R$.';
  } else if (currentAlgo === 'leaky-bucket') {
    if (tEl) tEl.innerText = 'LEAKY BUCKET (TRAFFIC SHAPING) MATHEMATICS';
    if (std) std.innerText = 'NGINX / Celery Queue Standard';
    if (fBox) fBox.innerHTML = '$$\\text{queue}_{\\text{new}} = \\max\\Big(0,\\; \\text{queue}_{\\text{old}} - \\Delta t \\times L\\Big) + 1$$';
    if (exp) exp.innerHTML = '<strong>How it works:</strong> Requests drop into a FIFO buffer of capacity $Q$. A background worker processes requests out of the funnel at a constant leak rate $L$. Eliminates bursts completely, smoothing jagged traffic into a flat, predictable stream for downstream databases.';
  } else if (currentAlgo === 'sliding-window') {
    if (tEl) tEl.innerText = 'SLIDING WINDOW COUNTER MATHEMATICS';
    if (std) std.innerText = 'Cloudflare / Twitter API Standard';
    if (fBox) fBox.innerHTML = '$$\\text{Count} = \\text{PrevWindowCount} \\times (1 - \\text{Progress}) + \\text{CurrWindowCount}$$';
    if (exp) exp.innerHTML = '<strong>How it works:</strong> Estimates request frequency by weighting the previous window by the remaining fraction of time. Eliminates the double-capacity boundary vulnerability of Fixed Window, while using only 2 counter integers in Redis ($O(1)$ memory).';
  } else {
    if (tEl) tEl.innerText = 'FIXED WINDOW COUNTER VULNERABILITY';
    if (std) std.innerText = 'Basic Memcached INCR';
    if (fBox) fBox.innerHTML = '$$\\text{Window}_{\\text{ID}} = \\Big\\lfloor \\frac{\\text{Timestamp}}{60} \\Big\\rfloor, \\quad \\text{INCR } \\text{key}$$';
    if (exp) exp.innerHTML = '<strong>Vulnerability:</strong> If a client sends 60 requests at 00:59 and another 60 requests at 01:01, both pass! The server experiences 120 requests in a 2-second interval ($2\\times$ overload attack).';
  }
}

function logLiveRl(msg, type = 'info') {
  const term = document.getElementById('live-rl-terminal');
  if (!term) return;
  const time = new Date().toISOString().substring(11, 19);
  const color = type === 'ok' ? 'text-emerald-400 font-mono' : (type === 'err' ? 'text-rose-400 font-bold font-mono' : 'text-slate-400');
  const row = document.createElement('div');
  row.className = color;
  row.innerHTML = `<span class="text-slate-600">[${time}]</span> ${msg}`;
  term.prepend(row);
}

function clearLiveRlLogs() {
  const term = document.getElementById('live-rl-terminal');
  if (term) term.innerHTML = '<div class="text-slate-600">[READY] Gateway access logs cleared.</div>';
}

// Initial Kick-off
try {
  startLiveRlEngine();
  updateAlgoDeepDiveText();
} catch(e) {}



/* =========================================================================
   GOD-LEVEL FAANG/STAFF+ SYSTEM DESIGN INTERVIEW SUITE (InterviewOS Pro)
   ========================================================================= */

// 8 Comprehensive FAANG Prompt Archetypes
const INTERVIEW_PROBLEMS = {
  stripe: {
    id: "stripe",
    title: "Design a Distributed Global Payment Engine (Stripe / Adyen)",
    tag: "FAANG ARCHETYPE: GLOBAL PAYMENTS",
    target: "Target Scale: 10,000 TPS &bull; 99.999% SLA &bull; Exactly-Once",
    calcDefaults: { dau: 100000000, actions: 5, ratio: 1, payload: 4.0, peak: 4.0 },
    phases: {
      1: {
        title: "Phase 1: Clarifying Requirements & Scoping (00:00 - 05:00)",
        checklist: [
          "Clarify payment flows: Credit cards, digital wallets (Apple Pay), ACH bank transfers, webhooks.",
          "Identify 3 core use cases: (1) Authorize & Capture, (2) Merchant Settlement Payouts, (3) Automated Refund Ledgers.",
          "Declare Out-of-Scope: PCI-DSS hardware appliance fabrication, KYC passport scanning, physical credit card printing.",
          "Non-Functional SLA: Zero double-charging (Idempotency guarantee), strictly serializable double-entry ledger, &lt; 250ms P99."
        ]
      },
      2: {
        title: "Phase 2: Back-of-the-Envelope Capacity & API Contract (05:00 - 12:00)",
        api: `// Idempotent Charge API Endpoint
POST /v1/charges
Headers:
  Idempotency-Key: idemp_94f8a2c1_uuidv4
  Authorization: Bearer sec_key_live_...
Payload:
{
  "amount_cents": 4999,
  "currency": "USD",
  "customer_id": "cus_9201",
  "merchant_id": "acct_8812",
  "payment_method_id": "pm_card_visa_4242"
}
Response 200 OK:
{
  "charge_id": "ch_7731",
  "status": "succeeded",
  "created_at": 1727440800,
  "ledger_tx_id": "ltx_9901"
}`,
        checklist: [
          "10,000 TPS average &bull; 40,000 TPS peak during Black Friday / Cyber Monday.",
          "Network: 4 KB average payload &times; 40,000 peak = 160 MB/sec (1.28 Gbps network ingress).",
          "Double-entry bookkeeping table: Immutable append-only debit/credit rows. 5-year storage: ~600 TB."
        ]
      },
      3: {
        title: "Phase 3: High-Level End-to-End Architecture (12:00 - 25:00)",
        topologyDesc: "Client &rarr; Anycast Cloudflare Edge &rarr; L7 Envoy Gateway &rarr; Idempotency Service (Redis Distributed Lock + PostgreSQL Unique Constraint) &rarr; Payment Orchestrator (SAGA state machine) &rarr; External Acquiring Banks (Visa/Mastercard) &rarr; Immutable Double-Entry Ledger (CockroachDB / Spanner) &rarr; Kafka Event Stream &rarr; Merchant Webhook Dispatcher.",
        checklist: [
          "Why CockroachDB / Google Spanner for the ledger? TrueTime serializability guarantees zero phantom writes without single-primary DB bottlenecks.",
          "Idempotency Guard: Redis SETNX key with 120s lease to prevent concurrent duplicate clicks; DB unique constraint on idempotency_key + merchant_id."
        ]
      },
      4: {
        title: "Phase 4: Component Deep-Dive & Bottleneck Mitigation (25:00 - 40:00)",
        checklist: [
          "Bank Timeout Reconciliation: If Visa times out with HTTP 504, NEVER mark transaction failed! Put into 'PENDING' state and query Acquiring Bank status via scheduled polling job before attempting refund.",
          "Dead-Letter Queues (DLQ) & Exponential Jitter: Webhook deliveries to merchants use exponential backoff with full jitter across 72 hours.",
          "Partitioning Strategy: Shard transaction tables by merchant_id hash. Use virtual ledger balancing accounts to prevent merchant-level write contention."
        ]
      },
      5: {
        title: "Phase 5: Staff+ Trade-offs, Failure Modes & Wrap-up (40:00 - 45:00)",
        checklist: [
          "2-Phase Commit (2PC) vs SAGA: Avoid synchronous 2PC across external third-party payment gateways; use Compensating SAGA Transactions with distributed state machines.",
          "Disaster Recovery (RPO=0, RTO < 30s): Multi-region synchronous replication across 3 Availability Zones. Read replicas for merchant analytics."
        ]
      }
    }
  },
  tiktok: {
    id: "tiktok",
    title: "Design Real-Time Live Stream Comments & Reactions (TikTok / Twitch)",
    tag: "FAANG ARCHETYPE: HIGH-CONCURRENCY CHAT",
    target: "Target Scale: 50,000,000 Viewers on 1 Stream &bull; Fanout-on-Read",
    calcDefaults: { dau: 500000000, actions: 40, ratio: 50, payload: 0.5, peak: 5.0 },
    phases: {
      1: {
        title: "Phase 1: Clarifying Requirements & Scoping (00:00 - 05:00)",
        checklist: [
          "Scale scope: Top celebrity live stream with 50M concurrent viewers dropping 500,000 comments/sec.",
          "Human perception limit: Humans can only read ~10 comments/sec. Showing all 500,000 comments crashes mobile apps!",
          "Non-Functional: Sub-500ms broadcast latency, lossy comment sampling under extreme spikes, zero server OOM crashes."
        ]
      },
      2: {
        title: "Phase 2: Capacity & API Signatures (05:00 - 12:00)",
        api: `// WebSocket Chat Stream Protocol (Bi-directional)
WS wss://chat.live.tiktok.com/v1/stream/{stream_id}
Message Inbound:
{
  "type": "comment",
  "user_id": "u_948",
  "text": "Amazing stream!",
  "badge": "vip"
}
Broadcast Outbound (Batched 100ms array):
{
  "type": "comment_batch",
  "count": 8,
  "comments": [...]
}`,
        checklist: [
          "50M concurrent connections &times; 8 KB WebSocket memory per socket = ~400 GB RAM across connection edge gateway tier.",
          "400 edge gateway nodes (125,000 WebSockets per gateway instance via epoll / Linux socket tuning)."
        ]
      },
      3: {
        title: "Phase 3: High-Level Architecture (12:00 - 25:00)",
        topologyDesc: "Mobile App &rarr; Anycast L4 BGP Maglev &rarr; WebSocket Gateway Fleet (Envoy with TCP proxy) &rarr; Kafka Comment Partition Topic (Keyed by stream_id) &rarr; Dynamic Rate Sampler Service (Drop algorithm based on stream QPS) &rarr; Redis Pub/Sub Fanout Hub &rarr; Gateway Broadcast Egress.",
        checklist: [
          "Fanout on Read vs Fanout on Write: NEVER push 500,000 messages to 50,000,000 sockets individually (would require 25 Trillion network writes/sec!).",
          "Dynamic Sampling: If stream QPS > 50,000/s, dynamically sample comments based on VIP badges, algorithmic quality score, and uniform lottery."
        ]
      },
      4: {
        title: "Phase 4: Component Deep-Dive & Scale (25:00 - 40:00)",
        checklist: [
          "Backpressure Management: If mobile device network throttles, gateway server drops comment batches rather than buffering into RAM and triggering OOM crashes.",
          "Redis Pub/Sub bottleneck: A single Redis instance cannot broadcast to 400 gateways at high QPS. Use hierarchical Redis broker tree."
        ]
      },
      5: {
        title: "Phase 5: Staff+ Trade-offs & Wrap-up (40:00 - 45:00)",
        checklist: [
          "WebSockets vs HTTP/3 Server-Sent Events (SSE): SSE has automatic HTTP/2 multiplexing, but WebSockets allow low-latency bidirectional reaction hearts.",
          "Trade-off: Accept partial message loss in chat stream to maintain sub-second video synchronization."
        ]
      }
    }
  },
  s3: {
    id: "s3",
    title: "Design a Planet-Scale Distributed Object Store (AWS S3)",
    tag: "FAANG ARCHETYPE: DISTRIBUTED STORAGE",
    target: "Target Scale: Exabytes of Storage &bull; 99.999999999% (11 9s) Durability",
    calcDefaults: { dau: 50000000, actions: 10, ratio: 10, payload: 1024.0, peak: 2.5 },
    phases: {
      1: {
        title: "Phase 1: Clarifying Requirements & Scoping (00:00 - 05:00)",
        checklist: [
          "Core operations: PutObject, GetObject, DeleteObject, ListObjects (prefix queries).",
          "Payload range: Small objects (4 KB) to giant video blobs (5 TB via multipart upload).",
          "Durability goal: 11 Nines (99.999999999%) durability against entire datacenter destruction."
        ]
      },
      2: {
        title: "Phase 2: Capacity & Math (05:00 - 12:00)",
        api: `PUT /bucket_name/object_key HTTP/1.1
Host: s3.us-east-1.amazonaws.com
x-amz-storage-class: STANDARD
Content-Length: 10485760
Content-Type: video/mp4

[10 MB Binary Stream Data]`,
        checklist: [
          "Durability strategy: 3-way cross-datacenter replication costs 300% storage overhead.",
          "Erasure Coding (8+4 Reed-Solomon): Breaks object into 8 data chunks + 4 parity chunks. Can tolerate ANY 4 disk/server/AZ failures with only 1.5x (50%) storage overhead!"
        ]
      },
      3: {
        title: "Phase 3: High-Level Architecture (12:00 - 25:00)",
        topologyDesc: "Client &rarr; API Gateway (Chunker & Multipart assembler) &rarr; Metadata Engine (Key-value LSM index with Raft consensus) &rarr; Placement Service &rarr; Storage Nodes (Append-only Bitcask chunk store on raw block NVMe).",
        checklist: [
          "Metadata / Blob Separation: Metadata (bucket, key, size, ACL, chunk IDs) stored in Spanner/CockroachDB; Raw payload bytes written directly to append-only disk files.",
          "Small File Problem: Writing millions of 4 KB files to ext4 causes inode exhaustion. Bundle small objects into 64 MB append-only chunk packs (Haystack / Bitcask)."
        ]
      },
      4: {
        title: "Phase 4: Deep Dive & Reliability (25:00 - 40:00)",
        checklist: [
          "Bit Rot Detection: Background scrubbing worker continuously reads chunks, computes SHA-256 checksums, and uses Reed-Solomon parity to rebuild corrupted sectors.",
          "Hot Partition Mitigation: When a bucket receives 100,000 writes/sec to keys like '2026-09-27/file1.png', hash-prefix the metadata key to distribute writes across all metadata shards."
        ]
      },
      5: {
        title: "Phase 5: Staff+ Trade-offs & Wrap-up (40:00 - 45:00)",
        checklist: [
          "Strong Consistency vs Eventual Consistency: S3 transitioned from eventual consistency to strong read-after-write consistency by coordinating metadata commits synchronously via Paxos/Raft.",
          "Cost optimization: Tiered lifecycle engine migrating cold objects to Erasure Coded Glacier deep tape storage after 90 days."
        ]
      }
    }
  },
  uber: {
    id: "uber",
    title: "Design Real-Time Geospatial Driver-Rider Dispatch (Uber / Lyft)",
    tag: "FAANG ARCHETYPE: GEOSPATIAL REAL-TIME",
    target: "Target Scale: 1,000,000 Active Drivers &bull; Sub-Second Dispatch",
    calcDefaults: { dau: 25000000, actions: 15, ratio: 5, payload: 1.0, peak: 3.5 },
    phases: {
      1: {
        title: "Phase 1: Clarifying Requirements & Scoping (00:00 - 05:00)",
        checklist: [
          "Driver location heartbeats: Every driver emits GPS ping (lat, lng, bearing, status) every 4 seconds.",
          "Rider matching: Query top 10 nearest available drivers within 3 km radius in < 100ms.",
          "Dispatch lock: Prevent two riders from simultaneously matching the same driver (Zero race condition)."
        ]
      },
      2: {
        title: "Phase 2: Capacity & Indexing Math (05:00 - 12:00)",
        api: `// Driver Location Ping
POST /v1/driver/location
{
  "driver_id": "drv_8831",
  "lat": 37.7749,
  "lng": -122.4194,
  "h3_index": "8828308281fffff",
  "status": "AVAILABLE"
}`,
        checklist: [
          "1,000,000 drivers &divide; 4 seconds = 250,000 GPS writes/sec!",
          "Geospatial Indexing Choice: QuadTree vs Geohash vs Uber H3 Hexagonal Hierarchical Spatial Index.",
          "Why H3? Hexagons have identical distance to all 6 adjacent neighbors (unlike squares in Geohash where diagonals are 1.414x further!)."
        ]
      },
      3: {
        title: "Phase 3: High-Level Architecture (12:00 - 25:00)",
        topologyDesc: "Driver Phone &rarr; Netty Gateway &rarr; Location Ingestion Service &rarr; Redis H3 Hexagon Geospatial Cluster (In-memory ring buffer) &rarr; Dispatch Matching Engine &rarr; Distributed Lock (Redlock / etcd lease) &rarr; Push Notification Gateway (APNs/FCM) &rarr; Rider App.",
        checklist: [
          "In-Memory State: Never write 250,000 GPS pings/sec to disk DB (PostGIS will melt). Keep ephemeral locations in memory; persist historical trips asynchronously to Cassandra."
        ]
      },
      4: {
        title: "Phase 4: Deep Dive & Race Conditions (25:00 - 40:00)",
        checklist: [
          "Driver Match Locking: When Dispatch engine selects Driver A for Rider 1, acquire an atomic Redis lease: SET lock:driver:drv_8831 rider_1 NX EX 15. If already locked, immediately fall back to Driver B.",
          "Hexagonal Ring Search: If no drivers in primary H3 hexagon (Resolution 8), expand search to k-ring 1 (6 adjacent hexagons), then k-ring 2."
        ]
      },
      5: {
        title: "Phase 5: Staff+ Trade-offs & Wrap-up (40:00 - 45:00)",
        checklist: [
          "Greedy Nearest Neighbor vs Batch Optimization: Matching the single nearest driver greedily causes suboptimal global wait times; dispatching in 5-second batch auctions minimizes overall pickup ETA across the city.",
          "Cell phone disconnection resilience: Dead-reckoning location prediction when driver enters tunnels."
        ]
      }
    }
  },
  tinyurl: {
    id: "tinyurl",
    title: "Design Global URL Shortener with Analytics (TinyURL / Bitly)",
    tag: "FAANG ARCHETYPE: HIGH-THROUGHPUT READ",
    target: "Target Scale: 100:1 Read-to-Write Ratio &bull; Sub-10ms Global Reads",
    calcDefaults: { dau: 50000000, actions: 10, ratio: 100, payload: 0.5, peak: 3.0 },
    phases: {
      1: {
        title: "Phase 1: Scope & Boundaries (0-5m)",
        checklist: ["Short URL character set: Base62 [0-9, a-z, A-Z]. 7 characters = 62^7 = 3.5 Trillion URLs.", "Custom alias support and expiring URLs.", "High-scale click analytics telemetry."]
      },
      2: {
        title: "Phase 2: Capacity & Key Generation (5-12m)",
        api: `POST /v1/urls
{
  "long_url": "https://example.com/very/long/path",
  "custom_alias": "my-deal"
}
Response 201 Created:
{
  "short_url": "https://sho.rt/aZ94kL",
  "expires_at": 1758988800
}`,
        checklist: ["100:1 Read ratio: 2,000 write QPS, 200,000 read QPS.", "Why MD5/SHA256 hash collision handling fails at scale: pre-generating keys using a Key Generation Service (KGS) eliminates runtime collisions completely!"]
      },
      3: {
        title: "Phase 3: High-Level Architecture (12-25m)",
        topologyDesc: "Client &rarr; Anycast CDN &rarr; L7 NGINX &rarr; Shortener Service &rarr; Redis Cache Cluster &rarr; MongoDB / DynamoDB Shards (Keyed by 7-char short_key) &bull; KGS Token Dispenser (ZooKeeper range allocator) &bull; Kafka Analytics &rarr; ClickHouse OLAP.",
        checklist: ["HTTP 301 vs 302 Redirect: 301 Permanent allows browser caching (faster, but loses click analytics); 302 Temporary forces every redirect through server (captures 100% analytics)."]
      },
      4: {
        title: "Phase 4: Deep Dive & Cache Tiering (25-40m)",
        checklist: ["80/20 Pareto caching: Cache top 20% most active URLs in Redis to absorb 80% of 200,000 QPS.", "Cache Stampede defense: Use probabilistic early expiration (XFetch) or mutex locks to prevent DB swarming."]
      },
      5: {
        title: "Phase 5: Staff+ Trade-offs & Wrap-up (40-45m)",
        checklist: ["KGS Single Point of Failure mitigation: Standby KGS instances with pre-assigned unique range segments (e.g. Server 1 gets 1M-2M, Server 2 gets 2M-3M)."]
      }
    }
  },
  docs: {
    id: "docs",
    title: "Design Collaborative Document Editing (Google Docs / Figma)",
    tag: "FAANG ARCHETYPE: DISTRIBUTED CONCURRENCY",
    target: "Target Scale: CRDT / Operational Transformation &bull; Sub-50ms Sync",
    calcDefaults: { dau: 30000000, actions: 100, ratio: 2, payload: 0.1, peak: 4.0 },
    phases: {
      1: { title: "Phase 1: Scope & Concurrency (0-5m)", checklist: ["Multi-user simultaneous typing in same paragraph.", "Offline mode and conflict resolution upon reconnect.", "Preserve character formatting, cursors, and undo/redo stacks."] },
      2: { title: "Phase 2: Math & Conflict Protocols (5-12m)", api: `WS /v1/docs/{doc_id}
Client Action:
{
  "op": "insert",
  "char": "X",
  "site_id": "client_42",
  "clock": 142,
  "position_id": [0.384, 0.491]
}`, checklist: ["OT (Operational Transformation) vs CRDT (Conflict-free Replicated Data Type).", "OT requires a central server to order transformations; CRDTs mathematically converge peer-to-peer (Figma / modern Google Docs)."] },
      3: { title: "Phase 3: High-Level Architecture (12-25m)", topologyDesc: "Client Editor (Local CRDT LWW-Element-Set) &rarr; WebSockets &rarr; Collab Gateway Fleet &rarr; Room Coordinator (Pinned Redis / Envoy consistent hash) &rarr; Document Snapshot Store (S3) &bull; Append-only Mutation Log.", checklist: ["Session Affinity: Consistent hash routes all active collaborators of doc_id to the same room worker process to optimize in-memory merge speed."] },
      4: { title: "Phase 4: Deep Dive & Memory Limits (25-40m)", checklist: ["Tombstone garbage collection: In CRDTs, deleted characters leave tombstones that bloat RAM. Run scheduled snapshot compaction to purge tombstones when all active peers pass a vector clock baseline."] },
      5: { title: "Phase 5: Staff+ Trade-offs (40-45m)", checklist: ["Client memory overhead: RGA / Yjs CRDT structures require 2x-5x memory over plain text string buffers. Mitigate with block-level chunking."] }
    }
  },
  crawler: {
    id: "crawler",
    title: "Design Global Distributed Web Crawler (Googlebot)",
    tag: "FAANG ARCHETYPE: BATCH / ASYNC PIPELINE",
    target: "Target Scale: 10 Billion Web Pages &bull; Politeness & Deduplication",
    calcDefaults: { dau: 10000000, actions: 5, ratio: 1, payload: 50.0, peak: 2.0 },
    phases: {
      1: { title: "Phase 1: Scope & Crawler Ethics (0-5m)", checklist: ["Crawl 10B pages/month, respect robots.txt, avoid spider traps (infinite calendar URLs), calculate HTML hash deduplication."] },
      2: { title: "Phase 2: URL Frontier Math (5-12m)", api: `Worker Fetch Contract:\nGET /robots.txt\nGET /page_url\nExtract Outbound Links &rarr; Enqueue into Frontier`, checklist: ["10 Billion pages / month = ~3,850 pages crawled/sec.", "Storage: 50 KB avg compressed HTML = 500 Terabytes / month."] },
      3: { title: "Phase 3: Architecture (12-25m)", topologyDesc: "URL Frontier (Priority & Politeness Queues) &rarr; DNS Resolver Cache &rarr; Fetcher Workers (libcurl / Chromium headless) &rarr; Content Deduplicator (SimHash / Bloom Filter) &rarr; Link Extractor &rarr; Document Store (Bigtable / S3).", checklist: ["Politeness Queue design: 2-tier queue. Host queue enforces 1-second delay per domain (mercilessly protects target web servers from accidental DDoS)."] },
      4: { title: "Phase 4: Deep Dive & URL Filtering (25-40m)", checklist: ["Bloom Filter for Visited URLs: 10 Billion URLs with 0.1% false-positive rate requires only ~18 GB RAM in memory!"] },
      5: { title: "Phase 5: Staff+ Trade-offs (40-45m)", checklist: ["Dynamic JS rendering: Headless Chromium executes heavy React/Next.js pages at 10x CPU cost; use static HTML scrapers first, only falling back to headless browser if content is sparse."] }
    }
  },
  temporal: {
    id: "temporal",
    title: "Design Distributed Workflow & Job Orchestration Engine (Temporal / Cadence)",
    tag: "FAANG ARCHETYPE: DURABLE WORKFLOW EXECUTION",
    target: "Target Scale: Millions of Long-Running Distributed Workflows &bull; Replay",
    calcDefaults: { dau: 5000000, actions: 50, ratio: 2, payload: 10.0, peak: 3.0 },
    phases: {
      1: { title: "Phase 1: Scope & Durability (0-5m)", checklist: ["Support workflows executing across minutes, days, or months. Survive arbitrary server reboots without re-executing completed side-effects."] },
      2: { title: "Phase 2: Event Sourcing & APIs (5-12m)", api: `POST /v1/workflows/start
{
  "workflow_id": "wf_order_882",
  "workflow_type": "FulfillOrderWorkflow",
  "input": { "order_id": "ord_102" }
}`, checklist: ["Event History Log: Every activity start, task complete, and timer firing is an immutable append-only event in the workflow history."] },
      3: { title: "Phase 3: Architecture (12-25m)", topologyDesc: "Client SDK &rarr; Frontend Service &rarr; Matching Service &rarr; History Service (Shard Controller with Raft) &rarr; Cassandra / MySQL DB &bull; Activity Worker Pollers (gRPC long-polling).", checklist: ["Deterministic Replay: Workflow code is replayed from event log to rebuild local memory state after worker crashes."] },
      4: { title: "Phase 4: Deep Dive & Timers (25-40m)", checklist: ["Timer Queue: Implemented via hierarchical time-wheel or partitioned scheduled database tables to awaken sleeping workflows across days."] },
      5: { title: "Phase 5: Staff+ Trade-offs (40-45m)", checklist: ["Large History Mitigation: Workflows exceeding 10,000 events must trigger 'ContinueAsNew' to truncate history log and prevent memory bloat."] }
    }
  }
};

// Interviewer Grilling Curveball Database (Staff+ Trap Scenarios)
const CURVEBALL_DATABASE = [
  {
    category: "Split-Brain & Partitioning",
    prompt: "Network partition cleanly isolates us-east-1 from us-west-2. Both sides believe they are the legitimate leader and continue accepting customer writes. How does your architecture detect and resolve this split-brain without data corruption?",
    staffDefense: "Relying on heartbeat timeouts alone causes split-brain. We use consensus-backed Fencing Tokens (monotonically increasing epoch IDs issued by etcd/ZooKeeper) and majority quorums (Q = ⌊N/2⌋ + 1). The minority partition (1 of 3 AZs) fails the quorum check and immediately enters read-only safe mode. When writes reach downstream databases, the storage engine rejects any write containing an obsolete fencing epoch. Zero split-brain data corruption.",
    juniorTrap: "Junior/Mid candidates often say 'we'll ping both servers and pick the latest timestamp', falling directly into the Clock Skew / NTP drift trap where clock drift can overwrite valid transactions!"
  },
  {
    category: "Thundering Herd & Celebrity Fanout",
    prompt: "Elon Musk posts a tweet to 180 Million followers. If your system writes a copy of the tweet to all 180M follower home timelines (Fanout-on-Write), your database queue explodes by 180M rows in 2 seconds. How do you solve this?",
    staffDefense: "We implement a Hybrid Fanout Model (Celebrity Cutoff). For standard users with < 25,000 followers, we use Fanout-on-Write for instant sub-millisecond timeline reads. For celebrities (> 25k followers), we bypass fanout completely! When an ordinary follower opens Twitter, their home timeline dynamically fetches the pre-computed fanout feed AND executes a fast multi-key lookup to append the celebrity's recent tweets on-the-fly (Fanout-on-Read). Blends the speed of write fanout with the safety of read fanout.",
    juniorTrap: "Saying 'we will just scale up the Kafka queue workers' ignores the storage write amplification ($100\times$) and memory cache eviction avalanche."
  },
  {
    category: "Cascading Cache Avalanche & Dogpiling",
    prompt: "Your top Redis cluster holding 500,000 cached user sessions crashes simultaneously due to an AWS rack power failure. What prevents every inbound request from slamming the underlying database and causing total system collapse?",
    staffDefense: "We implement a 3-layer defensive bastion: (1) Jittered TTLs: Add random jitter to cache expirations ($TTL = 3600 + \text{rand}(-300, 300)$) to prevent simultaneous batch expirations. (2) Mutex Locking (Single-Flight Pattern): When a cache miss occurs, only ONE thread acquires a distributed lock to query the DB and warm the cache; all other threads await the result. (3) Circuit Breaker (Envoy / Resilience4j): If DB latency exceeds 200ms or 5xx errors breach 5%, trip the circuit breaker and serve stale cache or graceful fallback responses.",
    juniorTrap: "Assuming that adding more read replicas will survive a sudden $100\times$ database query surge."
  },
  {
    category: "Distributed Concurrency & Race Conditions",
    prompt: "Two users in London and Tokyo attempt to book the final remaining hotel suite at the exact same millisecond. Prove how your architecture guarantees zero double-booking while sustaining 50,000 search QPS.",
    staffDefense: "We separate Search from Booking. Search reads from read-replica caches. When the user clicks 'Book', the request hits an isolated Reservation Service that uses Optimistic Concurrency Control (OCC) with row versioning: UPDATE inventory SET status='BOOKED', version=version+1 WHERE room_id=102 AND version=4. Only the first commit succeeds; the second receives an affected row count of 0 and is immediately shown 'Room already booked by another user'. For high-contention flash sales, we use an in-memory Redis token decrement with Lua (DECR inventory:room_102) before touching the DB.",
    juniorTrap: "Using distributed 2-Phase Commit (2PC) or global database table locks, which causes catastrophic query lockups across the entire database."
  }
];

// Current State
let activeProblemKey = 'stripe';
let activeStudioPhase = 1;
let studioTimer = 45 * 60;
let studioInterval = null;
let isStudioRunning = false;
let currentCurveballIdx = 0;

// Sub-Tab Switcher
function switchStudioSubTab(tab) {
  if (typeof playClickTone === 'function') playClickTone(700, 0.02);
  const tabs = ['framework', 'calculator', 'curveballs', 'rubric', 'notes'];
  tabs.forEach(t => {
    const el = document.getElementById('subview-studio-' + t);
    const btn = document.getElementById('tab-studio-' + t);
    if (el) {
      if (t === tab) el.classList.remove('hidden');
      else el.classList.add('hidden');
    }
    if (btn) {
      if (t === tab) btn.className = 'studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-amber-500 text-slate-950 transition-all flex items-center gap-1.5 shadow-lg shadow-amber-500/10';
      else btn.className = 'studio-subtab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5';
    }
  });

  if (tab === 'calculator') recalcInterviewMath();
  if (tab === 'curveballs') renderCurveball();
  if (tab === 'rubric') updateRubricLevel();
  if (tab === 'notes') loadScratchpadNotes();
  if (typeof safeCreateIcons === 'function') safeCreateIcons();
}

// Switch Active Problem
function switchInterviewProblem(probKey) {
  activeProblemKey = probKey;
  const p = INTERVIEW_PROBLEMS[probKey];
  if (!p) return;

  const tTag = document.getElementById('interview-active-tag'); if (tTag) tTag.innerText = p.tag;
  const tTitle = document.getElementById('interview-problem-title'); if (tTitle) tTitle.innerText = p.title;
  const tTarget = document.getElementById('interview-problem-target'); if (tTarget) tTarget.innerHTML = p.target;

  // Sync Calculator defaults
  applyInterviewCalcPreset();

  // Render Phase Content
  renderInterviewPhaseContent();

  // Reset Scratchpad with problem-tailored template
  resetScratchpadTemplate();
}

// Jump To Phase
function jumpToPhase(phaseNum) {
  activeStudioPhase = phaseNum;
  if (typeof playClickTone === 'function') playClickTone(600, 0.02);

  // Update phase step card styling
  for (let i = 1; i <= 5; i++) {
    const c = document.getElementById('phase-card-' + i);
    if (c) {
      if (i === phaseNum) {
        c.className = 'phase-step-btn p-3 rounded-xl border bg-cyan-500/15 border-cyan-500/50 text-white font-bold cursor-pointer transition-all space-y-1 shadow-lg shadow-cyan-500/10';
      } else {
        c.className = 'phase-step-btn p-3 rounded-xl border bg-slate-950 border-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all space-y-1';
      }
    }
  }

  // Update active phase pill in top nav
  const pill = document.getElementById('studio-active-phase-pill');
  const phasePillTexts = {
    1: 'PHASE 1: SCOPE & BOUNDARIES (0-5m)',
    2: 'PHASE 2: CAPACITY & APIS (5-12m)',
    3: 'PHASE 3: HIGH-LEVEL ARCHITECTURE (12-25m)',
    4: 'PHASE 4: DEEP DIVE & BOTTLENECK SCALE (25-40m)',
    5: 'PHASE 5: STAFF+ TRADE-OFFS & DEFENSE (40-45m)'
  };
  if (pill) pill.innerText = phasePillTexts[phaseNum] || 'INTERVIEW IN PROGRESS';

  renderInterviewPhaseContent();
}

// Render Active Phase Content for Selected Problem
function renderInterviewPhaseContent() {
  const container = document.getElementById('interview-phase-dynamic-body');
  if (!container) return;

  const p = INTERVIEW_PROBLEMS[activeProblemKey];
  if (!p || !p.phases[activeStudioPhase]) return;

  const ph = p.phases[activeStudioPhase];

  let html = `
    <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-bold text-cyan-400 font-mono flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-cyan-400"></span> ${ph.title}
        </h4>
        <span class="text-[10px] font-mono text-slate-500">FAANG Staff Whiteboard Checkpoint</span>
      </div>

      <div class="space-y-2 text-xs text-slate-300">
        <div class="font-bold text-white text-[11px] uppercase tracking-wider text-slate-400">Key Deliverables &amp; Verbal Script:</div>
        <ul class="space-y-1.5 list-disc list-inside text-slate-300">
          ${ph.checklist.map(item => `<li>${item}</li>`).join('')}
        </ul>
      </div>
  `;

  if (ph.api) {
    html += `
      <div class="pt-2">
        <div class="font-bold text-white text-[11px] uppercase tracking-wider text-slate-400 mb-1">Production Interface Contract (REST / gRPC):</div>
        <pre class="p-3 rounded-xl bg-black border border-slate-800 font-mono text-xs text-emerald-300 overflow-x-auto">${ph.api}</pre>
      </div>
    `;
  }

  if (ph.topologyDesc) {
    html += `
      <div class="pt-2">
        <div class="font-bold text-white text-[11px] uppercase tracking-wider text-slate-400 mb-1">Architectural Data Flow Pipeline:</div>
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800/80 font-mono text-xs text-amber-300 leading-relaxed">
          ${ph.topologyDesc}
        </div>
      </div>
    `;
  }

  html += `</div>`;
  container.innerHTML = html;
}

// Timer Functions
function toggleStudioTimer() {
  const btn = document.getElementById('btn-studio-timer');
  if (isStudioRunning) {
    clearInterval(studioInterval);
    isStudioRunning = false;
    if (btn) btn.innerText = 'Resume';
  } else {
    isStudioRunning = true;
    if (btn) btn.innerText = 'Pause';
    studioInterval = setInterval(() => {
      if (studioTimer > 0) {
        studioTimer--;
        renderStudioTimer();

        // Auto-switch phase indicators based on elapsed time
        const elapsed = (45 * 60) - studioTimer;
        if (elapsed < 5 * 60 && activeStudioPhase !== 1) jumpToPhase(1);
        else if (elapsed >= 5 * 60 && elapsed < 12 * 60 && activeStudioPhase !== 2) jumpToPhase(2);
        else if (elapsed >= 12 * 60 && elapsed < 25 * 60 && activeStudioPhase !== 3) jumpToPhase(3);
        else if (elapsed >= 25 * 60 && elapsed < 40 * 60 && activeStudioPhase !== 4) jumpToPhase(4);
        else if (elapsed >= 40 * 60 && activeStudioPhase !== 5) jumpToPhase(5);

      } else {
        clearInterval(studioInterval);
        isStudioRunning = false;
        alert('Time is up! Conclude interview with trade-offs and operational metrics.');
      }
    }, 1000);
  }
}

function resetStudioTimer() {
  clearInterval(studioInterval);
  isStudioRunning = false;
  studioTimer = 45 * 60;
  renderStudioTimer();
  jumpToPhase(1);
  const btn = document.getElementById('btn-studio-timer');
  if (btn) btn.innerText = 'Start';
}

function renderStudioTimer() {
  const display = document.getElementById('studio-timer-display');
  if (!display) return;
  const mins = Math.floor(studioTimer / 60);
  const secs = studioTimer % 60;
  display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  if (mins < 5) {
    display.className = 'font-mono text-xl font-black text-rose-500 tracking-wider animate-pulse';
  } else {
    display.className = 'font-mono text-xl font-black text-emerald-400 tracking-wider';
  }
}

// Back-of-the-Envelope Math Engine
function applyInterviewCalcPreset() {
  const p = INTERVIEW_PROBLEMS[activeProblemKey];
  if (!p || !p.calcDefaults) return;
  const def = p.calcDefaults;

  const inDau = document.getElementById('calc-in-dau'); if (inDau) inDau.value = def.dau;
  const inAct = document.getElementById('calc-in-actions'); if (inAct) inAct.value = def.actions;
  const inRat = document.getElementById('calc-in-ratio'); if (inRat) inRat.value = def.ratio;
  const inPay = document.getElementById('calc-in-payload'); if (inPay) inPay.value = def.payload;
  const inPk = document.getElementById('calc-in-peak'); if (inPk) inPk.value = def.peak;

  recalcInterviewMath();
}

function recalcInterviewMath() {
  const eDau = document.getElementById('calc-in-dau');
  const eAct = document.getElementById('calc-in-actions');
  const eRat = document.getElementById('calc-in-ratio');
  const ePay = document.getElementById('calc-in-payload');
  const ePk = document.getElementById('calc-in-peak');

  if (!eDau || !eAct || !eRat || !ePay || !ePk) return;

  const dau = parseFloat(eDau.value);
  const actions = parseFloat(eAct.value);
  const ratio = parseFloat(eRat.value); // read to write ratio: e.g. 10 means 10 reads per 1 write
  const payloadKb = parseFloat(ePay.value);
  const peakMult = parseFloat(ePk.value);

  // Update slider labels
  const vDau = document.getElementById('calc-val-dau'); if (vDau) vDau.innerText = dau.toLocaleString();
  const vAct = document.getElementById('calc-val-actions'); if (vAct) vAct.innerText = actions;
  const readPct = Math.round((ratio / (ratio + 1)) * 100);
  const vRat = document.getElementById('calc-val-ratio'); if (vRat) vRat.innerText = `${ratio} : 1 (${readPct}% Reads)`;
  const vPay = document.getElementById('calc-val-payload'); if (vPay) vPay.innerText = `${payloadKb.toFixed(1)} KB`;
  const vPk = document.getElementById('calc-val-peak'); if (vPk) vPk.innerText = `${peakMult.toFixed(1)}x`;

  // Calculations
  const totalDailyEvents = dau * actions;
  const totalAvgQps = totalDailyEvents / 86400;

  const writeFraction = 1 / (ratio + 1);
  const readFraction = ratio / (ratio + 1);

  const avgWriteQps = Math.round(totalAvgQps * writeFraction);
  const peakWriteQps = Math.round(avgWriteQps * peakMult);

  const avgReadQps = Math.round(totalAvgQps * readFraction);
  const peakReadQps = Math.round(avgReadQps * peakMult);

  // Storage
  const dailyWriteBytes = (totalDailyEvents * writeFraction) * (payloadKb * 1024);
  const annualStorageTb = (dailyWriteBytes * 365) / 1e12;
  const fiveYearStorageTb = annualStorageTb * 5;

  // Cache RAM (Pareto 20% of daily read volume cached)
  const dailyReadBytes = (totalDailyEvents * readFraction) * (payloadKb * 1024);
  const cacheRamBytes = dailyReadBytes * 0.20;
  const cacheRamGb = cacheRamBytes / 1e9;
  const redisNodeCount = Math.max(2, Math.ceil(cacheRamGb / 50)); // 50 GB per node

  // Bandwidth
  const ingressBps = avgWriteQps * (payloadKb * 1024) * 8;
  const egressBps = avgReadQps * (payloadKb * 1024) * 8;

  // Update UI Elements
  const rWQ = document.getElementById('calc-res-write-qps'); if (rWQ) rWQ.innerText = `${avgWriteQps.toLocaleString()} req/s`;
  const rPW = document.getElementById('calc-res-peak-write'); if (rPW) rPW.innerText = `Peak: ${peakWriteQps.toLocaleString()} req/s`;

  const rRQ = document.getElementById('calc-res-read-qps'); if (rRQ) rRQ.innerText = `${avgReadQps.toLocaleString()} req/s`;
  const rPR = document.getElementById('calc-res-peak-read'); if (rPR) rPR.innerText = `Peak: ${peakReadQps.toLocaleString()} req/s`;

  const rS1 = document.getElementById('calc-res-storage-1yr'); if (rS1) rS1.innerText = `${annualStorageTb.toFixed(1)} TB / yr`;
  const rS5 = document.getElementById('calc-res-storage-5yr'); if (rS5) rS5.innerText = `5 Years: ${fiveYearStorageTb.toFixed(1)} TB (${(fiveYearStorageTb / 1000).toFixed(2)} PB)`;

  const rCR = document.getElementById('calc-res-cache-ram'); if (rCR) rCR.innerText = `${cacheRamGb.toFixed(1)} GB RAM`;
  const rRN = document.getElementById('calc-res-redis-nodes'); if (rRN) rRN.innerText = `${redisNodeCount}x r6g.xlarge nodes (80/20 RAM)`;

  const rNet = document.getElementById('calc-res-network');
  if (rNet) {
    const inGbps = (ingressBps / 1e9).toFixed(2);
    const egGbps = (egressBps / 1e9).toFixed(2);
    const inMBps = (ingressBps / 8 / 1e6).toFixed(1);
    const egMBps = (egressBps / 8 / 1e6).toFixed(1);
    rNet.innerHTML = `Ingress: ${inMBps} MB/s (${inGbps} Gbps) &bull; Egress: ${egMBps} MB/s (${egGbps} Gbps)`;
  }
}

function copyCalcSummaryToNotes() {
  const eDau = document.getElementById('calc-val-dau')?.innerText || '100M';
  const wQps = document.getElementById('calc-res-write-qps')?.innerText || '2,000 req/s';
  const rQps = document.getElementById('calc-res-read-qps')?.innerText || '20,000 req/s';
  const s5 = document.getElementById('calc-res-storage-5yr')?.innerText || '500 TB';
  const ram = document.getElementById('calc-res-cache-ram')?.innerText || '70 GB';

  const snippet = `\n### Capacity & Sizing Estimation\n- **Daily Active Users**: ${eDau}\n- **Write Throughput**: ${wQps}\n- **Read Throughput**: ${rQps}\n- **Cumulative 5-Year Storage**: ${s5}\n- **RAM Cache Pool (20% Pareto)**: ${ram}\n`;

  const area = document.getElementById('interview-scratchpad-input');
  if (area) {
    area.value += snippet;
    saveScratchpadNotes();
    alert('Capacity math appended to Candidate Scratchpad!');
  }
}

// Interviewer Curveball Simulator
function drawRandomCurveball() {
  currentCurveballIdx = (currentCurveballIdx + 1) % CURVEBALL_DATABASE.length;
  renderCurveball();
}

function renderCurveball() {
  const container = document.getElementById('curveball-card-container');
  if (!container) return;

  const cb = CURVEBALL_DATABASE[currentCurveballIdx];
  if (!cb) return;

  container.innerHTML = `
    <div class="p-5 rounded-xl bg-slate-900 border border-rose-500/30 space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40 uppercase">
          ${cb.category}
        </span>
        <span class="text-xs font-mono text-slate-500">Interviewer Grilling Scenario #${currentCurveballIdx + 1}</span>
      </div>

      <div class="text-sm font-mono font-bold text-white leading-relaxed">
        &ldquo;${cb.prompt}&rdquo;
      </div>

      <div class="p-3.5 rounded-xl bg-rose-950/20 border border-rose-500/20 text-xs font-mono text-rose-300">
        <div class="font-bold text-rose-400 mb-1 flex items-center gap-1.5">
          <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> Common Junior/Mid Interview Trap:
        </div>
        ${cb.juniorTrap}
      </div>

      <div class="pt-2">
        <button onclick="toggleCurveballAnswer()" id="btn-reveal-curveball" class="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/20 transition-all flex items-center gap-1.5">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i> Reveal Staff+ Gold Standard Defense
        </button>
      </div>

      <div id="curveball-answer-box" class="hidden p-4 rounded-xl bg-slate-950 border border-emerald-500/30 text-xs font-mono text-slate-200 space-y-2">
        <div class="font-bold text-emerald-400 flex items-center gap-1.5">
          <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Staff Architect Defense Strategy:
        </div>
        <p class="leading-relaxed text-slate-300">${cb.staffDefense}</p>
      </div>
    </div>
  `;

  if (typeof safeCreateIcons === 'function') safeCreateIcons();
}

function toggleCurveballAnswer() {
  const box = document.getElementById('curveball-answer-box');
  const btn = document.getElementById('btn-reveal-curveball');
  if (!box) return;
  if (box.classList.contains('hidden')) {
    box.classList.remove('hidden');
    if (btn) btn.innerText = 'Hide Defense Strategy';
  } else {
    box.classList.add('hidden');
    if (btn) btn.innerText = 'Reveal Staff+ Gold Standard Defense';
  }
}

// FAANG L6/L7 Rubric Level Predictor
function updateRubricLevel() {
  const in1 = parseInt(document.getElementById('rubric-in-1')?.value || 3);
  const in2 = parseInt(document.getElementById('rubric-in-2')?.value || 3);
  const in3 = parseInt(document.getElementById('rubric-in-3')?.value || 3);
  const in4 = parseInt(document.getElementById('rubric-in-4')?.value || 3);

  const scores = [in1, in2, in3, in4];
  const scoreLabels = ['Needs Work (1/4)', 'Basic Mid-Level (2/4)', 'Solid Senior (3/4)', 'Staff / Principal (4/4)'];

  for (let i = 1; i <= 4; i++) {
    const lbl = document.getElementById('rubric-lbl-' + i);
    if (lbl) lbl.innerText = `Score: ${scores[i-1]} / 4 (${scoreLabels[scores[i-1] - 1]})`;
  }

  const total = in1 + in2 + in3 + in4;
  const card = document.getElementById('rubric-level-card');
  const title = document.getElementById('rubric-level-title');
  const sText = document.getElementById('rubric-level-score');
  const crit = document.getElementById('rubric-level-critique');

  if (sText) sText.innerText = `Composite Score: ${total} / 16 (${Math.round((total/16)*100)}%)`;

  if (total >= 15) {
    if (title) title.innerText = 'L7 / PRINCIPAL ENGINEER';
    if (card) card.className = 'p-4 rounded-xl bg-purple-950/30 border border-purple-500/40 text-center space-y-2';
    if (crit) crit.innerHTML = '<p class="text-purple-300 font-bold">Unanimous Strong Hire (Top 1%):</p><p>Demonstrates deep first-principles mastery, cross-system trade-off articulation, hardware physics awareness, and effortless operational resilience scoping.</p>';
  } else if (total >= 12) {
    if (title) title.innerText = 'L6 / STAFF ARCHITECT';
    if (card) card.className = 'p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 text-center space-y-2';
    if (crit) crit.innerHTML = '<p class="text-emerald-300 font-bold">Strong Hire for Staff Level (L6):</p><p>Drives the interview autonomously, resolves concurrency race conditions cleanly, and models operational failure modes before being prompted.</p>';
  } else if (total >= 8) {
    if (title) title.innerText = 'L5 / SENIOR ENGINEER';
    if (card) card.className = 'p-4 rounded-xl bg-cyan-950/30 border border-cyan-500/40 text-center space-y-2';
    if (crit) crit.innerHTML = '<p class="text-cyan-300 font-bold">Hire for Senior SDE (L5):</p><p>Solid architectural happy-path understanding. To reach Staff+, delve deeper into distributed consensus failure modes, split-brain fencing, and RPO/RTO tradeoffs.</p>';
  } else {
    if (title) title.innerText = 'L4 / MID-LEVEL ENGINEER';
    if (card) card.className = 'p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 text-center space-y-2';
    if (crit) crit.innerHTML = '<p class="text-amber-300 font-bold">L4 Level Execution:</p><p>Needs significant reinforcement on distributed locking, capacity math, and database partitioning strategies.</p>';
  }
}

// Candidate Scratchpad & Notes
function loadScratchpadNotes() {
  const saved = localStorage.getItem('interview_scratchpad_' + activeProblemKey);
  const area = document.getElementById('interview-scratchpad-input');
  if (area) {
    if (saved) {
      area.value = saved;
    } else {
      resetScratchpadTemplate();
    }
    updateScratchpadCount();
  }
}

function saveScratchpadNotes() {
  const area = document.getElementById('interview-scratchpad-input');
  if (area) {
    localStorage.setItem('interview_scratchpad_' + activeProblemKey, area.value);
    updateScratchpadCount();
  }
}

function updateScratchpadCount() {
  const area = document.getElementById('interview-scratchpad-input');
  const countEl = document.getElementById('scratchpad-word-count');
  if (area && countEl) {
    const words = area.value.trim() ? area.value.trim().split(/\s+/).length : 0;
    countEl.innerText = `${words} words`;
  }
}

function resetScratchpadTemplate() {
  const p = INTERVIEW_PROBLEMS[activeProblemKey];
  const area = document.getElementById('interview-scratchpad-input');
  if (!area || !p) return;

  area.value = `# System Design Proposal: ${p.title}

## 1. Scope & Requirements
### Functional Requirements
- 1. ...
- 2. ...
- 3. ...

### Non-Functional Requirements
- High Availability: 99.999%
- Latency: P99 < 150ms
- Consistency: Strong consistency for ledgers / eventual consistency for analytics

---

## 2. Capacity Estimation
- DAU: 100M
- Write QPS: ~2,500 req/s (Peak: 7,500 req/s)
- Read QPS: ~25,000 req/s
- 5-Year Storage: ~500 TB

---

## 3. High-Level Architecture
\`\`\`
Client -> L4 Anycast -> L7 Envoy Gateway -> Microservice Fleet -> Distributed Cache / DB
\`\`\`

---

## 4. Deep Dive & Bottlenecks
- Concurrency & Idempotency: ...
- Partition Key Strategy: ...
- Disaster Recovery (RPO / RTO): ...
`;
  saveScratchpadNotes();
}

function copyScratchpadToClipboard() {
  const area = document.getElementById('interview-scratchpad-input');
  const btn = document.getElementById('btn-copy-scratchpad');
  if (!area) return;

  if (typeof fallbackCopy === 'function') {
    fallbackCopy(area.value);
  } else if (navigator.clipboard) {
    navigator.clipboard.writeText(area.value);
  }

  if (btn) {
    btn.innerText = 'Copied!';
    setTimeout(() => { btn.innerText = 'Copy Markdown'; }, 2000);
  }
}

// Initial Bootstrapping
try {
  switchInterviewProblem('stripe');
  jumpToPhase(1);
} catch(e) {}
"""
