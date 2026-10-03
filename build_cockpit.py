# build_cockpit.py
# Next-Gen Zero-Scroll Cockpit Generator for NEXUS ARCHITECT
# Produces: d:/Antigravity/Shivam_Staff_Engineer_Mastery_Roadmap.html
# Mirrors to: C:/Users/shiva/.gemini/antigravity/brain/623354e4-df8d-442a-a628-1971c1a87479/Shivam_Staff_Engineer_Mastery_Roadmap.html

import sys
import shutil
import os
sys.path.append('d:/Antigravity')
import modules_tech
import modules_interactive
import system_design_data
import learning_resources_data

html_parts = []

# ============================================================================
# 1. HTML HEAD & STYLES (Cyberpunk / Linear / Obsidian Theme, 100vh Zero-Scroll)
# ============================================================================
html_parts.append("""<!DOCTYPE html>
<html lang="en" class="dark h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NEXUS ARCHITECT // Google L6/L8 Staff Engineering Cockpit | Shivam Agarwal</title>
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Fixed 100vh Zero-Scroll Application Canvas */
    html, body {
      height: 100vh;
      overflow: hidden;
      margin: 0;
      padding: 0;
      background-color: #040711;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    /* Micro Sleek Scrollbar for internal panels */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

    pre code {
      font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      font-size: 0.80rem;
      line-height: 1.55;
    }

    .code-block {
      background: #02040a;
      border: 1px solid rgba(30, 41, 59, 0.8);
      border-radius: 0.75rem;
      padding: 1rem;
      overflow-x: auto;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
    }

    .glass-card {
      background: rgba(10, 15, 29, 0.88);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .glow-border:hover {
      border-color: rgba(56, 189, 248, 0.5);
      box-shadow: 0 0 25px -5px rgba(56, 189, 248, 0.2);
    }

    /* Micro Tab Navigation */
    .micro-tab {
      cursor: pointer !important;
      user-select: none;
      white-space: nowrap;
      transition: all 0.15s ease;
      border-bottom: 2px solid transparent;
    }
    .micro-tab:hover {
      color: #ffffff !important;
      background: rgba(255, 255, 255, 0.08) !important;
    }
    .micro-tab.active {
      background: rgba(56, 189, 248, 0.18) !important;
      color: #38bdf8 !important;
      border-bottom: 2px solid #38bdf8 !important;
      font-weight: 700 !important;
    }

    .nav-stage-item.active {
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.5);
      color: #ffffff;
      box-shadow: inset 2px 0 0 #38bdf8;
    }

    /* Cloze Deletion Blur Mode */
    body.cloze-mode .cloze {
      background: #1e3a8a !important;
      color: transparent !important;
      border-radius: 4px;
      padding: 0 4px;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s ease;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
      display: inline-block;
    }
    body.cloze-mode .cloze:hover,
    body.cloze-mode .cloze.revealed {
      background: #0f2d59 !important;
      color: #93c5fd !important;
      text-shadow: none;
    }

    /* 3D Flip Card Styles */
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

    .toast {
      transform: translateY(100px);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    /* Whiteboard Stencil Nodes */
    .wb-node {
      user-select: none;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .wb-node.selected {
      outline: 2px solid #38bdf8 !important;
      border-color: #38bdf8 !important;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.6) !important;
    }

    .wb-tool.active {
      background: #0284c7 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
    }
  </style>
</head>
<body class="bg-[#030611] text-slate-200 h-screen overflow-hidden flex flex-col font-sans antialiased selection:bg-cyan-600 selection:text-white">
""")

# ============================================================================
# 2. TOP COMPACT HEADER (54px Fixed Height)
# ============================================================================
html_parts.append("""
  <!-- TOP COMPACT WORKSPACE HEADER -->
  <header class="h-[54px] shrink-0 bg-[#050814]/95 border-b border-white/[0.08] px-4 flex items-center justify-between gap-3 z-30 shadow-md">
    
    <!-- Brand Identity & Level Status -->
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700/80 flex items-center justify-center p-1 shadow">
        <svg class="w-6 h-6" viewBox="0 0 40 40" fill="none">
          <polygon points="20,2 38,12 38,28 20,38 2,28 2,12" stroke="url(#nexus-grad)" stroke-width="2.5" fill="#0b1329"/>
          <circle cx="20" cy="20" r="5" fill="#38bdf8"/>
          <path d="M20,6 L20,13 M33,14 L27,17 M33,26 L27,23 M20,34 L20,27 M7,26 L13,23 M7,14 L13,17" stroke="#38bdf8" stroke-width="1.5" stroke-linecap="round"/>
          <defs>
            <linearGradient id="nexus-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#38bdf8"/>
              <stop offset="50%" stop-color="#818cf8"/>
              <stop offset="100%" stop-color="#c084fc"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-sm font-black text-white font-mono tracking-wider">NEXUS<span class="text-cyan-400">.ARCHITECT</span></span>
          <span id="level-badge" class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/40">
            L6 STAFF ARCHITECT
          </span>
          <span class="text-[9px] font-mono text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-800/40">
            <span id="xp-display">1,450</span> XP
          </span>
          <span class="text-[9px] font-mono text-amber-300 bg-amber-950/60 px-1.5 py-0.5 rounded border border-amber-800/40">
            🔥 5-Day Streak
          </span>
        </div>
      </div>
    </div>

    <!-- Center: Pomodoro Focus Timer -->
    <div class="hidden md:flex items-center gap-2 px-3 py-1 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-mono">
      <span class="text-slate-400">⏱️ Focus:</span>
      <span id="pomo-display" class="font-bold text-cyan-400 text-xs">25:00</span>
      <button onclick="togglePomodoro()" id="btn-pomo-toggle" class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 text-[10px]">Start</button>
      <button onclick="resetPomodoro()" class="px-2 py-0.5 rounded bg-slate-800 text-slate-400 hover:text-white text-[10px]">Reset</button>
    </div>

    <!-- Right Controls: Split Studio, Whiteboard Modal, Trap Drill, Cloze, Theme, Progress -->
    <div class="flex items-center space-x-2 text-xs">
      
      <!-- Split-Screen Whiteboard Toggle (Draw Beside Text!) -->
      <button onclick="toggleSplitStudio()" id="btn-split-toggle" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 transition-all" title="Toggle side-by-side Whiteboard Studio while reading">
        <span>◫</span>
        <span class="hidden sm:inline">Split Studio</span>
      </button>

      <!-- Fullscreen Whiteboard Studio Modal -->
      <button onclick="openWhiteboardModal()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition-all" title="Open full-screen Whiteboard Studio">
        <span>🎨</span>
        <span class="hidden lg:inline">Fullscreen Studio</span>
      </button>

      <!-- Surprise L6 Trap Interview Drill -->
      <button onclick="triggerRandomTrapQuestion()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-rose-950/70 hover:bg-rose-900 border border-rose-800 text-rose-300 transition-all" title="Surprise Google Staff Trap Question">
        <span>⚡</span>
        <span class="hidden xl:inline">L6 Trap</span>
      </button>

      <!-- Cloze Active Recall Toggle -->
      <button onclick="toggleClozeMode()" id="cloze-toggle-btn" class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg font-semibold bg-slate-900 border border-slate-800 text-slate-300 hover:border-cyan-500 transition-all" title="Blur technical terms for active recall practice">
        <span>👁️</span>
        <span class="hidden 2xl:inline">Cloze</span>
      </button>

      <!-- Live Search -->
      <div class="relative hidden xl:block w-36">
        <input type="text" id="global-search" oninput="handleSearch(this.value)" placeholder="Search topic..." class="w-full bg-slate-900 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-all">
      </div>

      <!-- Mastery Progress -->
      <div class="flex items-center gap-2 pl-2 border-l border-slate-800">
        <div class="text-right">
          <div class="text-[9px] text-slate-400 uppercase font-semibold">Mastery</div>
          <div class="text-[11px] font-bold text-cyan-400"><span id="progress-percent">0%</span></div>
        </div>
        <div class="w-14 bg-slate-900 rounded-full h-1.5 overflow-hidden border border-slate-800">
          <div id="progress-bar" class="bg-gradient-to-r from-cyan-500 via-indigo-500 to-emerald-400 h-1.5 rounded-full transition-all duration-500" style="width: 0%"></div>
        </div>
      </div>

    </div>
  </header>
""")

# ============================================================================
# 3. THREE-PANEL APP LAYOUT (100% Height of Viewport - ZERO BODY SCROLL)
# ============================================================================
html_parts.append("""
  <!-- THREE-PANEL WORKSPACE CONTAINER -->
  <div class="flex-1 flex overflow-hidden">
    
    <!-- ==================== LEFT RAIL: STAGE EXPLORER (260px) ==================== -->
    <aside class="w-[260px] shrink-0 border-r border-white/[0.08] bg-[#060a17] flex flex-col justify-between overflow-y-auto select-none p-3 space-y-4">
      
      <div class="space-y-3">
        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 font-mono">Mastery Curriculum</span>
          <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">12 Stages</span>
        </div>

        <!-- 12 Progressive Stages Navigation -->
        <nav class="space-y-1 text-xs" id="nav-list">
          <div class="text-[9px] font-bold text-slate-400 uppercase tracking-wider px-2 pt-1 pb-1">Core Architecture Modules</div>
          
          <button onclick="goToStage(1)" id="side-nav-1" class="nav-stage-item active w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>⚡</span> 1. Ingress &amp; Zero-Copy</span>
            <span id="nav-ch1-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(2)" id="side-nav-2" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🔒</span> 2. Redis Mutex &amp; Fencing</span>
            <span id="nav-ch2-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(3)" id="side-nav-3" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🔁</span> 3. Outbox &amp; Idempotency</span>
            <span id="nav-ch3-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(4)" id="side-nav-4" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🌳</span> 4. PostgreSQL CTE Tree</span>
            <span id="nav-ch4-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(5)" id="side-nav-5" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🤖</span> 5. Edge AI &amp; GGUF RAG</span>
            <span id="nav-ch5-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(6)" id="side-nav-6" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🛡️</span> 6. 5G RAN &amp; SRE Multi-Burn</span>
            <span id="nav-ch6-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>
          <button onclick="goToStage(7)" id="side-nav-7" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🏥</span> 7. StAX &amp; Oracle VLDB</span>
            <span id="nav-ch7-status" class="w-2 h-2 rounded-full bg-slate-700 shrink-0"></span>
          </button>

          <div class="text-[9px] font-bold text-slate-400 uppercase tracking-wider px-2 pt-2.5 pb-1 border-t border-slate-800/80">Interactive Labs</div>
          
          <button onclick="goToStage(8)" id="side-nav-8" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🧪</span> 8. Visual Simulators</span>
            <span class="text-[8px] bg-cyan-500/20 text-cyan-400 px-1.5 py-0.5 rounded font-mono">7 Labs</span>
          </button>

          <div class="text-[9px] font-bold text-slate-400 uppercase tracking-wider px-2 pt-2.5 pb-1 border-t border-slate-800/80">Staff Strategy &amp; Certification</div>
          
          <button onclick="goToStage(9)" id="side-nav-9" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>👑</span> 9. Google Leadership</span>
            <span class="text-[8px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded font-mono">STAR</span>
          </button>
          <button onclick="goToStage(10)" id="side-nav-10" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>⚖️</span> 10. Trade-Off Matrix</span>
            <span class="text-[8px] bg-blue-500/20 text-blue-400 px-1.5 py-0.5 rounded font-mono">Grid</span>
          </button>
          <button onclick="goToStage(11)" id="side-nav-11" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>📜</span> 11. Google Papers</span>
            <span class="text-[8px] bg-indigo-500/20 text-indigo-400 px-1.5 py-0.5 rounded font-mono">Spanner</span>
          </button>
          <button onclick="goToStage(12)" id="side-nav-12" class="nav-stage-item w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg border border-transparent text-slate-300 hover:bg-slate-800/60 transition-all text-left">
            <span class="flex items-center gap-2 truncate"><span>🎯</span> 12. Bar-Raiser Exam</span>
            <span class="text-[8px] bg-rose-500/20 text-rose-400 px-1.5 py-0.5 rounded font-mono">6 Incidents</span>
          </button>
        </nav>
      </div>

      <!-- Bottom Tools & Audit -->
      <div class="pt-3 border-t border-slate-800/80 space-y-2.5">
        <button onclick="exportAllStudyNotes()" class="w-full py-1.5 px-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700 hover:border-cyan-500 font-semibold text-[11px] flex items-center justify-center gap-1.5 transition-all">
          <span>📥</span> Export Study Notes (.md)
        </button>

        <div class="p-2.5 rounded-xl bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-900/40 text-[10px]">
          <div class="font-bold text-indigo-300 flex items-center gap-1 mb-0.5">
            <span>🎓</span> IISc Bengaluru
          </div>
          <p class="text-slate-400 leading-snug">
            M.Tech. Data Science. Anchor Google L6 answers in kernel mechanics &amp; distributed proofs.
          </p>
        </div>
      </div>
    </aside>

    <!-- ==================== CENTER CANVAS: ACTIVE LEARNING STAGE ==================== -->
    <main class="flex-1 flex flex-col overflow-hidden bg-[#030611] relative" id="center-main-canvas">
""")

