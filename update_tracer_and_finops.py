# update_tracer_and_finops.py
# Elevates Packet Tracer and AWS FinOps to 100x God Level in data_interactive_tools.py
# and adds Instant Fuzzy Sidebar Search to build_cockpit_100x.py.

import os
import re

print("Starting 100x upgrade for Packet Tracer, FinOps, and Sidebar Search...")

# =========================================================================
# 1. NEW 100X PACKET TRACER HTML
# =========================================================================
NEW_TRACER_HTML = '''
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
'''

# =========================================================================
# 2. NEW 100X AWS FINOPS CALCULATOR HTML
# =========================================================================
NEW_FINOPS_HTML = '''
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
'''

# =========================================================================
# 3. NEW JAVASCRIPT ENGINES FOR PACKET TRACER & FINOPS
# =========================================================================
NEW_TRACER_AND_FINOPS_JS = '''
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
        headers: `GET /api/v1/products/4921 HTTP/3\\nHost: api.nexus.io\\nUser-Agent: NexusClient/2.4 (iOS 18.1)\\nAccept: application/json\\n0-RTT: 1`
      },
      {
        node: "cdn",
        x: 252, y: 76,
        desc: "Cloudflare Edge PoP receives request, checks WAF, finds hot key in RAM -> CACHE HIT (Age: 42s)!",
        protocol: "TLS 1.3 / RAM Cache",
        latencyHop: "+7.2 ms",
        headers: `HTTP/3 200 OK\\nCF-Cache-Status: HIT\\nAge: 42\\nContent-Type: application/json\\nContent-Encoding: br\\nServer: cloudflare`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Edge streams compressed Brotli JSON payload back to client. Origin servers are 100% bypassed!",
        protocol: "HTTP/3 200 OK",
        latencyHop: "+1.0 ms",
        headers: `Response Payload: { "product_id": 4921, "title": "Ultra Cluster X", "price": 499.00 }\\nTotal SLA Latency: 8.2 ms`
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
        headers: `POST /v1/orders HTTP/3\\nHost: api.nexus.io\\nAuthorization: Bearer eyJhbGciOi...\\nIdempotency-Key: idem_94812a\\nContent-Type: application/json`
      },
      {
        node: "cdn",
        x: 252, y: 76,
        desc: "Cloudflare Edge terminates TLS 1.3, verifies WAF DDoS rules, and proxies to origin backbone.",
        protocol: "Edge TLS Termination",
        latencyHop: "+6.8 ms",
        headers: `TCP Connection Re-used (Keep-Alive)\\nOrigin Backbone Route: US-East-1\\nX-Forwarded-For: 203.0.113.195`
      },
      {
        node: "l4",
        x: 427, y: 76,
        desc: "L4 Maglev LB hashes 5-tuple and forwards raw TCP frame to Envoy Gateway via Direct Server Return.",
        protocol: "IPVS / DSR (Kernel Bypass)",
        latencyHop: "+0.01 ms",
        headers: `Ethernet Frame: DSR Encapsulation\\nTarget MAC: Envoy-Node-04\\nSource IP Preserved: 203.0.113.195`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy API Gateway validates JWT, checks Token Bucket rate limit (84/100 tokens left), and routes to App pod.",
        protocol: "mTLS 1.3 X.509",
        latencyHop: "+1.2 ms",
        headers: `JWT Claims Verified: user_id=94821\\nRateLimit: OK (remaining=84)\\nUpstream Cluster: order-service.prod`
      },
      {
        node: "app",
        x: 597, y: 246,
        desc: "Order Service acquires distributed lock in Redis Cluster (Redlock) to ensure exactly-once execution.",
        protocol: "RESP3 Redis Lock",
        latencyHop: "+0.9 ms",
        headers: `SET lock:order:idem_94812a "token_uuid" NX PX 5000\\nRedis Status: +OK (Lock Acquired)`
      },
      {
        node: "db",
        x: 252, y: 246,
        desc: "Spanner executes 2PC transaction: Paxos consensus across 3 AZs with TrueTime (eps <= 4ms). Commit persisted!",
        protocol: "Paxos Consensus / 2PC",
        latencyHop: "+28.4 ms",
        headers: `BEGIN TRANSACTION\\nINSERT INTO orders (id, user_id, amount) VALUES ('ord_710', 94821, 149.00);\\nCOMMIT (TrueTime CommitTimestamp=1774892184912)`
      },
      {
        node: "kafka",
        x: 82, y: 246,
        desc: "Debezium CDC streams order_created event to Kafka KRaft; ClickHouse updates real-time analytics.",
        protocol: "Kafka KRaft / CDC",
        latencyHop: "+3.2 ms",
        headers: `Kafka Produce ACK (topic=order-events, partition=4, offset=891042)\\nClickHouse Consumer: Ingested Batch`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Envoy relays HTTP 201 Created back to client with order receipt. Total latency: 42.1 ms.",
        protocol: "HTTP/3 201 Created",
        latencyHop: "+1.6 ms",
        headers: `HTTP/3 201 Created\\nContent-Type: application/json\\nPayload: { "order_id": "ord_710", "status": "CONFIRMED" }`
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
        headers: `GET /v1/trends/tech HTTP/3\\nConcurrent Conns: 1,000\\nCache TTL on CDN: Expired (0s remaining)`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy routes the 1,000 concurrent requests into the Go Order/Feed service pods.",
        protocol: "Envoy Forwarding",
        latencyHop: "+3.2 ms",
        headers: `Active HTTP/2 Streams: 1,000\\nUpstream: feed-service`
      },
      {
        node: "cache",
        x: 427, y: 246,
        desc: "App checks Redis Cluster -> CACHE MISS! 1,000 threads simultaneously need fresh data.",
        protocol: "Redis GET (MISS)",
        latencyHop: "+0.8 ms",
        headers: `GET trend:tech\\nRedis Response: (nil) [Key Expired]`
      },
      {
        node: "app",
        x: 597, y: 246,
        desc: "Go singleflight.Group activates! Mutex barrier locks out 999 requests; exactly ONE thread queries the DB.",
        protocol: "Go singleflight.Group",
        latencyHop: "+0.2 ms",
        headers: `group.Do("trend:tech", fetchFn)\\nThread 1: Executing fetchFn()\\nThreads 2..1000: Suspended on sync.WaitGroup`
      },
      {
        node: "db",
        x: 252, y: 246,
        desc: "Database handles ONE single query instead of melting down under 1,000 concurrent queries!",
        protocol: "Spanner Single Read",
        latencyHop: "+11.8 ms",
        headers: `SELECT * FROM trends WHERE topic = 'tech'\\nReturned 1 row in 11.8 ms. Database load: 1 QPS (meltdown prevented!)`
      },
      {
        node: "cache",
        x: 427, y: 246,
        desc: "Single thread repopulates Redis with fresh 5-minute TTL and probabilistic early expiration (XFetch).",
        protocol: "Redis SETEX",
        latencyHop: "+0.9 ms",
        headers: `SETEX trend:tech 300 "{...}"\\nStatus: +OK`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "SingleFlight broadcasts result to all 999 waiting callers; all 1,000 clients receive HTTP 200 OK!",
        protocol: "HTTP/3 200 OK",
        latencyHop: "+1.5 ms",
        headers: `HTTP/3 200 OK (Served to 1,000 callers)\\nTotal Latency: 18.4 ms (DB Saved!)`
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
        headers: `POST /v1/checkout/external-payment HTTP/3\\nHost: api.nexus.io`
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
        headers: `HTTP 504 Gateway Timeout\\nDownstream Partner Unresponsive`
      },
      {
        node: "l7",
        x: 597, y: 76,
        desc: "Envoy Outlier Detection observes >50% failure rate: Circuit Breaker trips from CLOSED -> OPEN!",
        protocol: "Circuit Breaker OPEN",
        latencyHop: "+0.1 ms",
        headers: `Circuit Breaker: STATE_OPEN\\nConsecutive 5xx Count: 5 / 5\\nAll downstream calls short-circuited!`
      },
      {
        node: "client",
        x: 82, y: 76,
        desc: "Gateway intercepts request instantly, returning degraded async fallback in 1.2ms without consuming worker threads!",
        protocol: "HTTP 200 (Degraded)",
        latencyHop: "+0.1 ms",
        headers: `HTTP/3 200 OK\\nPayload: { "status": "QUEUED_ASYNC_RETRY", "fallback": true }\\nSLA: 1.2 ms (No origin thread starvation!)`
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
'''

