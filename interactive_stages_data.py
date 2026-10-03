# interactive_stages_data.py
# Rich Interactive Simulators for Stage 13, plus Stages 14, 15, 16, 17 and Whiteboard Modal

STAGE_13_SIMULATORS = """
<section id="stage-13" class="stage-section flex-1 flex flex-col overflow-hidden h-full" style="display: none;">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40 font-mono">
          Stage 13 • Advanced Distributed Systems Physics Lab
        </span>
        <span class="text-xs text-slate-400">8 Real-Time Interactive Engineering Simulators</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Distributed Systems Execution & Hardware Physics Simulators</h2>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-xs font-mono text-cyan-400 bg-cyan-950/80 px-2.5 py-1 rounded border border-cyan-800/60 font-bold">
        Interactive Visual Lab Active
      </span>
    </div>
  </div>

  <!-- Tabbed Simulator Switcher (Responsive Grid - All 8 Visible Without Scrolling) -->
  <div class="shrink-0 px-6 py-2 bg-[#040818] border-b border-white/[0.08]" id="sim-tabs">
    <div class="grid grid-cols-2 sm:grid-cols-4 xl:grid-cols-8 gap-1.5 text-xs">
      <button onclick="switchSim('sim-zerocopy')" id="tab-sim-zerocopy" class="tab-btn active px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">⚡ 1. Zero-Copy</button>
      <button onclick="switchSim('sim-raft')" id="tab-sim-raft" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🗳️ 2. Raft Cluster</button>
      <button onclick="switchSim('sim-hashring')" id="tab-sim-hashring" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🎯 3. Hash Ring</button>
      <button onclick="switchSim('sim-tokenbucket')" id="tab-sim-tokenbucket" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🚰 4. Rate Limiter</button>
      <button onclick="switchSim('sim-fencing')" id="tab-sim-fencing" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🔒 5. Fencing Token</button>
      <button onclick="switchSim('sim-tail')" id="tab-sim-tail" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">📈 6. Tail Latency</button>
      <button onclick="switchSim('sim-lsm')" id="tab-sim-lsm" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🧱 7. LSM Compaction</button>
      <button onclick="switchSim('sim-cte')" id="tab-sim-cte" class="tab-btn px-2 py-1.5 rounded-lg text-slate-300 hover:text-white transition-all font-medium text-center border border-white/[0.08] bg-slate-900/60 truncate">🌳 8. CTE Tree</button>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6">
    
    <!-- LAB 1: ZERO-COPY -->
    <div id="sim-zerocopy" class="sim-panel space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Linux Kernel Zero-Copy vs Traditional 4-Copy Memory Pipeline</h4>
            <p class="text-[11px] text-slate-400">Live animated packet particles traveling from Disk through Kernel PageCache, User-space heap, socket buffers, and NIC DMA rings.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="setZeroCopyMode('traditional')" id="btn-mode-trad" class="px-3 py-1 rounded-lg text-xs font-semibold bg-rose-950 text-rose-300 border border-rose-800 shadow">Traditional (4 Copies, 4 Context Switches)</button>
            <button onclick="setZeroCopyMode('zerocopy')" id="btn-mode-zero" class="px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800 hover:text-white">Zero-Copy sendfile() (0 CPU Copies)</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex flex-col justify-between overflow-hidden shadow-inner">
          <canvas id="zc-canvas" class="w-full h-full block"></canvas>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">CPU Copies per Packet:</span>
            <span id="zc-stat-cpu-copies" class="font-bold text-rose-400 text-sm">2 Copies (User/Kernel)</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Context Switches:</span>
            <span id="zc-stat-switches" class="font-bold text-rose-400 text-sm">4 Switches</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">JVM Heap GC Churn:</span>
            <span id="zc-stat-heap" class="font-bold text-rose-400 text-sm">45 MB/s Young Gen</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Ingestion Throughput:</span>
            <span id="zc-stat-tps" class="font-bold text-cyan-400 text-sm">18,500 TPS</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LAB 2: RAFT CONSENSUS -->
    <div id="sim-raft" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Raft Consensus Cluster: Leader Election & Log Replication</h4>
            <p class="text-[11px] text-slate-400">Interactive 5-node distributed cluster. Trigger leader network partitions, observe heartbeat timeouts, watch election of new leader with higher term, and submit linearizable transactions.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="raftPartitionLeader()" id="btn-raft-part" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold">⚡ Partition Leader</button>
            <button onclick="raftHealNetwork()" id="btn-raft-heal" class="px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs font-semibold">🩺 Heal Network</button>
            <button onclick="raftSubmitTx()" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-semibold">📝 Propose Log Tx (+25 XP)</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-80 flex items-center justify-center shadow-inner">
          <canvas id="raft-canvas" class="w-full h-full block"></canvas>
        </div>

        <div id="raft-log-status" class="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-[11px] text-slate-300 flex flex-wrap items-center justify-between gap-2">
          <span>Cluster: <strong class="text-emerald-400">5 Nodes Operational</strong> | Current Term: <strong id="raft-term-val" class="text-cyan-400">1</strong> | Leader: <strong id="raft-leader-val" class="text-amber-400">Node 1</strong> | Committed Index: <strong id="raft-commit-val" class="text-emerald-400">104</strong></span>
          <span class="text-[10px] text-slate-400">Quorum Requirement: (5/2 + 1) = 3 Nodes Majority</span>
        </div>
      </div>
    </div>

    <!-- LAB 3: CONSISTENT HASH RING -->
    <div id="sim-hashring" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Consistent Hash Ring with Virtual Nodes (V-Nodes)</h4>
            <p class="text-[11px] text-slate-400">Observe how virtual nodes eliminate hot-spot partitions in Cassandra/Scylla. Toggle between V=1 (severe hot spots) and V=150 (uniform distribution).</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="setVNodes(1)" id="btn-vnode-1" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs">V=1 (Naive)</button>
            <button onclick="setVNodes(50)" id="btn-vnode-50" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs">V=50</button>
            <button onclick="setVNodes(150)" id="btn-vnode-150" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-bold shadow">V=150 (Google Staff)</button>
            <button onclick="addHashNode()" class="px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs">+ Add Node E</button>
            <button onclick="removeHashNode()" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs">- Remove Node</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-80 flex items-center justify-center shadow-inner">
          <canvas id="hash-canvas" class="w-full h-full block"></canvas>
        </div>

        <div class="p-3 bg-slate-900 rounded-lg border border-slate-800 font-mono text-[11px] flex justify-between items-center text-slate-300">
          <span>Active Nodes: <strong id="hash-node-count" class="text-cyan-400">4 Physical Nodes</strong> | Total V-Nodes: <strong id="hash-vnode-count" class="text-emerald-400">600 Arcs</strong></span>
          <span>Key Standard Deviation: <strong id="hash-stddev-val" class="text-emerald-400">&lt; 3.2% (Uniform Distribution)</strong></span>
        </div>
      </div>
    </div>

    <!-- LAB 4: TOKEN BUCKET & GCRA -->
    <div id="sim-tokenbucket" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Dual Rate Limiter: Token Bucket vs Leaky Bucket (GCRA)</h4>
            <p class="text-[11px] text-slate-400">Simulate incoming traffic burst arrivals. Observe how GCRA calculates theoretical arrival times (TAT) to smooth spikes without dropping legitimate requests.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="injectBurst(20)" class="px-3 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-bold">+20 Normal Burst</button>
            <button onclick="injectBurst(60)" class="px-3 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-bold">+60 Flood Spike</button>
            <button onclick="resetTokenBucket()" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-xs">Reset</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center shadow-inner">
          <canvas id="tb-canvas" class="w-full h-full block"></canvas>
        </div>

        <div class="grid grid-cols-3 gap-3 text-xs font-mono">
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Token Bucket Available:</span>
            <span id="tb-tokens-val" class="font-bold text-cyan-400 text-sm">45 / 50 Tokens</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Allowed Requests (200 OK):</span>
            <span id="tb-allowed-val" class="font-bold text-emerald-400 text-sm">184 Requests</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Throttled (HTTP 429 Drops):</span>
            <span id="tb-dropped-val" class="font-bold text-rose-400 text-sm">0 Drops</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LAB 5: MONOTONIC FENCING -->
    <div id="sim-fencing" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Martin Kleppmann GC Pause & Monotonic Fencing Sentry</h4>
            <p class="text-[11px] text-slate-400">Step through the classic distributed locking flaw where a Stop-The-World GC pause causes lock expiration, leading to concurrent split-brain writes.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="fencingStep(1)" id="btn-fence-1" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-semibold">1. Client 1 Lock (Token 101)</button>
            <button onclick="fencingStep(2)" id="btn-fence-2" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold">2. Client 1 GC Pause (15s)</button>
            <button onclick="fencingStep(3)" id="btn-fence-3" class="px-2.5 py-1 rounded bg-amber-950 text-amber-300 border border-amber-800 text-xs font-semibold">3. Client 2 Lock (Token 102)</button>
            <button onclick="fencingStep(4)" id="btn-fence-4" class="px-2.5 py-1 rounded bg-purple-950 text-purple-300 border border-purple-800 text-xs font-semibold">4. Client 1 Zombie Write</button>
            <button onclick="fencingReset()" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-xs">Reset</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center shadow-inner">
          <canvas id="fence-canvas" class="w-full h-full block"></canvas>
        </div>

        <div id="fence-log-box" class="p-3 bg-slate-900 rounded-lg border border-slate-800 font-mono text-xs text-slate-300 leading-relaxed">
          Step 0: Ready. Click "1. Client 1 Lock (Token 101)" to start the distributed locking race scenario.
        </div>
      </div>
    </div>

    <!-- LAB 6: TAIL AT SCALE -->
    <div id="sim-tail" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Google "Tail at Scale" Hedged Requests Latency Simulator</h4>
            <p class="text-[11px] text-slate-400">Simulate fanout queries across 10 replica servers where Server 7 experiences a 450ms tail latency spike. Toggle Hedged Requests to observe tail latency reduction.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="toggleHedging(false)" id="btn-hedge-off" class="px-3 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold">Without Hedging (Wait for Slow Server)</button>
            <button onclick="toggleHedging(true)" id="btn-hedge-on" class="px-3 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-xs font-semibold">With Hedged Requests (Duplicate after 15ms)</button>
            <button onclick="runTailSimulation()" class="px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow">▶ Run Fanout Query</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center shadow-inner">
          <canvas id="tail-canvas" class="w-full h-full block"></canvas>
        </div>

        <div class="grid grid-cols-3 gap-3 text-xs font-mono">
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Overall Request Latency:</span>
            <span id="tail-p99-val" class="font-bold text-rose-400 text-sm">452 ms (Blocked by S7)</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Tail Latency Reduction:</span>
            <span id="tail-drop-val" class="font-bold text-emerald-400 text-sm">0% (Unmitigated)</span>
          </div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">Additional Server Overhead:</span>
            <span id="tail-overhead-val" class="font-bold text-cyan-400 text-sm">0.0%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LAB 7: LSM COMPACTION -->
    <div id="sim-lsm" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">LSM-Tree Storage Engine: MemTable Flush & Leveled Compaction</h4>
            <p class="text-[11px] text-slate-400">Observe writes inserting into concurrent SkipList MemTable, flushing immutable tables to L0 SSTables, and merging overlapping key ranges down to L1 and L2 via Leveled Compaction.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="lsmWriteKey()" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-bold">+ Write Key-Value</button>
            <button onclick="lsmFlush()" class="px-2.5 py-1 rounded bg-amber-950 text-amber-300 border border-amber-800 text-xs font-semibold">Flush MemTable to L0</button>
            <button onclick="lsmCompact()" class="px-2.5 py-1 rounded bg-purple-950 text-purple-300 border border-purple-800 text-xs font-semibold">Run Leveled Compaction</button>
            <button onclick="lsmProbeKey()" class="px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs font-semibold">🔍 Bloom Filter Probe</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center shadow-inner">
          <canvas id="lsm-canvas" class="w-full h-full block"></canvas>
        </div>

        <div id="lsm-log-box" class="p-3 bg-slate-900 rounded-lg border border-slate-800 font-mono text-[11px] text-slate-300 flex justify-between items-center">
          <span>MemTable: <strong id="lsm-mem-val" class="text-cyan-400">12 / 64 KB</strong> | L0 SSTables: <strong id="lsm-l0-val" class="text-amber-400">2 files</strong> | L1 Partitioned: <strong id="lsm-l1-val" class="text-emerald-400">4 files</strong></span>
          <span class="text-emerald-400 font-bold">Bloom Filter False Positive &lt; 1%</span>
        </div>
      </div>
    </div>

    <!-- LAB 8: CTE TREE -->
    <div id="sim-cte" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">3GPP CTE Charging Tree: Lock-Free Radix DAG & Quota Reservation</h4>
            <p class="text-[11px] text-slate-400">Interactive 3GPP TS 32.299 Charging Tree. Click a service request to watch lock-free prefix DAG traversal highlight matching tariffs in sub-millisecond time.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="cteSelectService('video')" id="btn-cte-video" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-bold">5G 4K Video Stream</button>
            <button onclick="cteSelectService('voice')" id="btn-cte-voice" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs">VoNR Ultra HD Voice</button>
            <button onclick="cteSelectService('iot')" id="btn-cte-iot" class="px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs">Massive IoT Sensor</button>
            <button onclick="cteSimulateQuotaReservation()" class="px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow">⚡ Reserve Quota (+25 XP)</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center shadow-inner">
          <canvas id="cte-canvas" class="w-full h-full block"></canvas>
        </div>

        <div id="cte-log-box" class="p-3 bg-slate-900 rounded-lg border border-slate-800 font-mono text-[11px] text-slate-300 flex justify-between items-center">
          <span>Active Packet: <strong id="cte-packet-label" class="text-cyan-400">Rating Group 100 (5G Video)</strong> | Tariff: <strong id="cte-rate-label" class="text-amber-400">$0.05 / MB</strong></span>
          <span>Traversal Time: <strong class="text-emerald-400">0.82 ms p99 (Zero DB Round-Trips)</strong></span>
        </div>
      </div>
    </div>

  </div>
</section>
"""