# ============================================================================
# 4. INGEST CHAPTERS 1 TO 7 (With 12 Multi-Modal Tabs per Chapter)
# ============================================================================
for mod in modules_tech.MODULES:
    ch_id = mod["id"]
    ch_num = mod["num"]
    ch_color = mod["color"]
    res = learning_resources_data.RESOURCES_DATA.get(ch_id, {})
    tldr = res.get("tldr", {})
    diff = res.get("diff", {})
    cap = res.get("capacity", {})
    videos = res.get("videos", [])
    sys_design = system_design_data.SYSTEM_DESIGNS.get(ch_id, {})
    fc = learning_resources_data.RESOURCES_DATA.get(ch_id, {}).get("tldr", {})

    # Build metric pills
    metric_pills = ""
    for item in tldr.get("numbers", []):
        metric_pills += f"""
          <div class="px-2.5 py-1 rounded-lg bg-slate-900/90 border border-slate-800 text-center shrink-0">
            <div class="text-[9px] text-slate-400 uppercase font-mono">{item["label"]}</div>
            <div class="text-xs font-bold text-cyan-300">{item["val"]}</div>
          </div>
        """

    # Build red flags with Junior vs Staff distinction
    red_flags_html = ""
    for rf in tldr.get("red_flags", []):
        if isinstance(rf, dict):
            red_flags_html += f"""
              <li class="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1 text-xs">
                <div class="text-rose-400 font-bold flex items-start gap-1.5"><span class="text-rose-500 font-bold shrink-0">✕ Junior Fallacy:</span> <span>{rf.get('junior', '')}</span></div>
                <div class="text-emerald-300 flex items-start gap-1.5"><span class="text-emerald-400 font-bold shrink-0">✔ Staff Defense:</span> <span>{rf.get('staff', '')}</span></div>
              </li>
            """
        else:
            red_flags_html += f"""
              <li class="flex items-start gap-1.5 text-xs text-rose-300/90">
                <span class="text-rose-500 font-bold shrink-0">✕</span>
                <span>{rf}</span>
              </li>
            """

    # Build battle scars
    battle_scars_html = ""
    for bs in tldr.get("battle_scars", []):
        battle_scars_html += f"""
          <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800 text-[11px] text-slate-300 space-y-0.5">
            <span class="text-amber-400 font-bold block">⚡ Production Battle Scar:</span>
            <p>{bs}</p>
          </div>
        """

    # Build invariants
    invariants_html = ""
    for inv in tldr.get("invariants", []):
        invariants_html += f"""
          <li class="flex items-start gap-2 text-xs text-slate-300">
            <span class="text-cyan-400 font-bold shrink-0">❖</span>
            <span>{inv}</span>
          </li>
        """

    # Build videos with embedded modal trigger & timestamps
    videos_html = ""
    for v in videos:
        timestamps_html = ""
        for ts in v.get("timestamps", []):
            timestamps_html += f"""
              <div class="flex items-center gap-2 text-[10px] text-slate-400 font-mono">
                <span class="text-cyan-400 font-bold">[{ts.get('time', '')}]</span>
                <span>{ts.get('topic', '')}</span>
              </div>
            """
        
        quote_html = ""
        if v.get("quote"):
            quote_html = f"""
              <div class="p-2 bg-slate-900/90 rounded border border-cyan-900/30 text-[11px] text-cyan-200 italic">
                💬 "{v.get('quote')}"
              </div>
            """

        safe_title = v["title"].replace("'", "")
        vid_id = v.get("videoId", "")
        videos_html += f"""
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
            <div class="space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white truncate max-w-[260px]">{v["title"]}</span>
                <span class="text-[9px] text-cyan-400 bg-cyan-950 px-1.5 py-0.5 rounded font-mono border border-cyan-800/40">{v.get("duration", "45 min")}</span>
              </div>
              <div class="text-[11px] text-slate-400 font-mono">Speaker: <strong class="text-slate-200">{v["speaker"]}</strong> • {v["event"]}</div>
              <p class="text-xs text-slate-300 leading-relaxed">{v["takeaway"]}</p>
              
              {f'<div class="pt-2 border-t border-slate-900 space-y-1"><span class="text-[10px] uppercase font-bold text-slate-500 font-mono">Key Timestamps:</span>{timestamps_html}</div>' if timestamps_html else ''}
              {quote_html}
            </div>
            
            <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2 text-xs">
              <button onclick="openVideoModal('{vid_id}', '{safe_title}')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold flex items-center gap-1.5 shadow transition-all">
                <span>▶</span> Watch In-App
              </button>
              <a href="{v['url']}" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-cyan-300 font-mono text-[11px] flex items-center gap-1">
                <span>↗ Open on YouTube</span>
              </a>
            </div>
          </div>
        """

    traps_html = ""
    for idx, trap in enumerate(mod.get("traps", [])):
        if isinstance(trap, dict):
            border_cls = "pt-4 border-t border-slate-800" if idx > 0 else ""
            traps_html += f"""
              <div class="{border_cls} space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 font-mono text-[10px]">L8 Ambush #{idx+1}</span>
                    {trap.get('title', '')}
                  </span>
                </div>
                
                <div class="p-3 bg-slate-900/90 rounded-lg border border-slate-800">
                  <span class="text-cyan-400 font-bold block mb-1">Scenario Interrogation:</span>
                  <p class="text-slate-200 text-xs italic">{trap.get('scenario', '')}</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                  <div class="p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 space-y-1">
                    <span class="text-rose-400 font-bold block">❌ Junior / L5 Fallacy:</span>
                    <p class="text-slate-400 leading-relaxed">{trap.get('junior_fallacy', '')}</p>
                  </div>
                  <div class="p-3 rounded-lg bg-blue-950/20 border border-blue-900/40 space-y-1">
                    <span class="text-blue-400 font-bold block">🔍 Kernel / Systems Root Cause:</span>
                    <p class="text-slate-300 leading-relaxed">{trap.get('root_cause', '')}</p>
                  </div>
                </div>

                <div class="p-3.5 rounded-lg bg-emerald-950/25 border border-emerald-900/50 space-y-1.5">
                  <div class="flex items-center justify-between">
                    <span class="text-emerald-400 font-bold text-xs">✅ Google Staff L6/L8 Architectural Defense:</span>
                    <span class="text-[9px] text-emerald-500 font-mono uppercase">Verbatim Interview Script</span>
                  </div>
                  <p class="text-slate-200 text-xs leading-relaxed font-sans">
                    <strong>Mitigation:</strong> {trap.get('l8_mitigation', '')}
                  </p>
                  <div class="p-2.5 rounded bg-slate-950 border border-emerald-900/40 text-emerald-300 font-mono text-[11px] leading-relaxed">
                    "{trap.get('defense_script', '')}"
                  </div>
                </div>
              </div>
            """
        elif isinstance(trap, (list, tuple)) and len(trap) >= 2:
            q, a = trap[0], trap[1]
            border_cls = "pt-3 border-t border-slate-800" if idx > 0 else ""
            traps_html += f"""
              <div class="{border_cls}">
                <span class="font-bold text-white text-xs block">Q{idx+1}: "{q}"</span>
                <p class="text-xs text-slate-400 mt-1">
                  <strong>Your Defense:</strong> <em>"{a}"</em>
                </p>
              </div>
            """

    chapter_html = f"""
      <!-- STAGE {ch_num} CONTAINER -->
      <section id="stage-{ch_num}" class="stage-section flex-1 flex flex-col overflow-hidden h-full">
        
        <!-- Stage Top Bar (Shrink-0) -->
        <div class="shrink-0 px-6 py-2.5 bg-[#050814]/90 border-b border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold uppercase tracking-wider text-{ch_color}-400 bg-{ch_color}-950/60 px-2 py-0.5 rounded border border-{ch_color}-800/40">
                Stage {ch_num} • {mod["domain"]}
              </span>
              <h2 class="text-base font-bold text-white">{mod["title"]}</h2>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <button onclick="loadDesignOnWhiteboard('{ch_id}')" class="px-2.5 py-1 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1 shadow transition-all" title="Sketch topology on whiteboard">
              <span>🎨</span> <span>Sketch Topology</span>
            </button>
            <label class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700 cursor-pointer text-xs font-medium text-slate-200">
              <input type="checkbox" id="{ch_id}-check" onchange="toggleChapter('{ch_id}')" class="rounded bg-slate-950 border-slate-600 text-cyan-500 focus:ring-0">
              <span>Mastered</span>
            </label>
          </div>
        </div>

        <!-- Metric Pills Ribbon (Shrink-0) -->
        <div class="shrink-0 px-6 py-2 bg-[#040612] border-b border-white/[0.05] flex items-center gap-2 overflow-x-auto">
          <span class="text-[9px] font-bold text-slate-400 uppercase font-mono mr-1">Numbers to Quote:</span>
          {metric_pills}
        </div>

        <!-- Micro-Tabs Navigation Bar (Shrink-0) -->
        <div class="shrink-0 px-6 bg-[#050917] border-b border-white/[0.08] flex gap-1 overflow-x-auto text-xs py-1" id="{ch_id}-tabs">
          <button onclick="switchTab('{ch_id}', 'blueprint')" id="{ch_id}-tab-blueprint" class="micro-tab active px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">📐 System Design Blueprint</button>
          <button onclick="switchTab('{ch_id}', 'tldr')" id="{ch_id}-tab-tldr" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">⚡ Executive TL;DR</button>
          <button onclick="switchTab('{ch_id}', 'diff')" id="{ch_id}-tab-diff" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">💻 Junior vs Staff Diff</button>
          <button onclick="switchTab('{ch_id}', 'capacity')" id="{ch_id}-tab-capacity" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🧮 Capacity Math</button>
          <button onclick="switchTab('{ch_id}', 'theory')" id="{ch_id}-tab-theory" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">📚 Deep Theory</button>
          <button onclick="switchTab('{ch_id}', 'project')" id="{ch_id}-tab-project" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🏭 Project Implementation</button>
          <button onclick="switchTab('{ch_id}', 'code')" id="{ch_id}-tab-code" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">⌨️ Production Code</button>
          <button onclick="switchTab('{ch_id}', 'traps')" id="{ch_id}-tab-traps" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">⚔️ L8 Traps</button>
          <button onclick="switchTab('{ch_id}', 'recall')" id="{ch_id}-tab-recall" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🎴 Active Recall Test</button>
          <button onclick="switchTab('{ch_id}', 'videos')" id="{ch_id}-tab-videos" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🎥 Masterclasses</button>
          <button onclick="switchTab('{ch_id}', 'pitch')" id="{ch_id}-tab-pitch" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">🎙️ 2-Min Pitch</button>
          <button onclick="switchTab('{ch_id}', 'notes')" id="{ch_id}-tab-notes" class="micro-tab px-3 py-1.5 rounded-t-lg text-slate-300 hover:text-white transition-all">📝 Notes</button>
        </div>

        <!-- Tab Content Viewport (Scrolls Internally without scrolling the page!) -->
        <div class="flex-1 overflow-y-auto px-6 py-5 space-y-6">
          
          <!-- TAB 1: SYSTEM DESIGN BLUEPRINT -->
          <div id="{ch_id}-content-blueprint" class="tab-content space-y-4 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-cyan-950/20 border border-cyan-900/40 rounded-xl flex flex-wrap items-center justify-between gap-3">
              <div>
                <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">Google L6/L8 Architecture Blueprint</span>
                <h3 class="text-sm font-bold text-white mt-0.5">{sys_design.get("title", "")}</h3>
              </div>
              <div class="flex gap-2">
                <button onclick="openSplitStudioWithTopology('{ch_id}')" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow transition-all">
                  <span>◫</span> Sketch in Split Studio
                </button>
              </div>
            </div>
            {sys_design.get("requirements", "")}
          </div>

          <!-- TAB 2: EXECUTIVE TL;DR CHEATSHEET -->
          <div id="{ch_id}-content-tldr" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
              
              <!-- 30-Sec Elevator Pitch -->
              <div class="p-3.5 bg-gradient-to-r from-cyan-950/40 to-slate-900 rounded-lg border border-cyan-900/40 space-y-1">
                <span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block font-mono">The 30-Second Executive Pitch (Google Staff / Principal)</span>
                <p class="text-xs text-white leading-relaxed italic">
                  "{tldr.get("elevator_pitch", tldr.get("principle", ""))}"
                </p>
              </div>

              <!-- Architectural Invariants -->
              <div class="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
                <span class="text-xs font-bold text-white uppercase tracking-wider block">Architectural Invariants & Laws of Physics</span>
                <ul class="space-y-1.5">
                  {invariants_html}
                </ul>
              </div>

              <!-- Red Flags & Battle Scars Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-3.5 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-2">
                  <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block">Top L6 Red Flags & Rejection Traps</span>
                  <ul class="space-y-2">
                    {red_flags_html}
                  </ul>
                </div>
                
                <div class="space-y-3">
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">Production Gotcha to Highlight</span>
                    <p class="text-slate-300 leading-relaxed text-[11px]">
                      {tldr.get("gotchas", "")}
                    </p>
                  </div>
                  
                  <div class="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider block">Real-World Production Battle Scars</span>
                    <div class="space-y-2">
                      {battle_scars_html}
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- TAB 3: JUNIOR VS STAFF CODE DIFF -->
          <div id="{ch_id}-content-diff" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white text-xs">{diff.get("title", "")}</span>
              <span class="text-[10px] text-slate-400 font-mono">Compare architectural anti-patterns with Google bar-raising standards</span>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div class="p-3.5 rounded-xl bg-[#140608] border border-rose-900/60 space-y-2">
                <div class="flex items-center justify-between text-xs text-rose-400 font-bold border-b border-rose-900/40 pb-1.5">
                  <span>❌ Naive Junior / Mid Implementation</span>
                  <span class="text-[9px] bg-rose-950 px-1.5 py-0.5 rounded font-mono">Anti-Pattern</span>
                </div>
                <div class="code-block text-[11px]">
                  <pre><code>{diff.get("junior", "")}</code></pre>
                </div>
              </div>
              <div class="p-3.5 rounded-xl bg-[#03150d] border border-emerald-900/60 space-y-2">
                <div class="flex items-center justify-between text-xs text-emerald-400 font-bold border-b border-emerald-900/40 pb-1.5">
                  <span>✅ Google Staff L6 Hardened Architecture</span>
                  <span class="text-[9px] bg-emerald-950 px-1.5 py-0.5 rounded font-mono">Bar-Raiser</span>
                </div>
                <div class="code-block text-[11px]">
                  <pre><code>{diff.get("staff", "")}</code></pre>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 4: INTERACTIVE CAPACITY MATH CALCULATOR -->
          <div id="{ch_id}-content-capacity" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800 space-y-4">
              <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h4 class="text-sm font-bold text-white">Live Back-of-the-Envelope Capacity Estimator</h4>
                  <p class="text-[11px] text-slate-400">Adjust the reactive sliders to observe cluster hardware sizing and network bandwidth math.</p>
                </div>
                <span class="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-800/40">Real-Time Compute</span>
              </div>

              <!-- Interactive Sliders Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]">
                    <span class="text-slate-400">Target QPS:</span>
                    <span id="{ch_id}-val-qps" class="font-bold text-cyan-400 font-mono">45,000 req/s</span>
                  </div>
                  <input type="range" min="1000" max="100000" step="1000" value="45000" id="{ch_id}-calc-qps" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-cyan-500 h-1.5">
                </div>

                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]">
                    <span class="text-slate-400">Message Size:</span>
                    <span id="{ch_id}-val-size" class="font-bold text-purple-400 font-mono">1.0 KB</span>
                  </div>
                  <input type="range" min="256" max="8192" step="256" value="1024" id="{ch_id}-calc-size" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-purple-500 h-1.5">
                </div>

                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]">
                    <span class="text-slate-400">Replication Factor:</span>
                    <span id="{ch_id}-val-rep" class="font-bold text-emerald-400 font-mono">3x</span>
                  </div>
                  <input type="range" min="1" max="5" step="1" value="3" id="{ch_id}-calc-rep" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-emerald-500 h-1.5">
                </div>

                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800 space-y-1.5">
                  <div class="flex justify-between text-[11px]">
                    <span class="text-slate-400">Retention Period:</span>
                    <span id="{ch_id}-val-ret" class="font-bold text-amber-400 font-mono">7 days</span>
                  </div>
                  <input type="range" min="1" max="30" step="1" value="7" id="{ch_id}-calc-ret" oninput="updateCapacityCalc('{ch_id}')" class="w-full accent-amber-500 h-1.5">
                </div>
              </div>

              <!-- Reactive Results Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2 font-mono text-xs">
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400">Network Ingress:</div>
                  <div id="{ch_id}-res-bw" class="font-bold text-cyan-400 mt-1">43.9 MB/s (0.35 Gbps)</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400">Daily Volume:</div>
                  <div id="{ch_id}-res-daily" class="font-bold text-purple-400 mt-1">11,390 GB / day</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400">Cluster Storage:</div>
                  <div id="{ch_id}-res-storage" class="font-bold text-emerald-400 mt-1">95.7 TB (with headroom)</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400">Partitions Required:</div>
                  <div id="{ch_id}-res-part" class="font-bold text-amber-400 mt-1">128 Partitions</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400">PageCache RAM:</div>
                  <div id="{ch_id}-res-ram" class="font-bold text-rose-400 mt-1">13 GB RAM</div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 5: DEEP THEORY -->
          <div id="{ch_id}-content-theory" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            {mod["theory"]}
          </div>

          <!-- TAB 6: PROJECT IMPLEMENTATION -->
          <div id="{ch_id}-content-project" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            {mod["project"]}
          </div>

          <!-- TAB 7: PRODUCTION CODE -->
          <div id="{ch_id}-content-code" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-{ch_color}-400">Production Code &amp; Schema Implementation</span>
              <button onclick="copyCode('code-{ch_id}')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded border border-slate-700 transition-all flex items-center gap-1">
                <span>📋</span> Copy Code
              </button>
            </div>
            <div class="code-block" id="code-{ch_id}">
              {mod["code"]}
            </div>
          </div>

          <!-- TAB 8: L8 BAR-RAISER TRAPS -->
          <div id="{ch_id}-content-traps" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-5 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
              {traps_html}
            </div>
          </div>

          <!-- TAB 9: ACTIVE RECALL FLASHCARD TEST -->
          <div id="{ch_id}-content-recall" class="tab-content hidden space-y-4 text-xs">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-xs font-bold text-white uppercase tracking-wider">Active Recall Self-Test • Stage {ch_num}</span>
                <p class="text-[11px] text-slate-400">Test your mental model immediately after studying this module. Click card or press Spacebar to flip.</p>
              </div>
              <div id="{ch_id}-recall-badge" class="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700 text-slate-400 text-xs font-mono">
                Status: Unattempted
              </div>
            </div>

            <!-- 3D Card -->
            <div class="max-w-2xl mx-auto flashcard-container min-h-[220px]">
              <div id="{ch_id}-card" onclick="flipModuleCard('{ch_id}')" class="flashcard relative w-full min-h-[220px] rounded-2xl bg-gradient-to-br from-slate-900 to-[#050b18] border border-slate-800 p-6 shadow-2xl flex flex-col justify-between hover:border-cyan-500/40">
                <div class="flashcard-front space-y-3">
                  <div class="flex justify-between items-center text-xs text-cyan-400 font-semibold uppercase tracking-wider">
                    <span>{mod["domain"]} • L6 Recall Question</span>
                    <span>Click to Flip 🔄</span>
                  </div>
                  <h4 class="text-base font-bold text-white leading-snug">
                    {mod["traps"][0].get("title", "Explain the core bottleneck of this architecture.") if mod.get("traps") and isinstance(mod["traps"][0], dict) else (mod["traps"][0][0] if mod.get("traps") else "Explain the core bottleneck of this architecture.")}
                  </h4>
                  <p class="text-[11px] text-slate-400 font-mono">
                    {mod["traps"][0].get("scenario", "Formulate your architectural explanation before flipping.") if mod.get("traps") and isinstance(mod["traps"][0], dict) else "Formulate your architectural explanation before flipping."}
                  </p>
                </div>
                <div class="flashcard-back absolute inset-0 p-6 rounded-2xl bg-[#080e22] border border-cyan-500/40 flex flex-col justify-between space-y-3">
                  <div>
                    <div class="flex justify-between items-center text-xs text-emerald-400 font-semibold uppercase tracking-wider mb-1.5">
                      <span>Google L6 Bar-Raiser Defense</span>
                      <span>Click to Flip 🔄</span>
                    </div>
                    <div class="text-xs text-slate-300 leading-relaxed space-y-1">
                      {mod["traps"][0].get("defense_script", "Verify PageCache dirty ratio and zero-copy DMA buffers.") if mod.get("traps") and isinstance(mod["traps"][0], dict) else (mod["traps"][0][1] if mod.get("traps") else "Verify PageCache dirty ratio and zero-copy DMA buffers.")}
                    </div>
                  </div>
                  <div class="pt-2 border-t border-slate-800 flex justify-end">
                    <span class="text-[10px] text-slate-400">Rate your recall below to log progress &amp; earn XP</span>
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
          </div>

          <!-- TAB 10: VIDEO MASTERCLASSES -->
          <div id="{ch_id}-content-videos" class="tab-content hidden space-y-4 text-xs">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              {videos_html}
            </div>
          </div>

          <!-- TAB 11: 2-MIN WHITEBOARD PITCH -->
          <div id="{ch_id}-content-pitch" class="tab-content hidden space-y-4 text-xs text-slate-300">
            <div class="p-5 bg-emerald-950/20 border border-emerald-900/40 rounded-xl space-y-3">
              <blockquote id="{ch_id}-pitch-text" class="italic text-xs text-slate-200 leading-relaxed">
                {mod["pitch"]}
              </blockquote>
              <div class="pt-3 border-t border-emerald-900/40 flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                  <button onclick="readAloudPitch('{ch_id}')" id="{ch_id}-tts-btn" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                    <span>🔊</span> <span id="{ch_id}-tts-label">Listen to L6 Pitch</span>
                  </button>
                  <button onclick="toggleVoiceRecording('{ch_id}')" id="{ch_id}-mic-btn" class="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs flex items-center gap-1.5 transition-all">
                    <span>🎙️</span> <span id="{ch_id}-mic-label">Record Pitch</span>
                  </button>
                  <span id="{ch_id}-timer" class="font-mono text-xs text-amber-300 font-bold">00:00 / 02:00</span>
                </div>
                <audio id="{ch_id}-audio" controls class="hidden h-7 max-w-xs"></audio>
              </div>
            </div>
          </div>

          <!-- TAB 12: PERSONAL NOTES -->
          <div id="{ch_id}-content-notes" class="tab-content hidden space-y-3">
            <div class="flex justify-between items-center text-xs text-slate-400">
              <span>Takeaways auto-save locally and persist across sessions:</span>
              <span class="text-emerald-400 font-mono text-[10px]">Auto-Save Active</span>
            </div>
            <textarea id="{ch_id}-notes-area" rows="8" placeholder="Write personal takeaways, interview framing tips, and architecture trade-offs for Stage {ch_num}..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-sans"></textarea>
          </div>

        </div>
      </section>
    """
    html_parts.append(chapter_html)