# Read data_interactive_tools.py
with open('data_interactive_tools.py', 'r', encoding='utf-8') as f:
    dit_content = f.read()

# Replace TRACER_HTML
pattern_tracer = r'TRACER_HTML\s*=\s*""".*?"""'
dit_content = re.sub(pattern_tracer, f'TRACER_HTML = """{NEW_TRACER_HTML}"""', dit_content, flags=re.DOTALL)
print("Updated TRACER_HTML in data_interactive_tools.py.")

# Replace FINOPS_HTML
pattern_finops = r'FINOPS_HTML\s*=\s*""".*?"""'
dit_content = re.sub(pattern_finops, f'FINOPS_HTML = """{NEW_FINOPS_HTML}"""', dit_content, flags=re.DOTALL)
print("Updated FINOPS_HTML in data_interactive_tools.py.")

# Replace tracer & finops JS inside TOOLS_JS
# It spans from `const nodeTelemetry = {` to right before `/* === GOD-LEVEL DISTRIBUTED SERVER DISTRIBUTION`
pattern_js = r'const nodeTelemetry\s*=\s*\{.*?/\* =========================================================================\s*GOD-LEVEL DISTRIBUTED SERVER DISTRIBUTION'
replacement_js = f"{NEW_TRACER_AND_FINOPS_JS}\n\n/* =========================================================================\n   GOD-LEVEL DISTRIBUTED SERVER DISTRIBUTION"

