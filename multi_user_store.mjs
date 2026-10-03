import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DATA_DIR = path.join(__dirname, 'data');
const USERS_FILE = path.join(DATA_DIR, 'users.json');
const SESSIONS_FILE = path.join(DATA_DIR, 'sessions.json');
const STATES_DIR = path.join(DATA_DIR, 'user_states');
const LEGACY_GYM_STATE_FILE = path.join(__dirname, 'gym_state.json');

// Ensure directories exist
if (!fsSync.existsSync(DATA_DIR)) fsSync.mkdirSync(DATA_DIR, { recursive: true });
if (!fsSync.existsSync(STATES_DIR)) fsSync.mkdirSync(STATES_DIR, { recursive: true });

// Password hashing using PBKDF2 (Native Node.js Crypto)
function hashPassword(password, salt = null) {
  const generatedSalt = salt || crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, generatedSalt, 10000, 64, 'sha512').toString('hex');
  return { salt: generatedSalt, hash };
}

function verifyPassword(password, salt, originalHash) {
  const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
  return crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(originalHash, 'hex'));
}

// In-Memory cache with atomic file persistence
let usersCache = null;
let sessionsCache = null;

async function loadUsers() {
  if (usersCache) return usersCache;
  try {
    const raw = await fs.readFile(USERS_FILE, 'utf-8');
    usersCache = JSON.parse(raw);
  } catch {
    usersCache = [];
    await saveUsers();
  }
  return usersCache;
}

async function saveUsers() {
  await fs.writeFile(USERS_FILE, JSON.stringify(usersCache || [], null, 2), 'utf-8');
}

async function loadSessions() {
  if (sessionsCache) return sessionsCache;
  try {
    const raw = await fs.readFile(SESSIONS_FILE, 'utf-8');
    sessionsCache = JSON.parse(raw);
  } catch {
    sessionsCache = {};
    await saveSessions();
  }
  return sessionsCache;
}

async function saveSessions() {
  await fs.writeFile(SESSIONS_FILE, JSON.stringify(sessionsCache || {}, null, 2), 'utf-8');
}

// Sanitize user for public/client delivery (strips password & salt)
function sanitizeUser(user) {
  if (!user) return null;
  const { salt, passwordHash, ...clean } = user;
  return clean;
}

// Initialize Default Admin and seed with existing Day 5 data
export async function initMultiUserStore() {
  const users = await loadUsers();
  await loadSessions();

  if (users.length === 0) {
    console.log('[Auth] Initializing default Admin account with existing data...');
    const { salt, hash } = hashPassword('admin123');
    const adminUser = {
      id: 'usr_admin_master',
      username: 'admin',
      displayName: 'Head Coach (Admin)',
      salt,
      passwordHash: hash,
      role: 'admin',
      avatar: '👑',
      createdAt: new Date().toISOString(),
      lastActiveAt: new Date().toISOString()
    };
    users.push(adminUser);
    await saveUsers();

    // Seed state from legacy gym_state.json if present
    let initialAdminState = {};
    if (fsSync.existsSync(LEGACY_GYM_STATE_FILE)) {
      try {
        const raw = fsSync.readFileSync(LEGACY_GYM_STATE_FILE, 'utf-8');
        initialAdminState = JSON.parse(raw);
        console.log('[Auth] Seeded Admin state from existing gym_state.json (Day 5 intact)');
      } catch (err) {
        console.warn('[Auth] Could not parse gym_state.json, creating clean state:', err.message);
      }
    }
    const adminStatePath = path.join(STATES_DIR, `${adminUser.id}.json`);
    await fs.writeFile(adminStatePath, JSON.stringify(initialAdminState, null, 2), 'utf-8');
  }
}

// Register a new user
export async function registerUser({ username, password, displayName, avatar = '⚡', goal = 'recomp', targetWeight = 74, bio = '' }) {
  if (!username || typeof username !== 'string' || username.trim().length < 3) {
    throw new Error('Username must be at least 3 characters');
  }
  if (!password || typeof password !== 'string' || password.length < 4) {
    throw new Error('Password must be at least 4 characters');
  }

  const cleanUsername = username.trim().toLowerCase();
  const users = await loadUsers();

  const existing = users.find(u => u.username === cleanUsername);
  if (existing) {
    throw new Error('Username is already taken');
  }

  const isFirstUser = users.length === 0;
  const role = isFirstUser ? 'admin' : 'user';
  const { salt, hash } = hashPassword(password);

  const newUser = {
    id: `usr_${crypto.randomBytes(8).toString('hex')}`,
    username: cleanUsername,
    displayName: (displayName && displayName.trim()) || cleanUsername,
    salt,
    passwordHash: hash,
    role,
    avatar: avatar || '⚡',
    goal: goal || 'recomp',
    targetWeight: parseFloat(targetWeight) || 74,
    startingWeight: parseFloat(targetWeight) || 74,
    bio: bio ? bio.trim().slice(0, 200) : 'Relentless athletic transformation & progression.',
    createdAt: new Date().toISOString(),
    lastActiveAt: new Date().toISOString()
  };

  users.push(newUser);
  await saveUsers();

  // Create isolated state file
  const userStatePath = path.join(STATES_DIR, `${newUser.id}.json`);
  const initialState = {
    gym_active_day: 1,
    gym_streak: 1,
    gym_365_completed: {},
    gym_set_logs: {},
    gym_metrics_logs: {},
    gym_unlocked_milestones: ['first_step'],
    _createdFor: newUser.id,
    _serverTimestamp: new Date().toISOString()
  };
  await fs.writeFile(userStatePath, JSON.stringify(initialState, null, 2), 'utf-8');

  // Create login session
  const token = await createSession(newUser.id);
  return { token, user: sanitizeUser(newUser) };
}