STAGE_14_LEADERSHIP = """
<section id="stage-14" class="stage-section flex-1 flex flex-col overflow-hidden h-full" style="display: none;">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40 font-mono">
          Stage 14 • Google Staff & Principal Leadership Playbook
        </span>
        <span class="text-xs text-slate-400">GCA, Googleyness & Staff Multiplier</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google L6/L8 Staff Leadership STAR Playbook</h2>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-2">
      <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block font-mono">Google 4-Pillar Evaluation Rubric for Staff Engineers</span>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-[11px] pt-1 font-mono">
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">1. GCA:</strong>
          <span class="text-slate-400">Decomposing ill-defined problems with first-principles reasoning under ambiguity.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">2. Role-Related Knowledge:</strong>
          <span class="text-slate-400">Mastery of kernel physics, distributed state, failure domains, and hardware bottlenecks.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">3. Leadership & Multiplier:</strong>
          <span class="text-slate-400">Leading without authority; unblocking cross-functional teams; leveling up senior engineers.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">4. Googleyness:</strong>
          <span class="text-slate-400">Intellectual humility, doing the right thing for users, and blameless post-mortem culture.</span>
        </div>
      </div>
    </div>

    <!-- STAR SCENARIOS -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <span class="font-bold text-emerald-400 block border-b border-slate-800 pb-1.5 font-mono">1. Resolving Cross-Org Architectural Deadlock</span>
        <p><strong>Situation:</strong> Gateway team demanded synchronous REST/HTTP with client-side polling, while Backend team advocated for Kafka event streams. 3 weeks from delivery slip.</p>
        <p><strong>Task:</strong> Align both teams without executive mandate to prevent a 6-month slip.</p>
        <p><strong>Action:</strong> Built benchmark prototype comparing 10k concurrent HTTP sockets vs Kafka zero-copy throughput. Held open RFC review addressing debugging concerns via Protobuf schemas.</p>
        <p><strong>Result:</strong> Gateway team unanimously adopted Kafka event model. Shipped on schedule with 99.999% availability.</p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <span class="font-bold text-rose-400 block border-b border-slate-800 pb-1.5 font-mono">2. Incident Command: Nationwide Outage & Blameless RCA</span>
        <p><strong>Situation:</strong> Rebalance storm locked out 20M cell tower parameters during peak traffic rollout.</p>
        <p><strong>Task:</strong> Lead incident command room, halt cascading failure, and conduct blameless post-mortem.</p>
        <p><strong>Action:</strong> Canary rollback in 3 minutes. Led RCA discovering Eager rebalance caused global freeze and lack of fencing caused state corruption. Implemented Cooperative Sticky assignor and monotonic tokens.</p>
        <p><strong>Result:</strong> Zero repeat occurrences; rebalance pauses dropped from 14s to 400ms.</p>
      </div>
    </div>
  </div>

    <!-- GOOGLE L6 TECHNICAL SCREENING & SYSTEM MASTERY Q&A (11 PRODUCTION QUESTIONS) -->
    <div class="mt-8 space-y-4 border-t border-white/[0.08] pt-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono flex items-center gap-2">
            <span>⚡</span> Google L6 Technical Screening &amp; Core Systems Mastery Q&amp;A
          </span>
          <p class="text-slate-400 text-[11px] mt-0.5">11 Battle-tested production answers anchored in carrier-grade distributed systems and real office architecture.</p>
        </div>
        <span class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px] font-mono">11 Core Answers</span>
      </div>

      <div class="space-y-3">
        
        <!-- Q1: Language Strength -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>1. Which programming language are you strongest in? (Java)</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Primary Language:</strong> Java (Java 21 / 17 / 11 / 8). Over 10 years architecting mission-critical, low-latency distributed systems.</p>
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Java 21 Virtual Threads (Loom):</strong> Solved high-density I/O bottlenecks in parallel firmware flashing and NETCONF sync by decoupling execution from bound OS platform threads.</li>
              <li><strong>Pattern Matching &amp; Records:</strong> Strongly typed, immutable event representations enforcing compile-time exhaustive state-machine transitions across complex telecom workflows.</li>
              <li><strong>JVM Internals &amp; Memory Physics:</strong> Garbage collection tuning (ZGC and G1GC) suppressing stop-the-world pauses on 64GB+ heaps; low-level profiling with async-profiler and JFR.</li>
            </ul>
          </div>
        </details>

        <!-- Q2: Microservices Architecture & Scalability -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>2. Describe the microservices architecture of your recent product. How do you make it scalable &amp; fault tolerant?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>System:</strong> Samsung Unified System Manager (USM) Configuration Management platform (3,164+ Java files across 60+ sub-modules) managing 4G/5G/O-RAN infrastructure for 15+ global Tier-1 operators.</p>
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Workload Bulkheading:</strong> Isolated worker execution pools per operator and per Network Element type, preventing bulk operator surges from starving neighboring queues.</li>
              <li><strong>Key-Partitioned Kafka Ingestion:</strong> Ingestion events partitioned by <code class="text-cyan-400 font-mono">NetworkElement_ID</code> to guarantee strict sequential FIFO processing per base station without cross-cluster distributed locks.</li>
              <li><strong>Stateless Compute &amp; Distributed Session Locking:</strong> Handlers are stateless on Kubernetes; multi-step editing operations on deep 3GPP containment trees use lease-based session locks (<code class="text-cyan-400 font-mono">SessionLocker</code>) with heartbeats to prevent split-brain updates.</li>
              <li><strong>Idempotency:</strong> Distributed sliding-window deduplication keys ensure flaky wireless retries do not trigger duplicate mutations.</li>
            </ul>
          </div>
        </details>

        <!-- Q3: Failures, Retries, Timeouts & Circuit Breaking -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>3. How do you handle service failures, retries, timeouts, and circuit breaking? (45k TPS Scale)</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Production Scale:</strong> Managing 20M+ cells and 1M+ Network Elements, sustaining peak ingestion bursts of <strong>45,000+ config transactions/sec</strong> during metropolitan reconfigurations.</p>
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Explicit Timeouts:</strong> Connect timeout (1-2s) and socket read timeout (5-8s) calibrated against observed p99 latencies.</li>
              <li><strong>Retries with Exponential Backoff &amp; Full Jitter:</strong> Retries applied strictly to idempotent requests on 5xx/network reset errors; randomized jitter prevents thundering herd collapses.</li>
              <li><strong>Circuit Breaking:</strong> Resilience4j/Envoy circuit breakers trip to OPEN when error rates exceed 50% over a 10s sliding window, fast-failing to preserve compute pools.</li>
              <li><strong>Dead Letter Queues (DLQ):</strong> Unrecoverable events are shunted to persistent DLQ topics for async reconciliation without blocking main ingestion pipelines.</li>
            </ul>
          </div>
        </details>

        <!-- Q4: Retail Inventory Visibility Design -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>4. Design a scalable backend system for real-time inventory visibility across thousands of retail stores.</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Architecture Blueprint:</strong> Thousands of stores, millions of SKUs, real-time read p99 &lt; 20ms.</p>
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Partitioned Ingestion:</strong> POS checkouts and web orders publish to Kafka keyed by <code class="text-cyan-400 font-mono">hash(store_id:sku_id)</code>, guaranteeing single-partition sequential processing per product per store.</li>
              <li><strong>Real-Time Serving Cache (Redis Cluster):</strong> Stock balances stored in Redis Hashes (<code class="text-cyan-400 font-mono">HSET store:{id} {sku} {qty}</code>). Decrements executed atomically via Lua scripts (<code class="text-cyan-400 font-mono">if qty &gt;= req then HINCRBY -req return 1 else return 0</code>), delivering sub-5ms read lookups.</li>
              <li><strong>Event-Sourced Persistence:</strong> Transactions appended to immutable ledger tables in sharded PostgreSQL/ScyllaDB; reconciliation processed via Debezium CDC.</li>
              <li><strong>Offline Store Edge Resilience:</strong> Stores maintain local SQLite cache for offline checkout, reconciling via vector clocks upon WAN restoration.</li>
            </ul>
          </div>
        </details>

        <!-- Q5: High Availability & Horizontal Scaling -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>5. How do you design for High Availability if services go down? How to scale horizontally?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Multi-AZ Active-Active:</strong> Stateless pods deployed across &ge;3 Availability Zones with automated health-check failover.</li>
              <li><strong>Graceful Degradation:</strong> If real-time inventory reservation degrades, checkout falls back to optimistic reservation with async reconciliation rather than hard 500 errors.</li>
              <li><strong>Domain-Driven Sharding:</strong> Shard compute and database tiers by <code class="text-cyan-400 font-mono">store_id</code> or <code class="text-cyan-400 font-mono">region</code>; transactions at Store 101 never contend with Store 502.</li>
              <li><strong>Custom Metric Autoscaling:</strong> Kubernetes HPA scales on Kafka consumer lag (via KEDA) and p99 latency rather than crude CPU metrics.</li>
              <li><strong>CQRS:</strong> High-frequency reads route to Redis clusters and read replicas; primary database handles transactional writes only.</li>
            </ul>
          </div>
        </details>

        <!-- Q6: System Re-Architecture -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>6. How do you identify and re-architect a legacy system facing scalability issues?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <ol class="list-decimal pl-4 space-y-1 text-slate-400">
              <li><strong>Measure First:</strong> Distributed tracing (OpenTelemetry/Jaeger), APM, and JVM profiling (async-profiler) to classify bottlenecks (DB locks, thread starvation, GC pauses, serial RPC queueing).</li>
              <li><strong>Strangler Fig Pattern:</strong> Avoid high-risk big-bang rewrites. Place a proxy in front of legacy systems, decouple synchronous calls into Kafka streams, and peel off bounded domains incrementally.</li>
              <li><strong>Shadow Traffic &amp; Dark Launch:</strong> Replay live production traffic to both systems in parallel to verify 100% output parity and latency improvements prior to canary rollout (1% &rarr; 10% &rarr; 100%).</li>
            </ol>
          </div>
        </details>

        <!-- Q7: Concurrency & Race Conditions -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>7. Real-world concurrency problem? What are race conditions and how to prevent them?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Real-World Case:</strong> Parallel firmware upgrades across 5,000 base stations previously required 14 hours sequentially. Re-architected using Java 21 Virtual Threads (Loom), slashing the runtime to <strong>22 minutes</strong> without thread exhaustion.</p>
            <p><strong>Race Condition Definition:</strong> Non-deterministic execution when concurrent threads mutate shared state without synchronization, causing lost updates or inconsistent reads.</p>
            <p><strong>Prevention Suite:</strong> Immutable objects (<code class="text-cyan-400 font-mono">records</code>), lock-free CAS primitives (<code class="text-cyan-400 font-mono">AtomicLong</code>, <code class="text-cyan-400 font-mono">LongAdder</code>), segment-locked collections (<code class="text-cyan-400 font-mono">ConcurrentHashMap</code>), timed locks (<code class="text-cyan-400 font-mono">ReentrantLock.tryLock</code>), and distributed monotonic fencing tokens.</p>
          </div>
        </details>

        <!-- Q8: SKU Latest State Stream Coding -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>8. Coding: Efficiently identify the latest state of each SKU from a large stream.</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Stream Architecture:</strong> Partition Kafka by <code class="text-cyan-400 font-mono">sku_id</code>; consume via stateful stream processor (Kafka Streams / Flink) backed by an in-memory RocksDB state store.</p>
            <pre class="bg-slate-950 p-2.5 rounded border border-slate-800 font-mono text-[10px] text-cyan-300 overflow-x-hidden">
stateStore.compute(incoming.getSkuId(), (sku, current) -> {
    if (current == null) return new SkuState(incoming);
    boolean isNewer = incoming.getSeq() > current.getSeq()
        || (incoming.getSeq() == current.getSeq() && incoming.getTs() > current.getTs());
    return isNewer ? new SkuState(incoming) : current; // drop stale out-of-order
});</pre>
            <p>Enable Kafka log compaction (<code class="text-cyan-400 font-mono">cleanup.policy=compact</code>) to automatically retain only the latest record per SKU indefinitely.</p>
          </div>
        </details>

        <!-- Q9: Duplicate Transactions at Scale -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>9. Coding: Find duplicate transactions efficiently from a large dataset.</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Real-Time Stream:</strong> Two-tier deduplication. Tier 1 fast-path distributed Bloom Filter for instant uniqueness. Tier 2 Redis Sorted Set window verification (<code class="text-cyan-400 font-mono">ZADD</code> with timestamp score, TTL 10m) to confirm matching transactions within &plusmn;5 minutes.</p>
            <p><strong>Batch Terabyte Scale (MapReduce / Spark):</strong> Hash-partition by <code class="text-cyan-400 font-mono">account_id</code> (guarantees candidate duplicates land on the same worker). Sort locally by timestamp in $O(M \log M)$, then execute a single-pass linear scan across the sliding 5-minute window in $O(M)$ time, avoiding $O(N^2)$ cross-joins.</p>
          </div>
        </details>

        <!-- Q10: Composition vs Inheritance -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>10. Difference between composition and inheritance? When do you prefer composition?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Inheritance ("is-a"):</strong> Compile-time tight coupling. Subclasses inherit parent internals; changes in base class risk breaking subclass invariants (Fragile Base Class problem).</p>
            <p><strong>Composition ("has-a"):</strong> Runtime loose coupling. Objects hold references to contracts/interfaces and delegate behavior.</p>
            <p><strong>Preference Criteria:</strong> Favor composition in 90%+ of systems designs to allow dynamic runtime strategy swapping, clean mockability in unit testing, and prevention of class explosion hierarchies.</p>
          </div>
        </details>

        <!-- Q11: Production Design Patterns & SOLID -->
        <details class="group bg-slate-900/80 rounded-xl border border-slate-800 p-3.5 transition-all">
          <summary class="font-mono font-bold text-xs text-cyan-300 cursor-pointer flex items-center justify-between">
            <span>11. Production design patterns? How do you design a system using SOLID principles?</span>
            <span class="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div class="mt-2.5 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-2">
            <p><strong>Production Patterns:</strong> Strategy (runtime protocol dispatching: NETCONF vs REST), Builder (40+ field 3GPP telemetry requests), Template Method (firmware upgrade lifecycle), Observer (YANG NRM change event dispatching).</p>
            <p><strong>SOLID in Order Processing Service:</strong></p>
            <ul class="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>S:</strong> Separate <code class="text-cyan-400 font-mono">OrderService</code> from <code class="text-cyan-400 font-mono">PaymentGateway</code>, <code class="text-cyan-400 font-mono">TaxCalculator</code>, and <code class="text-cyan-400 font-mono">NotificationService</code>.</li>
              <li><strong>O:</strong> Add new payment providers (ApplePay) by implementing <code class="text-cyan-400 font-mono">PaymentGateway</code> without modifying core service.</li>
              <li><strong>L:</strong> Any gateway implementation honors contract without throwing unexpected runtime exceptions.</li>
              <li><strong>I:</strong> Fine-grained interfaces (<code class="text-cyan-400 font-mono">OrderCreator</code>, <code class="text-cyan-400 font-mono">OrderCanceller</code>) over bloated 30-method interfaces.</li>
              <li><strong>D:</strong> High-level business services depend on abstract interfaces injected via Spring constructor injection.</li>
            </ul>
          </div>
        </details>

      </div>
    </div>
</section>
"""

