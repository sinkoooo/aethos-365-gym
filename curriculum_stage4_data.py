# curriculum_stage4_data.py
# Stage 4: Senior to Staff - Consistency Models, PACELC & Distributed Transactions

STAGE_4_CHAPTERS = [
    {
        "id": "c-08-cap-pacelc-deep",
        "stageId": "stage-4",
        "stageNum": "STAGE 04",
        "badge": "Senior / Staff",
        "color": "amber",
        "title": "4.1 Beyond Textbook CAP: Abadi's PACELC Theorem & Consistency Models",
        "difficulty": "Senior to Staff",
        "readTime": "25 min read",
        "simulatorKey": "interview",
        "summary": "Why Eric Brewer's CAP is outdated. Daniel Abadi's PACELC theorem, Quorum mathematics (R + W > N), Linearizability vs Causal consistency, and Dynamo vs Spanner trade-offs.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/20 text-amber-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-amber-400 mb-1">First-Principles Intuition</div>
    Most engineers memorize the textbook <strong>CAP Theorem</strong>: "Pick two of Consistency, Availability, Partition Tolerance".
    <br><br>
    The fatal flaw: <strong>Network Partitions ($P$) are rare</strong> (happening &lt; 0.1% of the time in modern cloud data centers).
    What trade-off does your system make during the remaining 99.9% of normal healthy runtime ($E$ - Else)?
    <br><br>
    That is <strong>Daniel Abadi's PACELC Theorem</strong>:
    <div class="font-mono font-bold text-white mt-1">
      If Partition ($P$): Choose Availability ($A$) OR Consistency ($C$);<br>
      ELSE ($E$): Choose Latency ($L$) OR Consistency ($C$).
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-amber-400"></span> 1. The PACELC Classification Matrix
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">System</th>
          <th class="p-2.5">PACELC Class</th>
          <th class="p-2.5">During Partition ($P$)</th>
          <th class="p-2.5">Normal Runtime ($E$)</th>
          <th class="p-2.5">Architectural Trade-Off</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">AWS DynamoDB / Cassandra</td>
          <td class="p-2.5 text-emerald-400">PA / EL</td>
          <td class="p-2.5">Available (Sloppy Quorums)</td>
          <td class="p-2.5 text-emerald-400">Low Latency (Asynchronous read/write)</td>
          <td class="p-2.5">Trades linearizability for ultra-fast &lt; 5ms global latency.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Google Spanner / CockroachDB</td>
          <td class="p-2.5 text-amber-400">PC / EC</td>
          <td class="p-2.5 text-amber-400">Consistent (Rejects minority writes)</td>
          <td class="p-2.5 text-amber-400">Consistent (Commit Wait $2\epsilon$)</td>
          <td class="p-2.5">Incurs higher write latency ($50-100\,\text{ms}$) to guarantee absolute linearizability.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">MongoDB (Default)</td>
          <td class="p-2.5 text-fuchsia-400">PC / EC</td>
          <td class="p-2.5">Consistent (Primary election pause)</td>
          <td class="p-2.5">Consistent (Reads hit primary by default)</td>
          <td class="p-2.5">Can be configured as PA/EL with secondary read preferences.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-amber-400"></span> 2. Quorum Mathematics: Strict vs Sloppy Quorums
  </h4>
  <p>
    In a leaderless distributed database with replication factor $N$:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800 space-y-1">
    <div>Let $N = \text{Total Replicas}$, $W = \text{Write Ack Quorum}$, $R = \text{Read Quorum}$</div>
    <div class="text-amber-400 font-bold">$$R + W > N \implies \text{Guaranteed Overlap (Pigeonhole Principle)}$$</div>
    <div>Example: $N = 5, W = 3, R = 3 \implies R + W = 6 > 5$. At least ONE node in any read quorum is guaranteed to contain the latest write!</div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- PACELC 2x2 QUADRANT -->
  <g transform="translate(60, 40)">
    <!-- Axes -->
    <line x1="200" y1="20" x2="200" y2="280" stroke="#334155" stroke-width="2"/>
    <line x1="40" y1="150" x2="360" y2="150" stroke="#334155" stroke-width="2"/>

    <text x="200" y="14" fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="middle">ELSE: LOW LATENCY (L)</text>
    <text x="200" y="295" fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="middle">ELSE: STRONG CONSISTENCY (C)</text>
    <text x="30" y="154" fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="end">PARTITION: (A)</text>
    <text x="370" y="154" fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="start">PARTITION: (C)</text>

    <!-- Quadrant 1: PA / EL (Dynamo / Cassandra) -->
    <rect x="50" y="30" width="140" height="110" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="62" y="52" fill="#34d399" font-size="11" font-weight="bold">PA / EL Class</text>
    <text x="62" y="70" fill="#a7f3d0" font-size="9" font-family="monospace">AWS DynamoDB</text>
    <text x="62" y="86" fill="#a7f3d0" font-size="9" font-family="monospace">Apache Cassandra</text>
    <text x="62" y="104" fill="#6ee7b7" font-size="8">Sloppy Quorums</text>
    <text x="62" y="120" fill="#facc15" font-size="8">Eventual Consistency</text>

    <!-- Quadrant 2: PC / EC (Spanner / Cockroach) -->
    <rect x="210" y="160" width="140" height="110" rx="8" fill="#431407" stroke="#ea580c" stroke-width="1.5"/>
    <text x="222" y="182" fill="#fb923c" font-size="11" font-weight="bold">PC / EC Class</text>
    <text x="222" y="200" fill="#fed7aa" font-size="9" font-family="monospace">Google Spanner</text>
    <text x="222" y="216" fill="#fed7aa" font-size="9" font-family="monospace">CockroachDB</text>
    <text x="222" y="234" fill="#fdba74" font-size="8">TrueTime Atomic Clocks</text>
    <text x="222" y="250" fill="#f43f5e" font-size="8">Linearizable Consistency</text>
  </g>

  <!-- QUORUM OVERLAP VISUALIZATION (RIGHT PANEL) -->
  <g transform="translate(480, 40)">
    <rect width="440" height="300" rx="10" fill="#0f172a" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="12" font-family="sans-serif" font-weight="bold">Strict Quorum Invariant: R + W > N (N = 5)</text>
    <text x="20" y="50" fill="#94a3b8" font-size="9" font-family="monospace">Mathematical Proof of Read/Write Overlap</text>

    <!-- 5 Node Circles -->
    <!-- Node 1: Write only -->
    <rect x="20" y="80" width="70" height="80" rx="6" fill="#1e1b4b" stroke="#7c3aed"/>
    <text x="55" y="105" fill="#c084fc" font-size="10" font-weight="bold" text-anchor="middle">Node 1</text>
    <text x="55" y="130" fill="#c084fc" font-size="9" font-family="monospace" text-anchor="middle">Write (W)</text>

    <!-- Node 2: Write only -->
    <rect x="100" y="80" width="70" height="80" rx="6" fill="#1e1b4b" stroke="#7c3aed"/>
    <text x="135" y="105" fill="#c084fc" font-size="10" font-weight="bold" text-anchor="middle">Node 2</text>
    <text x="135" y="130" fill="#c084fc" font-size="9" font-family="monospace" text-anchor="middle">Write (W)</text>

    <!-- Node 3: OVERLAP (Write + Read) -->
    <rect x="180" y="70" width="80" height="100" rx="6" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="220" y="95" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">Node 3</text>
    <rect x="190" y="105" width="60" height="20" rx="4" fill="#042f2e"/>
    <text x="220" y="119" fill="#facc15" font-size="8" font-family="monospace" text-anchor="middle">OVERLAP!</text>
    <text x="220" y="145" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">W=3 &amp; R=3</text>
    <text x="220" y="158" fill="#34d399" font-size="7" font-family="monospace" text-anchor="middle">Latest Version</text>

    <!-- Node 4: Read only -->
    <rect x="270" y="80" width="70" height="80" rx="6" fill="#0c4a6e" stroke="#0284c7"/>
    <text x="305" y="105" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">Node 4</text>
    <text x="305" y="130" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="middle">Read (R)</text>

    <!-- Node 5: Read only -->
    <rect x="350" y="80" width="70" height="80" rx="6" fill="#0c4a6e" stroke="#0284c7"/>
    <text x="385" y="105" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">Node 5</text>
    <text x="385" y="130" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="middle">Read (R)</text>

    <!-- Bottom Explanation -->
    <rect x="20" y="190" width="400" height="90" rx="6" fill="#02040d" stroke="#1e293b"/>
    <text x="32" y="214" fill="#facc15" font-size="9" font-family="monospace" font-weight="bold">THE PIGEONHOLE GUARANTEE:</text>
    <text x="32" y="234" fill="#cbd5e1" font-size="8" font-family="sans-serif">
      Because $3 + 3 = 6 > 5$, any valid read quorum of 3 nodes MUST intersect with at least one node that acknowledged the write.
    </text>
    <text x="32" y="254" fill="#34d399" font-size="8" font-family="monospace">
      Read Repair: Node 3 updates stale replicas in background!
    </text>
  </g>
</svg>
""",
        "codeSnippet": """# Production Python Quorum Consistency Simulator
# Demonstrating Strict Quorums, Read Repair & Version Vector Reconciliation
from typing import List, Dict, Tuple
import time

class QuorumReplica:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.data: Dict[str, Tuple[any, int]] = {} # key -> (value, version)

class QuorumCluster:
    def __init__(self, total_nodes: int = 5, write_quorum: int = 3, read_quorum: int = 3):
        assert write_quorum + read_quorum > total_nodes, "PACELC Invariant Violated: R + W must exceed N!"
        self.N = total_nodes
        self.W = write_quorum
        self.R = read_quorum
        self.replicas = [QuorumReplica(i) for i in range(total_nodes)]

    def write(self, key: str, val: any) -> bool:
        # Step 1: Discover highest current version across a read quorum
        read_nodes = self.replicas[:self.R]
        max_ver = max((n.data.get(key, (None, 0))[1] for n in read_nodes), default=0)
        new_ver = max_ver + 1

        # Step 2: Write (val, new_ver) to W nodes
        acked = 0
        for node in self.replicas[:self.W]:
            node.data[key] = (val, new_ver)
            acked += 1

        return acked >= self.W

    def read_with_repair(self, key: str) -> any:
        # Step 1: Query R replicas
        read_nodes = self.replicas[:self.R]
        responses = [n.data.get(key, (None, 0)) for n in read_nodes]

        # Step 2: Find record with highest version
        best_val, highest_ver = max(responses, key=lambda x: x[1])

        # Step 3: Asynchronous Read-Repair: Heal any lagging node in quorum
        for node in read_nodes:
            curr_val, curr_ver = node.data.get(key, (None, 0))
            if curr_ver < highest_ver:
                node.data[key] = (best_val, highest_ver) # Repaired in background!

        return best_val
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The AWS Kinesis 2020 Global Outage (Cascading Fleet Collapse)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Downed major portions of the global internet (Roku, Adobe, Target, Amazon Alexa) for over 15 hours.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      On November 25, 2020, AWS engineers added capacity to the front-end fleet of Kinesis in <code>us-east-1</code>.
      Every server in the Kinesis front-end fleet maintains an internal operating system thread for every other server in the cluster to track partition state.
    </p>
    <p>
      When the fleet size crossed a critical threshold, the operating system kernel reached its maximum thread limit (<code>threads-max</code>).
      Nodes began crashing simultaneously. As surviving nodes attempted to rebalance partitions and form quorums, their thread counts spiked further, knocking them offline.
      <strong>The entire frontend fleet went into an unrecoverable restart loop that took 15 hours to manually cold-boot server by server!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Cell-Based Architecture:</strong> Decompose monolithic regional clusters into isolated <strong>Cells</strong> (e.g. max 1,000 nodes per cell). A failure in Cell A can never cascade to Cell B.</li>
      <li><strong class="text-white">Elimination of Full Mesh Topologies:</strong> Replace $O(N^2)$ all-to-all thread connections with hierarchical gossip protocols or centralized consensus control planes (KRaft / Paxos).</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "In a distributed key-value store with $N=3, W=2, R=2$, does satisfying $R+W > N$ guarantee Linearizable (Strong) Consistency? Why or why not?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "No! This is one of the most common misconceptions in distributed systems.
      Satisfying $R + W > N$ guarantees <strong>Regular Consistency</strong> (you will not read a value older than the most recently completed write), but it does <strong>NOT guarantee Linearizability</strong> in the presence of concurrent operations.
      <br><br>
      Consider this failure mode: A write operation updates Node 1 and Node 2.
      Client A begins reading from Node 1 and Node 3. It sees the new write on Node 1 and returns it at $T=1$.
      A split-second later ($T=2$), Client B reads from Node 2 and Node 3. If Node 2's packet is delayed or dropped, Client B might only observe the old stale value from Node 3!
      <br><br>
      To a real-time outside observer, Client B read backwards in time <em>after</em> Client A had already seen the newer value!
      To achieve true Linearizability, a leaderless database must execute a <strong>Synchronous Write-Back during Reads (Read-Repair before returning)</strong> or use a consensus coordinator like Paxos/Raft."
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-09-distributed-transactions",
        "stageId": "stage-4",
        "stageNum": "STAGE 04",
        "badge": "Senior / Staff",
        "color": "amber",
        "title": "4.2 Distributed Transactions: Two-Phase Commit (2PC) vs The Saga Pattern",
        "difficulty": "Senior to Staff",
        "readTime": "24 min read",
        "simulatorKey": "interview",
        "summary": "Atomic cross-service transactions. Why Two-Phase Commit (2PC) kills throughput in cloud networks. Choreographed vs Orchestrated Sagas and compensating transactions.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/20 text-amber-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-amber-400 mb-1">First-Principles Intuition</div>
    Imagine booking a vacation requiring: (1) Flight reservation, (2) Hotel booking, (3) Rental car.
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-amber-200">
      <li><strong>Two-Phase Commit (2PC):</strong> You call the airline, hotel, and car rental. You order all three to freeze the seats and rooms with locks ($Phase 1 - Prepare$). If the car rental agent's phone drops, the airline and hotel hold those seats locked indefinitely, blocking other customers from booking until the coordinator recovers! ($Blocking protocol$).</li>
      <li><strong>The Saga Pattern:</strong> You book and pay for the flight ($T_1$). Next, you book and pay for the hotel ($T_2$). If the rental car is sold out ($T_3$ fails), you invoke <strong>Compensating Transactions</strong>: automatically cancel the hotel ($C_2$) and refund the flight ($C_1$). No blocking locks, 100x higher throughput!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-amber-400"></span> 1. Why 2PC Fails at Scale in Cloud Environments
  </h4>
  <p>
    Two-Phase Commit is an inherently <strong>blocking protocol</strong>. During Phase 1, participating database engines acquire row-level exclusive locks and write prepare records to disk:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-rose-300 border border-slate-800 space-y-1">
    <div>1. Coordinator &rarr; Node 1, 2, 3: "PREPARE"</div>
    <div>2. Node 1, 2, 3: Lock rows &rarr; Return "VOTE_COMMIT"</div>
    <div>3. Coordinator crashes before sending "GLOBAL_COMMIT"!</div>
    <div class="text-white font-bold">&rArr; Nodes 1, 2, 3 are in the In-Doubt state. Rows remain locked FOREVER until human intervention!</div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-amber-400"></span> 2. Choreography vs Orchestration in Sagas
  </h4>
  <ul class="list-disc list-inside space-y-2 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Choreographed Saga (Event-Driven):</strong> Services publish events to Kafka (e.g. <code>OrderCreated</code> &rarr; <code>PaymentCharged</code> &rarr; <code>InventoryReserved</code>). Flaw: Complex cyclic dependencies and spaghetti debugging when 10+ services participate.</li>
    <li><strong class="text-white">Orchestrated Saga (State Machine / Temporal):</strong> A centralized Orchestrator service executes a deterministic workflow state machine, invoking gRPC endpoints and tracking transaction state in a persistent WAL. If any step fails, the orchestrator triggers backward compensation in reverse order.</li>
  </ul>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-fwd" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
    <marker id="arr-rev" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- SAGA ORCHESTRATOR (TEMPORAL) -->
  <g transform="translate(40, 110)">
    <rect width="200" height="150" rx="10" fill="#1e1b4b" stroke="#7c3aed" stroke-width="2"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Saga Orchestrator</text>
    <text x="16" y="48" fill="#c084fc" font-size="9" font-family="monospace">Temporal Workflow Engine</text>
    <rect x="16" y="60" width="168" height="74" rx="4" fill="#0f0c29"/>
    <text x="24" y="78" fill="#a7f3d0" font-size="8" font-family="monospace">Step 1: Order (Pending)</text>
    <text x="24" y="94" fill="#a7f3d0" font-size="8" font-family="monospace">Step 2: Payment (Charged)</text>
    <text x="24" y="110" fill="#f87171" font-size="8" font-family="monospace">Step 3: Inventory (FAIL)</text>
    <text x="24" y="126" fill="#facc15" font-size="8" font-family="monospace">&rArr; Trigger Compensations!</text>
  </g>

  <!-- STEP 1: ORDER SERVICE -->
  <g transform="translate(300, 30)">
    <rect width="180" height="95" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <text x="14" y="24" fill="#38bdf8" font-size="11" font-weight="bold">1. Order Service</text>
    <text x="14" y="42" fill="#a7f3d0" font-size="8" font-family="monospace">Action: createOrder()</text>
    <text x="14" y="58" fill="#cbd5e1" font-size="8">Status: PENDING</text>
    <text x="14" y="76" fill="#f43f5e" font-size="8" font-family="monospace">Compensate: cancelOrder()</text>
  </g>

  <!-- STEP 2: PAYMENT SERVICE -->
  <g transform="translate(520, 30)">
    <rect width="180" height="95" rx="8" fill="#0f172a" stroke="#059669" stroke-width="1.5"/>
    <text x="14" y="24" fill="#34d399" font-size="11" font-weight="bold">2. Payment Service</text>
    <text x="14" y="42" fill="#a7f3d0" font-size="8" font-family="monospace">Action: chargeCard()</text>
    <text x="14" y="58" fill="#cbd5e1" font-size="8">Status: CHARGED $120</text>
    <text x="14" y="76" fill="#f43f5e" font-size="8" font-family="monospace">Compensate: refundCard()</text>
  </g>

  <!-- STEP 3: INVENTORY SERVICE (FAILS!) -->
  <g transform="translate(740, 30)">
    <rect width="180" height="95" rx="8" fill="#431407" stroke="#ea580c" stroke-width="2"/>
    <text x="14" y="24" fill="#fb923c" font-size="11" font-weight="bold">3. Inventory Service</text>
    <text x="14" y="42" fill="#f87171" font-size="8" font-family="monospace">Action: reserveStock()</text>
    <text x="14" y="58" fill="#f87171" font-size="8" font-weight="bold">ERROR: OUT OF STOCK!</text>
    <text x="14" y="76" fill="#fed7aa" font-size="8">Returns Failure to Saga</text>
  </g>

  <!-- FORWARD WORKFLOW ARROWS -->
  <path d="M 240 140 L 300 80" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-fwd)"/>
  <path d="M 480 80 L 520 80" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-fwd)"/>
  <path d="M 700 80 L 740 80" fill="none" stroke="#ea580c" stroke-width="2"/>

  <!-- BACKWARD COMPENSATING ARROWS -->
  <path d="M 740 110 Q 500 240 240 180" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4" marker-end="url(#arr-rev)"/>
  <text x="500" y="210" fill="#f43f5e" font-size="9" font-family="monospace" text-anchor="middle">Step 3 Fails &rarr; Trigger Compensating Refund</text>

  <!-- REFUND EXECUTION -->
  <path d="M 240 220 L 610 130" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#arr-rev)"/>
  <text x="460" y="170" fill="#f43f5e" font-size="8" font-family="monospace">refundCard($120)</text>

  <!-- FOOTER CARD -->
  <g transform="translate(40, 290)">
    <rect width="880" height="60" rx="8" fill="#0f172a" stroke="#1e293b"/>
    <text x="16" y="24" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">THE SAGA GUARANTEE: EVENTUAL CONSISTENCY WITHOUT BLOCKING LOCKS</text>
    <text x="16" y="44" fill="#cbd5e1" font-size="9" font-family="sans-serif">
      Each step commits locally within its own private database. Zero distributed locking. System reaches consistent terminal state in &lt; 500ms.
    </text>
  </g>
</svg>
""",
        "codeSnippet": """// Production Go Orchestrated Saga Engine with Compensating Actions
package saga

import (
	"context"
	"fmt"
	"time"
)

type Step struct {
	Name       string
	Action     func(ctx context.Context) error
	Compensate func(ctx context.Context) error
}

type SagaCoordinator struct {
	steps []Step
}

func (s *SagaCoordinator) AddStep(step Step) {
	s.steps = append(s.steps, step)
}

func (s *SagaCoordinator) Execute(ctx context.Context) error {
	var executedSteps []Step

	for _, step := range s.steps {
		fmt.Printf("[SAGA] Executing action: %s\\n", step.Name)
		err := step.Action(ctx)
		if err != nil {
			fmt.Printf("[SAGA ERROR] %s failed: %v. Initiating Rollback...\\n", step.Name, err)
			s.rollback(ctx, executedSteps)
			return fmt.Errorf("saga aborted at step '%s': %w", step.Name, err)
		}
		// Track successfully completed steps for potential reverse compensation
		executedSteps = append(executedSteps, step)
	}

	fmt.Println("[SAGA SUCCESS] All steps committed successfully.")
	return nil
}

func (s *SagaCoordinator) rollback(ctx context.Context, steps []Step) {
	// Execute compensating transactions in reverse chronological order
	for i := len(steps) - 1; i >= 0; i-- {
		step := steps[i]
		if step.Compensate == nil {
			continue
		}
		fmt.Printf("[SAGA COMPENSATE] Executing compensation: %s\\n", step.Name)
		
		// Retry compensation with exponential backoff; compensations MUST succeed!
		backoff := 100 * time.Millisecond
		for attempt := 1; attempt <= 5; attempt++ {
			err := step.Compensate(ctx)
			if err == nil {
				break
			}
			fmt.Printf("Compensation attempt %d failed: %v. Retrying in %v...\\n", attempt, err, backoff)
			time.Sleep(backoff)
			backoff *= 2
		}
	}
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The FinTech Phantom Balance Outage ($20 Million Debit Card Desync)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 40,000 customers withdrew funds that were never deducted from their bank accounts due to an uncompensated saga crash.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      A European digital bank migrated from 2PC to a choreographed saga for ATM cash withdrawals.
      When a user requested cash, Step 1 authorized the card with Visa/Mastercard. Step 2 debited the internal core banking Postgres balance.
    </p>
    <p>
      During a cloud database failover, Step 2 timed out.
      However, the microservice was not configured with a persistent workflow WAL. When the pod restarted, <strong>it lost memory of the in-flight saga</strong>.
      The ATM dispensed physical cash, but the compensating debit was never executed.
      Word spread on social media, resulting in $20 million in unauthorized cash withdrawals in 4 hours!
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Persistent Saga Event Sourcing (Temporal / Cadence):</strong> Saga orchestrators must persist every state transition to an append-only event history before executing RPCs. If a worker pod crashes, a replacement resumes from the exact recorded state.</li>
      <li><strong class="text-white">Idempotent Compensating Actions:</strong> All compensating functions (e.g. <code>refundCard()</code>) must be strictly idempotent to allow infinite retries until verified.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "In the Saga pattern, what happens if a Compensating Transaction fails? How does the system avoid leaving customer accounts in an inconsistent state?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "In a production Saga architecture, <strong>Compensating Transactions are mathematically required to eventually succeed</strong>. A compensation is not allowed to fail permanently.
      <br><br>
      To guarantee this invariant:
      <br><br>
      1. <strong>Infinite Exponential Backoff with Jitter:</strong> If a compensation fails due to a network timeout or remote service 503, the orchestrator retries indefinitely (e.g. up to 24 hours).
      <br><br>
      2. <strong>Strict Idempotency:</strong> The compensation endpoint takes the original saga UUID and executes idempotently, so 10 retries cause no damage.
      <br><br>
      3. <strong>Dead Letter Queue (DLQ) &amp; Automated Financial Escort:</strong> If an unrecoverable failure occurs (e.g. the user's bank account was closed during the transaction), the saga halts, routes the payload to a high-priority Dead Letter Queue, and triggers a PagerDuty alert for human operator reconciliation.
      This is why mission-critical banking ledgers always use <strong>Double-Entry Bookkeeping</strong>: discrepancies immediately flag on balancing invariants rather than silently corrupting money."
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 4 loaded with {len(STAGE_4_CHAPTERS)} comprehensive chapters.")