// Login user
export async function loginUser(username, password) {
  if (!username || !password) {
    throw new Error('Username and password are required');
  }
  const cleanUsername = username.trim().toLowerCase();
  const users = await loadUsers();
  let user = users.find(u => u.username === cleanUsername);

  // Smart Admin Alias: allow 'admin' or 'shivam' for the head coach account
  if (!user && (cleanUsername === 'shivam' || cleanUsername === 'admin')) {
    user = users.find(u => u.role === 'admin' || u.id === 'usr_admin_master');
  }

  if (!user) {
    throw new Error('Invalid username or password');
  }

  let isValid = verifyPassword(password, user.salt, user.passwordHash);
  // Also allow 'admin', 'admin123', or 'shivam' for the head coach account
  if (!isValid && (user.role === 'admin' || user.id === 'usr_admin_master')) {
    if (password === 'admin123' || password === 'admin' || password === 'shivam') {
      isValid = true;
    }
  }

  if (!isValid) {
    throw new Error('Invalid username or password');
  }

  user.lastActiveAt = new Date().toISOString();
  await saveUsers();

  const token = await createSession(user.id);
  return { token, user: sanitizeUser(user) };
}

// Session Management
async function createSession(userId) {
  const sessions = await loadSessions();
  const token = `aethos_${crypto.randomBytes(24).toString('hex')}`;
  sessions[token] = {
    userId,
    createdAt: new Date().toISOString(),
    expiresAt: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString() // 180 days
  };
  await saveSessions();
  return token;
}

export async function getUserByToken(token) {
  if (!token) return null;
  const sessions = await loadSessions();
  const session = sessions[token];
  if (!session) return null;

  if (new Date(session.expiresAt) < new Date()) {
    delete sessions[token];
    await saveSessions();
    return null;
  }

  const users = await loadUsers();
  const user = users.find(u => u.id === session.userId);
  if (!user) return null;

  user.lastActiveAt = new Date().toISOString();
  return sanitizeUser(user);
}

export async function destroySession(token) {
  const sessions = await loadSessions();
  if (token && sessions[token]) {
    delete sessions[token];
    await saveSessions();
  }
  return true;
}

// Update Profile Attributes
export async function updateUserProfile(userId, updates = {}) {
  const users = await loadUsers();
  const user = users.find(u => u.id === userId);
  if (!user) throw new Error('User not found');

  if (updates.displayName && typeof updates.displayName === 'string') {
    user.displayName = updates.displayName.trim();
  }
  if (updates.avatar && typeof updates.avatar === 'string') {
    user.avatar = updates.avatar.trim();
  }
  if (updates.goal && typeof updates.goal === 'string') {
    user.goal = updates.goal.trim();
  }
  if (updates.targetWeight !== undefined) {
    user.targetWeight = parseFloat(updates.targetWeight) || user.targetWeight;
  }
  if (updates.bio && typeof updates.bio === 'string') {
    user.bio = updates.bio.trim().slice(0, 200);
  }

  user.lastActiveAt = new Date().toISOString();
  await saveUsers();
  return sanitizeUser(user);
}

// Get Public Profiles for Quick Account Switcher
export async function getPublicProfilesList() {
  const users = await loadUsers();
  return users.map(u => ({
    id: u.id,
    username: u.username,
    displayName: u.displayName,
    avatar: u.avatar || '⚡',
    role: u.role,
    goal: u.goal || 'recomp'
  }));
}

// User-Isolated Gym State Management
export async function getUserGymState(userId) {
  const filePath = path.join(STATES_DIR, `${userId}.json`);
  try {
    const raw = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(raw);
  } catch {
    // If not found, create empty state
    const cleanState = { gym_active_day: 1, _serverTimestamp: new Date().toISOString() };
    await fs.writeFile(filePath, JSON.stringify(cleanState, null, 2), 'utf-8');
    return cleanState;
  }
}

export async function saveUserGymState(userId, payload) {
  const filePath = path.join(STATES_DIR, `${userId}.json`);
  let state = payload;
  if (state && typeof state === 'object' && state.data && typeof state.data === 'object') {
    state = state.data;
  }
  const stateWithMeta = {
    ...state,
    _serverTimestamp: new Date().toISOString()
  };
  await fs.writeFile(filePath, JSON.stringify(stateWithMeta, null, 2), 'utf-8');
  return stateWithMeta;
}

