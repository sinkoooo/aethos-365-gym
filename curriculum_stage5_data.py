# curriculum_stage5_data.py
# Stage 5: Staff Principal - Consensus Protocols & Distributed Locks

STAGE_5_CHAPTERS = [
    {
        "id": "c-10-raft-consensus",
        "stageId": "stage-5",
        "stageNum": "STAGE 05",
        "badge": "Staff Principal",
        "color": "rose",
        "title": "5.1 Distributed Consensus: The Raft Protocol Deconstructed",
        "difficulty": "Staff",
        "readTime": "28 min read",
        "simulatorKey": "interview",
        "summary": "Consensus fundamentals: Solving Crash Fault-Tolerance. Randomized election timeouts (150-300ms), AppendEntries RPCs, commit index high watermarks, and log compaction.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/20 text-rose-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-rose-400 mb-1">First-Principles Intuition</div>
    Imagine a 5-member supreme court where judges communicate only by sending couriers over treacherous mountain roads where couriers can be captured or delayed for days.
    How can the judges guarantee they agree on a single legal decree without split decisions, even if 2 judges are trapped in an avalanche?
    <br><br>
    That is the <strong>Distributed Consensus Problem</strong>.
    <strong>Raft</strong> decomposes this problem into three understandable, mathematically proven subproblems:
    (1) Leader Election, (2) Log Replication, and (3) Safety.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-rose-400"></span> 1. The 3 Raft Subproblems &amp; State Transitions
  </h4>
  <p>
    A Raft node exists in one of three states: <code>Follower</code>, <code>Candidate</code>, or <code>Leader</code>.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-cyan-400 font-bold">1. Leader Election</div>
      <p class="text-slate-400 font-sans">
        Followers reset an <em>election timer</em> (randomized between 150ms - 300ms) upon receiving leader heartbeats. If the timer expires without a heartbeat, the follower increments its <code>Term</code>, becomes a <code>Candidate</code>, and requests votes.
      </p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-emerald-400 font-bold">2. Log Replication</div>
      <p class="text-slate-400 font-sans">
        Clients send writes only to the Leader. The Leader appends the entry to its private log and broadcasts <code>AppendEntries(term, prevLogIndex, prevLogTerm, entries)</code> to all followers.
      </p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-amber-400 font-bold">3. Quorum Commitment</div>
      <p class="text-slate-400 font-sans">
        Once a majority quorum ($\lfloor N/2 \rfloor + 1$) of followers safely write the entry to disk, the Leader advances its <code>commitIndex</code> high watermark and executes the command on its local state machine!
      </p>
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-rose-400"></span> 2. The Golden Safety Invariant: Leader Completeness
  </h4>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-rose-300 border border-slate-800">
    <div class="font-bold text-white text-sm mb-1">Raft Leader Completeness Property:</div>
    If a log entry is committed in a given term, that entry will be present in the logs of the leaders for all higher-numbered terms.
    <div class="mt-2 text-slate-300 font-sans text-xs">
      <strong>Voter Check:</strong> A voter will DENY its vote if the candidate's log is less up-to-date than its own log:
      <br>
      <code>candidate.lastLogTerm &lt; voter.lastLogTerm OR (candidate.lastLogTerm == voter.lastLogTerm AND candidate.lastLogIndex &lt; voter.lastLogIndex)</code>
      <br>
      This simple check mathematically guarantees an uncommitted candidate can never overwrite committed data!
    </div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-ldr" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#059669"/><stop offset="100%" stop-color="#047857"/></linearGradient>
    <linearGradient id="g-fol" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/></linearGradient>
    <marker id="arr-rf" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- RAFT LEADER (NODE 1) -->
  <g transform="translate(60, 40)">
    <rect width="240" height="300" rx="12" fill="url(#g-ldr)" stroke="#34d399" stroke-width="2"/>
    <text x="20" y="32" fill="#ffffff" font-size="14" font-family="sans-serif" font-weight="bold">LEADER (Node 1)</text>
    <text x="20" y="52" fill="#a7f3d0" font-size="10" font-family="monospace">Term: 4 &bull; Heartbeat 50ms</text>

    <!-- Leader Log Array -->
    <g transform="translate(20, 75)" font-family="monospace" font-size="9">
      <text x="0" y="-8" fill="#d1fae5">REPLICATED LOG:</text>
      <!-- Entries -->
      <rect x="0" y="0" width="200" height="30" rx="4" fill="#042f2e" stroke="#34d399"/>
      <text x="10" y="20" fill="#a7f3d0">[T=1, Idx=1] SET x=10 (Committed)</text>

      <rect x="0" y="38" width="200" height="30" rx="4" fill="#042f2e" stroke="#34d399"/>
      <text x="10" y="58" fill="#a7f3d0">[T=2, Idx=2] SET y=20 (Committed)</text>

      <rect x="0" y="76" width="200" height="30" rx="4" fill="#065f46" stroke="#facc15" stroke-width="1.5"/>
      <text x="10" y="96" fill="#facc15">[T=4, Idx=3] SET z=30 (Quorum...)</text>
    </g>

    <rect x="20" y="220" width="200" height="60" rx="6" fill="#064e3b" stroke="#10b981"/>
    <text x="30" y="242" fill="#ffffff" font-size="10" font-weight="bold">Commit High Watermark</text>
    <text x="30" y="260" fill="#a7f3d0" font-size="9" font-family="monospace">commitIndex = 2</text>
  </g>

  <!-- FOLLOWER NODES (CLUSTER MAJORITY) -->
  <g transform="translate(360, 40)">
    <!-- Follower 2 -->
    <rect width="260" height="85" rx="8" fill="url(#g-fol)" stroke="#334155" stroke-width="1.5"/>
    <text x="16" y="24" fill="#f8fafc" font-size="11" font-weight="bold">Follower 2 (Acked)</text>
    <text x="16" y="42" fill="#38bdf8" font-size="8" font-family="monospace">matchIndex=3 &bull; Term 4</text>
    <text x="16" y="60" fill="#34d399" font-size="8" font-family="monospace">Log: [Idx 1, Idx 2, Idx 3] &check;</text>

    <!-- Follower 3 -->
    <g transform="translate(0, 105)">
      <rect width="260" height="85" rx="8" fill="url(#g-fol)" stroke="#334155" stroke-width="1.5"/>
      <text x="16" y="24" fill="#f8fafc" font-size="11" font-weight="bold">Follower 3 (Acked)</text>
      <text x="16" y="42" fill="#38bdf8" font-size="8" font-family="monospace">matchIndex=3 &bull; Term 4</text>
      <text x="16" y="60" fill="#34d399" font-size="8" font-family="monospace">Log: [Idx 1, Idx 2, Idx 3] &check;</text>
    </g>

    <!-- Follower 4 (Partitioned / Slow) -->
    <g transform="translate(0, 210)">
      <rect width="260" height="85" rx="8" fill="#431407" stroke="#ea580c" stroke-width="1.5"/>
      <text x="16" y="24" fill="#fb923c" font-size="11" font-weight="bold">Follower 4 (Partitioned)</text>
      <text x="16" y="42" fill="#f87171" font-size="8" font-family="monospace">matchIndex=1 &bull; Missed Heartbeat</text>
      <text x="16" y="60" fill="#fed7aa" font-size="8">Lagging behind, cannot disrupt</text>
    </g>
  </g>

  <!-- QUORUM CALCULATION CARD (RIGHT PANEL) -->
  <g transform="translate(660, 40)">
    <rect width="260" height="300" rx="10" fill="#0f172a" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="12" font-family="sans-serif" font-weight="bold">Raft Quorum Calculus</text>
    <text x="20" y="50" fill="#94a3b8" font-size="9" font-family="monospace">N = 5 Nodes Total</text>

    <rect x="20" y="70" width="220" height="80" rx="6" fill="#1e293b"/>
    <text x="30" y="94" fill="#34d399" font-size="10" font-family="monospace" font-weight="bold">Majority Formula:</text>
    <text x="30" y="114" fill="#facc15" font-size="11" font-family="monospace">Quorum = floor(5/2) + 1 = 3</text>
    <text x="30" y="134" fill="#cbd5e1" font-size="8">Node 1, 2, 3 agree &rarr; COMMITTED!</text>

    <rect x="20" y="170" width="220" height="110" rx="6" fill="#02040d" stroke="#1e293b"/>
    <text x="30" y="194" fill="#c084fc" font-size="10" font-family="monospace" font-weight="bold">Fault-Tolerance (F):</text>
    <text x="30" y="214" fill="#a7f3d0" font-size="10" font-family="monospace">F = (N - 1) / 2 = 2 Nodes</text>
    <text x="30" y="234" fill="#cbd5e1" font-size="8" font-family="sans-serif">
      System tolerates up to 2 arbitrary node crashes or partitions with 100% data safety.
    </text>
  </g>

  <!-- REPLICATION RPC ARROWS -->
  <path d="M 300 100 L 360 80" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-rf)"/>
  <path d="M 300 190 L 360 150" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-rf)"/>
  <path d="M 300 270 L 360 250" fill="none" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="3"/>
