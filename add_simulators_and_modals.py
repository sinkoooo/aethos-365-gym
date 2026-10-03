# add_simulators_and_modals.py
# Injects Video Modal, switchCodeTab, and Real Canvas Simulators into build_cockpit.py

with open("d:/Antigravity/build_cockpit.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add Video Modal before </body>
modal_html = """
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
"""

if 'id="video-modal"' not in code:
    code = code.replace("</body>", modal_html + "\n</body>")
    print("Injected video modal HTML!")

# 2. Add JavaScript functions for Video Modal, Code Tabs, and Canvas Simulators
sim_js = """
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
"""

# Replace the one-line forwarders with the rich simulator functions
old_stubs = """    // Simulators logic forwarder
    function setZeroCopyMode(m) { showToast(`Zero-Copy mode: ${m}`); }
    function rehashKeys(k) { showToast(`Re-hashed to ${k} partitions`); }
    function requestToken(t) { showToast(`Token requested: ${t}`); }
    function runFencingDemo() { showToast('Fencing simulation active.'); }
    function runCteBenchmark(t) { showToast(`Benchmark: ${t}`); }
    function setLlmFormat(f) { showToast(`LLM format set to ${f}`); }
    function addConsumerPod() { showToast('Consumer scaled up.'); }
    function killConsumerPod() { showToast('Simulated consumer crash.'); }
    function checkAnswer(q, c, isOk) {
      const fb = document.getElementById(`q${q}-feedback`);
      if (fb) {
        fb.className = isOk ? 'mt-2 p-2.5 rounded text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono' : 'mt-2 p-2.5 rounded text-xs bg-rose-950 text-rose-300 border border-rose-800 font-mono';
        fb.innerHTML = isOk ? '✔ Correct Google Staff choice!' : '✖ Sub-optimal anti-pattern.';
        fb.classList.remove('hidden');
      }
      if (isOk) addXP(100, `Solved Scenario ${q}`);
    }"""

if old_stubs in code:
    code = code.replace(old_stubs, sim_js)
    print("Replaced simulator stubs with advanced canvas engines!")
else:
    print("Could not find old simulator stubs directly, appending before DOMContentLoaded...")
    idx = code.find("// ==================== INIT ENGINE ====================")
    if idx != -1:
        code = code[:idx] + sim_js + "\n" + code[idx:]
        print("Inserted simulator engine before INIT ENGINE!")

# Ensure initCanvas is called on DOMContentLoaded or stage switch
dom_load_hook = """      updateXpDisplay();
      goToStage(activeStage);
      updateProgress();
      setTimeout(() => {
        initZeroCopyCanvas();
        drawRaft();
        drawHashRing();
        drawTokenBucket();
      }, 300);"""

if "updateProgress();" in code and "initZeroCopyCanvas" not in code:
    code = code.replace("updateProgress();", dom_load_hook, 1)
    print("Hooked simulator canvas initialization on load!")

with open("d:/Antigravity/build_cockpit.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Updated build_cockpit.py with simulators & modals successfully!")
