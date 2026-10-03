// test_full_isolation_and_profiles.mjs
// Comprehensive test verifying multi-user profile persistence, custom stats, and zero leakage

const BASE_URL = 'http://localhost:3000';

async function run() {
  console.log('🧪 Starting Full Multi-User Profile & Data Isolation Verification...\n');

  // Test Case 1: Unauthenticated visitor has ZERO access to workout data
  const guestRes = await fetch(`${BASE_URL}/api/gym/state`);
  const guestJson = await guestRes.json();
  if (guestJson.authenticated !== false || guestJson.data !== null) {
    throw new Error('❌ Test Case 1 Failed: Guest received data!');
  }
  console.log('✅ 1. Guest Strict Zero-Leak Isolation Passed');

  // Test Case 2: Shivam / Admin login & state verification
  const shivamLoginRes = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'shivam', password: 'admin' })
  });
  const shivamLogin = await shivamLoginRes.json();
  if (!shivamLogin.success || shivamLogin.user.id !== 'usr_admin_master') {
    throw new Error('❌ Test Case 2 Failed: Shivam login alias failed');
  }
  const shivamToken = shivamLogin.token;

  const shivamStateRes = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${shivamToken}` }
  });
  const shivamState = await shivamStateRes.json();
  if (parseInt(shivamState.data.gym_active_day, 10) !== 5) {
    throw new Error(`❌ Test Case 2 Failed: Shivam day is ${shivamState.data.gym_active_day}, expected 5`);
  }
  console.log('✅ 2. Shivam Admin Login & Day 5 Data Integrity Passed');

  // Test Case 3: Create User Profile A (Trainee "Thor")
  const thorUsername = `thor_${Date.now()}`;
  const thorRegRes = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: thorUsername,
      password: 'password_thor',
      displayName: 'Thor Odinson',
      avatar: '🦅',
      goal: 'strength',
      startingWeight: 95.0,
      targetWeight: 100.0,
      bio: 'God of Thunder, Master of Iron.'
    })
  });
  const thorReg = await thorRegRes.json();
  if (!thorReg.success || thorReg.user.goal !== 'strength') {
    throw new Error('❌ Test Case 3 Failed: Thor registration failed');
  }
  const thorToken = thorReg.token;
  console.log('✅ 3. Trainee Thor Created with Custom Goal (strength) & Bio Passed');

  // Test Case 4: Verify Thor's initial state is pristine (Day 1, 0 completed workouts)
  const thorStateRes1 = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${thorToken}` }
  });
  const thorState1 = await thorStateRes1.json();
  if (parseInt(thorState1.data.gym_active_day, 10) !== 1 || Object.keys(thorState1.data.gym_365_completed || {}).length !== 0) {
    throw new Error('❌ Test Case 4 Failed: Thor received corrupted or leaked state');
  }
  console.log('✅ 4. Thor Initial State is Clean Day 1 Passed');

  // Test Case 5: Thor logs workout progress on Day 1
  const thorSaveRes = await fetch(`${BASE_URL}/api/gym/state`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${thorToken}`
    },
    body: JSON.stringify({
      gym_active_day: 2,
      gym_streak: 2,
      gym_365_completed: { 1: { timestamp: new Date().toISOString(), totalVolume: 12500 } },
      gym_set_logs: { 'd1_ex1': { sets: [1, 2, 3], done: true } },
      gym_metrics_logs: [{ date: '2026-10-03', wt: 95.0 }]
    })
  });
  const thorSave = await thorSaveRes.json();
  if (!thorSave.success) {
    throw new Error('❌ Test Case 5 Failed: Thor workout state save failed');
  }
  console.log('✅ 5. Thor Workout Progress Saved Passed');

  // Test Case 6: Create User Profile B (Trainee "Athena")
  const athenaUsername = `athena_${Date.now()}`;
  const athenaRegRes = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: athenaUsername,
      password: 'password_athena',
      displayName: 'Goddess Athena',
      avatar: '🛡️',
      goal: 'shred',
      startingWeight: 62.0,
      targetWeight: 58.0,
      bio: 'Goddess of Tactical Strength.'
    })
  });
  const athenaReg = await athenaRegRes.json();
  if (!athenaReg.success || athenaReg.user.goal !== 'shred') {
    throw new Error('❌ Test Case 6 Failed: Athena registration failed');
  }
  const athenaToken = athenaReg.token;
  console.log('✅ 6. Trainee Athena Created with Custom Goal (shred) Passed');

  // Test Case 7: Verify Athena sees ZERO data from Thor and ZERO data from Shivam
  const athenaStateRes = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${athenaToken}` }
  });
  const athenaState = await athenaStateRes.json();
  if (parseInt(athenaState.data.gym_active_day, 10) !== 1 || Object.keys(athenaState.data.gym_365_completed || {}).length !== 0) {
    throw new Error('❌ Test Case 7 Failed: Cross-contamination between Thor and Athena!');
  }
  console.log('✅ 7. Cross-User Data Isolation (Thor vs Athena vs Shivam) Strictly Verified');

  // Test Case 8: Athena logs her own workout
  await fetch(`${BASE_URL}/api/gym/state`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${athenaToken}`
    },
    body: JSON.stringify({
      gym_active_day: 3,
      gym_streak: 3,
      gym_365_completed: { 1: { timestamp: new Date().toISOString() }, 2: { timestamp: new Date().toISOString() } },
      gym_set_logs: { 'd2_ex1': { sets: [1, 2], done: true } }
    })
  });

  // Test Case 9: Verify Thor still has his exact Day 2 state
  const thorCheck = await (await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${thorToken}` }
  })).json();
  if (parseInt(thorCheck.data.gym_active_day, 10) !== 2 || !thorCheck.data.gym_set_logs['d1_ex1']) {
    throw new Error('❌ Test Case 9 Failed: Thor state was overwritten by Athena');
  }
  console.log('✅ 8. Thor State Isolated & Intact After Athena Workout Passed');

  // Test Case 10: Verify Shivam still has his exact Day 5 state
  const shivamCheck = await (await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${shivamToken}` }
  })).json();
  if (parseInt(shivamCheck.data.gym_active_day, 10) !== 5) {
    throw new Error('❌ Test Case 10 Failed: Shivam Day 5 was modified');
  }
  console.log('✅ 9. Shivam Day 5 Master Account Intact Passed');

  // Test Case 11: Update Profile Settings for Thor via PUT /api/auth/profile
  const thorUpdateRes = await fetch(`${BASE_URL}/api/auth/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${thorToken}`
    },
    body: JSON.stringify({
      displayName: 'Thor Allfather',
      goal: 'hypertrophy',
      targetWeight: 105.0,
      bio: 'Ascended to the throne of Asgard.'
    })
  });
  const thorUpdate = await thorUpdateRes.json();
  if (!thorUpdate.success || thorUpdate.user.displayName !== 'Thor Allfather' || thorUpdate.user.goal !== 'hypertrophy') {
    throw new Error('❌ Test Case 11 Failed: Profile update failed');
  }
  console.log('✅ 10. Thor Profile Settings Update (Name, Goal, Target Wt, Bio) Passed');

  // Test Case 12: Community Leaderboard reflects all 3 distinct trainees with their custom stats
  const lbRes = await fetch(`${BASE_URL}/api/gym/leaderboard`);
  const lbJson = await lbRes.json();
  if (!lbJson.success || lbJson.leaderboard.length < 3) {
    throw new Error('❌ Test Case 12 Failed: Leaderboard did not contain all users');
  }
  const thorLb = lbJson.leaderboard.find(u => u.displayName === 'Thor Allfather');
  const athenaLb = lbJson.leaderboard.find(u => u.displayName === 'Goddess Athena');
  if (!thorLb || !athenaLb) {
    throw new Error('❌ Test Case 12 Failed: Custom profiles missing from leaderboard');
  }
  console.log('✅ 11. Community Leaderboard Aggregates All Profiles Accurately Passed');

  console.log('\n🎉 ALL 11 MULTI-TENANT PROFILE & DATA ISOLATION TESTS PASSED WITH 100% SUCCESS!');
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