# ============================================================================
# 5. STAGES 8 TO 12 (Simulators Sandbox, Leadership, Trade-offs, Papers, Exam)
# ============================================================================
# Wrap Stage 8 to 12 sections inside full-height section containers
stage_8_wrapper = f"""
  <div id="stage-8" class="stage-section hidden flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
    {modules_interactive.STAGE_8_SIMULATORS}
  </div>
"""
stage_9_wrapper = f"""
  <div id="stage-9" class="stage-section hidden flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
    {modules_interactive.STAGE_9_LEADERSHIP}
  </div>
"""
stage_10_wrapper = f"""
  <div id="stage-10" class="stage-section hidden flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
    {modules_interactive.STAGE_10_TRADEOFFS}
  </div>
"""
stage_11_wrapper = f"""
  <div id="stage-11" class="stage-section hidden flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
    {modules_interactive.STAGE_11_PAPERS}
  </div>
"""
stage_12_wrapper = f"""
  <div id="stage-12" class="stage-section hidden flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
    {modules_interactive.STAGE_12_EXAM}
  </div>
"""

html_parts.append(stage_8_wrapper)
html_parts.append(stage_9_wrapper)
html_parts.append(stage_10_wrapper)
html_parts.append(stage_11_wrapper)
html_parts.append(stage_12_wrapper)