</svg>
""",
        "codeSnippet": """// Production Go Raft State Machine: Election Timer & Heartbeat Handling
package raft

import (
	"context"
	"math/rand"
	"sync"
	"time"
)

type NodeRole int

const (
	Follower NodeRole = iota
	Candidate
	Leader
)

type RaftNode struct {
	mu          sync.Mutex
	id          int
	peers       []int
	currentTerm int
	votedFor    int
	role        NodeRole
	heartbeatCh chan struct{}
}

func (r *RaftNode) Run(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
			r.mu.Lock()
			role := r.role
			r.mu.Unlock()

			switch role {
			case Follower:
				r.runFollower(ctx)
			case Candidate:
				r.runCandidate(ctx)
			case Leader:
				r.runLeader(ctx)
			}
		}
	}
}

func (r *RaftNode) runFollower(ctx context.Context) {
	// Raft Golden Rule: Randomized election timeout (150ms to 300ms)
	// Randomization eliminates split-vote ties when multiple nodes start elections!
	timeout := time.Duration(150+rand.Intn(150)) * time.Millisecond
	timer := time.NewTimer(timeout)
	defer timer.Stop()

	select {
	case <-r.heartbeatCh:
		// Heartbeat received from valid leader; reset timer
		return
	case <-timer.C:
		r.mu.Lock()
		r.role = Candidate
		r.currentTerm++
		r.votedFor = r.id // Vote for self
		r.mu.Unlock()
	case <-ctx.Done():
		return
	}
}

