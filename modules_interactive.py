# modules_interactive.py
# High-density interactive study materials for Stages 8, 9, 10, 11, 12 and Whiteboard Modal

STAGE_8_SIMULATORS = """
<section id="stage-8" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
          Stage 8 • Interactive Physics & Architecture Lab
        </span>
        <span class="text-xs text-slate-400">5 Advanced Distributed Systems Simulators</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Distributed Systems Execution & Mechanics Simulators</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch8-check" onchange="toggleChapter('ch8')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <!-- Tabbed Simulator Switcher -->
  <div class="shrink-0 px-6 bg-[#050917] border-b border-white/[0.08] flex gap-1 overflow-x-auto text-xs py-1" id="sim-tabs">
    <button onclick="switchSim('sim-zerocopy')" id="tab-sim-zerocopy" class="tab-btn active px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">⚡ 1. Zero-Copy vs 4-Copy Packet Flow</button>
    <button onclick="switchSim('sim-raft')" id="tab-sim-raft" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🗳️ 2. Raft Distributed Consensus Cluster</button>
    <button onclick="switchSim('sim-hashring')" id="tab-sim-hashring" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🎯 3. Consistent Hashing & Virtual Nodes</button>
    <button onclick="switchSim('sim-tokenbucket')" id="tab-sim-tokenbucket" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🚰 4. Dual Token / Leaky Bucket Limiter</button>
    <button onclick="switchSim('sim-cte')" id="tab-sim-cte" class="tab-btn px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🌳 5. 3GPP CTE Charging Tree</button>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6">
    
    <!-- SIMULATOR 1: ZERO-COPY -->
    <div id="sim-zerocopy" class="sim-panel space-y-4">
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-white">Linux Kernel Zero-Copy vs Traditional 4-Copy Pipeline</h4>
            <p class="text-[11px] text-slate-400">Simulate packet flow from NVMe disk through PageCache, User-space heap, socket buffers, and NIC DMA rings.</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="setZeroCopyMode('traditional')" id="btn-mode-trad" class="px-3 py-1 rounded-lg text-xs font-semibold bg-rose-950 text-rose-300 border border-rose-800">Traditional (4 Copies, 4 Context Switches)</button>
            <button onclick="setZeroCopyMode('zerocopy')" id="btn-mode-zero" class="px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800">Zero-Copy sendfile() (0 CPU Copies)</button>
          </div>
        </div>

        <!-- Visual Canvas -->
        <div class="relative bg-[#020512] rounded-xl border border-slate-800 p-4 h-64 flex flex-col justify-between overflow-hidden">
          <canvas id="zc-canvas" class="w-full h-full block"></canvas>
        </div>

        <!-- Metrics Dashboard -->
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

    <!-- SIMULATOR 2: RAFT CONSENSUS -->
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

    <!-- SIMULATOR 3: CONSISTENT HASH RING -->
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

    <!-- SIMULATOR 4: TOKEN BUCKET -->
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

    <!-- SIMULATOR 5: CTE CHARGING TREE -->
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

STAGE_9_LEADERSHIP = """
<section id="stage-9" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
          Stage 9 • Google Staff & Principal Leadership Playbook
        </span>
        <span class="text-xs text-slate-400">GCA, Googleyness & Staff Multiplier</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google L6/L8 Staff Leadership STAR Playbook</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch9-check" onchange="toggleChapter('ch9')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    
    <!-- Google Hiring Rubric Overview -->
    <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-2">
      <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">Google 4-Pillar Evaluation Rubric for Staff Engineers</span>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-[11px] pt-1">
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">1. GCA (General Cognitive Ability):</strong>
          <span class="text-slate-400">Structured problem solving under ambiguity; decomposing ill-defined problems with first-principles reasoning.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">2. Role-Related Knowledge:</strong>
          <span class="text-slate-400">Mastery of kernel physics, distributed state, failure domains, and hardware bottlenecks.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">3. Leadership & Multiplier:</strong>
          <span class="text-slate-400">Leading without authority; unblocking cross-functional teams; sponsoring and leveling up senior engineers.</span>
        </div>
        <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800">
          <strong class="text-white block mb-0.5">4. Googleyness:</strong>
          <span class="text-slate-400">Intellectual humility, doing the right thing for users, thriving in ambiguity, and blameless post-mortem culture.</span>
        </div>
      </div>
    </div>

    <!-- STAR SCENARIOS GRID -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      
      <!-- SCENARIO 1 -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2">
          <span class="font-bold text-emerald-400">1. Resolving Cross-Org Architectural Deadlock</span>
          <span class="text-[9px] bg-emerald-950 px-1.5 py-0.5 rounded font-mono text-emerald-300">Staff Alignment</span>
        </div>
        <p><strong>Situation:</strong> During nationwide 5G rollout, the Gateway team demanded synchronous REST/HTTP with heavy client-side polling, while my Backend team advocated for an asynchronous Kafka event-driven pipeline. Delivery was 3 weeks from stalling.</p>
        <p><strong>Task:</strong> As Lead Architect, resolve the deadlock without escalating to executive mandate, establishing cross-team technical consensus.</p>
        <p><strong>Action:</strong> Built a data-backed benchmark harness simulating 10k concurrent cell connections. Demonstrated that REST connection pools exhausted Linux file descriptors and increased p99 latency to 1,200ms. Created an RFC showing Kafka zero-copy ingress sustained 45k TPS at 42ms p99. Hosted an open design review addressing their debugging and schema validation concerns by introducing Protobuf contracts with backward compatibility.</p>
        <p><strong>Result:</strong> Gateway team unanimously adopted the Kafka event model. We shipped on schedule with zero socket starvation incidents and 99.999% availability.</p>
      </div>

      <!-- SCENARIO 2 -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2">
          <span class="font-bold text-rose-400">2. Crisis Command: Nationwide Outage & Blameless RCA</span>
          <span class="text-[9px] bg-rose-950 px-1.5 py-0.5 rounded font-mono text-rose-300">SRE Crisis Command</span>
        </div>
        <p><strong>Situation:</strong> A nationwide configuration rollout triggered a consumer group rebalance storm, locking out 20M cell tower parameters during peak traffic.</p>
        <p><strong>Task:</strong> Assume Incident Commander role, halt the cascading failure, restore service under strict SLA, and conduct a transparent blameless post-mortem.</p>
        <p><strong>Action:</strong> Rolled back deployment via automated canary within 3 minutes. Led incident command room, establishing clear communication cadence. Conducted a blameless post-mortem identifying that the legacy Eager Rebalance protocol caused nationwide partition freezes and absence of downstream fencing allowed stale writes. Architected the migration to Cooperative Sticky Rebalance and implemented monotonic fencing tokens.</p>
        <p><strong>Result:</strong> Zero repeat occurrences; rebalance pauses dropped from 14s to 400ms. Instituted multi-window burn rate alerts across the entire USM engineering organization.</p>
      </div>

      <!-- SCENARIO 3 -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2">
          <span class="font-bold text-blue-400">3. Mentorship & The Staff+ Multiplier Effect</span>
          <span class="text-[9px] bg-blue-950 px-1.5 py-0.5 rounded font-mono text-blue-300">Leveling L5 to L6</span>
        </div>
        <p><strong>Situation:</strong> Senior (L5) engineers were delivering functional code but repeatedly missing distributed edge cases (race conditions, memory leaks, missing idempotency).</p>
        <p><strong>Task:</strong> Elevate the technical rigor of 4 Senior Engineers to take independent ownership of distributed sub-modules.</p>
        <p><strong>Action:</strong> Instituted weekly Architecture Dissections analyzing real production crash dumps, profiling Linux PageCache dirty pages, and modeling failure domains with Jepsen tests. Created an RFC template requiring explicit failure mode analysis before any code was written.</p>
        <p><strong>Result:</strong> 2 engineers promoted to Tech Leads within 12 months; production defect escapes dropped by 25% across the division.</p>
      </div>

      <!-- SCENARIO 4 -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2.5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2">
          <span class="font-bold text-amber-400">4. Pushing Back on VP Deadlines for Reliability</span>
          <span class="text-[9px] bg-amber-950 px-1.5 py-0.5 rounded font-mono text-amber-300">Executive Pushback</span>
        </div>
        <p><strong>Situation:</strong> Executive leadership pressed to cut corner on shadow traffic verification to ship the database migration 2 months early.</p>
        <p><strong>Task:</strong> Defend engineering rigor and system durability without being perceived as an obstructionist.</p>
        <p><strong>Action:</strong> Framed the risk in terms of customer revenue and regulatory penalties: demonstrated that 0.01% unverified divergence in 500M records translates to 50,000 corrupt subscriber accounts. Proposed a compromised parallelized shadow testing plan using synthetic traffic generators that compressed verification from 8 weeks to 3 weeks while maintaining 100% parity proof.</p>
        <p><strong>Result:</strong> Shipped migration with zero data loss and received commendation from the VP for protecting carrier SLA commitments.</p>
      </div>

    </div>
  </div>
