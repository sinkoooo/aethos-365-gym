# build_world_class_system_design.py
# Compiles the commercial-grade "SYSTEM ARCHITECT BIBLE: From Scratch to God"

import os
import data_curriculum_deep
import data_blueprints_deep
import data_interactive_tools
import data_cheatsheets

def generate_masterpiece():
    tiers = data_curriculum_deep.TIERS
    blueprints = data_blueprints_deep.BLUEPRINTS
    tools_html = data_interactive_tools.TOOLS_HTML
    tools_js = data_interactive_tools.TOOLS_JS
    cards = data_cheatsheets.BATTLE_CARDS

    total_curriculum_chapters = sum(len(t['chapters']) for t in tiers)
    total_blueprints_count = len(blueprints)
    total_mastery_items = total_curriculum_chapters + total_blueprints_count

    print(f"Building masterpiece: {len(tiers)} Tiers ({total_curriculum_chapters} Chapters), {total_blueprints_count} Blueprints, {len(cards)} Battle Cards.")

    html = []

    # HTML HEADER & TAILWIND & FONTS
    html.append(f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SYSTEM ARCHITECT BIBLE &bull; From Scratch to God-Level Distributed Systems</title>
  
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpolygon points='20,2 38,12 38,28 20,38 2,28 2,12' stroke='%2310b981' stroke-width='2.5' fill='%23050b1a'/%3E%3Ccircle cx='20' cy='20' r='6' fill='%2300f0ff'/%3E%3Cpath d='M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17' stroke='%2338bdf8' stroke-width='1.5'/%3E%3C/svg%3E">

  <!-- Tailwind CSS & Google Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#ecfdf5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
            }}
          }},
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
          }}
        }}
      }}
    }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Icons & Confetti -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

  <style>
    body {{
      background-color: #07090e;
      color: #cbd5e1;
      font-family: 'Inter', sans-serif;
    }}
    code, pre, .font-mono {{
      font-family: 'Fira Code', monospace;
    }}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #07090e;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1e293b;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #334155;
    }}
    .perspective-1000 {{
      perspective: 1000px;
    }}
    .transform-style-3d {{
      transform-style: preserve-3d;
    }}
    .backface-hidden {{
      backface-visibility: hidden;
    }}
    .rotate-y-180 {{
      transform: rotateY(180deg);
    }}
  </style>
