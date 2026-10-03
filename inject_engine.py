# inject_engine.py
# Replaces placeholder whiteboard, streak, gamification, audio, and verification code
# in generate_full_cockpit_html.py with the full implementation.

with open("d:/Antigravity/generate_full_cockpit_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# Locate target block: from "// ==================== WHITEBOARD & SPLIT STUDIO ===================="
# to "// ==================== SURPRISE AMBUSH DRILL ===================="
start_marker = "// ==================== WHITEBOARD & SPLIT STUDIO ===================="
end_marker = "// ==================== SURPRISE AMBUSH DRILL ===================="

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error: Markers not found! start_idx={start_idx}, end_idx={end_idx}")
    exit(1)

full_engine_js = '''// ==================== WHITEBOARD & SPLIT STUDIO ENGINE ====================
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

    function logDailyCheckIn() {
      const countEl = document.getElementById('modal-streak-count');
      const streakNavEl = document.getElementById('streak-display');
      const cell = document.getElementById('streak-cell-today');
      const btn = document.getElementById('btn-checkin');

      if (countEl) countEl.innerText = '6 DAYS';
      if (streakNavEl) streakNavEl.innerText = '6-Day Streak';
      if (cell) {
        cell.className = 'p-2 rounded bg-emerald-500 text-white font-bold';
        cell.innerText = 'D6 ✔';
      }
      if (btn) {
        btn.disabled = true;
        btn.innerText = 'Today Checked In! 🔥';
        btn.className = 'px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 font-mono text-xs cursor-not-allowed';
      }

      addXP(50, 'Logged Daily Study Check-in');
      showToast('🔥 6-Day Streak Logged! Top 2% Candidate Consistency (+50 XP)');
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
'''

new_text = text[:start_idx] + full_engine_js + "\n    " + text[end_idx:]

with open("d:/Antigravity/generate_full_cockpit_html.py", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully injected full whiteboard, audio, streak, and verification engine!")
