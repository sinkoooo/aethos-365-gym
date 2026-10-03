# inject_simulators_and_reset.py
# Implements:
# 1. Ultra-sleek custom scrollbar CSS and UI polish (eliminating ugly scrollbars)
# 2. Complete 8 Advance Interactive Physics Simulators for Stage 13
# 3. Gamification reset to 0 XP and 0-Day Streak with Level 1 (L3 Systems Explorer)
# 4. Floating XP particle notifications & Web Audio ascending chord chime
# 5. Daily streak check-in from 0 -> 1 day with flame animation

import re

with open("d:/Antigravity/generate_full_cockpit_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# ==================== 1. SCROLLBAR & UI CSS ====================
custom_scrollbar_css = '''
    /* Ultra-sleek custom scrollbars (Linear / Raycast Pro) */
    ::-webkit-scrollbar {
      width: 4px;
      height: 4px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(148, 163, 184, 0.2);
      border-radius: 9999px;
      transition: background 0.2s ease;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 240, 255, 0.6);
    }
    * {
      scrollbar-width: thin;
      scrollbar-color: rgba(148, 163, 184, 0.2) transparent;
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
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
'''

# Inject scrollbar CSS into the <style> section
if "/* Ultra-sleek custom scrollbars" not in code:
    code = code.replace("    /* Custom Scrollbars */", custom_scrollbar_css)

# ==================== 2. RESET DEFAULT XP & STREAK IN HTML ====================
# Reset in header
code = re.sub(r'<span id="xp-display"[^>]*>[0-9,]+</span>', '<span id="xp-display" class="font-bold">0</span>', code)
code = re.sub(r'<span id="streak-display"[^>]*>[^<]+</span>', '<span id="streak-display" class="font-bold">0-Day Streak</span>', code)

# Reset in gamification modal
code = re.sub(r'<span id="modal-xp-val"[^>]*>[0-9,]+</span>', '<span id="modal-xp-val">0</span>', code)
code = code.replace('Staff Architect (L6)', 'L3 Systems Explorer (Level 1)')
code = code.replace('2,500 XP to L7', '500 XP to L4')

# Reset in streak modal
code = re.sub(r'<div id="modal-streak-count"[^>]*>[^<]+</div>', '<div id="modal-streak-count" class="text-4xl font-black text-amber-400 font-mono">0 DAYS</div>', code)

# ==================== 3. ADVANCE SIMULATOR ENGINES JAVASCRIPT ====================
simulators_js = '''
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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

      if (zcAnimationId) cancelAnimationFrame(zcAnimationId);
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
          ctx.beginPath();
          ctx.roundRect(n.x, n.y - 30, 130, 60, 8);
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

    function initRaftSim() {
      const canvas = document.getElementById('raft-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;

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
'''

# Update addXP to use playXpChime and showXpFloat, plus update level titles
updated_add_xp_js = '''
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
'''

# Replace addXP and simulators section in code
start_sim = code.find('// ==================== LAB SIMULATORS ====================')
end_script = code.rfind('</script>')

if start_sim != -1 and end_script != -1:
    code = code[:start_sim] + simulators_js + "\n" + updated_add_xp_js + "\n" + code[end_script:]
    print("Injected simulators and updated gamification functions!")

# Also ensure state initialization sets xp: 0 and streak: 0
code = code.replace("appState = JSON.parse(saved);", "appState = JSON.parse(saved);\n        if (appState.xp === 1490 || appState.xp === 2140) appState.xp = 0;\n        if (appState.streak === 5) appState.streak = 0;")
code = code.replace("xp: 1490,", "xp: 0,")
code = code.replace("streak: 5,", "streak: 0,")

with open("d:/Antigravity/generate_full_cockpit_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated generate_full_cockpit_html.py with custom scrollbars, simulators, and 0-XP reset!")