html_parts.append("""
    </main>
""")

# ============================================================================
# 6. RIGHT PANEL: SPLIT-SCREEN WHITEBOARD STUDIO DOCK (560px Wide)
# ============================================================================
html_parts.append("""
    <!-- ==================== RIGHT PANEL: SPLIT-SCREEN WHITEBOARD DOCK ==================== -->
    <div id="split-studio-panel" class="hidden w-[580px] shrink-0 border-l border-white/[0.08] bg-[#050917] flex flex-col overflow-hidden select-none">
      
      <!-- Split Studio Header -->
      <div class="px-4 py-2.5 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm">🎨</span>
          <span class="text-xs font-bold text-white font-mono">SPLIT WHITEBOARD STUDIO</span>
        </div>
        <div class="flex items-center gap-1.5">
          <button onclick="undoWhiteboard()" class="px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-[10px]" title="Undo">↩️ Undo</button>
          <button onclick="clearWhiteboard()" class="px-2 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 text-[10px]" title="Clear All">🗑️ Clear All</button>
          <button onclick="openWhiteboardModal()" class="px-2 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]" title="Maximize to full modal">⛶ Fullscreen</button>
          <button onclick="toggleSplitStudio()" class="w-6 h-6 rounded bg-slate-800 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center text-xs font-bold" title="Close Split Studio">✕</button>
        </div>
      </div>

      <!-- Split Studio Toolbar -->
      <div class="px-3 py-2 bg-slate-950/80 border-b border-slate-800 text-xs flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-1">
          <button onclick="setWbTool('pen')" id="split-tool-pen" class="wb-tool active px-2 py-0.5 rounded bg-slate-800 text-white border border-slate-700 text-[11px]">✏️ Pen</button>
          <button onclick="setWbTool('arrow')" id="split-tool-arrow" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">➡️ Arrow</button>
          <button onclick="setWbTool('box')" id="split-tool-box" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">⬜ Box</button>
          <button onclick="setWbTool('circle')" id="split-tool-circle" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">⚪ Circle</button>
          <button onclick="setWbTool('eraser')" id="split-tool-eraser" class="wb-tool px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[11px]">🧹 Eraser</button>
        </div>

        <div class="flex items-center gap-1">
          <button onclick="addStencil('gateway')" class="px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 text-[10px]">+ Gateway</button>
          <button onclick="addStencil('kafka')" class="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]">+ Kafka</button>
          <button onclick="addStencil('redis')" class="px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 text-[10px]">+ Redis</button>
          <button onclick="addStencil('postgres')" class="px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[10px]">+ Postgres</button>
          <button onclick="addStencil('pod')" class="px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px]">+ Pod</button>
        </div>
      </div>

      <!-- Canvas Viewport in Split Panel -->
      <div id="split-viewport" class="relative flex-1 bg-[#030611] overflow-hidden">
        <canvas id="split-canvas" class="w-full h-full cursor-crosshair block absolute inset-0 z-0"></canvas>
        <div id="split-nodes" class="absolute inset-0 pointer-events-none z-10 overflow-hidden"></div>
      </div>

      <!-- Split Footer -->
      <div class="px-3 py-1.5 bg-slate-950 border-t border-slate-800 text-[10px] text-slate-400 flex items-center justify-between font-mono">
        <span>Click ❌ or Delete to remove stencil</span>
        <button onclick="downloadWhiteboard()" class="text-cyan-400 hover:underline">💾 Export PNG</button>
      </div>

    </div>

  </div> <!-- End Three-Panel Container -->
""")

# Ingest dedicated Whiteboard Modal HTML
html_parts.append(modules_interactive.WHITEBOARD_MODAL_HTML)

# Add Surprise Trap Modal & Toast
html_parts.append("""
  <!-- SURPRISE L6 TRAP MODAL -->
  <div id="trap-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-rose-600/60 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in duration-200">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-rose-400 text-lg">⚠️</span>
          <span class="text-xs font-bold uppercase tracking-wider text-rose-400">Google Staff Interviewer Interruption!</span>
        </div>
        <span id="trap-timer" class="text-xs font-mono font-bold text-amber-300">60s</span>
      </div>

      <div class="space-y-2">
        <p id="trap-question-text" class="text-sm font-bold text-white leading-relaxed">
          "Wait Shivam, you mentioned you keyed Kafka by NetworkElement_ID. What if a firmware push causes 50,000 parameter updates on a single cell tower? How does your consumer prevent partition head-of-line blocking?"
        </p>
        <p class="text-xs text-slate-400">Formulate your L6 defense out loud, then click Reveal to check your answer:</p>
      </div>

      <div id="trap-answer-reveal" class="hidden p-3 rounded-xl bg-slate-950 border border-emerald-500/40 text-xs text-emerald-300 leading-relaxed">
        <strong>The Staff Defense:</strong> "We implement Compound Salting: append a bounded random salt (cellId + '_' + (hash % 4)) to fan out the hot tower across 4 partitions. Downstream consumers re-assemble ordering via an in-memory priority queue before database commit."
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <button onclick="revealTrapAnswer()" id="btn-reveal-trap" class="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold">Reveal Defense (+150 XP)</button>
        <button onclick="closeTrapModal()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs">Dismiss</button>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="toast fixed bottom-6 right-6 bg-slate-900 border border-slate-700 text-white px-4 py-2.5 rounded-xl shadow-2xl text-xs flex items-center gap-2 z-50">
    <span class="text-cyan-400">✔</span>
    <span id="toast-msg">Action completed</span>
  </div>
""")