</section>
"""

STAGE_10_TRADEOFFS = """
<section id="stage-10" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/40">
          Stage 10 • Macro System Design Cheatsheet
        </span>
        <span class="text-xs text-slate-400">Master Trade-Off Matrix</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Distributed Architecture Master Trade-Off Grid</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch10-check" onchange="toggleChapter('ch10')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
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
            <td class="py-3 px-4 text-cyan-400">B-Tree (Postgres/InnoDB) vs LSM-Tree (RocksDB/Cassandra)</td>
            <td class="py-3 px-4 text-slate-300 font-sans">B-Tree: Low-latency point reads; random I/O write degradation.<br>LSM: Blazing sequential writes; read/compaction amplification.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">LSM for write-heavy ingestion logs (&gt;10k TPS); B-Tree for multi-table relational ACID queries.</td>
          </tr>
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">Consensus Models</td>
            <td class="py-3 px-4 text-purple-400">Raft / Paxos vs 2-Phase Commit (2PC)</td>
            <td class="py-3 px-4 text-slate-300 font-sans">2PC is a blocking protocol: coordinator crash blocks all locks.<br>Raft/Paxos: Non-blocking as long as majority quorum (N/2 + 1) survives.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">Never use 2PC across wide-area networks; use Raft for leader leases and state machine replication.</td>
          </tr>
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">I/O Concurrency</td>
            <td class="py-3 px-4 text-blue-400">epoll Event Loop vs Thread-per-Core (Seastar) vs Loom Virtual Threads</td>
            <td class="py-3 px-4 text-slate-300 font-sans">epoll: Single-thread head-of-line blocking.<br>Seastar: Zero locks, pinned to NUMA; complex async coding.<br>Loom: Synchronous code style with lightweight user-space scheduling.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">Thread-per-core for sub-millisecond C++ storage engines; Virtual Threads for Java I/O web fleets.</td>
          </tr>
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">Replication</td>
            <td class="py-3 px-4 text-amber-400">Sync 2PC vs Tunable Quorum (LOCAL_QUORUM)</td>
            <td class="py-3 px-4 text-slate-300 font-sans">Sync: 120ms transatlantic speed-of-light delay; link cut halts writes.<br>LOCAL_QUORUM: 4ms local write; async cross-region replication.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">LOCAL_QUORUM is mandatory for multi-region systems requiring high availability and low latency.</td>
          </tr>
          <tr>
            <td class="py-3 px-4 text-white font-sans font-bold">Communication</td>
            <td class="py-3 px-4 text-rose-400">gRPC/Protobuf vs REST/JSON vs Aeron IPC</td>
            <td class="py-3 px-4 text-slate-300 font-sans">REST: Human-readable but heavy CPU serialization and text overhead.<br>gRPC: Binary Protobuf over HTTP/2.<br>Aeron: Shared-memory zero-copy IPC.</td>
            <td class="py-3 px-4 text-emerald-400 font-sans">Aeron IPC for same-host ultra-low latency (&lt;1us); gRPC for internal service mesh; REST for external browsers.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
