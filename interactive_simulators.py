# interactive_simulators.py
# HTML and JS logic for the 5 God-Level Simulators

SIMULATORS_HTML = """
<!-- SIMULATOR TABS & WORKBENCH -->
<div id="sandbox-section" class="mt-12 space-y-8">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
    <div>
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">INTERACTIVE LAB</span>
        <h3 class="text-2xl font-bold text-white tracking-tight">System Design Engineering Workbench</h3>
      </div>
      <p class="text-sm text-slate-400 mt-1">Live distributed systems calculators, visual hash rings, and algorithm testbenches.</p>
    </div>
    
    <!-- Tab Controls -->
    <div class="flex items-center gap-1.5 p-1 bg-slate-900/90 rounded-xl border border-slate-800 overflow-x-auto max-w-full">
      <button onclick="switchTab('tab-capacity')" id="btn-tab-capacity" class="tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all bg-emerald-500 text-slate-950 font-bold shadow-lg shadow-emerald-500/20">
        Capacity Estimator
      </button>
      <button onclick="switchTab('tab-latency')" id="btn-tab-latency" class="tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
        Latency Machine
      </button>
      <button onclick="switchTab('tab-hashing')" id="btn-tab-hashing" class="tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
        Consistent Hash Ring
      </button>
      <button onclick="switchTab('tab-ratelimit')" id="btn-tab-ratelimit" class="tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
        Rate Limiter Lab
      </button>
      <button onclick="switchTab('tab-interview')" id="btn-tab-interview" class="tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
        Interview Framework
      </button>
    </div>
  </div>

  <!-- TAB 1: CAPACITY ESTIMATOR -->
  <div id="tab-capacity" class="tab-content block">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Input Controls (5 Cols) -->
      <div class="lg:col-span-5 bg-slate-900/70 border border-slate-800 rounded-2xl p-5 space-y-5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">Parameters &amp; Presets</span>
          <select id="capacity-presets" onchange="applyPreset(this.value)" class="bg-slate-950 text-slate-300 text-xs px-2.5 py-1 rounded-lg border border-slate-700 outline-none">
            <option value="custom">-- Custom System --</option>
            <option value="twitter">Twitter / X (500M DAU)</option>
            <option value="whatsapp">WhatsApp (2B DAU)</option>
            <option value="tinyurl">TinyURL (100M URLs/mo)</option>
            <option value="netflix">Netflix (250M Users)</option>
          </select>
        </div>

        <!-- Slider: DAU -->
        <div class="space-y-1.5">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Daily Active Users (DAU)</span>
            <span id="lbl-dau" class="font-mono text-emerald-400 font-bold">50,000,000</span>
          </div>
          <input type="range" id="input-dau" min="100000" max="1000000000" step="500000" value="50000000" oninput="calculateCapacity()" class="w-full accent-emerald-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <!-- Slider: Actions per user per day -->
        <div class="space-y-1.5">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Requests / User / Day</span>
            <span id="lbl-requests-per-day" class="font-mono text-cyan-400 font-bold">20</span>
          </div>
          <input type="range" id="input-requests-per-day" min="1" max="200" step="1" value="20" oninput="calculateCapacity()" class="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <!-- Slider: Read/Write Ratio -->
        <div class="space-y-1.5">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Read : Write Ratio</span>
            <span id="lbl-ratio" class="font-mono text-indigo-400 font-bold">10 : 1 (91% Reads)</span>
          </div>
          <input type="range" id="input-ratio" min="1" max="100" step="1" value="10" oninput="calculateCapacity()" class="w-full accent-indigo-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <!-- Slider: Payload Size (KB) -->
        <div class="space-y-1.5">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Avg Request Payload</span>
            <span id="lbl-payload" class="font-mono text-amber-400 font-bold">2.0 KB</span>
          </div>
          <input type="range" id="input-payload" min="0.1" max="50" step="0.1" value="2.0" oninput="calculateCapacity()" class="w-full accent-amber-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>

        <!-- Slider: Data Retention -->
        <div class="space-y-1.5">
          <div class="flex justify-between text-xs">
            <span class="text-slate-300 font-medium">Data Retention Period</span>
            <span id="lbl-retention" class="font-mono text-fuchsia-400 font-bold">365 Days (1 Year)</span>
          </div>
          <input type="range" id="input-retention" min="30" max="3650" step="30" value="365" oninput="calculateCapacity()" class="w-full accent-fuchsia-400 bg-slate-800 rounded-lg cursor-pointer">
        </div>
      </div>

      <!-- Live Results Deck (7 Cols) -->
      <div class="lg:col-span-7 space-y-4">
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <!-- Avg QPS -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-medium">Avg Read QPS</div>
            <div id="res-read-qps" class="text-xl font-mono font-bold text-cyan-400 mt-1">10,500</div>
            <div class="text-[10px] text-slate-500 mt-1">Total: <span id="res-total-qps" class="text-slate-300">11,574</span> QPS</div>
          </div>

          <!-- Peak QPS -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-medium">Peak QPS (2.5&times;)</div>
            <div id="res-peak-qps" class="text-xl font-mono font-bold text-amber-400 mt-1">28,935</div>
            <div class="text-[10px] text-slate-500 mt-1">Headroom for spikes</div>
          </div>

          <!-- Write QPS -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-medium">Avg Write QPS</div>
            <div id="res-write-qps" class="text-xl font-mono font-bold text-rose-400 mt-1">1,050</div>
            <div class="text-[10px] text-slate-500 mt-1">Disk append throughput</div>
          </div>

          <!-- Storage / Day -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-medium">Daily Storage Ingest</div>
            <div id="res-storage-day" class="text-xl font-mono font-bold text-indigo-400 mt-1">181 GB</div>
            <div class="text-[10px] text-slate-500 mt-1">Raw uncompressed</div>
          </div>

          <!-- Total Retention Storage -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-medium">Storage Required</div>
            <div id="res-storage-retention" class="text-xl font-mono font-bold text-fuchsia-400 mt-1">66.2 TB</div>
            <div class="text-[10px] text-slate-500 mt-1">For entire retention period</div>
          </div>

          <!-- 80/20 Cache RAM -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-emerald-800/40 bg-emerald-950/10">
            <div class="text-[11px] text-emerald-400 font-medium">80/20 Cache RAM</div>
            <div id="res-cache-ram" class="text-xl font-mono font-bold text-emerald-400 mt-1">36.2 GB</div>
            <div class="text-[10px] text-slate-400 mt-1">20% daily working set</div>
          </div>
        </div>

        <!-- Bandwidth & Sizing Summary Card -->
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <span class="text-xs font-mono font-bold text-white">Network Bandwidth Ingress / Egress</span>
            <span id="res-bandwidth" class="text-xs font-mono text-emerald-400 font-bold">185.2 Mbps / 1.85 Gbps</span>
          </div>
          <div class="text-xs text-slate-300 leading-relaxed">
            <strong class="text-white">Recommended Architecture Tier:</strong>
            <span id="res-architecture-rec" class="text-cyan-400 font-semibold">Horizontally sharded application tier behind L7 load balancer with Redis cluster (3x nodes) and read-replica database pool.</span>
          </div>
          <div class="p-3 rounded-lg bg-slate-950 font-mono text-[11px] text-slate-400 space-y-1">
            <div>&bull; Math: <code class="text-slate-300">Daily Writes = DAU &times; (Reqs/Day) / (Ratio + 1)</code></div>
            <div>&bull; Math: <code class="text-slate-300">Write QPS = Daily Writes / 86,400 s</code></div>
            <div>&bull; Math: <code class="text-slate-300">Hot Cache RAM = Daily Storage Ingest &times; 0.20 (Pareto)</code></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 2: LATENCY MACHINE -->
  <div id="tab-latency" class="tab-content hidden">
    <div class="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h4 class="text-lg font-bold text-white">Latency Numbers Every Programmer Must Internalize</h4>
          <p class="text-xs text-slate-400">Jeff Dean's famous distributed latency figures, visualized in computer time vs human time.</p>
        </div>
        <div class="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-800">
          <button id="btn-scale-raw" onclick="toggleLatencyScale('raw')" class="px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 text-slate-950">Nanoseconds (Raw)</button>
          <button id="btn-scale-human" onclick="toggleLatencyScale('human')" class="px-3 py-1 rounded-lg text-xs font-mono text-slate-400 hover:text-white">Human Scale (1 cycle = 1 sec)</button>
        </div>
      </div>

      <!-- Latency Timeline Items -->
      <div id="latency-items-container" class="space-y-3 font-mono text-xs">
        <!-- Javascript populates this dynamically -->
      </div>

      <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed">
        <strong class="text-amber-400">The Staff Engineer Insight:</strong> Notice that reading sequentially from memory takes 100ns (1.7 human minutes), while fetching over a WAN cross-Atlantic link takes 150,000,000ns (4.8 human years). In a single network round-trip to London, your CPU could have executed <strong>150,000,000 instructions</strong>! This is why batching, pipelining, and geo-local caching dominate distributed systems architecture.
      </div>
    </div>
  </div>

  <!-- TAB 3: CONSISTENT HASH RING SIMULATOR -->
  <div id="tab-hashing" class="tab-content hidden">
    <div class="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h4 class="text-lg font-bold text-white">Interactive Consistent Hashing Ring</h4>
          <p class="text-xs text-slate-400">Add/remove nodes and virtual nodes, insert keys, and observe that only $K/N$ keys move on topology change.</p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="addHashNode()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950">+ Add Node</button>
          <button onclick="removeHashNode()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-500 hover:bg-rose-400 text-slate-950">- Remove Node</button>
          <button onclick="insertSampleKeys()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-white border border-slate-700">Add 20 Keys</button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <!-- SVG Canvas for the Hash Ring -->
        <div class="lg:col-span-7 flex justify-center">
          <svg id="hash-ring-svg" viewBox="0 0 400 400" class="w-full max-w-[380px] h-auto bg-slate-950 rounded-2xl border border-slate-800 p-2"></svg>
        </div>

        <!-- Node Distribution Table & Controls -->
        <div class="lg:col-span-5 space-y-4">
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="text-slate-300 font-medium">Virtual Nodes (vnodes per server)</span>
              <span id="lbl-vnodes" class="font-mono text-emerald-400 font-bold">3 vnodes</span>
            </div>
            <input type="range" id="input-vnodes" min="1" max="15" step="1" value="3" oninput="updateVNodes(this.value)" class="w-full accent-emerald-400 bg-slate-800 rounded-lg cursor-pointer">
            <div class="text-[10px] text-slate-500">Higher vnodes guarantee uniform key distribution and eliminate hot partitions.</div>
          </div>

          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
            <div class="text-xs font-mono font-bold text-white flex justify-between">
              <span>ACTIVE SERVERS</span>
              <span id="lbl-total-keys" class="text-cyan-400">0 Keys Placed</span>
            </div>
            <div id="hash-nodes-list" class="space-y-2 text-xs font-mono max-h-48 overflow-y-auto pr-1">
              <!-- Dynamically populated -->
            </div>
          </div>

          <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-300">
            <strong>Key Rehash Invariant:</strong> When Server C crashes, only the keys belonging to Server C's sector shift to the next clockwise server. All other servers maintain 100% cache continuity!
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 4: RATE LIMITER LAB -->
  <div id="tab-ratelimit" class="tab-content hidden">
    <div class="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h4 class="text-lg font-bold text-white">Rate Limiting Algorithm Simulator</h4>
          <p class="text-xs text-slate-400">Simulate Token Bucket vs Leaky Bucket vs Sliding Window Counter with live traffic bursts.</p>
        </div>
        <div class="flex items-center gap-2">
          <select id="rl-algo-select" onchange="changeRateLimiterAlgo(this.value)" class="bg-slate-950 text-slate-200 text-xs px-3 py-1.5 rounded-lg border border-slate-700 outline-none">
            <option value="token-bucket">Token Bucket (Amazon / Stripe Standard)</option>
            <option value="leaky-bucket">Leaky Bucket (Constant Outflow Traffic Shaping)</option>
            <option value="sliding-window">Sliding Window Counter (Smooth Edge Boundary)</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Controls & Gauge (5 Cols) -->
        <div class="lg:col-span-5 space-y-4">
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
            <div class="flex justify-between items-center text-xs">
              <span class="text-slate-400">Bucket Capacity</span>
              <span class="font-mono text-white font-bold">10 Tokens</span>
            </div>
            <div class="flex justify-between items-center text-xs">
              <span class="text-slate-400">Refill Rate</span>
              <span class="font-mono text-white font-bold">2 Tokens / Second</span>
            </div>

            <!-- Visual Meter -->
            <div class="space-y-1 pt-2">
              <div class="flex justify-between text-xs font-mono">
                <span class="text-slate-400">Available Capacity:</span>
                <span id="rl-meter-text" class="text-emerald-400 font-bold">10 / 10</span>
              </div>
              <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700">
                <div id="rl-meter-bar" class="h-full bg-emerald-500 rounded-full transition-all duration-200" style="width: 100%;"></div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <button onclick="sendRateLimitRequest(1)" class="p-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs transition-all">Send 1 Request</button>
            <button onclick="sendRateLimitRequest(5)" class="p-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-xs transition-all">Send 5 Burst</button>
            <button onclick="simulateTrafficAttack()" class="p-2.5 rounded-xl bg-rose-500 hover:bg-rose-400 text-white font-bold text-xs col-span-2 transition-all">Simulate 25 Requests Burst</button>
          </div>
        </div>

        <!-- Terminal Traffic Logs (7 Cols) -->
        <div class="lg:col-span-7 bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs flex flex-col h-64">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800 text-slate-500 text-[11px]">
            <span>TRAFFIC LOGS &amp; HTTP STATUS</span>
            <button onclick="clearRateLimitLogs()" class="hover:text-slate-300">Clear</button>
          </div>
          <div id="rl-log-terminal" class="flex-1 overflow-y-auto space-y-1.5 pt-2 text-[11px]">
            <div class="text-slate-500">[System Ready] Bucket initialized with 10 tokens. Refill rate = 2/sec.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 5: INTERVIEW FRAMEWORK -->
  <div id="tab-interview" class="tab-content hidden">
    <div class="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h4 class="text-lg font-bold text-white">The 45-Minute Staff+ Interview Framework</h4>
          <p class="text-xs text-slate-400">The battle-tested 4-step framework used at Google, Meta, Amazon, and Netflix.</p>
        </div>
        <div class="flex items-center gap-3">
          <div id="interview-timer-display" class="font-mono text-xl font-bold text-emerald-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">45:00</div>
          <button onclick="toggleInterviewTimer()" id="btn-timer-toggle" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500 text-slate-950">Start Timer</button>
          <button onclick="resetInterviewTimer()" class="px-2.5 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white border border-slate-700">Reset</button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Step 1 -->
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-mono text-cyan-400">
            <span class="font-bold">STEP 1 (00-05m)</span>
            <span>5 Mins</span>
          </div>
          <h5 class="text-sm font-bold text-white">Requirements &amp; Scope</h5>
          <ul class="text-[11px] text-slate-400 space-y-1 list-disc list-inside">
            <li>Clarify 3-4 core functional features.</li>
            <li>Define non-functional SLAs: P99 latency, 99.99% availability, CAP trade-off.</li>
            <li>Establish out-of-scope boundaries to avoid rabbit holes.</li>
          </ul>
        </div>

        <!-- Step 2 -->
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-mono text-emerald-400">
            <span class="font-bold">STEP 2 (05-12m)</span>
            <span>7 Mins</span>
          </div>
          <h5 class="text-sm font-bold text-white">Capacity &amp; API Contracts</h5>
          <ul class="text-[11px] text-slate-400 space-y-1 list-disc list-inside">
            <li>Estimate DAU, Read/Write QPS, and Peak factor.</li>
            <li>Calculate 5-year storage &amp; 80/20 cache memory.</li>
            <li>Draft clean REST / gRPC API endpoints with idempotency keys.</li>
          </ul>
        </div>

        <!-- Step 3 -->
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-mono text-indigo-400">
            <span class="font-bold">STEP 3 (12-28m)</span>
            <span>16 Mins</span>
          </div>
          <h5 class="text-sm font-bold text-white">High-Level Architecture</h5>
          <ul class="text-[11px] text-slate-400 space-y-1 list-disc list-inside">
            <li>Draw end-to-end data flow: Client &rarr; DNS &rarr; CDN &rarr; L7 LB &rarr; Services.</li>
            <li>Define database schemas, primary keys, and shard keys.</li>
            <li>Walk through the happy path for read and write flows.</li>
          </ul>
        </div>

        <!-- Step 4 -->
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-mono text-rose-400">
            <span class="font-bold">STEP 4 (28-45m)</span>
            <span>17 Mins</span>
          </div>
          <h5 class="text-sm font-bold text-white">Deep Dive &amp; Scale</h5>
          <ul class="text-[11px] text-slate-400 space-y-1 list-disc list-inside">
            <li>Address bottlenecks: hot partitions, split-brain, cache avalanche.</li>
            <li>Fault tolerance: circuit breakers, leader re-election, CDC shadow replay.</li>
            <li>Observability: metrics (Prometheus), distributed traces (OpenTelemetry).</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
"""

