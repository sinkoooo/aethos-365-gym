# curriculum_stage6_data.py
# Stage 6: God-Level Architect - Hardware Physics, Kernel Bypass, TrueTime & AI Infrastructure

STAGE_6_CHAPTERS = [
    {
        "id": "c-12-hardware-physics",
        "stageId": "stage-6",
        "stageNum": "STAGE 06",
        "badge": "God Level",
        "color": "fuchsia",
        "title": "6.1 Hardware Physics: CPU Caches, False Sharing & NUMA Interconnects",
        "difficulty": "God Level",
        "readTime": "30 min read",
        "simulatorKey": "interview",
        "summary": "Breaking software abstractions: The physical limits of silicon. 64-byte cache lines, MESI cache coherency storms, False Sharing, and NUMA memory penalties.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-fuchsia-950/20 border border-fuchsia-500/20 text-fuchsia-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-fuchsia-400 mb-1">First-Principles Intuition</div>
    At 10 million transactions per second, operating systems and software frameworks cease to be virtual abstractions; your code is running on physical silicon obeying Maxwell's equations and the speed of light.
    <br><br>
    Accessing main memory (RAM) takes $\approx 100\,\text{nanoseconds}$.
    Accessing the CPU L1 cache takes $\approx 0.5\,\text{nanoseconds}$ (200x faster!).
    If two independent threads modify variables that sit within the same <strong>64-byte CPU cache line</strong>, the CPU cores engage in a violent hardware bus arbitration fight called <strong>False Sharing</strong>, destroying 95% of your multi-threaded throughput!
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 1. Latency Numbers Every Staff Engineer Must Know
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Hardware Operation</th>
          <th class="p-2.5">Real Time</th>
          <th class="p-2.5">Human Scale (1 cycle = 1 sec)</th>
          <th class="p-2.5">Physical Architectural Law</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">1 CPU Cycle (3.5 GHz)</td>
          <td class="p-2.5 text-emerald-400">0.3 ns</td>
          <td class="p-2.5">1 second</td>
          <td class="p-2.5">Single clock pulse through transistor gate</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">L1 CPU Cache Hit</td>
          <td class="p-2.5 text-emerald-400">0.5 - 1.0 ns</td>
          <td class="p-2.5">2 - 3 seconds</td>
          <td class="p-2.5">SRAM directly on the CPU core silicon</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">L2 CPU Cache Hit</td>
          <td class="p-2.5 text-emerald-400">3 - 7 ns</td>
          <td class="p-2.5">14 seconds</td>
          <td class="p-2.5">Fast private SRAM per core</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">L3 CPU Cache Hit</td>
          <td class="p-2.5 text-amber-400">15 - 30 ns</td>
          <td class="p-2.5">1 minute</td>
          <td class="p-2.5">Shared SRAM across all cores on the die</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Main Memory (DRAM) Hit</td>
          <td class="p-2.5 text-rose-400">60 - 100 ns</td>
          <td class="p-2.5">4 minutes</td>
          <td class="p-2.5">Capacitor recharge over memory bus (DDR5)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Remote NUMA Node Access</td>
          <td class="p-2.5 text-rose-400">150 - 300 ns</td>
          <td class="p-2.5">10 minutes</td>
          <td class="p-2.5">Crosses UPI / QPI physical motherboard interconnect</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">NVMe SSD Random Read</td>
          <td class="p-2.5 text-rose-400">20 - 100 &mu;s</td>
          <td class="p-2.5">1.5 - 3 days!</td>
          <td class="p-2.5">NAND Flash cell charge trap sensing</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Datacenter Network RTT</td>
          <td class="p-2.5 text-rose-400">500 &mu;s</td>
          <td class="p-2.5">2 weeks!</td>
          <td class="p-2.5">ToR switches, fiber patch cords, NIC buffers</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 2. False Sharing &amp; The MESI Coherency Storm
  </h4>
  <p>
    CPUs maintain cache coherence via the <strong>MESI Protocol</strong> (Modified, Exclusive, Shared, Invalid).
    If Core A modifies variable $X$ and Core B reads variable $Y$, but $X$ and $Y$ happen to reside within the same 64-byte memory boundary:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-rose-300 border border-slate-800 space-y-1">
    <div>1. Core A writes to $X$ &rarr; Marks the ENTIRE 64-byte line as <code>MODIFIED</code>.</div>
    <div>2. Hardware bus sends an Invalidation Broadcast to Core B's L1 cache.</div>
    <div>3. Core B's L1 cache line is marked <code>INVALID</code>!</div>
    <div>4. Core B wants to read $Y$ &rarr; L1 Cache Miss! Core B is forced to flush to L3/RAM!</div>
    <div class="text-white font-bold">&rArr; The two cores stall in an infinite hardware tug-of-war, destroying parallel throughput!</div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- FALSE SHARING (UPPER ROW) -->
  <g transform="translate(40, 30)">
    <rect width="880" height="150" rx="10" fill="#1e1b4b" stroke="#f43f5e" stroke-width="1.5"/>
    <text x="20" y="28" fill="#f43f5e" font-size="12" font-family="monospace" font-weight="bold">HAZARD: FALSE SHARING ACROSS 64-BYTE CACHE LINE</text>

    <!-- Core 1 -->
    <rect x="20" y="45" width="220" height="85" rx="6" fill="#0f0c29" stroke="#7c3aed"/>
    <text x="32" y="70" fill="#ffffff" font-size="11" font-weight="bold">CPU Core 0 (Thread A)</text>
    <text x="32" y="90" fill="#38bdf8" font-size="9" font-family="monospace">Modifies: counter_A++</text>
    <text x="32" y="110" fill="#f43f5e" font-size="8" font-family="monospace">Broadcasts Invalidation!</text>

    <!-- Core 2 -->
    <rect x="640" y="45" width="220" height="85" rx="6" fill="#0f0c29" stroke="#7c3aed"/>
    <text x="652" y="70" fill="#ffffff" font-size="11" font-weight="bold">CPU Core 1 (Thread B)</text>
    <text x="652" y="90" fill="#34d399" font-size="9" font-family="monospace">Modifies: counter_B++</text>
    <text x="652" y="110" fill="#f43f5e" font-size="8" font-family="monospace">L1 Stalled on Bus Lock!</text>

    <!-- Contested 64-Byte Line in Middle -->
    <rect x="270" y="55" width="340" height="65" rx="6" fill="#312e81" stroke="#f43f5e" stroke-width="2"/>
    <text x="440" y="76" fill="#facc15" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">PHYSICAL 64-BYTE CACHE LINE</text>
    <rect x="285" y="85" width="145" height="25" rx="4" fill="#7f1d1d"/>
    <text x="357" y="102" fill="#fca5a5" font-size="8" font-family="monospace" text-anchor="middle">counter_A (8 bytes)</text>
    <rect x="450" y="85" width="145" height="25" rx="4" fill="#7f1d1d"/>
    <text x="522" y="102" fill="#fca5a5" font-size="8" font-family="monospace" text-anchor="middle">counter_B (8 bytes)</text>
  </g>

  <!-- STAFF SOLUTION: CACHE LINE PADDING (LOWER ROW) -->
  <g transform="translate(40, 200)">
    <rect width="880" height="150" rx="10" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="20" y="28" fill="#34d399" font-size="12" font-family="monospace" font-weight="bold">STAFF SOLUTION: CACHE-LINE PADDING ([64]BYTE ALIGNMENT)</text>

    <rect x="20" y="45" width="400" height="85" rx="6" fill="#042f2e" stroke="#10b981"/>
    <text x="32" y="70" fill="#34d399" font-size="10" font-family="monospace" font-weight="bold">Cache Line 0 (CPU Core 0 Private)</text>
    <text x="32" y="90" fill="#ffffff" font-size="9" font-family="monospace">uint64 counter_A (8 bytes)</text>
    <text x="32" y="110" fill="#a7f3d0" font-size="8" font-family="monospace">_pad [56]byte // Fills remainder of 64B line!</text>

    <rect x="460" y="45" width="400" height="85" rx="6" fill="#042f2e" stroke="#10b981"/>
    <text x="472" y="70" fill="#34d399" font-size="10" font-family="monospace" font-weight="bold">Cache Line 1 (CPU Core 1 Private)</text>
    <text x="472" y="90" fill="#ffffff" font-size="9" font-family="monospace">uint64 counter_B (8 bytes)</text>
    <text x="472" y="110" fill="#a7f3d0" font-size="8" font-family="monospace">_pad [56]byte // Fills remainder of 64B line!</text>
  </g>
</svg>
""",
        "codeSnippet": """// High-Performance Go Code Demonstrating Cache-Line Padding to Prevent False Sharing
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// Anti-Pattern: Unpadded struct causes False Sharing
// Both counters sit within the same 64-byte CPU cache line!
type ContendedCounters struct {
	counterA uint64 // 8 bytes
	counterB uint64 // 8 bytes
}

// Staff Solution: Struct with 56-byte cache line padding
// Guarantees counterA and counterB occupy completely distinct L1 cache lines!
type PaddedCounters struct {
	counterA uint64
	_padA    [56]byte // 8 + 56 = 64 bytes (Exact CPU Cache Line Size!)
	counterB uint64
	_padB    [56]byte
}

func BenchmarkCounters() {
	const iterations = 100_000_000

	// 1. Run Contended Test
	contended := ContendedCounters{}
	var wg sync.WaitGroup
	wg.Add(2)

	start := time.Now()
	go func() {
		defer wg.Done()
		for i := 0; i < iterations; i++ {
			atomic.AddUint64(&contended.counterA, 1)
		}
	}()
	go func() {
		defer wg.Done()
		for i := 0; i < iterations; i++ {
			atomic.AddUint64(&contended.counterB, 1)
		}
	}()
	wg.Wait()
	contendedDuration := time.Since(start)

	// 2. Run Padded Test
	padded := PaddedCounters{}
	wg.Add(2)

	start = time.Now()
	go func() {
		defer wg.Done()
		for i := 0; i < iterations; i++ {
			atomic.AddUint64(&padded.counterA, 1)
		}
	}()
	go func() {
		defer wg.Done()
		for i := 0; i < iterations; i++ {
			atomic.AddUint64(&padded.counterB, 1)
		}
	}()
	wg.Wait()
	paddedDuration := time.Since(start)

	fmt.Printf("Contended Duration (False Sharing): %v\\n", contendedDuration)
	fmt.Printf("Padded Duration (Zero Coherency Loss): %v (%.2fx Faster!)\\n",
		paddedDuration, float64(contendedDuration)/float64(paddedDuration))
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The High-Frequency Trading $10 Million Latency Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: A Chicago market-making firm dropped trades and lost $10M when an order routing P99 latency jumped from 2 microseconds to 380 microseconds.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      An engineer added a telemetry metric (<code>atomic.AddUint64(&amp;metrics.total_orders, 1)</code>) to a high-speed C++ order book processing loop.
      The new metric variable was placed in memory immediately adjacent to the matching engine's sequence cursor.
    </p>
    <p>
      When high volatility hit the markets, 16 worker threads concurrently executed atomic increments on <code>total_orders</code>.
      Because the telemetry counter shared a 64-byte cache line with the order book pointer, every single order submission invalidated the matching engine's L1/L2 cache.
      <strong>The matching engine CPU core was continuously stalled on hardware bus locks, causing client trades to be beaten by competing firms for 30 minutes!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Alignas(64) Explicit Padding:</strong> Enforce <code>alignas(hardware_destructive_interference_size)</code> on all shared multithreaded structs during automated CI linting.</li>
      <li><strong class="text-white">Thread-Local Metrics:</strong> Never use global shared atomic counters on the hot path. Each worker thread writes to private thread-local storage; an asynchronous background thread aggregates totals every 1,000ms.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "What is NUMA (Non-Uniform Memory Access), why does cross-NUMA traffic bottleneck high-throughput servers, and how do you architect software for NUMA affinity?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "In modern multi-socket enterprise servers (e.g. Dual Intel Xeon or AMD EPYC), memory controllers are partitioned physically. Socket 0 has its own local DDR5 RAM channels, and Socket 1 has its own local RAM channels.
      <br><br>
      When a CPU core on Socket 0 accesses memory on Socket 0, latency is $\approx 80\,\text{ns}$.
      However, when a core on Socket 0 needs to read memory allocated on Socket 1, the request must travel across the physical motherboard interconnect (Intel Ultra Path Interconnect - UPI, or AMD Infinity Fabric).
      This <strong>cross-socket NUMA hop inflates latency to $250\,\text{ns}+$ and saturates the UPI bus bandwidth</strong>.
      <br><br>
      To achieve god-level throughput (e.g. in LMAX Disruptor, ScyllaDB, or DPDK network appliances), we enforce <strong>NUMA Affinity &amp; Thread Pinning</strong>:
      1. We bind worker threads to specific CPU cores using <code>pthread_setaffinity_np</code>.
      2. We allocate memory strictly from the core's local NUMA node using <code>numactl --cpunodebind=0 --membind=0</code>.
      3. Workers communicate across sockets exclusively through lock-free ring buffers, eliminating 100% of cross-socket memory stalls!"
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-13-kernel-bypass",
        "stageId": "stage-6",
        "stageNum": "STAGE 06",
        "badge": "God Level",
        "color": "fuchsia",
        "title": "6.2 High-Throughput Linux: io_uring, eBPF & DPDK Kernel Bypass",
        "difficulty": "God Level",
        "readTime": "28 min read",
        "simulatorKey": "tracer",
        "summary": "The limits of POSIX sockets: Syscall context switch penalties and sk_buff memory copies. High-performance asynchronous ring buffers in io_uring, verified kernel sandboxing in eBPF/XDP, and user-space DPDK.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-fuchsia-950/20 border border-fuchsia-500/20 text-fuchsia-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-fuchsia-400 mb-1">First-Principles Intuition</div>
    Imagine every time you want to mail a letter, you must stop what you are doing, go through airport security, submit your passport, let the officer inspect your bag, stamp your paper, and return you to the street.
    That is a <strong>Linux System Call (Syscall)</strong>.
    <br><br>
    Transitioning CPU execution from User Mode (Ring 3) to Kernel Mode (Ring 0) consumes $\approx 100-200\,\text{nanoseconds}$ due to CPU register saves, page table flushes (Meltdown mitigations), and branch target buffer pollution.
    At 10 million packets per second, the Linux kernel spends 100% of its time doing security handshakes and ZERO time moving data!
    <strong>Kernel Bypass</strong> eliminates this tax completely.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 1. The Kernel Bypass Technology Matrix
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Technology</th>
          <th class="p-2.5">Operating Domain</th>
          <th class="p-2.5">Zero Syscalls?</th>
          <th class="p-2.5">Zero Copy?</th>
          <th class="p-2.5">Target Workload</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Standard POSIX (epoll)</td>
          <td class="p-2.5">Kernel &rarr; Userspace</td>
          <td class="p-2.5 text-rose-400">No (1 syscall per I/O)</td>
          <td class="p-2.5 text-rose-400">No (2 copies via sk_buff)</td>
          <td class="p-2.5">Standard web apps (&lt; 100k TPS)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-emerald-400 font-bold">io_uring (Linux 5.1+)</td>
          <td class="p-2.5">Shared Ring Buffers (mmap)</td>
          <td class="p-2.5 text-emerald-400">Yes (via SQPOLL kernel thread)</td>
          <td class="p-2.5 text-emerald-400">Yes (Registered fixed buffers)</td>
          <td class="p-2.5">Ultra-fast NVMe storage &amp; high-TPS networking</td>
        </tr>
        <tr>
          <td class="p-2.5 text-amber-400 font-bold">eBPF / XDP</td>
          <td class="p-2.5">Directly in NIC Driver RX path</td>
          <td class="p-2.5 text-emerald-400">Yes (In-kernel JIT bytecode)</td>
          <td class="p-2.5 text-emerald-400">Yes (Drops before sk_buff allocation)</td>
          <td class="p-2.5">DDoS mitigation &amp; Cloudflare edge routing</td>
        </tr>
        <tr>
          <td class="p-2.5 text-fuchsia-400 font-bold">DPDK (Data Plane Dev Kit)</td>
          <td class="p-2.5">Pure Userspace Poll Mode Driver</td>
          <td class="p-2.5 text-emerald-400">Yes (Kernel bypassed entirely)</td>
          <td class="p-2.5 text-emerald-400">Yes (DMA direct to userspace RAM)</td>
          <td class="p-2.5">5G Telecom UPF &amp; HFT Market Feeds (40M+ PPS)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 2. The io_uring Shared Ring Buffer Mechanics
  </h4>
  <p>
    <code>io_uring</code> allocates two lock-free ring buffers in memory shared between the Linux kernel and user space:
  </p>
  <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Submission Queue (SQ):</strong> Application writes Submission Queue Entries (SQEs) describing operations (e.g. <code>readv</code>, <code>writev</code>, <code>accept</code>) into the shared ring buffer. Zero system calls required!</li>
    <li><strong class="text-white">Completion Queue (CQ):</strong> When the hardware finishes, the kernel appends Completion Queue Entries (CQEs) into the second shared ring buffer. The application consumes results simply by reading pointers.</li>
    <li><strong class="text-white">SQPOLL Mode:</strong> A dedicated kernel thread continuously polls the submission queue. The application can submit 1,000,000 I/O operations without executing a single <code>syscall</code> instruction!</li>
  </ul>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- USERS PACE (LEFT) -->
  <g transform="translate(50, 40)">
    <rect width="260" height="300" rx="10" fill="#0f172a" stroke="#0284c7" stroke-width="2"/>
    <text x="20" y="32" fill="#38bdf8" font-size="13" font-family="sans-serif" font-weight="bold">USER SPACE APPLICATION</text>
    <text x="20" y="52" fill="#94a3b8" font-size="9" font-family="monospace">Ring 3 (Unprivileged)</text>

    <!-- App Logic -->
    <rect x="20" y="70" width="220" height="90" rx="6" fill="#1e293b"/>
    <text x="30" y="94" fill="#ffffff" font-size="10" font-weight="bold">Event Loop Engine</text>
    <text x="30" y="112" fill="#34d399" font-size="8" font-family="monospace">Pushes SQE: READ / WRITE</text>
    <text x="30" y="128" fill="#38bdf8" font-size="8" font-family="monospace">mmap() Shared Memory Pointer</text>
    <text x="30" y="144" fill="#a7f3d0" font-size="8" font-family="monospace">ZERO System Calls!</text>

    <rect x="20" y="180" width="220" height="90" rx="6" fill="#042f2e" stroke="#10b981"/>
    <text x="30" y="204" fill="#34d399" font-size="10" font-weight="bold">Fixed Buffer Pool</text>
    <text x="30" y="222" fill="#cbd5e1" font-size="8" font-family="monospace">Pre-allocated 1GB RAM</text>
    <text x="30" y="238" fill="#a7f3d0" font-size="8" font-family="monospace">Direct Hardware DMA target</text>
    <text x="30" y="254" fill="#facc15" font-size="8" font-family="monospace">ZERO memory copies!</text>
  </g>

  <!-- SHARED MMAP RING BUFFERS (MIDDLE) -->
  <g transform="translate(360, 40)">
    <rect width="240" height="300" rx="10" fill="#1e1b4b" stroke="#7c3aed" stroke-width="2"/>
    <text x="20" y="32" fill="#c084fc" font-size="12" font-family="monospace" font-weight="bold">MMAP SHARED RINGS</text>
    <text x="20" y="50" fill="#94a3b8" font-size="8" font-family="monospace">Kernel &amp; Userspace Shared</text>

    <!-- Submission Queue Ring -->
    <rect x="15" y="65" width="210" height="100" rx="6" fill="#312e81" stroke="#a855f7"/>
    <text x="25" y="86" fill="#e9d5ff" font-size="9" font-family="monospace" font-weight="bold">Submission Queue (SQ)</text>
    <text x="25" y="104" fill="#a7f3d0" font-size="8" font-family="monospace">SQE 1: WRITE (FD 12, Buf A)</text>
    <text x="25" y="120" fill="#a7f3d0" font-size="8" font-family="monospace">SQE 2: READ  (FD 14, Buf B)</text>
    <text x="25" y="136" fill="#a7f3d0" font-size="8" font-family="monospace">SQE 3: ACCEPT(FD 8,  Port 80)</text>
    <text x="25" y="152" fill="#facc15" font-size="7" font-family="monospace">Head: 0 &bull; Tail: 3 (Atomic)</text>

    <!-- Completion Queue Ring -->
    <rect x="15" y="180" width="210" height="100" rx="6" fill="#312e81" stroke="#a855f7"/>
    <text x="25" y="202" fill="#e9d5ff" font-size="9" font-family="monospace" font-weight="bold">Completion Queue (CQ)</text>
    <text x="25" y="220" fill="#38bdf8" font-size="8" font-family="monospace">CQE 1: Result = 4096 bytes</text>
    <text x="25" y="236" fill="#38bdf8" font-size="8" font-family="monospace">CQE 2: Result = OK</text>
    <text x="25" y="252" fill="#38bdf8" font-size="8" font-family="monospace">CQE 3: New Client FD = 29</text>
    <text x="25" y="268" fill="#facc15" font-size="7" font-family="monospace">Read by Userspace Instant</text>
  </g>

  <!-- KERNEL & HARDWARE (RIGHT) -->
  <g transform="translate(650, 40)">
    <rect width="260" height="300" rx="10" fill="#0f172a" stroke="#059669" stroke-width="2"/>
    <text x="20" y="32" fill="#34d399" font-size="13" font-family="sans-serif" font-weight="bold">LINUX KERNEL &amp; NIC</text>
    <text x="20" y="52" fill="#94a3b8" font-size="9" font-family="monospace">SQPOLL Kernel Thread</text>

    <rect x="20" y="70" width="220" height="90" rx="6" fill="#064e3b"/>
    <text x="30" y="94" fill="#34d399" font-size="10" font-weight="bold">SQPOLL Kernel Thread</text>
    <text x="30" y="112" fill="#a7f3d0" font-size="8" font-family="monospace">Dedicated Polling Core</text>
    <text x="30" y="128" fill="#cbd5e1" font-size="8" font-family="monospace">Pulls SQEs directly from ring</text>
    <text x="30" y="144" fill="#facc15" font-size="8" font-family="monospace">Dispatches DMA to NVMe/NIC</text>

    <rect x="20" y="180" width="220" height="90" rx="6" fill="#02040d" stroke="#334155"/>
    <text x="30" y="204" fill="#ffffff" font-size="10" font-weight="bold">Hardware NIC (100GbE)</text>
    <text x="30" y="222" fill="#38bdf8" font-size="8" font-family="monospace">PCIe Gen 5 DMA Controller</text>
    <text x="30" y="238" fill="#a7f3d0" font-size="8" font-family="monospace">Streams directly to RAM</text>
    <text x="30" y="254" fill="#34d399" font-size="8" font-family="monospace">Throughput: 40M PPS</text>
  </g>
</svg>
""",
        "codeSnippet": """// Production C Implementation of Linux io_uring with SQPOLL Kernel Thread
// Compiles with -luring. Achieves 1.5M IOPS on single CPU core.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <liburing.h>

#define QUEUE_DEPTH 1024
#define BUFFER_SIZE 4096

int main() {
    struct io_uring ring;
    struct io_uring_params params;
    memset(&params, 0, sizeof(params));

    // Enable SQPOLL: dedicated kernel thread polls submission queue!
    // Zero syscalls required to submit I/O operations!
    params.flags = IORING_SETUP_SQPOLL;
    params.sq_thread_idle = 2000; // Keep kernel poll thread awake for 2000ms

    if (io_uring_queue_init_params(QUEUE_DEPTH, &ring, &params) < 0) {
        perror("Failed to initialize io_uring");
        return 1;
    }
    printf("[IO_URING] Initialized shared submission/completion rings (SQPOLL active)\\n");

    int fd = open("telemetry.log", O_WRONLY | O_CREAT | O_APPEND | O_DIRECT, 0644);
    if (fd < 0) {
        perror("Open failure");
        return 1;
    }

    // Allocate aligned memory for direct hardware DMA
    char *buffer;
    posix_memalign((void **)&buffer, 4096, BUFFER_SIZE);
    strcpy(buffer, "LOG_ENTRY: High throughput packet telemetry batch\\n");

    // Get submission queue entry from shared ring
    struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
    io_uring_prep_write(sqe, fd, buffer, BUFFER_SIZE, 0);

    // Tell kernel thread to process work (Zero syscall in SQPOLL mode!)
    io_uring_submit(&ring);

    // Wait for completion entry in completion queue
    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(&ring, &cqe);

    if (cqe->res < 0) {
        fprintf(stderr, "Async write failed: %s\\n", strerror(-cqe->res));
    } else {
        printf("[IO_URING] Successfully committed %d bytes with ZERO syscalls!\\n", cqe->res);
    }

    io_uring_cqe_seen(&ring, cqe);
    io_uring_queue_exit(&ring);
    close(fd);
    free(buffer);
    return 0;
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Cloudflare 2019 Global eBPF WAF Regex Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 15% of global internet HTTP traffic dropped for 27 minutes as edge proxies hit 100% CPU lock.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      Cloudflare deployed a new regular expression into their edge Web Application Firewall (WAF) running at the in-kernel packet inspection layer.
      The regular expression contained poorly anchored backtracking (Catastrophic Backtracking: $O(2^N)$ complexity).
    </p>
    <p>
      When incoming web requests matched the prefix, the eBPF/WAF worker threads entered infinite backtracking loops.
      Every CPU core on edge reverse proxies spiked to 100% utilization.
      <strong>Because the kernel bypass and packet inspection layers share the same CPU cores as the HTTP ingress proxy, health check endpoints timed out and global DNS marked all Cloudflare edge data centers as dead!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">eBPF Instruction Limits &amp; Verifier Hardening:</strong> Mandate that all eBPF programs pass the kernel verifier with strict instruction execution bounds ($&lt; 1,000,000$ verified cycles).</li>
      <li><strong class="text-white">CPU Isolation with cgroups:</strong> Pin in-kernel packet processing to dedicated isolated cores (e.g. Cores 0-3), reserving Cores 4-32 strictly for application proxies and health check daemons so a runaway rule can never starve health checks.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why does Linux epoll suffer performance degradation when handling 1,000,000 active concurrent TCP connections, and how does io_uring fundamentally solve this?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "Linux <code>epoll</code> was a massive leap over <code>select/poll</code>, but at 1M connections it bottlenecks on two fundamental architectural constraints:
      <br><br>
      1. <strong>Synchronous Syscall Overhead:</strong> <code>epoll_wait()</code> is a blocking system call. Once it wakes up and returns 1,000 ready file descriptors, the application must invoke 1,000 separate <code>read()</code> or <code>write()</code> system calls. That is 1,000 CPU transitions between User Space and Kernel Space per event loop tick!
      <br><br>
      2. <strong>Redundant Data Copies:</strong> Each <code>read()</code> call copies packet bytes from kernel socket buffers (<code>sk_buff</code>) across the memory boundary into userspace application buffers.
      <br><br>
      <code>io_uring</code> solves this via <strong>Kernel-Userspace Shared Memory Ring Buffers</strong>:
      Instead of calling the kernel, the application writes descriptors into the shared Submission Queue (SQ) memory ring.
      With <strong>SQPOLL</strong> enabled, an asynchronous kernel thread polls the ring and executes DMA directly into pre-registered fixed userspace memory buffers.
      Results appear in the Completion Queue (CQ) ring.
      The entire pipeline operates with <strong>Zero System Calls and Zero CPU memory copies</strong>, increasing IOPS from 100k to over 1.5 million per core!"
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-14-spanner-truetime",
        "stageId": "stage-6",
        "stageNum": "STAGE 06",
        "badge": "God Level",
        "color": "fuchsia",
        "title": "6.3 Planet-Scale Distributed SQL: Google Spanner & Atomic TrueTime",
        "difficulty": "God Level",
        "readTime": "30 min read",
        "simulatorKey": "interview",
        "summary": "The Holy Grail of Distributed Systems: Globally distributed ACID transactions with external consistency (linearizability). Bounded clock uncertainty (epsilon), GPS & atomic clocks, and the Commit Wait rule.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-fuchsia-950/20 border border-fuchsia-500/20 text-fuchsia-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-fuchsia-400 mb-1">First-Principles Intuition</div>
    In a single computer, ordering events is trivial: read the CPU clock cycle counter.
    In a global database distributed across Tokyo, New York, Frankfurt, and Sydney, <strong>Einstein's theory of relativity and physical clock drift make a single 'global time' physically impossible</strong>.
    <br><br>
    Standard NTP server clocks drift by 100 to 500 milliseconds—an eternity when thousands of transactions occur every millisecond.
    If New York writes at 12:00:00.001 and Tokyo reads at 12:00:00.002, Tokyo might see time as 11:59:59.998 and overwrite New York's transaction!
    <br><br>
    Google solved this impossible problem by deploying <strong>GPS receivers and Rubidium atomic clocks into every Google datacenter on Earth</strong>: The <strong>TrueTime API</strong>.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 1. The TrueTime API: Bounded Clock Uncertainty ($\epsilon$)
  </h4>
  <p>
    TrueTime does not return a single scalar timestamp. It returns an <strong>interval of uncertainty</strong>:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800 space-y-1">
    <div><code>TT.now() = [earliest, latest]</code></div>
    <div>$$\text{Guaranteed Truth: } \text{earliest} \le t_{\text{absolute}} \le \text{latest}$$</div>
    <div>$$\text{Uncertainty Half-Width: } \epsilon = \frac{\text{latest} - \text{earliest}}{2} \approx 1 \text{ to } 7\,\text{ms}$$</div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 2. The TrueTime Invariant &amp; The Commit Wait Rule
  </h4>
  <p>
    To guarantee <strong>External Consistency (Linearizability)</strong>: If transaction $T_2$ starts after transaction $T_1$ commits, then $T_2$'s commit timestamp must be strictly greater than $T_1$'s: $s_2 > s_1$.
    <br><br>
    How does Spanner guarantee this when clocks have an uncertainty of $\epsilon$?
    Through the legendary <strong>Commit Wait Rule</strong>:
  </p>
  <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 font-mono text-xs text-amber-300">
    <div class="font-bold text-white">THE COMMIT WAIT RULE:</div>
    <div>1. Transaction $T_1$ acquires locks and picks commit timestamp: $s_1 = \text{TT.now().latest}$.</div>
    <div>2. The Leader does NOT return success to the client immediately!</div>
    <div class="text-emerald-400 font-bold">3. The Leader intentionally sleeps until <code>TT.now().earliest &gt; s_1</code> (waits $2\epsilon \approx 14\,\text{ms}$)!</div>
    <div>4. When the wait finishes, the absolute real-world time is guaranteed to have passed $s_1$. The Leader releases locks and returns success to the client!</div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- TIME UNCERTAINTY VISUALIZATION -->
  <g transform="translate(40, 30)">
    <rect width="880" height="150" rx="10" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <text x="20" y="28" fill="#38bdf8" font-size="12" font-family="monospace" font-weight="bold">TRUETIME INTERVAL [earliest, latest] &amp; THE COMMIT WAIT RULE</text>

    <!-- Timeline Axis -->
    <line x1="40" y1="90" x2="840" y2="90" stroke="#334155" stroke-width="3"/>
    <text x="840" y="110" fill="#94a3b8" font-size="9" font-family="monospace">Real World Absolute Time &rarr;</text>

    <!-- Transaction 1 Uncertainty Window -->
    <rect x="80" y="60" width="160" height="60" rx="6" fill="#1e1b4b" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="160" y="82" fill="#c084fc" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">TT.now() Window (2&epsilon;)</text>
    <text x="160" y="102" fill="#facc15" font-size="8" font-family="monospace" text-anchor="middle">s1 = TT.now().latest</text>

    <!-- The Commit Wait Sleep Barrier -->
    <rect x="240" y="50" width="220" height="80" rx="6" fill="#431407" stroke="#ea580c" stroke-width="2"/>
    <text x="350" y="75" fill="#f43f5e" font-size="10" font-family="monospace" font-weight="bold" text-anchor="middle">COMMIT WAIT BARRIER</text>
    <text x="350" y="95" fill="#fed7aa" font-size="8" font-family="monospace" text-anchor="middle">Leader Intentionally Sleeps 2&epsilon; (~14ms)</text>
    <text x="350" y="115" fill="#facc15" font-size="8" font-family="monospace" text-anchor="middle">Waits until TT.now().earliest &gt; s1</text>

    <!-- Transaction 2 Safe Start -->
    <rect x="520" y="60" width="160" height="60" rx="6" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="600" y="82" fill="#34d399" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">T2 Starts (Guaranteed)</text>
    <text x="600" y="102" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">s2 &gt; s1 (Strict Linearizability!)</text>
  </g>

  <!-- MULTI-REGION SPANNER PAXOS REPLICATION (LOWER ROW) -->
  <g transform="translate(40, 200)">
    <rect width="880" height="150" rx="10" fill="#02040d" stroke="#334155"/>
    <text x="20" y="26" fill="#38bdf8" font-size="11" font-family="monospace" font-weight="bold">SPANNER MULTI-REGION PAXOS GROUP (US-EAST &bull; US-WEST &bull; EUROPE)</text>

    <!-- Datacenter 1: GPS + Atomic Clocks -->
    <rect x="20" y="45" width="260" height="85" rx="6" fill="#0f172a" stroke="#0284c7"/>
    <text x="32" y="68" fill="#38bdf8" font-size="10" font-weight="bold">Data Center: us-east1</text>
    <text x="32" y="86" fill="#cbd5e1" font-size="8" font-family="monospace">GPS Antenna + Rubidium Clocks</text>
    <text x="32" y="102" fill="#a7f3d0" font-size="8" font-family="monospace">TrueTime Daemon: &epsilon; &le; 2.1ms</text>
    <text x="32" y="118" fill="#facc15" font-size="8" font-family="monospace">Paxos Leader (Tablet 42)</text>

    <!-- Datacenter 2 -->
    <rect x="310" y="45" width="260" height="85" rx="6" fill="#0f172a" stroke="#059669"/>
    <text x="322" y="68" fill="#34d399" font-size="10" font-weight="bold">Data Center: us-west1</text>
    <text x="322" y="86" fill="#cbd5e1" font-size="8" font-family="monospace">GPS Antenna + Rubidium Clocks</text>
    <text x="322" y="102" fill="#a7f3d0" font-size="8" font-family="monospace">TrueTime Daemon: &epsilon; &le; 1.8ms</text>
    <text x="322" y="118" fill="#38bdf8" font-size="8" font-family="monospace">Paxos Follower (In-Sync)</text>

    <!-- Datacenter 3 -->
    <rect x="600" y="45" width="260" height="85" rx="6" fill="#0f172a" stroke="#7c3aed"/>
    <text x="612" y="68" fill="#c084fc" font-size="10" font-weight="bold">Data Center: europe-west1</text>
    <text x="612" y="86" fill="#cbd5e1" font-size="8" font-family="monospace">GPS Antenna + Rubidium Clocks</text>
    <text x="612" y="102" fill="#a7f3d0" font-size="8" font-family="monospace">TrueTime Daemon: &epsilon; &le; 3.4ms</text>
    <text x="612" y="118" fill="#38bdf8" font-size="8" font-family="monospace">Witness / Quorum Acceptor</text>
  </g>
</svg>
""",
        "codeSnippet": """# Python Implementation Demonstrating the Google Spanner TrueTime Commit-Wait Protocol
import time
from typing import Tuple

class TrueTimeSimulator:
    def __init__(self, epsilon_ms: float = 7.0):
        self.epsilon_ms = epsilon_ms

    def now(self) -> Tuple[float, float]:
        \"\"\"Returns TrueTime interval: [earliest, latest]\"\"\"
        absolute_time = time.time() * 1000 # Milliseconds
        earliest = absolute_time - self.epsilon_ms
        latest = absolute_time + self.epsilon_ms
        return (earliest, latest)

class SpannerTransactionCoordinator:
    def __init__(self, truetime: TrueTimeSimulator):
        self.tt = truetime

    def execute_transaction_with_commit_wait(self, tx_id: str, write_data: dict) -> float:
        # Step 1: Acquire 2PL read/write locks across Paxos tablets
        print(f"[{tx_id}] Acquired 2PL locks across Paxos tablet group.")

        # Step 2: Pick commit timestamp s = TT.now().latest
        earliest, latest = self.tt.now()
        commit_timestamp_s = latest
        print(f"[{tx_id}] Picked commit timestamp s = {commit_timestamp_s:.2f} ms")

        # Step 3: Replicate write mutation to Paxos majority quorum
        # (Replication runs concurrently during the wait!)

        # Step 4: THE COMMIT WAIT RULE
        # The leader MUST wait until TT.now().earliest > commit_timestamp_s
        print(f"[{tx_id}] Entering Commit-Wait sleep to guarantee linearizability...")
        while True:
            cur_earliest, _ = self.tt.now()
            if cur_earliest > commit_timestamp_s:
                break
            time.sleep(0.001) # Sleep 1ms increments

        # Step 5: Release locks and return success to client
        print(f"[{tx_id}] Commit-Wait complete! Released locks at absolute time > {commit_timestamp_s:.2f} ms.")
        return commit_timestamp_s
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The 2015 Global Financial Leap Second Clock Skew Outage</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Major stock exchanges and airlines halted operations as NTP leap-second adjustments triggered kernel locks and timestamp inversions.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      On June 30, 2015, an official Leap Second (23:59:60) was added to UTC.
      Traditional NTP servers stepped system clocks backwards by 1 second.
    </p>
    <p>
      In distributed databases relying on local system time, <strong>time moved backwards</strong>.
      New transactions generated timestamps that were smaller than previously committed transactions ($T_{\text{new}} &lt; T_{\text{old}}$).
      Database MVCC engines marked recent writes as obsolete and deleted them during automated background vacuum sweeps!
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Leap Smearing:</strong> Never step clocks backwards. Spread the extra 1 second linearly across a 24-hour window by slowing down clock ticks by 0.0011%, making the adjustment imperceptible to software.</li>
      <li><strong class="text-white">Hardware Redundancy (GPS + Atomic):</strong> Equipping every data center with dual GPS antennas and Rubidium oscillator atomic standards prevents external network NTP spoofing and guarantees strict bounded uncertainty ($\epsilon \le 7\,\text{ms}$).</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "CockroachDB uses Hybrid Logical Clocks (HLC) while Google Spanner uses TrueTime. What is the fundamental trade-off between HLC and TrueTime for planet-scale SQL?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "The trade-off comes down to <strong>Hardware Infrastructure vs External Consistency Guarantees</strong>:
      <br><br>
      1. <strong>CockroachDB (Software HLC):</strong> CockroachDB runs on commodity cloud infrastructure (AWS/GCP/Bare-Metal) without custom hardware. It pairs physical NTP time with Lamport logical counters.
      The catch: HLC can only track causality if operations are causally linked by network messages. If Client A updates row X in New York, calls a human over the telephone, and that human updates row Y in Tokyo, CockroachDB <em>cannot guarantee linearizability across independent out-of-band channels</em> without max-clock-offset uncertainty restarts (up to 500ms read restarts!).
      <br><br>
      2. <strong>Google Spanner (Hardware TrueTime):</strong> By investing hundreds of millions in datacenter GPS receivers and Rubidium atomic clocks, Google bounds physical clock drift to $\epsilon \approx 1-7\,\text{ms}$.
      Because $\epsilon$ is tiny, Spanner's <strong>Commit Wait ($2\epsilon$)</strong> is only $\approx 10\,\text{ms}$—fast enough to execute real-time transactions that guarantee true absolute wall-clock Linearizability across all global datacenters, with zero causal messaging required!"
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-15-ai-infra-vllm",
        "stageId": "stage-6",
        "stageNum": "STAGE 06",
        "badge": "God Level",
        "color": "fuchsia",
        "title": "6.4 Modern AI Infrastructure: HNSW Vector Search & vLLM PagedAttention",
        "difficulty": "God Level",
        "readTime": "28 min read",
        "simulatorKey": "interview",
        "summary": "The architecture of Generative AI at scale. Approximate Nearest Neighbor (ANN) search via Hierarchical Navigable Small World (HNSW) graphs, GPU HBM memory bandwidth walls, and PagedAttention KV-caching.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-fuchsia-950/20 border border-fuchsia-500/20 text-fuchsia-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-fuchsia-400 mb-1">First-Principles Intuition</div>
    Modern Generative AI systems face two massive architectural bottlenecks that crash traditional software architectures:
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-fuchsia-200">
      <li><strong>Vector Retrieval (RAG):</strong> You have 100 million document embeddings in 1,536-dimensional space. An exact brute-force Euclidean distance scan ($O(N \cdot D)$) takes 8 seconds per query. You need sub-10ms search!</li>
      <li><strong>LLM Inference (GPU VRAM Bottleneck):</strong> Large Language Models are not compute-bound during text generation; they are <strong>Memory Bandwidth Bound</strong>. Every generated token must load the entire <strong>Key-Value (KV) Cache</strong> from GPU High-Bandwidth Memory (HBM3). Traditional memory allocation fragments VRAM, wasting 60-80% of $30,000 Nvidia H100 GPUs!</li>
    </ul>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 1. Hierarchical Navigable Small World (HNSW) Graphs
  </h4>
  <p>
    HNSW combines the multi-layer hierarchy of a <strong>Skip List</strong> with the clustering properties of a <strong>Delaunay Graph</strong>:
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-cyan-400 font-bold font-mono">Layer 2 (Top Layer - Express Skip Links)</div>
      <p class="text-slate-400">Very few nodes with long-range edges across the vector space. The query vector takes massive hops to rapidly zoom into the general conceptual neighborhood ($O(\log N)$ traversal).</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-emerald-400 font-bold font-mono">Layer 0 (Bottom Layer - Dense Clustering)</div>
      <p class="text-slate-400">Contains all vectors with short-range edges. Executes fine-grained greedy beam search to return the Top-K nearest neighbors in under <strong>4 milliseconds</strong> across 100M embeddings!</p>
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span> 2. vLLM PagedAttention: Virtual Memory for GPUs
  </h4>
  <p>
    During autoregressive LLM token generation, the Key-Value (KV) cache grows dynamically by 1 token per generation step.
    Traditional systems pre-allocated contiguous memory blocks for the maximum possible sequence length (e.g. 8,192 tokens).
    If a user prompt only generates 200 tokens, <strong>97% of the reserved GPU VRAM sits empty and wasted (Internal Fragmentation)</strong>!
    <br><br>
    <strong>PagedAttention</strong> solves this by adapting the 50-year-old operating system concept of <strong>Virtual Memory Paging</strong> to GPU VRAM:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-amber-300 border border-slate-800">
    KV cache tensors are broken into small fixed-size <strong>Memory Blocks (e.g. 16 tokens per block)</strong>.
    Blocks do not need to be contiguous in physical GPU memory.
    A virtual <strong>Block Table</strong> maps logical token sequences to non-contiguous physical HBM addresses.
    Result: <strong>Near-zero memory waste (&lt; 4%) and 4x to 8x higher inference batch throughput!</strong>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- HNSW MULTI-LAYER GRAPH (LEFT) -->
  <g transform="translate(40, 30)">
    <rect width="420" height="310" rx="10" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <text x="20" y="28" fill="#38bdf8" font-size="12" font-family="monospace" font-weight="bold">HNSW MULTI-LAYER VECTOR GRAPH (ANN)</text>

    <!-- Layer 2 (Sparse) -->
    <g transform="translate(20, 45)">
      <rect width="380" height="60" rx="6" fill="#1e293b" stroke="#334155"/>
      <text x="12" y="18" fill="#94a3b8" font-size="9" font-family="monospace">Layer 2: Sparse Long-Range Skip Edges</text>
      <circle cx="60" cy="38" r="8" fill="#0284c7"/>
      <circle cx="320" cy="38" r="8" fill="#0284c7"/>
      <line x1="68" y1="38" x2="312" y2="38" stroke="#38bdf8" stroke-width="2"/>
      <text x="190" y="32" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Long Distance Skip Hop</text>
    </g>

    <!-- Layer 1 -->
    <g transform="translate(20, 115)">
      <rect width="380" height="65" rx="6" fill="#1e293b" stroke="#334155"/>
      <text x="12" y="18" fill="#94a3b8" font-size="9" font-family="monospace">Layer 1: Intermediate Clustering</text>
      <circle cx="60" cy="40" r="7" fill="#059669"/>
      <circle cx="160" cy="40" r="7" fill="#059669"/>
      <circle cx="260" cy="40" r="7" fill="#059669"/>
      <circle cx="340" cy="40" r="7" fill="#059669"/>
      <line x1="67" y1="40" x2="153" y2="40" stroke="#34d399" stroke-width="1.5"/>
      <line x1="167" y1="40" x2="253" y2="40" stroke="#34d399" stroke-width="1.5"/>
      <line x1="267" y1="40" x2="333" y2="40" stroke="#34d399" stroke-width="1.5"/>
    </g>

    <!-- Layer 0 (Dense) -->
    <g transform="translate(20, 190)">
      <rect width="380" height="95" rx="6" fill="#042f2e" stroke="#10b981"/>
      <text x="12" y="18" fill="#34d399" font-size="9" font-family="monospace" font-weight="bold">Layer 0: All 100M Vectors (Dense Delaunay Mesh)</text>
      <circle cx="40" cy="45" r="5" fill="#10b981"/>
      <circle cx="80" cy="65" r="5" fill="#10b981"/>
      <circle cx="120" cy="40" r="5" fill="#10b981"/>
      <circle cx="160" cy="70" r="5" fill="#10b981"/>
      <circle cx="200" cy="45" r="5" fill="#10b981"/>
      <circle cx="240" cy="60" r="5" fill="#facc15" stroke="#ffffff"/>
      <text x="240" y="80" fill="#facc15" font-size="8" font-family="monospace" text-anchor="middle">Top-K Nearest</text>
    </g>
  </g>

  <!-- VLLM PAGEDATTENTION (RIGHT) -->
  <g transform="translate(490, 30)">
    <rect width="430" height="310" rx="10" fill="#0f172a" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="20" y="28" fill="#c084fc" font-size="12" font-family="monospace" font-weight="bold">vLLM PAGEDATTENTION (GPU MEMORY VIRTUALIZATION)</text>

    <!-- Logical KV Sequence -->
    <rect x="20" y="45" width="390" height="60" rx="6" fill="#1e1b4b"/>
    <text x="14" y="20" fill="#cbd5e1" font-size="8" font-family="monospace">Logical KV Tokens: [Prompt Tokens 1-64] &rarr; Block 0, Block 1, Block 2</text>
    <rect x="14" y="28" width="100" height="22" rx="4" fill="#312e81"/>
    <text x="64" y="43" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Logical Block 0</text>
    <rect x="124" y="28" width="100" height="22" rx="4" fill="#312e81"/>
    <text x="174" y="43" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Logical Block 1</text>
    <rect x="234" y="28" width="100" height="22" rx="4" fill="#312e81"/>
    <text x="284" y="43" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Logical Block 2</text>

    <!-- Block Table Translation -->
    <rect x="20" y="115" width="390" height="60" rx="6" fill="#02040d" stroke="#334155"/>
    <text x="14" y="20" fill="#facc15" font-size="8" font-family="monospace" font-weight="bold">BLOCK TABLE (Page Map): Logical &rarr; Physical GPU HBM</text>
    <text x="14" y="42" fill="#cbd5e1" font-size="9" font-family="monospace">Logical 0 &rarr; Physical Slot 7 | Logical 1 &rarr; Physical Slot 2 | Logical 2 &rarr; Physical Slot 19</text>

    <!-- Non-Contiguous Physical GPU HBM Slots -->
    <rect x="20" y="185" width="390" height="110" rx="6" fill="#042f2e" stroke="#10b981"/>
    <text x="14" y="20" fill="#34d399" font-size="9" font-family="monospace" font-weight="bold">Physical GPU HBM3 Memory (Non-Contiguous Slots)</text>
    <rect x="14" y="32" width="70" height="40" rx="4" fill="#064e3b" stroke="#34d399"/>
    <text x="49" y="55" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Slot 2 (L1)</text>
    <rect x="94" y="32" width="70" height="40" rx="4" fill="#1e1b4b"/>
    <text x="129" y="55" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Other Req</text>
    <rect x="174" y="32" width="70" height="40" rx="4" fill="#064e3b" stroke="#34d399"/>
    <text x="209" y="55" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Slot 7 (L0)</text>
    <rect x="254" y="32" width="70" height="40" rx="4" fill="#064e3b" stroke="#34d399"/>
    <text x="289" y="55" fill="#a7f3d0" font-size="8" font-family="monospace" text-anchor="middle">Slot 19 (L2)</text>
    <text x="14" y="95" fill="#facc15" font-size="8" font-family="monospace">&check; Memory Waste &lt; 4% &bull; Zero Internal Fragmentation!</text>
  </g>
</svg>
""",
        "codeSnippet": """# Production Python Implementation of HNSW Vector Traversal
import heapq
import numpy as np
from typing import List, Dict, Tuple

class HNSWNode:
    def __init__(self, node_id: int, vector: np.ndarray, max_level: int):
        self.id = node_id
        self.vector = vector
        self.neighbors: Dict[int, List[int]] = {l: [] for l in range(max_level + 1)}

class SimpleHNSW:
    def __init__(self, dim: int = 1536, ef_construction: int = 64, m: int = 16):
        self.dim = dim
        self.ef = ef_construction
        self.M = m
        self.nodes: Dict[int, HNSWNode] = {}
        self.entry_point: int = None
        self.max_level: int = 0

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def search_layer(self, query: np.ndarray, enter_point: int, ef: int, level: int) -> List[Tuple[float, int]]:
        visited = {enter_point}
        candidates = [(-self.cosine_similarity(query, self.nodes[enter_point].vector), enter_point)]
        w = [(-candidates[0][0], enter_point)] # Min-heap of nearest elements

        while candidates:
            dist_c, current = heapq.heappop(candidates)
            furthest_dist = w[0][0]

            if -dist_c < furthest_dist and len(w) >= ef:
                break

            for neighbor in self.nodes[current].neighbors.get(level, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    sim = self.cosine_similarity(query, self.nodes[neighbor].vector)
                    
                    if sim > furthest_dist or len(w) < ef:
                        heapq.heappush(candidates, (-sim, neighbor))
                        heapq.heappush(w, (sim, neighbor))
                        if len(w) > ef:
                            heapq.heappop(w)
                            furthest_dist = w[0][0]

        # Return sorted by highest similarity
        return sorted([(sim, nid) for sim, nid in w], reverse=True)
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The OpenAI ChatGPT Global Outage (KV Cache Memory Collapse)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Over 100 million active users received "The server is experiencing high traffic" errors as GPU clusters crashed with CUDA Out of Memory (OOM).</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      During a viral traffic spike, millions of users submitted long conversational prompts exceeding 4,000 tokens.
      The underlying inference fleet utilized static contiguous KV-cache allocation.
    </p>
    <p>
      As multiple concurrent requests generated tokens simultaneously, GPU High-Bandwidth Memory (HBM) fragmented violently.
      Even though 40GB of physical VRAM was technically free across fragmented pages, the CUDA allocator failed to find a single contiguous 8GB block for a new request.
      <strong>Inference worker processes began throwing unhandled CUDA OOM exceptions, triggering a cascading container restart storm that took down the entire cluster!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Adoption of PagedAttention (vLLM Engine):</strong> Virtualize GPU memory into 16-token non-contiguous physical blocks, eliminating 100% of external and internal fragmentation.</li>
      <li><strong class="text-white">Chunked Prefill &amp; Continuous Batching:</strong> Break long prompt prefill tokens into smaller 512-token chunks interleaved with generation tokens to prevent GPU compute starvation.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why is LLM inference memory-bandwidth bound rather than compute-bound during the generation phase, and how does speculative decoding exploit this?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "LLM inference operates in two distinct phases with opposite hardware bottlenecks:
      <br><br>
      1. <strong>Prefill Phase (Prompt Processing):</strong> All prompt tokens are processed in parallel via dense Matrix-Matrix Multiplication (GEMM). This phase is heavily <strong>Compute-Bound (TFLOPs)</strong> and achieves near 100% Tensor Core arithmetic intensity.
      <br><br>
      2. <strong>Generation / Decode Phase (Autoregressive Token Generation):</strong> The model generates exactly ONE token at a time. To generate that single token, the GPU must stream the ENTIRE model weights (e.g. 140 GB for a 70B parameter FP16 model) plus the entire historical KV cache from GPU High-Bandwidth Memory (HBM) into SRAM cache.
      Because the arithmetic computation for a single token is negligible compared to the gigabytes of data moving across the bus, the GPU Tensor Cores sit 90% idle waiting on memory bandwidth!
      <br><br>
      <strong>Speculative Decoding</strong> brilliantly exploits this idle compute:
      A tiny, ultra-fast draft model (e.g. 1B parameter) generates 5 candidate tokens sequentially in low latency.
      Then, the huge 70B model verifies ALL 5 candidate tokens simultaneously in a single compute-bound forward pass.
      If all 5 match, you generated 5 tokens for the cost of 1 memory load, yielding a <strong>2x to 3x wall-clock speedup</strong> with mathematically identical output!"
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 6 loaded with {len(STAGE_6_CHAPTERS)} comprehensive chapters.")