function safeParseJson(val, fallback = null) {
  if (val === null || val === undefined) return fallback;
  if (typeof val === 'object') return val;
  if (typeof val === 'string') {
    try {
      return JSON.parse(val);
    } catch {
      return fallback;
    }
  }
  return fallback;
}

// Calculate Trainee Stats for Leaderboard & Admin Inspection
function calculateTraineeStats(user, rawState = {}) {
  const state = rawState || {};
  let completedDays = 0;
  const completedParsed = safeParseJson(state.gym_365_completed, state.gym_365_completed);
  if (Array.isArray(completedParsed)) {
    completedDays = completedParsed.length;
  } else if (completedParsed && typeof completedParsed === 'object') {
    completedDays = Object.keys(completedParsed).length;
  }

  let totalSets = 0;
  const setLogsParsed = safeParseJson(state.gym_set_logs, state.gym_set_logs);
  if (setLogsParsed && typeof setLogsParsed === 'object') {
    Object.values(setLogsParsed).forEach(item => {
      if (Array.isArray(item)) {
        totalSets += item.length;
      } else if (item && typeof item === 'object') {
        if ('done' in item || 'reps' in item || 'wt' in item) {
          totalSets += 1;
        } else {
          Object.values(item).forEach(inner => {
            if (Array.isArray(inner)) totalSets += inner.length;
            else if (inner && typeof inner === 'object') totalSets += 1;
          });
        }
      }
    });
  }

  // Calculate XP & Level
  // Each completed day = 150 XP, each logged set = 15 XP
  const activeDayNum = parseInt(state.gym_active_day, 10) || 1;
  const xp = (completedDays * 150) + (totalSets * 15) + (activeDayNum * 20);
  
  let level = 1;
  let levelTitle = 'Initiate';
  if (xp >= 10000) { level = 10; levelTitle = 'Aethos Titan'; }
  else if (xp >= 7500) { level = 9; levelTitle = 'Olympian'; }
  else if (xp >= 5500) { level = 8; levelTitle = 'Centurion'; }
  else if (xp >= 4000) { level = 7; levelTitle = 'Gladiator'; }
  else if (xp >= 2800) { level = 6; levelTitle = 'Ironborn'; }
  else if (xp >= 1800) { level = 5; levelTitle = 'Spartan'; }
  else if (xp >= 1100) { level = 4; levelTitle = 'Warrior'; }
  else if (xp >= 600) { level = 3; levelTitle = 'Aspirant'; }
  else if (xp >= 250) { level = 2; levelTitle = 'Apprentice'; }

  let unlockedBadges = 0;
  const milestonesParsed = safeParseJson(state.gym_unlocked_milestones, state.gym_unlocked_milestones);
  if (Array.isArray(milestonesParsed)) {
    unlockedBadges = milestonesParsed.length;
  } else if (milestonesParsed && typeof milestonesParsed === 'object') {
    unlockedBadges = Object.keys(milestonesParsed).length;
  }

  let streak = completedDays > 0 ? completedDays : (parseInt(state.gym_streak, 10) || 1);

  return {
    userId: user.id,
    username: user.username,
    displayName: user.displayName,
    avatar: user.avatar || '⚡',
    role: user.role,
    goal: user.goal || 'recomp',
    bio: user.bio || '',
    level,
    levelTitle,
    xp,
    streak,
    totalWorkouts: completedDays,
    totalSets,
    unlockedBadges,
    currentDay: activeDayNum,
    lastActiveAt: user.lastActiveAt
  };
}

// Community Leaderboard (Strictly Public Metrics, zero privacy leaks)
export async function getCommunityLeaderboard() {
  const users = await loadUsers();
  const leaderboard = [];

  for (const user of users) {
    try {
      const state = await getUserGymState(user.id);
      const stats = calculateTraineeStats(user, state);
      leaderboard.push(stats);
    } catch {
      // ignore corrupted state
    }
  }

  // Sort descending by XP
  leaderboard.sort((a, b) => b.xp - a.xp);

  // Assign ranks
  return leaderboard.map((entry, index) => ({
    rank: index + 1,
    ...entry
  }));
}

// Admin Roster Inspection (Admin Eyes Only)
export async function getAdminRoster() {
  const users = await loadUsers();
  const roster = [];

  for (const user of users) {
    try {
      const state = await getUserGymState(user.id);
      const stats = calculateTraineeStats(user, state);
      roster.push({
        ...sanitizeUser(user),
        stats,
        hasPhotos: !!(state.gym_photo_1 || state.gym_photo_2 || state.gym_photo_3)
      });
    } catch {
      roster.push({ ...sanitizeUser(user), stats: null });
    }
  }

  return roster;
}

// Admin inspects a specific user's complete state
export async function adminGetUserState(targetUserId) {
  const users = await loadUsers();
  const user = users.find(u => u.id === targetUserId);
  if (!user) throw new Error('User not found');
  const state = await getUserGymState(targetUserId);
  const stats = calculateTraineeStats(user, state);
  return { user: sanitizeUser(user), state, stats };
}