# ============================================================================
# 7. MASTER JAVASCRIPT ENGINE
# ============================================================================
html_parts.append("""
  <!-- JAVASCRIPT ENGINE -->
  <script>
    const STORAGE_KEY = 'nexus_architect_mastery_v8';
    let appState = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {
      currentStage: 1,
      xp: 1450,
      level: 'L6 Staff Architect',
      streak: 5,
      chapters: {},
      recall: {},
      notes: {},
      audit: { 1: 5, 2: 4, 3: 4, 4: 5, 5: 4, 6: 4, 7: 4 }
    };

    let activeStage = appState.currentStage || 1;
    let splitStudioOpen = false;

    // ==================== STAGE NAVIGATION ====================
    function goToStage(stageNum) {
      activeStage = stageNum;
      appState.currentStage = stageNum;
      saveState();

      // Update sidebar nav items
      for (let i = 1; i <= 12; i++) {
        const item = document.getElementById(`side-nav-${i}`);
        const sec = document.getElementById(`stage-${i}`);
        const isCurrent = (i === stageNum);

        if (item) {
          item.classList.toggle('active', isCurrent);
          item.classList.toggle('border-slate-800', !isCurrent);
        }
        if (sec) {
          sec.style.display = isCurrent ? 'flex' : 'none';
        }
      }

      // Initialize capacity calculation for current chapter
      if (stageNum <= 7) {
        updateCapacityCalc(`ch${stageNum}`);
      }
    }

    // ==================== TAB SWITCHING ====================
    function switchTab(chapter, tabName) {
      // Find stage section: stage-1 for ch1, stage-2 for ch2, etc.
      let container = null;
      if (chapter) {
        const num = chapter.replace('ch', '');
        container = document.getElementById(`stage-${num}`) || document.getElementById(chapter);
      }
      if (!container) {
        container = document.getElementById(`stage-${activeStage}`);
      }
      if (!container) {
        container = document;
      }

      container.querySelectorAll('.micro-tab').forEach(btn => btn.classList.remove('active'));
      container.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

      const activeBtn = document.getElementById(`${chapter}-tab-${tabName}`);
      const activeContent = document.getElementById(`${chapter}-content-${tabName}`);
      if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
      }
      if (activeContent) {
        activeContent.classList.remove('hidden');
      }

      // If switching to capacity math, ensure calculation is refreshed
      if (tabName === 'capacity') {
        updateCapacityCalc(chapter);
      }
    }

    function switchSim(simId) {
      document.querySelectorAll('#sim-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.sim-panel').forEach(panel => panel.classList.add('hidden'));

      const activeBtn = document.getElementById(`tab-${simId}`);
      const activePanel = document.getElementById(simId);
      if (activeBtn) activeBtn.classList.add('active');
      if (activePanel) activePanel.classList.remove('hidden');
    }

    // ==================== LIVE CAPACITY MATH ENGINE ====================
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

      // Display inputs
      document.getElementById(`${chId}-val-qps`).innerText = qps.toLocaleString() + ' req/s';
      document.getElementById(`${chId}-val-size`).innerText = size >= 1024 ? (size/1024).toFixed(1) + ' KB' : size + ' B';
      document.getElementById(`${chId}-val-rep`).innerText = rep + 'x';
      document.getElementById(`${chId}-val-ret`).innerText = ret + ' days';

      // Capacity Calculations
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

    // ==================== SPLIT STUDIO TOGGLE ====================
    function toggleSplitStudio() {
      splitStudioOpen = !splitStudioOpen;
      const panel = document.getElementById('split-studio-panel');
      const btn = document.getElementById('btn-split-toggle');
      if (panel) {
        panel.classList.toggle('hidden', !splitStudioOpen);
        if (splitStudioOpen) {
          btn.className = 'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-600 text-white transition-all shadow';
          initSplitCanvas();
        } else {
          btn.className = 'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-semibold bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 transition-all';
        }
      }
    }

    function openSplitStudioWithTopology(chId) {
      if (!splitStudioOpen) toggleSplitStudio();
      loadDesignOnWhiteboard(chId);
    }

    // ==================== WHITEBOARD STUDIO ENGINE ====================
    let wbCanvas = null;
    let wbCtx = null;
    let wbTool = 'pen';
    let wbColor = '#f8fafc';
    let wbWidth = 4;
    let wbDrawing = false;
    let wbStartX = 0;
    let wbStartY = 0;
    let wbHistory = [];
    let wbSnapshot = null;
    let wbNodes = [];
    let selectedWbNodeId = null;
    let isDraggingNode = false;
    let dragNodeId = null;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    const WB_STENCIL_CONFIGS = {
      'gateway': { title: 'Envoy API Gateway', subtext: 'TLS + Token Bucket Limiter', bg: '#0b192e', border: '#1d4ed8', textColor: 'text-blue-300', dotColor: 'bg-blue-400', icon: '🌐' },
      'kafka': { title: 'Kafka Cluster [128P]', subtext: 'PageCache DMA Zero-Copy', bg: '#081e28', border: '#0284c7', textColor: 'text-cyan-300', dotColor: 'bg-cyan-400', icon: '⚡' },
      'redis': { title: 'Redis Mutex Lock', subtext: 'Monotonic Fencing Token', bg: '#170c2a', border: '#9333ea', textColor: 'text-purple-300', dotColor: 'bg-purple-400', icon: '🔒' },
      'postgres': { title: 'PostgreSQL DB', subtext: 'ACID Outbox & CTE WorkTable', bg: '#231805', border: '#d97706', textColor: 'text-amber-300', dotColor: 'bg-amber-400', icon: '🐘' },
      'pod': { title: 'Spring Service Pod', subtext: 'Virtual Threads (Loom)', bg: '#062017', border: '#059669', textColor: 'text-emerald-300', dotColor: 'bg-emerald-400', icon: '📦' },
      'gnodeb': { title: '5G gNodeB / RAN', subtext: 'eCPRI / SCTP Telemetry', bg: '#260a12', border: '#e11d48', textColor: 'text-rose-300', dotColor: 'bg-rose-400', icon: '📡' },
      'llm': { title: 'Edge LLM (GGUF)', subtext: '4-Bit Quantized AVX-512', bg: '#041f1f', border: '#0d9488', textColor: 'text-teal-300', dotColor: 'bg-teal-400', icon: '🧠' },
      'prom': { title: 'Prometheus / SRE', subtext: 'Multi-Window Multi-Burn', bg: '#241206', border: '#ea580c', textColor: 'text-orange-300', dotColor: 'bg-orange-400', icon: '📊' },
      's3': { title: 'Object Store / S3', subtext: 'Partitioned Parquet Lake', bg: '#0f172a', border: '#475569', textColor: 'text-slate-300', dotColor: 'bg-slate-400', icon: '🗄️' }
    };

    function openWhiteboardModal() {
      const modal = document.getElementById('whiteboard-modal');
      if (modal) {
        modal.classList.remove('hidden');
        setTimeout(() => {
          initWhiteboardCanvas();
        }, 50);
      }
    }

    function closeWhiteboardModal() {
      const modal = document.getElementById('whiteboard-modal');
      if (modal) modal.classList.add('hidden');
    }

    function initSplitCanvas() {
      const canvas = document.getElementById('split-canvas');
      const viewport = document.getElementById('split-viewport');
      if (!canvas || !viewport) return;

      const rect = viewport.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;
      wbCanvas = canvas;
      wbCtx = canvas.getContext('2d');
      wbCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
      wbCtx.lineCap = 'round';
      wbCtx.lineJoin = 'round';

      canvas.onmousedown = wbStart;
      canvas.onmousemove = wbDraw;
      canvas.onmouseup = wbEnd;
      canvas.onmouseleave = wbEnd;
    }

    function initWhiteboardCanvas() {
      wbCanvas = document.getElementById('whiteboard-canvas');
      const viewport = document.getElementById('whiteboard-viewport');
      if (!wbCanvas || !viewport) return;
      
      wbCtx = wbCanvas.getContext('2d');
      const rect = viewport.getBoundingClientRect();
      wbCanvas.width = rect.width * window.devicePixelRatio;
      wbCanvas.height = rect.height * window.devicePixelRatio;
      wbCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
      wbCtx.lineCap = 'round';
      wbCtx.lineJoin = 'round';

      if (wbHistory.length === 0) saveWbState();

      wbCanvas.onmousedown = wbStart;
      wbCanvas.onmousemove = wbDraw;
      wbCanvas.onmouseup = wbEnd;
      wbCanvas.onmouseleave = wbEnd;

      window.addEventListener('mousemove', handleWbNodeDrag);
      window.addEventListener('mouseup', endWbNodeDrag);
    }

    function saveWbState() {
      if (!wbCtx || !wbCanvas) return;
      wbHistory.push(wbCtx.getImageData(0, 0, wbCanvas.width, wbCanvas.height));
      if (wbHistory.length > 25) wbHistory.shift();
    }

    function undoWhiteboard() {
      if (wbHistory.length > 1) {
        wbHistory.pop();
        const prev = wbHistory[wbHistory.length - 1];
        wbCtx.putImageData(prev, 0, 0);
        showToast('Whiteboard stroke undone.');
      }
    }

    function clearWhiteboard() {
      if (wbCtx && wbCanvas) {
        wbCtx.clearRect(0, 0, wbCanvas.width, wbCanvas.height);
        saveWbState();
      }
      const nodesContainer = document.getElementById(splitStudioOpen ? 'split-nodes' : 'whiteboard-nodes');
      if (nodesContainer) nodesContainer.innerHTML = '';
      const otherContainer = document.getElementById(splitStudioOpen ? 'whiteboard-nodes' : 'split-nodes');
      if (otherContainer) otherContainer.innerHTML = '';
      wbNodes = [];
      selectedWbNodeId = null;
      updateWbNodeCount();
      showToast('Canvas strokes and all stencils cleared!');
    }

    function setWbTool(tool) {
      wbTool = tool;
      document.querySelectorAll('.wb-tool').forEach(b => b.classList.remove('active'));
      const btn1 = document.getElementById(`wb-tool-${tool}`);
      const btn2 = document.getElementById(`split-tool-${tool}`);
      if (btn1) btn1.classList.add('active');
      if (btn2) btn2.classList.add('active');
    }

    function setWbColor(color) { wbColor = color; }
    function setWbWidth(width) { wbWidth = width; }

    function wbStart(e) {
      wbDrawing = true;
      wbStartX = e.offsetX;
      wbStartY = e.offsetY;
      wbSnapshot = wbCtx.getImageData(0, 0, wbCanvas.width, wbCanvas.height);

      if (wbTool === 'pen' || wbTool === 'eraser') {
        wbCtx.beginPath();
        wbCtx.moveTo(wbStartX, wbStartY);
      } else if (wbTool === 'text') {
        const text = prompt('Enter architecture node text / annotation:', 'Service Pod [QPS: 10k]');
        if (text) {
          wbCtx.font = 'bold 12px JetBrains Mono, monospace';
          wbCtx.fillStyle = wbColor;
          wbCtx.fillText(text, wbStartX, wbStartY);
          saveWbState();
        }
        wbDrawing = false;
      }
    }

    function wbDraw(e) {
      if (!wbDrawing) return;
      const currX = e.offsetX;
      const currY = e.offsetY;

      if (wbTool === 'pen') {
        wbCtx.strokeStyle = wbColor;
        wbCtx.lineWidth = wbWidth;
        wbCtx.lineTo(currX, currY);
        wbCtx.stroke();
      } else if (wbTool === 'eraser') {
        wbCtx.save();
        wbCtx.globalCompositeOperation = 'destination-out';
        wbCtx.beginPath();
        wbCtx.arc(currX, currY, wbWidth * 4, 0, Math.PI * 2);
        wbCtx.fill();
        wbCtx.restore();
      } else if (wbTool === 'box') {
        wbCtx.putImageData(wbSnapshot, 0, 0);
        wbCtx.strokeStyle = wbColor;
        wbCtx.lineWidth = wbWidth;
        wbCtx.strokeRect(wbStartX, wbStartY, currX - wbStartX, currY - wbStartY);
      } else if (wbTool === 'circle') {
        wbCtx.putImageData(wbSnapshot, 0, 0);
        wbCtx.strokeStyle = wbColor;
        wbCtx.lineWidth = wbWidth;
        wbCtx.beginPath();
        const rx = Math.abs(currX - wbStartX) / 2;
        const ry = Math.abs(currY - wbStartY) / 2;
        const cx = Math.min(wbStartX, currX) + rx;
        const cy = Math.min(wbStartY, currY) + ry;
        wbCtx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
        wbCtx.stroke();
      } else if (wbTool === 'arrow') {
        wbCtx.putImageData(wbSnapshot, 0, 0);
        wbCtx.strokeStyle = wbColor;
        wbCtx.lineWidth = wbWidth;
        drawArrow(wbCtx, wbStartX, wbStartY, currX, currY);
      }
    }

    function wbEnd() {
      if (wbDrawing) {
        wbDrawing = false;
        saveWbState();
      }
    }

    function drawArrow(ctx, fromx, fromy, tox, toy) {
      const headlen = 12;
      const angle = Math.atan2(toy - fromy, tox - fromx);
      ctx.beginPath();
      ctx.moveTo(fromx, fromy);
      ctx.lineTo(tox, toy);
      ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
      ctx.moveTo(tox, toy);
      ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
      ctx.stroke();
    }

    // ==================== STENCIL DOM NODES (1-Click Red ❌ & Delete Key) ====================
    function addStencil(type, x, y, customTitle) {
      if (!wbCanvas || !wbCtx) {
        if (splitStudioOpen) initSplitCanvas();
        else initWhiteboardCanvas();
      }
      const cfg = WB_STENCIL_CONFIGS[type] || WB_STENCIL_CONFIGS['pod'];
      const title = customTitle || cfg.title;

      const viewport = document.getElementById(splitStudioOpen ? 'split-viewport' : 'whiteboard-viewport');
      const rect = viewport ? viewport.getBoundingClientRect() : { width: 500, height: 400 };
      
      const posX = (x !== undefined) ? x : Math.floor(40 + Math.random() * Math.max(50, rect.width - 220));
      const posY = (y !== undefined) ? y : Math.floor(40 + Math.random() * Math.max(50, rect.height - 120));
      const id = `wb_node_${Date.now()}_${Math.floor(Math.random() * 1000)}`;

      const nodeObj = {
        id,
        type,
        x: posX,
        y: posY,
        title,
        subtext: cfg.subtext,
        bg: cfg.bg,
        border: cfg.border,
        textColor: cfg.textColor,
        icon: cfg.icon
      };
      wbNodes.push(nodeObj);

      const nodeEl = document.createElement('div');
      nodeEl.id = id;
      nodeEl.className = 'wb-node absolute pointer-events-auto cursor-grab active:cursor-grabbing border rounded-xl shadow-2xl flex flex-col p-2.5 transition-all select-none';
      nodeEl.style.left = `${posX}px`;
      nodeEl.style.top = `${posY}px`;
      nodeEl.style.width = '165px';
      nodeEl.style.backgroundColor = cfg.bg;
      nodeEl.style.borderColor = cfg.border;

      // Includes User-Requested RED ❌ CLOSE BUTTON
      nodeEl.innerHTML = `
        <div class="flex items-center justify-between pb-1 border-b border-white/10 gap-1">
          <span class="flex items-center gap-1.5 text-xs font-bold ${cfg.textColor} truncate">
            <span class="text-sm">${cfg.icon}</span>
            <span id="${id}-label" class="wb-node-title truncate" title="Double click to rename" ondblclick="editWbNodeTitle('${id}', event)">${title}</span>
          </span>
          <button onclick="removeWbNode('${id}', event)" class="w-5 h-5 rounded-full bg-rose-950 hover:bg-rose-600 text-rose-300 hover:text-white flex items-center justify-center text-xs font-black border border-rose-800/80 transition-all shrink-0 shadow" title="Delete stencil (or press Delete key)">
            ✕
          </button>
        </div>
        <div class="mt-1 text-[9px] text-slate-400 font-mono flex items-center justify-between">
          <span class="truncate">${cfg.subtext}</span>
          <span class="w-2 h-2 rounded-full ${cfg.dotColor} shrink-0 ml-1"></span>
        </div>
      `;

      nodeEl.onclick = (e) => selectWbNode(id, e);
      nodeEl.onmousedown = (e) => startDragWbNode(id, e);

      const nodesContainer = document.getElementById(splitStudioOpen ? 'split-nodes' : 'whiteboard-nodes');
      if (nodesContainer) nodesContainer.appendChild(nodeEl);

      updateWbNodeCount();
      selectWbNode(id);
      addXP(10, `Placed ${title}`);
    }

    function removeWbNode(id, event) {
      if (event) event.stopPropagation();
      const el = document.getElementById(id);
      if (el) el.remove();
      wbNodes = wbNodes.filter(n => n.id !== id);
      if (selectedWbNodeId === id) selectedWbNodeId = null;
      updateWbNodeCount();
      showToast('Stencil removed.');
    }

    function selectWbNode(id, event) {
      if (event) event.stopPropagation();
      selectedWbNodeId = id;
      document.querySelectorAll('.wb-node').forEach(node => {
        if (node.id === id) {
          node.classList.add('selected');
        } else {
          node.classList.remove('selected');
        }
      });
    }

    function editWbNodeTitle(id, event) {
      if (event) event.stopPropagation();
      const label = document.getElementById(`${id}-label`);
      if (!label) return;
      const newTitle = prompt('Rename architectural component:', label.innerText);
      if (newTitle && newTitle.trim()) {
        label.innerText = newTitle.trim();
        const node = wbNodes.find(n => n.id === id);
        if (node) node.title = newTitle.trim();
        showToast(`Renamed to "${newTitle.trim()}"`);
      }
    }

    function startDragWbNode(id, event) {
      if (event.target.tagName === 'BUTTON') return;
      isDraggingNode = true;
      dragNodeId = id;
      selectWbNode(id, event);

      const el = document.getElementById(id);
      if (el) {
        const rect = el.getBoundingClientRect();
        dragOffsetX = event.clientX - rect.left;
        dragOffsetY = event.clientY - rect.top;
      }
    }

    function handleWbNodeDrag(e) {
      if (!isDraggingNode || !dragNodeId) return;
      const el = document.getElementById(dragNodeId);
      const viewport = document.getElementById(splitStudioOpen ? 'split-viewport' : 'whiteboard-viewport');
      if (!el || !viewport) return;

      const vRect = viewport.getBoundingClientRect();
      let left = e.clientX - vRect.left - dragOffsetX;
      let top = e.clientY - vRect.top - dragOffsetY;

      left = Math.max(5, Math.min(left, vRect.width - 175));
      top = Math.max(5, Math.min(top, vRect.height - 65));

      el.style.left = `${left}px`;
      el.style.top = `${top}px`;

      const node = wbNodes.find(n => n.id === dragNodeId);
      if (node) {
        node.x = left;
        node.y = top;
      }
    }

    function endWbNodeDrag() {
      isDraggingNode = false;
      dragNodeId = null;
    }

    function updateWbNodeCount() {
      const badge = document.getElementById('wb-node-count');
      if (badge) badge.innerText = `${wbNodes.length} Stencils Active`;
    }

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if ((e.key === 'Delete' || e.key === 'Backspace') && selectedWbNodeId) {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
          e.preventDefault();
          removeWbNode(selectedWbNodeId);
        }
      }
      if (e.key === 'Escape') {
        closeWhiteboardModal();
        closeTrapModal();
      }
    });

    // Combined PNG Export (Canvas strokes + DOM Stencils)
    function downloadWhiteboard() {
      if (!wbCanvas || !wbCtx) return;
      const exportCanvas = document.createElement('canvas');
      exportCanvas.width = wbCanvas.width;
      exportCanvas.height = wbCanvas.height;
      const expCtx = exportCanvas.getContext('2d');

      expCtx.fillStyle = '#030611';
      expCtx.fillRect(0, 0, exportCanvas.width, exportCanvas.height);
      expCtx.drawImage(wbCanvas, 0, 0);

      const scale = window.devicePixelRatio || 1;
      wbNodes.forEach(node => {
        const el = document.getElementById(node.id);
        const x = (el ? el.offsetLeft : node.x) * scale;
        const y = (el ? el.offsetTop : node.y) * scale;
        const w = 165 * scale;
        const h = 55 * scale;

        expCtx.save();
        expCtx.fillStyle = node.bg;
        expCtx.strokeStyle = node.border;
        expCtx.lineWidth = 2 * scale;
        expCtx.beginPath();
        expCtx.roundRect(x, y, w, h, 8 * scale);
        expCtx.fill();
        expCtx.stroke();

        expCtx.fillStyle = '#ffffff';
        expCtx.font = `bold ${10 * scale}px JetBrains Mono, monospace`;
        expCtx.fillText(`${node.icon} ${node.title}`, x + 8 * scale, y + 18 * scale);

        expCtx.fillStyle = '#94a3b8';
        expCtx.font = `${8 * scale}px JetBrains Mono, monospace`;
        expCtx.fillText(node.subtext, x + 8 * scale, y + 40 * scale);
        expCtx.restore();
      });

      const link = document.createElement('a');
      link.download = `Shivam_Architecture_Whiteboard_${Date.now()}.png`;
      link.href = exportCanvas.toDataURL('image/png');
      link.click();
      showToast('Architecture exported to PNG!');
      addXP(50, 'Exported Architecture Diagram');
    }

    function loadTemplate(type) {
      if (!type) return;
      loadDesignOnWhiteboard(type);
    }

    function loadDesignOnWhiteboard(chId) {
      if (!splitStudioOpen) openWhiteboardModal();
      clearWhiteboard();

      setTimeout(() => {
        if (chId === 'ch1') {
          addStencil('gateway', 40, 160, 'Envoy Gateway');
          addStencil('kafka', 220, 160, 'Kafka [128P]');
          addStencil('pod', 380, 160, 'Consumer Pods');
          addStencil('postgres', 540, 160, 'PostgreSQL');
          wbCtx.strokeStyle = '#38bdf8';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 165, 185, 220, 185);
          drawArrow(wbCtx, 345, 185, 380, 185);
          drawArrow(wbCtx, 505, 185, 540, 185);
        } else if (chId === 'ch2') {
          addStencil('pod', 50, 100, 'Worker Pod A');
          addStencil('pod', 50, 240, 'Worker Pod B');
          addStencil('redis', 280, 170, 'Redis Lock Mutex');
          addStencil('postgres', 480, 170, 'PostgreSQL (ver guard)');
          wbCtx.strokeStyle = '#c084fc';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 175, 125, 280, 180);
          drawArrow(wbCtx, 175, 265, 280, 195);
          drawArrow(wbCtx, 405, 195, 480, 195);
        } else if (chId === 'ch3') {
          addStencil('pod', 50, 160, 'Order Service');
          addStencil('postgres', 230, 160, 'Postgres Outbox');
          addStencil('kafka', 410, 160, 'Kafka Topic');
          addStencil('pod', 580, 160, 'Idempotent Consumer');
          wbCtx.strokeStyle = '#34d399';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 175, 185, 230, 185);
          drawArrow(wbCtx, 355, 185, 410, 185);
          drawArrow(wbCtx, 535, 185, 580, 185);
        } else if (chId === 'ch4') {
          addStencil('pod', 60, 160, 'Carrier Web UI');
          addStencil('postgres', 280, 160, 'Postgres (WITH RECURSIVE)');
          addStencil('s3', 500, 160, 'Composite Index');
          wbCtx.strokeStyle = '#fbbf24';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 185, 185, 280, 185);
          drawArrow(wbCtx, 405, 185, 500, 185);
        } else if (chId === 'ch5') {
          addStencil('gateway', 50, 160, 'Operator Browser');
          addStencil('llm', 260, 160, 'Edge LLM (4-bit GGUF)');
          addStencil('s3', 480, 160, 'Vector DB');
          wbCtx.strokeStyle = '#2dd4bf';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 175, 185, 260, 185);
          drawArrow(wbCtx, 385, 185, 480, 185);
        } else if (chId === 'ch6') {
          addStencil('gnodeb', 50, 160, '20M 5G gNodeBs');
          addStencil('kafka', 230, 160, 'Kafka Telemetry');
          addStencil('prom', 410, 160, 'Multi-Burn Prometheus');
          addStencil('pod', 580, 160, 'PagerDuty Alert');
          wbCtx.strokeStyle = '#f43f5e';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 175, 185, 230, 185);
          drawArrow(wbCtx, 355, 185, 410, 185);
          drawArrow(wbCtx, 535, 185, 580, 185);
        } else if (chId === 'ch7') {
          addStencil('s3', 50, 160, '2GB XML Stream');
          addStencil('pod', 240, 160, 'StAX Pull Reader');
          addStencil('postgres', 440, 160, 'Oracle Direct-Path');
          wbCtx.strokeStyle = '#38bdf8';
          wbCtx.lineWidth = 3;
          drawArrow(wbCtx, 175, 185, 240, 185);
          drawArrow(wbCtx, 365, 185, 440, 185);
        }
        saveWbState();
        showToast(`Loaded ${chId.toUpperCase()} topology onto Whiteboard!`);
      }, 100);
    }

    // ==================== GAMIFICATION XP & LEVEL ENGINE ====================
    function addXP(amount, reason) {
      appState.xp = (appState.xp || 1450) + amount;
      let newLevel = 'L5 Senior Engineer';
      if (appState.xp >= 5000) newLevel = 'L8 Principal Architect';
      else if (appState.xp >= 2500) newLevel = 'L7 Senior Staff Architect';
      else if (appState.xp >= 1000) newLevel = 'L6 Staff Architect';

      const leveledUp = (newLevel !== appState.level);
      appState.level = newLevel;
      saveState();
      updateXpDisplay();

      if (leveledUp) {
        showToast(`🎉 PROMOTION! Promoted to ${newLevel}! (${appState.xp} XP)`);
      } else {
        showToast(`+${amount} XP: ${reason}! Total: ${appState.xp} XP`);
      }
    }

    function updateXpDisplay() {
      const xpEl = document.getElementById('xp-display');
      const lvlEl = document.getElementById('level-badge');
      if (xpEl) xpEl.innerText = (appState.xp || 1450).toLocaleString();
      if (lvlEl) lvlEl.innerText = (appState.level || 'L6 STAFF ARCHITECT').toUpperCase();
    }

    // ==================== MODULE FLASHCARD ENGINE ====================
    function flipModuleCard(chId) {
      const card = document.getElementById(`${chId}-card`);
      if (card) card.classList.toggle('flipped');
    }

    function rateModuleCard(chId, rating) {
      if (!appState.recall) appState.recall = {};
      appState.recall[chId] = rating;
      saveState();

      const badge = document.getElementById(`${chId}-recall-badge`);
      if (badge) {
        if (rating === 'Mastered') {
          badge.className = 'px-2.5 py-1 rounded-lg bg-emerald-950/80 border border-emerald-700 text-emerald-300 text-xs font-mono font-bold';
          badge.innerText = 'Status: ✅ Mastered';
          addXP(50, `Mastered ${chId.toUpperCase()} Recall`);
        } else {
          badge.className = 'px-2.5 py-1 rounded-lg bg-amber-950/80 border border-amber-700 text-amber-300 text-xs font-mono font-bold';
          badge.innerText = `Status: ${rating}`;
          addXP(10, `Reviewed ${chId.toUpperCase()}`);
        }
      }
      updateProgress();
    }

    // ==================== POMODORO FOCUS TIMER ====================
    let pomoSeconds = 25 * 60;
    let pomoTimer = null;
    let pomoRunning = false;

    function updatePomoDisplay() {
      const m = Math.floor(pomoSeconds / 60).toString().padStart(2, '0');
      const s = (pomoSeconds % 60).toString().padStart(2, '0');
      const el = document.getElementById('pomo-display');
      if (el) el.innerText = `${m}:${s}`;
    }

    function togglePomodoro() {
      const btn = document.getElementById('btn-pomo-toggle');
      if (!pomoRunning) {
        pomoRunning = true;
        if (btn) { btn.innerText = 'Pause'; btn.className = 'px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[10px]'; }
        pomoTimer = setInterval(() => {
          if (pomoSeconds > 0) {
            pomoSeconds--;
            updatePomoDisplay();
          } else {
            clearInterval(pomoTimer);
            pomoRunning = false;
            addXP(100, 'Completed 25m Focus Block');
            showToast('Pomodoro focus cycle complete! Earned 100 XP!');
            resetPomodoro();
          }
        }, 1000);
      } else {
        clearInterval(pomoTimer);
        pomoRunning = false;
        if (btn) { btn.innerText = 'Resume'; btn.className = 'px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]'; }
      }
    }

    function resetPomodoro() {
      clearInterval(pomoTimer);
      pomoRunning = false;
      pomoSeconds = 25 * 60;
      updatePomoDisplay();
      const btn = document.getElementById('btn-pomo-toggle');
      if (btn) { btn.innerText = 'Start'; btn.className = 'px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 text-[10px]'; }
    }

    // ==================== CLOZE DELETION BLUR MODE ====================
    let clozeActive = false;
    function toggleClozeMode() {
      clozeActive = !clozeActive;
      document.body.classList.toggle('cloze-mode', clozeActive);
      showToast(clozeActive ? 'Cloze Mode ON: Critical terms blurred for active recall!' : 'Cloze Mode OFF: Full text visible.');
    }

    // ==================== TTS & AUDIO RECORDER ====================
    let isSpeaking = false;
    function readAloudPitch(chId) {
      if (!('speechSynthesis' in window)) {
        showToast('Web Speech API is not supported in this browser.');
        return;
      }
      if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        const btnLabel = document.getElementById(`${chId}-tts-label`);
        if (btnLabel) btnLabel.innerText = 'Listen to L6 Pitch';
        return;
      }

      const textEl = document.getElementById(`${chId}-pitch-text`);
      if (!textEl) return;
      const utterance = new SpeechSynthesisUtterance(textEl.innerText);
      utterance.rate = 1.0;
      const voices = window.speechSynthesis.getVoices();
      const googleVoice = voices.find(v => v.name.includes('Google') || v.lang === 'en-US');
      if (googleVoice) utterance.voice = googleVoice;

      const btnLabel = document.getElementById(`${chId}-tts-label`);
      utterance.onstart = () => { isSpeaking = true; if (btnLabel) btnLabel.innerText = 'Pause Pitch'; };
      utterance.onend = utterance.onerror = () => { isSpeaking = false; if (btnLabel) btnLabel.innerText = 'Listen to L6 Pitch'; };

      window.speechSynthesis.speak(utterance);
      showToast('Playing authoritative L6 Whiteboard Pitch audio...');
    }

    let mediaRecorders = {};
    let recordedChunks = {};
    let recordTimers = {};
    let recordDurations = {};

    async function toggleVoiceRecording(chId) {
      const btn = document.getElementById(`${chId}-mic-btn`);
      const label = document.getElementById(`${chId}-mic-label`);
      const timerEl = document.getElementById(`${chId}-timer`);
      const audioEl = document.getElementById(`${chId}-audio`);

      if (mediaRecorders[chId] && mediaRecorders[chId].state === 'recording') {
        mediaRecorders[chId].stop();
        clearInterval(recordTimers[chId]);
        if (label) label.innerText = 'Re-record Pitch';
        if (btn) btn.className = 'px-3 py-1.5 rounded-lg bg-slate-800 text-slate-200 font-semibold text-xs flex items-center gap-1.5';
        showToast('Pitch recorded! Play back to self-evaluate.');
        addXP(75, 'Recorded Whiteboard Pitch');
        return;
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        mediaRecorders[chId] = recorder;
        recordedChunks[chId] = [];
        recordDurations[chId] = 0;

        recorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks[chId].push(e.data); };
        recorder.onstop = () => {
          const blob = new Blob(recordedChunks[chId], { type: 'audio/webm' });
          if (audioEl) { audioEl.src = URL.createObjectURL(blob); audioEl.classList.remove('hidden'); }
          stream.getTracks().forEach(track => track.stop());
        };

        recorder.start();
        if (label) label.innerText = 'Stop Recording';
        if (btn) btn.className = 'px-3 py-1.5 rounded-lg bg-red-600 text-white font-semibold text-xs flex items-center gap-1.5 animate-pulse';

        recordTimers[chId] = setInterval(() => {
          recordDurations[chId]++;
          const m = Math.floor(recordDurations[chId] / 60).toString().padStart(2, '0');
          const s = (recordDurations[chId] % 60).toString().padStart(2, '0');
          if (timerEl) timerEl.innerText = `${m}:${s} / 02:00`;
          if (recordDurations[chId] >= 120) toggleVoiceRecording(chId);
        }, 1000);

        showToast('Recording started: Deliver your 2-minute whiteboard pitch!');
      } catch (err) {
        showToast('Microphone access denied or unavailable.');
      }
    }

    // ==================== SURPRISE TRAP QUESTIONS DRILL ====================
    const TRAPS_POOL = [
      {
        q: "What if a network partition splits your Redis cluster in half during a cell re-configuration? Which side wins?",
        a: "Redis Sentinel or Cluster majority quorum dictates the winning master. However, because Redis asynchronous replication is not strictly linearizable, downstream storage MUST enforce fencing tokens (WHERE version < token) to reject zombie writes from the isolated partition."
      },
      {
        q: "Why didn't you use distributed 2-Phase Commit (2PC / XA transactions) between PostgreSQL and Kafka?",
        a: "2PC requires distributed locks held across network round-trips, destroying throughput (dropping QPS by 10x-50x) and creating single-point-of-failure coordinator deadlocks. The Transactional Outbox pattern provides local ACID atomicity with asynchronous CDC streaming, achieving 45k TPS with zero cross-network locking."
      },
      {
        q: "In your 5G SRE alerting, what happens if an upstream scraping agent fails and metrics drop to zero? Does your multi-burn alert fire?",
        a: "Pure error rate PromQL expressions evaluate to NaN when traffic is zero. A Staff-level rule pairs burn-rate alerting with an absent_over_time() watchdog probe that pages SREs if telemetry ceases for >90 seconds."
      }
    ];

    let trapTimer = null;
    let trapSeconds = 60;

    function triggerRandomTrapQuestion() {
      const modal = document.getElementById('trap-modal');
      const qText = document.getElementById('trap-question-text');
      const reveal = document.getElementById('trap-answer-reveal');
      const timerEl = document.getElementById('trap-timer');
      const btnReveal = document.getElementById('btn-reveal-trap');

      const trap = TRAPS_POOL[Math.floor(Math.random() * TRAPS_POOL.length)];
      if (qText) qText.innerText = `"${trap.q}"`;
      if (reveal) {
        reveal.innerHTML = `<strong>The Staff Defense:</strong> "${trap.a}"`;
        reveal.classList.add('hidden');
      }
      if (btnReveal) btnReveal.innerText = 'Reveal Defense (+150 XP)';

      trapSeconds = 60;
      if (timerEl) timerEl.innerText = '60s';
      if (modal) modal.classList.remove('hidden');

      clearInterval(trapTimer);
      trapTimer = setInterval(() => {
        trapSeconds--;
        if (timerEl) timerEl.innerText = `${trapSeconds}s`;
        if (trapSeconds <= 0) {
          clearInterval(trapTimer);
          revealTrapAnswer();
        }
      }, 1000);
    }

    function revealTrapAnswer() {
      clearInterval(trapTimer);
      const reveal = document.getElementById('trap-answer-reveal');
      if (reveal) reveal.classList.remove('hidden');
      const btnReveal = document.getElementById('btn-reveal-trap');
      if (btnReveal) btnReveal.innerText = 'Defense Revealed';
      addXP(150, 'Answered L6 Trap Drill');
    }

    function closeTrapModal() {
      clearInterval(trapTimer);
      const modal = document.getElementById('trap-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ==================== SEARCH & PROGRESS ====================
    function handleSearch(query) {
      if (!query || query.length < 2) return;
      const q = query.toLowerCase();
      for (let i = 1; i <= 12; i++) {
        const sec = document.getElementById(`stage-${i}`);
        if (sec && sec.innerText.toLowerCase().includes(q)) {
          goToStage(i);
          showToast(`Found match in Stage ${i}`);
          break;
        }
      }
    }

    function saveState() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
    }

    function updateProgress() {
      let masteredCount = 0;
      for (let k in appState.chapters) {
        if (appState.chapters[k]) masteredCount++;
      }
      for (let k in appState.recall) {
        if (appState.recall[k] === 'Mastered') masteredCount += 0.5;
      }

      const totalItems = 7 + 3.5;
      const pct = Math.min(100, Math.round((masteredCount / totalItems) * 100));

      const pBar = document.getElementById('progress-bar');
      const pText = document.getElementById('progress-percent');
      if (pBar) pBar.style.width = `${pct}%`;
      if (pText) pText.innerText = `${pct}%`;

      for (let i = 1; i <= 7; i++) {
        const dot = document.getElementById(`nav-ch${i}-status`);
        if (dot) {
          dot.className = appState.chapters[`ch${i}`] ? 'w-2 h-2 rounded-full bg-emerald-400 shrink-0' : 'w-2 h-2 rounded-full bg-slate-700 shrink-0';
        }
      }
    }

    function toggleChapter(chId) {
      const el = document.getElementById(`${chId}-check`);
      appState.chapters[chId] = el.checked;
      saveState();
      updateProgress();
      if (el.checked) addXP(100, `Completed Stage ${chId.toUpperCase()}`);
    }

    function exportAllStudyNotes() {
      let content = '# NEXUS ARCHITECT: Shivam Agarwal Google L6 Study Notes\\n\\n';
      content += `Generated on: ${new Date().toISOString()}\\n\\n`;
      for (let i = 1; i <= 7; i++) {
        const noteArea = document.getElementById(`ch${i}-notes-area`);
        const text = noteArea ? noteArea.value : '';
        content += `## Stage ${i} Notes\\n${text || '*(No notes recorded)*'}\\n\\n`;
      }
      const blob = new Blob([content], { type: 'text/markdown;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `Shivam_Agarwal_Google_L6_Study_Notes_${Date.now()}.md`;
      link.click();
      showToast('Exported all study notes to Markdown!');
      addXP(50, 'Exported Study Notes');
    }

    function copyCode(elementId) {
      const codeEl = document.getElementById(elementId);
      if (codeEl) {
        navigator.clipboard.writeText(codeEl.innerText).then(() => {
          showToast('Code copied to clipboard!');
        });
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      const toastMsg = document.getElementById('toast-msg');
      if (!toast || !toastMsg) return;
      toastMsg.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => { toast.classList.remove('show'); }, 3000);
    }


    // ==================== VIDEO MODAL ====================
    function openVideoModal(videoId, title) {
      const modal = document.getElementById('video-modal');
      const iframe = document.getElementById('video-modal-iframe');
      const titleEl = document.getElementById('video-modal-title');
      if (titleEl) titleEl.innerText = title;
      if (iframe && videoId) {
        iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
      }
      if (modal) modal.classList.remove('hidden');
    }

    function closeVideoModal() {
      const modal = document.getElementById('video-modal');
      const iframe = document.getElementById('video-modal-iframe');
      if (iframe) iframe.src = '';
      if (modal) modal.classList.add('hidden');
    }

    // ==================== CODE TAB SWITCHING ====================
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

    // ==================== ADVANCED INTERACTIVE SIMULATORS ====================
    let zeroCopyMode = 'traditional';
    let zcPackets = [];
    let zcAnimId = null;

    function setZeroCopyMode(mode) {
      zeroCopyMode = mode;
      const btnTrad = document.getElementById('btn-mode-trad');
      const btnZero = document.getElementById('btn-mode-zero');
      if (mode === 'zerocopy') {
        if (btnZero) { btnZero.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-cyan-950 text-cyan-300 border border-cyan-800'; }
        if (btnTrad) { btnTrad.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800'; }
        document.getElementById('zc-stat-cpu-copies').innerText = '0 Copies (DMA Only)';
        document.getElementById('zc-stat-cpu-copies').className = 'font-bold text-emerald-400 text-sm';
        document.getElementById('zc-stat-switches').innerText = '2 Switches';
        document.getElementById('zc-stat-switches').className = 'font-bold text-emerald-400 text-sm';
        document.getElementById('zc-stat-heap').innerText = '0 MB/s (Zero Heap)';
        document.getElementById('zc-stat-heap').className = 'font-bold text-emerald-400 text-sm';
        document.getElementById('zc-stat-tps').innerText = '45,000 TPS (Wire Speed)';
        document.getElementById('zc-stat-tps').className = 'font-bold text-emerald-400 text-sm';
        showToast('Zero-Copy sendfile() active: 0 CPU copies, 0 Heap churn!');
      } else {
        if (btnTrad) { btnTrad.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-rose-950 text-rose-300 border border-rose-800'; }
        if (btnZero) { btnZero.className = 'px-3 py-1 rounded-lg text-xs font-semibold bg-slate-900 text-slate-400 border border-slate-800'; }
        document.getElementById('zc-stat-cpu-copies').innerText = '2 Copies (Kernel <-> User)';
        document.getElementById('zc-stat-cpu-copies').className = 'font-bold text-rose-400 text-sm';
        document.getElementById('zc-stat-switches').innerText = '4 Switches';
        document.getElementById('zc-stat-switches').className = 'font-bold text-rose-400 text-sm';
        document.getElementById('zc-stat-heap').innerText = '45 MB/s Young Gen';
        document.getElementById('zc-stat-heap').className = 'font-bold text-rose-400 text-sm';
        document.getElementById('zc-stat-tps').innerText = '18,500 TPS (GC Limited)';
        document.getElementById('zc-stat-tps').className = 'font-bold text-rose-400 text-sm';
        showToast('Traditional mode: 4 context switches, 2 CPU copies, GC pressure active.');
      }
    }

    function initZeroCopyCanvas() {
      const canvas = document.getElementById('zc-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.parentElement.clientWidth * dpr;
      canvas.height = canvas.parentElement.clientHeight * dpr;
      ctx.scale(dpr, dpr);

      const W = canvas.parentElement.clientWidth;
      const H = canvas.parentElement.clientHeight;

      const nodes = [
        { name: 'NVMe Disk', x: W * 0.1, y: H * 0.5, color: '#38bdf8' },
        { name: 'OS PageCache', x: W * 0.3, y: H * 0.5, color: '#34d399' },
        { name: 'JVM Heap Buffer', x: W * 0.5, y: H * 0.25, color: '#c084fc' },
        { name: 'Socket Buffer', x: W * 0.7, y: H * 0.5, color: '#818cf8' },
        { name: '10 GbE NIC DMA', x: W * 0.9, y: H * 0.5, color: '#38bdf8' }
      ];

      function renderZC() {
        ctx.clearRect(0, 0, W, H);

        // Draw connections
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#1e293b';
        ctx.beginPath();
        if (zeroCopyMode === 'traditional') {
          // Disk -> PageCache -> JVM -> Socket -> NIC
          ctx.moveTo(nodes[0].x, nodes[0].y);
          ctx.lineTo(nodes[1].x, nodes[1].y);
          ctx.lineTo(nodes[2].x, nodes[2].y);
          ctx.lineTo(nodes[3].x, nodes[3].y);
          ctx.lineTo(nodes[4].x, nodes[4].y);
        } else {
          // Zero-Copy: Disk -> PageCache -> NIC directly!
          ctx.moveTo(nodes[0].x, nodes[0].y);
          ctx.lineTo(nodes[1].x, nodes[1].y);
          ctx.lineTo(nodes[4].x, nodes[4].y);
        }
        ctx.stroke();

        // Draw Nodes
        nodes.forEach((n, idx) => {
          if (zeroCopyMode === 'zerocopy' && (idx === 2 || idx === 3)) {
            // Faded bypassed nodes
            ctx.fillStyle = '#0f172a';
            ctx.strokeStyle = '#334155';
          } else {
            ctx.fillStyle = '#0b1329';
            ctx.strokeStyle = n.color;
          }
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(n.x - 45, n.y - 20, 90, 40, 8);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = (zeroCopyMode === 'zerocopy' && (idx === 2 || idx === 3)) ? '#475569' : '#f8fafc';
          ctx.font = '10px monospace';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(n.name, n.x, n.y);
        });

        // Spawn packets
        if (Math.random() < 0.15) {
          zcPackets.push({ progress: 0, speed: zeroCopyMode === 'zerocopy' ? 0.025 : 0.015 });
        }

        // Animate packets
        for (let i = zcPackets.length - 1; i >= 0; i--) {
          const p = zcPackets[i];
          p.progress += p.speed;
          if (p.progress >= 1) {
            zcPackets.splice(i, 1);
            continue;
          }

          let px, py;
          if (zeroCopyMode === 'traditional') {
            const seg = p.progress * 4;
            const idx = Math.floor(seg);
            const frac = seg - idx;
            if (idx < 4) {
              px = nodes[idx].x + (nodes[idx+1].x - nodes[idx].x) * frac;
              py = nodes[idx].y + (nodes[idx+1].y - nodes[idx].y) * frac;
            }
          } else {
            // Direct PageCache to NIC
            if (p.progress < 0.25) {
              const frac = p.progress / 0.25;
              px = nodes[0].x + (nodes[1].x - nodes[0].x) * frac;
              py = nodes[0].y + (nodes[1].y - nodes[0].y) * frac;
            } else {
              const frac = (p.progress - 0.25) / 0.75;
              px = nodes[1].x + (nodes[4].x - nodes[1].x) * frac;
              py = nodes[1].y + (nodes[4].y - nodes[1].y) * frac;
            }
          }

          ctx.fillStyle = zeroCopyMode === 'zerocopy' ? '#38bdf8' : '#fb7185';
          ctx.beginPath();
          ctx.arc(px, py, 4, 0, Math.PI * 2);
          ctx.fill();
        }

        zcAnimId = requestAnimationFrame(renderZC);
      }
      renderZC();
    }

    // ==================== RAFT CONSENSUS SIMULATOR ====================
    let raftTerm = 1;
    let raftLeader = 1;
    let raftPartitioned = false;
    let raftCommitIndex = 104;

    function raftPartitionLeader() {
      raftPartitioned = true;
      raftTerm++;
      raftLeader = 2; // Node 2 becomes new leader of majority partition
      const statusEl = document.getElementById('raft-log-status');
      if (statusEl) {
        statusEl.innerHTML = `<span class="text-rose-400 font-bold">⚠️ NETWORK PARTITION ACTIVE!</span> Node 1 isolated in minority partition. Majority partition (Nodes 2,3,4,5) elected <strong>Node 2</strong> as Leader in <strong>Term ${raftTerm}</strong>. Quorum maintained!`;
      }
      drawRaft();
      showToast('Network partition: Leader 1 isolated, majority elected Leader 2!');
    }

    function raftHealNetwork() {
      raftPartitioned = false;
      const statusEl = document.getElementById('raft-log-status');
      if (statusEl) {
        statusEl.innerHTML = `<span class="text-emerald-400 font-bold">✔ NETWORK HEALED:</span> Node 1 detected higher Term ${raftTerm} and stepped down to Follower. Node 2 remains stable Leader. All 5 nodes synchronized!`;
      }
      drawRaft();
      showToast('Network healed: Stale leader stepped down, cluster unified.');
    }

    function raftSubmitTx() {
      raftCommitIndex++;
      const statusEl = document.getElementById('raft-log-status');
      if (statusEl) {
        statusEl.innerHTML = `Write committed at Index <strong>#${raftCommitIndex}</strong> (Term ${raftTerm}). Replicated to majority quorum (Nodes 2, 3, 4). State Machine updated!`;
      }
      drawRaft(true);
      showToast(`Transaction #${raftCommitIndex} committed across Raft quorum!`);
      addXP(25, 'Committed Raft Transaction');
    }

    function drawRaft(highlightTx = false) {
      const canvas = document.getElementById('raft-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.parentElement.clientWidth * dpr;
      canvas.height = canvas.parentElement.clientHeight * dpr;
      ctx.scale(dpr, dpr);

      const W = canvas.parentElement.clientWidth;
      const H = canvas.parentElement.clientHeight;
      ctx.clearRect(0, 0, W, H);

      const cx = W / 2;
      const cy = H / 2;
      const R = Math.min(W, H) * 0.35;

      const nodes = [
        { id: 1, label: 'Node 1' },
        { id: 2, label: 'Node 2' },
        { id: 3, label: 'Node 3' },
        { id: 4, label: 'Node 4' },
        { id: 5, label: 'Node 5' }
      ];

      // Draw mesh lines
      ctx.lineWidth = 1;
      ctx.strokeStyle = '#1e293b';
      for (let i = 0; i < 5; i++) {
        for (let j = i + 1; j < 5; j++) {
          const a1 = (i * 2 * Math.PI) / 5 - Math.PI / 2;
          const a2 = (j * 2 * Math.PI) / 5 - Math.PI / 2;
          const x1 = cx + R * Math.cos(a1);
          const y1 = cy + R * Math.sin(a1);
          const x2 = cx + R * Math.cos(a2);
          const y2 = cy + R * Math.sin(a2);

          // If partitioned, don't draw link to Node 1
          if (raftPartitioned && (i === 0 || j === 0)) {
            ctx.setLineDash([4, 4]);
            ctx.strokeStyle = '#450a0a';
          } else {
            ctx.setLineDash([]);
            ctx.strokeStyle = '#1e293b';
          }
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
        }
      }
      ctx.setLineDash([]);

      // Draw nodes
      nodes.forEach((n, idx) => {
        const angle = (idx * 2 * Math.PI) / 5 - Math.PI / 2;
        const x = cx + R * Math.cos(angle);
        const y = cy + R * Math.sin(angle);

        const isLeader = (n.id === raftLeader);
        const isIsolated = (raftPartitioned && n.id === 1);

        ctx.fillStyle = isLeader ? '#042f2e' : (isIsolated ? '#450a0a' : '#0b1329');
        ctx.strokeStyle = isLeader ? '#2dd4bf' : (isIsolated ? '#f43f5e' : '#38bdf8');
        ctx.lineWidth = isLeader ? 3 : 1.5;

        ctx.beginPath();
        ctx.arc(x, y, 24, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(n.label, x, y - 4);

        ctx.font = '8px monospace';
        ctx.fillStyle = isLeader ? '#2dd4bf' : (isIsolated ? '#f43f5e' : '#94a3b8');
        ctx.fillText(isLeader ? 'LEADER' : (isIsolated ? 'STALE' : 'FOLLOWER'), x, y + 8);
      });
    }

    // ==================== CONSISTENT HASH RING ====================
    let currentVNodes = 150;
    function setVNodes(v) {
      currentVNodes = v;
      drawHashRing();
      showToast(`Set Virtual Nodes per physical node: ${v}`);
    }

    function drawHashRing() {
      const canvas = document.getElementById('hash-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.parentElement.clientWidth * dpr;
      canvas.height = canvas.parentElement.clientHeight * dpr;
      ctx.scale(dpr, dpr);

      const W = canvas.parentElement.clientWidth;
      const H = canvas.parentElement.clientHeight;
      ctx.clearRect(0, 0, W, H);

      const cx = W / 2;
      const cy = H / 2;
      const R = Math.min(W, H) * 0.38;

      // Draw Main Ring
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.stroke();

      const colors = ['#38bdf8', '#c084fc', '#34d399', '#fbbf24'];
      const totalPoints = 4 * currentVNodes;

      // Draw Virtual Node points
      for (let i = 0; i < totalPoints; i++) {
        // pseudo-random deterministic distribution based on murmur hash
        const hashFrac = ((i * 2654435761) % (2**32)) / (2**32);
        const angle = hashFrac * Math.PI * 2;
        const px = cx + R * Math.cos(angle);
        const py = cy + R * Math.sin(angle);

        ctx.fillStyle = colors[i % 4];
        ctx.beginPath();
        ctx.arc(px, py, currentVNodes > 50 ? 1.5 : 3, 0, Math.PI * 2);
        ctx.fill();
      }

      // Center Stat
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${currentVNodes * 4} Virtual Nodes`, cx, cy - 8);
      ctx.font = '10px monospace';
      ctx.fillStyle = currentVNodes > 50 ? '#34d399' : '#f87171';
      ctx.fillText(currentVNodes > 50 ? 'StdDev σ: 2.1% (Balanced)' : 'StdDev σ: 38.4% (Hotspotting!)', cx, cy + 10);
    }

    // ==================== TOKEN BUCKET SIMULATOR ====================
    let bucketTokens = 80;
    const bucketMax = 100;
    function injectBurst(count) {
      bucketTokens = Math.max(0, bucketTokens - count);
      drawTokenBucket();
      showToast(`Injected burst: ${count} tokens drained!`);
    }

    function drawTokenBucket() {
      const canvas = document.getElementById('tb-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.parentElement.clientWidth * dpr;
      canvas.height = canvas.parentElement.clientHeight * dpr;
      ctx.scale(dpr, dpr);

      const W = canvas.parentElement.clientWidth;
      const H = canvas.parentElement.clientHeight;
      ctx.clearRect(0, 0, W, H);

      const bx = W * 0.4;
      const bw = W * 0.2;
      const by = H * 0.2;
      const bh = H * 0.6;

      // Draw Bucket Container
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(bx, by);
      ctx.lineTo(bx, by + bh);
      ctx.lineTo(bx + bw, by + bh);
      ctx.lineTo(bx + bw, by);
      ctx.stroke();

      // Draw Water / Tokens Fill
      const fillHeight = (bucketTokens / bucketMax) * bh;
      ctx.fillStyle = 'rgba(56, 189, 248, 0.35)';
      ctx.fillRect(bx + 2, by + bh - fillHeight, bw - 4, fillHeight);

      // Label
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`Tokens: ${bucketTokens} / ${bucketMax}`, bx + bw / 2, by + bh / 2);
    }

    // ==================== EXAM CHECKER ====================
    function checkExamAnswer(qNum, choice) {
      const fb = document.getElementById(`q${qNum}-feedback`);
      const scoreEl = document.getElementById('exam-score');
      if (!fb) return;

      if (qNum === 1 && choice === 'B') {
        fb.className = 'p-3 rounded-lg text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono mt-2';
        fb.innerHTML = '✔ CORRECT (Google Staff Choice): As Martin Kleppmann showed, locks cannot guarantee mutual exclusion in asynchronous networks without storage-level fencing. Monotonic tokens prevent stale writes regardless of GC pauses.';
        fb.classList.remove('hidden');
        if (scoreEl) scoreEl.innerText = 'Score: 100 / 100 (Google L6 Staff)';
        addXP(100, 'Bar-Raiser Exam Passed');
      } else {
        fb.className = 'p-3 rounded-lg text-xs bg-rose-950 text-rose-300 border border-rose-800 font-mono mt-2';
        fb.innerHTML = '✖ SUB-OPTIMAL (L5 Fallacy): Modifying timeouts or retry loops does not eliminate the asynchronous pause hazard. Without downstream fencing, stale workers will overwrite state.';
        fb.classList.remove('hidden');
      }
    }


    // ==================== INIT ENGINE ====================
    window.addEventListener('DOMContentLoaded', () => {
      for (let i = 1; i <= 7; i++) {
        const chk = document.getElementById(`ch${i}-check`);
        if (chk && appState.chapters[`ch${i}`]) chk.checked = true;

        const note = document.getElementById(`ch${i}-notes-area`);
        if (note) {
          note.value = appState.notes[`ch${i}`] || '';
          note.addEventListener('input', (e) => {
            appState.notes[`ch${i}`] = e.target.value;
            saveState();
          });
        }

        const rating = appState.recall ? appState.recall[`ch${i}`] : null;
        if (rating) {
          const badge = document.getElementById(`ch${i}-recall-badge`);
          if (badge) {
            badge.innerText = (rating === 'Mastered') ? 'Status: ✅ Mastered' : `Status: ${rating}`;
            if (rating === 'Mastered') badge.className = 'px-2.5 py-1 rounded-lg bg-emerald-950/80 border border-emerald-700 text-emerald-300 text-xs font-mono font-bold';
          }
        }
      }

      updateXpDisplay();
      goToStage(activeStage);
      updateProgress();
    });
  </script>

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

</body>
</html>
""")

final_html = "".join(html_parts)

# Write to workspace
out_path = "d:/Antigravity/Shivam_Staff_Engineer_Mastery_Roadmap.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_html)
print(f"[OK] Generated: {out_path} ({len(final_html)} bytes)")

# Mirror to brain artifact
brain_path = "C:/Users/shiva/.gemini/antigravity/brain/623354e4-df8d-442a-a628-1971c1a87479/Shivam_Staff_Engineer_Mastery_Roadmap.html"
try:
    shutil.copyfile(out_path, brain_path)
    print(f"[OK] Mirrored to brain artifact: {brain_path}")
except Exception as e:
    print(f"[WARN] Brain mirror error: {e}")
