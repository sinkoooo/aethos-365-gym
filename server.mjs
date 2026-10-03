import express from 'express';
import cors from 'cors';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  initMultiUserStore,
  registerUser,
  loginUser,
  getUserByToken,
  destroySession,
  getUserGymState,
  saveUserGymState,
  getCommunityLeaderboard,
  getAdminRoster,
  adminGetUserState
} from './multi_user_store.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Aggressive Cache-Control headers to ensure zero stale browser/proxy caching
app.use((req, res, next) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  next();
});

// Authentication Extraction Middleware
async function authenticateUser(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    req.user = null;
    return next();
  }
  const token = authHeader.substring(7).trim();
  try {
    const user = await getUserByToken(token);
    req.user = user;
    req.token = token;
  } catch (err) {
    req.user = null;
  }
  next();
}
app.use(authenticateUser);

// Quick alias routes for home gym app
app.get(['/', '/gym', '/homegym', '/aethos', '/index.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'home_gym_zero_to_hero.html'));
});

// Serve static directory with strict no-cache options
app.use(express.static(__dirname, {
  etag: false,
  lastModified: false,
  setHeaders: (res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
  }
}));

// Persistent store files
const PROGRESS_FILE = path.join(__dirname, 'study_progress.json');
const NOTES_FILE = path.join(__dirname, 'study_notes.json');
const GYM_STATE_FILE = path.join(__dirname, 'gym_state.json');

// Murmur2 32-bit Hash Implementation (matching Apache Kafka's default partitioner)
function murmur2(data, seed = 0x9747b28c) {
  const m = 0x5bd1e995;
  const r = 24;
  let len = data.length;
  let h = seed ^ len;
  let i = 0;

  while (len >= 4) {
    let k =
      (data.charCodeAt(i) & 0xff) |
      ((data.charCodeAt(i + 1) & 0xff) << 8) |
      ((data.charCodeAt(i + 2) & 0xff) << 16) |
      ((data.charCodeAt(i + 3) & 0xff) << 24);

    k = Math.imul(k, m);
    k ^= k >>> r;
    k = Math.imul(k, m);

    h = Math.imul(h, m) ^ k;
    i += 4;
    len -= 4;
  }

  switch (len) {
    case 3:
      h ^= (data.charCodeAt(i + 2) & 0xff) << 16;
    case 2:
      h ^= (data.charCodeAt(i + 1) & 0xff) << 8;
    case 1:
      h ^= data.charCodeAt(i) & 0xff;
      h = Math.imul(h, m);
  }

  h ^= h >>> 13;
  h = Math.imul(h, m);
  h ^= h >>> 15;

  return (h >>> 0); // Convert to unsigned 32-bit integer
}

// Kafka partition assigner
function computeKafkaPartition(key, totalPartitions = 128) {
  const hash = murmur2(key);
  // Kafka formula: toPositive(hash) % numPartitions
  const positiveHash = hash & 0x7fffffff;
  return positiveHash % totalPartitions;
}

// ==================== REST APIS ====================

// 1. Health & Server Telemetry
app.get('/api/health', (req, res) => {
  const mem = process.memoryUsage();
  res.json({
    status: 'online',
    platform: 'Google L8 Technical Mastery Hub',
    runtime: {
      node: process.version,
      platform: process.platform,
      arch: process.arch,
      uptimeSeconds: Math.floor(process.uptime()),
      heapUsedMB: Math.round(mem.heapUsed / 1024 / 1024),
      heapTotalMB: Math.round(mem.heapTotal / 1024 / 1024)
    },
    timestamp: new Date().toISOString()
  });
});

// 2. Study Progress Persistence
app.get('/api/progress', async (req, res) => {
  try {
    const data = await fs.readFile(PROGRESS_FILE, 'utf-8');
    res.json(JSON.parse(data));
  } catch (err) {
    res.json({
      chapters: {},
      milestones: {},
      quizScore: 0,
      lastUpdated: new Date().toISOString()
    });
  }
});

app.post('/api/progress', async (req, res) => {
  try {
    const payload = {
      ...req.body,
      lastUpdated: new Date().toISOString()
    };
    await fs.writeFile(PROGRESS_FILE, JSON.stringify(payload, null, 2));
    res.json({ success: true, message: 'Progress saved successfully', payload });
  } catch (err) {
    res.status(500).json({ error: 'Failed to persist progress' });
  }
});