match = re.search(pattern_js, dit_content, flags=re.DOTALL)
if match:
    dit_content = dit_content[:match.start()] + replacement_js + dit_content[match.end():]
    print("Replaced tracer & finops JS inside TOOLS_JS successfully!")
else:
    print("WARNING: Could not find regex match for TOOLS_JS tracer & finops block!")

with open('data_interactive_tools.py', 'w', encoding='utf-8') as f:
    f.write(dit_content)

print(f"data_interactive_tools.py written cleanly. Size: {len(dit_content)} bytes.")

# =========================================================================
# 4. UPDATE build_cockpit_100x.py WITH SIDEBAR SEARCH & SHORTCUT
# =========================================================================
with open('build_cockpit_100x.py', 'r', encoding='utf-8') as f:
    cockpit_content = f.read()

# Add Sidebar Search HTML into #cockpit-sidebar
old_sidebar_header = '''      <div class="p-3 border-b border-white/[0.06] flex items-center justify-between text-[11px] font-mono font-bold text-slate-400">
        <span>CURRICULUM DIRECTORY</span>
        <span id="sidebar-count" class="text-emerald-400">{len(topics)} Modules</span>
      </div>

      <!-- Items List -->'''

new_sidebar_header = '''      <div class="p-3 border-b border-white/[0.06] flex items-center justify-between text-[11px] font-mono font-bold text-slate-400">
        <span>CURRICULUM DIRECTORY</span>
        <span id="sidebar-count" class="text-emerald-400">{len(topics)} Modules</span>
      </div>

      <!-- Instant Real-time Search Box -->
      <div class="p-2 border-b border-white/[0.06] bg-slate-950/70">
        <div class="relative flex items-center">
          <i data-lucide="search" class="w-3.5 h-3.5 text-slate-500 absolute left-2.5 pointer-events-none"></i>
          <input id="sidebar-search-input" type="text" placeholder="Search 27 modules (e.g. Spanner, Raft)..." 
            oninput="filterSidebarBySearch(this.value)"
            class="w-full bg-slate-900/90 text-xs font-mono text-slate-200 placeholder-slate-500 pl-8 pr-7 py-1.5 rounded-lg border border-white/[0.08] focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/30 transition-all">
          <button id="sidebar-search-clear" onclick="clearSidebarSearch()" class="hidden absolute right-2 text-slate-400 hover:text-white" title="Clear Search">
            <i data-lucide="x" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>

      <!-- Items List -->'''

if old_sidebar_header in cockpit_content:
    cockpit_content = cockpit_content.replace(old_sidebar_header, new_sidebar_header)
    print("Added Instant Search Box to cockpit sidebar HTML.")
else:
    print("WARNING: Could not find old_sidebar_header in build_cockpit_100x.py!")

# Update renderSidebar() and add search helper functions in build_cockpit_100x.py
old_render_sidebar = '''    // Render Left Sidebar List
    function renderSidebar() {
      const container = document.getElementById('sidebar-items-list');
      if (!container) return;
      
      const filtered = TOPICS.filter(it => {
        if (activeFilter === 'all') return true;
        if (activeFilter === 'blueprints') return it.type === 'blueprint';
        return it.stageId === activeFilter;
      });

      container.innerHTML = filtered.map((it, idx) => {
        const isMastered = masteredIds.includes(it.id);
        const isActive = TOPICS[currentIndex] && TOPICS[currentIndex].id === it.id;
        const activeClass = isActive 
          ? 'bg-emerald-500/15 border-emerald-500/50 text-white font-bold' 
          : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-white hover:bg-slate-900';
        return `
          <div onclick="selectItemById('${it.id}')" class="p-2.5 rounded-xl border ${activeClass} cursor-pointer transition-all flex items-center justify-between gap-2 text-xs">
            <div class="flex items-center gap-2 truncate">
              <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-400 animate-pulse' : (isMastered ? 'bg-emerald-500' : 'bg-slate-700')}"></span>
              <span class="truncate">${it.title}</span>
            </div>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-500 shrink-0">${it.stageNum}</span>
          </div>
        `;
      }).join('');

      const countEl = document.getElementById('sidebar-count');
      if (countEl) countEl.innerText = `${filtered.length} Modules`;
    }'''