STAGE_15_TRADEOFFS = """
<section id="stage-15" class="stage-section flex-1 flex flex-col overflow-hidden h-full" style="display: none;">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/40 font-mono">
          Stage 15 • Google Production Trade-Off Grid
        </span>
        <span class="text-xs text-slate-400">Architectural Decision Matrix</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google Staff Trade-Off & Invariant Matrix</h2>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
      <div class="overflow-x-auto no-scrollbar">
        <table class="w-full text-left font-mono text-[11px] border-collapse">
          <thead>
            <tr class="border-b border-slate-800 text-slate-400 bg-slate-900/60">
              <th class="p-3">DECISION AXIS</th>
              <th class="p-3 text-cyan-400">OPTION A</th>
              <th class="p-3 text-purple-400">OPTION B</th>
              <th class="p-3 text-emerald-400">GOOGLE STAFF SELECTION RULE</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60">
            <tr>
              <td class="p-3 font-bold text-white">Storage Engine</td>
              <td class="p-3">B-Tree (PostgreSQL)</td>
              <td class="p-3">LSM-Tree (ScyllaDB / RocksDB)</td>
              <td class="p-3 text-slate-300">Choose LSM for high-write ingest (>20k TPS) to eliminate random disk seeks via sequential append.</td>
            </tr>
            <tr>
              <td class="p-3 font-bold text-white">Consensus & Locking</td>
              <td class="p-3">Distributed Lock (Redis)</td>
              <td class="p-3">Monotonic Fencing Token</td>
              <td class="p-3 text-slate-300">Never rely on distributed lock TTL alone. Must attach 64-bit monotonic token verified at storage engine.</td>
            </tr>
            <tr>
              <td class="p-3 font-bold text-white">Cross-Region Consistency</td>
              <td class="p-3">Global Quorum (ALL)</td>
              <td class="p-3">LOCAL_QUORUM + Async Gossip</td>
              <td class="p-3 text-slate-300">Never execute cross-continental write quorums on hot path. Transatlantic fiber cuts take down writes globally.</td>
            </tr>
            <tr>
              <td class="p-3 font-bold text-white">Tail Latency Defense</td>
              <td class="p-3">Static Retry Loops</td>
              <td class="p-3">Hedged Requests (p95 threshold)</td>
              <td class="p-3 text-slate-300">Dispatch duplicate request at p95 mark. Shaves 65%+ off p99.9 with only 2% extra cluster overhead.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>
"""

