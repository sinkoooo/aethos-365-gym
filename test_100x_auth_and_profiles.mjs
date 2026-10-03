import assert from 'assert';

const BASE = 'http://localhost:3000';

async function runTests() {
  console.log('🧪 Starting 100x Auth, Profiles & Data Isolation Test Suite...\n');

  // Test 1: Health check
  const healthRes = await fetch(`${BASE}/api/health`);
  assert.strictEqual(healthRes.status, 200, 'Server should be online');
  const health = await healthRes.json();
  console.log('✅ 1. Server Health:', health.status);

  // Test 2: Unauthenticated state check (Strict Privacy & Zero Leakage)
  const guestStateRes = await fetch(`${BASE}/api/gym/state`);
  const guestState = await guestStateRes.json();
  assert.strictEqual(guestState.authenticated, false, 'Guest should not be authenticated');
  assert.strictEqual(guestState.data, null, 'Guest MUST NOT receive any user data (Zero Leakage)');
  console.log('✅ 2. Zero-Leak Guest Privacy: Verified (No user data exposed)');

  // Test 3: Guest /api/auth/me returns 401 unauthenticated
  const guestMeRes = await fetch(`${BASE}/api/auth/me`);
  assert.strictEqual(guestMeRes.status, 401, 'Guest /api/auth/me should return 401');
  console.log('✅ 3. Guest Auth Status: Verified 401 Unauthorized');

  // Test 4: Admin Login via Alias 'shivam'
  const adminLoginRes = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'shivam', password: 'admin' })
  });
  assert.strictEqual(adminLoginRes.status, 200, 'Admin login should succeed');
  const adminLogin = await adminLoginRes.json();
  assert.strictEqual(adminLogin.success, true, 'Admin login success should be true');
  assert.ok(adminLogin.token, 'Admin token should be present');
  assert.strictEqual(adminLogin.user.role, 'admin', 'Admin role should be admin');
  console.log('✅ 4. Admin Login with alias "shivam": Success, Token received');

  // Test 5: Verify Admin State Integrity (Day 5 workouts & notes preserved)
  const adminStateRes = await fetch(`${BASE}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${adminLogin.token}` }
  });
  const adminState = await adminStateRes.json();
  assert.strictEqual(adminState.authenticated, true, 'Admin should be authenticated');
  assert.ok(adminState.data, 'Admin state data must exist');
  assert.strictEqual(adminState.data.gym_active_day, '5', 'Admin Day 5 state must be preserved intact');
  console.log('✅ 5. Admin Day 5 Data Integrity: Preserved intact (gym_active_day = 5)');

  // Test 6: Trainee Registration with custom profile goals, avatar, and metrics
  const uniqueUname = `trainee_${Date.now()}`;
  const regRes = await fetch(`${BASE}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: uniqueUname,
      password: 'password123',
      displayName: 'Alex Spartan',
      avatar: '🦁',
      goal: 'hypertrophy',
      startingWeight: 80,
      targetWeight: 75,
      bio: 'Lifting heavy every single day.'
    })
  });
  assert.strictEqual(regRes.status, 200, 'Registration should succeed');
  const regData = await regRes.json();
  assert.strictEqual(regData.success, true, 'Registration success should be true');
  assert.ok(regData.token, 'Trainee token should be generated');
  assert.strictEqual(regData.user.displayName, 'Alex Spartan');
  assert.strictEqual(regData.user.avatar, '🦁');
  console.log(`✅ 6. Trainee Registration (@${uniqueUname}): Success with custom avatar & bio`);

  // Test 7: Trainee Saves Custom State (Strict Isolation Check)
  const traineeToken = regData.token;
  const customTraineePayload = {
    gym_active_day: '12',
    gym_365_completed: JSON.stringify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
    gym_user_profile: JSON.stringify({ name: 'Alex Spartan', weight: 80, goal: 'hypertrophy' })
  };
  const saveRes = await fetch(`${BASE}/api/gym/state`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${traineeToken}`
    },
    body: JSON.stringify(customTraineePayload)
  });
  assert.strictEqual(saveRes.status, 200, 'Trainee state save should succeed');
  console.log('✅ 7. Trainee State Persistence: Successfully saved Day 12 state');

  // Test 8: Verify Trainee Isolated State Fetch
  const traineeStateRes = await fetch(`${BASE}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${traineeToken}` }
  });
  const traineeState = await traineeStateRes.json();
  assert.strictEqual(traineeState.data.gym_active_day, '12', 'Trainee should have Day 12');
  console.log('✅ 8. Trainee State Fetch: Verified Day 12 retrieved accurately');

  // Test 9: Verify Admin State is COMPLETELY UNTOUCHED by Trainee Action
  const verifyAdminRes = await fetch(`${BASE}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${adminLogin.token}` }
  });
  const verifyAdmin = await verifyAdminRes.json();
  assert.strictEqual(verifyAdmin.data.gym_active_day, '5', 'Admin Day 5 must remain completely unmodified');
  console.log('✅ 9. Multi-Tenant Strict Isolation: Verified (Admin Day 5 unmodified by Trainee Day 12)');

  // Test 10: Dynamic Profile Setting Update (PUT /api/auth/profile)
  const updateProfileRes = await fetch(`${BASE}/api/auth/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${traineeToken}`
    },
    body: JSON.stringify({
      displayName: 'Alexander The Great',
      goal: 'strength',
      targetWeight: 72,
      avatar: '👑',
      bio: 'Conquering the world, one rep at a time.'
    })
  });
  assert.strictEqual(updateProfileRes.status, 200, 'Profile update should succeed');
  const updateData = await updateProfileRes.json();
  assert.strictEqual(updateData.success, true);
  assert.strictEqual(updateData.user.displayName, 'Alexander The Great');
  assert.strictEqual(updateData.user.avatar, '👑');
  assert.strictEqual(updateData.user.goal, 'strength');
  console.log('✅ 10. Dynamic Profile Setting Update (PUT /api/auth/profile): Success');

  // Test 11: Public Profiles List for Quick Account Switcher
  const profilesRes = await fetch(`${BASE}/api/auth/profiles`);
  const profilesData = await profilesRes.json();
  assert.strictEqual(profilesData.success, true);
  assert.ok(Array.isArray(profilesData.profiles), 'Profiles should be an array');
  const alexProfile = profilesData.profiles.find(p => p.username === uniqueUname);
  assert.ok(alexProfile, 'New trainee should appear in public profiles list');
  assert.strictEqual(alexProfile.displayName, 'Alexander The Great');
  assert.strictEqual(alexProfile.avatar, '👑');
  console.log('✅ 11. Quick Account Switcher Roster: Accurately reflects updated profile');

  // Test 12: Admin Roster Oversight
  const adminRosterRes = await fetch(`${BASE}/api/admin/users`, {
    headers: { 'Authorization': `Bearer ${adminLogin.token}` }
  });
  assert.strictEqual(adminRosterRes.status, 200);
  const rosterData = await adminRosterRes.json();
  assert.ok(rosterData.success);
  assert.ok(rosterData.roster.some(u => u.username === uniqueUname), 'Trainee should appear in admin cockpit');
  console.log('✅ 12. Head Coach Admin Cockpit: Accurately monitors all trainee athletes');

  console.log('\n🎉 ALL 12 PROFESSIONAL TESTS PASSED WITH 100% SUCCESS!');
}

runTests().catch(err => {
  console.error('❌ Test Failure:', err);
  process.exit(1);
});