new_render_sidebar = '''    let sidebarSearchQuery = '';

    function filterSidebarBySearch(q) {
      sidebarSearchQuery = (q || '').trim().toLowerCase();
      const clearBtn = document.getElementById('sidebar-search-clear');
      if (clearBtn) {
        if (sidebarSearchQuery.length > 0) {
          clearBtn.classList.remove('hidden');
        } else {
          clearBtn.classList.add('hidden');
        }
      }
      renderSidebar();
    }

    function clearSidebarSearch() {
      const input = document.getElementById('sidebar-search-input');
      if (input) input.value = '';
      sidebarSearchQuery = '';
      const clearBtn = document.getElementById('sidebar-search-clear');
      if (clearBtn) clearBtn.classList.add('hidden');
      renderSidebar();
      if (input) input.focus();
    }

    // Render Left Sidebar List
    function renderSidebar() {
      const container = document.getElementById('sidebar-items-list');
      if (!container) return;
      
      const filtered = TOPICS.filter(it => {
        let matchesStage = true;
        if (activeFilter === 'all') matchesStage = true;
        else if (activeFilter === 'blueprints') matchesStage = (it.type === 'blueprint');
        else matchesStage = (it.stageId === activeFilter);

        if (!matchesStage) return false;

        if (!sidebarSearchQuery) return true;

        const q = sidebarSearchQuery;
        const inTitle = (it.title || '').toLowerCase().includes(q);
        const inSummary = (it.summary || '').toLowerCase().includes(q);
        const inStage = (it.stageNum || '').toLowerCase().includes(q);
        const inId = (it.id || '').toLowerCase().includes(q);
        const inType = (it.type || '').toLowerCase().includes(q);
        return inTitle || inSummary || inStage || inId || inType;
      });

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="p-6 text-center text-slate-500 text-xs font-mono space-y-2">
            <i data-lucide="search-x" class="w-8 h-8 text-slate-600 mx-auto stroke-1"></i>
            <div>No modules matching "<span class="text-white">${sidebarSearchQuery}</span>"</div>
            <button onclick="clearSidebarSearch()" class="px-3 py-1.5 rounded-lg bg-slate-900 text-cyan-400 hover:text-cyan-300 text-[11px] font-bold border border-slate-800 transition-all cursor-pointer">Clear Search</button>
          </div>
        `;
        safeCreateIcons();
        const countEl = document.getElementById('sidebar-count');
        if (countEl) countEl.innerText = `0 Matches`;
        return;
      }

      container.innerHTML = filtered.map((it, idx) => {
        const isMastered = masteredIds.includes(it.id);
        const isActive = TOPICS[currentIndex] && TOPICS[currentIndex].id === it.id;
        const activeClass = isActive 
          ? 'bg-emerald-500/15 border-emerald-500/50 text-white font-bold' 
          : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-white hover:bg-slate-900';
        return `
          <div onclick="selectItemById('${it.id}')" class="p-2.5 rounded-xl border ${activeClass} cursor-pointer transition-all flex items-center justify-between gap-2 text-xs">
            <div class="flex items-center gap-2 truncate">
              <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-400 animate-pulse' : (isMastered ? 'bg-emerald-500' : 'bg-slate-700')}"></span>
              <span class="truncate">${it.title}</span>
            </div>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-500 shrink-0">${it.stageNum}</span>
          </div>
        `;
      }).join('');

      const countEl = document.getElementById('sidebar-count');
      if (countEl) {
        if (sidebarSearchQuery) {
          countEl.innerText = `${filtered.length} / ${TOPICS.length} Matches`;
        } else {
          countEl.innerText = `${filtered.length} Modules`;
        }
      }
    }'''

if old_render_sidebar in cockpit_content:
    cockpit_content = cockpit_content.replace(old_render_sidebar, new_render_sidebar)
    print("Updated renderSidebar() with fuzzy search in build_cockpit_100x.py.")
else:
    print("WARNING: Could not find old_render_sidebar in build_cockpit_100x.py!")

# Add shortcut / to focus search
old_keydown = "if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;"
new_keydown = """// Focus search shortcut / or Ctrl+K
      if ((e.key === '/' || ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K'))) && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (!isSidebarOpen) toggleSidebar();
        const searchInput = document.getElementById('sidebar-search-input');
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
        return;
      }

      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if (e.key === 'Escape') {
          e.target.blur();
        }
        return;
      }"""

if old_keydown in cockpit_content:
    cockpit_content = cockpit_content.replace(old_keydown, new_keydown, 1)
    print("Added / and Ctrl+K search shortcuts to build_cockpit_100x.py.")
else:
    print("WARNING: Could not find old_keydown in build_cockpit_100x.py!")

with open('build_cockpit_100x.py', 'w', encoding='utf-8') as f:
    f.write(cockpit_content)

print(f"build_cockpit_100x.py written cleanly. Size: {len(cockpit_content)} bytes.")
print("All updates applied!")