</head>
<body class="min-h-screen text-slate-300 antialiased selection:bg-emerald-500/25 selection:text-emerald-300">
""")

    # STICKY FROSTED HEADER
    html.append(f"""
  <!-- STICKY FROSTED HEADER -->
  <header class="sticky top-0 z-50 border-b border-white/[0.08] bg-slate-950/80 backdrop-blur-2xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-500 via-cyan-500 to-indigo-500 p-0.5 shadow-xl shadow-emerald-500/20 flex items-center justify-center">
          <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
            <i data-lucide="layers" class="w-5 h-5 text-emerald-400"></i>
          </div>
        </div>
        <div>
          <div class="text-sm font-black text-white tracking-tight flex items-center gap-2">
            SYSTEM ARCHITECT BIBLE
            <span class="text-[9px] font-mono px-2 py-0.5 rounded-full bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 text-emerald-400 border border-emerald-500/30">COMMERCIAL GRADE</span>
          </div>
          <div class="text-[10px] text-slate-400 font-mono">From Scratch to God &bull; Staff+ Distributed Systems</div>
        </div>
      </div>

      <nav class="hidden lg:flex items-center gap-6 text-xs font-semibold text-slate-400">
        <a href="#interactive-lab" class="hover:text-emerald-400 transition-colors">Lab Workbench</a>
        <a href="#curriculum" class="hover:text-cyan-400 transition-colors">Curriculum ({len(tiers)} Tiers)</a>
        <a href="#blueprints" class="hover:text-indigo-400 transition-colors">12 Blueprints</a>
        <a href="#battlecards" class="hover:text-fuchsia-400 transition-colors">Battle Cards</a>
        <a href="#comparisons" class="hover:text-amber-400 transition-colors">Cheat Sheets</a>
      </nav>

      <div class="flex items-center gap-3">
        <!-- Search -->
        <div class="relative hidden sm:block">
          <input type="text" id="global-search-input" oninput="liveFilterApp(this.value)" placeholder="Search concepts, blueprints, algorithms... (Ctrl+K)" class="w-64 bg-slate-900/90 border border-white/[0.08] rounded-xl px-3 py-1.5 pl-8 text-xs text-slate-200 placeholder-slate-500 outline-none focus:border-emerald-500 transition-all font-mono">
          <i data-lucide="search" class="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-2.5"></i>
        </div>

        <!-- Audio Synthesizer Toggle -->
        <button onclick="toggleAudioFx()" id="btn-audio-toggle" title="Toggle UI sound effects" class="p-2 rounded-xl bg-slate-900 border border-white/[0.08] text-slate-400 hover:text-white transition-all">
          <i data-lucide="volume-2" id="icon-volume" class="w-4 h-4"></i>
        </button>

        <!-- Mastery Badge -->
        <div class="flex items-center gap-2 bg-slate-900/90 border border-white/[0.08] rounded-2xl px-3 py-1.5">
          <div class="text-right">
            <div class="text-[9px] uppercase font-mono text-slate-400">Mastery</div>
            <div id="mastery-lbl" class="text-xs font-mono font-bold text-emerald-400">0% Done</div>
          </div>
          <div class="w-7 h-7 relative flex items-center justify-center">
            <svg class="w-7 h-7 -rotate-90" viewBox="0 0 36 36">
              <path class="text-slate-800" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path id="mastery-donut" class="text-emerald-400 transition-all duration-500" stroke-dasharray="0, 100" stroke-width="3" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </header>
""")

    # HERO SECTION
    html.append(f"""
  <!-- HERO SHOWCASE -->
  <section class="relative overflow-hidden pt-16 pb-20 border-b border-white/[0.08]">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-950/30 via-slate-950/60 to-slate-950 -z-10"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono font-bold">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        THE DEFINITIVE DISTRIBUTED SYSTEMS COMPENDIUM
      </div>
      
      <h1 class="text-4xl sm:text-7xl font-black text-white tracking-tight leading-none max-w-4xl mx-auto">
        System Design: <span class="bg-gradient-to-r from-emerald-400 via-cyan-400 to-indigo-400 bg-clip-text text-transparent">From Scratch to God</span>
      </h1>

      <p class="text-base sm:text-xl text-slate-300 max-w-3xl mx-auto font-normal leading-relaxed">
        The commercial-grade, textbook-deep interactive guide built for Senior, Staff, and Principal Engineers. From CPU cache lines and Linux kernel bypass up to globally linearizable distributed SQL and 100M-user social feeds.
      </p>

      <!-- Stat Badges Grid -->
      <div class="pt-6 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto text-left">
        <div class="p-4 rounded-2xl bg-slate-900/60 border border-white/[0.08] backdrop-blur-xl">
          <div class="text-[11px] font-mono text-slate-400 uppercase">Curriculum Tiers</div>
          <div class="text-2xl font-mono font-black text-white mt-1">6 Tiers</div>
          <div class="text-[11px] text-emerald-400 mt-0.5">{total_curriculum_chapters} Comprehensive Chapters</div>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900/60 border border-white/[0.08] backdrop-blur-xl">
          <div class="text-[11px] font-mono text-slate-400 uppercase">Production Blueprints</div>
          <div class="text-2xl font-mono font-black text-cyan-400 mt-1">12 Systems</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Spanner, Stripe, Uber, Netflix...</div>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900/60 border border-white/[0.08] backdrop-blur-xl">
          <div class="text-[11px] font-mono text-slate-400 uppercase">Interactive Lab</div>
          <div class="text-2xl font-mono font-black text-indigo-400 mt-1">5 Simulators</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Tracer, AWS FinOps, Hash Ring</div>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900/60 border border-white/[0.08] backdrop-blur-xl">
          <div class="text-[11px] font-mono text-slate-400 uppercase">Staff+ Battle Cards</div>
          <div class="text-2xl font-mono font-black text-fuchsia-400 mt-1">12 Cards</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Principal-Level Interview Drills</div>
        </div>
      </div>
    </div>
  </section>