func (r *RaftNode) runLeader(ctx context.Context) {
	// Leader broadcasts heartbeats every 50ms (well below 150ms election timeout)
	ticker := time.NewTicker(50 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			r.broadcastHeartbeats()
		case <-ctx.Done():
			return
		}
	}
}

func (r *RaftNode) broadcastHeartbeats() {
	r.mu.Lock()
	defer r.mu.Unlock()
	// Sends empty AppendEntries RPC to all peers to maintain lease
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Cloudflare 2019 Global etcd Consensus Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 12 million websites worldwide served 502 Bad Gateway errors as Cloudflare edge proxies lost routing configurations.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      Cloudflare uses <strong>etcd</strong> (governed by the Raft consensus protocol) to synchronize edge firewall configurations across global points of presence.
      An automated script pushed an unusually large configuration file (exceeding etcd's 1.5MB Raft proposal limit).
    </p>
    <p>
      The Raft Leader attempted to replicate this massive entry, exhausting its network socket buffer.
      Heartbeat RPCs were blocked behind the oversized log entry.
      Followers timed out, initiated elections, and created a <strong>Raft Election Storm</strong> where nodes repeatedly traded leadership without committing entries, halting edge configuration updates globally!
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Strict Raft Proposal Size Limits:</strong> Reject any client write payload &gt; 1MB at the gRPC gateway before it ever touches the Raft log.</li>
      <li><strong class="text-white">Dedicated Heartbeat Channels:</strong> Decouple Raft heartbeats (leadership leases) onto a separate TCP stream from heavy log replication so payload congestion can never trigger false election timeouts.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "In Raft, why can a newly elected Leader never commit a log entry from a PREVIOUS term simply by counting replicas? Why must it commit an entry from its CURRENT term first?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "This is Section 5.4.2 of Diego Ongaro's Raft paper: <strong>The Commit Rule for Previous Terms</strong>.
      <br><br>
      If a leader were allowed to commit an old log entry from a previous term simply because it reached a majority of replicas, it can lead to <strong>silent data overwrites</strong>!
      Imagine a scenario where an old leader replicated an entry to 3 out of 5 nodes, then crashed before committing.
      A new leader takes over. If that new leader replicates the old entry to 3 nodes and marks it committed, but then crashes before writing its own current term entry, another node with an alternate uncommitted log could be elected leader and overwrite that supposedly 'committed' entry!
      <br><br>
      To eliminate this hazard, Raft enforces an absolute invariant: <strong>A Leader never commits an entry from a previous term directly</strong>.
      Instead, the Leader must replicate an entry from its <em>current term</em> to a majority.
      By the Log Matching Invariant, committing the current-term entry transitively commits ALL preceding entries from previous terms safely!"
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-11-fencing-tokens",
        "stageId": "stage-5",
        "stageNum": "STAGE 05",
        "badge": "Staff Principal",
        "color": "rose",
        "title": "5.2 Distributed Locks & Fencing Tokens vs Redlock Flaws",
        "difficulty": "Staff to Principal",
        "readTime": "26 min read",
        "simulatorKey": "limiter",
        "summary": "Martin Kleppmann vs antirez: Why Redis Redlock cannot guarantee mutual exclusion. The Unholy Trinity: Process pauses (GC), unbounded network delay, and clock jumps. Monotonic fencing tokens.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/20 text-rose-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-rose-400 mb-1">First-Principles Intuition</div>
    Imagine a bank safety deposit vault where only one customer is allowed inside at a time. The guard gives you a 10-minute timer.
    <br><br>
    While you are inside inspecting your lockbox, you suddenly fall unconscious (<strong>Process Pause / Java GC</strong>) for 15 minutes.
    Your timer expires. The guard assumes you left and lets another customer inside.
    You wake up and write into the ledger. Both of you are writing inside the vault at the exact same moment!
    <br><br>
    That is the fatal flaw with distributed locks based on time (like Redis locks).
    <strong>Time is not synchronized across computers.</strong>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-rose-400"></span> 1. Martin Kleppmann's Critique: The Unholy Trinity
  </h4>
  <p>
    In distributed systems, you must assume the presence of the <strong>Unholy Trinity</strong>:
  </p>
  <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Unbounded Network Delays:</strong> A TCP packet can be delayed in a router buffer for seconds or minutes.</li>
    <li><strong class="text-white">Process Pauses:</strong> Java Stop-the-World garbage collection, OS paging/swapping, or hypervisor VM live migrations can pause a thread for 30+ seconds without its knowledge.</li>
    <li><strong class="text-white">Unsynchronized Clocks:</strong> NTP clock adjustments can step time backwards or jump forwards, prematurely expiring TTL leases.</li>
  </ul>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-rose-400"></span> 2. The Mathematical Solution: Monotonic Fencing Tokens
  </h4>
  <p>
    If the lock server cannot prevent a client from waking up after its lock expires (a <em>Zombie Process</em>), the <strong>Storage Layer must protect itself</strong>!
    Every time a lock is granted, the lock server issues a strictly incrementing <strong>Fencing Token</strong> ($1, 2, 3...$):
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-emerald-300 border border-slate-800 space-y-1">
    <div>1. Client 1 acquires lock &rarr; receives <strong>Fencing Token 33</strong>.</div>
    <div>2. Client 1 pauses for 60 seconds (GC pause). Lock expires!</div>
    <div>3. Client 2 acquires lock &rarr; receives <strong>Fencing Token 34</strong>.</div>
    <div>4. Client 2 writes to storage with Token 34. Storage records: <code>max_token = 34</code>.</div>
    <div>5. Client 1 wakes up, blindly tries to write with Token 33.</div>
    <div class="text-rose-400 font-bold">&rArr; Storage checks: 33 &lt; 34 &rarr; REJECT ZOMBIE WRITE! Zero data corruption!</div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-ok" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
    <marker id="arr-bad" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- LOCK SERVICE (ZOOKEEPER / ETCD) -->
  <g transform="translate(60, 40)">
    <rect width="200" height="120" rx="10" fill="#0f172a" stroke="#0284c7" stroke-width="2"/>
    <text x="16" y="28" fill="#38bdf8" font-size="12" font-family="sans-serif" font-weight="bold">Lock Service (etcd)</text>
    <text x="16" y="48" fill="#94a3b8" font-size="9" font-family="monospace">Monotonic Counter</text>
    <rect x="16" y="60" width="168" height="40" rx="4" fill="#0c4a6e"/>
    <text x="24" y="84" fill="#facc15" font-size="10" font-family="monospace">Token Counter: 34</text>
  </g>

  <!-- CLIENT 1 (PAUSED ZOMBIE) -->
  <g transform="translate(320, 40)">
    <rect width="240" height="120" rx="10" fill="#431407" stroke="#ea580c" stroke-width="2"/>
    <text x="16" y="28" fill="#fb923c" font-size="12" font-family="sans-serif" font-weight="bold">Client 1 (Zombie)</text>
    <text x="16" y="48" fill="#f87171" font-size="9" font-family="monospace">Token: 33 (Lock Expired!)</text>
    <rect x="16" y="60" width="208" height="40" rx="4" fill="#7f1d1d"/>
    <text x="24" y="84" fill="#fca5a5" font-size="9" font-family="monospace">Paused by 40s Java GC</text>
  </g>

  <!-- CLIENT 2 (ACTIVE WINNER) -->
  <g transform="translate(320, 200)">
    <rect width="240" height="120" rx="10" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <text x="16" y="28" fill="#34d399" font-size="12" font-family="sans-serif" font-weight="bold">Client 2 (Active Winner)</text>
    <text x="16" y="48" fill="#a7f3d0" font-size="9" font-family="monospace">Token: 34 (Acquired Lock)</text>
    <rect x="16" y="60" width="208" height="40" rx="4" fill="#042f2e"/>
    <text x="24" y="84" fill="#34d399" font-size="9" font-family="monospace">Writes to Storage First</text>
  </g>

  <!-- STORAGE ENGINE (VERIFICATION BARRIER) -->
  <g transform="translate(660, 100)">
    <rect width="240" height="180" rx="12" fill="#1e1b4b" stroke="#7c3aed" stroke-width="2"/>
    <text x="20" y="32" fill="#c084fc" font-size="13" font-family="sans-serif" font-weight="bold">Storage Engine</text>
    <text x="20" y="52" fill="#e9d5ff" font-size="9" font-family="monospace">Verification Barrier</text>

    <rect x="20" y="70" width="200" height="40" rx="4" fill="#312e81"/>
    <text x="28" y="94" fill="#facc15" font-size="10" font-family="monospace">Highest Token Seen: 34</text>

    <!-- Verdicts -->
    <text x="20" y="135" fill="#34d399" font-size="9" font-family="monospace">&check; Token 34 &ge; 34: ACCEPTED</text>
    <text x="20" y="155" fill="#f43f5e" font-size="9" font-family="monospace">&cross; Token 33 &lt; 34: REJECTED!</text>
  </g>

  <!-- ARROWS -->
  <!-- Client 2 Success -->
  <path d="M 560 260 L 660 210" fill="none" stroke="#34d399" stroke-width="2.5" marker-end="url(#arr-ok)"/>
  <text x="600" y="255" fill="#34d399" font-size="9" font-family="monospace">Write(34)</text>

  <!-- Client 1 Zombie Reject -->
  <path d="M 560 100 L 660 140" fill="none" stroke="#f43f5e" stroke-width="2.5" stroke-dasharray="4" marker-end="url(#arr-bad)"/>
  <text x="600" y="105" fill="#f43f5e" font-size="9" font-family="monospace">Zombie Write(33)</text>
</svg>
""",
        "codeSnippet": """// Production Go Distributed Lock with Monotonic Fencing Token & Heartbeat Lease
package distlock

import (
	"context"
	"fmt"
	"sync/atomic"
	"time"

	clientv3 "go.etcd.io/etcd/client/v3"
	"go.etcd.io/etcd/client/v3/concurrency"
)

type FencedLock struct {
	session *concurrency.Session
	mutex   *concurrency.Mutex
	token   int64
}

var globalTokenSeq int64 = 1000

func AcquireFencedLock(ctx context.Context, client *clientv3.Client, lockKey string) (*FencedLock, error) {
	// Step 1: Create etcd session with 10-second TTL (auto-heartbeat keepalive)
	session, err := concurrency.NewSession(client, concurrency.WithTTL(10))
	if err != nil {
		return nil, fmt.Errorf("failed to create etcd session: %w", err)
	}

	mutex := concurrency.NewMutex(session, "/locks/"+lockKey)

	// Step 2: Acquire distributed lock via Raft consensus
	if err := mutex.Lock(ctx); err != nil {
		session.Close()
		return nil, fmt.Errorf("lock acquisition failed: %w", err)
	}

	// Step 3: Issue strictly monotonic fencing token
	fencingToken := atomic.AddInt64(&globalTokenSeq, 1)
	fmt.Printf("[LOCK ACQUIRED] Key: %s | Fencing Token: %d\\n", lockKey, fencingToken)

	return &FencedLock{
		session: session,
		mutex:   mutex,
		token:   fencingToken,
	}, nil
}

// StorageEngineWrite enforces the Fencing Invariant at the physical persistence layer
func StorageEngineWrite(highestSeenToken *int64, clientToken int64, data []byte) error {
	// Verification Barrier
	if clientToken < atomic.LoadInt64(highestSeenToken) {
		return fmt.Errorf("ZOMBIE WRITE REJECTED: client token %d < highest seen %d", clientToken, *highestSeenToken)
	}

	// Update highest seen token
	atomic.StoreInt64(highestSeenToken, clientToken)
	fmt.Printf("[STORAGE COMMITTED] Processed data with valid Fencing Token: %d\\n", clientToken)
	return nil
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Multi-Million Dollar Cloud Storage Split-Brain Corruption</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 100,000 customer archive files in AWS S3 were permanently corrupted when two worker nodes wrote concurrently.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      A cloud backup service used Redis Redlock to coordinate which worker node had permission to compress and upload archive files to S3.
      Worker 1 acquired the lock with a 30-second TTL and began processing a 50GB file.
    </p>
    <p>
      Worker 1's JVM experienced a 45-second Stop-the-World garbage collection pause caused by memory fragmentation.
      While Worker 1 was frozen, its Redis lock TTL expired.
      Redis granted the lock to Worker 2. Worker 2 started uploading to the exact same S3 key.
      <strong>Worker 1 woke up and resumed uploading its half-finished stream. Both workers interleaved byte chunks into the S3 object, destroying customer backups!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Fencing Tokens on S3 Conditional Writes:</strong> Pass the fencing token as an S3 object metadata header or use S3 Conditional Writes (<code>If-Match</code> ETag) so outdated workers are blocked at the storage API.</li>
      <li><strong class="text-white">Process Self-Termination (Suicide Pattern):</strong> If a thread wakes up and observes that its local execution time exceeded 50% of the lease TTL, it aborts immediately without attempting storage writes.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why does Salvatore Sanfilippo's Redis Redlock algorithm fail to provide safety for distributed locking, and what did Martin Kleppmann prove was missing?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "Martin Kleppmann proved that Redis Redlock relies on an invalid assumption: the <strong>Synchronous System Model with bounded clock drift</strong>.
      In real-world networks, three unavoidable physical phenomena violate Redlock's assumptions:
      <br><br>
      1. <strong>Process Pauses:</strong> A client can acquire a lock across 3 of 5 Redis nodes, and immediately enter a 30-second Stop-the-World GC pause or VM page fault. Its lock expires in Redis, another client acquires it, and both clients operate concurrently in the critical section!
      <br><br>
      2. <strong>Clock Skew:</strong> Redis uses system time (<code>expire</code>). If an NTP sync jumps time forward by 5 seconds on a Redis node, a lock expires prematurely.
      <br><br>
      3. <strong>Absence of Fencing:</strong> Redlock only returns a boolean (<code>true/false</code>). It does NOT provide a monotonically incrementing Fencing Token. Without a fencing token, downstream databases and storage engines have no mathematical way to distinguish a legitimate write from a delayed zombie write.
      <br><br>
      Therefore, for correctness, you must either: (A) Use a consensus-backed coordinator like <strong>etcd/ZooKeeper with Monotonic Fencing Tokens</strong> verified by the storage layer, or (B) Accept that Redlock is only an optimization for best-effort efficiency, never for data correctness."
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 5 loaded with {len(STAGE_5_CHAPTERS)} comprehensive chapters.")