STAGE_16_PAPERS = """
<section id="stage-16" class="stage-section flex-1 flex flex-col overflow-hidden h-full" style="display: none;">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800/40 font-mono">
          Stage 16 • Google Classic Systems Papers
        </span>
        <span class="text-xs text-slate-400">Foundational Distributed Systems Literature</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Classic Google Systems Papers & Interview Citations</h2>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <span class="text-cyan-400 font-bold font-mono text-sm block">1. Google Spanner (OSDI 2012)</span>
        <p class="text-slate-400">Corbett et al. — Globally Distributed Database with TrueTime API.</p>
        <p class="text-slate-300 font-mono text-[11px] bg-slate-900 p-2.5 rounded border border-slate-800">
          "Key Takeaway: TrueTime bounds clock drift uncertainty to &epsilon; &lt; 7ms using atomic clocks and GPS, enabling lock-free consistent read transactions across the globe."
        </p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <span class="text-amber-400 font-bold font-mono text-sm block">2. The Tail at Scale (CACM 2013)</span>
        <p class="text-slate-400">Dean & Barroso — Software Techniques for Taming Tail Latency.</p>
        <p class="text-slate-300 font-mono text-[11px] bg-slate-900 p-2.5 rounded border border-slate-800">
          "Key Takeaway: In fanout systems across 1,000 servers, 63% of user queries experience tail latency. Hedged requests cut p99.9 latency by over 60% with negligible server cost."
        </p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <span class="text-emerald-400 font-bold font-mono text-sm block">3. Maglev: A Fast and Reliable Software Network Load Balancer (NSDI 2016)</span>
        <p class="text-slate-400">Eisenbud et al. — Line-Rate Kernel Bypass Load Balancing.</p>
        <p class="text-slate-300 font-mono text-[11px] bg-slate-900 p-2.5 rounded border border-slate-800">
          "Key Takeaway: Consistent hashing lookup table combined with kernel-bypass packet processing sustains 100 Gbps wire rates per server with deterministic connection stickiness."
        </p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <span class="text-purple-400 font-bold font-mono text-sm block">4. Raft: In Search of an Understandable Consensus Algorithm (USENIX ATC 2014)</span>
        <p class="text-slate-400">Ongaro & Ousterhout — State Machine Replication.</p>
        <p class="text-slate-300 font-mono text-[11px] bg-slate-900 p-2.5 rounded border border-slate-800">
          "Key Takeaway: Decomposes consensus into leader election, log replication, and safety invariants. Randomized election timers eliminate split-vote livelocks."
        </p>
      </div>
    </div>
  </div>
</section>
"""

