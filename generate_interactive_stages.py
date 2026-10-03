# generate_interactive_stages.py
# Generates rich interactive stages 13 to 17 and Whiteboard components for interactive_stages_data.py

content = '''# interactive_stages_data.py
# Interactive sections for Stages 13, 14, 15, 16, 17 and Global Whiteboard Modal

STAGE_13_SIMULATORS = """
<section id="stage-13" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
          Stage 13 • Advanced Distributed Systems Physics Lab
        </span>
        <span class="text-xs text-slate-400">8 Real-Time Interactive Simulators</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Distributed Systems Execution & Hardware Physics Simulators</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch13-check" onchange="toggleChapter('ch13')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <!-- Tabbed Simulator Switcher -->
  <div class="shrink-0 px-6 bg-[#050917] border-b border-white/[0.08] flex gap-1 overflow-x-auto text-xs py-1" id="sim-tabs">
    <button onclick="switchSim('sim-zerocopy')" id="tab-sim-zerocopy" class="tab-btn active px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">⚡ 1. Zero-Copy I/O</button>
    <button onclick="switchSim('sim-raft')" id="tab-sim-raft" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🗳️ 2. Raft Consensus</button>
    <button onclick="switchSim('sim-hashring')" id="tab-sim-hashring" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🎯 3. Consistent Hash Ring</button>
    <button onclick="switchSim('sim-tokenbucket')" id="tab-sim-tokenbucket" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🚰 4. GCRA Token Bucket</button>
    <button onclick="switchSim('sim-fencing')" id="tab-sim-fencing" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🔒 5. Monotonic Fencing</button>
    <button onclick="switchSim('sim-tail')" id="tab-sim-tail" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">📈 6. Tail at Scale Amplification</button>
    <button onclick="switchSim('sim-lsm')" id="tab-sim-lsm" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🧱 7. LSM Compaction</button>
    <button onclick="switchSim('sim-cte')" id="tab-sim-cte" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🌳 8. 3GPP CTE Tree</button>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6">
    
    <!-- LAB 1: ZERO-COPY -->
    <div id="sim-zerocopy" class="sim-panel space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Linux Kernel Zero-Copy vs Traditional 4-Copy Memory Pipeline</h4>
            <p class="text-[11px] text-slate-400">Simulate packet flow from NVMe disk through PageCache, User-space heap, socket buffers, and NIC DMA rings.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="setZeroCopyMode('traditional')" id="btn-mode-trad" class="px-3 py-1 rounded-lg text-xs font-semibold bg-rose-950 text-rose-300 border border-rose-800">Traditional (4 Copies, 4 Context Switches)</button>
            <button onclick="setZeroCopyMode('zerocopy')" id="btn-mode-zero" class="px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800">Zero-Copy sendfile() (0 CPU Copies)</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-64 flex flex-col justify-between overflow-hidden">
          <canvas id="zc-canvas" class="w-full h-full block"></canvas>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block">CPU Copies per Packet:</span>
            <span id="zc-stat-cpu-copies" class="font-bold text-rose-400 text-sm">2 Copies</span>
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
            <span class="text-[10px] text-slate-400 block">Effective Throughput:</span>
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
            <p class="text-[11px] text-slate-400">Simulate a 5-node distributed cluster. Trigger network partitions, vote requests, log quorum commits, and split-brain resolution.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="raftPartitionLeader()" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold">⚡ Partition Leader</button>
            <button onclick="raftHealNetwork()" class="px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs font-semibold">🩺 Heal Network</button>
            <button onclick="raftSubmitTx()" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-semibold">📝 Submit Write Tx</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center">
          <canvas id="raft-canvas" class="w-full h-full block"></canvas>
        </div>

        <div id="raft-log-status" class="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-[11px] text-slate-300">
          Cluster Status: 5 Nodes Operational | Term: 1 | Leader: Node 1 | Quorum: 3/5 Required | Committed Index: 104
        </div>
      </div>
    </div>

    <!-- LAB 3: CONSISTENT HASH RING -->
    <div id="sim-hashring" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Consistent Hash Ring with Virtual Nodes (V-Nodes)</h4>
            <p class="text-[11px] text-slate-400">Observe how virtual nodes eliminate hot spotting and reduce standard deviation across Cassandra/Scylla partitions.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="setVNodes(1)" class="px-2.5 py-1 rounded bg-slate-900 text-slate-300 border border-slate-700 text-xs">V=1 (Naive)</button>
            <button onclick="setVNodes(50)" class="px-2.5 py-1 rounded bg-slate-900 text-slate-300 border border-slate-700 text-xs">V=50</button>
            <button onclick="setVNodes(150)" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-bold">V=150 (Production)</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-72 flex items-center justify-center">
          <canvas id="hash-canvas" class="w-full h-full block"></canvas>
        </div>
      </div>
    </div>

    <!-- LAB 4: TOKEN BUCKET -->
    <div id="sim-tokenbucket" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Dual Rate Limiter: Token Bucket vs Leaky Bucket (GCRA)</h4>
            <p class="text-[11px] text-slate-400">Simulate burst arrivals and observe how GCRA calculates theoretical arrival times to smooth traffic.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="injectBurst(50)" class="px-3 py-1 rounded bg-amber-950 text-amber-300 border border-amber-800 text-xs font-bold">+50 Burst Requests</button>
          </div>
        </div>

        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-64 flex items-center justify-center">
          <canvas id="tb-canvas" class="w-full h-full block"></canvas>
        </div>
      </div>
    </div>

    <!-- LAB 5: MONOTONIC FENCING -->
    <div id="sim-fencing" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <h4 class="text-sm font-bold text-white">Martin Kleppmann GC Pause & Monotonic Fencing Simulator</h4>
        <p class="text-[11px] text-slate-400">Simulate Client 1 entering a 15-second GC pause while Client 2 acquires lease. Watch the downstream database reject Client 1's stale commit.</p>
        <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-purple-300">
          Status: Monotonic Token Counter = 1048. Conditional UPDATE WHERE last_token &lt; incoming_token ensures 100% split-brain immunity.
        </div>
      </div>
    </div>

    <!-- LAB 6: TAIL AT SCALE -->
    <div id="sim-tail" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <h4 class="text-sm font-bold text-white">Jeff Dean Tail Latency Amplification Simulator</h4>
        <p class="text-[11px] text-slate-400">Calculate tail latency across 1 to 1,000 fanout microservices: P(overall &gt; 1s) = 1 - (1 - p)^N.</p>
        <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-cyan-300">
          N = 100 Sub-services: 63.4% of all user requests experience &gt;1s tail latency!<br>
          With Hedged Requests (95th percentile delay): Tail latency drops by 82% with only 3.8% additional network load.
        </div>
      </div>
    </div>

    <!-- LAB 7: LSM COMPACTION -->
    <div id="sim-lsm" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <h4 class="text-sm font-bold text-white">LSM-Tree MemTable Flush & Leveled Compaction Lab</h4>
        <p class="text-[11px] text-slate-400">Simulate MemTable flush to L0 SSTables and observe write amplification vs read amplification trade-offs.</p>
        <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-emerald-300">
          L0: 4 SSTables (Uncompacted) &rarr; L1: 10 MB (Key ranges partitioned) &rarr; L2: 100 MB. Bloom filters eliminate 99% of unnecessary disk seeks!
        </div>
      </div>
    </div>

    <!-- LAB 8: CTE TREE -->
    <div id="sim-cte" class="sim-panel hidden space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <h4 class="text-sm font-bold text-white">3GPP CTE Hierarchical Rule Evaluation & Quota Reservation</h4>
        <div class="p-3 bg-slate-900 rounded-lg font-mono text-[11px] text-slate-300">
          Traverse multi-tier rating hierarchies: Subscriber Tier &rarr; Rating Group &rarr; Service ID &rarr; Tariff Table with sub-millisecond evaluation.
        </div>
      </div>
    </div>

  </div>
</section>
"""

STAGE_14_LEADERSHIP = """
<section id="stage-14" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
          Stage 14 • Google Staff & Principal Leadership Playbook
        </span>
        <span class="text-xs text-slate-400">GCA, Googleyness & Staff Multiplier</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google L6/L8 Staff Leadership STAR Playbook</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch14-check" onchange="toggleChapter('ch14')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-2">
      <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">Google 4-Pillar Evaluation Rubric for Staff Engineers</span>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-[11px] pt-1">
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
        <span class="font-bold text-emerald-400 block border-b border-slate-800 pb-1.5">1. Resolving Cross-Org Architectural Deadlock</span>
        <p><strong>Situation:</strong> Gateway team demanded synchronous REST/HTTP with client-side polling, while Backend team advocated for Kafka event streams. 3 weeks from delivery slip.</p>
        <p><strong>Task:</strong> Align both teams without executive mandate to prevent a 6-month slip.</p>
        <p><strong>Action:</strong> Built benchmark prototype comparing 10k concurrent HTTP sockets vs Kafka zero-copy throughput. Held open RFC review addressing debugging concerns via Protobuf schemas.</p>
        <p><strong>Result:</strong> Gateway team unanimously adopted Kafka event model. Shipped on schedule with 99.999% availability.</p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <span class="font-bold text-rose-400 block border-b border-slate-800 pb-1.5">2. Incident Command: Nationwide Outage & Blameless RCA</span>
        <p><strong>Situation:</strong> Rebalance storm locked out 20M cell tower parameters during peak traffic rollout.</p>
        <p><strong>Task:</strong> Lead incident command room, halt cascading failure, and conduct blameless post-mortem.</p>
        <p><strong>Action:</strong> Canary rollback in 3 minutes. Led RCA discovering Eager rebalance caused global freeze and lack of fencing caused state corruption. Implemented Cooperative Sticky assignor and monotonic tokens.</p>
        <p><strong>Result:</strong> Zero repeat occurrences; rebalance pauses dropped from 14s to 400ms.</p>
      </div>
    </div>
  </div>
</section>
"""

STAGE_15_TRADEOFFS = """
<section id="stage-15" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/40">
          Stage 15 • Macro System Design Cheatsheet
        </span>
        <span class="text-xs text-slate-400">Master Trade-Off Matrix</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Distributed Architecture Master Trade-Off Grid</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch15-check" onchange="toggleChapter('ch15')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs">
    <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-950">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-slate-800 text-slate-400 bg-slate-900/60 text-[11px]">
            <th class="py-3 px-4 font-semibold">Category</th>
            <th class="py-3 px-4 font-semibold">Options Compared</th>
            <th class="py-3 px-4 font-semibold">Primary Trade-Off & Bottleneck</th>
            <th class="py-3 px-4 font-semibold">Google L6/L8 Decision Heuristic</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60 font-mono text-[11px]">
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">Storage Engines</td>
            <td class="py-3 px-4 text-cyan-400">B-Tree vs LSM-Tree</td>
            <td class="py-3 px-4 text-slate-300 font-sans">B-Tree: Low-latency point reads; random I/O write degradation.<br>LSM: Blazing sequential writes; read/compaction amplification.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">LSM for write-heavy ingestion logs (&gt;10k TPS); B-Tree for multi-table relational ACID queries.</td>
          </tr>
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">Consensus</td>
            <td class="py-3 px-4 text-purple-400">Raft / Paxos vs 2PC</td>
            <td class="py-3 px-4 text-slate-300 font-sans">2PC is blocking on coordinator crash.<br>Raft/Paxos: Non-blocking as long as majority quorum survives.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">Never use 2PC across wide-area networks; use Raft for leader leases and replication.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
"""

STAGE_16_PAPERS = """
<section id="stage-16" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-800/40">
          Stage 16 • Canonical Google Distributed Systems Research
        </span>
        <span class="text-xs text-slate-400">The 8 Foundational Papers</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google Systems Engineering Research Pack</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch16-check" onchange="toggleChapter('ch16')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">1. Google Spanner (OSDI '12)</span>
          <span class="text-[10px] text-indigo-400 font-mono">External Consistency</span>
        </div>
        <p><strong>Core Thesis:</strong> Spanner provides external consistency (linearizability) across global datacenters without global locks via the TrueTime API.</p>
      </div>

      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">2. The Tail at Scale (Dean & Barroso, 2013)</span>
          <span class="text-[10px] text-indigo-400 font-mono">CACM Classic</span>
        </div>
        <p><strong>Core Thesis:</strong> In a 1,000-service fan-out architecture, tail latency dominates. Hedged requests cut p99.9 latency by 80% with &lt;5% load.</p>
      </div>
    </div>
  </div>
</section>
"""

STAGE_17_EXAM = """
<section id="stage-17" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-800/40">
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

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
      <h4 class="text-sm font-bold text-white">Scenario 1: The Multi-Datacenter Asynchronous Lock Hazard</h4>
      <p>
        Your distributed workflow engine acquires a lock in Redis before updating a customer ledger in PostgreSQL. Redis master crashes and Sentinel promotes a replica before replication completes. A second worker acquires the same lock. How do you guarantee zero data corruption?
      </p>
      <div class="space-y-2 pt-2">
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
        <span class="text-xs font-bold text-white font-mono uppercase tracking-wider">L6/L8 Architectural Whiteboard Studio</span>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="undoWhiteboard()" class="px-2.5 py-1 rounded bg-slate-900 text-slate-300 border border-slate-700 text-xs font-semibold hover:bg-slate-800">↩ Undo</button>
        <button onclick="clearWhiteboard()" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold hover:bg-rose-900">Clear Canvas</button>
        <button onclick="exportWhiteboardPng()" class="px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-semibold hover:bg-cyan-900">📷 Export PNG</button>
        <button onclick="closeWhiteboardModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold">&times;</button>
      </div>
    </div>

    <!-- Whiteboard Toolbar -->
    <div class="h-10 shrink-0 bg-slate-900/80 border-b border-slate-800 px-4 flex items-center justify-between text-xs gap-2">
      <div class="flex items-center gap-1">
        <button onclick="setWbTool('pen')" id="wb-tool-pen" class="wb-tool active px-2.5 py-1 rounded bg-slate-800 text-white border border-slate-700 text-[11px]">✏️ Pen</button>
        <button onclick="setWbTool('arrow')" id="wb-tool-arrow" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">➡️ Arrow</button>
        <button onclick="setWbTool('rect')" id="wb-tool-rect" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">▭ Box</button>
        <button onclick="setWbTool('circle')" id="wb-tool-circle" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">◯ Circle</button>
        <button onclick="setWbTool('eraser')" id="wb-tool-eraser" class="wb-tool px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">🧹 Eraser</button>
      </div>

      <div class="flex items-center gap-1">
        <span class="text-[10px] text-slate-400 uppercase font-mono mr-1">Stencils:</span>
        <button onclick="addStencil('gateway')" class="px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 text-[10px]">+ Gateway</button>
        <button onclick="addStencil('kafka')" class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]">+ Kafka</button>
        <button onclick="addStencil('redis')" class="px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 text-[10px]">+ Redis</button>
        <button onclick="addStencil('scylla')" class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[10px]">+ ScyllaDB</button>
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
'''

with open("d:/Antigravity/interactive_stages_data.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated interactive_stages_data.py successfully!")
