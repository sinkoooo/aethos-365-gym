# build_god_level_system_design.py
# Compiles modules, blueprints, simulators, flashcards, and cheat-sheets into god_level_system_design.html

import json
import os
import modules_scratch_to_god
import blueprints_data
import interactive_simulators

def build_full_html():
    levels = modules_scratch_to_god.LEVELS_DATA
    blueprints = blueprints_data.BLUEPRINTS
    sim_html = interactive_simulators.SIMULATORS_HTML
    sim_js = interactive_simulators.SIMULATORS_JS

    print(f"Loaded {len(levels)} foundation levels and {len(blueprints)} god-level blueprints.")

    # 12 Staff+ Battle Cards
    battle_cards = [
        {
            "q": "Why did Kafka drop ZooKeeper in favor of KRaft?",
            "category": "Event Streaming",
            "ans": "ZooKeeper was an external bottleneck for metadata. In clusters with millions of partitions, leader failover took minutes because state had to be transferred from ZooKeeper into the Kafka broker. KRaft (Kafka Raft) embeds consensus directly into Kafka event logs, scaling to 10M+ partitions and enabling sub-second failover."
        },
        {
            "q": "How does Zoom handle packet loss without freezing audio?",
            "category": "Real-Time Protocols",
            "ans": "Zoom uses UDP with Forward Error Correction (FEC) and dynamic jitter buffers. When packets drop, redundant parity packets reconstruct missing audio frames on the fly without waiting for TCP retransmission (which would cause human-noticeable audio jitter and delay)."
        },
        {
            "q": "Why does Google Spanner not require read locks?",
            "category": "Distributed Databases",
            "ans": "TrueTime bounds physical clock uncertainty across global datacenters to &le; 7ms using atomic rubidium clocks and GPS. By executing 'Commit Wait' on writes, read transactions can simply query an MVCC snapshot at a past timestamp (t &le; now - &epsilon;) with strict serializability and ZERO read locks!"
        },
        {
            "q": "How does Stripe prevent double-charges on network timeout?",
            "category": "Fintech & Ledgers",
            "ans": "Clients supply a unique 'Idempotency-Key' in HTTP headers. Stripe atomically reserves this key in Redis and checks PostgreSQL ledger state. If a client retries after a network drop, Stripe recognizes the duplicate key and immediately returns the previously recorded response without re-charging the credit card."
        },
        {
            "q": "What is the XFetch algorithm for Cache Stampede?",
            "category": "Caching Architecture",
            "ans": "Instead of waiting for an item to expire, XFetch uses probabilistic early expiration: e^(-&beta; * &delta; * ln(rand())) > expiry - now. As TTL approaches zero, background worker threads probabilistically refresh the cache before it ever misses, completely eliminating cache stampedes."
        },
        {
            "q": "Why do LSM-Trees beat B+ Trees for write-heavy workloads?",
            "category": "Storage Engines",
            "ans": "B+ Trees perform random in-place disk page updates, bottlenecked by disk IOPS. LSM-Trees append writes sequentially to an in-memory MemTable and commit log, flushing sequentially to immutable disk SSTables. Sequential disk writes on NVMe reach 3,500+ MB/s, vastly outperforming random I/O."
        },
        {
            "q": "How do you solve the Twitter Celebrity Fanout problem?",
            "category": "Social Graphs",
            "ans": "Hybrid timeline model: Normal users (&lt;25k followers) use Fanout-on-Write (push into followers' Redis lists for O(1) read). Celebrities (&gt;25k followers) use Fanout-on-Read: their tweets are pulled at request time and merged with the user's cached timeline in memory."
        },
        {
            "q": "Why is Redis Redlock criticized by Martin Kleppmann?",
            "category": "Distributed Locks",
            "ans": "Redlock relies on physical system clock synchronization. A Stop-The-World GC pause or network delay can freeze a client while its TTL expires in Redis; another client acquires the lock, leading to dual writers and data corruption. Fencing tokens issued by consensus protocols (etcd) are required for safety."
        },
        {
            "q": "Why did Uber create H3 hexagons instead of Geohashes?",
            "category": "Geospatial Systems",
            "ans": "In rectangular grids or Geohashes, diagonal neighbors are sqrt(2) times farther than orthogonal neighbors, distorting radius queries. In a hexagonal grid, all 6 neighbors share identical edge lengths and center-to-center distances, enabling clean O(1) concentric K-ring radius expansions."
        },
        {
            "q": "When should you choose Kafka over RabbitMQ?",
            "category": "Message Brokers",
            "ans": "Choose Kafka for high-throughput append-only event streaming (1M+ msgs/sec), message replayability, log retention, and stream processing (Flink). Choose RabbitMQ for complex AMQP routing (topic/headers), individual message ACK/nack, and discrete task queue dispatch."
        },
        {
            "q": "What is Split-Brain and how is it mathematically prevented?",
            "category": "Distributed Consensus",
            "ans": "Split-brain occurs when a network partition cuts a cluster in half, and both sides elect independent leaders that accept conflicting writes. It is prevented by enforcing Quorum: any decision or leader election requires a strict majority (N/2 + 1) of all nodes, meaning only one partition can ever form a quorum."
        },
        {
            "q": "Why is Two-Phase Commit (2PC) an anti-pattern in microservices?",
            "category": "Microservices",
            "ans": "2PC is a blocking protocol. If the coordinator crashes during the commit phase, database locks remain held indefinitely across multiple services, choking throughput. Modern distributed architectures replace 2PC with the Saga pattern and asynchronous compensating events."
        }
    ]

    html = []

    # HEAD
    html.append("""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ARCHITECT'S CODEX &bull; System Design from Scratch to God</title>
  
  <!-- High-Tech Favicon -->
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpolygon points='20,2 38,12 38,28 20,38 2,28 2,12' stroke='%2310b981' stroke-width='2.5' fill='%23050b1a'/%3E%3Ccircle cx='20' cy='20' r='6' fill='%2300f0ff'/%3E%3Cpath d='M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17' stroke='%2338bdf8' stroke-width='1.5'/%3E%3C/svg%3E">

  <!-- Tailwind CSS & Google Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#ecfdf5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
            }
          },
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
          }
        }
      }
    }
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

  <style>
    body {
      background-color: #030712;
      color: #cbd5e1;
      font-family: 'Inter', sans-serif;
    }
    code, pre, .font-mono {
      font-family: 'Fira Code', monospace;
    }
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #030712;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }
    .glass-card {
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(51, 65, 85, 0.6);
    }
    .perspective-1000 {
      perspective: 1000px;
    }
    .transform-style-3d {
      transform-style: preserve-3d;
    }
    .backface-hidden {
      backface-visibility: hidden;
    }
    .rotate-y-180 {
      transform: rotateY(180deg);
    }
  </style>
</head>
<body class="min-h-screen text-slate-300 antialiased selection:bg-emerald-500/20 selection:text-emerald-300">
""")

    # NAVIGATION HEADER
    html.append("""
  <!-- Top Navigation Sticky Bar -->
  <header class="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 p-0.5 shadow-lg shadow-emerald-500/20 flex items-center justify-center">
          <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
            <i data-lucide="cpu" class="w-4 h-4 text-emerald-400"></i>
          </div>
        </div>
        <div>
          <div class="text-sm font-bold text-white tracking-tight flex items-center gap-2">
            ARCHITECT'S CODEX
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">GOD LEVEL</span>
          </div>
          <div class="text-[10px] text-slate-400 font-mono">Planet-Scale Distributed Systems Mastery</div>
        </div>
      </div>

      <!-- Quick Nav Links -->
      <nav class="hidden md:flex items-center gap-6 text-xs font-medium text-slate-400">
        <a href="#curriculum" class="hover:text-emerald-400 transition-colors">Curriculum</a>
        <a href="#sandbox-section" class="hover:text-cyan-400 transition-colors">Interactive Lab</a>
        <a href="#blueprints" class="hover:text-indigo-400 transition-colors">10 Blueprints</a>
        <a href="#battlecards" class="hover:text-fuchsia-400 transition-colors">Battle Cards</a>
        <a href="#comparisons" class="hover:text-amber-400 transition-colors">Cheat Sheets</a>
      </nav>

      <!-- Search & Progress Tracker -->
      <div class="flex items-center gap-3">
        <!-- Search Trigger -->
        <div class="relative hidden sm:block">
          <input type="text" id="global-search" oninput="filterEverything(this.value)" placeholder="Search topics, blueprints, algorithms... (Ctrl+K)" class="w-64 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5 pl-8 text-xs text-slate-200 placeholder-slate-500 outline-none focus:border-emerald-500 transition-all font-mono">
          <i data-lucide="search" class="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-2.5"></i>
        </div>

        <!-- Mastery Badge -->
        <div class="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
          <div class="text-right">
            <div class="text-[9px] uppercase font-mono text-slate-400">Mastery</div>
            <div id="mastery-pct" class="text-xs font-mono font-bold text-emerald-400">0% Done</div>
          </div>
          <div class="w-7 h-7 relative flex items-center justify-center">
            <svg class="w-7 h-7 -rotate-90" viewBox="0 0 36 36">
              <path class="text-slate-800" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path id="mastery-progress-circle" class="text-emerald-400 transition-all duration-500" stroke-dasharray="0, 100" stroke-width="3" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </header>
""")

    # HERO SECTION
    html.append("""
  <!-- HERO COMMAND CENTER -->
  <section class="relative overflow-hidden pt-12 pb-16 border-b border-slate-800/80">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-950/20 via-slate-950 to-slate-950 -z-10"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto space-y-4">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          ZERO-TO-HERO &bull; STAFF &bull; PRINCIPAL DISTRIBUTED SYSTEMS
        </div>
        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
          System Design: <span class="bg-gradient-to-r from-emerald-400 via-cyan-400 to-indigo-400 bg-clip-text text-transparent">From Scratch to God</span>
        </h1>
        <p class="text-base sm:text-lg text-slate-400 leading-relaxed font-normal">
          The definitive interactive engineering guide. No hand-waving, no trivial oversimplifications. Real hardware limits, high-throughput kernel bypass, distributed consensus, and 10 production planet-scale architectures.
        </p>

        <!-- Stat Pill Counters -->
        <div class="pt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto text-left">
          <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="text-xs text-slate-400 font-medium">Curriculum Levels</div>
            <div class="text-xl font-mono font-bold text-white mt-0.5">5 Levels</div>
            <div class="text-[10px] text-emerald-400">Scratch &rarr; God Level</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="text-xs text-slate-400 font-medium">Blueprints</div>
            <div class="text-xl font-mono font-bold text-cyan-400 mt-0.5">10 Systems</div>
            <div class="text-[10px] text-slate-500">Spanner, Kafka, Uber...</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="text-xs text-slate-400 font-medium">Interactive Sandboxes</div>
            <div class="text-xl font-mono font-bold text-indigo-400 mt-0.5">4 Simulators</div>
            <div class="text-[10px] text-slate-500">Capacity, Ring, Latency</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="text-xs text-slate-400 font-medium">Interview Playbook</div>
            <div class="text-xl font-mono font-bold text-fuchsia-400 mt-0.5">45-Min Timer</div>
            <div class="text-[10px] text-slate-500">Staff+ Rubric Checklist</div>
          </div>
        </div>
      </div>
    </div>
  </section>
""")

    # MAIN CONTENT CONTAINER
    html.append("""
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-16">
""")

    # 1. INTERACTIVE LAB SECTION (SIMULATORS)
    html.append(sim_html)

    # 2. CURRICULUM SECTION (LEVEL 0 TO LEVEL 3)
    html.append("""
    <!-- CURRICULUM ACCORDION -->
    <section id="curriculum" class="space-y-8">
      <div class="border-b border-slate-800 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div>
          <span class="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider">Comprehensive Roadmap</span>
          <h2 class="text-2xl font-black text-white tracking-tight">The 5 Mastery Levels: Foundations to Planet Scale</h2>
        </div>
        <div class="text-xs text-slate-400">Click any topic to expand deep technical breakdown. Check off mastered topics!</div>
      </div>

      <div class="space-y-6">
""")

    # Render Foundation Levels (0 to 3)
    for lvl in levels:
        html.append(f"""
        <!-- {lvl['title']} -->
        <div class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
            <div class="flex items-center gap-3">
              <span class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-{lvl['badgeColor']}-500/10 text-{lvl['badgeColor']}-400 border border-{lvl['badgeColor']}-500/30">LEVEL {lvl['levelNum']}</span>
              <div>
                <h3 class="text-lg font-bold text-white">{lvl['title']}</h3>
                <p class="text-xs text-slate-400">{lvl['subtitle']}</p>
              </div>
            </div>
            <div class="text-xs font-mono text-slate-500">{len(lvl['topics'])} In-Depth Modules</div>
          </div>

          <!-- Topics List -->
          <div class="space-y-3">
""")
        for topic in lvl['topics']:
            html.append(f"""
            <div class="topic-card rounded-xl bg-slate-950 border border-slate-800/80 overflow-hidden transition-all duration-200">
              <div class="p-4 flex items-center justify-between gap-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onclick="toggleTopic('{topic['id']}')">
                <div class="flex items-center gap-3 flex-1">
                  <!-- Checkbox -->
                  <input type="checkbox" id="chk-{topic['id']}" onclick="event.stopPropagation(); toggleMastery('{topic['id']}')" class="w-4 h-4 rounded accent-emerald-500 bg-slate-900 border-slate-700 cursor-pointer">
                  <div>
                    <h4 class="text-sm font-semibold text-white tracking-tight flex items-center gap-2">
                      {topic['title']}
                      <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">{topic['difficulty']}</span>
                    </h4>
                    <p class="text-xs text-slate-400 mt-0.5">{topic['summary']}</p>
                  </div>
                </div>
                <div class="flex items-center gap-3 text-slate-500 text-xs font-mono">
                  <span>{topic['readTime']}</span>
                  <i data-lucide="chevron-down" id="icon-{topic['id']}" class="w-4 h-4 transition-transform duration-200"></i>
                </div>
              </div>
              <div id="body-{topic['id']}" class="hidden p-5 pt-3 border-t border-slate-800/80 bg-slate-950/80 text-xs">
                {topic['content']}
              </div>
            </div>
""")
        html.append("""
          </div>
        </div>
""")

    html.append("""
      </div>
    </section>
""")

    # 3. LEVEL 4: THE 10 GOD-LEVEL BLUEPRINTS
    html.append("""
    <!-- 10 GOD-LEVEL BLUEPRINTS -->
    <section id="blueprints" class="space-y-8">
      <div class="border-b border-slate-800 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div>
          <span class="text-xs font-mono font-bold text-fuchsia-400 uppercase tracking-wider">LEVEL 04 &bull; GOD LEVEL</span>
          <h2 class="text-2xl font-black text-white tracking-tight">The 10 Master Production Blueprints</h2>
        </div>
        <div class="text-xs text-slate-400">Complete architectural topologies, scale math, and real production trade-offs.</div>
      </div>

      <div class="space-y-8">
""")

    for bp in blueprints:
        stats_pills = "".join([f"""
          <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800">
            <div class="text-[10px] font-mono uppercase text-slate-500">{k}</div>
            <div class="text-xs font-mono font-bold text-white mt-0.5">{v}</div>
          </div>
        """ for k, v in bp['scaleStats'].items()])

        html.append(f"""
        <!-- Blueprint: {bp['title']} -->
        <div class="blueprint-card rounded-2xl bg-slate-900/60 border border-slate-800 p-6 space-y-6">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div class="flex items-start gap-3">
              <input type="checkbox" id="chk-{bp['id']}" onclick="toggleMastery('{bp['id']}')" class="mt-1 w-4 h-4 rounded accent-emerald-500 bg-slate-900 border-slate-700 cursor-pointer">
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-fuchsia-500/10 text-fuchsia-400 border border-fuchsia-500/20">{bp['badge']}</span>
                  <h3 class="text-lg font-bold text-white">{bp['title']}</h3>
                </div>
                <p class="text-xs text-slate-400 mt-1">{bp['description']}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {stats_pills}
            </div>
          </div>

          <!-- Architecture SVG Canvas -->
          <div>
            <div class="text-xs font-mono font-bold text-slate-400 mb-2 flex items-center justify-between">
              <span>SYSTEM ARCHITECTURE &amp; DATA FLOW TOPOLOGY</span>
              <span class="text-emerald-400 font-normal">Interactive Vector Diagram</span>
            </div>
            {bp['architectureSvg']}
          </div>

          <!-- Technical Deep Dive Box -->
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            {bp['technicalDeepDive']}
          </div>
        </div>
""")

    html.append("""
      </div>
    </section>
""")

    # 4. STAFF+ BATTLE CARDS SECTION
    html.append("""
    <!-- BATTLE CARDS (FLASHCARDS) -->
    <section id="battlecards" class="space-y-8">
      <div class="border-b border-slate-800 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div>
          <span class="text-xs font-mono font-bold text-indigo-400 uppercase tracking-wider">Interactive Drills</span>
          <h2 class="text-2xl font-black text-white tracking-tight">12 Staff+ System Design Battle Cards</h2>
        </div>
        <div class="text-xs text-slate-400">Click any card to flip and reveal the Staff-level explanation!</div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
""")

    for idx, bc in enumerate(battle_cards):
        html.append(f"""
        <div class="battlecard-container h-56 perspective-1000 cursor-pointer" onclick="flipCard(this)">
          <div class="battlecard relative w-full h-full transform-style-3d transition-transform duration-500 rounded-2xl shadow-xl">
            <!-- Front -->
            <div class="absolute inset-0 backface-hidden p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400">
                  <span>CARD #{idx+1:02d}</span>
                  <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-400">{bc['category']}</span>
                </div>
                <h4 class="text-sm font-bold text-white mt-3 leading-snug">{bc['q']}</h4>
              </div>
              <div class="text-[10px] font-mono text-slate-500 flex items-center justify-between">
                <span>Click to flip</span>
                <i data-lucide="rotate-cw" class="w-3.5 h-3.5"></i>
              </div>
            </div>
            <!-- Back -->
            <div class="absolute inset-0 backface-hidden rotate-y-180 p-5 rounded-2xl bg-slate-950 border border-indigo-500/40 flex flex-col justify-between overflow-y-auto">
              <div>
                <div class="text-[10px] font-mono text-emerald-400 font-bold mb-2">STAFF ARCHITECT ANSWER:</div>
                <p class="text-xs text-slate-300 leading-relaxed">{bc['ans']}</p>
              </div>
              <div class="text-[10px] font-mono text-slate-500 text-right mt-2">Click to flip back</div>
            </div>
          </div>
        </div>
""")

    html.append("""
      </div>
    </section>
""")

    # 5. GOLDEN COMPARISON MATRICES & CHEAT SHEETS
    html.append("""
    <!-- COMPARISON MATRIX & CHEAT SHEETS -->
    <section id="comparisons" class="space-y-8">
      <div class="border-b border-slate-800 pb-4">
        <span class="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider">Quick Reference</span>
        <h2 class="text-2xl font-black text-white tracking-tight">The Golden Architecture Comparison Matrices</h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Matrix 1: Storage Options -->
        <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="database" class="w-4 h-4 text-cyan-400"></i> SQL vs NoSQL vs In-Memory
          </h4>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800 font-mono text-[11px]">
                  <th class="p-2">Database</th>
                  <th class="p-2">Data Model</th>
                  <th class="p-2">Concurrency</th>
                  <th class="p-2">Best For</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td class="p-2 font-bold text-white">PostgreSQL</td>
                  <td class="p-2">Relational / JSONB</td>
                  <td class="p-2 text-cyan-400">ACID MVCC</td>
                  <td class="p-2">Financials, complex joins, primary source of truth.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Cassandra</td>
                  <td class="p-2">Wide-Column LSM</td>
                  <td class="p-2 text-amber-400">Eventual / Tunable</td>
                  <td class="p-2">High write throughput, time-series, IoT sensors.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Redis</td>
                  <td class="p-2">Key-Value / Data Structs</td>
                  <td class="p-2 text-emerald-400">Single-Threaded Epoll</td>
                  <td class="p-2">Caches, session state, rate limiters, leaderboards.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Spanner</td>
                  <td class="p-2">Distributed Relational</td>
                  <td class="p-2 text-indigo-400">Strict Serializability</td>
                  <td class="p-2">Global multi-region ACID without manual sharding.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Matrix 2: Protocols -->
        <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="radio" class="w-4 h-4 text-emerald-400"></i> Real-Time Communication Protocols
          </h4>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800 font-mono text-[11px]">
                  <th class="p-2">Protocol</th>
                  <th class="p-2">Direction</th>
                  <th class="p-2">Header Overhead</th>
                  <th class="p-2">Ideal Scenario</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td class="p-2 font-bold text-white">Short Polling</td>
                  <td class="p-2">Client &rarr; Server</td>
                  <td class="p-2 text-rose-400">Extremely High</td>
                  <td class="p-2">Legacy fallback only; terrible for battery/bandwidth.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">SSE (Server-Sent)</td>
                  <td class="p-2">Server &rarr; Client</td>
                  <td class="p-2 text-emerald-400">Low (HTTP/2 stream)</td>
                  <td class="p-2">LLM token streaming, stock tickers, notification feed.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">WebSockets</td>
                  <td class="p-2">Full-Duplex (Bidirectional)</td>
                  <td class="p-2 text-emerald-400">2-10 Bytes per frame</td>
                  <td class="p-2">Chat applications, collaborative whiteboards, gaming.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">gRPC (HTTP/2)</td>
                  <td class="p-2">Bidirectional Streaming</td>
                  <td class="p-2 text-cyan-400">Protobuf Binary</td>
                  <td class="p-2">Inter-service microservice RPC, high throughput.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
""")

    html.append("""
  </main>
""")

    # FOOTER
    html.append("""
  <footer class="border-t border-slate-800 py-10 mt-20 bg-slate-950 text-xs text-slate-500 text-center space-y-2">
    <div class="font-mono text-slate-400">ARCHITECT'S CODEX &bull; System Design From Scratch to God</div>
    <div>Engineered for Staff &amp; Principal Distributed Systems Architects. Completely self-contained.</div>
  </footer>
""")

    # SCRIPTS & INTERACTIVITY
    html.append(f"""
  <script>
    // Lucide Icons
    lucide.createIcons();

    // Topic Accordion Toggle
    function toggleTopic(id) {{
      const body = document.getElementById('body-' + id);
      const icon = document.getElementById('icon-' + id);
      if (body) {{
        body.classList.toggle('hidden');
        if (icon) {{
          icon.classList.toggle('rotate-180');
        }}
      }}
    }}

    // Flip Battle Card
    function flipCard(el) {{
      const card = el.querySelector('.battlecard');
      if (card) {{
        card.classList.toggle('rotate-y-180');
      }}
    }}

    // Global Mastery Persistence
    const TOTAL_ITEMS = {len(levels[0]['topics']) + len(levels[1]['topics']) + len(levels[2]['topics']) + len(levels[3]['topics']) + len(blueprints)};
    let masteredItems = JSON.parse(localStorage.getItem('sysdesign_mastery') || '[]');

    function initMastery() {{
      masteredItems.forEach(id => {{
        const chk = document.getElementById('chk-' + id);
        if (chk) chk.checked = true;
      }});
      updateMasteryUI();
    }}

    function toggleMastery(id) {{
      const idx = masteredItems.indexOf(id);
      if (idx >= 0) {{
        masteredItems.splice(idx, 1);
      }} else {{
        masteredItems.push(id);
        // Confetti burst on milestone
        if (masteredItems.length === TOTAL_ITEMS) {{
          confetti({{ particleCount: 150, spread: 80, origin: {{ y: 0.6 }} }});
        }}
      }}
      localStorage.setItem('sysdesign_mastery', JSON.stringify(masteredItems));
      updateMasteryUI();
    }}

    function updateMasteryUI() {{
      const pct = Math.round((masteredItems.length / TOTAL_ITEMS) * 100);
      const pctEl = document.getElementById('mastery-pct');
      const circleEl = document.getElementById('mastery-progress-circle');
      if (pctEl) pctEl.innerText = `${{pct}}% Done (${{masteredItems.length}}/${{TOTAL_ITEMS}})`;
      if (circleEl) circleEl.setAttribute('stroke-dasharray', `${{pct}}, 100`);
    }}

    // Global Search Filter
    function filterEverything(query) {{
      const q = query.toLowerCase().trim();
      document.querySelectorAll('.topic-card, .blueprint-card').forEach(card => {{
        const text = card.innerText.toLowerCase();
        if (!q || text.includes(q)) {{
          card.classList.remove('hidden');
        }} else {{
          card.classList.add('hidden');
        }}
      }});
    }}

    // Keyboard shortcut for search
    window.addEventListener('keydown', (e) => {{
      if ((e.ctrlKey || e.metaKey) && e.key === 'k' || e.key === '/') {{
        e.preventDefault();
        const searchInput = document.getElementById('global-search');
        if (searchInput) {{
          searchInput.focus();
        }}
      }}
    }});

    // Simulators JavaScript Bundle
    {sim_js}

    window.addEventListener('DOMContentLoaded', () => {{
      initMastery();
    }});
  </script>
</body>
</html>
""")

    output_path = os.path.join(os.path.dirname(__file__), "god_level_system_design.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(html))

    print(f"Successfully generated {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    build_full_html()