""")

    # MAIN CONTENT CONTAINER
    html.append("""
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-20">
""")

    # 1. INTERACTIVE LAB SECTION
    html.append(tools_html)

    # 2. COMPREHENSIVE CURRICULUM ACCORDION (TIER 00 TO TIER 05)
    html.append(f"""
    <!-- CURRICULUM ROADMAP -->
    <section id="curriculum" class="space-y-8">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/[0.08] pb-6">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-mono font-semibold mb-3">
            PEDAGOGICAL RIGOR &bull; 6 MASTERY TIERS
          </div>
          <h2 class="text-3xl font-black text-white tracking-tight">The 6-Tier Distributed Curriculum</h2>
          <p class="text-slate-400 text-sm mt-1 max-w-2xl">
            A step-by-step progression from silicon physics and TCP congestion control to distributed consensus algorithms and high-availability chaos engineering.
          </p>
        </div>
        <div class="text-xs font-mono text-slate-400">Total {total_curriculum_chapters} In-Depth Chapters</div>
      </div>

      <div class="space-y-8">
""")

    for t in tiers:
        html.append(f"""
        <!-- {t['title']} -->
        <div class="p-6 rounded-3xl bg-slate-900/40 border border-white/[0.08] backdrop-blur-xl space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
            <div class="flex items-center gap-3">
              <span class="px-3 py-1 rounded-xl text-xs font-mono font-bold bg-{t['color']}-500/10 text-{t['color']}-400 border border-{t['color']}-500/25">{t['num']}</span>
              <div>
                <h3 class="text-xl font-bold text-white tracking-tight">{t['title']}</h3>
                <p class="text-xs text-slate-400 mt-0.5">{t['tagline']}</p>
              </div>
            </div>
            <div class="text-xs font-mono text-slate-500">{len(t['chapters'])} Chapters</div>
          </div>

          <div class="space-y-3">
