# patch_build_cockpit.py
# Applies deep technical upgrades to build_cockpit.py

with open("d:/Antigravity/build_cockpit.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update the loop that builds red_flags, videos, traps
old_loop_chunk = """    # Build red flags
    red_flags_html = ""
    for rf in tldr.get("red_flags", []):
        red_flags_html += f\"\"\"
          <li class="flex items-start gap-1.5 text-xs text-rose-300/90">
            <span class="text-rose-500 font-bold shrink-0">✕</span>
            <span>{rf}</span>
          </li>
        \"\"\"

    # Build videos
    videos_html = ""
    for v in videos:
        videos_html += f\"\"\"
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-2">
            <div>
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white truncate">{v["title"]}</span>
                <span class="text-[9px] text-cyan-400 bg-cyan-950 px-1.5 py-0.5 rounded font-mono">{v["event"]}</span>
              </div>
              <div class="text-[11px] text-slate-400 font-mono mt-0.5">Speaker: {v["speaker"]}</div>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">{v["takeaway"]}</p>
            </div>
            <a href="{v["url"]}" target="_blank" class="inline-flex items-center gap-1 text-xs font-semibold text-cyan-400 hover:text-cyan-300 pt-2 border-t border-slate-800">
              <span>▶ Watch Lecture Reference</span>
              <span>&rarr;</span>
            </a>
          </div>
        \"\"\"

    traps_html = ""
    for idx, (q, a) in enumerate(mod["traps"]):
        border_cls = "pt-3 border-t border-slate-800" if idx > 0 else ""
        traps_html += f\"\"\"
          <div class="{border_cls}">
            <span class="font-bold text-white text-xs block">Q{idx+1}: "{q}"</span>
            <p class="text-xs text-slate-400 mt-1">
              <strong>Your Defense:</strong> <em>"{a}"</em>
            </p>
          </div>
        \"\"\""""

new_loop_chunk = """    # Build red flags with Junior vs Staff distinction
    red_flags_html = ""
    for rf in tldr.get("red_flags", []):
        if isinstance(rf, dict):
            red_flags_html += f\"\"\"
              <li class="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1 text-xs">
                <div class="text-rose-400 font-bold flex items-start gap-1.5"><span class="text-rose-500 font-bold shrink-0">✕ Junior Fallacy:</span> <span>{rf.get('junior', '')}</span></div>
                <div class="text-emerald-300 flex items-start gap-1.5"><span class="text-emerald-400 font-bold shrink-0">✔ Staff Defense:</span> <span>{rf.get('staff', '')}</span></div>
              </li>
            \"\"\"
        else:
            red_flags_html += f\"\"\"
              <li class="flex items-start gap-1.5 text-xs text-rose-300/90">
                <span class="text-rose-500 font-bold shrink-0">✕</span>
                <span>{rf}</span>
              </li>
            \"\"\"

    # Build battle scars
    battle_scars_html = ""
    for bs in tldr.get("battle_scars", []):
        battle_scars_html += f\"\"\"
          <div class="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800 text-[11px] text-slate-300 space-y-0.5">
            <span class="text-amber-400 font-bold block">⚡ Production Battle Scar:</span>
            <p>{bs}</p>
          </div>
        \"\"\"

    # Build invariants
    invariants_html = ""
    for inv in tldr.get("invariants", []):
        invariants_html += f\"\"\"
          <li class="flex items-start gap-2 text-xs text-slate-300">
            <span class="text-cyan-400 font-bold shrink-0">❖</span>
            <span>{inv}</span>
          </li>
        \"\"\"

    # Build videos with embedded modal trigger & timestamps
    videos_html = ""
    for v in videos:
        timestamps_html = ""
        for ts in v.get("timestamps", []):
            timestamps_html += f\"\"\"
              <div class="flex items-center gap-2 text-[10px] text-slate-400 font-mono">
                <span class="text-cyan-400 font-bold">[{ts.get('time', '')}]</span>
                <span>{ts.get('topic', '')}</span>
              </div>
            \"\"\"
        
        quote_html = ""
        if v.get("quote"):
            quote_html = f\"\"\"
              <div class="p-2 bg-slate-900/90 rounded border border-cyan-900/30 text-[11px] text-cyan-200 italic">
                💬 "{v.get('quote')}"
              </div>
            \"\"\"

        safe_title = v["title"].replace("'", "")
        vid_id = v.get("videoId", "")
        videos_html += f\"\"\"
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
        \"\"\"

    traps_html = ""
    for idx, trap in enumerate(mod.get("traps", [])):
        if isinstance(trap, dict):
            border_cls = "pt-4 border-t border-slate-800" if idx > 0 else ""
            traps_html += f\"\"\"
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
            \"\"\"
        elif isinstance(trap, (list, tuple)) and len(trap) >= 2:
            q, a = trap[0], trap[1]
            border_cls = "pt-3 border-t border-slate-800" if idx > 0 else ""
            traps_html += f\"\"\"
              <div class="{border_cls}">
                <span class="font-bold text-white text-xs block">Q{idx+1}: "{q}"</span>
                <p class="text-xs text-slate-400 mt-1">
                  <strong>Your Defense:</strong> <em>"{a}"</em>
                </p>
              </div>
            \"\"\""""

if old_loop_chunk in code:
    code = code.replace(old_loop_chunk, new_loop_chunk)
    print("Replaced loop chunk successfully!")
else:
    print("Could not find old loop chunk!")

# 2. Update Executive TL;DR tab rendering
old_tldr_chunk = """          <!-- TAB 2: EXECUTIVE TL;DR CHEATSHEET -->
          <div id="{ch_id}-content-tldr" class="tab-content hidden space-y-4 text-xs text-slate-300 leading-relaxed">
            <div class="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3">
              <div class="text-xs font-bold text-cyan-400 uppercase tracking-wider">Core Architectural Principle:</div>
              <p class="text-sm text-white font-medium leading-relaxed italic bg-slate-900/70 p-3 rounded-lg border border-slate-800">
                "{tldr.get("principle", "")}"
              </p>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div class="p-3.5 bg-rose-950/20 border border-rose-900/40 rounded-xl space-y-2">
                  <span class="text-xs font-bold text-rose-400 uppercase tracking-wider block">Top 3 L6 Red Flags (Instant Rejection)</span>
                  <ul class="space-y-1.5">
                    {red_flags_html}
                  </ul>
                </div>
                <div class="p-3.5 bg-amber-950/20 border border-amber-900/40 rounded-xl space-y-2">
                  <span class="text-xs font-bold text-amber-400 uppercase tracking-wider block">Production Gotcha to Highlight</span>
                  <p class="text-slate-300 leading-relaxed">
                    {tldr.get("gotchas", "")}
                  </p>
                </div>
              </div>
            </div>
          </div>"""

new_tldr_chunk = """          <!-- TAB 2: EXECUTIVE TL;DR CHEATSHEET -->
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
          </div>"""

if old_tldr_chunk in code:
    code = code.replace(old_tldr_chunk, new_tldr_chunk)
    print("Replaced TLDR chunk successfully!")
else:
    print("Could not find old TLDR chunk!")

with open("d:/Antigravity/build_cockpit.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Updated build_cockpit.py successfully!")
