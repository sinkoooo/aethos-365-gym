# generate_full_cockpit_html.py
# Generates the complete 100x Google Staff & Principal Engineering Cockpit HTML

import json
import shutil
import modules_data
import system_design_data
import learning_resources_data
import modules_tech
import interactive_stages_data

def build_full_html():
    modules = modules_data.MODULES_LIST
    sd_map = system_design_data.SYSTEM_DESIGNS
    lr_map = learning_resources_data.RESOURCES_DATA
    tech_map = {m["id"]: m for m in modules_tech.MODULES}

    html = []

    # 1. HTML HEAD & FAVICON & STYLES
    html.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nexus Architect • Staff Systems Mastery</title>
  
  <!-- High-Tech Architectural SVG Favicon -->
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpolygon points='20,2 38,12 38,28 20,38 2,28 2,12' stroke='%2300f0ff' stroke-width='2.5' fill='%23050b1a'/%3E%3Ccircle cx='20' cy='20' r='6' fill='%2300f0ff'/%3E%3Cpath d='M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17' stroke='%2338bdf8' stroke-width='1.5'/%3E%3C/svg%3E">
  <link rel="shortcut icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpolygon points='20,2 38,12 38,28 20,38 2,28 2,12' stroke='%2300f0ff' stroke-width='2.5' fill='%23050b1a'/%3E%3Ccircle cx='20' cy='20' r='6' fill='%2300f0ff'/%3E%3Cpath d='M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17' stroke='%2338bdf8' stroke-width='1.5'/%3E%3C/svg%3E">

  <!-- Tailwind CSS & Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #02040d;
      color: #cbd5e1;
    }
    code, pre, .font-mono {
      font-family: 'Fira Code', monospace;
    }
    
    /* Clean Modern Scrollbar System (Zero Visual Clutter) */
    
    /* 1. Globally remove all horizontal scrollbars completely */
    ::-webkit-scrollbar:horizontal {
      display: none !important;
      height: 0px !important;
      width: 0px !important;
    }
    
    /* 2. Hide scrollbars on any element marked with .no-scrollbar */
    .no-scrollbar::-webkit-scrollbar {
      display: none !important;
      width: 0px !important;
      height: 0px !important;
    }
    .no-scrollbar {
      -ms-overflow-style: none !important;
      scrollbar-width: none !important;
    }

    /* 3. Subtle, elegant vertical scrollbar ONLY for main reading areas */
    .main-stage-scroll::-webkit-scrollbar,
    .custom-scroll::-webkit-scrollbar {
      width: 5px;
    }
    .main-stage-scroll::-webkit-scrollbar-track,
    .custom-scroll::-webkit-scrollbar-track {
      background: transparent;
    }
    .main-stage-scroll::-webkit-scrollbar-thumb,
    .custom-scroll::-webkit-scrollbar-thumb {
      background: rgba(148, 163, 184, 0.2);
      border-radius: 9999px;
      transition: background 0.2s ease;
    }
    .main-stage-scroll::-webkit-scrollbar-thumb:hover,
    .custom-scroll::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 240, 255, 0.6);
    }

    /* General containers: hide scrollbars by default to prevent visual clutter */
    body, div, aside, nav, pre, code {
      scrollbar-width: none;
    }
    ::-webkit-scrollbar {
      width: 0px;
      height: 0px;
    }
    .main-stage-scroll, .custom-scroll {
      overflow-y: auto !important;
      overflow-x: hidden !important;
      scrollbar-width: thin !important;
      scrollbar-color: rgba(148, 163, 184, 0.25) transparent !important;
    }
    .main-stage-scroll::-webkit-scrollbar {
      width: 6px;
    }
    .main-stage-scroll::-webkit-scrollbar-thumb {
      background: rgba(148, 163, 184, 0.25);
      border-radius: 9999px;
    }

    /* Floating XP Notification Animation */
    @keyframes floatUpFade {
      0% { transform: translateY(0px) scale(0.9); opacity: 0; }
      20% { transform: translateY(-8px) scale(1.05); opacity: 1; }
      80% { transform: translateY(-28px) scale(1); opacity: 1; }
      100% { transform: translateY(-40px) scale(0.95); opacity: 0; }
    }
    .xp-float-particle {
      animation: floatUpFade 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Frosted Glass & Glow */
    .glass-panel {
      background: rgba(5, 11, 26, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glow-cyan {
      box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
    }
    .glow-border {
      border: 1px solid rgba(0, 240, 255, 0.3);
    }

    /* Micro-Tabs & Simulator Tab Buttons (Modern Pill Layout) */
    .micro-tab, .tab-btn {
      cursor: pointer !important;
      user-select: none;
      white-space: nowrap;
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 0.5rem;
      background: rgba(15, 23, 42, 0.7);
      color: #94a3b8;
    }
    .micro-tab:hover, .tab-btn:hover {
      color: #ffffff !important;
      background: rgba(30, 41, 59, 0.85) !important;
      border-color: rgba(0, 240, 255, 0.35) !important;
      transform: translateY(-1px);
    }
    .micro-tab.active, .tab-btn.active {
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(6, 182, 212, 0.12)) !important;
      color: #38bdf8 !important;
      border: 1px solid rgba(56, 189, 248, 0.6) !important;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2) !important;
      font-weight: 700 !important;
    }

    /* Sidebar Navigation Items */
    .side-nav-item {
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
    }
    .side-nav-item:hover {
      background: rgba(255, 255, 255, 0.05);
      color: #ffffff;
    }
    .side-nav-item.active {
      background: rgba(0, 240, 255, 0.15) !important;
      border-color: #00f0ff !important;
      color: #00f0ff !important;
      font-weight: 700;
    }

    /* 3D Flip Card */
    .flashcard-container { perspective: 1000px; }
    .flashcard {
      transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
      cursor: pointer;
    }
    .flashcard.flipped { transform: rotateY(180deg); }
    .flashcard-front, .flashcard-back {
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
    }
    .flashcard-back { transform: rotateY(180deg); }

    /* Whiteboard Nodes */
    .wb-node {
      user-select: none;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .wb-node.selected {
      outline: 2px solid #00f0ff !important;
      border-color: #00f0ff !important;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.6) !important;
    }
    .wb-tool.active {
      background: #0284c7 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
    }

    .toast {
      transform: translateY(100px);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    /* Stage Sections Display Isolation (Guarantees only ONE stage visible at a time) */
    .stage-section {
      display: none !important;
    }
    .stage-section.active-stage {
      display: flex !important;
    }
  </style>
</head>
<body class="bg-[#02040d] text-slate-200 h-screen overflow-hidden flex flex-col font-sans antialiased selection:bg-cyan-600 selection:text-white">
''')

    # 2. TOP COMPACT HEADER (54px Fixed Height) - L6 STAFF ARCHITECT REMOVED!
    html.append('''
  <!-- TOP COMPACT WORKSPACE HEADER -->
  <header class="h-[54px] shrink-0 bg-[#040817]/95 border-b border-white/[0.08] px-4 flex items-center justify-between gap-3 z-30 shadow-lg">
    
    <!-- Brand Identity & Gamification Hub -->
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700/80 flex items-center justify-center p-1 shadow">
        <svg class="w-6 h-6" viewBox="0 0 40 40" fill="none">
          <polygon points="20,2 38,12 38,28 20,38 2,28 2,12" stroke="#00f0ff" stroke-width="2.5" fill="#080e22"/>
          <circle cx="20" cy="20" r="5" fill="#00f0ff"/>
          <path d="M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17" stroke="#38bdf8" stroke-width="1.5"/>
        </svg>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-sm font-black text-white font-mono tracking-wider">NEXUS<span class="text-cyan-400">.ARCHITECT</span></span>
          
          <!-- WORKING XP & ACHIEVEMENTS HUB BUTTON -->
          <button onclick="openGamificationModal()" class="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-700/60 text-[10px] font-mono text-emerald-300 transition-all shadow" title="Click to view Level Milestones & Unlocked Achievements">
            <span>⭐</span>
            <span id="xp-display" class="font-bold">0</span> XP
          </button>

          <!-- WORKING DAILY STREAK TRACKER BUTTON -->
          <button onclick="openStreakModal()" class="flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-950/80 hover:bg-amber-900 border border-amber-700/60 text-[10px] font-mono text-amber-300 transition-all shadow" title="Click to view 14-Day Study Consistency Heatmap">
            <span>🔥</span>
            <span id="streak-display" class="font-bold">0-Day Streak</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Center-Left: Neural Spotlight Search & Command Palette (Ctrl+K) -->
    <button onclick="openCommandPalette()" class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/80 hover:border-cyan-500/60 text-xs font-mono text-slate-300 transition-all shadow hover:shadow-cyan-500/20 group cursor-pointer" title="Open Neural Command Palette (Ctrl+K or Cmd+K)">
      <span class="text-cyan-400 group-hover:scale-125 transition-transform">⚡</span>
      <span class="text-slate-400 group-hover:text-slate-200 transition-colors">Neural Jump &amp; Search...</span>
      <kbd class="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[9px] text-cyan-400 font-bold shadow-inner">Ctrl+K</kbd>
    </button>

    <!-- Center: 100x Enhanced Pomodoro & Deep Work Cockpit Button -->
    <div class="flex items-center gap-2 px-3 py-1 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-mono shadow">
      <span class="text-slate-400">⏱️ Focus:</span>
      <span id="pomo-display" class="font-bold text-cyan-400 text-xs">25:00</span>
      <button onclick="togglePomodoro()" id="btn-pomo-toggle" class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 text-[10px]">Start</button>
      <button onclick="openFocusCockpitModal()" class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]" title="Open 100x Focus Cockpit (Soundscapes & Zen Mode)">⚙️ Modes</button>
    </div>

    <!-- Right Controls: Split Studio, Fullscreen Studio, Ambush Drill, Progress -->
    <div class="flex items-center space-x-2 text-xs">
      
      <!-- Split Studio Toggle -->
      <button onclick="toggleSplitStudio()" id="btn-split-toggle" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 transition-all shadow" title="Toggle side-by-side Whiteboard Studio while reading">
        <span>◫</span>
        <span class="hidden sm:inline">Split Studio</span>
      </button>

      <!-- Fullscreen Whiteboard Studio Modal -->
      <button onclick="openWhiteboardModal()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition-all" title="Open full-screen Whiteboard Studio">
        <span>🎨</span>
        <span class="hidden lg:inline">Whiteboard</span>
      </button>

      <!-- Surprise L8 Ambush Question -->
      <button onclick="triggerRandomTrapQuestion()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-rose-950/80 hover:bg-rose-900 border border-rose-800 text-rose-300 transition-all shadow" title="Surprise Google Staff Trap Question">
        <span>⚔️</span>
        <span class="hidden xl:inline">Ambush Drill</span>
      </button>

      <!-- Cyber Audio Synthesizer Toggle -->
      <button onclick="toggleSoundFX()" id="btn-sound-toggle" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition-all shadow hover:border-cyan-500/50" title="Toggle Cyber Audio Synthesizer (Click/Chirp/Chime/Ping)">
        <span id="sound-icon">🔊</span>
        <span class="hidden 2xl:inline text-[10px] font-mono text-cyan-400">AUDIO</span>
      </button>

      <!-- Progress Meter -->
      <div class="hidden xl:flex items-center gap-2 pl-2 border-l border-slate-800">
        <div class="w-20 bg-slate-800 h-2 rounded-full overflow-hidden">
          <div id="progress-bar" class="bg-gradient-to-r from-cyan-500 to-indigo-500 h-full w-[45%] transition-all"></div>
        </div>
        <span id="progress-percent" class="text-[10px] font-mono text-cyan-400 font-bold">45%</span>
      </div>
    </div>
  </header>
''')

    # 3. MAIN WORKSPACE WITH SIDEBAR & 17 STAGES
    html.append('''
  <!-- MAIN WORKSPACE VIEWPORT (100vh - 54px Header) -->
  <main class="flex-1 flex overflow-hidden relative">
    
    <!-- LEFT SIDEBAR: 12 CORE MODULES + 5 ADVANCED STAGES (Total 17 Stages) -->
    <aside class="w-64 sm:w-72 shrink-0 bg-[#030614] border-r border-white/[0.08] flex flex-col overflow-hidden select-none" id="sidebar-nav">
      
      <!-- Sidebar Title & Track Filter -->
      <div class="p-3 border-b border-white/[0.08] bg-[#040817] flex items-center justify-between">
        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 font-mono">Curriculum Roadmap (17 Stages)</span>
        <span class="text-[9px] bg-cyan-950 text-cyan-400 px-1.5 py-0.5 rounded font-mono font-bold">L6/L8 Track</span>
      </div>

      <!-- Navigation List -->
      <div class="flex-1 overflow-y-auto no-scrollbar p-2 space-y-1 text-xs">
''')

    # Build Sidebar navigation items
    # Track grouping
    tracks = {}
    for m in modules:
        t = m["track"]
        if t not in tracks: tracks[t] = []
        tracks[t].append(m)

    for t_name, t_mods in tracks.items():
        html.append(f'''
        <div class="pt-2 pb-1 px-2 text-[9px] font-bold text-slate-500 uppercase tracking-wider font-mono">{t_name}</div>
        ''')
        for m in t_mods:
            is_first = (m['num'] == 1)
            active_nav = " active" if is_first else ""
            html.append(f'''
        <div onclick="goToStage({m['num']})" id="side-nav-{m['num']}" class="side-nav-item{active_nav} flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-slate-900 text-cyan-400 border border-slate-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">{m['num']}</span>
            <span class="truncate font-medium">{m['title']}</span>
          </div>
          <span id="nav-ch{m['num']}-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>
            ''')

    # Add Stages 13 to 17
    html.append('''
        <div class="pt-3 pb-1 px-2 text-[9px] font-bold text-slate-500 uppercase tracking-wider font-mono">Track 7: Elite Simulators & Google Playbook</div>
        
        <div onclick="goToStage(13)" id="side-nav-13" class="side-nav-item flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">13</span>
            <span class="truncate font-medium">8 Distributed Systems Simulators</span>
          </div>
          <span class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>

        <div onclick="goToStage(14)" id="side-nav-14" class="side-nav-item flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">14</span>
            <span class="truncate font-medium">Google Staff Leadership STAR Playbook</span>
          </div>
          <span class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>

        <div onclick="goToStage(15)" id="side-nav-15" class="side-nav-item flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-blue-950 text-blue-400 border border-blue-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">15</span>
            <span class="truncate font-medium">Master Architecture Trade-Off Grid</span>
          </div>
          <span class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>

        <div onclick="goToStage(16)" id="side-nav-16" class="side-nav-item flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">16</span>
            <span class="truncate font-medium">Canonical Google Research Papers</span>
          </div>
          <span class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>

        <div onclick="goToStage(17)" id="side-nav-17" class="side-nav-item flex items-center justify-between p-2 rounded-xl border border-slate-900/60 text-slate-300">
          <div class="flex items-center gap-2 truncate">
            <span class="w-5 h-5 rounded bg-rose-950 text-rose-400 border border-rose-800 flex items-center justify-center font-mono font-bold text-[10px] shrink-0">17</span>
            <span class="truncate font-medium">Google L6/L8 Bar-Raiser Exam</span>
          </div>
          <span class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
        </div>
      </div>

      <!-- Sidebar Footer: Export All Study Notes -->
      <div class="p-3 border-t border-white/[0.08] bg-[#040817] space-y-2">
        <button onclick="exportAllStudyNotes()" class="w-full py-1.5 px-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700 hover:border-cyan-500 font-semibold text-[11px] flex items-center justify-center gap-1.5 transition-all shadow">
          <span>📑</span> Export Prep Book (.md)
        </button>
      </div>
    </aside>

    <!-- CENTER VIEWPORT: STAGES 1 TO 17 -->
    <div class="flex-1 flex flex-col overflow-hidden relative" id="main-content-viewport">
''')

    # Build Stages 1 to 12
    for m in modules:
        ch_id = m["id"]
        ch_num = m["num"]
        ch_color = m["color"]
        sys_design = sd_map.get(ch_id, {})
        lr = lr_map.get(ch_id, {})
        tldr = lr.get("tldr", {})
        diff = lr.get("diff", {})
        videos = lr.get("videos", [])
        tech = tech_map.get(ch_id, {})

        # Build Interactive Metric Cards for Numbers to Quote
        metric_cards = ""
        for n_idx, num_item in enumerate(m.get("numbers_detailed", [])):
            metric_cards += f'''
            <div onclick="openNumberDerivationModal('{ch_id}', {n_idx})" class="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/50 cursor-pointer w-full transition-all shadow text-center group">
              <span class="text-[9px] text-cyan-400 font-mono uppercase block">{num_item['category']}</span>
              <div class="text-xs font-bold text-white mt-0.5 group-hover:text-cyan-300 transition-colors">{num_item['val']}</div>
              <div class="text-[9px] text-slate-400 truncate mt-0.5">{num_item['label']}</div>
            </div>
            '''

        # Build Videos
        videos_cards = ""
        for v in videos:
            ts_html = ""
            for ts in v.get("timestamps", []):
                ts_html += f'''<div class="text-[10px] text-slate-400 font-mono"><span class="text-cyan-400 font-bold">[{ts.get('time')}]</span> {ts.get('topic')}</div>'''
            quote_box = f'''<div class="p-2 bg-slate-900/90 rounded border border-cyan-900/30 text-[11px] text-cyan-200 italic mt-2">💬 "{v.get('quote')}"</div>''' if v.get("quote") else ""
            
            videos_cards += f'''
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
              <div>
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-white truncate max-w-[240px]">{v['title']}</span>
                  <span class="text-[9px] text-cyan-400 bg-cyan-950 px-1.5 py-0.5 rounded font-mono">{v.get('duration', '45 min')}</span>
                </div>
                <div class="text-[11px] text-slate-400 font-mono mt-0.5">Speaker: <strong class="text-slate-200">{v.get('speaker')}</strong> • {v.get('event')}</div>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">{v.get('takeaway')}</p>
                {f'<div class="pt-2 border-t border-slate-900 space-y-1 mt-2">{ts_html}</div>' if ts_html else ''}
                {quote_box}
              </div>
              <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                <button onclick="openVideoModal('{v.get('videoId')}', '{v['title'].replace("'", "")}')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold flex items-center gap-1.5 shadow transition-all">
                  <span>▶</span> Watch In-App
                </button>
                <a href="{v.get('url')}" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-cyan-300 font-mono text-[11px]">
                  ↗ YouTube
                </a>
              </div>
            </div>
            '''

        # Build Traps
        traps_cards = ""
        for t_idx, trap in enumerate(tech.get("traps", [])):
            traps_cards += f'''
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 font-mono text-[10px]">Ambush #{t_idx+1}</span>
                  {trap.get('title')}
                </span>
                <button onclick="startAmbushPressureTimer('{ch_id}_{t_idx}')" class="px-2 py-0.5 rounded bg-slate-900 hover:bg-slate-800 text-cyan-400 border border-slate-700 text-[10px] font-mono">⏱️ 60s Drill</button>
              </div>
              <div class="p-3 bg-slate-900/90 rounded-lg border border-slate-800 text-xs text-slate-200 italic">
                "{trap.get('scenario')}"
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                <div class="p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 space-y-1">
                  <strong class="text-rose-400 block font-bold">❌ Junior / L5 Fallacy:</strong>
                  <p class="text-slate-400 leading-relaxed">{trap.get('junior_fallacy')}</p>
                </div>
                <div class="p-3 rounded-lg bg-blue-950/20 border border-blue-900/40 space-y-1">
                  <strong class="text-blue-400 block font-bold">🔍 Kernel Root Cause:</strong>
                  <p class="text-slate-300 leading-relaxed">{trap.get('root_cause')}</p>
                </div>
              </div>
              <div class="p-3.5 rounded-lg bg-emerald-950/25 border border-emerald-900/50 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-emerald-400 font-bold text-xs">✅ Google Staff L6/L8 Architectural Defense:</span>
                  <span class="text-[9px] text-emerald-500 font-mono uppercase">Verbatim Defense Script</span>
                </div>
                <p class="text-slate-200 text-xs font-sans"><strong>Mitigation:</strong> {trap.get('l8_mitigation')}</p>
                <div class="p-2.5 rounded bg-slate-950 border border-emerald-900/40 text-emerald-300 font-mono text-[11px] leading-relaxed">
                  "{trap.get('defense_script')}"
                </div>
              </div>
            </div>
            '''

        is_first = (ch_num == 1)
        active_cls = " active-stage" if is_first else ""
        disp_style = "" if is_first else ' style="display: none;"'

        html.append(f'''
      <!-- STAGE {ch_num} CONTAINER -->
      <section id="stage-{ch_num}" class="stage-section{active_cls} flex-1 flex flex-col overflow-hidden h-full"{disp_style}>
        
        <!-- Stage Top Bar (Shrink-0) -->
        <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40 font-mono">
                Stage {ch_num} • {m["track"].split(":")[1] if ":" in m["track"] else m["track"]}
              </span>
              <h2 class="text-base font-bold text-white">{m["title"]}</h2>
            </div>
          </div>
          
          <!-- Interactive Module Mastery Hub Widget -->
          <div class="flex items-center gap-2">
            <button onclick="openMasteryHubModal('{ch_id}')" id="{ch_id}-mastery-pill" class="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-mono text-slate-300 transition-all shadow">
              <span id="{ch_id}-mastery-status-icon">⚪</span>
              <span id="{ch_id}-mastery-status-text">Status: Learning</span>
            </button>
          </div>
        </div>

        <!-- Numbers to Quote: Interactive Executive Dashboard Ribbon (Responsive 4-Grid, No Scrollbar Needed) -->
        <div class="shrink-0 px-6 py-2 bg-[#030612] border-b border-white/[0.05]">
          <div class="flex flex-wrap items-center gap-2.5">
            <div class="flex items-center gap-1.5 shrink-0 pr-2 border-r border-slate-800">
              <span class="text-xs">📊</span>
              <span class="text-[10px] font-bold text-cyan-400 uppercase font-mono tracking-wider">Numbers to Quote</span>
            </div>
            <div class="flex-1 grid grid-cols-2 md:grid-cols-4 gap-2">
              {metric_cards}
            </div>
          </div>
        </div>

        <!-- Micro-Tabs Navigation Control Hub (All 12 Modules 100% Accessible Without Scrolling) -->
        <div class="shrink-0 px-6 py-2 bg-[#040818] border-b border-white/[0.08] flex flex-col gap-1.5" id="{ch_id}-tabs-hub">
          <!-- Tier 1: Core Architecture & Implementation (7 Tabs) + Quick Stepper -->
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="flex flex-wrap items-center gap-1.5" id="{ch_id}-tabs-t1">
              <span class="text-[9px] font-bold text-cyan-400 uppercase font-mono tracking-wider px-2 py-0.5 rounded bg-cyan-950/70 border border-cyan-800/50 shrink-0">
                Arch Hub
              </span>
              <button onclick="switchTab('{ch_id}', 'blueprint')" id="{ch_id}-tab-blueprint" class="micro-tab active px-2.5 py-1 text-xs">📐 Blueprint</button>
              <button onclick="switchTab('{ch_id}', 'tldr')" id="{ch_id}-tab-tldr" class="micro-tab px-2.5 py-1 text-xs">⚡ Executive TL;DR</button>
              <button onclick="switchTab('{ch_id}', 'diff')" id="{ch_id}-tab-diff" class="micro-tab px-2.5 py-1 text-xs">💻 Junior vs Staff</button>
              <button onclick="switchTab('{ch_id}', 'capacity')" id="{ch_id}-tab-capacity" class="micro-tab px-2.5 py-1 text-xs">🧮 Capacity Math</button>
              <button onclick="switchTab('{ch_id}', 'theory')" id="{ch_id}-tab-theory" class="micro-tab px-2.5 py-1 text-xs">📚 Deep Theory</button>
              <button onclick="switchTab('{ch_id}', 'project')" id="{ch_id}-tab-project" class="micro-tab px-2.5 py-1 text-xs">🏭 Project Arch</button>
              <button onclick="switchTab('{ch_id}', 'code')" id="{ch_id}-tab-code" class="micro-tab px-2.5 py-1 text-xs">⌨️ Production Code</button>
            </div>

            <!-- Quick Section Steppers -->
            <div class="flex items-center gap-1.5 shrink-0">
              <button onclick="stepTab('{ch_id}', -1)" title="Previous Section" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-500/50 text-slate-300 hover:text-white text-xs font-mono transition-all flex items-center gap-1 shadow">
                <span>‹</span> <span>Prev</span>
              </button>
              <span id="{ch_id}-tab-indicator" class="text-[10px] font-mono font-bold text-cyan-400 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">1 / 12</span>
              <button onclick="stepTab('{ch_id}', 1)" title="Next Section" class="px-2.5 py-1 rounded-lg bg-cyan-950 hover:bg-cyan-900 border border-cyan-800 hover:border-cyan-500 text-cyan-300 hover:text-white text-xs font-mono transition-all flex items-center gap-1 shadow">
                <span>Next</span> <span>›</span>
              </button>
            </div>
          </div>

          <!-- Tier 2: Staff Interview & Mastery Drills (5 Tabs) -->
          <div class="flex flex-wrap items-center gap-1.5 pt-1 border-t border-white/[0.04]" id="{ch_id}-tabs-t2">
            <span class="text-[9px] font-bold text-amber-400 uppercase font-mono tracking-wider px-2 py-0.5 rounded bg-amber-950/70 border border-amber-800/50 shrink-0">
              Staff Drills
            </span>
            <button onclick="switchTab('{ch_id}', 'traps')" id="{ch_id}-tab-traps" class="micro-tab px-2.5 py-1 text-xs">⚔️ L8 Ambush Traps</button>
            <button onclick="switchTab('{ch_id}', 'recall')" id="{ch_id}-tab-recall" class="micro-tab px-2.5 py-1 text-xs">🎴 Active Recall Test</button>
            <button onclick="switchTab('{ch_id}', 'videos')" id="{ch_id}-tab-videos" class="micro-tab px-2.5 py-1 text-xs">🎥 Masterclasses</button>
            <button onclick="switchTab('{ch_id}', 'pitch')" id="{ch_id}-tab-pitch" class="micro-tab px-2.5 py-1 text-xs">🎙️ 2-Min Pitch</button>
            <button onclick="switchTab('{ch_id}', 'notes')" id="{ch_id}-tab-notes" class="micro-tab px-2.5 py-1 text-xs">📝 Notes Journal</button>
          </div>
        </div>

        <!-- Tab Content Viewport -->
        <div class="flex-1 overflow-y-auto main-stage-scroll px-6 py-5 space-y-6">
          
          <!-- TAB 1: SYSTEM DESIGN BLUEPRINT -->
          <div id="{ch_id}-content-blueprint" class="tab-content space-y-4 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-cyan-950/20 border border-cyan-900/40 rounded-xl flex flex-wrap items-center justify-between gap-3">
              <div>
                <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block font-mono">Google L6/L8 Architecture Blueprint</span>
                <h3 class="text-sm font-bold text-white mt-0.5">{sys_design.get("title", m["title"])}</h3>
              </div>
              <div class="flex gap-2">
                <button onclick="openSplitStudioWithTopology('{ch_id}')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow transition-all">
                  <span>◫</span> Sketch in Split Studio
                </button>
              </div>
            </div>

            <!-- Option A: Canonical Reference Topology Pre-Sketched -->
            {m.get("reference_topology", "")}

            <!-- 7-Section Blueprint Body -->
            {sys_design.get("requirements", "")}

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <div></div>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: ⚡ Executive TL;DR <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 2: EXECUTIVE TL;DR CHEATSHEET -->
          <div id="{ch_id}-content-tldr" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
              <div class="p-3.5 bg-gradient-to-r from-cyan-950/40 to-slate-900 rounded-lg border border-cyan-900/40 space-y-1">
                <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block font-mono">The 30-Second Executive Pitch (Google Staff / Principal)</span>
                <p class="text-xs text-white leading-relaxed italic">
                  "{tldr.get("elevator_pitch", tldr.get("principle", ""))}"
                </p>
              </div>

              <div class="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
                <span class="text-xs font-bold text-white uppercase tracking-wider block font-mono">Architectural Invariants & Laws of Physics</span>
                <ul class="space-y-1.5">
                  {"".join(f'<li class="flex items-start gap-2 text-xs text-slate-300"><span class="text-cyan-400 font-bold shrink-0">❖</span><span>{inv}</span></li>' for inv in tldr.get("invariants", []))}
                </ul>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-3.5 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-2">
                  <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block font-mono">Top L6 Red Flags & Rejection Traps</span>
                  <ul class="space-y-2">
                    {"".join(f'<li class="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1"><div class="text-rose-400 font-bold flex items-start gap-1.5"><span class="text-rose-500 font-bold">✕ Junior:</span> <span>{rf.get("junior", "") if isinstance(rf, dict) else rf}</span></div><div class="text-emerald-300 flex items-start gap-1.5"><span class="text-emerald-400 font-bold">✔ Staff:</span> <span>{rf.get("staff", "") if isinstance(rf, dict) else ""}</span></div></li>' for rf in tldr.get("red_flags", []))}
                  </ul>
                </div>
                
                <div class="space-y-3">
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block font-mono">Production Gotcha to Highlight</span>
                    <p class="text-slate-300 leading-relaxed text-[11px]">{tldr.get("gotchas", "")}</p>
                  </div>
                  
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider block font-mono">Real-World Production Battle Scars</span>
                    <div class="space-y-2">
                      {"".join(f'<div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800 text-[11px] text-slate-300 space-y-0.5"><span class="text-amber-400 font-bold block">⚡ Battle Scar:</span><p>{bs}</p></div>' for bs in tldr.get("battle_scars", []))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 📐 Blueprint
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 💻 Junior vs Staff Diff <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 3: JUNIOR VS STAFF DIFF -->
          <div id="{ch_id}-content-diff" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
              <h4 class="text-sm font-bold text-white">{diff.get("title", "Junior vs Staff Architecture")}</h4>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div class="p-3.5 rounded-xl bg-[#140608] border border-rose-900/60 space-y-2">
                  <span class="text-xs font-bold text-rose-400 block border-b border-rose-900/40 pb-1.5 font-mono">❌ Naive Junior / Mid Implementation</span>
                  <div class="code-block text-[11px] font-mono"><pre><code>{diff.get("junior", "")}</code></pre></div>
                </div>
                <div class="p-3.5 rounded-xl bg-[#03150d] border border-emerald-900/60 space-y-2">
                  <span class="text-xs font-bold text-emerald-400 block border-b border-emerald-900/40 pb-1.5 font-mono">✅ Google Staff L6 Hardened Architecture</span>
                  <div class="code-block text-[11px] font-mono"><pre><code>{diff.get("staff", "")}</code></pre></div>
                </div>
              </div>
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: ⚡ Executive TL;DR
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 🧮 Capacity Math <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 4: CAPACITY MATH -->
          <div id="{ch_id}-content-capacity" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800 space-y-4">
              <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h4 class="text-sm font-bold text-white">Live Back-of-the-Envelope Capacity Estimator</h4>
                  <p class="text-[11px] text-slate-400">Reactive sizing for {m['title']}. Adjust sliders to compute hardware bounds.</p>
                </div>
                <span class="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-800/40">Real-Time Compute</span>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Target QPS:</span><span id="{ch_id}-val-qps" class="font-bold text-cyan-400 font-mono">45,000 req/s</span></div>
                  <input type="range" min="1000" max="100000" step="1000" value="45000" id="{ch_id}-calc-qps" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-cyan-500 h-1.5">
                </div>
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Message Size:</span><span id="{ch_id}-val-size" class="font-bold text-purple-400 font-mono">1.0 KB</span></div>
                  <input type="range" min="256" max="8192" step="256" value="1024" id="{ch_id}-calc-size" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-purple-500 h-1.5">
                </div>
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Replication:</span><span id="{ch_id}-val-rep" class="font-bold text-emerald-400 font-mono">3x</span></div>
                  <input type="range" min="1" max="5" step="1" value="3" id="{ch_id}-calc-rep" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-emerald-500 h-1.5">
                </div>
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]"><span class="text-slate-400">Retention:</span><span id="{ch_id}-val-ret" class="font-bold text-amber-400 font-mono">7 days</span></div>
                  <input type="range" min="1" max="30" step="1" value="7" id="{ch_id}-calc-ret" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-amber-500 h-1.5">
                </div>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2 font-mono text-xs">
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800"><div class="text-[10px] text-slate-400">Network Ingress:</div><div id="{ch_id}-res-bw" class="font-bold text-cyan-400 mt-1">43.9 MB/s (0.35 Gbps)</div></div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800"><div class="text-[10px] text-slate-400">Daily Ingress:</div><div id="{ch_id}-res-daily" class="font-bold text-purple-400 mt-1">11,390 GB / day</div></div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800"><div class="text-[10px] text-slate-400">Cluster Storage:</div><div id="{ch_id}-res-storage" class="font-bold text-emerald-400 mt-1">95.7 TB (with headroom)</div></div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800"><div class="text-[10px] text-slate-400">Partitions Required:</div><div id="{ch_id}-res-part" class="font-bold text-amber-400 mt-1">128 Partitions</div></div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800"><div class="text-[10px] text-slate-400">PageCache RAM:</div><div id="{ch_id}-res-ram" class="font-bold text-rose-400 mt-1">13 GB RAM</div></div>
              </div>
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 💻 Junior vs Staff Diff
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 📚 Deep Theory <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 5: DEEP THEORY -->
          <div id="{ch_id}-content-theory" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            {tech.get("theory", "")}

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 🧮 Capacity Math
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 🏭 Project Implementation <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 6: PROJECT IMPLEMENTATION -->
          <div id="{ch_id}-content-project" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            {tech.get("project", "")}

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 📚 Deep Theory
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: ⌨️ Production Code <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 7: PRODUCTION CODE -->
          <div id="{ch_id}-content-code" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono">Production Code & Schema Implementation</span>
              <button onclick="copyCode('code-{ch_id}')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded border border-slate-700 transition-all flex items-center gap-1 font-mono">
                <span>📋</span> Copy Code
              </button>
            </div>
            <div class="code-block" id="code-{ch_id}">
              {tech.get("code", "")}
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 🏭 Project Implementation
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: ⚔️ L8 Ambush Traps Drill <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 8: L8 BAR-RAISER TRAPS -->
          <div id="{ch_id}-content-traps" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="space-y-4">
              {traps_cards}
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: ⌨️ Production Code
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 🎴 Active Recall Test <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 9: ACTIVE RECALL FLASHCARD TEST -->
          <div id="{ch_id}-content-recall" class="tab-content hidden space-y-4 text-xs">
            <div class="max-w-2xl mx-auto flashcard-container min-h-[220px]">
              <div id="{ch_id}-card" onclick="flipModuleCard('{ch_id}')" class="flashcard relative w-full min-h-[220px] rounded-2xl bg-gradient-to-br from-slate-900 to-[#050b18] border border-slate-800 p-6 shadow-2xl flex flex-col justify-between hover:border-cyan-500/40">
                <div class="flashcard-front space-y-3">
                  <div class="flex justify-between items-center text-xs text-cyan-400 font-semibold uppercase tracking-wider font-mono">
                    <span>{m["domain"]} • L6 Recall Question</span>
                    <span>Click to Flip 🔄</span>
                  </div>
                  <h4 class="text-base font-bold text-white leading-snug">
                    What is the core bottleneck and physics invariant of {m['title']}?
                  </h4>
                  <p class="text-[11px] text-slate-400">Formulate your verbal architectural explanation before flipping.</p>
                </div>
                <div class="flashcard-back absolute inset-0 p-6 rounded-2xl bg-[#080e22] border border-cyan-500/40 flex flex-col justify-between space-y-3">
                  <div>
                    <div class="flex justify-between items-center text-xs text-emerald-400 font-semibold uppercase tracking-wider mb-1.5 font-mono">
                      <span>Google L6 Bar-Raiser Defense</span>
                      <span>Click to Flip 🔄</span>
                    </div>
                    <div class="text-xs text-slate-300 leading-relaxed space-y-1">
                      {tldr.get("principle", "Verify zero-copy PageCache buffers, avoid heap allocation, and enforce monotonic version fencing.")}
                    </div>
                  </div>
                  <div class="pt-2 border-t border-slate-800 flex justify-end">
                    <span class="text-[10px] text-slate-400 font-mono">Click card or press Spacebar to flip</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-2 pt-2">
              <button onclick="rateModuleCard('{ch_id}', 'Again')" class="px-3 py-1.5 rounded-lg bg-rose-950/60 hover:bg-rose-900 text-rose-300 border border-rose-800 text-xs font-semibold">1: Again (&lt;1d)</button>
              <button onclick="rateModuleCard('{ch_id}', 'Hard')" class="px-3 py-1.5 rounded-lg bg-amber-950/60 hover:bg-amber-900 text-amber-300 border border-amber-800 text-xs font-semibold">2: Hard (2d)</button>
              <button onclick="rateModuleCard('{ch_id}', 'Good')" class="px-3 py-1.5 rounded-lg bg-emerald-950/60 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 text-xs font-semibold">3: Good (4d)</button>
              <button onclick="rateModuleCard('{ch_id}', 'Mastered')" class="px-3 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-700 text-xs font-bold">4: Mastered (+50 XP)</button>
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: ⚔️ L8 Ambush Traps
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 🎥 Masterclasses <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 10: VIDEO MASTERCLASSES -->
          <div id="{ch_id}-content-videos" class="tab-content hidden space-y-4 text-xs">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              {videos_cards}
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 🎴 Active Recall Test
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 🎙️ 2-Min Pitch Studio <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 11: 2-MIN WHITEBOARD PITCH -->
          <div id="{ch_id}-content-pitch" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800 space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-bold text-white">2-Minute Executive Pitch Rehearsal Studio</h4>
                  <p class="text-[11px] text-slate-400">Rehearse articulating the architecture under 120 seconds with microphone recording.</p>
                </div>
                <div class="flex items-center gap-2">
                  <span id="{ch_id}-pitch-timer" class="font-mono text-cyan-400 font-bold text-sm bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-800/40">00:00 / 02:00</span>
                  <button onclick="togglePitchRecording('{ch_id}')" id="{ch_id}-btn-pitch" class="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow transition-all">
                    <span>🎙️</span> <span>Record Pitch</span>
                  </button>
                </div>
              </div>
              <div class="p-4 bg-slate-900/90 rounded-xl border border-slate-800 space-y-2">
                <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider font-mono">Suggested Verbal Pitch Script:</span>
                <p class="text-xs text-slate-200 leading-relaxed italic">{tech.get("pitch", "")}</p>
              </div>
            </div>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 🎥 Masterclasses
              </button>
              <button onclick="stepTab('{ch_id}', 1)" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950 transition-all">
                Next: 📝 Engineering Notes Journal <span>→</span>
              </button>
            </div>
          </div>

          <!-- TAB 12: ENGINEERING STUDY JOURNAL -->
          <div id="{ch_id}-content-notes" class="tab-content hidden space-y-3">
            <div class="flex justify-between items-center text-xs text-slate-400">
              <span>Personal Engineering Journal & Trade-Off Takeaways:</span>
              <div class="flex items-center gap-2 font-mono text-[10px]">
                <button onclick="insertNoteTemplate('{ch_id}', 'tradeoff')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700">+ Trade-Off Template</button>
                <button onclick="insertNoteTemplate('{ch_id}', 'gotcha')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700">+ Gotcha Template</button>
                <span class="text-emerald-400">Auto-Saved in localStorage</span>
              </div>
            </div>
            <textarea id="{ch_id}-notes-area" rows="10" placeholder="Record your personal architectural trade-offs, numbers to memorize, and failure mode defenses for Stage {ch_num}..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono leading-relaxed"></textarea>

            <!-- Section Bottom Nav -->
            <div class="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <button onclick="stepTab('{ch_id}', -1)" class="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all">
                <span>←</span> Previous: 🎙️ 2-Min Pitch
              </button>
              <button onclick="goToStage({ch_num + 1 if ch_num < 17 else 1})" class="px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-emerald-950 transition-all">
                Advance to Stage {ch_num + 1 if ch_num < 17 else 1} <span>→</span>
              </button>
            </div>
          </div>

        </div>
      </section>
        ''')

    # Add Stages 13 to 17
    html.append(interactive_stages_data.STAGE_13_SIMULATORS)
    html.append(interactive_stages_data.STAGE_14_LEADERSHIP)
    html.append(interactive_stages_data.STAGE_15_TRADEOFFS)
    html.append(interactive_stages_data.STAGE_16_PAPERS)
    html.append(interactive_stages_data.STAGE_17_EXAM)

    # Close main viewport & main
    html.append('''
    </div>

    <!-- RIGHT SPLIT STUDIO DOCK PANEL (Draw Beside Study Material!) -->
    <div id="split-studio-panel" class="hidden w-[580px] shrink-0 border-l border-white/[0.08] bg-[#040818] flex flex-col overflow-hidden select-none">
      
      <!-- Split Studio Header -->
      <div class="px-4 py-2.5 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm">◫</span>
          <span class="text-xs font-bold text-white font-mono uppercase tracking-wider">SPLIT WHITEBOARD STUDIO</span>
        </div>
        <div class="flex items-center gap-1.5">
          <button onclick="loadActiveModuleTopologyToSplit()" class="px-2 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px] font-semibold" title="Load active module reference topology">📐 Load Active Topology</button>
          <button onclick="verifyArchitectureScore()" class="px-2 py-1 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 text-[10px] font-semibold" title="Test architecture against Google L6 rubrics">🤖 Verify Design</button>
          <button onclick="clearWhiteboard()" class="px-2 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-[10px]" title="Clear All">Clear</button>
          <button onclick="toggleSplitStudio()" class="w-6 h-6 rounded bg-slate-800 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center text-xs font-bold">&times;</button>
        </div>
      </div>

      <!-- Split Studio Toolbar -->
      <div class="px-3 py-2 bg-slate-950/80 border-b border-slate-800 text-xs flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-1">
          <button onclick="setWbTool('pen')" id="split-tool-pen" class="wb-tool active px-2 py-0.5 rounded bg-slate-800 text-white border border-slate-700 text-[11px]">✏️ Pen</button>
          <button onclick="setWbTool('arrow')" id="split-tool-arrow" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">➡️ Arrow</button>
          <button onclick="setWbTool('rect')" id="split-tool-rect" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">▭ Box</button>
          <button onclick="setWbTool('eraser')" id="split-tool-eraser" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">🧹 Eraser</button>
        </div>
        <div class="flex items-center gap-1">
          <button onclick="addStencil('gateway')" class="px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 text-[10px]">+ Gateway</button>
          <button onclick="addStencil('kafka')" class="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]">+ Kafka</button>
          <button onclick="addStencil('scylla')" class="px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[10px]">+ Scylla</button>
          <button onclick="addStencil('redis')" class="px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 text-[10px]">+ Redis</button>
        </div>
      </div>

      <!-- Split Viewport -->
      <div id="split-viewport" class="relative flex-1 bg-[#030611] overflow-hidden">
        <canvas id="split-canvas" class="w-full h-full cursor-crosshair block absolute inset-0 z-0"></canvas>
        <div id="split-nodes" class="absolute inset-0 pointer-events-none z-10 overflow-hidden"></div>
      </div>
    </div>

  </main>
''')

    # Add Modals
    html.append(interactive_stages_data.WHITEBOARD_MODAL_HTML)
    
    # Add Video Modal
    html.append('''
  <!-- VIDEO MASTERCLASS MODAL (EMBEDDED YOUTUBE PLAYER) -->
  <div id="video-modal" class="fixed inset-0 z-50 bg-[#02050f]/90 backdrop-blur-xl flex items-center justify-center p-3 sm:p-6 hidden select-none">
    <div class="relative w-full max-w-4xl bg-slate-950 border border-cyan-500/40 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
      <div class="h-12 bg-slate-900 border-b border-slate-800 px-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-cyan-400 font-bold">▶</span>
          <span id="video-modal-title" class="text-xs font-bold text-white font-mono truncate max-w-lg">Lecture Masterclass</span>
        </div>
        <button onclick="closeVideoModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold">&times;</button>
      </div>
      <div class="relative w-full aspect-video bg-black">
        <iframe id="video-modal-iframe" class="w-full h-full" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
      </div>
    </div>
  </div>

  
  <!-- GAMIFICATION / ACHIEVEMENTS MODAL -->
  <div id="gamification-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-xl bg-slate-950 border border-emerald-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">🏆</span>
          <div>
            <h3 class="text-base font-bold text-white">Engineering Level & Progression</h3>
            <span class="text-[10px] text-emerald-400 font-mono">Google Engineering Career Ladder</span>
          </div>
        </div>
        <button onclick="closeGamificationModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>

      <div class="p-4 bg-slate-900/90 rounded-xl border border-slate-800 space-y-2">
        <div class="flex justify-between text-xs font-mono">
          <span class="text-slate-400">Current Rank: <strong id="modal-level-title" class="text-emerald-400">L3 Systems Explorer (Level 1)</strong></span>
          <span class="text-cyan-400 font-bold"><span id="modal-xp-val">0</span> / 500 XP to L4</span>
        </div>
        <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
          <div id="modal-xp-bar" class="bg-gradient-to-r from-emerald-500 to-cyan-500 h-full w-[60%] transition-all"></div>
        </div>
        <p class="text-[11px] text-slate-400 pt-1">Earn XP by testing active recall flashcards (+50 XP), defending L8 traps (+100 XP), verifying whiteboard topologies (+50 XP), and running simulation labs (+25 XP).</p>
      </div>

      <div class="space-y-2">
        <span class="text-xs font-bold text-white uppercase font-mono">Unlocked Engineering Badges:</span>
        <div class="grid grid-cols-2 gap-2 text-xs font-mono">
          <div class="p-2.5 rounded-lg bg-slate-900 border border-emerald-900/40 text-emerald-300">⚡ Zero-Copy Kernel Master</div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-purple-900/40 text-purple-300">🔒 Fencing Token Sentry</div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-blue-900/40 text-blue-300">🗳️ Raft Quorum Commander</div>
          <div class="p-2.5 rounded-lg bg-slate-900 border border-amber-900/40 text-amber-300">⚔️ L8 Ambush Survivor</div>
        </div>
      </div>

      <div class="p-3 bg-emerald-950/20 border border-emerald-900/40 rounded-xl flex items-center justify-between text-xs">
        <span class="text-emerald-300 font-medium">Daily Engineering Practice Bonus:</span>
        <button onclick="claimDailyBonus()" id="btn-claim-bonus" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold shadow transition-all">
          Claim Bonus (+50 XP)
        </button>
      </div>
    </div>
  </div>


  <!-- DAILY STREAK HEATMAP MODAL -->
  <div id="streak-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-md bg-slate-950 border border-amber-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">🔥</span>
          <div>
            <h3 class="text-base font-bold text-white">Daily Study Consistency Streak</h3>
            <span class="text-[10px] text-amber-400 font-mono">14-Day Architectural Mastery Tracker</span>
          </div>
        </div>
        <button onclick="closeStreakModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>

      <div class="text-center p-4 bg-slate-900/90 rounded-xl border border-slate-800 space-y-1">
        <div id="modal-streak-count" class="text-4xl font-black text-amber-400 font-mono">0 DAYS</div>
        <p class="text-xs text-slate-300">You are in the top 3% of consistent Staff candidates!</p>
        <span class="text-[10px] text-emerald-400 font-mono block">Best Record: 14 Consecutive Days</span>
      </div>

      <div>
        <div class="flex justify-between items-center mb-2">
          <span class="text-[10px] font-bold text-slate-400 uppercase font-mono">14-Day Activity Heatmap:</span>
          <span class="text-[9px] text-slate-500 font-mono">Green = Completed | Cyan = Active</span>
        </div>
        <div class="grid grid-cols-7 gap-1.5 text-center text-[10px] font-mono" id="streak-heatmap-grid">
          <div class="p-2 rounded bg-emerald-500/80 text-white font-bold" title="Day 1: Completed">D1</div>
          <div class="p-2 rounded bg-emerald-500/80 text-white font-bold" title="Day 2: Completed">D2</div>
          <div class="p-2 rounded bg-emerald-500/80 text-white font-bold" title="Day 3: Completed">D3</div>
          <div class="p-2 rounded bg-emerald-500/80 text-white font-bold" title="Day 4: Completed">D4</div>
          <div class="p-2 rounded bg-emerald-500/80 text-white font-bold" title="Day 5: Completed">D5</div>
          <div id="streak-cell-today" class="p-2 rounded bg-cyan-600 text-white font-bold animate-pulse" title="Day 6: In Progress">D6</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 7: Upcoming">D7</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 8: Upcoming">D8</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 9: Upcoming">D9</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 10: Upcoming">D10</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 11: Upcoming">D11</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 12: Upcoming">D12</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 13: Upcoming">D13</div>
          <div class="p-2 rounded bg-slate-800 text-slate-500 font-bold" title="Day 14: Upcoming">D14</div>
        </div>
      </div>

      <div class="p-3 bg-amber-950/20 border border-amber-900/40 rounded-xl flex items-center justify-between text-xs">
        <span class="text-amber-300 font-medium">Ready for today's review?</span>
        <button onclick="logDailyCheckIn()" id="btn-checkin" class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold shadow transition-all">
          Log Today (+50 XP)
        </button>
      </div>
    </div>
  </div>


  <!-- FOCUS COCKPIT & AMBIENT SOUNDSCAPES MODAL -->
  <div id="focus-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-lg bg-slate-950 border border-cyan-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">⏱️</span>
          <div>
            <h3 class="text-base font-bold text-white">Deep Work & Focus Cockpit</h3>
            <span class="text-[10px] text-cyan-400 font-mono">Offline Web Audio Generator & Flow State Controls</span>
          </div>
        </div>
        <button onclick="closeFocusCockpitModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>

      <div class="space-y-1.5">
        <span class="text-[11px] font-bold text-slate-400 uppercase font-mono">Pomodoro Duration Presets:</span>
        <div class="grid grid-cols-3 gap-2 text-xs font-mono">
          <button onclick="setPomodoroTime(25)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500 text-center">🍅 25m Focus</button>
          <button onclick="setPomodoroTime(50)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500 text-center">⚡ 50m Deep</button>
          <button onclick="setPomodoroTime(90)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500 text-center">🚀 90m Sprint</button>
        </div>
      </div>

      <div class="p-4 bg-slate-900/90 rounded-xl border border-slate-800 space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-xs font-bold text-white block">Offline Ambient Sound Generator (Web Audio API):</span>
          <button onclick="stopAmbientNoise()" class="text-[10px] text-rose-400 hover:underline font-mono">⏹ Stop Sound</button>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs font-mono">
          <button onclick="toggleAmbientNoise('server')" id="btn-sound-server" class="p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-cyan-500 text-slate-300 text-left">🖥️ Datacenter Drone</button>
          <button onclick="toggleAmbientNoise('binaural')" id="btn-sound-binaural" class="p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-cyan-500 text-slate-300 text-left">🧠 Alpha 10Hz Beats</button>
          <button onclick="toggleAmbientNoise('brown')" id="btn-sound-brown" class="p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-cyan-500 text-slate-300 text-left">🎧 Brown Noise</button>
          <button onclick="toggleAmbientNoise('white')" id="btn-sound-white" class="p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-cyan-500 text-slate-300 text-left">🌊 White Noise</button>
        </div>
        <div class="pt-1 flex items-center justify-between text-xs">
          <span class="text-slate-400 font-mono text-[11px]">Volume:</span>
          <input type="range" min="0" max="100" value="30" oninput="setAudioVolume(this.value)" class="w-48 accent-cyan-400">
        </div>
      </div>

      <div class="p-3 bg-cyan-950/20 border border-cyan-900/40 rounded-xl flex items-center justify-between text-xs">
        <div>
          <span class="text-cyan-300 font-bold block">Zen Immersion Mode</span>
          <span class="text-slate-400 text-[10px]">Hides sidebars and headers for total focus</span>
        </div>
        <button onclick="toggleZenMode()" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold shadow transition-all">
          Toggle Zen Mode
        </button>
      </div>
    </div>
  </div>


  <!-- ARCHITECTURE VERIFICATION ASSISTANT MODAL (Google L6 Rubric) -->
  <div id="arch-verify-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-xl bg-slate-950 border border-indigo-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">🤖</span>
          <div>
            <h3 class="text-base font-bold text-white">Google Staff L6 Architecture Verification Report</h3>
            <span class="text-[10px] text-indigo-400 font-mono">Automated Topology Rubric Evaluator</span>
          </div>
        </div>
        <button onclick="closeArchVerifyModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>

      <div class="p-4 bg-indigo-950/30 rounded-xl border border-indigo-900/50 flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 block font-mono">Overall Architecture Score:</span>
          <span class="text-3xl font-black text-indigo-300 font-mono">96 / 100</span>
        </div>
        <span class="px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700 text-xs font-bold font-mono">
          ✔ Google L6 Certified
        </span>
      </div>

      <div class="space-y-2.5 text-xs font-mono">
        <div class="space-y-1">
          <div class="flex justify-between text-slate-300">
            <span>1. Ingress Decoupling & Queue Buffering</span>
            <span class="text-emerald-400 font-bold">100% (Passed)</span>
          </div>
          <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div class="bg-emerald-500 h-full w-[100%]"></div></div>
        </div>
        <div class="space-y-1">
          <div class="flex justify-between text-slate-300">
            <span>2. Persistence Engine & Zero-Copy I/O</span>
            <span class="text-emerald-400 font-bold">98% (Passed)</span>
          </div>
          <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div class="bg-emerald-500 h-full w-[98%]"></div></div>
        </div>
        <div class="space-y-1">
          <div class="flex justify-between text-slate-300">
            <span>3. High-Availability & Quorum Replication</span>
            <span class="text-emerald-400 font-bold">94% (Passed)</span>
          </div>
          <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div class="bg-emerald-500 h-full w-[94%]"></div></div>
        </div>
        <div class="space-y-1">
          <div class="flex justify-between text-slate-300">
            <span>4. Fencing Token & Poison Pill Defense</span>
            <span class="text-indigo-400 font-bold">92% (Passed)</span>
          </div>
          <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div class="bg-indigo-500 h-full w-[92%]"></div></div>
        </div>
      </div>

      <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 text-xs space-y-1">
        <span class="text-indigo-400 font-bold font-mono block">Google Principal Bar-Raiser Feedback:</span>
        <p class="text-slate-300 leading-relaxed text-[11px]">
          "Exceptional component isolation. Decoupling ingress via partition streams completely insulates wire traffic from database compaction stalls. Staff recommendation: Ensure the edge rate-limiting gateway incorporates a fail-open circuit breaker to prevent cascading edge drops during telemetry surges."
        </p>
      </div>

      <div class="flex justify-between items-center pt-2">
        <span class="text-[10px] text-emerald-400 font-mono">+50 XP Awarded for Architecture Verification</span>
        <button onclick="closeArchVerifyModal()" class="px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow">
          Accept & Continue
        </button>
      </div>
    </div>
  </div>

<!-- NUMBER DERIVATION MODAL -->
  <div id="number-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-lg bg-slate-950 border border-cyan-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-cyan-400 font-bold font-mono">🧮</span>
          <h3 id="num-modal-title" class="text-base font-bold text-white">45,000 TPS Dimensional Analysis</h3>
        </div>
        <button onclick="closeNumberDerivationModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-cyan-400 uppercase font-mono block">Exact Derivation Formula:</span>
        <p id="num-modal-derivation" class="text-xs text-slate-200 font-mono leading-relaxed"></p>
      </div>
      <div class="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-1">
        <span class="text-xs font-bold text-emerald-400 uppercase font-mono block">How to Quote With Authority:</span>
        <p id="num-modal-soundbite" class="text-xs text-slate-200 italic leading-relaxed"></p>
      </div>
      <div class="p-4 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-1">
        <span class="text-xs font-bold text-rose-400 uppercase font-mono block">The Bar-Raiser Follow-Up Question:</span>
        <p id="num-modal-question" class="text-xs text-slate-300 leading-relaxed"></p>
      </div>
    </div>
  </div>

  <!-- MODULE MASTERY HUB MODAL -->
  <div id="mastery-modal" class="fixed inset-0 z-50 bg-[#02050f]/85 backdrop-blur-xl flex items-center justify-center p-4 hidden select-none">
    <div class="relative w-full max-w-lg bg-slate-950 border border-cyan-500/40 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">🛡️</span>
          <h3 class="text-base font-bold text-white">Module Mastery Assessment</h3>
        </div>
        <button onclick="closeMasteryHubModal()" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center font-bold">&times;</button>
      </div>
      <div class="space-y-3 text-xs">
        <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
          <span class="text-white font-bold block">3-Phase Mastery Checklist:</span>
          <label class="flex items-center gap-2 cursor-pointer text-slate-300"><input type="checkbox" id="mchk-1" class="text-cyan-500 rounded bg-slate-950 border-slate-700"> <span>1. Reviewed Deep Theory & Executive Pitch</span></label>
          <label class="flex items-center gap-2 cursor-pointer text-slate-300"><input type="checkbox" id="mchk-2" class="text-cyan-500 rounded bg-slate-950 border-slate-700"> <span>2. Sketched Canonical Topology on Whiteboard</span></label>
          <label class="flex items-center gap-2 cursor-pointer text-slate-300"><input type="checkbox" id="mchk-3" class="text-cyan-500 rounded bg-slate-950 border-slate-700"> <span>3. Passed 60s Pressure L8 Ambush Drills</span></label>
        </div>
        <div class="flex justify-between items-center pt-2">
          <button onclick="setMasteryStatus('learning')" class="px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 border border-slate-800 hover:text-white">In Progress</button>
          <button onclick="setMasteryStatus('review')" class="px-3 py-1.5 rounded-lg bg-amber-950 text-amber-300 border border-amber-800">Needs Review</button>
          <button onclick="setMasteryStatus('mastered')" class="px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold shadow-lg shadow-cyan-500/25">Mark Mastered (+100 XP)</button>
        </div>
      </div>
    </div>
  </div>

  <!-- SURPRISE AMBUSH QUESTION MODAL -->
  <div id="trap-modal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 select-none">
    <div class="relative w-full max-w-xl bg-slate-950 border border-rose-600/60 rounded-2xl shadow-2xl p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-rose-500 animate-ping"></span>
          <span class="text-xs font-bold text-rose-400 uppercase tracking-widest font-mono">Google Bar-Raiser Ambush Drill</span>
        </div>
        <span id="trap-drill-timer" class="font-mono text-rose-400 font-bold text-xs bg-rose-950 px-2 py-0.5 rounded border border-rose-800">60s</span>
      </div>
      <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 text-xs text-slate-200 italic" id="trap-modal-question"></div>
      <div class="space-y-2 text-xs" id="trap-modal-options"></div>
      <div id="trap-modal-feedback" class="hidden p-3 rounded-lg text-xs font-mono"></div>
      <div class="flex justify-end pt-2">
        <button onclick="closeTrapModal()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs">Close Drill</button>
      </div>
    </div>
  </div>

  <!-- NEURAL COMMAND PALETTE MODAL (CTRL+K SPOTLIGHT) -->
  <div id="command-palette-modal" class="fixed inset-0 z-50 bg-[#02050f]/80 backdrop-blur-md flex items-start justify-center pt-16 sm:pt-24 p-3 hidden select-none animate-fadeIn" onclick="if(event.target === this) closeCommandPalette()">
    <div class="relative w-full max-w-2xl bg-[#050b18] border border-cyan-500/50 rounded-2xl shadow-2xl flex flex-col overflow-hidden ring-1 ring-cyan-500/20" onclick="event.stopPropagation()">
      
      <!-- Search Input Bar -->
      <div class="h-14 px-4 bg-slate-900/90 border-b border-slate-800 flex items-center gap-3">
        <span class="text-cyan-400 text-lg">⚡</span>
        <input id="cmd-palette-input" type="text" placeholder="Jump to system design, simulator, tool, or trap (e.g. 'raft', 'ch1', 'fencing', 'whiteboard')..." 
               class="flex-1 bg-transparent text-white font-mono text-sm placeholder-slate-500 focus:outline-none"
               oninput="filterCommandPalette(this.value)"
               onkeydown="handleCommandPaletteKey(event)" />
        <span class="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">ESC to exit</span>
        <button onclick="closeCommandPalette()" class="text-slate-400 hover:text-white text-xl px-1">&times;</button>
      </div>

      <!-- Quick Category Filter Pills -->
      <div class="px-4 py-2 bg-slate-950/90 border-b border-slate-800 flex flex-wrap items-center gap-1.5 text-[11px] font-mono">
        <button onclick="setCommandFilter('all')" id="cmd-filter-all" class="cmd-filter active px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold transition-all">All</button>
        <button onclick="setCommandFilter('systems')" id="cmd-filter-systems" class="cmd-filter px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition-all">🏛️ Systems (12)</button>
        <button onclick="setCommandFilter('simulators')" id="cmd-filter-simulators" class="cmd-filter px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition-all">🔬 Simulators (8)</button>
        <button onclick="setCommandFilter('tools')" id="cmd-filter-tools" class="cmd-filter px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition-all">🛠️ Tools</button>
        <button onclick="setCommandFilter('traps')" id="cmd-filter-traps" class="cmd-filter px-2.5 py-0.5 rounded-full bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition-all">🚨 Traps &amp; Drills</button>
      </div>

      <!-- Results Container (Max Height, Scrollable, Keyboard Navigable) -->
      <div id="cmd-palette-results" class="max-h-[380px] overflow-y-auto p-2 space-y-1 divide-y divide-slate-800/40">
        <!-- Rendered dynamically by JS -->
      </div>

      <!-- Footer with Shortcuts Legend -->
      <div class="h-9 px-4 bg-slate-950/90 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-slate-400">
        <div class="flex items-center gap-3">
          <span><kbd class="px-1 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-400">↑↓</kbd> Navigate</span>
          <span><kbd class="px-1 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-400">↵</kbd> Select</span>
          <span><kbd class="px-1 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-400">ESC</kbd> Dismiss</span>
        </div>
        <span class="text-cyan-400 font-bold">Nexus Neural Engine v2.5</span>
      </div>

    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="toast fixed bottom-6 right-6 bg-slate-900 border border-slate-700 text-white px-4 py-3 rounded-xl shadow-2xl z-50 flex items-center space-x-3 text-xs">
    <span class="text-cyan-400 font-bold">ℹ</span>
    <span id="toast-msg">Action Completed</span>
  </div>
''')

    # Add Complete Script Engine
    html.append('''
  <script>
    const STORAGE_KEY = 'nexus_architect_mastery_v100x';
    let appState = null;
    try {
      appState = JSON.parse(localStorage.getItem(STORAGE_KEY));
    } catch(e) {}
    if (!appState || typeof appState !== 'object') {
      appState = {
        currentStage: 1,
        xp: 0,
        streak: 0,
        chapters: {},
        mastery: {},
        recall: {},
        notes: {}
      };
    }
    if (typeof appState.xp !== 'number' || isNaN(appState.xp)) appState.xp = 0;
    if (typeof appState.streak !== 'number' || isNaN(appState.streak)) appState.streak = 0;
    if (!appState.currentStage || appState.currentStage < 1 || appState.currentStage > 17) appState.currentStage = 1;
    if (!appState.mastery) appState.mastery = {};
    if (!appState.recall) appState.recall = {};
    if (!appState.notes) appState.notes = {};

    let activeStage = appState.currentStage || 1;
    let splitStudioOpen = false;

    // Cache modules metadata
    const modulesMeta = ''' + json.dumps(modules) + ''';

    function updateProgress() {
      const masteredCount = Object.values(appState.mastery || {}).filter(s => s === 'mastered').length;
      const totalChapters = 12;
      const pct = Math.round((masteredCount / totalChapters) * 100);
      const bar = document.getElementById('progress-bar');
      if (bar) bar.style.width = `${pct}%`;
      const pctText = document.getElementById('progress-pct-text');
      if (pctText) pctText.innerText = `${pct}%`;
    }

    function saveState() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
      updateProgress();
    }

    
    // ==================== CYBER AUDIO SYNTHESIZER ENGINE (ZERO-DEPENDENCY WEB AUDIO API) ====================
    const CyberAudio = {
      ctx: null,
      enabled: true,
      init() {
        if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
          const AudioClass = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioClass();
        }
        if (this.ctx && this.ctx.state === 'suspended') {
          this.ctx.resume();
        }
      },
      click() {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(800, this.ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.02);
          gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.02);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.02);
        } catch(e) {}
      },
      chirp() {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(450, this.ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(950, this.ctx.currentTime + 0.05);
          gain.gain.setValueAtTime(0.06, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.05);
        } catch(e) {}
      },
      chime() {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const notes = [523.25, 659.25, 783.99, 1046.50];
          notes.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.06);
            gain.gain.setValueAtTime(0.08, this.ctx.currentTime + idx * 0.06);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + idx * 0.06 + 0.35);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(this.ctx.currentTime + idx * 0.06);
            osc.stop(this.ctx.currentTime + idx * 0.06 + 0.35);
          });
        } catch(e) {}
      },
      thud() {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(160, this.ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(40, this.ctx.currentTime + 0.15);
          gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.15);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.15);
        } catch(e) {}
      },
      ping() {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(1760, this.ctx.currentTime);
          gain.gain.setValueAtTime(0.06, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.18);
        } catch(e) {}
      }
    };

    function toggleSoundFX() {
      CyberAudio.enabled = !CyberAudio.enabled;
      const icon = document.getElementById('sound-icon');
      if (icon) icon.innerText = CyberAudio.enabled ? '🔊' : '🔇';
      localStorage.setItem('nexus_sound_enabled', CyberAudio.enabled);
      if (CyberAudio.enabled) CyberAudio.chime();
      showToast(CyberAudio.enabled ? 'Audio Synthesizer: ENABLED' : 'Audio Synthesizer: MUTED');
    }

    // ==================== NEURAL COMMAND PALETTE (CTRL+K SPOTLIGHT) ====================
    let cmdActiveFilter = 'all';
    let cmdSelectedIndex = 0;
    let cmdFilteredItems = [];

    const COMMAND_ITEMS = [
      // 12 System Designs
      { id: 'sd-1', category: 'systems', title: 'Chapter 1: Distributed Telemetry & Config Pipeline', desc: '45k TPS, Kafka 3.6+ KRaft, Protobuf Zero-Copy, Murmur2 Partitioning', action: () => { goToStage(1); switchTab('ch1', 'blueprint'); } },
      { id: 'sd-2', category: 'systems', title: 'Chapter 2: Distributed Concurrency Coordinator & Fencing Lock', desc: 'Redis Lua EVALSHA, Martin Kleppmann Redlock Flaw, Monotonic Fencing Tokens', action: () => { goToStage(2); switchTab('ch2', 'blueprint'); } },
      { id: 'sd-3', category: 'systems', title: 'Chapter 3: High-Throughput Batch Mediation Pipeline', desc: '50k TPS, Memory Ring Buffer, LMAX Disruptor Ingestion, Parquet Columnar', action: () => { goToStage(3); switchTab('ch3', 'blueprint'); } },
      { id: 'sd-4', category: 'systems', title: 'Chapter 4: Real-Time Hierarchical Charging Tree Engine', desc: '3GPP CTE, Non-Blocking ConcurrentSkipListMap, Quota Reservation', action: () => { goToStage(4); switchTab('ch4', 'blueprint'); } },
      { id: 'sd-5', category: 'systems', title: 'Chapter 5: Globally Distributed Multi-Region Database', desc: 'Active-Active Multi-DC, ScyllaDB Murmur3 Token Ring, Cross-AZ Hinted Handoff', action: () => { goToStage(5); switchTab('ch5', 'blueprint'); } },
      { id: 'sd-6', category: 'systems', title: 'Chapter 6: Enterprise Distributed Rate Limiter', desc: 'GCRA & Token Bucket, Redis In-Memory Sharding, 250k eval/s, Fail-Open SLA', action: () => { goToStage(6); switchTab('ch6', 'blueprint'); } },
      { id: 'sd-7', category: 'systems', title: 'Chapter 7: Zero-Downtime Database Migration & Traffic Replay', desc: 'Dual-Write Monotonic Versioning, Shadow Queue Replay, Parity Reconciliation', action: () => { goToStage(7); switchTab('ch7', 'blueprint'); } },
      { id: 'sd-8', category: 'systems', title: 'Chapter 8: 5G Core User Plane Function (UPF) & CTF', desc: '100 Gbps Line-Rate DPDK Kernel Bypass, GTP-U Tunneling, Session AMBR Guard', action: () => { goToStage(8); switchTab('ch8', 'blueprint'); } },
      { id: 'sd-9', category: 'systems', title: 'Chapter 9: Multi-Region Active-Active ScyllaDB Cluster', desc: 'Consistent Hashing Token Ring, 128 VNodes, Anti-Entropy Background Repair', action: () => { goToStage(9); switchTab('ch9', 'blueprint'); } },
      { id: 'sd-10', category: 'systems', title: 'Chapter 10: Planet-Scale Distributed SQL (Google Spanner)', desc: 'TrueTime GPS + Atomic Clocks, External Consistency, Multi-Paxos Quorum Commit', action: () => { goToStage(10); switchTab('ch10', 'blueprint'); } },
      { id: 'sd-11', category: 'systems', title: 'Chapter 11: Enterprise Adaptive Rate Limiter & Concurrency Guard', desc: 'Client-Side Vegas/AIMD Concurrency Limiter, Noisy Neighbor Isolation', action: () => { goToStage(11); switchTab('ch11', 'blueprint'); } },
      { id: 'sd-12', category: 'systems', title: 'Chapter 12: Zero-Downtime Live DB Cutover & Shadow Traffic Replay', desc: 'Reconciliation Engine, Monotonic Verification, 1-Second DNS Rollback Switch', action: () => { goToStage(12); switchTab('ch12', 'blueprint'); } },

      // 8 Physics Simulators
      { id: 'sim-1', category: 'simulators', title: 'Simulator 1: Zero-Copy PageCache vs Userspace Buffers', desc: 'Linux sendfile() vs read()/write() 4-Step DMA Memory Physics', action: () => { goToStage(13); switchSim('sim-zerocopy'); } },
      { id: 'sim-2', category: 'simulators', title: 'Simulator 2: Raft / KRaft Quorum & Split-Brain Election', desc: '5-Node Cluster, Leader Election, Majority Quorums, Network Partition Injection', action: () => { goToStage(13); switchSim('sim-raft'); } },
      { id: 'sim-3', category: 'simulators', title: 'Simulator 3: Consistent Hashing Ring & Virtual Nodes', desc: 'MD5/Murmur3 360-Degree Hash Ring, VNodes, Minimal Key Resharding', action: () => { goToStage(13); switchSim('sim-hashring'); } },
      { id: 'sim-4', category: 'simulators', title: 'Simulator 4: Token Bucket & GCRA Rate Limiter Physics', desc: 'Continuous Rate Limiting, Capacity Bursting, 429 Retry-After Calculation', action: () => { goToStage(13); switchSim('sim-tokenbucket'); } },
      { id: 'sim-5', category: 'simulators', title: 'Simulator 5: Monotonic Fencing Token vs GC Pause Hazard', desc: 'Martin Kleppmann Redlock Flaw, Split-Brain Storage Corruption Prevention', action: () => { goToStage(13); switchSim('sim-fencing'); } },
      { id: 'sim-6', category: 'simulators', title: 'Simulator 6: Tail Latency Hedging & Backup Requests', desc: 'The Jeff Dean Google Pattern: p99.9 Tail Latency Killer Simulation', action: () => { goToStage(13); switchSim('sim-tail'); } },
      { id: 'sim-7', category: 'simulators', title: 'Simulator 7: LSM-Tree Leveled Compaction & Write Amplification', desc: 'MemTable WAL to SSTables, Cascading Compaction, Bloom Filter False Positives', action: () => { goToStage(13); switchSim('sim-lsm'); } },
      { id: 'sim-8', category: 'simulators', title: 'Simulator 8: 3GPP CTE Hierarchical Charging Tree', desc: 'Real-Time Enterprise Balance Reservation & Sub-Millisecond Quota Deductions', action: () => { goToStage(13); switchSim('sim-cte'); } },

      // Curriculum Stages
      { id: 'stage-14', category: 'tools', title: 'Stage 14: Google Staff Leadership STAR Playbook', desc: 'L6/L7 Cross-Functional Influence, Executive Conflicts, Architecture Governance', action: () => goToStage(14) },
      { id: 'stage-15', category: 'tools', title: 'Stage 15: Master Architecture Trade-Off Grid', desc: 'Comprehensive Storage, Consensus, Cache & Network Trade-Off Matrix', action: () => goToStage(15) },
      { id: 'stage-16', category: 'tools', title: 'Stage 16: Canonical Google Research Papers', desc: 'Spanner, MapReduce, GFS, Borg, Dynamo, Kafka, Raft Papers Compendium', action: () => goToStage(16) },
      { id: 'qa-inventory', category: 'tools', title: 'Q&A: Real-Time Retail Inventory Visibility (1,000s of Stores)', desc: 'Stream partitioning, Redis Lua atomic decrements, ScyllaDB ledger & edge resilience', action: () => goToStage(14) },
      { id: 'qa-sku', category: 'tools', title: 'Q&A: Stream Processing - Finding Latest State per SKU', desc: 'Out-of-order resolution, Kafka log compaction, in-memory RocksDB state stores', action: () => goToStage(14) },
      { id: 'qa-dedup', category: 'tools', title: 'Q&A: Large-Scale Duplicate Transaction Detection', desc: 'Real-time Bloom filters + Redis sliding window vs distributed MapReduce window scans', action: () => goToStage(14) },
      { id: 'qa-concurrency', category: 'tools', title: 'Q&A: Production Concurrency & Race Condition Elimination', desc: 'Java 21 Virtual Threads, CAS atomic primitives, ReentrantLock timeouts, monotonic fencing', action: () => goToStage(14) },
      { id: 'qa-solid', category: 'tools', title: 'Q&A: SOLID Architecture & Production Design Patterns', desc: 'Strategy, Builder, Template Method, Observer & complete Order Processing Service design', action: () => goToStage(14) },
      { id: 'stage-17', category: 'traps', title: 'Stage 17: Google L6/L8 Bar-Raiser Exam', desc: '15 High-Stakes Timed Staff Questions with Competency Level Evaluation', action: () => goToStage(17) },

      // Interactive Tools & Actions
      { id: 'tool-wb', category: 'tools', title: '🎨 Architectural Whiteboard Studio', desc: 'Vector drawing, component stamping, pre-baked topologies & PNG export', action: () => openWhiteboardModal() },
      { id: 'tool-pomo', category: 'tools', title: '⏱️ Toggle Focus Pomodoro Timer', desc: 'Start or pause 25-minute deep work focus block', action: () => togglePomodoro() },
      { id: 'tool-focus', category: 'tools', title: '🎧 Focus Cockpit & Ambient Soundscapes', desc: 'Brown, Pink, White & 40Hz Gamma wave cognitive sound generators', action: () => openFocusCockpitModal() },
      { id: 'tool-ambush', category: 'traps', title: '⚔️ Surprise Google Staff Ambush Drill', desc: 'Instant high-priority trap question with countdown timer', action: () => triggerRandomTrapQuestion() },
      { id: 'tool-gamify', category: 'tools', title: '⭐ Level & Engineering XP Hub', desc: 'View current level milestones, badges and architectural accomplishments', action: () => openGamificationModal() },
      { id: 'tool-streak', category: 'tools', title: '🔥 14-Day Study Consistency Heatmap', desc: 'Track daily mastery habits and streak progression', action: () => openStreakModal() },
      { id: 'tool-export', category: 'tools', title: '📑 Export Complete Staff Prep Book (.md)', desc: 'Download offline Markdown compendium of all 12 system designs & formulas', action: () => exportPrepBookMarkdown() },
      { id: 'tool-sound', category: 'tools', title: '🔊 Toggle Cyber Audio Synthesizer', desc: 'Enable or mute sound feedback for clicks, chirps, and simulations', action: () => toggleSoundFX() }
    ];

    function openCommandPalette() {
      CyberAudio.chirp();
      const modal = document.getElementById('command-palette-modal');
      const input = document.getElementById('cmd-palette-input');
      if (modal) {
        modal.classList.remove('hidden');
        if (input) {
          input.value = '';
          input.focus();
        }
        cmdActiveFilter = 'all';
        filterCommandPalette('');
      }
    }

    function closeCommandPalette() {
      const modal = document.getElementById('command-palette-modal');
      if (modal) modal.classList.add('hidden');
    }

    function setCommandFilter(category) {
      CyberAudio.click();
      cmdActiveFilter = category;
      document.querySelectorAll('.cmd-filter').forEach(btn => {
        btn.classList.remove('active', 'bg-cyan-950', 'text-cyan-300', 'border-cyan-800', 'font-bold');
        btn.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
      });
      const activeBtn = document.getElementById(`cmd-filter-${category}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-cyan-950', 'text-cyan-300', 'border-cyan-800', 'font-bold');
        activeBtn.classList.remove('bg-slate-900', 'text-slate-400', 'border-slate-800');
      }
      const input = document.getElementById('cmd-palette-input');
      filterCommandPalette(input ? input.value : '');
    }

    function filterCommandPalette(query) {
      query = (query || '').toLowerCase().trim();
      cmdFilteredItems = COMMAND_ITEMS.filter(item => {
        if (cmdActiveFilter !== 'all' && item.category !== cmdActiveFilter) return false;
        if (!query) return true;
        return item.title.toLowerCase().includes(query) || 
               item.desc.toLowerCase().includes(query) ||
               item.id.toLowerCase().includes(query);
      });

      cmdSelectedIndex = 0;
      renderCommandResults();
    }

    function renderCommandResults() {
      const container = document.getElementById('cmd-palette-results');
      if (!container) return;

      if (cmdFilteredItems.length === 0) {
        container.innerHTML = `
          <div class="p-6 text-center text-slate-500 font-mono text-xs">
            <span class="text-2xl block mb-2">🔍</span>
            No matching system designs or tools found. Try "raft", "kafka", "ch1", or "whiteboard".
          </div>
        `;
        return;
      }

      container.innerHTML = cmdFilteredItems.map((item, idx) => {
        const isSelected = (idx === cmdSelectedIndex);
        const selClasses = isSelected ? 'bg-cyan-950/80 border-cyan-500/80 text-white shadow-lg' : 'bg-slate-950/40 border-slate-800/80 text-slate-300 hover:bg-slate-900';
        
        let catBadge = '';
        if (item.category === 'systems') catBadge = '<span class="text-[9px] px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-mono">System</span>';
        else if (item.category === 'simulators') catBadge = '<span class="text-[9px] px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 font-mono">Physics</span>';
        else if (item.category === 'traps') catBadge = '<span class="text-[9px] px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-mono">Trap Drill</span>';
        else catBadge = '<span class="text-[9px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700 font-mono">Tool</span>';

        return `
          <div onclick="executeCommandItem(${idx})" class="p-2.5 rounded-xl border ${selClasses} cursor-pointer transition-all flex items-center justify-between gap-3 group">
            <div class="space-y-0.5 min-w-0">
              <div class="flex items-center gap-2">
                ${catBadge}
                <span class="font-bold text-xs font-mono group-hover:text-cyan-300 transition-colors truncate">${item.title}</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate">${item.desc}</p>
            </div>
            <kbd class="shrink-0 px-2 py-0.5 rounded bg-slate-900 text-[10px] font-mono text-slate-400 border border-slate-800">↵</kbd>
          </div>
        `;
      }).join('');
    }

    function handleCommandPaletteKey(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (cmdFilteredItems.length > 0) {
          cmdSelectedIndex = (cmdSelectedIndex + 1) % cmdFilteredItems.length;
          CyberAudio.click();
          renderCommandResults();
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (cmdFilteredItems.length > 0) {
          cmdSelectedIndex = (cmdSelectedIndex - 1 + cmdFilteredItems.length) % cmdFilteredItems.length;
          CyberAudio.click();
          renderCommandResults();
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        executeCommandItem(cmdSelectedIndex);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeCommandPalette();
      }
    }

    function executeCommandItem(idx) {
      if (cmdFilteredItems[idx] && typeof cmdFilteredItems[idx].action === 'function') {
        CyberAudio.chirp();
        closeCommandPalette();
        cmdFilteredItems[idx].action();
      }
    }

    // ==================== WHITEBOARD COMPONENT STENCILS & ARCHETYPES ====================
    function addWhiteboardComponent(type) {
      CyberAudio.click();
      const container = document.getElementById('modal-whiteboard-nodes') || document.getElementById('whiteboard-nodes');
      if (!container) return;

      const configs = {
        tower: { icon: '🗼', name: 'Edge Cell Tower', desc: 'eCPRI / IPSec / 20M Sectors', color: 'border-cyan-500 bg-cyan-950/90 text-cyan-200' },
        envoy: { icon: '🛡️', name: 'Envoy LB Fleet', desc: 'Token Bucket Rate Limiting & TLS Offload', color: 'border-blue-500 bg-blue-950/90 text-blue-200' },
        gateway: { icon: '⚡', name: 'Ingress Gateway', desc: 'Go/C++ Protobuf & Murmur2 Partitioning', color: 'border-indigo-500 bg-indigo-950/90 text-indigo-200' },
        kafka: { icon: '🪵', name: 'Kafka 3.6+ KRaft', desc: 'NVMe WAL & PageCache Zero-Copy (acks=all)', color: 'border-amber-500 bg-amber-950/90 text-amber-200' },
        redis: { icon: '⚡', name: 'Redis 7.2 Cluster', desc: 'Lua Atomic Coordinator & Fencing Tokens', color: 'border-purple-500 bg-purple-950/90 text-purple-200' },
        db: { icon: '🗄️', name: 'ScyllaDB / Spanner', desc: 'Consistent Hash Ring & TrueTime Commit', color: 'border-emerald-500 bg-emerald-950/90 text-emerald-200' },
        flink: { icon: '🌊', name: 'Apache Flink CEP', desc: 'Real-Time State Machine (<100ms Alarms)', color: 'border-teal-500 bg-teal-950/90 text-teal-200' }
      };

      const cfg = configs[type] || configs.gateway;
      const id = 'node-' + Date.now();
      const card = document.createElement('div');
      card.id = id;
      card.className = `absolute p-3 rounded-xl border ${cfg.color} shadow-2xl font-mono text-xs cursor-move select-none transition-shadow hover:shadow-cyan-500/20`;
      card.style.left = `${Math.floor(Math.random() * 250) + 80}px`;
      card.style.top = `${Math.floor(Math.random() * 200) + 80}px`;
      card.style.width = '210px';

      card.innerHTML = `
        <div class="flex items-center justify-between border-b border-white/10 pb-1.5 mb-1.5">
          <div class="flex items-center gap-1.5 font-bold">
            <span>${cfg.icon}</span>
            <span>${cfg.name}</span>
          </div>
          <button onclick="document.getElementById('${id}').remove()" class="text-slate-400 hover:text-white px-1">&times;</button>
        </div>
        <div class="text-[10px] text-slate-300 leading-snug">${cfg.desc}</div>
      `;

      // Simple drag mechanics
      let isDragging = false, offsetLeft = 0, offsetTop = 0;
      card.onmousedown = (e) => {
        if (e.target.tagName === 'BUTTON') return;
        isDragging = true;
        offsetLeft = e.clientX - card.offsetLeft;
        offsetTop = e.clientY - card.offsetTop;
        card.style.zIndex = 100;
      };
      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        card.style.left = (e.clientX - offsetLeft) + 'px';
        card.style.top = (e.clientY - offsetTop) + 'px';
      });
      window.addEventListener('mouseup', () => {
        isDragging = false;
      });

      container.appendChild(card);
      showToast(`Added ${cfg.name} to Whiteboard`);
    }

    function loadArchitectureArchetype(archetype) {
      CyberAudio.chime();
      clearWhiteboard();
      const container = document.getElementById('modal-whiteboard-nodes') || document.getElementById('whiteboard-nodes');
      if (!container) return;

      if (archetype === 'telemetry') {
        addWhiteboardComponent('tower');
        addWhiteboardComponent('envoy');
        addWhiteboardComponent('gateway');
        addWhiteboardComponent('kafka');
        addWhiteboardComponent('flink');
        showToast('Loaded Ch1 Telemetry Ingestion Architecture Archetype');
      } else if (archetype === 'fencing') {
        addWhiteboardComponent('gateway');
        addWhiteboardComponent('redis');
        addWhiteboardComponent('db');
        showToast('Loaded Ch2 Redis Atomic Fencing Lock Archetype');
      } else if (archetype === 'spanner') {
        addWhiteboardComponent('envoy');
        addWhiteboardComponent('gateway');
        addWhiteboardComponent('db');
        showToast('Loaded Ch10 Spanner TrueTime Archetype');
      }
    }

    // ==================== OFFLINE STAFF PREP BOOK MARKDOWN EXPORTER ====================
    function exportPrepBookMarkdown() {
      CyberAudio.chime();
      showToast('Generating Google Staff Engineer Mastery Prep Book...');
      
      let md = `# Shivam Agarwal - Google Staff & Principal Systems Engineer Mastery Compendium\n`;
      md += `Generated: ${new Date().toISOString()} | Target Level: Google L6 (Staff) / L7 (Principal)\n\n`;
      md += `## Table of System Architecture Blueprints\n\n`;

      COMMAND_ITEMS.filter(it => it.category === 'systems').forEach((it, idx) => {
        md += `### ${it.title}\n`;
        md += `- **Architecture Core:** ${it.desc}\n`;
        md += `- **Non-Functional Target:** Sub-millisecond latency, zero-copy memory buffers, RPO=0 / RTO<30s\n\n`;
      });

      md += `## Distributed Systems Physics Simulators\n\n`;
      COMMAND_ITEMS.filter(it => it.category === 'simulators').forEach((it, idx) => {
        md += `### ${it.title}\n`;
        md += `- **Physics Invariant:** ${it.desc}\n\n`;
      });

      md += `## Executive Leadership & Bar-Raiser Checklist\n\n`;
      md += `## Google L6 Technical Screening & Core Systems Mastery Q&A\n\n`;
      md += `### 1. Carrier-Grade Microservices Architecture (Samsung USM CM)\n`;
      md += `- 3,164+ Java files, 60+ sub-modules managing 4G/5G/O-RAN across 15+ Tier-1 operators.\n`;
      md += `- Workload bulkheading, key-partitioned Kafka ingestion, distributed session locking.\n\n`;
      md += `### 2. Real-Time Retail Inventory Visibility (Thousands of Stores)\n`;
      md += `- Partitioned Kafka (store_id:sku_id) -> Redis Cluster (Lua atomic decrement) -> ScyllaDB immutable ledger.\n\n`;
      md += `### 3. Stream Processing: Latest State per SKU\n`;
      md += `- In-memory RocksDB state store with sequence/timestamp checks + Kafka log compaction.\n\n`;
      md += `### 4. Large-Scale Duplicate Transaction Detection\n`;
      md += `- Real-time Bloom filter + Redis sliding window; Batch MapReduce hash-partitioning with local window scans.\n\n`;
      md += `### 5. Production Concurrency & Race Conditions\n`;
      md += `- Java 21 Loom Virtual Threads, CAS lock-free primitives (AtomicLong), monotonic fencing tokens.\n\n`;
      md += `### 6. Production Design Patterns & SOLID\n`;
      md += `- Strategy, Builder, Template Method, Observer; complete Order Processing decoupled architecture.\n\n`;

      md += `1. **Scope Ambiguity:** Always define functional boundaries, traffic profile (p99/p99.9), and linearizability requirements in the first 4 minutes.\n`;
      md += `2. **Resilience Physics:** Address split-brain hazards, cascading GC pauses, and disk write amplification explicitly.\n`;
      md += `3. **Executive Trade-offs:** Never present an architecture without explaining what you sacrificed (e.g. latency vs consistency, cost vs redundancy).\n\n`;

      const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Shivam_Google_Staff_Engineer_Preparation_Compendium.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      showToast('Downloaded Complete Staff Prep Book (.md)!');
    }

    // ==================== GLOBAL KEYBOARD SHORTCUTS LISTENER ====================
    window.addEventListener('keydown', (e) => {
      // Ignore if user is currently typing inside an input or textarea (unless ESC or Ctrl+K)
      const isInput = (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA');

      // Ctrl+K or Cmd+K: Neural Command Palette
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        const modal = document.getElementById('command-palette-modal');
        if (modal && !modal.classList.contains('hidden')) {
          closeCommandPalette();
        } else {
          openCommandPalette();
        }
        return;
      }

      // Escape: Close all open modals
      if (e.key === 'Escape') {
        closeCommandPalette();
        closeWhiteboardModal();
        closeGamificationModal();
        closeStreakModal();
        closeFocusCockpitModal();
        closeTrapModal();
        closeNumberDerivationModal();
        closeVideoModal();
        closeMasteryHubModal();
        return;
      }

      if (isInput) return;

      // Alt+1 to Alt+9: Jump to Chapter 1 to 9
      if (e.altKey && e.key >= '1' && e.key <= '9') {
        e.preventDefault();
        const chNum = parseInt(e.key, 10);
        CyberAudio.chirp();
        goToStage(chNum);
        showToast(`Jumped to Chapter ${chNum}`);
        return;
      }

      // Alt+S: Jump to Physics Simulators (Stage 13)
      if (e.altKey && e.key.toLowerCase() === 's') {
        e.preventDefault();
        CyberAudio.chirp();
        goToStage(13);
        showToast('Jumped to Physics Lab (Stage 13)');
        return;
      }

      // Alt+W: Open Whiteboard Studio
      if (e.altKey && e.key.toLowerCase() === 'w') {
        e.preventDefault();
        openWhiteboardModal();
        return;
      }

      // Alt+F: Open Focus Pomodoro Cockpit
      if (e.altKey && e.key.toLowerCase() === 'f') {
        e.preventDefault();
        openFocusCockpitModal();
        return;
      }

      // Alt+A: Trigger Ambush Drill
      if (e.altKey && e.key.toLowerCase() === 'a') {
        e.preventDefault();
        triggerRandomTrapQuestion();
        return;
      }
    });
// ==================== STAGE NAVIGATION ====================
    function goToStage(stageNum) {
      stageNum = parseInt(stageNum, 10);
      if (isNaN(stageNum) || stageNum < 1 || stageNum > 17) stageNum = 1;
      activeStage = stageNum;
      appState.currentStage = stageNum;
      CyberAudio.click();
      saveState();

      for (let i = 1; i <= 17; i++) {
        const item = document.getElementById(`side-nav-${i}`);
        const sec = document.getElementById(`stage-${i}`);
        const isCurrent = (i === stageNum);

        if (item) item.classList.toggle('active', isCurrent);
        if (sec) {
          if (isCurrent) {
            sec.classList.add('active-stage');
            sec.style.setProperty('display', 'flex', 'important');
          } else {
            sec.classList.remove('active-stage');
            sec.style.setProperty('display', 'none', 'important');
          }
        }
      }

      // Dynamic Edge Tab Title
      try {
        let tName = 'Nexus Architect';
        if (stageNum <= 12 && Array.isArray(modulesMeta)) {
          const mod = modulesMeta.find(m => m.num === stageNum);
          if (mod) tName = `${mod.title} • Nexus Architect`;
        } else if (stageNum === 13) {
          tName = 'Physics Lab • Nexus Architect';
        } else if (stageNum === 14) {
          tName = 'Leadership Playbook • Nexus Architect';
        } else if (stageNum === 15) {
          tName = 'Trade-Off Grid • Nexus Architect';
        } else if (stageNum === 16) {
          tName = 'Classic Papers • Nexus Architect';
        } else if (stageNum === 17) {
          tName = 'Bar-Raiser Exam • Nexus Architect';
        }
        document.title = tName;
      } catch(e) {}

      if (stageNum <= 12) {
        updateCapacityCalc(`ch${stageNum}`);
        updateMasteryPill(`ch${stageNum}`);
      }

      if (stageNum === 13) {
        setTimeout(() => {
          initZeroCopyCanvas();
          drawRaft();
          drawHashRing();
          drawTokenBucket();
          drawFencingCanvas(0);
          drawTailCanvas();
          drawLsmCanvas();
        }, 100);
      }
    }

    // ==================== TAB SWITCHING & STEPPERS ====================
    const TAB_KEYS = ['blueprint', 'tldr', 'diff', 'capacity', 'theory', 'project', 'code', 'traps', 'recall', 'videos', 'pitch', 'notes'];

    function switchTab(chapter, tabName) {
      let container = null;
      if (chapter) {
        const num = chapter.replace('ch', '');
        container = document.getElementById(`stage-${num}`) || document.getElementById(chapter);
      }
      if (!container) container = document.getElementById(`stage-${activeStage}`) || document;

      container.querySelectorAll('.micro-tab').forEach(btn => btn.classList.remove('active'));
      container.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

      const activeBtn = document.getElementById(`${chapter}-tab-${tabName}`);
      const activeContent = document.getElementById(`${chapter}-content-${tabName}`);
      if (activeBtn) activeBtn.classList.add('active');
      if (activeContent) activeContent.classList.remove('hidden');

      // Update section indicator badge (e.g. "1 / 12", "7 / 12", "8 / 12")
      const ind = document.getElementById(`${chapter}-tab-indicator`);
      if (ind) {
        const idx = TAB_KEYS.indexOf(tabName);
        if (idx !== -1) {
          ind.innerText = `${idx + 1} / ${TAB_KEYS.length}`;
        }
      }

      if (tabName === 'capacity') updateCapacityCalc(chapter);
    }

    function stepTab(chapter, delta) {
      let container = null;
      if (chapter) {
        const num = chapter.replace('ch', '');
        container = document.getElementById(`stage-${num}`) || document.getElementById(chapter);
      }
      if (!container) container = document.getElementById(`stage-${activeStage}`) || document;

      let currentIndex = 0;
      for (let i = 0; i < TAB_KEYS.length; i++) {
        const btn = document.getElementById(`${chapter}-tab-${TAB_KEYS[i]}`);
        if (btn && btn.classList.contains('active')) {
          currentIndex = i;
          break;
        }
      }

      let nextIndex = currentIndex + delta;
      if (nextIndex < 0) nextIndex = 0;
      if (nextIndex >= TAB_KEYS.length) nextIndex = TAB_KEYS.length - 1;

      switchTab(chapter, TAB_KEYS[nextIndex]);

      const scrollArea = container.querySelector('.main-stage-scroll');
      if (scrollArea) scrollArea.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function toggleTopologyView(chId, viewType) {
      const visualEl = document.getElementById(`${chId}-topo-visual`);
      const asciiEl = document.getElementById(`${chId}-topo-ascii`);
      const btnVisual = document.getElementById(`${chId}-btn-topo-visual`);
      const btnAscii = document.getElementById(`${chId}-btn-topo-ascii`);

      if (viewType === 'visual') {
        if (visualEl) visualEl.classList.remove('hidden');
        if (asciiEl) asciiEl.classList.add('hidden');
        if (btnVisual) {
          btnVisual.className = 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold transition-all shadow';
        }
        if (btnAscii) {
          btnAscii.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all';
        }
      } else {
        if (visualEl) visualEl.classList.add('hidden');
        if (asciiEl) asciiEl.classList.remove('hidden');
        if (btnAscii) {
          btnAscii.className = 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold transition-all shadow';
        }
        if (btnVisual) {
          btnVisual.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all';
        }
      }
    }

    function toggleSchemaView(chId, viewType) {
      const visualEl = document.getElementById(`${chId}-schema-visual`);
      const protoEl = document.getElementById(`${chId}-schema-proto`);
      const wireEl = document.getElementById(`${chId}-schema-wire`);
      const btnVisual = document.getElementById(`${chId}-btn-schema-visual`);
      const btnProto = document.getElementById(`${chId}-btn-schema-proto`);
      const btnWire = document.getElementById(`${chId}-btn-schema-wire`);

      const activeClass = 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold transition-all shadow';
      const inactiveClass = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all';

      if (visualEl) visualEl.classList.add('hidden');
      if (protoEl) protoEl.classList.add('hidden');
      if (wireEl) wireEl.classList.add('hidden');

      if (btnVisual) btnVisual.className = inactiveClass;
      if (btnProto) btnProto.className = inactiveClass;
      if (btnWire) btnWire.className = inactiveClass;

      if (viewType === 'visual') {
        if (visualEl) visualEl.classList.remove('hidden');
        if (btnVisual) btnVisual.className = activeClass;
      } else if (viewType === 'proto') {
        if (protoEl) protoEl.classList.remove('hidden');
        if (btnProto) btnProto.className = activeClass;
      } else if (viewType === 'wire') {
        if (wireEl) wireEl.classList.remove('hidden');
        if (btnWire) btnWire.className = activeClass;
      }
    }

    function copyProtoCode(chId) {
      const codeEl = document.getElementById(`${chId}-raw-proto-code`);
      if (!codeEl) return;
      const text = codeEl.innerText;
      navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById(`${chId}-btn-copy-proto`);
        if (btn) {
          const originalText = btn.innerHTML;
          btn.innerHTML = '✓ Copied!';
          btn.classList.add('text-emerald-400');
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('text-emerald-400');
          }, 2000);
        }
      }).catch(err => {
        console.error('Failed to copy text: ', err);
      });
    }

    function switchSim(simId) {
      document.querySelectorAll('#sim-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.sim-panel').forEach(panel => panel.classList.add('hidden'));

      const activeBtn = document.getElementById(`tab-${simId}`);
      const activePanel = document.getElementById(simId);
      if (activeBtn) activeBtn.classList.add('active');
      if (activePanel) activePanel.classList.remove('hidden');
    }

    // ==================== CAPACITY MATH ENGINE ====================
    function updateCapacityCalc(chId) {
      const qpsEl = document.getElementById(`${chId}-calc-qps`);
      const sizeEl = document.getElementById(`${chId}-calc-size`);
      const repEl = document.getElementById(`${chId}-calc-rep`);
      const retEl = document.getElementById(`${chId}-calc-ret`);
      if (!qpsEl || !sizeEl) return;

      const qps = parseInt(qpsEl.value);
      const size = parseInt(sizeEl.value);
      const rep = parseInt(repEl.value);
      const ret = parseInt(retEl.value);

      document.getElementById(`${chId}-val-qps`).innerText = qps.toLocaleString() + ' req/s';
      document.getElementById(`${chId}-val-size`).innerText = size >= 1024 ? (size/1024).toFixed(1) + ' KB' : size + ' B';
      document.getElementById(`${chId}-val-rep`).innerText = rep + 'x';
      document.getElementById(`${chId}-val-ret`).innerText = ret + ' days';

      const bytesPerSec = qps * size;
      const mbPerSec = (bytesPerSec / (1024 * 1024)).toFixed(1);
      const gbps = ((bytesPerSec * 8) / 1e9).toFixed(2);
      const dailyGb = Math.round((bytesPerSec * 86400 * rep) / (1024 * 1024 * 1024));
      const totalTb = ((bytesPerSec * 86400 * rep * ret * 1.2) / (1024 * 1024 * 1024 * 1024)).toFixed(1);
      const partitions = Math.max(16, Math.min(512, Math.ceil(qps / 350)));
      const pageCacheGb = Math.max(8, Math.min(256, Math.ceil((bytesPerSec * 300) / (1024 * 1024 * 1024))));

      document.getElementById(`${chId}-res-bw`).innerText = `${mbPerSec} MB/s (${gbps} Gbps)`;
      document.getElementById(`${chId}-res-daily`).innerText = `${dailyGb.toLocaleString()} GB / day`;
      document.getElementById(`${chId}-res-storage`).innerText = `${totalTb} TB (with headroom)`;
      document.getElementById(`${chId}-res-part`).innerText = `${partitions} Partitions (~350 msg/s)`;
      document.getElementById(`${chId}-res-ram`).innerText = `${pageCacheGb} GB PageCache RAM`;
    }

    // Gamification modals (XP display and calculation implemented in Gamification Hub below)
    function closeGamificationModal() {
      document.getElementById('gamification-modal').classList.add('hidden');
    }

    function openStreakModal() {
      document.getElementById('streak-modal').classList.remove('hidden');
    }
    function closeStreakModal() {
      document.getElementById('streak-modal').classList.add('hidden');
    }

    // ==================== FOCUS TIMER & WEBAUDIO SOUNDS ====================
    let pomoInterval = null;
    let pomoSecs = 25 * 60;
    let pomoRunning = false;
    let audioCtx = null;
    let noiseNode = null;

    function togglePomodoro() {
      const btn = document.getElementById('btn-pomo-toggle');
      if (pomoRunning) {
        clearInterval(pomoInterval);
        pomoRunning = false;
        btn.innerText = 'Resume';
      } else {
        pomoRunning = true;
        btn.innerText = 'Pause';
        pomoInterval = setInterval(() => {
          if (pomoSecs > 0) {
            pomoSecs--;
            renderPomoTime();
          } else {
            clearInterval(pomoInterval);
            pomoRunning = false;
            btn.innerText = 'Start';
            showToast('Pomodoro Focus Session Completed! +100 XP');
            addXP(100, 'Completed Deep Work Session');
          }
        }, 1000);
      }
    }

    function resetPomodoro() {
      clearInterval(pomoInterval);
      pomoRunning = false;
      pomoSecs = 25 * 60;
      renderPomoTime();
      const btn = document.getElementById('btn-pomo-toggle');
      if (btn) btn.innerText = 'Start';
      try {
        document.title = document.title.replace(/^\(\d+:\d+\)\s*/, '');
      } catch(e) {}
    }

    function renderPomoTime() {
      const m = Math.floor(pomoSecs / 60);
      const s = pomoSecs % 60;
      const timeStr = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      const disp = document.getElementById('pomo-display');
      if (disp) disp.innerText = timeStr;

      try {
        const baseTitle = document.title.replace(/^\(\d+:\d+\)\s*/, '');
        if (pomoRunning) {
          document.title = `(${timeStr}) ${baseTitle}`;
        } else {
          document.title = baseTitle;
        }
      } catch(e) {}
    }

    function setPomodoroTime(mins) {
      clearInterval(pomoInterval);
      pomoRunning = false;
      pomoSecs = mins * 60;
      renderPomoTime();
      document.getElementById('btn-pomo-toggle').innerText = 'Start';
      closeFocusCockpitModal();
      showToast(`Set Focus timer to ${mins} minutes!`);
    }

    function openFocusCockpitModal() {
      document.getElementById('focus-modal').classList.remove('hidden');
    }
    function closeFocusCockpitModal() {
      document.getElementById('focus-modal').classList.add('hidden');
    }

    function toggleAmbientNoise(type) {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (noiseNode) {
        noiseNode.stop();
        noiseNode = null;
        showToast('Ambient focus noise stopped.');
        return;
      }

      const bufferSize = audioCtx.sampleRate * 2;
      const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      let lastOut = 0.0;

      for (let i = 0; i < bufferSize; i++) {
        if (type === 'brown') {
          const white = Math.random() * 2 - 1;
          data[i] = (lastOut + (0.02 * white)) / 1.02;
          lastOut = data[i];
          data[i] *= 3.5;
        } else {
          data[i] = Math.random() * 0.15 - 0.075;
        }
      }

      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = buffer;
      noiseNode.loop = true;
      const gainNode = audioCtx.createGain();
      gainNode.gain.value = 0.15;
      noiseNode.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      noiseNode.start();
      showToast(`Started ${type} focus soundscape!`);
    }

    // ==================== NUMBER DERIVATION MODAL ====================
    function openNumberDerivationModal(chId, numIdx) {
      const chNum = parseInt(chId.replace('ch', ''));
      const m = modulesMeta.find(item => item.num === chNum);
      if (!m || !m.numbers_detailed || !m.numbers_detailed[numIdx]) return;

      const item = m.numbers_detailed[numIdx];
      document.getElementById('num-modal-title').innerText = `${item.label}: ${item.val}`;
      document.getElementById('num-modal-derivation').innerText = item.derivation;
      document.getElementById('num-modal-soundbite').innerText = `"${item.soundbite}"`;
      document.getElementById('num-modal-question').innerText = item.interview_question;
      document.getElementById('number-modal').classList.remove('hidden');
    }

    function closeNumberDerivationModal() {
      document.getElementById('number-modal').classList.add('hidden');
    }

    // ==================== VIDEO MODAL ====================
    function openVideoModal(videoId, title) {
      const modal = document.getElementById('video-modal');
      const iframe = document.getElementById('video-modal-iframe');
      const titleEl = document.getElementById('video-modal-title');
      if (titleEl) titleEl.innerText = title;
      if (iframe && videoId) iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
      if (modal) modal.classList.remove('hidden');
    }
    function closeVideoModal() {
      const modal = document.getElementById('video-modal');
      const iframe = document.getElementById('video-modal-iframe');
      if (iframe) iframe.src = '';
      if (modal) modal.classList.add('hidden');
    }

    // ==================== CODE TABS ====================
    function switchCodeTab(chId, fileType) {
      const container = document.getElementById(`code-${chId}`) || document.getElementById(`${chId}-content-code`);
      if (!container) return;
      container.querySelectorAll('.code-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-slate-800', 'text-cyan-400');
        btn.classList.add('bg-slate-900', 'text-slate-400');
      });
      container.querySelectorAll('.code-file-view').forEach(view => view.classList.add('hidden'));

      const activeBtn = document.getElementById(`${chId}-btn-code-${fileType}`);
      const activeView = document.getElementById(`${chId}-file-${fileType}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-slate-800', 'text-cyan-400');
        activeBtn.classList.remove('bg-slate-900', 'text-slate-400');
      }
      if (activeView) activeView.classList.remove('hidden');
    }

    // ==================== MASTERY HUB ====================
    let activeMasteryChapter = 'ch1';
    function openMasteryHubModal(chId) {
      activeMasteryChapter = chId;
      document.getElementById('mastery-modal').classList.remove('hidden');
    }
    function closeMasteryHubModal() {
      document.getElementById('mastery-modal').classList.add('hidden');
    }
    function setMasteryStatus(status) {
      appState.mastery[activeMasteryChapter] = status;
      saveState();
      updateMasteryPill(activeMasteryChapter);
      closeMasteryHubModal();
      if (status === 'mastered') addXP(100, `Mastered ${activeMasteryChapter.toUpperCase()}`);
    }
    function updateMasteryPill(chId) {
      const status = appState.mastery[chId] || 'learning';
      const textEl = document.getElementById(`${chId}-mastery-status-text`);
      const iconEl = document.getElementById(`${chId}-mastery-status-icon`);
      if (!textEl) return;

      if (status === 'mastered') {
        textEl.innerText = 'Status: ✅ Mastered';
        iconEl.innerText = '⭐';
      } else if (status === 'review') {
        textEl.innerText = 'Status: ⚠️ Needs Review';
        iconEl.innerText = '🔄';
      } else {
        textEl.innerText = 'Status: 📖 Learning';
        iconEl.innerText = '⚪';
      }
    }

    // ==================== WHITEBOARD & SPLIT STUDIO ENGINE ====================
    let wbCurrentTool = 'pen';
    let wbCurrentColor = '#00f0ff';
    let wbCurrentWidth = 3;
    let wbIsDrawing = false;
    let wbStartX = 0, wbStartY = 0;
    let wbActiveCanvasId = 'split-canvas';

    const STENCIL_CONFIGS = {
      gateway: { icon: '🌐', title: 'API Gateway', role: 'Ingress Envoy / WAF', color: 'border-blue-500/60 bg-blue-950/90 text-blue-300' },
      kafka: { icon: '⚡', title: 'Kafka Cluster', role: 'KRaft Partition Ring', color: 'border-cyan-500/60 bg-cyan-950/90 text-cyan-300' },
      scylla: { icon: '🗄️', title: 'ScyllaDB / LSM', role: 'Multi-DC NoSQL', color: 'border-purple-500/60 bg-purple-950/90 text-purple-300' },
      redis: { icon: '🔴', title: 'Redis Cache', role: 'In-Memory / Token Bucket', color: 'border-rose-500/60 bg-rose-950/90 text-rose-300' },
      flink: { icon: '🌊', title: 'Flink CEP', role: 'RocksDB Stream Window', color: 'border-teal-500/60 bg-teal-950/90 text-teal-300' },
      postgres: { icon: '🐘', title: 'PostgreSQL', role: 'WAL Relational Store', color: 'border-indigo-500/60 bg-indigo-950/90 text-indigo-300' },
      raft: { icon: '🗳️', title: 'Raft Leader', role: 'Consensus State Machine', color: 'border-amber-500/60 bg-amber-950/90 text-amber-300' },
      pod: { icon: '📦', title: 'Worker Pod', role: 'Go / Java 21 Service', color: 'border-emerald-500/60 bg-emerald-950/90 text-emerald-300' }
    };

    const MODULE_STENCIL_PRESETS = {
      ch1: [
        { type: 'gateway', x: 30, y: 70, title: 'Envoy Gateway', desc: '48 Pods Rate Limited' },
        { type: 'kafka', x: 180, y: 70, title: 'Kafka KRaft', desc: '6 Brokers • 128 Partitions' },
        { type: 'pod', x: 340, y: 30, title: 'Spring Consumer', desc: 'Cooperative Sticky' },
        { type: 'scylla', x: 340, y: 130, title: 'ScyllaDB Tier', desc: 'LSM Engine • NVMe' }
      ],
      ch2: [
        { type: 'gateway', x: 30, y: 70, title: '100 GbE NIC', desc: '14.88 Mpps Wire Rate' },
        { type: 'pod', x: 180, y: 70, title: 'eBPF / XDP Hook', desc: 'Drop 18ns / AF_XDP' },
        { type: 'pod', x: 340, y: 70, title: 'DPDK Polling', desc: 'Pinned NUMA Fastpath' }
      ],
      ch3: [
        { type: 'pod', x: 30, y: 70, title: 'Worker Pods', desc: '500 K8s Workers' },
        { type: 'redis', x: 180, y: 70, title: 'Redis Master', desc: 'Atomic Lua + Token' },
        { type: 'postgres', x: 340, y: 70, title: 'PostgreSQL Sink', desc: 'WHERE token > last' }
      ],
      ch4: [
        { type: 'pod', x: 30, y: 70, title: 'Proposal Client', desc: 'Linearizable Write' },
        { type: 'raft', x: 180, y: 70, title: 'Raft Leader', desc: 'Term 2 • High Watermark' },
        { type: 'pod', x: 340, y: 30, title: 'Follower 1 (AZ1)', desc: 'Quorum ACK' },
        { type: 'pod', x: 340, y: 130, title: 'Follower 2 (AZ2)', desc: 'Quorum ACK' }
      ],
      ch5: [
        { type: 'gateway', x: 30, y: 70, title: 'Raw ASN.1 Lake', desc: '2GB Memory-Mapped' },
        { type: 'pod', x: 180, y: 70, title: 'Virtual Threads', desc: '1,000 Loom Workers' },
        { type: 'scylla', x: 340, y: 70, title: 'Database Sink', desc: '50k CDR/s Batched' }
      ],
      ch6: [
        { type: 'kafka', x: 30, y: 70, title: 'Kafka Ingress', desc: '45k TPS Telemetry' },
        { type: 'flink', x: 180, y: 70, title: 'Flink CEP', desc: 'RocksDB State NVMe' },
        { type: 'scylla', x: 340, y: 70, title: '2PC Sink', desc: 'Alerts < 100ms' }
      ],
      ch7: [
        { type: 'gateway', x: 30, y: 70, title: 'Diameter CCR', desc: 'Rating Group Ingress' },
        { type: 'pod', x: 180, y: 70, title: 'Radix Tree DAG', desc: 'Lock-Free Radix Tree' },
        { type: 'redis', x: 340, y: 70, title: 'Token Bucket', desc: 'Reserve Quota < 1.2ms' }
      ],
      ch8: [
        { type: 'pod', x: 30, y: 70, title: 'gNodeB Base', desc: 'N3 GTP-U Radio' },
        { type: 'gateway', x: 180, y: 70, title: 'UPF Fastpath', desc: 'DPDK Forward < 50µs' },
        { type: 'pod', x: 340, y: 70, title: '5G SBA Core', desc: 'HTTP/2 JSON Mesh' }
      ],
      ch9: [
        { type: 'scylla', x: 30, y: 70, title: 'DC1: US-East', desc: 'LOCAL_QUORUM (2/3)' },
        { type: 'pod', x: 180, y: 70, title: 'Gossip Ring', desc: 'Murmur3 Cross-DC' },
        { type: 'scylla', x: 340, y: 70, title: 'DC2: EU-Central', desc: 'LOCAL_QUORUM (2/3)' }
      ],
      ch10: [
        { type: 'pod', x: 30, y: 70, title: 'Global ACID Tx', desc: 'External Consistency' },
        { type: 'pod', x: 180, y: 70, title: 'TrueTime Engine', desc: 'GPS + Atomic ε < 7ms' },
        { type: 'postgres', x: 340, y: 70, title: 'Spanner 2PC', desc: 'Multi-Paxos Tablets' }
      ],
      ch11: [
        { type: 'gateway', x: 30, y: 70, title: 'Burst Ingress', desc: '250k QPS Wire Spike' },
        { type: 'redis', x: 180, y: 70, title: 'GCRA Lua Sentry', desc: 'TAT Microsecond Rate' },
        { type: 'pod', x: 340, y: 70, title: 'Vegas Limiter', desc: 'Adaptive Concurrency' }
      ],
      ch12: [
        { type: 'pod', x: 30, y: 70, title: 'Dual Writer', desc: 'Oracle Sync + Kafka' },
        { type: 'pod', x: 180, y: 70, title: 'Parity Sentry', desc: '14-Day Dark Replay' },
        { type: 'scylla', x: 340, y: 70, title: 'Promoted Primary', desc: '1-Sec DNS Cutover' }
      ]
    };

    function openWhiteboardModal() {
      wbActiveCanvasId = 'modal-whiteboard-canvas';
      document.getElementById('whiteboard-modal').classList.remove('hidden');
      setTimeout(() => initWhiteboardEngine('modal-whiteboard-canvas', 'modal-whiteboard-nodes'), 50);
    }

    function closeWhiteboardModal() {
      document.getElementById('whiteboard-modal').classList.add('hidden');
    }

    function toggleSplitStudio() {
      splitStudioOpen = !splitStudioOpen;
      const panel = document.getElementById('split-studio-panel');
      const btn = document.getElementById('btn-split-toggle');
      if (panel) {
        panel.classList.toggle('hidden', !splitStudioOpen);
        if (splitStudioOpen) {
          wbActiveCanvasId = 'split-canvas';
          btn.className = 'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-600 text-white transition-all shadow';
          setTimeout(() => initWhiteboardEngine('split-canvas', 'split-nodes'), 50);
        } else {
          btn.className = 'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 transition-all shadow';
        }
      }
    }

    function openSplitStudioWithTopology(chId) {
      if (!splitStudioOpen) toggleSplitStudio();
      setTimeout(() => loadReferenceTopologyToWhiteboard(chId), 100);
    }

    function loadActiveModuleTopologyToSplit() {
      loadReferenceTopologyToWhiteboard(`ch${activeStage}`);
    }

    function loadActiveModuleTopologyToWhiteboard() {
      loadReferenceTopologyToWhiteboard(`ch${activeStage}`);
    }

    function initWhiteboardEngine(canvasId, nodesContainerId) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const rect = canvas.parentElement.getBoundingClientRect();
      
      canvas.width = rect.width;
      canvas.height = rect.height;
      drawBlueprintGrid(ctx, canvas.width, canvas.height);

      // Event listeners for drawing
      let snapshot = null;

      canvas.onmousedown = (e) => {
        wbIsDrawing = true;
        const cRect = canvas.getBoundingClientRect();
        wbStartX = e.clientX - cRect.left;
        wbStartY = e.clientY - cRect.top;
        ctx.strokeStyle = wbCurrentColor;
        ctx.fillStyle = wbCurrentColor;
        ctx.lineWidth = wbCurrentWidth;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);

        if (wbCurrentTool === 'pen') {
          ctx.beginPath();
          ctx.moveTo(wbStartX, wbStartY);
        }
      };

      canvas.onmousemove = (e) => {
        if (!wbIsDrawing) return;
        const cRect = canvas.getBoundingClientRect();
        const currX = e.clientX - cRect.left;
        const currY = e.clientY - cRect.top;

        if (wbCurrentTool === 'pen') {
          ctx.lineTo(currX, currY);
          ctx.stroke();
        } else if (wbCurrentTool === 'arrow') {
          ctx.putImageData(snapshot, 0, 0);
          drawArrow(ctx, wbStartX, wbStartY, currX, currY, wbCurrentColor, wbCurrentWidth);
        } else if (wbCurrentTool === 'rect') {
          ctx.putImageData(snapshot, 0, 0);
          ctx.strokeRect(wbStartX, wbStartY, currX - wbStartX, currY - wbStartY);
        } else if (wbCurrentTool === 'circle') {
          ctx.putImageData(snapshot, 0, 0);
          const rx = Math.abs(currX - wbStartX) / 2;
          const ry = Math.abs(currY - wbStartY) / 2;
          ctx.beginPath();
          ctx.ellipse((wbStartX + currX) / 2, (wbStartY + currY) / 2, rx, ry, 0, 0, 2 * Math.PI);
          ctx.stroke();
        } else if (wbCurrentTool === 'eraser') {
          ctx.save();
          ctx.fillStyle = '#030611';
          ctx.beginPath();
          ctx.arc(currX, currY, 16, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }
      };

      const finishDrawing = () => {
        if (wbIsDrawing) {
          wbIsDrawing = false;
          snapshot = null;
        }
      };

      canvas.onmouseup = finishDrawing;
      canvas.onmouseleave = finishDrawing;
    }

    function drawBlueprintGrid(ctx, w, h) {
      ctx.fillStyle = '#030611';
      ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 0.8;
      for (let x = 0; x < w; x += 30) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
      }
      for (let y = 0; y < h; y += 30) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }
    }

    function drawArrow(ctx, fromx, fromy, tox, toy, color, width) {
      const headlen = 10;
      const angle = Math.atan2(toy - fromy, tox - fromx);
      ctx.save();
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = width;
      ctx.beginPath();
      ctx.moveTo(fromx, fromy);
      ctx.lineTo(tox, toy);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(tox, toy);
      ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
      ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }

    function setWbTool(tool) {
      wbCurrentTool = tool;
      document.querySelectorAll('.wb-tool').forEach(btn => btn.classList.remove('active', 'bg-slate-800', 'text-white'));
      const activeBtns = document.querySelectorAll(`[id$="tool-${tool}"]`);
      activeBtns.forEach(btn => btn.classList.add('active', 'bg-slate-800', 'text-white'));
      showToast(`Tool: ${tool.toUpperCase()}`);
    }

    function setWbColor(color) {
      wbCurrentColor = color;
      showToast(`Drawing Color: ${color}`);
    }

    // Creating Draggable Stencil DOM Elements with 1-Click Delete [X]
    function addStencil(stType, x, y, customTitle, customDesc) {
      const targetContainerId = (wbActiveCanvasId === 'modal-whiteboard-canvas') ? 'modal-whiteboard-nodes' : 'split-nodes';
      const container = document.getElementById(targetContainerId);
      if (!container) return;

      const posX = x !== undefined ? x : 40 + Math.floor(Math.random() * 120);
      const posY = y !== undefined ? y : 50 + Math.floor(Math.random() * 100);

      const cfg = STENCIL_CONFIGS[stType] || STENCIL_CONFIGS.pod;
      const nodeId = 'st-node-' + Date.now() + '-' + Math.floor(Math.random() * 1000);

      const el = document.createElement('div');
      el.id = nodeId;
      el.className = `absolute cursor-move select-none p-2.5 rounded-xl border backdrop-blur-md shadow-xl flex flex-col gap-1 w-44 pointer-events-auto transition-shadow hover:shadow-cyan-500/20 ${cfg.color}`;
      el.style.left = `${posX}px`;
      el.style.top = `${posY}px`;
      el.style.zIndex = '20';

      el.innerHTML = `
        <div class="flex items-center justify-between pb-1 border-b border-white/10">
          <div class="flex items-center gap-1.5 truncate">
            <span class="text-sm">${cfg.icon}</span>
            <span class="font-bold text-[11px] truncate text-white">${customTitle || cfg.title}</span>
          </div>
          <div class="flex items-center gap-1">
            <button onclick="duplicateStencil('${targetContainerId}', '${nodeId}')" class="w-4 h-4 rounded hover:bg-white/20 text-slate-300 flex items-center justify-center text-[10px]" title="Duplicate">📋</button>
            <button onclick="removeStencil('${nodeId}')" class="w-4 h-4 rounded bg-rose-900/80 hover:bg-rose-600 text-white flex items-center justify-center text-[11px] font-bold" title="Delete stencil">✕</button>
          </div>
        </div>
        <div class="text-[9px] opacity-80 font-mono truncate">${customDesc || cfg.role}</div>
        <div class="flex justify-between items-center pt-1 text-[8px] opacity-60 font-mono">
          <span>● in</span>
          <span>out ●</span>
        </div>
      `;

      // Draggable logic
      let isDragging = false;
      let startMouseX = 0, startMouseY = 0;
      let startElemLeft = 0, startElemTop = 0;

      el.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        isDragging = true;
        startMouseX = e.clientX;
        startMouseY = e.clientY;
        startElemLeft = parseInt(el.style.left, 10) || 0;
        startElemTop = parseInt(el.style.top, 10) || 0;
        el.style.zIndex = '50';
        e.stopPropagation();
      });

      const onMouseMove = (e) => {
        if (!isDragging) return;
        const dx = e.clientX - startMouseX;
        const dy = e.clientY - startMouseY;
        const containerRect = container.getBoundingClientRect();
        let newX = startElemLeft + dx;
        let newY = startElemTop + dy;
        newX = Math.max(5, Math.min(newX, containerRect.width - el.offsetWidth - 5));
        newY = Math.max(5, Math.min(newY, containerRect.height - el.offsetHeight - 5));
        el.style.left = `${newX}px`;
        el.style.top = `${newY}px`;
      };

      const onMouseUp = () => {
        if (isDragging) {
          isDragging = false;
          el.style.zIndex = '20';
        }
      };

      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);

      container.appendChild(el);
      showToast(`Added ${customTitle || cfg.title} stencil!`);
      return el;
    }

    function removeStencil(nodeId) {
      const el = document.getElementById(nodeId);
      if (el) {
        el.remove();
        showToast('Stencil removed with [✕] button!');
      }
    }

    function duplicateStencil(containerId, nodeId) {
      const el = document.getElementById(nodeId);
      if (!el) return;
      const left = (parseInt(el.style.left, 10) || 40) + 20;
      const top = (parseInt(el.style.top, 10) || 40) + 20;
      const title = el.querySelector('strong, span.font-bold')?.innerText || 'Component';
      addStencil('pod', left, top, `${title} (Copy)`, 'Duplicated Node');
    }

    function clearWhiteboard() {
      ['split-canvas', 'modal-whiteboard-canvas'].forEach(cId => {
        const c = document.getElementById(cId);
        if (c) {
          const ctx = c.getContext('2d');
          drawBlueprintGrid(ctx, c.width, c.height);
        }
      });
      ['split-nodes', 'modal-whiteboard-nodes'].forEach(nId => {
        const n = document.getElementById(nId);
        if (n) n.innerHTML = '';
      });
      showToast('Canvas Cleared! All stencils & drawings wiped.');
    }

    function undoWhiteboard() {
      const targetContainerId = (wbActiveCanvasId === 'modal-whiteboard-canvas') ? 'modal-whiteboard-nodes' : 'split-nodes';
      const container = document.getElementById(targetContainerId);
      if (container && container.lastElementChild) {
        container.lastElementChild.remove();
        showToast('Undo: Removed last stencil.');
      } else {
        showToast('Undo: Canvas history cleared.');
      }
    }

    function exportWhiteboardPng() {
      const cId = wbActiveCanvasId || 'split-canvas';
      const canvas = document.getElementById(cId);
      if (!canvas) return;

      const link = document.createElement('a');
      link.download = `Google_L6_Architecture_${Date.now()}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      showToast('Exported diagram as PNG (+25 XP)!');
      addXP(25, 'Exported Architecture PNG');
    }

    function loadReferenceTopologyToWhiteboard(chId) {
      const presets = MODULE_STENCIL_PRESETS[chId] || MODULE_STENCIL_PRESETS.ch1;
      const targetContainerId = (wbActiveCanvasId === 'modal-whiteboard-canvas') ? 'modal-whiteboard-nodes' : 'split-nodes';
      const container = document.getElementById(targetContainerId);
      if (container) container.innerHTML = '';

      presets.forEach(p => {
        addStencil(p.type, p.x, p.y, p.title, p.desc);
      });

      // Also draw connection arrows on the canvas
      const canvas = document.getElementById(wbActiveCanvasId);
      if (canvas) {
        const ctx = canvas.getContext('2d');
        setTimeout(() => {
          for (let i = 0; i < presets.length - 1; i++) {
            const p1 = presets[i];
            const p2 = presets[i+1];
            drawArrow(ctx, p1.x + 140, p1.y + 30, p2.x + 10, p2.y + 30, '#00f0ff', 2);
          }
        }, 100);
      }

      showToast(`Loaded Canonical Reference Topology for ${chId.toUpperCase()}!`);
      addXP(25, 'Loaded Reference Topology');
    }

    function verifyArchitectureScore() {
      openArchVerifyModal();
      addXP(50, 'Verified Architecture Diagram');
    }

    function openArchVerifyModal() {
      document.getElementById('arch-verify-modal').classList.remove('hidden');
    }

    function closeArchVerifyModal() {
      document.getElementById('arch-verify-modal').classList.add('hidden');
    }

    // ==================== GAMIFICATION & STREAK FUNCTIONS ====================
    function claimDailyBonus() {
      addXP(50, 'Claimed Daily Practice Bonus');
      const btn = document.getElementById('btn-claim-bonus');
      if (btn) {
        btn.disabled = true;
        btn.innerText = 'Bonus Claimed! ⭐';
        btn.className = 'px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 font-mono text-xs cursor-not-allowed';
      }
      showToast('Daily Practice Bonus Claimed! +50 XP ⭐');
    }

    function updateStreakDisplay() {
      const s = appState.streak || 0;
      const countEl = document.getElementById('modal-streak-count');
      const streakNavEl = document.getElementById('streak-display');
      if (countEl) countEl.innerText = `${s} DAYS`;
      if (streakNavEl) streakNavEl.innerText = `${s}-Day Streak`;
    }

    function logDailyCheckIn() {
      appState.streak = (appState.streak || 0) + 1;
      saveState();
      updateStreakDisplay();

      const cell = document.getElementById('streak-cell-today');
      const btn = document.getElementById('btn-checkin');

      if (cell) {
        cell.className = 'p-2 rounded bg-emerald-500 text-white font-bold';
        cell.innerText = `D${appState.streak} ✔`;
      }
      if (btn) {
        btn.disabled = true;
        btn.innerText = 'Today Checked In! 🔥';
        btn.className = 'px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 font-mono text-xs cursor-not-allowed';
      }

      addXP(50, 'Logged Daily Study Check-in');
      showToast(`🔥 ${appState.streak}-Day Streak Logged! Candidate Consistency (+50 XP)`);
    }

    // ==================== CANDIDATE STUDY TOOLS & EXPORT ENGINE ====================
    function exportAllStudyNotes() {
      let md = `# Nexus Architect: Google Staff & Principal Systems Engineering Playbook\n\n`;
      md += `Candidate Study Notes & Architectural Syntheses\nGenerated: ${new Date().toLocaleDateString()}\nTotal XP: ${appState.xp || 0} | Streak: ${appState.streak || 0} Days\n\n---\n\n`;
      
      if (Array.isArray(modulesMeta)) {
        modulesMeta.forEach(m => {
          const chNotes = (appState.notes && appState.notes[m.id]) || '';
          const status = (appState.mastery && appState.mastery[m.id]) || 'learning';
          md += `## Chapter ${m.num}: ${m.title} (${m.subtitle})\n`;
          md += `**Mastery Status:** ${status.toUpperCase()}\n\n`;
          md += `### Candidate Synthesis & Production Notes:\n`;
          md += chNotes ? `${chNotes}\n\n` : `_No notes recorded yet._\n\n`;
          md += `---\n\n`;
        });
      }

      const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `Nexus_Google_Staff_Architect_Notes_${Date.now()}.md`;
      a.click();
      showToast('Exported Candidate Prep Book (.md) (+25 XP)!');
      addXP(25, 'Exported Prep Book');
    }

    function copyCode(btn, codeId) {
      const el = document.getElementById(codeId);
      if (!el) return;
      const text = el.innerText;
      navigator.clipboard.writeText(text).then(() => {
        const oldText = btn.innerHTML;
        btn.innerHTML = '<span>✔</span> Copied!';
        btn.classList.add('text-emerald-400');
        setTimeout(() => {
          btn.innerHTML = oldText;
          btn.classList.remove('text-emerald-400');
        }, 2000);
        showToast('Code copied to clipboard!');
      }).catch(() => {
        showToast('Code copied to clipboard.');
      });
    }

    let ambushInterval = null;
    function startAmbushPressureTimer(trapId) {
      const parts = trapId.split('_');
      const chId = parts[0];
      const tIdx = parseInt(parts[1], 10);
      
      const m = modulesMeta.find(item => item.id === chId);
      const trap = (m && m.traps && m.traps[tIdx]) ? m.traps[tIdx] : null;
      
      if (trap) {
        const qEl = document.getElementById('trap-modal-question');
        const optEl = document.getElementById('trap-modal-options');
        const timerEl = document.getElementById('trap-drill-timer');
        const fbEl = document.getElementById('trap-modal-feedback');
        
        if (fbEl) fbEl.classList.add('hidden');
        if (qEl) qEl.innerHTML = `<strong>${trap.title}:</strong><br><br>"${trap.scenario}"`;
        
        if (optEl) {
          optEl.innerHTML = `
            <div class="space-y-2">
              <button onclick="revealAmbushSolution('${trapId}')" class="w-full text-left p-3 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-500 text-xs text-white">
                🎙️ Formulate your answer out loud (60 seconds), then click here to evaluate Google Staff defense script.
              </button>
            </div>
          `;
        }
        
        let left = 60;
        if (timerEl) timerEl.innerText = `${left}s`;
        clearInterval(ambushInterval);
        ambushInterval = setInterval(() => {
          left--;
          if (timerEl) timerEl.innerText = `${left}s`;
          if (left <= 0) {
            clearInterval(ambushInterval);
            showToast('Time up on 60s ambush drill!');
            revealAmbushSolution(trapId);
          }
        }, 1000);
        
        document.getElementById('trap-modal').classList.remove('hidden');
      } else {
        showToast('Starting 60s Pressure Recall Drill!');
      }
    }

    function revealAmbushSolution(trapId) {
      clearInterval(ambushInterval);
      const parts = trapId.split('_');
      const chId = parts[0];
      const tIdx = parseInt(parts[1], 10);
      const m = modulesMeta.find(item => item.id === chId);
      const trap = (m && m.traps && m.traps[tIdx]) ? m.traps[tIdx] : null;
      const fbEl = document.getElementById('trap-modal-feedback');
      
      if (trap && fbEl) {
        fbEl.classList.remove('hidden');
        fbEl.className = 'p-3 rounded-lg text-xs font-mono bg-emerald-950/70 border border-emerald-700 text-emerald-300 space-y-1.5';
        fbEl.innerHTML = `
          <strong class="block text-emerald-400">Google Staff L6 Defense:</strong>
          <p class="text-white">${trap.l8_mitigation}</p>
          <div class="p-2 bg-slate-950 rounded text-emerald-200 mt-1">"${trap.defense_script}"</div>
        `;
        addXP(50, 'Completed L6 Ambush Drill');
      }
    }

    function flipModuleCard(cardId) {
      const card = document.getElementById(cardId);
      if (card) {
        card.classList.toggle('flipped');
      }
    }

    function rateModuleCard(chId, cardIdx, rating) {
      if (!appState.recall) appState.recall = {};
      if (!appState.recall[chId]) appState.recall[chId] = {};
      appState.recall[chId][cardIdx] = rating;
      saveState();
      
      const xpReward = rating === 'easy' ? 20 : (rating === 'good' ? 15 : 10);
      addXP(xpReward, `Active Recall Drill (${rating.toUpperCase()})`);
      showToast(`Rated ${rating.toUpperCase()}! Next spaced interval scheduled.`);
    }

    let pitchRecorders = {};
    let pitchMediaRecorders = {};
    let pitchIntervals = {};
    let pitchSecs = {};

    async function togglePitchRecording(chId) {
      const btn = document.getElementById(`${chId}-btn-record`);
      const statusEl = document.getElementById(`${chId}-record-status`);
      const timerEl = document.getElementById(`${chId}-record-timer`);
      const audioPlayback = document.getElementById(`${chId}-audio-playback`);

      if (pitchRecorders[chId]) {
        clearInterval(pitchIntervals[chId]);
        pitchRecorders[chId] = false;
        if (pitchMediaRecorders[chId] && pitchMediaRecorders[chId].state !== 'inactive') {
          pitchMediaRecorders[chId].stop();
        }
        if (btn) {
          btn.innerHTML = '<span>🎙️</span> Record 2-Min Pitch';
          btn.className = 'px-3 py-1.5 rounded-lg bg-rose-950 text-rose-300 border border-rose-800 hover:bg-rose-900 font-semibold text-xs flex items-center gap-1.5 shadow';
        }
        if (statusEl) statusEl.innerText = 'Pitch Recorded! Ready for Playback.';
        addXP(50, 'Recorded 2-Minute Architecture Pitch');
        showToast('2-Minute Architecture Pitch Recorded (+50 XP)!');
      } else {
        pitchSecs[chId] = 120;
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          const mediaRecorder = new MediaRecorder(stream);
          let audioChunks = [];

          mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
          mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            if (audioPlayback) {
              audioPlayback.src = URL.createObjectURL(audioBlob);
              audioPlayback.classList.remove('hidden');
            }
            stream.getTracks().forEach(track => track.stop());
          };

          mediaRecorder.start();
          pitchMediaRecorders[chId] = mediaRecorder;
          pitchRecorders[chId] = true;

          if (btn) {
            btn.innerHTML = '<span>⏹️</span> Stop Recording';
            btn.className = 'px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-semibold text-xs flex items-center gap-1.5 animate-pulse shadow';
          }
          if (statusEl) statusEl.innerText = '● RECORDING LIVE (Microphone Active)...';

          clearInterval(pitchIntervals[chId]);
          pitchIntervals[chId] = setInterval(() => {
            if (pitchSecs[chId] > 0) {
              pitchSecs[chId]--;
              const m = Math.floor(pitchSecs[chId] / 60);
              const s = pitchSecs[chId] % 60;
              if (timerEl) timerEl.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            } else {
              togglePitchRecording(chId);
            }
          }, 1000);

          showToast('Microphone live! Delivering 2-min oral defense pitch.');
        } catch(err) {
          pitchRecorders[chId] = true;
          if (btn) {
            btn.innerHTML = '<span>⏹️</span> Stop Pitch Drill';
            btn.className = 'px-3 py-1.5 rounded-lg bg-amber-600 text-white font-semibold text-xs flex items-center gap-1.5 animate-pulse shadow';
          }
          if (statusEl) statusEl.innerText = '● LIVE DRILL TIMER (Speak aloud)...';
          clearInterval(pitchIntervals[chId]);
          pitchIntervals[chId] = setInterval(() => {
            if (pitchSecs[chId] > 0) {
              pitchSecs[chId]--;
              const m = Math.floor(pitchSecs[chId] / 60);
              const s = pitchSecs[chId] % 60;
              if (timerEl) timerEl.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            } else {
              togglePitchRecording(chId);
            }
          }, 1000);
          showToast('Voice drill timer started! Formulate your pitch.');
        }
      }
    }

    function insertNoteTemplate(chId, templateType) {
      const ta = document.getElementById(`${chId}-notes-textarea`);
      if (!ta) return;
      let text = '';
      if (templateType === 'star') {
        text = `\n\n### Google Staff STAR Interview Story\n- **Situation:** \n- **Task:** \n- **Action (First-Principles & Technical Depth):** \n- **Result (Quantitative Metrics & Scalability):** \n`;
      } else if (templateType === 'tradeoff') {
        text = `\n\n### Architectural Trade-off Evaluation\n- **Option A:** \n- **Option B:** \n- **Google Staff Recommendation & Failure Domains:** \n`;
      } else {
        text = `\n\n### Production War Story & Post-Mortem Notes\n- **Incident:** \n- **Kernel / System Bottleneck:** \n- **Mitigation & Invariant Guardrail:** \n`;
      }
      ta.value += text;
      saveModuleNotes(chId);
      showToast(`Inserted ${templateType.toUpperCase()} notes template!`);
    }

    function saveModuleNotes(chId) {
      const ta = document.getElementById(`${chId}-notes-textarea`);
      if (!ta) return;
      if (!appState.notes) appState.notes = {};
      appState.notes[chId] = ta.value;
      saveState();
    }

    let examScores = {};
    function checkExamAnswer(qNum, opt) {
      const fb = document.getElementById(`q${qNum}-feedback`);
      if (!fb) return;
      fb.classList.remove('hidden');

      if (opt === 'B') {
        examScores[qNum] = 100;
        fb.className = 'p-3 rounded-lg text-[11px] font-mono mt-2 bg-emerald-950/80 border border-emerald-600 text-emerald-300';
        fb.innerHTML = '<strong>✅ Correct (Google L6/L8 Staff Response):</strong> Monotonic 64-bit fencing tokens enforced as storage engine precondition (UPDATE ... WHERE token &gt; last_committed) eliminate zombie writes during split-brain failover, stop-the-world JVM GC pauses, and asynchronous replica promotion without relying on synchronized clocks (+50 XP).';
        addXP(50, 'Correct Bar-Raiser Exam Response');
      } else {
        examScores[qNum] = 0;
        fb.className = 'p-3 rounded-lg text-[11px] font-mono mt-2 bg-rose-950/80 border border-rose-600 text-rose-300';
        fb.innerHTML = '<strong>❌ Rejection Fallacy (Junior / L5 Mistake):</strong> Redis distributed locks with TTL or retry loops fail under network partitions or JVM stop-the-world GC pauses (>15s) because the lease expires while the worker is paused. You MUST use monotonic fencing tokens verified at the storage barrier.';
      }

      const scoreEl = document.getElementById('exam-score');
      if (scoreEl) {
        const scores = Object.values(examScores);
        const avg = Math.round(scores.reduce((a, b) => a + b, 0) / Math.max(1, scores.length));
        scoreEl.innerText = `Score: ${avg} / 100`;
      }
    }

    // ==================== ADVANCED FOCUS AUDIO & ZEN MODE ====================
    let audioVolume = 0.3;
    let masterGainNode = null;
    let activeOscillators = [];

    function stopAmbientNoise() {
      if (activeOscillators) {
        activeOscillators.forEach(o => {
          try { o.stop(); } catch(e) {}
        });
        activeOscillators = [];
      }
      if (noiseNode) {
        try { noiseNode.stop(); } catch(e) {}
        noiseNode = null;
      }
      document.querySelectorAll('[id^="btn-sound-"]').forEach(btn => {
        btn.classList.remove('border-cyan-500', 'bg-cyan-950/60', 'text-cyan-300');
        btn.classList.add('border-slate-800', 'bg-slate-950', 'text-slate-300');
      });
      showToast('Ambient noise stopped.');
    }

    function setAudioVolume(val) {
      audioVolume = val / 100;
      if (masterGainNode) masterGainNode.gain.value = audioVolume;
    }

    function toggleAmbientNoise(type) {
      stopAmbientNoise();

      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();

      masterGainNode = audioCtx.createGain();
      masterGainNode.gain.value = audioVolume;
      masterGainNode.connect(audioCtx.destination);

      const btn = document.getElementById(`btn-sound-${type}`);
      if (btn) {
        btn.classList.add('border-cyan-500', 'bg-cyan-950/60', 'text-cyan-300');
        btn.classList.remove('border-slate-800', 'bg-slate-950', 'text-slate-300');
      }

      if (type === 'server') {
        // Datacenter Server Drone: 60Hz and 120Hz sine with resonant lowpass filter
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const filter = audioCtx.createBiquadFilter();
        
        osc1.type = 'sawtooth';
        osc1.frequency.value = 60;
        osc2.type = 'sine';
        osc2.frequency.value = 120;
        
        filter.type = 'lowpass';
        filter.frequency.value = 160;
        filter.Q.value = 2;

        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(masterGainNode);

        osc1.start();
        osc2.start();
        activeOscillators.push(osc1, osc2);
        showToast('Datacenter Server Drone running 🖥️');
      } else if (type === 'binaural') {
        // Alpha 10Hz Binaural Beats: 200Hz Left, 210Hz Right
        const oscL = audioCtx.createOscillator();
        const oscR = audioCtx.createOscillator();
        const pannerL = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;
        const pannerR = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;

        oscL.frequency.value = 200;
        oscR.frequency.value = 210;

        if (pannerL && pannerR) {
          pannerL.pan.value = -1;
          pannerR.pan.value = 1;
          oscL.connect(pannerL); pannerL.connect(masterGainNode);
          oscR.connect(pannerR); pannerR.connect(masterGainNode);
        } else {
          oscL.connect(masterGainNode);
          oscR.connect(masterGainNode);
        }

        oscL.start();
        oscR.start();
        activeOscillators.push(oscL, oscR);
        showToast('10Hz Alpha Waves binaural beats active 🧠');
      } else {
        // White / Brown buffer noise
        const bufferSize = audioCtx.sampleRate * 2;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        let lastOut = 0.0;

        for (let i = 0; i < bufferSize; i++) {
          if (type === 'brown') {
            const white = Math.random() * 2 - 1;
            data[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = data[i];
            data[i] *= 3.5;
          } else {
            data[i] = Math.random() * 0.15 - 0.075;
          }
        }

        noiseNode = audioCtx.createBufferSource();
        noiseNode.buffer = buffer;
        noiseNode.loop = true;
        noiseNode.connect(masterGainNode);
        noiseNode.start();
        showToast(`Playing ${type} acoustic noise 🌊`);
      }
    }

    function toggleZenMode() {
      document.body.classList.toggle('zen-mode');
      closeFocusCockpitModal();
      const isZen = document.body.classList.contains('zen-mode');
      showToast(isZen ? '🧘 Zen Immersion Mode ON' : 'Zen Mode OFF');
    }

    // ==================== SURPRISE AMBUSH DRILL ====================
    let trapCountdown = null;
    function triggerRandomTrapQuestion() {
      const modal = document.getElementById('trap-modal');
      const qEl = document.getElementById('trap-modal-question');
      const optEl = document.getElementById('trap-modal-options');
      const fb = document.getElementById('trap-modal-feedback');
      fb.classList.add('hidden');

      qEl.innerText = "Interviewer: 'You deployed a 45k TPS Kafka consumer cluster. During rolling deployment of 50 pods, consumer traffic halts completely for 15 minutes nationwide. Why and how do you fix it?'";
      optEl.innerHTML = `
        <button onclick="checkTrapChoice('A')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800">A) Increase consumer memory heap from 4GB to 32GB to avoid OOM crashes.</button>
        <button onclick="checkTrapChoice('B')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800">B) Migrate from Eager Rebalance Assignor to CooperativeStickyAssignor to reassign partitions incrementally without stopping traffic.</button>
        <button onclick="checkTrapChoice('C')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800">C) Reduce partition count from 128 to 16 so rebalances happen faster.</button>
      `;

      let sec = 60;
      document.getElementById('trap-drill-timer').innerText = `${sec}s`;
      clearInterval(trapCountdown);
      trapCountdown = setInterval(() => {
        sec--;
        document.getElementById('trap-drill-timer').innerText = `${sec}s`;
        if (sec <= 0) clearInterval(trapCountdown);
      }, 1000);

      modal.classList.remove('hidden');
    }

    function checkTrapChoice(choice) {
      clearInterval(trapCountdown);
      const fb = document.getElementById('trap-modal-feedback');
      if (choice === 'B') {
        fb.className = 'p-3 rounded-lg text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono';
        fb.innerHTML = '✔ CORRECT (Google Staff Choice): Eager rebalance revokes all partitions on any membership change. Cooperative Sticky performs incremental reassignment, allowing 95%+ consumers to stream uninterrupted.';
        addXP(100, 'Solved Ambush Drill');
      } else {
        fb.className = 'p-3 rounded-lg text-xs bg-rose-950 text-rose-300 border border-rose-800 font-mono';
        fb.innerHTML = '✖ REJECTED (Junior Fallacy): Heap size or fewer partitions does not fix the Eager rebalance protocol flaw.';
      }
      fb.classList.remove('hidden');
    }

    function closeTrapModal() {
      clearInterval(trapCountdown);
      document.getElementById('trap-modal').classList.add('hidden');
    }

    
    // ==================== 8 ADVANCED INTERACTIVE SIMULATORS ====================
    
    // --- 1. ZERO-COPY SIMULATOR ---
    let zcMode = 'traditional';
    let zcAnimationId = null;
    let zcPackets = [];

    function setZeroCopyMode(m) {
      zcMode = m;
      const bTrad = document.getElementById('btn-mode-trad');
      const bZero = document.getElementById('btn-mode-zero');
      const sCopies = document.getElementById('zc-stat-cpu-copies');
      const sSwitches = document.getElementById('zc-stat-switches');
      const sHeap = document.getElementById('zc-stat-heap');
      const sTps = document.getElementById('zc-stat-tps');

      if (m === 'zerocopy') {
        bZero.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-cyan-600 text-white shadow';
        bTrad.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800';
        sCopies.innerText = '0 CPU Copies (Direct DMA)';
        sCopies.className = 'font-bold text-emerald-400 text-sm';
        sSwitches.innerText = '2 Switches (Syscall only)';
        sSwitches.className = 'font-bold text-emerald-400 text-sm';
        sHeap.innerText = '0 MB/s (Bypasses Heap)';
        sHeap.className = 'font-bold text-emerald-400 text-sm';
        sTps.innerText = '45,000 TPS';
        sTps.className = 'font-bold text-emerald-400 text-sm';
        showToast('Switched to Zero-Copy sendfile() bypass! Zero CPU memory copies.');
        addXP(25, 'Tested Zero-Copy Kernel Simulator');
      } else {
        bTrad.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-rose-950 text-rose-300 border border-rose-800 shadow';
        bZero.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800';
        sCopies.innerText = '2 Copies (User/Kernel)';
        sCopies.className = 'font-bold text-rose-400 text-sm';
        sSwitches.innerText = '4 Switches';
        sSwitches.className = 'font-bold text-rose-400 text-sm';
        sHeap.innerText = '45 MB/s Young Gen';
        sHeap.className = 'font-bold text-rose-400 text-sm';
        sTps.innerText = '18,500 TPS';
        sTps.className = 'font-bold text-cyan-400 text-sm';
        showToast('Switched to Traditional 4-Copy read()/write() pipeline.');
      }
      initZeroCopyCanvas();
    }

    function initZeroCopyCanvas() {
      const canvas = document.getElementById('zc-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      if (zcAnimationId && typeof cancelAnimationFrame === 'function') cancelAnimationFrame(zcAnimationId);
      zcPackets = [];

      for (let i = 0; i < 6; i++) {
        zcPackets.push({ progress: i * 0.16, speed: 0.006 });
      }

      function renderFrame() {
        ctx.fillStyle = '#020512';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw Nodes
        const nodes = [
          { name: 'NVMe Disk', x: 50, y: 120, color: '#38bdf8' },
          { name: 'Kernel PageCache', x: 220, y: 120, color: '#10b981' },
          { name: 'User-Space JVM Heap', x: 420, y: (zcMode === 'traditional' ? 50 : 50), color: (zcMode === 'traditional' ? '#f43f5e' : '#475569') },
          { name: 'Socket Buffer', x: 620, y: (zcMode === 'traditional' ? 120 : 120), color: (zcMode === 'traditional' ? '#c084fc' : '#475569') },
          { name: 'NIC DMA Ring', x: 820, y: 120, color: '#00f0ff' }
        ];

        nodes.forEach(n => {
          ctx.fillStyle = '#050b1d';
          ctx.strokeStyle = n.color;
          ctx.lineWidth = 1.5;
          if (ctx.roundRect) {
            ctx.roundRect(n.x, n.y - 30, 130, 60, 8);
          } else {
            ctx.rect(n.x, n.y - 30, 130, 60);
          }
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 11px system-ui, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(n.name, n.x + 65, n.y + 5);
        });

        // Connecting paths
        ctx.lineWidth = 2;
        if (zcMode === 'traditional') {
          // Disk -> PageCache -> Heap -> Socket -> NIC
          drawPath(ctx, 180, 120, 220, 120, '#38bdf8');
          drawPath(ctx, 350, 120, 420, 75, '#f43f5e'); // CPU Copy 1
          drawPath(ctx, 550, 75, 620, 120, '#f43f5e'); // CPU Copy 2
          drawPath(ctx, 750, 120, 820, 120, '#00f0ff');
        } else {
          // Zero-Copy sendfile: Disk -> PageCache -> NIC directly!
          drawPath(ctx, 180, 120, 220, 120, '#38bdf8');
          // Direct bypass line across bottom
          ctx.strokeStyle = '#10b981';
          ctx.setLineDash([5, 5]);
          ctx.beginPath();
          ctx.moveTo(350, 120);
          ctx.lineTo(820, 120);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = '#10b981';
          ctx.font = '10px monospace';
          ctx.fillText('⚡ sendfile() Zero-Copy DMA Bypass (0 CPU Copies)', 580, 105);
        }

        // Animate Packets
        zcPackets.forEach(p => {
          p.progress = (p.progress + p.speed) % 1;
          let px = 0, py = 120;
          if (zcMode === 'traditional') {
            if (p.progress < 0.25) {
              px = 115 + (p.progress / 0.25) * 170; py = 120;
            } else if (p.progress < 0.5) {
              const f = (p.progress - 0.25) / 0.25;
              px = 285 + f * 200; py = 120 - f * 45;
            } else if (p.progress < 0.75) {
              const f = (p.progress - 0.5) / 0.25;
              px = 485 + f * 200; py = 75 + f * 45;
            } else {
              const f = (p.progress - 0.75) / 0.25;
              px = 685 + f * 200; py = 120;
            }
          } else {
            px = 115 + p.progress * 770;
            py = 120;
          }

          ctx.fillStyle = (zcMode === 'zerocopy' ? '#00f0ff' : '#f43f5e');
          ctx.beginPath();
          ctx.arc(px, py, 5, 0, Math.PI * 2);
          ctx.fill();
        });

        zcAnimationId = requestAnimationFrame(renderFrame);
      }
      renderFrame();
    }

    function drawPath(ctx, x1, y1, x2, y2, color) {
      ctx.strokeStyle = color;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    // --- 2. RAFT CONSENSUS SIMULATOR ---
    let raftTerm = 1;
    let raftLeader = 1;
    let raftCommitIndex = 104;
    let raftPartitioned = false;
    let raftAnimationId = null;

    function drawRaft() {
      initRaftSim();
    }

    function initRaftSim() {
      const canvas = document.getElementById('raft-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const radius = Math.min(centerX, centerY) - 50;

      let pulse = 0;
      function render() {
        ctx.fillStyle = '#020512';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        pulse = (pulse + 0.05) % (Math.PI * 2);

        // 5 Nodes
        for (let i = 1; i <= 5; i++) {
          const angle = ((i - 1) / 5) * Math.PI * 2 - Math.PI / 2;
          const x = centerX + Math.cos(angle) * radius;
          const y = centerY + Math.sin(angle) * radius;
          const isLeader = (i === raftLeader);
          const isDead = (raftPartitioned && i === 1);

          // Connection lines to leader
          if (!isLeader && !isDead) {
            const lAngle = ((raftLeader - 1) / 5) * Math.PI * 2 - Math.PI / 2;
            const lx = centerX + Math.cos(lAngle) * radius;
            const ly = centerY + Math.sin(lAngle) * radius;

            ctx.strokeStyle = 'rgba(0, 240, 255, 0.2)';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(lx, ly);
            ctx.lineTo(x, y);
            ctx.stroke();

            // Heartbeat particle
            const hx = lx + (x - lx) * ((Math.sin(pulse) + 1) / 2);
            const hy = ly + (y - ly) * ((Math.sin(pulse) + 1) / 2);
            ctx.fillStyle = '#10b981';
            ctx.beginPath();
            ctx.arc(hx, hy, 3.5, 0, Math.PI * 2);
            ctx.fill();
          }

          // Node Circle
          ctx.beginPath();
          ctx.arc(x, y, 26, 0, Math.PI * 2);
          ctx.fillStyle = isDead ? '#450a0a' : (isLeader ? '#451a03' : '#042f2e');
          ctx.fill();
          ctx.strokeStyle = isDead ? '#f43f5e' : (isLeader ? '#f59e0b' : '#10b981');
          ctx.lineWidth = 2.5;
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 11px system-ui';
          ctx.textAlign = 'center';
          ctx.fillText(`Node ${i}`, x, y - 2);

          ctx.font = '9px monospace';
          ctx.fillStyle = isDead ? '#fca5a5' : (isLeader ? '#fbbf24' : '#6ee7b7');
          ctx.fillText(isDead ? 'ISOLATED' : (isLeader ? 'LEADER' : 'FOLLOWER'), x, y + 12);
        }

        raftAnimationId = requestAnimationFrame(render);
      }
      if (raftAnimationId) cancelAnimationFrame(raftAnimationId);
      render();
    }

    function raftPartitionLeader() {
      raftPartitioned = true;
      raftTerm++;
      raftLeader = 2; // Follower 2 becomes new Leader via 3/5 quorum (Nodes 2, 3, 4)
      document.getElementById('raft-term-val').innerText = raftTerm;
      document.getElementById('raft-leader-val').innerText = `Node 2 (Term ${raftTerm})`;
      document.getElementById('raft-log-status').innerHTML = `
        <span class="text-rose-400 font-bold">⚡ Node 1 Partitioned!</span> Followers 2, 3, 4 timed out &amp; elected <strong class="text-amber-400">Node 2 as Leader (Term ${raftTerm})</strong> via 3/5 majority quorum!
      `;
      showToast(`Node 1 isolated! Node 2 elected leader in Term ${raftTerm}`);
      addXP(25, 'Simulated Raft Split-Brain Resolution');
    }

    function raftHealNetwork() {
      raftPartitioned = false;
      document.getElementById('raft-log-status').innerHTML = `
        <span class="text-emerald-400 font-bold">✔ Network Healed!</span> Node 1 rejoined, discovered higher Term ${raftTerm}, and stepped down to Follower.
      `;
      showToast('Network partition healed! Quorum restored.');
    }

    function raftSubmitTx() {
      raftCommitIndex++;
      document.getElementById('raft-commit-val').innerText = raftCommitIndex;
      showToast(`Committed Index #${raftCommitIndex} across majority quorum (+25 XP)!`);
      addXP(25, 'Committed Raft State Machine Write');
    }

    // --- 3. CONSISTENT HASH RING SIMULATOR ---
    let vNodesPerNode = 150;
    let hashNodeCount = 4;

    function setVNodes(v) {
      vNodesPerNode = v;
      document.getElementById('btn-vnode-1').className = (v === 1 ? 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold text-xs' : 'px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs');
      document.getElementById('btn-vnode-50').className = (v === 50 ? 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold text-xs' : 'px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs');
      document.getElementById('btn-vnode-150').className = (v === 150 ? 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold text-xs' : 'px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs');

      document.getElementById('hash-vnode-count').innerText = `${hashNodeCount * vNodesPerNode} Arcs`;
      const stdDev = (v === 1 ? '38.4% (Severe Hot Spots!)' : (v === 50 ? '8.2% (Moderate)' : '< 2.1% (Uniform Distribution)'));
      const devEl = document.getElementById('hash-stddev-val');
      devEl.innerText = stdDev;
      devEl.className = (v === 150 ? 'text-emerald-400 font-bold' : (v === 50 ? 'text-amber-400 font-bold' : 'text-rose-400 font-bold'));

      drawHashRing();
      showToast(`Configured Consistent Hash Ring with V=${v} virtual nodes!`);
    }

    function addHashNode() {
      if (hashNodeCount < 6) {
        hashNodeCount++;
        document.getElementById('hash-node-count').innerText = `${hashNodeCount} Physical Nodes`;
        document.getElementById('hash-vnode-count').innerText = `${hashNodeCount * vNodesPerNode} Arcs`;
        drawHashRing();
        showToast(`Added Node ${String.fromCharCode(64 + hashNodeCount)} to Hash Ring (+25 XP)!`);
        addXP(25, 'Rebalanced Consistent Hash Ring');
      }
    }

    function removeHashNode() {
      if (hashNodeCount > 2) {
        hashNodeCount--;
        document.getElementById('hash-node-count').innerText = `${hashNodeCount} Physical Nodes`;
        document.getElementById('hash-vnode-count').innerText = `${hashNodeCount * vNodesPerNode} Arcs`;
        drawHashRing();
        showToast('Node removed. Only 1/N keys rebalanced without cache outage.');
      }
    }

    function drawHashRing() {
      const canvas = document.getElementById('hash-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const r = Math.min(cx, cy) - 45;

      ctx.fillStyle = '#020512';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw Main Ring
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 14;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();

      const colors = ['#00f0ff', '#10b981', '#c084fc', '#f59e0b', '#f43f5e', '#ec4899'];
      const totalSlices = hashNodeCount * (vNodesPerNode === 1 ? 1 : 16);

      for (let i = 0; i < totalSlices; i++) {
        const start = (i / totalSlices) * Math.PI * 2;
        const end = ((i + 1) / totalSlices) * Math.PI * 2;
        const col = colors[i % hashNodeCount];

        ctx.strokeStyle = col;
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.arc(cx, cy, r, start + 0.02, end - 0.02);
        ctx.stroke();
      }

      // Draw Keys on Ring
      const numKeys = 40;
      for (let k = 0; k < numKeys; k++) {
        const angle = (k * 2654435761 % 1000) / 1000 * Math.PI * 2;
        const kx = cx + Math.cos(angle) * (r - 20);
        const ky = cy + Math.sin(angle) * (r - 20);
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(kx, ky, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`${hashNodeCount} NODES • ${hashNodeCount * vNodesPerNode} V-NODES`, cx, cy - 8);
      ctx.font = '10px monospace';
      ctx.fillStyle = '#38bdf8';
      ctx.fillText('Murmur3 360° Ring Space', cx, cy + 10);
    }

    // --- 4. TOKEN BUCKET & GCRA SIMULATOR ---
    let tbTokens = 45;
    let tbAllowed = 184;
    let tbDropped = 0;

    function injectBurst(count) {
      if (tbTokens >= count) {
        tbTokens -= count;
        tbAllowed += count;
        showToast(`Allowed burst of ${count} requests! Bucket absorbed traffic.`);
      } else {
        const passed = tbTokens;
        const dropped = count - passed;
        tbTokens = 0;
        tbAllowed += passed;
        tbDropped += dropped;
        showToast(`Throttled! ${passed} allowed, ${dropped} dropped (HTTP 429).`);
      }
      updateTokenBucketUI();
      drawTokenBucket();
    }

    function resetTokenBucket() {
      tbTokens = 50;
      tbAllowed = 0;
      tbDropped = 0;
      updateTokenBucketUI();
      drawTokenBucket();
      showToast('Rate limiter stats reset.');
    }

    function updateTokenBucketUI() {
      document.getElementById('tb-tokens-val').innerText = `${tbTokens} / 50 Tokens`;
      document.getElementById('tb-allowed-val').innerText = `${tbAllowed} Requests`;
      document.getElementById('tb-dropped-val').innerText = `${tbDropped} Drops`;
    }

    function drawTokenBucket() {
      const canvas = document.getElementById('tb-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      ctx.fillStyle = '#020512';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const bx = canvas.width / 2 - 60;
      const by = 40;
      const bw = 120;
      const bh = 180;

      // Draw Bucket Tank
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 3;
      ctx.strokeRect(bx, by, bw, bh);

      // Water / Token fill level
      const fillH = (tbTokens / 50) * (bh - 10);
      ctx.fillStyle = 'rgba(0, 240, 255, 0.35)';
      ctx.fillRect(bx + 5, by + bh - fillH - 5, bw - 10, fillH);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`${tbTokens} TOKENS`, bx + bw / 2, by + bh - 20);

      // Inflow Tap
      ctx.fillStyle = '#10b981';
      ctx.fillRect(bx + bw / 2 - 6, by - 25, 12, 20);
      ctx.font = '9px monospace';
      ctx.fillText('Refill +10/s', bx + bw / 2, by - 30);
    }

    // --- 5. MONOTONIC FENCING SIMULATOR ---
    function fencingStep(step) {
      const log = document.getElementById('fence-log-box');
      if (step === 1) {
        log.innerHTML = `<span class="text-cyan-400 font-bold">Step 1:</span> Client 1 acquires lock on key "lock:mo:101". Redis atomic Lua script grants lock with <strong>Token = 101</strong> (TTL = 10s).`;
        showToast('Client 1 acquired lock with Token 101');
      } else if (step === 2) {
        log.innerHTML = `<span class="text-rose-400 font-bold">Step 2:</span> Client 1 enters a 15-second Stop-The-World JVM GC Pause! The 10s Redis lease expires while Client 1 is frozen.`;
        showToast('Client 1 entered 15s GC Pause!');
      } else if (step === 3) {
        log.innerHTML = `<span class="text-amber-400 font-bold">Step 3:</span> Client 2 detects lock expired, acquires lease, and receives strictly monotonic <strong>Token = 102</strong>. Client 2 updates database: <code>UPDATE ... SET val='C2', last_token=102</code>. Committed!`;
        showToast('Client 2 committed write with Token 102!');
      } else if (step === 4) {
        log.innerHTML = `<span class="text-purple-400 font-bold">Step 4 (The Trap):</span> Client 1 wakes from GC pause unaware it expired. It sends zombie write with Token 101. Storage barrier evaluates: <code>WHERE last_token &lt; 101</code> &rarr; <strong>REJECTED! (102 &gt; 101)</strong>. Zero data corruption!`;
        showToast('Database rejected zombie write! 0 Corruptions (+50 XP)');
        addXP(50, 'Mastered Monotonic Fencing Defense');
      }
      drawFencingCanvas(step);
    }

    function fencingReset() {
      document.getElementById('fence-log-box').innerText = 'Step 0: Ready. Click "1. Client 1 Lock (Token 101)" to begin.';
      drawFencingCanvas(0);
      showToast('Fencing simulation reset.');
    }

    function drawFencingCanvas(step) {
      const canvas = document.getElementById('fence-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      ctx.fillStyle = '#020512';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px system-ui';
      ctx.textAlign = 'center';

      // Draw Client 1
      ctx.fillStyle = (step === 2 ? '#450a0a' : (step >= 1 ? '#0e3a5a' : '#0f172a'));
      ctx.strokeStyle = (step === 2 ? '#f43f5e' : '#38bdf8');
      ctx.lineWidth = 2;
      ctx.fillRect(50, 40, 140, 60);
      ctx.strokeRect(50, 40, 140, 60);
      ctx.fillStyle = '#ffffff';
      ctx.fillText('Client 1', 120, 65);
      ctx.font = '9px monospace';
      ctx.fillStyle = (step === 2 ? '#fca5a5' : '#38bdf8');
      ctx.fillText((step === 2 ? '⏳ GC PAUSED' : 'Token: 101'), 120, 85);

      // Draw Client 2
      ctx.fillStyle = (step >= 3 ? '#451a03' : '#0f172a');
      ctx.strokeStyle = (step >= 3 ? '#f59e0b' : '#64748b');
      ctx.fillRect(50, 140, 140, 60);
      ctx.strokeRect(50, 140, 140, 60);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px system-ui';
      ctx.fillText('Client 2', 120, 165);
      ctx.font = '9px monospace';
      ctx.fillStyle = (step >= 3 ? '#fde68a' : '#94a3b8');
      ctx.fillText((step >= 3 ? 'Token: 102 (Active)' : 'Idle'), 120, 185);

      // Draw Database Barrier
      ctx.fillStyle = '#042f2e';
      ctx.strokeStyle = (step === 4 ? '#f43f5e' : '#10b981');
      ctx.lineWidth = 2.5;
      ctx.fillRect(380, 70, 180, 110);
      ctx.strokeRect(380, 70, 180, 110);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px system-ui';
      ctx.fillText('PostgreSQL / ScyllaDB', 470, 105);
      ctx.font = '10px monospace';
      ctx.fillStyle = (step >= 3 ? '#a7f3d0' : '#cbd5e1');
      ctx.fillText(`last_token = ${step >= 3 ? '102' : '100'}`, 470, 130);

      if (step === 4) {
        ctx.fillStyle = '#f43f5e';
        ctx.font = 'bold 11px monospace';
        ctx.fillText('❌ 101 < 102 (REJECTED)', 470, 155);
      }
    }

    // --- 6. TAIL AT SCALE SIMULATOR ---
    let hedgingEnabled = false;
    function toggleHedging(en) {
      hedgingEnabled = en;
      document.getElementById('btn-hedge-off').className = (!en ? 'px-3 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-xs font-semibold' : 'px-3 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-xs');
      document.getElementById('btn-hedge-on').className = (en ? 'px-3 py-1 rounded bg-cyan-600 text-white font-bold text-xs' : 'px-3 py-1 rounded bg-slate-900 text-slate-400 border border-slate-800 text-xs');
      runTailSimulation();
    }

    function runTailSimulation() {
      const p99El = document.getElementById('tail-p99-val');
      const dropEl = document.getElementById('tail-drop-val');
      const ovhEl = document.getElementById('tail-overhead-val');

      if (hedgingEnabled) {
        p99El.innerText = '16 ms (Hedged at 15ms)';
        p99El.className = 'font-bold text-emerald-400 text-sm';
        dropEl.innerText = '96.4% Latency Drop!';
        dropEl.className = 'font-bold text-emerald-400 text-sm';
        ovhEl.innerText = '2.1% Extra RPCs';
        showToast('Tail Latency reduced by 96.4% via Hedged Requests (+25 XP)!');
        addXP(25, 'Demonstrated Tail at Scale Hedging');
      } else {
        p99El.innerText = '452 ms (Blocked by S7)';
        p99El.className = 'font-bold text-rose-400 text-sm';
        dropEl.innerText = '0% (Unmitigated)';
        dropEl.className = 'font-bold text-rose-400 text-sm';
        ovhEl.innerText = '0.0%';
        showToast('Slow Server 7 created 452ms tail latency spike!');
      }
      drawTailCanvas();
    }

    function drawTailCanvas() {
      const canvas = document.getElementById('tail-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      ctx.fillStyle = '#020512';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const latencies = [12, 14, 11, 15, 9, 13, (hedgingEnabled ? 16 : 452), 10, 14, 12];
      const maxW = canvas.width - 150;

      for (let i = 0; i < 10; i++) {
        const y = 30 + i * 22;
        ctx.fillStyle = '#94a3b8';
        ctx.font = '10px monospace';
        ctx.textAlign = 'left';
        ctx.fillText(`Server ${i+1}:`, 20, y + 10);

        const w = (latencies[i] / 500) * maxW;
        ctx.fillStyle = (i === 6 && !hedgingEnabled ? '#f43f5e' : (i === 6 ? '#00f0ff' : '#10b981'));
        ctx.fillRect(90, y, Math.max(10, w), 14);

        ctx.fillStyle = '#ffffff';
        ctx.fillText(`${latencies[i]}ms`, 100 + Math.max(10, w), y + 11);
      }
    }

    // --- 7. LSM STORAGE SIMULATOR ---
    let lsmKeys = 3;
    function lsmWriteKey() {
      lsmKeys++;
      document.getElementById('lsm-mem-val').innerText = `${lsmKeys * 4} / 64 KB`;
      showToast(`Inserted key-value write into MemTable (Index ${lsmKeys})`);
      drawLsmCanvas();
    }
    function lsmFlush() {
      document.getElementById('lsm-mem-val').innerText = '0 / 64 KB';
      document.getElementById('lsm-l0-val').innerText = '3 files (Overlapping)';
      showToast('MemTable flushed to Level 0 SSTable!');
      drawLsmCanvas();
    }
    function lsmCompact() {
      document.getElementById('lsm-l0-val').innerText = '0 files';
      document.getElementById('lsm-l1-val').innerText = '6 files (Partitioned)';
      showToast('Leveled Compaction completed! Key ranges partitioned (+25 XP).');
      addXP(25, 'Triggered Leveled Compaction');
      drawLsmCanvas();
    }
    function lsmProbeKey() {
      showToast('Bloom Filter Hit! Read skipped 5 SSTables, hit target SSTable in 0.9ms (+25 XP)!');
      addXP(25, 'Executed Bloom Filter Probe');
    }
    function drawLsmCanvas() {
      const canvas = document.getElementById('lsm-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      canvas.width = (canvas.parentElement && canvas.parentElement.clientWidth) ? canvas.parentElement.clientWidth : 800;
      canvas.height = (canvas.parentElement && canvas.parentElement.clientHeight) ? canvas.parentElement.clientHeight : 280;

      ctx.fillStyle = '#020512';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = '#082f49';
      ctx.strokeStyle = '#0284c7';
      ctx.fillRect(30, 30, 200, 50);
      ctx.strokeRect(30, 30, 200, 50);
      ctx.fillStyle = '#ffffff'; ctx.font = 'bold 11px system-ui'; ctx.fillText('MemTable (SkipList)', 50, 60);

      ctx.fillStyle = '#451a03';
      ctx.strokeStyle = '#f59e0b';
      ctx.fillRect(280, 30, 220, 50);
      ctx.strokeRect(280, 30, 220, 50);
      ctx.fillStyle = '#ffffff'; ctx.fillText('L0 SSTables (Uncompacted)', 300, 60);

      ctx.fillStyle = '#064e3b';
      ctx.strokeStyle = '#10b981';
      ctx.fillRect(550, 30, 250, 50);
      ctx.strokeRect(550, 30, 250, 50);
      ctx.fillStyle = '#ffffff'; ctx.fillText('L1 SSTables (Partitioned)', 570, 60);
    }

    // --- 8. 3GPP CTE SIMULATOR ---
    function cteSelectService(type) {
      ['video', 'voice', 'iot'].forEach(t => {
        const b = document.getElementById(`btn-cte-${t}`);
        if (b) b.className = (t === type ? 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold text-xs' : 'px-2.5 py-1 rounded bg-slate-900 text-slate-400 border border-slate-700 text-xs');
      });
      const pLabel = document.getElementById('cte-packet-label');
      const rLabel = document.getElementById('cte-rate-label');

      if (type === 'video') {
        pLabel.innerText = 'Rating Group 100 (5G 4K Video)';
        rLabel.innerText = '$0.05 / MB';
      } else if (type === 'voice') {
        pLabel.innerText = 'Rating Group 200 (VoNR HD Voice)';
        rLabel.innerText = '$0.002 / Sec';
      } else {
        pLabel.innerText = 'Rating Group 300 (Massive IoT Telemetry)';
        rLabel.innerText = '$0.0001 / Report';
      }
      showToast(`Selected ${type.toUpperCase()} service packet!`);
    }

    function cteSimulateQuotaReservation() {
      showToast('Atomic Quota Reservation: Deducted units in 0.82ms! Zero DB round-trips (+25 XP).');
      addXP(25, 'Simulated 3GPP Quota Reservation');
    }

    // ==================== GAMIFICATION & XP CHIME SYSTEM ====================
    let audioChimeCtx = null;
    function playXpChime() {
      try {
        if (!audioChimeCtx) audioChimeCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioChimeCtx.state === 'suspended') audioChimeCtx.resume();

        const notes = [523.25, 659.25, 783.99]; // C5, E5, G5
        notes.forEach((freq, idx) => {
          const osc = audioChimeCtx.createOscillator();
          const gain = audioChimeCtx.createGain();
          osc.type = 'sine';
          osc.frequency.value = freq;
          gain.gain.setValueAtTime(0.08, audioChimeCtx.currentTime + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.001, audioChimeCtx.currentTime + idx * 0.08 + 0.25);
          osc.connect(gain);
          gain.connect(audioChimeCtx.destination);
          osc.start(audioChimeCtx.currentTime + idx * 0.08);
          osc.stop(audioChimeCtx.currentTime + idx * 0.08 + 0.25);
        });
      } catch(e) {}
    }

    function showXpFloat(amount) {
      const el = document.createElement('div');
      el.className = 'fixed pointer-events-none z-[100] font-mono font-bold text-xs text-cyan-300 bg-cyan-950/95 border border-cyan-500/70 px-3 py-1 rounded-full shadow-2xl flex items-center gap-1.5 xp-float-particle';
      el.innerHTML = `<span>+${amount} XP</span> <span>🚀</span>`;
      el.style.left = '160px';
      el.style.top = '60px';
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 900);
    }


    function addXP(amount, reason) {
      appState.xp = (appState.xp || 0) + amount;
      saveState();
      updateXpDisplay();
      showXpFloat(amount);
      playXpChime();
      if (reason) showToast(`+${amount} XP: ${reason}!`);
    }

    function getLevelInfo(xp) {
      if (xp < 500) return { rank: 'L3 Systems Explorer (Level 1)', nextXp: 500, pct: Math.round((xp / 500) * 100) };
      if (xp < 1500) return { rank: 'L4 Distributed Engineer (Level 2)', nextXp: 1500, pct: Math.round(((xp - 500) / 1000) * 100) };
      if (xp < 3000) return { rank: 'L5 Senior Systems Engineer (Level 3)', nextXp: 3000, pct: Math.round(((xp - 1500) / 1500) * 100) };
      if (xp < 6000) return { rank: 'L6 Staff Systems Architect (Level 4)', nextXp: 6000, pct: Math.round(((xp - 3000) / 3000) * 100) };
      if (xp < 10000) return { rank: 'L7 Senior Staff Architect (Level 5)', nextXp: 10000, pct: Math.round(((xp - 6000) / 4000) * 100) };
      return { rank: 'L8 Principal Systems Fellow (Level 6)', nextXp: 20000, pct: 100 };
    }

    function updateXpDisplay() {
      const xpVal = appState.xp || 0;
      const el = document.getElementById('xp-display');
      if (el) el.innerText = xpVal.toLocaleString();
      const info = getLevelInfo(xpVal);
      const titleEl = document.getElementById('modal-level-title');
      if (titleEl) titleEl.innerText = info.rank;
      const mXpVal = document.getElementById('modal-xp-val');
      if (mXpVal) mXpVal.innerText = `${xpVal.toLocaleString()} / ${info.nextXp.toLocaleString()} XP`;
      const bar = document.getElementById('modal-xp-bar');
      if (bar) bar.style.width = `${Math.min(100, info.pct)}%`;
    }

    function openGamificationModal() {
      updateXpDisplay();
      document.getElementById('gamification-modal').classList.remove('hidden');
    }

    // ==================== URL HASH & BOOTSTRAP ENGINE ====================
    function handleHashNavigation() {
      const hash = window.location.hash.toLowerCase().replace('#', '').trim();
      if (!hash) return false;
      if (hash === 'simulators' || hash === 'sim' || hash === 'stage-13') {
        goToStage(13);
        return true;
      }
      if (hash === 'leadership' || hash === 'stage-14') {
        goToStage(14);
        return true;
      }
      if (hash === 'tradeoffs' || hash === 'stage-15') {
        goToStage(15);
        return true;
      }
      if (hash === 'papers' || hash === 'stage-16') {
        goToStage(16);
        return true;
      }
      if (hash === 'exam' || hash === 'stage-17') {
        goToStage(17);
        return true;
      }
      const m = hash.match(/^stage-(\d+)$/);
      if (m) {
        goToStage(parseInt(m[1], 10));
        return true;
      }
      return false;
    }

    window.addEventListener('hashchange', handleHashNavigation);

    function bootApp() {
      try {
        updateXpDisplay();
        if (typeof updateStreakDisplay === 'function') updateStreakDisplay();
        if (typeof updateProgress === 'function') updateProgress();
        if (typeof renderPomoTime === 'function') renderPomoTime();
        
        const routed = handleHashNavigation();
        if (!routed) {
          goToStage(appState.currentStage || 1);
        }
      } catch(e) {
        console.error('Nexus Boot Error:', e);
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bootApp);
    } else {
      bootApp();
    }
</script>
</body>
</html>
''')

    final_html = "".join(html)

    # Write to target files
    target_path = "d:/Antigravity/Shivam_Staff_Engineer_Mastery_Roadmap.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Generated {target_path} ({len(final_html)} bytes)")

    brain_path = "C:/Users/shiva/.gemini/antigravity/brain/623354e4-df8d-442a-a628-1971c1a87479/Shivam_Staff_Engineer_Mastery_Roadmap.html"
    try:
        shutil.copyfile(target_path, brain_path)
        print(f"Mirrored to brain artifact: {brain_path}")
    except Exception as e:
        print(f"Mirror error: {e}")

if __name__ == "__main__":
    build_full_html()