""")
        for ch in t['chapters']:
            html.append(f"""
            <div class="curriculum-item rounded-2xl bg-slate-950 border border-slate-800/80 overflow-hidden transition-all duration-200">
              <div class="p-4 flex items-center justify-between gap-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onclick="toggleChapter('{ch['id']}')">
                <div class="flex items-center gap-3 flex-1">
                  <input type="checkbox" id="chk-{ch['id']}" onclick="event.stopPropagation(); toggleItemMastery('{ch['id']}')" class="w-4 h-4 rounded accent-emerald-500 bg-slate-900 border-slate-700 cursor-pointer">
                  <div>
                    <h4 class="text-sm font-bold text-white tracking-tight flex items-center gap-2">
                      {ch['title']}
                      <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">{ch['difficulty']}</span>
                    </h4>
                    <p class="text-xs text-slate-400 mt-0.5">{ch['summary']}</p>
                  </div>
                </div>
                <div class="flex items-center gap-3 text-slate-500 text-xs font-mono">
                  <span>{ch['readTime']}</span>
                  <i data-lucide="chevron-down" id="icon-{ch['id']}" class="w-4 h-4 transition-transform duration-200"></i>
                </div>
              </div>
              <div id="body-{ch['id']}" class="hidden p-6 pt-3 border-t border-slate-800/80 bg-slate-950/90 text-xs">
                {ch['html']}
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

    # 3. THE 12 BIBLE PRODUCTION BLUEPRINTS
    html.append(f"""
    <!-- 12 PRODUCTION BLUEPRINTS -->
    <section id="blueprints" class="space-y-8">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/[0.08] pb-6">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono font-semibold mb-3">
            TIER 06 &bull; GOD LEVEL BLUEPRINTS
          </div>
          <h2 class="text-3xl font-black text-white tracking-tight">The 12 Master Planet-Scale Blueprints</h2>
          <p class="text-slate-400 text-sm mt-1 max-w-2xl">
            Exhaustive, uncompromised real-world production architectures: vector diagrams, scale statistics, and failure mitigation strategies.
          </p>
        </div>
        <div class="text-xs font-mono text-slate-400">{len(blueprints)} Full Production Architectures</div>
      </div>

      <div class="space-y-8">
""")

    for bp in blueprints:
        stat_pills = "".join([f"""
          <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
            <div class="text-[9px] font-mono uppercase text-slate-500">{k}</div>
            <div class="text-xs font-mono font-bold text-white mt-0.5">{v}</div>
          </div>
        """ for k, v in bp['stats'].items()])

        html.append(f"""
        <!-- Blueprint #{bp['num']} -->
        <div class="blueprint-item rounded-3xl bg-slate-900/50 border border-white/[0.08] p-6 space-y-6 backdrop-blur-xl">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
            <div class="flex items-start gap-3">
              <input type="checkbox" id="chk-{bp['id']}" onclick="toggleItemMastery('{bp['id']}')" class="mt-1 w-4 h-4 rounded accent-emerald-500 bg-slate-900 border-slate-700 cursor-pointer">
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">BLUEPRINT #{bp['num']} &bull; {bp['badge']}</span>
                  <h3 class="text-lg font-bold text-white">{bp['title']}</h3>
                </div>
                <p class="text-xs text-slate-400 mt-1">{bp['tagline']}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {stat_pills}
            </div>
          </div>

          <!-- Vector Schematic -->
          <div>
            <div class="text-xs font-mono font-bold text-slate-400 mb-2 flex items-center justify-between">
              <span>SYSTEM TOPOLOGY &amp; PACKET FLOW SCHEMATIC</span>
              <span class="text-emerald-400 font-normal">Interactive Vector Diagram</span>
            </div>
            {bp['svg']}
          </div>

          <!-- Deep Dive Card -->
          <div class="p-5 rounded-2xl bg-slate-950 border border-white/[0.08]">
            {bp['deepDive']}
          </div>
        </div>
""")

    html.append("""
      </div>
    </section>
""")

    # 4. STAFF+ 3D BATTLE CARDS
    html.append(f"""
    <!-- 12 STAFF+ BATTLE CARDS -->
    <section id="battlecards" class="space-y-8">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/[0.08] pb-6">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-fuchsia-500/10 border border-fuchsia-500/20 text-fuchsia-400 text-xs font-mono font-semibold mb-3">
            STAFF &bull; PRINCIPAL INTERVIEW DRILLS
          </div>
          <h2 class="text-3xl font-black text-white tracking-tight">12 Staff+ System Design Battle Cards</h2>
          <p class="text-slate-400 text-sm mt-1 max-w-2xl">
            The counter-intuitive trade-offs and edge-case questions that distinguish L6/L7 Staff and Principal engineers from Senior candidates. Click any card to flip.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
""")

    for bc in cards:
        html.append(f"""
        <div class="h-60 perspective-1000 cursor-pointer" onclick="flipBattleCard(this)">
          <div class="battlecard-inner relative w-full h-full transform-style-3d transition-transform duration-500 rounded-3xl shadow-2xl">
            <!-- Front -->
            <div class="absolute inset-0 backface-hidden p-6 rounded-3xl bg-slate-900 border border-white/[0.08] flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400">
                  <span>{bc['num']}</span>
                  <span class="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">{bc['cat']}</span>
                </div>
                <h4 class="text-sm font-bold text-white mt-4 leading-snug">{bc['q']}</h4>
              </div>
              <div class="text-[10px] font-mono text-slate-500 flex items-center justify-between">
                <span>Click to reveal staff answer</span>
                <i data-lucide="rotate-cw" class="w-3.5 h-3.5"></i>
              </div>
            </div>
            <!-- Back -->
            <div class="absolute inset-0 backface-hidden rotate-y-180 p-6 rounded-3xl bg-slate-950 border border-indigo-500/40 flex flex-col justify-between overflow-y-auto">
              <div>
                <div class="text-[10px] font-mono text-emerald-400 font-bold mb-2 uppercase tracking-wider">STAFF ARCHITECT ANSWER:</div>
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

    # 5. GOLDEN COMPARISON MATRICES
    html.append("""
    <!-- GOLDEN COMPARISON MATRICES -->
    <section id="comparisons" class="space-y-8">
      <div class="border-b border-white/[0.08] pb-6">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-mono font-semibold mb-3">
          QUICK REFERENCE CHEAT SHEETS
        </div>
        <h2 class="text-3xl font-black text-white tracking-tight">The Golden Architecture Comparison Matrices</h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Matrix 1: Storage -->
        <div class="p-6 rounded-3xl bg-slate-900/50 border border-white/[0.08] space-y-4 backdrop-blur-xl">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="database" class="w-4 h-4 text-cyan-400"></i> Storage Engines Comparison
          </h4>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800 font-mono text-[11px]">
                  <th class="p-2">Engine</th>
                  <th class="p-2">Data Structure</th>
                  <th class="p-2">Write / Read Latency</th>
                  <th class="p-2">Ideal Workload</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td class="p-2 font-bold text-white">PostgreSQL</td>
                  <td class="p-2">B+ Tree Pages (8KB)</td>
                  <td class="p-2 text-cyan-400">Read: O(log N) &bull; Write: Random IO</td>
                  <td class="p-2">ACID transactions, relational joins, financial ledgers.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">RocksDB / Cassandra</td>
                  <td class="p-2">LSM-Tree + SSTables</td>
                  <td class="p-2 text-emerald-400">Write: O(1) Append &bull; Read: Bloom + SSTable</td>
                  <td class="p-2">High write throughput, time-series, event telemetry.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Redis</td>
                  <td class="p-2">In-Memory SkipList / Hash</td>
                  <td class="p-2 text-emerald-400">Sub-millisecond RAM</td>
                  <td class="p-2">Caches, rate limiters, session stores, leaderboards.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Google Spanner</td>
                  <td class="p-2">Distributed LSM + Paxos</td>
                  <td class="p-2 text-indigo-400">Strict Serializability via TrueTime</td>
                  <td class="p-2">Global multi-region ACID without manual sharding.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Matrix 2: Protocols -->
        <div class="p-6 rounded-3xl bg-slate-900/50 border border-white/[0.08] space-y-4 backdrop-blur-xl">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="radio" class="w-4 h-4 text-emerald-400"></i> Real-Time Communication Protocols
          </h4>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800 font-mono text-[11px]">
                  <th class="p-2">Protocol</th>
                  <th class="p-2">Direction</th>
                  <th class="p-2">Frame Overhead</th>
                  <th class="p-2">Ideal Scenario</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td class="p-2 font-bold text-white">HTTP/1.1 Polling</td>
                  <td class="p-2">Client &rarr; Server</td>
                  <td class="p-2 text-rose-400">High (500B+ headers)</td>
                  <td class="p-2">Legacy fallback only; terrible for mobile battery.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">Server-Sent Events</td>
                  <td class="p-2">Server &rarr; Client</td>
                  <td class="p-2 text-emerald-400">Low (HTTP/2 stream)</td>
                  <td class="p-2">LLM token streaming, notifications, live stock quotes.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-white">WebSockets</td>
                  <td class="p-2">Bidirectional (Full Duplex)</td>
                  <td class="p-2 text-emerald-400">2 - 10 Bytes</td>
                  <td class="p-2">Chat messaging, multiplayer gaming, collaborative boards.</td>
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
  <footer class="border-t border-white/[0.08] py-12 mt-24 bg-slate-950 text-xs text-slate-500 text-center space-y-3">
    <div class="font-mono text-slate-400 font-bold">SYSTEM ARCHITECT BIBLE &bull; FROM SCRATCH TO GOD</div>
    <div>Authored for Senior, Staff, and Principal Distributed Systems Engineers worldwide.</div>
    <div class="text-[11px] text-slate-600">Completely standalone &bull; Zero external build tools required &bull; Persistent browser state</div>
  </footer>
""")

    # SCRIPTS & LOGIC
    html.append(f"""
  <script>
    lucide.createIcons();

    // Web Audio API Sound Synthesizer (Optional High-Tech Clicks)
    let audioCtx = null;
    let audioEnabled = true;

    function playAudioClick(freq = 600, type = 'sine', duration = 0.04) {{
      if (!audioEnabled) return;
      try {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      }} catch (e) {{}}
    }}

    function toggleAudioFx() {{
      audioEnabled = !audioEnabled;
      const icon = document.getElementById('icon-volume');
      if (icon) {{
        icon.setAttribute('data-lucide', audioEnabled ? 'volume-2' : 'volume-x');
        lucide.createIcons();
      }}
      if (audioEnabled) playAudioClick(800, 'sine', 0.05);
    }}

    // Chapter Accordion
    function toggleChapter(id) {{
      playAudioClick(500, 'triangle', 0.03);
      const body = document.getElementById('body-' + id);
      const icon = document.getElementById('icon-' + id);
      if (body) {{
        body.classList.toggle('hidden');
        if (icon) icon.classList.toggle('rotate-180');
      }}
    }}

    // Battle Card Flip
    function flipBattleCard(el) {{
      playAudioClick(700, 'sine', 0.04);
      const card = el.querySelector('.battlecard-inner');
      if (card) card.classList.toggle('rotate-y-180');
    }}

    // Mastery Tracker with LocalStorage
    const TOTAL_TRACKABLE_ITEMS = {total_mastery_items};
    let masteredItemSet = JSON.parse(localStorage.getItem('sysarchitect_mastery_items') || '[]');

    function initMasterySystem() {{
      masteredItemSet.forEach(id => {{
        const chk = document.getElementById('chk-' + id);
        if (chk) chk.checked = true;
      }});
      updateMasteryDisplay();
    }}

    function toggleItemMastery(id) {{
      playAudioClick(900, 'sine', 0.05);
      const idx = masteredItemSet.indexOf(id);
      if (idx >= 0) {{
        masteredItemSet.splice(idx, 1);
      }} else {{
        masteredItemSet.push(id);
        if (masteredItemSet.length === TOTAL_TRACKABLE_ITEMS) {{
          confetti({{ particleCount: 200, spread: 90, origin: {{ y: 0.6 }} }});
        }}
      }}
      localStorage.setItem('sysarchitect_mastery_items', JSON.stringify(masteredItemSet));
      updateMasteryDisplay();
    }}

    function updateMasteryDisplay() {{
      const pct = Math.round((masteredItemSet.length / TOTAL_TRACKABLE_ITEMS) * 100);
      const lbl = document.getElementById('mastery-lbl');
      const donut = document.getElementById('mastery-donut');
      if (lbl) lbl.innerText = `${{pct}}% Done (${{masteredItemSet.length}}/${{TOTAL_TRACKABLE_ITEMS}})`;
      if (donut) donut.setAttribute('stroke-dasharray', `${{pct}}, 100`);
    }}

    // Live Search Filter
    function liveFilterApp(query) {{
      const q = query.toLowerCase().trim();
      document.querySelectorAll('.curriculum-item, .blueprint-item').forEach(card => {{
        const text = card.innerText.toLowerCase();
        if (!q || text.includes(q)) {{
          card.classList.remove('hidden');
        }} else {{
          card.classList.add('hidden');
        }}
      }});
    }}

    window.addEventListener('keydown', (e) => {{
      if ((e.ctrlKey || e.metaKey) && e.key === 'k' || e.key === '/') {{
        e.preventDefault();
        const searchInput = document.getElementById('global-search-input');
        if (searchInput) searchInput.focus();
      }}
    }});

    // Tool Controllers JS
    {tools_js}

    window.addEventListener('DOMContentLoaded', () => {{
      initMasterySystem();
    }});
  </script>
</body>
</html>
""")

    output_path = os.path.join(os.path.dirname(__file__), "god_level_system_design.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(html))

    print(f"Masterpiece built successfully at {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_masterpiece()