STAGE_17_EXAM = """
<section id="stage-17" class="stage-section flex-1 flex flex-col overflow-hidden h-full" style="display: none;">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-800/40 font-mono">
          Stage 17 • Final Evaluation
        </span>
        <span class="text-xs text-slate-400">Interactive Bar-Raiser Simulation</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google L6/L8 Staff Bar-Raiser Scenario Exam</h2>
    </div>
    <div class="flex items-center gap-2">
      <span id="exam-score" class="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/80 px-2.5 py-1 rounded border border-cyan-800/60">Score: 0 / 100</span>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
      <h4 class="text-sm font-bold text-white">Scenario 1: The Multi-Datacenter Asynchronous Lock Hazard</h4>
      <p>
        Your distributed workflow engine acquires a lock in Redis before updating a customer ledger in PostgreSQL. Redis master crashes and Sentinel promotes a replica before replication completes. A second worker acquires the same lock. How do you guarantee zero data corruption?
      </p>
      <div class="space-y-2 pt-2 font-mono">
        <label class="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900 border border-slate-800 cursor-pointer hover:border-slate-700">
          <input type="radio" name="q1" onchange="checkExamAnswer(1, 'A')" class="mt-0.5 text-cyan-500">
          <span>A) Increase Redis heartbeat timeouts to 30 seconds and enable appendonly fsync always.</span>
        </label>
        <label class="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900 border border-slate-800 cursor-pointer hover:border-slate-700">
          <input type="radio" name="q1" onchange="checkExamAnswer(1, 'B')" class="mt-0.5 text-cyan-500">
          <span>B) Issue a strictly monotonic 64-bit fencing token with each lock grant, and enforce a conditional update in PostgreSQL: UPDATE ... WHERE fencing_token &gt; last_committed_token.</span>
        </label>
        <label class="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900 border border-slate-800 cursor-pointer hover:border-slate-700">
          <input type="radio" name="q1" onchange="checkExamAnswer(1, 'C')" class="mt-0.5 text-cyan-500">
          <span>C) Wrap the Redis client in a distributed mutex retry loop with exponential backoff.</span>
        </label>
      </div>
      <div id="q1-feedback" class="hidden p-3 rounded-lg text-[11px] font-mono mt-2"></div>
    </div>
  </div>
</section>
"""