// 3. User Personal Study Notes Persistence
app.get('/api/notes', async (req, res) => {
  try {
    const data = await fs.readFile(NOTES_FILE, 'utf-8');
    res.json(JSON.parse(data));
  } catch (err) {
    res.json({ notes: {} });
  }
});

app.post('/api/notes', async (req, res) => {
  try {
    await fs.writeFile(NOTES_FILE, JSON.stringify(req.body, null, 2));
    res.json({ success: true, message: 'Notes saved successfully' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to persist study notes' });
  }
});

// 4. Kafka Partition Murmur2 Hasher Simulator
app.post('/api/simulate/kafka', (req, res) => {
  const { keys, totalPartitions = 128 } = req.body;
  if (!Array.isArray(keys)) {
    return res.status(400).json({ error: 'Expected array of keys' });
  }

  const results = keys.map((key) => {
    const hash = murmur2(key);
    const partition = computeKafkaPartition(key, totalPartitions);
    return {
      key,
      murmur2Hash: '0x' + hash.toString(16).toUpperCase(),
      assignedPartition: partition,
      guarantee: `All requests for '${key}' strictly routed to Partition #${partition}`
    };
  });

  res.json({
    totalPartitions,
    algorithm: 'Murmur2 (Apache Kafka Default Partitioner)',
    results
  });
});

// 5. Distributed Lock & Fencing Token Step-Through Simulator
app.post('/api/simulate/fencing', (req, res) => {
  const { gcPauseMs = 15000, lockTtlMs = 10000 } = req.body;

  const logs = [];
  logs.push({
    step: 1,
    timeMs: 0,
    actor: 'Worker A (Pod 1)',
    event: `Acquires Redis lock on 'cell:104' with TTL ${lockTtlMs}ms`,
    redisState: { lockOwner: 'Worker-A-UUID', fencingToken: 42, ttlRemainingMs: lockTtlMs },
    dbVersion: 41,
    status: 'ACTIVE'
  });

  logs.push({
    step: 2,
    timeMs: 2000,
    actor: 'Worker A (Pod 1)',
    event: `JVM Stop-The-World (STW) Garbage Collection freeze begins! (Duration: ${gcPauseMs}ms)`,
    redisState: { lockOwner: 'Worker-A-UUID', fencingToken: 42, ttlRemainingMs: lockTtlMs - 2000 },
    dbVersion: 41,
    status: 'FROZEN_IN_GC'
  });

  logs.push({
    step: 3,
    timeMs: 10000,
    actor: 'Redis Server',
    event: `TTL expired! Worker A failed to send heartbeat ping. Lock is evicted.`,
    redisState: { lockOwner: null, fencingToken: 42, ttlRemainingMs: 0 },
    dbVersion: 41,
    status: 'LOCK_EXPIRED'
  });

  logs.push({
    step: 4,
    timeMs: 10500,
    actor: 'Worker B (Pod 2)',
    event: `Acquires lock! Redis increments fencing token from 42 to 43.`,
    redisState: { lockOwner: 'Worker-B-UUID', fencingToken: 43, ttlRemainingMs: lockTtlMs },
    dbVersion: 41,
    status: 'ACTIVE'
  });

  logs.push({
    step: 5,
    timeMs: 12000,
    actor: 'Worker B (Pod 2)',
    event: `Worker B commits to DB with version 43: 'UPDATE mo SET data=?, version=43 WHERE id=? AND version < 43'`,
    redisState: { lockOwner: 'Worker-B-UUID', fencingToken: 43, ttlRemainingMs: 8500 },
    dbVersion: 43,
    status: 'COMMITTED_SUCCESS'
  });

  logs.push({
    step: 6,
    timeMs: gcPauseMs,
    actor: 'Worker A (Pod 1)',
    event: `Worker A wakes up from GC! Believes it still owns the lock. Attempts stale DB write with token 42: 'UPDATE mo SET data=?, version=42 WHERE id=? AND version < 42'`,
    redisState: { lockOwner: 'Worker-B-UUID', fencingToken: 43, ttlRemainingMs: 0 },
    dbVersion: 43,
    status: 'REJECTED_BY_DATABASE',
    result: 'Zero rows updated! Monotonic fencing token saved the system from split-brain data corruption.'
  });

  res.json({
    simulation: 'Martin Kleppmann GC Pause Hazard & Monotonic Fencing Token Defense',
    parameters: { gcPauseMs, lockTtlMs },
    timeline: logs
  });
});

// ==================== MULTI-USER AUTHENTICATION APIS ====================
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, password, displayName, avatar } = req.body || {};
    const result = await registerUser({ username, password, displayName, avatar });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(400).json({ success: false, error: err.message });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body || {};
    const result = await loginUser(username, password);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(401).json({ success: false, error: err.message });
  }
});