SIMULATORS_JS = """
// ----------------------------------------------------
// TAB SWITCHER
// ----------------------------------------------------
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('block'));
  const target = document.getElementById(tabId);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('block');
  }

  // Update button styles
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.className = 'tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white';
  });
  const activeBtn = document.getElementById('btn-' + tabId);
  if (activeBtn) {
    activeBtn.className = 'tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all bg-emerald-500 text-slate-950 font-bold shadow-lg shadow-emerald-500/20';
  }

  if (tabId === 'tab-hashing') {
    renderHashRing();
  }
}

// ----------------------------------------------------
// 1. CAPACITY ESTIMATOR CALCULATIONS
// ----------------------------------------------------
const presets = {
  twitter: { dau: 500000000, reqs: 25, ratio: 20, payload: 1.5, retention: 730 },
  whatsapp: { dau: 2000000000, reqs: 50, ratio: 1, payload: 0.5, retention: 90 },
  tinyurl: { dau: 10000000, reqs: 15, ratio: 100, payload: 0.5, retention: 1825 },
  netflix: { dau: 250000000, reqs: 10, ratio: 50, payload: 10.0, retention: 365 },
};

function applyPreset(name) {
  if (!presets[name]) return;
  const p = presets[name];
  document.getElementById('input-dau').value = p.dau;
  document.getElementById('input-requests-per-day').value = p.reqs;
  document.getElementById('input-ratio').value = p.ratio;
  document.getElementById('input-payload').value = p.payload;
  document.getElementById('input-retention').value = p.retention;
  calculateCapacity();
}

function calculateCapacity() {
  const dau = parseFloat(document.getElementById('input-dau').value);
  const reqsPerDay = parseFloat(document.getElementById('input-requests-per-day').value);
  const ratio = parseFloat(document.getElementById('input-ratio').value);
  const payloadKb = parseFloat(document.getElementById('input-payload').value);
  const retentionDays = parseFloat(document.getElementById('input-retention').value);

  // Labels update
  document.getElementById('lbl-dau').innerText = dau.toLocaleString();
  document.getElementById('lbl-requests-per-day').innerText = reqsPerDay;
  const readPct = Math.round((ratio / (ratio + 1)) * 100);
  document.getElementById('lbl-ratio').innerText = ratio + ' : 1 (' + readPct + '% Reads)';
  document.getElementById('lbl-payload').innerText = payloadKb.toFixed(1) + ' KB';
  document.getElementById('lbl-retention').innerText = retentionDays + ' Days (' + (retentionDays / 365).toFixed(1) + ' Years)';

  // Math
  const totalDailyRequests = dau * reqsPerDay;
  const totalQps = Math.round(totalDailyRequests / 86400);
  const writeFraction = 1 / (ratio + 1);
  const readFraction = ratio / (ratio + 1);

  const writeQps = Math.round(totalQps * writeFraction);
  const readQps = Math.round(totalQps * readFraction);
  const peakQps = Math.round(totalQps * 2.5);

  const dailyStorageBytes = totalDailyRequests * writeFraction * (payloadKb * 1024);
  const retentionStorageBytes = dailyStorageBytes * retentionDays;
  const hotCacheRamBytes = dailyStorageBytes * 0.20; // 80/20 rule

  const ingressBps = writeQps * (payloadKb * 1024) * 8;
  const egressBps = readQps * (payloadKb * 1024) * 8;

  // Format
  document.getElementById('res-total-qps').innerText = totalQps.toLocaleString();
  document.getElementById('res-read-qps').innerText = readQps.toLocaleString();
  document.getElementById('res-write-qps').innerText = writeQps.toLocaleString();
  document.getElementById('res-peak-qps').innerText = peakQps.toLocaleString();

  document.getElementById('res-storage-day').innerText = formatBytes(dailyStorageBytes);
  document.getElementById('res-storage-retention').innerText = formatBytes(retentionStorageBytes);
  document.getElementById('res-cache-ram').innerText = formatBytes(hotCacheRamBytes);

  document.getElementById('res-bandwidth').innerText =
    (ingressBps / 1e6).toFixed(1) + ' Mbps In / ' + (egressBps / 1e9).toFixed(2) + ' Gbps Out';

  // Architecture recommendation
  let arch = '';
  if (totalQps < 1000) {
    arch = 'Standard monolithic/microservice tier with a single PostgreSQL instance and read replica.';
  } else if (totalQps < 20000) {
    arch = 'Horizontal stateless services behind L7 Nginx/Envoy, Redis cluster for caching, sharded DB with read replicas.';
  } else {
    arch = 'Planet-scale multi-region active-active deployment, Anycast DNS, Kafka streaming backbone, distributed NoSQL / Spanner, and multi-tier edge CDN caching.';
  }
  document.getElementById('res-architecture-rec').innerText = arch;
}

function formatBytes(bytes) {
  if (bytes < 1e9) return (bytes / 1e6).toFixed(1) + ' MB';
  if (bytes < 1e12) return (bytes / 1e9).toFixed(1) + ' GB';
  return (bytes / 1e12).toFixed(1) + ' TB';
}

// ----------------------------------------------------
// 2. LATENCY MACHINE
// ----------------------------------------------------
const latencyData = [
  { name: 'L1 CPU Cache Reference', ns: 0.5, human: '0.5 Seconds (A blink)', color: 'text-emerald-400' },
  { name: 'Branch Mispredict Penalty', ns: 5, human: '5 Seconds', color: 'text-emerald-400' },
  { name: 'L2 CPU Cache Reference', ns: 7, human: '7 Seconds', color: 'text-emerald-400' },
  { name: 'Mutex Lock / Unlock', ns: 25, human: '25 Seconds', color: 'text-cyan-400' },
  { name: 'Main Memory (RAM) Access', ns: 100, human: '1.7 Minutes (Making coffee)', color: 'text-cyan-400' },
  { name: 'Compress 1KB with Snappy/ZSTD', ns: 2000, human: '33 Minutes', color: 'text-indigo-400' },
  { name: 'Send 2KB over 1 Gbps Network', ns: 20000, human: '5.5 Hours (A work shift)', color: 'text-indigo-400' },
  { name: 'Read 1MB Sequentially from NVMe SSD', ns: 100000, human: '1.2 Days (A weekend getaway)', color: 'text-amber-400' },
  { name: 'HDD Random Disk Seek', ns: 10000000, human: '3.8 Months (A college semester)', color: 'text-rose-400' },
  { name: 'Cross-Atlantic Roundtrip (NYC to London)', ns: 150000000, human: '4.8 Years (Earning a degree!)', color: 'text-rose-500 font-bold' }
];

let latencyMode = 'raw';
function toggleLatencyScale(mode) {
  latencyMode = mode;
  document.getElementById('btn-scale-raw').className = mode === 'raw' ? 'px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 text-slate-950' : 'px-3 py-1 rounded-lg text-xs font-mono text-slate-400 hover:text-white';
  document.getElementById('btn-scale-human').className = mode === 'human' ? 'px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 text-slate-950' : 'px-3 py-1 rounded-lg text-xs font-mono text-slate-400 hover:text-white';
  renderLatency();
}

function renderLatency() {
  const container = document.getElementById('latency-items-container');
  if (!container) return;
  container.innerHTML = latencyData.map(item => {
    const valDisplay = latencyMode === 'raw' ? item.ns.toLocaleString() + ' ns' : item.human;
    // Logarithmic width for bar
    const barWidth = Math.min(100, Math.max(2, Math.log10(item.ns + 1) * 11));
    return `
      <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div class="w-72 truncate text-slate-300">${item.name}</div>
        <div class="flex-1 mx-2 h-2 bg-slate-800 rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full" style="width: ${barWidth}%"></div>
        </div>
        <div class="w-56 text-right font-mono font-bold ${item.color}">${valDisplay}</div>
      </div>
    `;
  }).join('');
}

// ----------------------------------------------------
// 3. CONSISTENT HASH RING
// ----------------------------------------------------
let hashNodes = [
  { id: 'Node-A', color: '#06b6d4', angle: 45 },
  { id: 'Node-B', color: '#10b981', angle: 135 },
  { id: 'Node-C', color: '#f59e0b', angle: 225 },
  { id: 'Node-D', color: '#ec4899', angle: 315 },
];
let sampleKeys = [];
let vnodesCount = 3;

function updateVNodes(val) {
  vnodesCount = parseInt(val);
  document.getElementById('lbl-vnodes').innerText = val + ' vnodes';
  renderHashRing();
}

function addHashNode() {
  const names = ['Node-E', 'Node-F', 'Node-G', 'Node-H'];
  const colors = ['#8b5cf6', '#3b82f6', '#14b8a6', '#f97316'];
  const idx = hashNodes.length;
  if (idx >= 8) {
    alert('Maximum 8 nodes in demo simulator.');
    return;
  }
  const name = names[idx - 4] || ('Node-' + (idx + 1));
  const color = colors[idx - 4] || '#38bdf8';
  hashNodes.push({ id: name, color: color, angle: Math.floor(Math.random() * 360) });
  renderHashRing();
}

function removeHashNode() {
  if (hashNodes.length <= 2) {
    alert('Minimum 2 nodes required for hash ring.');
    return;
  }
  hashNodes.pop();
  renderHashRing();
}

function insertSampleKeys() {
  sampleKeys = [];
  for (let i = 1; i <= 20; i++) {
    sampleKeys.push({ id: 'user_' + Math.floor(Math.random() * 9000 + 1000), angle: Math.floor(Math.random() * 360) });
  }
  renderHashRing();
}

function renderHashRing() {
  const svg = document.getElementById('hash-ring-svg');
  if (!svg) return;
  const cx = 200, cy = 200, r = 140;

  // Build virtual nodes
  let allPoints = [];
  hashNodes.forEach(node => {
    for (let v = 0; v < vnodesCount; v++) {
      const vAngle = (node.angle + (v * (360 / (hashNodes.length * vnodesCount)))) % 360;
      allPoints.push({
        nodeId: node.id,
        color: node.color,
        angle: vAngle,
        label: v === 0 ? node.id : ''
      });
    }
  });

  allPoints.sort((a, b) => a.angle - b.angle);

  // Compute key distribution
  let distribution = {};
  hashNodes.forEach(n => distribution[n.id] = 0);

  sampleKeys.forEach(k => {
    // Find next clockwise node
    let target = allPoints.find(p => p.angle >= k.angle);
    if (!target) target = allPoints[0];
    distribution[target.nodeId]++;
  });

  // SVG Content
  let svgContent = `
    <!-- Outer Ring -->
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#334155" stroke-width="4" stroke-dasharray="4"/>
    <text x="${cx}" y="${cy - 8}" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">HASH RING</text>
    <text x="${cx}" y="${cy + 12}" fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="middle">0 &rarr; 2^32 - 1</text>
  `;

  // Draw Keys
  sampleKeys.forEach(k => {
    const rad = (k.angle * Math.PI) / 180;
    const kx = cx + (r - 20) * Math.cos(rad);
    const ky = cy + (r - 20) * Math.sin(rad);
    svgContent += `<circle cx="${kx}" cy="${ky}" r="3" fill="#cbd5e1" opacity="0.8"/>`;
  });

  // Draw Nodes & Vnodes
  allPoints.forEach(p => {
    const rad = (p.angle * Math.PI) / 180;
    const nx = cx + r * Math.cos(rad);
    const ny = cy + r * Math.sin(rad);
    const isPrimary = p.label !== '';
    const nodeRadius = isPrimary ? 10 : 5;
    svgContent += `
      <circle cx="${nx}" cy="${ny}" r="${nodeRadius}" fill="${p.color}" stroke="#0f172a" stroke-width="2"/>
    `;
    if (isPrimary) {
      const tx = cx + (r + 22) * Math.cos(rad);
      const ty = cy + (r + 22) * Math.sin(rad) + 4;
      svgContent += `
        <text x="${tx}" y="${ty}" fill="${p.color}" font-size="10" font-weight="bold" font-family="monospace" text-anchor="middle">${p.label}</text>
      `;
    }
  });

  svg.innerHTML = svgContent;

  // Update distribution table
  const listEl = document.getElementById('hash-nodes-list');
  if (listEl) {
    listEl.innerHTML = hashNodes.map(n => {
      const count = distribution[n.id] || 0;
      const pct = sampleKeys.length > 0 ? Math.round((count / sampleKeys.length) * 100) : 0;
      return `
        <div class="flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${n.color};"></span>
            <span class="text-white">${n.id}</span>
          </div>
          <div class="text-slate-400">${count} keys (${pct}%)</div>
        </div>
      `;
    }).join('');
    document.getElementById('lbl-total-keys').innerText = sampleKeys.length + ' Keys Placed';
  }
}

// ----------------------------------------------------
// 4. RATE LIMITER SIMULATOR
// ----------------------------------------------------
let rlCapacity = 10;
let rlTokens = 10;
let rlRefillRate = 2; // per second
let rlTimer = null;

function startRateLimiterTicker() {
  if (rlTimer) clearInterval(rlTimer);
  rlTimer = setInterval(() => {
    if (rlTokens < rlCapacity) {
      rlTokens = Math.min(rlCapacity, rlTokens + 1);
      updateRateLimiterUI();
    }
  }, 500); // 2 tokens per sec -> 1 every 500ms
}

function updateRateLimiterUI() {
  const pct = Math.round((rlTokens / rlCapacity) * 100);
  const bar = document.getElementById('rl-meter-bar');
  const text = document.getElementById('rl-meter-text');
  if (bar) bar.style.width = pct + '%';
  if (text) {
    text.innerText = rlTokens + ' / ' + rlCapacity;
    text.className = rlTokens > 3 ? 'text-emerald-400 font-bold' : (rlTokens > 0 ? 'text-amber-400 font-bold' : 'text-rose-400 font-bold');
  }
}

function logRateLimit(msg, type) {
  const term = document.getElementById('rl-log-terminal');
  if (!term) return;
  const time = new Date().toISOString().substring(11, 19);
  const color = type === 'ok' ? 'text-emerald-400' : (type === 'err' ? 'text-rose-400 font-bold' : 'text-slate-400');
  const row = document.createElement('div');
  row.className = color;
  row.innerHTML = `<span class="text-slate-600">[${time}]</span> ${msg}`;
  term.prepend(row);
}

function clearRateLimitLogs() {
  const term = document.getElementById('rl-log-terminal');
  if (term) term.innerHTML = '<div class="text-slate-500">[Logs Cleared]</div>';
}

function sendRateLimitRequest(count) {
  for (let i = 0; i < count; i++) {
    if (rlTokens >= 1) {
      rlTokens--;
      logRateLimit(`HTTP 200 OK &bull; Token consumed (Remaining: ${rlTokens})`, 'ok');
    } else {
      logRateLimit(`HTTP 429 Too Many Requests &bull; Rate limit exceeded! (Retry-After: 1s)`, 'err');
    }
  }
  updateRateLimiterUI();
}

function simulateTrafficAttack() {
  sendRateLimitRequest(25);
}

function changeRateLimiterAlgo(val) {
  rlTokens = 10;
  updateRateLimiterUI();
  logRateLimit(`Switched algorithm to: ${val}`, 'info');
}

// ----------------------------------------------------
// 5. 45-MINUTE INTERVIEW TIMER
// ----------------------------------------------------
let interviewTime = 45 * 60;
let interviewTimerInterval = null;
let isInterviewRunning = false;

function toggleInterviewTimer() {
  const btn = document.getElementById('btn-timer-toggle');
  if (isInterviewRunning) {
    clearInterval(interviewTimerInterval);
    isInterviewRunning = false;
    btn.innerText = 'Resume';
    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-cyan-500 text-slate-950';
  } else {
    isInterviewRunning = true;
    btn.innerText = 'Pause';
    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-500 text-slate-950';
    interviewTimerInterval = setInterval(() => {
      if (interviewTime > 0) {
        interviewTime--;
        renderInterviewTimer();
      } else {
        clearInterval(interviewTimerInterval);
        isInterviewRunning = false;
        alert('Time is up! Conclude with trade-offs and monitoring.');
      }
    }, 1000);
  }
}

function resetInterviewTimer() {
  clearInterval(interviewTimerInterval);
  isInterviewRunning = false;
  interviewTime = 45 * 60;
  renderInterviewTimer();
  const btn = document.getElementById('btn-timer-toggle');
  if (btn) {
    btn.innerText = 'Start Timer';
    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500 text-slate-950';
  }
}

function renderInterviewTimer() {
  const display = document.getElementById('interview-timer-display');
  if (!display) return;
  const mins = Math.floor(interviewTime / 60);
  const secs = interviewTime % 60;
  display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  if (mins < 5) {
    display.className = 'font-mono text-xl font-bold text-rose-500 bg-slate-950 px-3 py-1.5 rounded-lg border border-rose-800';
  } else {
    display.className = 'font-mono text-xl font-bold text-emerald-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800';
  }
}

// ----------------------------------------------------
// INITIALIZATION ON LOAD
// ----------------------------------------------------
window.addEventListener('DOMContentLoaded', () => {
  calculateCapacity();
  renderLatency();
  renderHashRing();
  startRateLimiterTicker();
  renderInterviewTimer();
});
"""

print("Simulators HTML and JS prepared successfully.")