WHITEBOARD_MODAL_HTML = """
<div id="whiteboard-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-2 sm:p-4 hidden select-none">
  <div class="relative w-full h-full max-w-7xl bg-[#030611] border border-cyan-500/40 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
    
    <!-- Whiteboard Top Header -->
    <div class="h-12 shrink-0 bg-slate-950 border-b border-slate-800 px-4 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="text-base">🎨</span>
        <div>
          <span class="text-xs font-bold text-white font-mono uppercase tracking-wider">L6/L8 Architectural Whiteboard Studio</span>
          <span class="text-[9px] text-cyan-400 font-mono block">Freehand Vectors, Shapes & Interactive Stencils with 1-Click Delete [✕]</span>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="loadActiveModuleTopologyToWhiteboard()" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-semibold hover:bg-cyan-900">📐 Load Active Topology</button>
        <button onclick="verifyArchitectureScore()" class="px-2.5 py-1 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 text-xs font-semibold hover:bg-indigo-900">🤖 Verify Design</button>
        <button onclick="undoWhiteboard()" class="px-2.5 py-1 rounded bg-slate-900 text-slate-300 border border-slate-700 text-xs font-semibold hover:bg-slate-800">↩ Undo</button>
        <button onclick="clearWhiteboard()" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold hover:bg-rose-900">Clear Canvas</button>
        <button onclick="exportWhiteboardPng()" class="px-2.5 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow">📷 Export PNG</button>
        <button onclick="closeWhiteboardModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold">&times;</button>
      </div>
    </div>

    <!-- Whiteboard Toolbar -->
    <div class="h-11 shrink-0 bg-slate-900/90 border-b border-slate-800 px-4 flex flex-wrap items-center justify-between text-xs gap-2">
      <!-- Architecture Component Stencils & Archetypes -->
      <div class="flex items-center gap-1.5 overflow-x-auto py-1 px-1 bg-slate-950/70 rounded-lg border border-slate-800 text-[11px] font-mono">
        <span class="text-cyan-400 font-bold px-1 shrink-0">🏛️ Stencils:</span>
        <button onclick="addWhiteboardComponent('tower')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 shrink-0 transition-all">+ 🗼 Tower</button>
        <button onclick="addWhiteboardComponent('envoy')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 shrink-0 transition-all">+ 🛡️ Envoy LB</button>
        <button onclick="addWhiteboardComponent('gateway')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 shrink-0 transition-all">+ ⚡ Gateway</button>
        <button onclick="addWhiteboardComponent('kafka')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 shrink-0 transition-all">+ 🪵 Kafka</button>
        <button onclick="addWhiteboardComponent('redis')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-purple-300 border border-slate-700 shrink-0 transition-all">+ ⚡ Redis</button>
        <button onclick="addWhiteboardComponent('db')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 border border-slate-700 shrink-0 transition-all">+ 🗄️ ScyllaDB</button>
        <button onclick="addWhiteboardComponent('flink')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700 shrink-0 transition-all">+ 🌊 Flink</button>
        <span class="border-l border-slate-700 h-4 mx-1 shrink-0"></span>
        <span class="text-purple-400 font-bold px-1 shrink-0">⚡ Archetypes:</span>
        <button onclick="loadArchitectureArchetype('telemetry')" class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 shrink-0 transition-all">Ingestion</button>
        <button onclick="loadArchitectureArchetype('fencing')" class="px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 hover:bg-purple-900 shrink-0 transition-all">Fencing Lock</button>
        <button onclick="loadArchitectureArchetype('spanner')" class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 hover:bg-emerald-900 shrink-0 transition-all">Spanner TrueTime</button>
      </div>

      <!-- Drawing Tools -->
      <div class="flex items-center gap-1">
        <button onclick="setWbTool('pen')" id="wb-tool-pen" class="wb-tool active px-2.5 py-1 rounded bg-slate-800 text-white border border-slate-700 text-[11px]">✏️ Pen</button>
        <button onclick="setWbTool('arrow')" id="wb-tool-arrow" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">➡️ Arrow</button>
        <button onclick="setWbTool('rect')" id="wb-tool-rect" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">▭ Box</button>
        <button onclick="setWbTool('circle')" id="wb-tool-circle" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">◯ Circle</button>
        <button onclick="setWbTool('eraser')" id="wb-tool-eraser" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">🧹 Eraser</button>
      </div>

      <!-- Color Palette -->
      <div class="flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-950 border border-slate-800">
        <button onclick="setWbColor('#00f0ff')" class="w-4 h-4 rounded-full bg-[#00f0ff] border border-white/40 shadow-sm" title="Electric Cyan"></button>
        <button onclick="setWbColor('#10b981')" class="w-4 h-4 rounded-full bg-[#10b981] border border-white/40 shadow-sm" title="Neon Emerald"></button>
        <button onclick="setWbColor('#c084fc')" class="w-4 h-4 rounded-full bg-[#c084fc] border border-white/40 shadow-sm" title="Vivid Purple"></button>
        <button onclick="setWbColor('#f59e0b')" class="w-4 h-4 rounded-full bg-[#f59e0b] border border-white/40 shadow-sm" title="Amber"></button>
        <button onclick="setWbColor('#f43f5e')" class="w-4 h-4 rounded-full bg-[#f43f5e] border border-white/40 shadow-sm" title="Rose Red"></button>
        <button onclick="setWbColor('#ffffff')" class="w-4 h-4 rounded-full bg-[#ffffff] border border-white/40 shadow-sm" title="Crisp White"></button>
      </div>

      <!-- Stencils -->
      <div class="flex flex-wrap items-center gap-1.5">
        <span class="text-[10px] text-slate-400 uppercase font-mono mr-1">Add Stencil:</span>
        <button onclick="addStencil('gateway')" class="px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 text-[10px]">+ Gateway</button>
        <button onclick="addStencil('kafka')" class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]">+ Kafka</button>
        <button onclick="addStencil('scylla')" class="px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 text-[10px]">+ Scylla</button>
        <button onclick="addStencil('redis')" class="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 text-[10px]">+ Redis</button>
        <button onclick="addStencil('flink')" class="px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800 text-[10px]">+ Flink</button>
        <button onclick="addStencil('pod')" class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px]">+ Pod</button>
      </div>
    </div>

    <!-- Whiteboard Canvas Viewport -->
    <div id="modal-whiteboard-viewport" class="relative flex-1 bg-[#030611] overflow-hidden">
      <canvas id="modal-whiteboard-canvas" class="w-full h-full cursor-crosshair block absolute inset-0 z-0"></canvas>
      <div id="modal-whiteboard-nodes" class="absolute inset-0 pointer-events-none z-10 overflow-hidden"></div>
    </div>
  </div>
</div>
"""