app.get('/api/auth/me', (req, res) => {
  if (!req.user) {
    return res.status(401).json({ authenticated: false, user: null });
  }
  res.json({ authenticated: true, user: req.user });
});

app.post('/api/auth/logout', async (req, res) => {
  if (req.token) {
    await destroySession(req.token);
  }
  res.json({ success: true });
});

// ==================== USER-ISOLATED GYM STATE APIS ====================
app.get('/api/gym/state', async (req, res) => {
  try {
    // If authenticated, strictly load that user's private state
    if (req.user) {
      const data = await getUserGymState(req.user.id);
      return res.json({ exists: true, data, user: req.user });
    }
    // Fallback for unauthenticated local browser: load admin state for seamless continuity
    const data = await getUserGymState('usr_admin_master');
    res.json({ exists: true, data, user: null, note: 'Guest / Default Fallback' });
  } catch (err) {
    res.json({ exists: false, data: null });
  }
});

app.post('/api/gym/state', async (req, res) => {
  try {
    let payload = req.body;
    if (!payload || typeof payload !== 'object') {
      return res.status(400).json({ error: 'Invalid state payload' });
    }
    if (payload.data && typeof payload.data === 'object') {
      payload = payload.data;
    }

    const targetUserId = req.user ? req.user.id : 'usr_admin_master';
    const saved = await saveUserGymState(targetUserId, payload);

    // Mirror to legacy gym_state.json if admin/default for backward safety
    if (!req.user || req.user.role === 'admin') {
      try {
        await fs.writeFile(GYM_STATE_FILE, JSON.stringify(saved, null, 2), 'utf-8');
      } catch {}
    }

    res.json({ success: true, timestamp: saved._serverTimestamp, userId: targetUserId });
  } catch (err) {
    console.error('Failed to save gym state:', err);
    res.status(500).json({ error: 'Failed to persist gym state' });
  }
});

// ==================== 🏆 COMMUNITY LEADERBOARD (PUBLIC AGGREGATES) ====================
app.get('/api/gym/leaderboard', async (req, res) => {
  try {
    const leaderboard = await getCommunityLeaderboard();
    res.json({ success: true, leaderboard });
  } catch (err) {
    console.error('Failed to fetch leaderboard:', err);
    res.status(500).json({ success: false, error: 'Failed to load leaderboard' });
  }
});

// ==================== 🛡️ ADMIN OVERSIGHT & ROSTER (ADMIN EYES ONLY) ====================
app.get('/api/admin/users', async (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden: Admin access required' });
  }
  try {
    const roster = await getAdminRoster();
    res.json({ success: true, roster });
  } catch (err) {
    console.error('Admin roster fetch failed:', err);
    res.status(500).json({ error: 'Failed to fetch member roster' });
  }
});

app.get('/api/admin/user/:userId/state', async (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden: Admin access required' });
  }
  try {
    const userDetail = await adminGetUserState(req.params.userId);
    res.json({ success: true, ...userDetail });
  } catch (err) {
    res.status(404).json({ error: err.message });
  }
});

// Launch server with multi-tenant store initialization
async function startServer() {
  await initMultiUserStore();
  app.listen(PORT, () => {
    console.log(`\n============================================================`);
    console.log(`  🚀 Google L8 / Staff Engineer Technical Mastery Platform`);
    console.log(`  🔗 Running at: http://localhost:${PORT}`);
    console.log(`  📦 Node.js Engine: ${process.version} (Native ESM)`);
    console.log(`  ⚡ APIs active: /api/health, /api/auth/*, /api/gym/*, /api/admin/*`);
    console.log(`============================================================\n`);
  });
}

startServer().catch(err => {
  console.error('Fatal server boot failure:', err);
  process.exit(1);
});