"""

STAGE_11_PAPERS = """
<section id="stage-11" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-800/40">
          Stage 11 • Canonical Google Distributed Systems Research
        </span>
        <span class="text-xs text-slate-400">The 8 Foundational Papers</span>
      </div>
      <h2 class="text-base font-bold text-white mt-0.5">Google Systems Engineering Research Pack</h2>
    </div>
    <div class="flex items-center gap-2">
      <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
        <input type="checkbox" id="ch11-check" onchange="toggleChapter('ch11')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
        <span>Mastered</span>
      </label>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6 text-xs text-slate-300 leading-relaxed">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      
      <!-- PAPER 1: SPANNER -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">1. Google Spanner (OSDI '12)</span>
          <span class="text-[10px] text-indigo-400 font-mono">External Consistency</span>
        </div>
        <p><strong>Core Thesis:</strong> Spanner is Google's globally distributed database providing external consistency (linearizability) across global datacenters without global locks.</p>
        <p><strong>Breakthrough:</strong> The <strong>TrueTime API</strong> exposes clock uncertainty explicitly as an interval <code class="text-indigo-300 font-mono">[earliest, latest]</code> using GPS receivers and atomic clocks. By waiting out the clock uncertainty bound (&epsilon; &lt; 7ms), Spanner ensures commit timestamps reflect true causal order across continents.</p>
        <p class="text-slate-400 font-mono text-[11px]">Interview Citation: "Spanner proves that linearizable ACID transactions across datacenters are possible if clock uncertainty is bounded via hardware TrueTime."</p>
      </div>

      <!-- PAPER 2: TAIL AT SCALE -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">2. The Tail at Scale (Dean & Barroso, 2013)</span>
          <span class="text-[10px] text-indigo-400 font-mono">CACM Classic</span>
        </div>
        <p><strong>Core Thesis:</strong> In a fan-out architecture where a single query touches 1,000 sub-services, if each service has a 99th percentile latency of 1 second, 99.99% of user requests will take over 1 second! The tail dominates user experience.</p>
        <p><strong>Breakthrough:</strong> <strong>Hedged Requests</strong>: send a duplicate request to a secondary replica after the 95th percentile latency threshold elapses. This cuts p99.9 latency by 80% while adding less than 5% overall request load.</p>
        <p class="text-slate-400 font-mono text-[11px]">Interview Citation: "To tame tail latency in fan-out microservices, we implement hedged requests with delayed cancellation and tied requests."</p>
      </div>

      <!-- PAPER 3: BORG -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">3. Google Borg (EuroSys '15)</span>
          <span class="text-[10px] text-indigo-400 font-mono">Cluster Scheduling</span>
        </div>
        <p><strong>Core Thesis:</strong> The architectural predecessor to Kubernetes. Borg manages millions of tasks across tens of thousands of machines.</p>
        <p><strong>Breakthrough:</strong> Priority classes (Production vs Non-Production Batch), admission control, quota management, and declarative cell specification with Linux cgroups resource isolation.</p>
        <p class="text-slate-400 font-mono text-[11px]">Interview Citation: "Borg established that overcommitting resources through priority preemption is the only way to achieve high datacenter server utilization."</p>
      </div>

      <!-- PAPER 4: CHUBBY -->
      <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
        <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
          <span class="font-bold text-white">4. The Chubby Lock Service (OSDI '06)</span>
          <span class="text-[10px] text-indigo-400 font-mono">Distributed Locking</span>
        </div>
        <p><strong>Core Thesis:</strong> Provides coarse-grained locking and consensus for loosely-coupled distributed systems (used by GFS and Bigtable to elect leaders).</p>
        <p><strong>Breakthrough:</strong> Coarse-grained locking (locks held for hours/days), epoch numbers for monotonic fencing, event notifications to avoid client polling, and Paxos consensus.</p>
        <p class="text-slate-400 font-mono text-[11px]">Interview Citation: "Chubby demonstrated that distributed locks must issue epoch sequence numbers to prevent delayed network packets from corrupting state."</p>
      </div>

    </div>
  </div>
</section>
"""

STAGE_12_EXAM = """
<section id="stage-12" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
  <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] font-bold uppercase tracking-wider text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-800/40">
          Stage 12 • Final Evaluation
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
        <span class="text-xs font-bold text-white font-mono uppercase tracking-wider">L6 Architectural Whiteboard Studio</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="clearWhiteboard()" class="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold hover:bg-rose-900">Clear Canvas</button>
        <button onclick="closeWhiteboardModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold">&times;</button>
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
