# build_cockpit_100x.py
# Compiles the 100x Enhanced Zero-Scroll Commercial System Design Cockpit Operating System
# Bulletproof, Zero-Crash, High-Reliability Architecture

import os
import json
import data_curriculum_100x
import data_cheatsheets
import data_interactive_tools

def build_cockpit_100x():
    topics = data_curriculum_100x.ALL_TOPICS_100X
    battle_cards = data_cheatsheets.BATTLE_CARDS

    print(f"Compiling Cockpit 100x with {len(topics)} multi-dimensional modules...")

    json_topics = json.dumps(topics)
    json_battle_cards = json.dumps(battle_cards)

    html = []

    # 1. HTML HEAD & STYLES
    html.append(f"""<!DOCTYPE html>
<html lang="en" class="dark h-screen w-screen overflow-hidden">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NEXUS &bull; God-Level System Design Operating System (Scratch to God)</title>
  
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpolygon points='20,2 38,12 38,28 20,38 2,28 2,12' stroke='%2310b981' stroke-width='2.5' fill='%23050b1a'/%3E%3Ccircle cx='20' cy='20' r='6' fill='%2300f0ff'/%3E%3Cpath d='M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17' stroke='%2338bdf8' stroke-width='1.5'/%3E%3C/svg%3E">

  <!-- Tailwind CSS & Google Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (window.tailwind) {{
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            colors: {{
              obsidian: {{
                950: '#07090e',
                900: '#0c0e14',
                850: '#121620',
                800: '#1b2230',
              }}
            }},
            fontFamily: {{
              sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
              mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
            }}
          }}
        }}
      }};
    }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Lucide Icons & Confetti with async safety -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

  <style>
    body {{
      background-color: #07090e;
      color: #cbd5e1;
      font-family: 'Inter', sans-serif;
      overflow: hidden;
      user-select: none;
    }}
    code, pre, .font-mono {{
      font-family: 'Fira Code', monospace;
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 5px;
      height: 5px;
    }}
    .custom-scroll::-webkit-scrollbar-track {{
      background: #07090e;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #1e293b;
      border-radius: 4px;
    }}
    .custom-scroll::-webkit-scrollbar-thumb:hover {{
      background: #334155;
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
    }}
  </style>
</head>
<body class="h-screen w-screen flex flex-col bg-[#07090e] text-slate-300">
""")

    # 2. TOP HEADER COCKPIT BAR (48px)
    html.append(f"""
  <!-- TOP FIXED HEADER BAR -->
  <header class="h-12 border-b border-white/[0.08] bg-[#090b10] px-3 flex items-center justify-between shrink-0 z-50">
    <!-- Brand & Platform Identity -->
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 cursor-pointer" onclick="selectItemById('c-01-client-server')">
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-500 to-cyan-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <i data-lucide="cpu" class="w-4 h-4 text-slate-950 stroke-[2.5]"></i>
        </div>
        <div>
          <span class="font-black text-xs tracking-wider text-white">NEXUS</span>
          <span class="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20 ml-1">OS 2.0</span>
        </div>
      </div>
      <div class="hidden lg:flex items-center gap-2 text-[11px] font-mono text-slate-500 border-l border-white/[0.08] pl-3">
        <span>God-Level System Design</span>
        <span>&bull;</span>
        <span class="text-cyan-400 font-bold">Scratch &rarr; God</span>
      </div>
    </div>

    <!-- Center Stage Filter Quick Switcher -->
    <div class="hidden md:flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-white/[0.06] text-xs font-mono">
      <button onclick="filterSidebar('all')" id="filter-all" class="stage-filter-btn px-2.5 py-1 rounded-lg text-white bg-slate-800 font-bold transition-all">All (27)</button>
      <button onclick="filterSidebar('stage-1')" id="filter-stage-1" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S1 (Scratch)</button>
      <button onclick="filterSidebar('stage-2')" id="filter-stage-2" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S2 (Scale)</button>
      <button onclick="filterSidebar('stage-3')" id="filter-stage-3" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S3 (Dist)</button>
      <button onclick="filterSidebar('stage-4')" id="filter-stage-4" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S4 (CAP)</button>
      <button onclick="filterSidebar('stage-5')" id="filter-stage-5" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S5 (Raft)</button>
      <button onclick="filterSidebar('stage-6')" id="filter-stage-6" class="stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all">S6 (God)</button>
      <button onclick="filterSidebar('blueprints')" id="filter-blueprints" class="stage-filter-btn px-2.5 py-1 rounded-lg text-indigo-400 hover:text-indigo-300 transition-all font-bold">12 Blueprints</button>
    </div>

    <!-- Right Controls: Progress & Audio -->
    <div class="flex items-center gap-3">
      <!-- Curriculum Progress Indicator -->
      <div class="flex items-center gap-2 px-2.5 py-1 rounded-xl bg-slate-950 border border-slate-800">
        <svg class="w-4 h-4 transform -rotate-90">
          <circle cx="8" cy="8" r="6" stroke="#1e293b" stroke-width="2" fill="none"/>
          <circle id="cockpit-progress-ring" cx="8" cy="8" r="6" stroke="#10b981" stroke-width="2" fill="none" stroke-dasharray="0, 100"/>
        </svg>
        <span id="cockpit-mastery-text" class="text-[11px] font-mono font-bold text-slate-300">0% Mastery</span>
      </div>

      <!-- Tactile Audio Toggle -->
      <button onclick="toggleAudio()" title="Toggle Web Audio Feedback" class="p-1.5 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 hover:text-white hover:border-slate-700 transition-all">
        <i data-lucide="volume-2" id="audio-icon" class="w-3.5 h-3.5 text-emerald-400"></i>
      </button>

      <!-- Toggle Inspector Button -->
      <button onclick="toggleInspector()" id="btn-toggle-inspector" title="Toggle Inspector [I]" class="p-1.5 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 hover:text-white hover:border-slate-700 transition-all">
        <i data-lucide="panel-right-close" id="icon-toggle-inspector" class="w-3.5 h-3.5 text-cyan-400"></i>
      </button>
    </div>
  </header>
""")

    # 3. THREE-COLUMN COCKPIT BODY
    html.append(f"""
  <!-- WORKSPACE BODY (ZERO SCROLL CONTAINER) -->
  <div class="flex-1 flex overflow-hidden relative min-h-0">

    <!-- LEFT SIDEBAR: DIRECTORY -->
    <aside id="cockpit-sidebar" class="w-72 bg-[#090b10] border-r border-white/[0.08] flex flex-col shrink-0 overflow-hidden transition-all duration-300">
      <div class="p-3 border-b border-white/[0.06] flex items-center justify-between text-[11px] font-mono font-bold text-slate-400">
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

      <!-- Items List -->
      <div id="sidebar-items-list" class="flex-1 overflow-y-auto custom-scroll p-2 space-y-1">
        <!-- Dynamically populated by renderSidebar() -->
      </div>
    </aside>

    <!-- CENTER WORKBENCH (FLEX-1) -->
    <main class="flex-1 flex flex-col bg-[#0c0e14] overflow-hidden min-w-0">
      
      <!-- Top Workbench Mode Bar: Studio + Global Labs -->
      <div class="h-11 border-b border-white/[0.08] bg-[#090b10] px-3 flex items-center justify-between gap-3 shrink-0">
        
        <!-- Left group: Sidebar Toggle & Studio + 5 Global Simulators -->
        <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
          <button onclick="toggleSidebar()" id="btn-toggle-sidebar" title="Toggle Directory [B]" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all shrink-0">
            <i data-lucide="panel-left-close" id="icon-toggle-sidebar" class="w-4 h-4"></i>
          </button>

          <div class="h-4 w-px bg-slate-800 mx-1 shrink-0"></div>

          <!-- Primary Studio & Global Labs Switchers -->
          <button onclick="switchWorkbenchMode('studio')" id="btn-mode-studio" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 text-slate-950 transition-all flex items-center gap-1.5 shrink-0 shadow-lg shadow-emerald-500/10">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> <span>Topic Studio (5D)</span>
          </button>
          <button onclick="switchWorkbenchMode('tracer')" id="btn-mode-tracer" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0">
            <i data-lucide="network" class="w-3.5 h-3.5"></i> <span>Packet Tracer</span>
          </button>
          <button onclick="switchWorkbenchMode('finops')" id="btn-mode-finops" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0">
            <i data-lucide="calculator" class="w-3.5 h-3.5"></i> <span>AWS FinOps</span>
          </button>
          <button onclick="switchWorkbenchMode('ring')" id="btn-mode-ring" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0">
            <i data-lucide="circle-dot" class="w-3.5 h-3.5"></i> <span>Server Distribution (Ring &amp; LB)</span>
          </button>
          <button onclick="switchWorkbenchMode('limiter')" id="btn-mode-limiter" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0">
            <i data-lucide="gauge" class="w-3.5 h-3.5"></i> <span>Rate Limiter</span>
          </button>
          <button onclick="switchWorkbenchMode('interview')" id="btn-mode-interview" class="mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0">
            <i data-lucide="clock" class="w-3.5 h-3.5"></i> <span>Interview Studio</span>
          </button>
        </div>
      </div>

      <!-- WORKBENCH BODY STAGES -->
      <div class="flex-1 overflow-hidden relative">

        <!-- 1. TOPIC STUDIO (5-DIMENSION MULTI-TAB MASTERCLASS) -->
        <div id="view-studio" class="workbench-view h-full flex flex-col overflow-hidden">
          
          <!-- Sticky Topic Header Card -->
          <div class="p-4 lg:px-8 border-b border-white/[0.06] bg-[#090b10] shrink-0">
            <div class="max-w-5xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div class="flex items-center gap-2 text-xs font-mono text-slate-400 mb-1">
                  <span id="topic-stage-crumb" class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">STAGE 01</span>
                  <span>&bull;</span>
                  <span id="topic-diff-crumb" class="text-cyan-400 font-bold">Day 1 Beginner</span>
                  <span>&bull;</span>
                  <span id="topic-time-crumb" class="text-slate-400">18 min read</span>
                </div>
                <h2 id="topic-title" class="text-xl lg:text-2xl font-black text-white tracking-tight">1.1 The Client-Server Model &amp; Sockets</h2>
                <p id="topic-summary" class="text-xs text-slate-400 mt-1 max-w-3xl">First principles: What is a computer network? IPv4/IPv6, TCP ports, and socket descriptors.</p>
              </div>

              <!-- Action Buttons -->
              <div class="flex items-center gap-2.5 shrink-0">
                <!-- Quick Simulator Shortcut Button -->
                <button onclick="launchCurrentTopicSimulator()" id="btn-quick-sim" class="px-3.5 py-2 rounded-xl bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-xs font-mono font-bold hover:bg-cyan-500/20 transition-all flex items-center gap-1.5 shadow-lg shadow-cyan-500/10 cursor-pointer">
                  <i data-lucide="play" class="w-3.5 h-3.5"></i>
                  <span id="btn-quick-sim-text">Launch Lab</span>
                </button>

                <!-- Mark Mastered Action -->
                <button onclick="toggleItemCompleteCurrent()" id="btn-mark-done" class="px-4 py-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold hover:bg-emerald-500/20 transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/10 cursor-pointer">
                  <i data-lucide="check-circle" class="w-4 h-4"></i>
                  <span id="btn-mark-done-text">Mark Mastered</span>
                </button>
              </div>
            </div>

            <!-- The 5-Dimension Sub-Tab Selector -->
            <div class="max-w-5xl mx-auto mt-3.5 pt-3 border-t border-slate-800/80 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
              <button onclick="switchTopicDimension('guidebook')" id="tab-dim-guidebook" class="dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-slate-800 text-white border border-slate-700 transition-all flex items-center gap-1.5 shrink-0">
                <i data-lucide="book-open" class="w-3.5 h-3.5 text-emerald-400"></i>
                <span>Master Guidebook</span>
              </button>
              <button onclick="switchTopicDimension('topology')" id="tab-dim-topology" class="dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent transition-all flex items-center gap-1.5 shrink-0">
                <i data-lucide="git-branch" class="w-3.5 h-3.5 text-cyan-400"></i>
                <span>Vector Topology</span>
              </button>
              <button onclick="switchTopicDimension('code')" id="tab-dim-code" class="dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent transition-all flex items-center gap-1.5 shrink-0">
                <i data-lucide="code" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>Production Code</span>
              </button>
              <button onclick="switchTopicDimension('disasters')" id="tab-dim-disasters" class="dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent transition-all flex items-center gap-1.5 shrink-0">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-400"></i>
                <span>Outage Post-Mortems</span>
              </button>
              <button onclick="switchTopicDimension('interview')" id="tab-dim-interview" class="dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent transition-all flex items-center gap-1.5 shrink-0">
                <i data-lucide="shield-check" class="w-3.5 h-3.5 text-fuchsia-400"></i>
                <span>Staff Interview Defense</span>
              </button>
            </div>
          </div>

          <!-- Dimension Content Scrollable Body -->
          <div class="flex-1 overflow-y-auto custom-scroll p-6 lg:p-8">
            <div class="max-w-5xl mx-auto">
              
              <!-- 1. Master Guidebook Dimension -->
              <div id="dim-view-guidebook" class="dim-content-view space-y-6">
                <div id="topic-guidebook-body"></div>
              </div>

              <!-- 2. Vector Topology Dimension -->
              <div id="dim-view-topology" class="dim-content-view hidden space-y-4">
                <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div class="text-xs font-mono font-bold text-slate-300 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                    <span>PRODUCTION ARCHITECTURAL SCHEMATIC</span>
                  </div>
                  <span class="text-[10px] font-mono text-slate-500">Vector SVG &bull; High Resolution</span>
                </div>
                <div id="topic-topology-svg" class="w-full"></div>
              </div>

              <!-- 3. Production Code Dimension -->
              <div id="dim-view-code" class="dim-content-view hidden space-y-4">
                <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div class="text-xs font-mono font-bold text-slate-300 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                    <span id="topic-code-lang">PRODUCTION-GRADE IMPLEMENTATION</span>
                  </div>
                  <button onclick="copyCurrentCode()" class="px-2.5 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-mono flex items-center gap-1.5 border border-slate-800 transition-all cursor-pointer">
                    <i data-lucide="copy" class="w-3 h-3"></i>
                    <span id="copy-btn-text">Copy Code</span>
                  </button>
                </div>
                <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 overflow-x-auto">
                  <pre id="topic-code-block" class="font-mono text-xs text-cyan-300 leading-relaxed"></pre>
                </div>
              </div>

              <!-- 4. Outage Post-Mortems Dimension -->
              <div id="dim-view-disasters" class="dim-content-view hidden space-y-4">
                <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/20 text-rose-300 flex items-center justify-between">
                  <div class="text-xs font-mono font-bold flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></span>
                    <span>PRODUCTION DISASTER CASE STUDY &amp; POST-MORTEM</span>
                  </div>
                  <span class="text-[10px] font-mono text-rose-400">Cascading Failures &bull; Remediation</span>
                </div>
                <div id="topic-disaster-body" class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4"></div>
              </div>

              <!-- 5. Staff Interview Defense Dimension -->
              <div id="dim-view-interview" class="dim-content-view hidden space-y-4">
                <div class="p-4 rounded-xl bg-fuchsia-950/20 border border-fuchsia-500/20 text-fuchsia-300 flex items-center justify-between">
                  <div class="text-xs font-mono font-bold flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-fuchsia-400"></span>
                    <span>FAANG STAFF &amp; PRINCIPAL ARCHITECT INTERVIEW DEFENSE</span>
                  </div>
                  <span class="text-[10px] font-mono text-fuchsia-400">Trap Questions &bull; Whiteboard Rubric</span>
                </div>
                <div id="topic-interview-body" class="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4"></div>
              </div>

            </div>
          </div>
        </div>

        <!-- 2. ARCHITECTURE TRACER STAGE -->
        <div id="view-tracer" class="workbench-view hidden h-full overflow-y-auto custom-scroll p-6 space-y-6">
          <div class="max-w-5xl mx-auto">
            {data_interactive_tools.TRACER_HTML}
          </div>
        </div>

        <!-- 3. FINOPS CLOUD SIZING STAGE -->
        <div id="view-finops" class="workbench-view hidden h-full overflow-y-auto custom-scroll p-6 space-y-6">
          <div class="max-w-5xl mx-auto">
            {data_interactive_tools.FINOPS_HTML}
          </div>
        </div>

        <!-- 4. CONSISTENT HASH RING STAGE -->
        <div id="view-ring" class="workbench-view hidden h-full overflow-y-auto custom-scroll p-6 space-y-6">
          <div class="max-w-5xl mx-auto">
            {data_interactive_tools.RING_HTML}
          </div>
        </div>

        <!-- 5. RATE LIMITER LAB STAGE -->
        <div id="view-limiter" class="workbench-view hidden h-full overflow-y-auto custom-scroll p-6 space-y-6">
          <div class="max-w-5xl mx-auto">
            {data_interactive_tools.LIMITER_HTML}
          </div>
        </div>

        <!-- 6. INTERVIEW STUDIO STAGE -->
        <div id="view-interview" class="workbench-view hidden h-full overflow-y-auto custom-scroll p-6 space-y-6">
          <div class="max-w-5xl mx-auto">
            {data_interactive_tools.INTERVIEW_HTML}
          </div>
        </div>

      </div>
    </main>

    <!-- RIGHT INSPECTOR PANEL (320px) -->
    <aside id="cockpit-inspector" class="w-80 bg-[#090b10] border-l border-white/[0.08] flex flex-col shrink-0 overflow-hidden transition-all duration-300">
      <div class="p-3 border-b border-white/[0.06] flex items-center justify-between text-[11px] font-mono font-bold text-slate-400">
        <span>ARCHITECTURAL INSPECTOR</span>
        <i data-lucide="info" class="w-3.5 h-3.5 text-slate-500"></i>
      </div>

      <div class="flex-1 overflow-y-auto custom-scroll p-4 space-y-5 text-xs">
        <!-- Live Telemetry Card -->
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2 font-mono">
          <div class="text-[10px] text-slate-500 uppercase">SYSTEM CLASSIFICATION</div>
          <div id="inspector-system-type" class="text-xs font-bold text-emerald-400">Stage 01 &bull; Day 1 Scratch</div>
          <div class="text-[10px] text-slate-400 pt-1 border-t border-slate-800">
            Target SLA Latency: <span id="inspector-p99" class="text-white">&lt; 10 ms</span>
          </div>
          <div class="text-[10px] text-slate-400">
            Throughput Target: <span id="inspector-throughput" class="text-cyan-400">50,000 QPS</span>
          </div>
        </div>

        <!-- Key Formula / Invariant -->
        <div class="space-y-1.5">
          <div class="text-[10px] font-mono uppercase text-slate-400 font-bold">GOLDEN INVARIANT / FORMULA</div>
          <div id="inspector-formula" class="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-cyan-300 leading-relaxed">
            Total QPS = (DAU &times; Reqs) / 86,400s
          </div>
        </div>

        <!-- Quick Battle Card Drill -->
        <div class="space-y-2 pt-2 border-t border-slate-800">
          <div class="flex items-center justify-between text-[10px] font-mono text-fuchsia-400 font-bold">
            <span>STAFF BATTLE CARD FLASH DRILL</span>
            <button onclick="cycleBattleCard()" class="text-slate-400 hover:text-white cursor-pointer">Next &rarr;</button>
          </div>
          <div id="inspector-battle-card" class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div id="bc-drill-q" class="font-bold text-white text-[11px] leading-snug">Why did Kafka drop ZooKeeper for KRaft?</div>
            <button onclick="revealCardAnswer()" id="btn-reveal-bc" class="w-full py-1 text-[10px] font-mono font-bold text-center rounded bg-slate-900 text-slate-300 hover:bg-slate-800 cursor-pointer">Reveal Staff Answer</button>
            <div id="bc-drill-ans" class="hidden text-[10px] text-slate-300 pt-1 border-t border-slate-800 leading-relaxed font-sans"></div>
          </div>
        </div>

        <!-- Shortcut Cheatsheet -->
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 font-mono text-[10px] text-slate-400">
          <div class="font-bold text-slate-300 uppercase">COCKPIT KEYMAP</div>
          <div class="flex justify-between"><span>Next / Prev Topic</span><span class="text-white">[J] / [K]</span></div>
          <div class="flex justify-between"><span>Switch 5D Tabs</span><span class="text-cyan-400">[1 - 5]</span></div>
          <div class="flex justify-between"><span>Launch Lab</span><span class="text-amber-400">[6 - 9]</span></div>
          <div class="flex justify-between"><span>Toggle Sidebar</span><span class="text-white">[B]</span></div>
          <div class="flex justify-between"><span>Toggle Inspector</span><span class="text-white">[I]</span></div>
          <div class="flex justify-between"><span>Mark Mastered</span><span class="text-emerald-400">[Space] / [M]</span></div>
        </div>

      </div>
    </aside>

  </div>
""")

    # 4. BOTTOM STATUS BAR (24px)
    html.append(f"""
  <!-- BOTTOM FIXED STATUS BAR -->
  <footer class="h-6 border-t border-white/[0.08] bg-[#090b10] px-3 flex items-center justify-between text-[10px] font-mono text-slate-500 shrink-0 z-40">
    <div class="flex items-center gap-4">
      <span class="flex items-center gap-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="status-topic" class="text-slate-300 font-bold">1.1 Client-Server</span>
      </span>
      <span class="hidden sm:inline">&bull;</span>
      <span class="hidden sm:inline">Zero-Scroll Cockpit &bull; 100x Content Engine</span>
    </div>

    <div class="flex items-center gap-4">
      <span class="hidden md:inline">[1-5] Dimension Tabs</span>
      <span class="hidden md:inline">[J/K] Navigate Topics</span>
      <span class="hidden md:inline">[B] Toggle Sidebar</span>
      <span class="hidden md:inline">[I] Toggle Inspector</span>
      <span class="text-slate-400 font-bold">NEXUS OPERATING SYSTEM</span>
    </div>
  </footer>
""")

    # 5. SCRIPT & CONTROLLERS (100% BULLETPROOF & SAFE)
    html.append(f"""
  <script>
    // Bulletproof Icon Renderer
    function safeCreateIcons() {{
      try {{
        if (window.lucide && typeof window.lucide.createIcons === 'function') {{
          window.lucide.createIcons();
        }}
      }} catch(e) {{}}
    }}

    const TOPICS = {json_topics};
    const BATTLE_CARDS = {json_battle_cards};

    let currentIndex = 0;
    let activeFilter = 'all';
    let currentDimension = 'guidebook';
    let masteredIds = JSON.parse(localStorage.getItem('cockpit_mastered_ids') || '[]');
    let audioOn = true;
    let audioCtx = null;
    let isSidebarOpen = true;
    let isInspectorOpen = true;

    // Web Audio Synthesizer Feedback
    function playClickTone(freq = 650, duration = 0.03) {{
      if (!audioOn) return;
      try {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      }} catch(e) {{}}
    }}

    function toggleAudio() {{
      audioOn = !audioOn;
      const icon = document.getElementById('audio-icon');
      if (icon) {{
        icon.setAttribute('data-lucide', audioOn ? 'volume-2' : 'volume-x');
        safeCreateIcons();
      }}
      if (audioOn) playClickTone(800, 0.04);
    }}

    // Toggle Left Sidebar
    function toggleSidebar() {{
      isSidebarOpen = !isSidebarOpen;
      playClickTone(500, 0.03);
      const sb = document.getElementById('cockpit-sidebar');
      const icon = document.getElementById('icon-toggle-sidebar');
      if (sb) {{
        if (isSidebarOpen) {{
          sb.classList.remove('w-0', 'opacity-0', 'border-r-0');
          sb.classList.add('w-72');
          if (icon) icon.setAttribute('data-lucide', 'panel-left-close');
        }} else {{
          sb.classList.remove('w-72');
          sb.classList.add('w-0', 'opacity-0', 'border-r-0');
          if (icon) icon.setAttribute('data-lucide', 'panel-left-open');
        }}
        safeCreateIcons();
      }}
    }}

    // Toggle Right Inspector
    function toggleInspector() {{
      isInspectorOpen = !isInspectorOpen;
      playClickTone(500, 0.03);
      const insp = document.getElementById('cockpit-inspector');
      const icon = document.getElementById('icon-toggle-inspector');
      if (insp) {{
        if (isInspectorOpen) {{
          insp.classList.remove('w-0', 'opacity-0', 'border-l-0');
          insp.classList.add('w-80');
          if (icon) icon.setAttribute('data-lucide', 'panel-right-close');
        }} else {{
          insp.classList.remove('w-80');
          insp.classList.add('w-0', 'opacity-0', 'border-l-0');
          if (icon) icon.setAttribute('data-lucide', 'panel-right-open');
        }}
        safeCreateIcons();
      }}
    }}

    let sidebarSearchQuery = '';

    function filterSidebarBySearch(q) {{
      sidebarSearchQuery = (q || '').trim().toLowerCase();
      const clearBtn = document.getElementById('sidebar-search-clear');
      if (clearBtn) {{
        if (sidebarSearchQuery.length > 0) {{
          clearBtn.classList.remove('hidden');
        }} else {{
          clearBtn.classList.add('hidden');
        }}
      }}
      renderSidebar();
    }}

    function clearSidebarSearch() {{
      const input = document.getElementById('sidebar-search-input');
      if (input) input.value = '';
      sidebarSearchQuery = '';
      const clearBtn = document.getElementById('sidebar-search-clear');
      if (clearBtn) clearBtn.classList.add('hidden');
      renderSidebar();
      if (input) input.focus();
    }}

    // Render Left Sidebar List
    function renderSidebar() {{
      const container = document.getElementById('sidebar-items-list');
      if (!container) return;
      
      const filtered = TOPICS.filter(it => {{
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
      }});

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div class="p-6 text-center text-slate-500 text-xs font-mono space-y-2">
            <i data-lucide="search-x" class="w-8 h-8 text-slate-600 mx-auto stroke-1"></i>
            <div>No modules matching "<span class="text-white">${{sidebarSearchQuery}}</span>"</div>
            <button onclick="clearSidebarSearch()" class="px-3 py-1.5 rounded-lg bg-slate-900 text-cyan-400 hover:text-cyan-300 text-[11px] font-bold border border-slate-800 transition-all cursor-pointer">Clear Search</button>
          </div>
        `;
        safeCreateIcons();
        const countEl = document.getElementById('sidebar-count');
        if (countEl) countEl.innerText = '0 Matches';
        return;
      }}

      container.innerHTML = filtered.map((it, idx) => {{
        const isMastered = masteredIds.includes(it.id);
        const isActive = TOPICS[currentIndex] && TOPICS[currentIndex].id === it.id;
        const activeClass = isActive 
          ? 'bg-emerald-500/15 border-emerald-500/50 text-white font-bold' 
          : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-white hover:bg-slate-900';
        return `
          <div onclick="selectItemById('${{it.id}}')" class="p-2.5 rounded-xl border ${{activeClass}} cursor-pointer transition-all flex items-center justify-between gap-2 text-xs">
            <div class="flex items-center gap-2 truncate">
              <span class="w-1.5 h-1.5 rounded-full ${{isActive ? 'bg-emerald-400 animate-pulse' : (isMastered ? 'bg-emerald-500' : 'bg-slate-700')}}"></span>
              <span class="truncate">${{it.title}}</span>
            </div>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-500 shrink-0">${{it.stageNum}}</span>
          </div>
        `;
      }}).join('');

      const countEl = document.getElementById('sidebar-count');
      if (countEl) {{
        if (sidebarSearchQuery) {{
          countEl.innerText = `${{filtered.length}} / ${{TOPICS.length}} Matches`;
        }} else {{
          countEl.innerText = `${{filtered.length}} Modules`;
        }}
      }}
    }}

    function filterSidebar(filter) {{
      playClickTone(500, 0.02);
      activeFilter = filter;
      document.querySelectorAll('.stage-filter-btn').forEach(btn => {{
        btn.className = 'stage-filter-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white transition-all';
      }});
      const target = document.getElementById('filter-' + filter);
      if (target) {{
        target.className = 'stage-filter-btn px-2.5 py-1 rounded-lg text-white bg-slate-800 font-bold transition-all';
      }}
      renderSidebar();
    }}

    function selectItemById(id) {{
      const idx = TOPICS.findIndex(x => x.id === id);
      if (idx >= 0) {{
        currentIndex = idx;
        switchWorkbenchMode('studio');
        loadTopic();
      }}
    }}

    // Load active topic data across all 5 dimensions
    function loadTopic() {{
      const it = TOPICS[currentIndex];
      if (!it) return;

      playClickTone(600, 0.02);

      // Topic Header
      const tSc = document.getElementById('topic-stage-crumb'); if (tSc) tSc.innerText = it.stageNum;
      const tTc = document.getElementById('topic-time-crumb'); if (tTc) tTc.innerText = it.readTime;
      const tDc = document.getElementById('topic-diff-crumb'); if (tDc) tDc.innerText = it.difficulty;
      const tTitle = document.getElementById('topic-title'); if (tTitle) tTitle.innerText = it.title;
      const tSummary = document.getElementById('topic-summary'); if (tSummary) tSummary.innerText = it.summary;

      // Populate 5 Dimensions
      const gBody = document.getElementById('topic-guidebook-body'); if (gBody) gBody.innerHTML = it.guidebook || '<p class="text-slate-400">Content loading...</p>';
      const topSvg = document.getElementById('topic-topology-svg'); if (topSvg) topSvg.innerHTML = it.topologySvg || '<p class="text-slate-400">Topology schematic loading...</p>';
      const cBlock = document.getElementById('topic-code-block'); if (cBlock) cBlock.innerText = it.codeSnippet || '// Production implementation loading...';
      const dBody = document.getElementById('topic-disaster-body'); if (dBody) dBody.innerHTML = it.disasterStudy || '<p class="text-slate-400">Disaster study loading...</p>';
      const iBody = document.getElementById('topic-interview-body'); if (iBody) iBody.innerHTML = it.interviewDefense || '<p class="text-slate-400">Interview defense loading...</p>';

      // Bottom Status bar
      const sTopic = document.getElementById('status-topic'); if (sTopic) sTopic.innerText = it.title;

      // Quick Lab Launch text
      const simNames = {{
        'tracer': 'Open in Packet Tracer',
        'finops': 'Open in AWS FinOps',
        'ring': 'Open in Hash Ring',
        'limiter': 'Open in Rate Limiter',
        'interview': 'Open in Mock Studio'
      }};
      const simBtnText = document.getElementById('btn-quick-sim-text');
      if (simBtnText) {{
        simBtnText.innerText = simNames[it.simulatorKey] || 'Launch Lab';
      }}

      // Inspector Telemetry
      const iType = document.getElementById('inspector-system-type'); if (iType) iType.innerText = `${{it.stageNum}} &bull; ${{it.badge}}`;
      const iP99 = document.getElementById('inspector-p99'); if (iP99) iP99.innerText = it.type === 'blueprint' ? '< 30 ms' : '< 5 ms';
      const iTput = document.getElementById('inspector-throughput'); if (iTput) iTput.innerText = it.type === 'blueprint' ? '250,000 QPS' : '50,000 QPS';

      // Mark Mastered button state
      const markBtn = document.getElementById('btn-mark-done');
      const markText = document.getElementById('btn-mark-done-text');
      if (markBtn && markText) {{
        if (masteredIds.includes(it.id)) {{
          markBtn.className = 'px-4 py-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-mono font-bold transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/15 cursor-pointer';
          markText.innerText = 'Mastered (Done)';
        }} else {{
          markBtn.className = 'px-4 py-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold hover:bg-emerald-500/20 transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/10 cursor-pointer';
          markText.innerText = 'Mark Mastered';
        }}
      }}

      // Synchronize active dimension tab view
      switchTopicDimension(currentDimension || 'guidebook');

      renderSidebar();
      updateMasteryStatus();
      safeCreateIcons();
    }}

    // Switch between the 5 topic study dimensions
    function switchTopicDimension(dim) {{
      playClickTone(700, 0.02);
      currentDimension = dim;

      document.querySelectorAll('.dim-content-view').forEach(v => v.classList.add('hidden'));
      const activeDimView = document.getElementById('dim-view-' + dim);
      if (activeDimView) activeDimView.classList.remove('hidden');

      document.querySelectorAll('.dim-tab-btn').forEach(btn => {{
        btn.className = 'dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent transition-all flex items-center gap-1.5 shrink-0';
      }});
      const targetBtn = document.getElementById('tab-dim-' + dim);
      if (targetBtn) {{
        targetBtn.className = 'dim-tab-btn px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-slate-800 text-white border border-slate-700 transition-all flex items-center gap-1.5 shrink-0 shadow-lg';
      }}
      safeCreateIcons();
    }}

    function launchCurrentTopicSimulator() {{
      const it = TOPICS[currentIndex];
      if (!it) return;
      const sim = it.simulatorKey || 'tracer';
      switchWorkbenchMode(sim);
    }}

    function copyCurrentCode() {{
      const it = TOPICS[currentIndex];
      if (!it || !it.codeSnippet) return;
      playClickTone(900, 0.03);
      const text = it.codeSnippet;
      
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
      }} else {{
        fallbackCopy(text);
      }}

      const btnText = document.getElementById('copy-btn-text');
      if (btnText) {{
        btnText.innerText = 'Copied!';
        setTimeout(() => {{ btnText.innerText = 'Copy Code'; }}, 2000);
      }}
    }}

    function fallbackCopy(text) {{
      try {{
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }} catch(e) {{}}
    }}

    function toggleItemCompleteCurrent() {{
      const it = TOPICS[currentIndex];
      if (!it) return;
      playClickTone(900, 0.04);
      const idx = masteredIds.indexOf(it.id);
      if (idx >= 0) {{
        masteredIds.splice(idx, 1);
      }} else {{
        masteredIds.push(it.id);
        if (masteredIds.length === TOPICS.length && typeof confetti === 'function') {{
          try {{
            confetti({{ particleCount: 200, spread: 80, origin: {{ y: 0.6 }} }});
          }} catch(e) {{}}
        }}
      }}
      localStorage.setItem('cockpit_mastered_ids', JSON.stringify(masteredIds));
      loadTopic();
    }}

    function updateMasteryStatus() {{
      const pct = Math.round((masteredIds.length / TOPICS.length) * 100);
      const mText = document.getElementById('cockpit-mastery-text'); if (mText) mText.innerText = `${{pct}}% Mastery`;
      const mRing = document.getElementById('cockpit-progress-ring'); if (mRing) mRing.setAttribute('stroke-dasharray', `${{pct}}, 100`);
    }}

    // Workbench Mode Switcher (Studio vs Global Simulators)
    function switchWorkbenchMode(mode) {{
      playClickTone(700, 0.02);
      document.querySelectorAll('.workbench-view').forEach(v => v.classList.add('hidden'));
      const activeView = document.getElementById('view-' + mode);
      if (activeView) activeView.classList.remove('hidden');

      document.querySelectorAll('.mode-tab-btn').forEach(btn => {{
        btn.className = 'mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-white transition-all flex items-center gap-1.5 shrink-0';
      }});
      const targetBtn = document.getElementById('btn-mode-' + mode);
      if (targetBtn) {{
        targetBtn.className = 'mode-tab-btn px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 text-slate-950 transition-all flex items-center gap-1.5 shrink-0 shadow-lg shadow-emerald-500/10';
      }}

      // Activate simulator lifecycle hooks
      if (mode === 'ring') {{
        if (typeof renderLiveHashRing === 'function') renderLiveHashRing();
        if (typeof renderLbUI === 'function') renderLbUI();
      }}
      if (mode === 'finops' && typeof recomputeCost === 'function') recomputeCost();
      if (mode === 'limiter' && typeof updateLiveRlUI === 'function') updateLiveRlUI();
      if (mode === 'interview' && typeof renderStudioTimer === 'function') renderStudioTimer();
      if (mode === 'tracer' && typeof inspectNode === 'function') inspectNode('client');

      safeCreateIcons();
    }}

    // Battle Card Drill Controller (Handles q / ans properly)
    let currentBcIdx = 0;
    function renderBattleCard() {{
      const card = BATTLE_CARDS[currentBcIdx];
      if (!card) return;
      const qEl = document.getElementById('bc-drill-q'); 
      if (qEl) qEl.innerText = card.q || card.front || 'Question';
      
      const ansEl = document.getElementById('bc-drill-ans');
      const btn = document.getElementById('btn-reveal-bc');
      if (ansEl) {{
        ansEl.innerText = card.ans || card.back || 'Answer';
        ansEl.classList.add('hidden');
      }}
      if (btn) btn.innerText = 'Reveal Staff Answer';
    }}

    function revealCardAnswer() {{
      playClickTone(800, 0.02);
      const ansEl = document.getElementById('bc-drill-ans');
      const btn = document.getElementById('btn-reveal-bc');
      if (ansEl && ansEl.classList.contains('hidden')) {{
        ansEl.classList.remove('hidden');
        if (btn) btn.innerText = 'Hide Answer';
      }} else if (ansEl) {{
        ansEl.classList.add('hidden');
        if (btn) btn.innerText = 'Reveal Staff Answer';
      }}
    }}

    function cycleBattleCard() {{
      playClickTone(600, 0.02);
      currentBcIdx = (currentBcIdx + 1) % BATTLE_CARDS.length;
      renderBattleCard();
    }}

    // Keyboard Shortcuts Navigation
    document.addEventListener('keydown', (e) => {{
      // Focus search shortcut / or Ctrl+K
      if ((e.key === '/' || ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K'))) && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
        e.preventDefault();
        if (!isSidebarOpen) toggleSidebar();
        const searchInput = document.getElementById('sidebar-search-input');
        if (searchInput) {{
          searchInput.focus();
          searchInput.select();
        }}
        return;
      }}

      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {{
        if (e.key === 'Escape') {{
          e.target.blur();
        }}
        return;
      }}

      // J: Next Topic
      if (e.key === 'j' || e.key === 'J') {{
        if (currentIndex < TOPICS.length - 1) {{
          currentIndex++;
          switchWorkbenchMode('studio');
          loadTopic();
        }}
      }}
      // K: Prev Topic
      if (e.key === 'k' || e.key === 'K') {{
        if (currentIndex > 0) {{
          currentIndex--;
          switchWorkbenchMode('studio');
          loadTopic();
        }}
      }}
      // B: Toggle Sidebar
      if (e.key === 'b' || e.key === 'B') {{
        toggleSidebar();
      }}
      // I: Toggle Inspector
      if (e.key === 'i' || e.key === 'I') {{
        toggleInspector();
      }}
      // Space or M: Mark Mastered
      if (e.key === ' ' || e.key === 'm' || e.key === 'M') {{
        e.preventDefault();
        toggleItemCompleteCurrent();
      }}
      // 1-5: Switch Dimension Tabs in Topic Studio
      if (e.key === '1') switchTopicDimension('guidebook');
      if (e.key === '2') switchTopicDimension('topology');
      if (e.key === '3') switchTopicDimension('code');
      if (e.key === '4') switchTopicDimension('disasters');
      if (e.key === '5') switchTopicDimension('interview');

      // 6-9: Switch Global Labs
      if (e.key === '6') switchWorkbenchMode('tracer');
      if (e.key === '7') switchWorkbenchMode('finops');
      if (e.key === '8') switchWorkbenchMode('ring');
      if (e.key === '9') switchWorkbenchMode('limiter');
    }});

    // Bulletproof App Initialization (Guaranteed to execute regardless of load order)
    function initCockpitApp() {{
      try {{
        renderSidebar();
        loadTopic();
        renderBattleCard();
        updateMasteryStatus();
        if (typeof initServerDistribution === 'function') initServerDistribution();
        if (typeof recomputeCost === 'function') recomputeCost();
        if (typeof startLiveRlEngine === 'function') startLiveRlEngine();
        safeCreateIcons();
      }} catch(err) {{
        console.error("Cockpit Initialization Exception:", err);
      }}
    }}

    if (document.readyState === 'loading') {{
      document.addEventListener('DOMContentLoaded', initCockpitApp);
    }} else {{
      initCockpitApp();
    }}
    window.addEventListener('load', () => {{
      const list = document.getElementById('sidebar-items-list');
      if (list && !list.hasChildNodes()) {{
        initCockpitApp();
      }}
      safeCreateIcons();
    }});
  </script>

  <!-- Interactive Simulators Engine Scripts (Safely wrapped in script tags) -->
  <script>
    {data_interactive_tools.TOOLS_JS}
  </script>

</body>
</html>
""")

    output_html = "\n".join(html)

    target_path = os.path.join(os.path.dirname(__file__), "god_level_system_design.html")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"SUCCESS: Generated {target_path} (Size: {len(output_html):,} bytes)")

if __name__ == "__main__":
    build_cockpit_100x()
