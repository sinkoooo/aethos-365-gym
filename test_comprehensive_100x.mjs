// test_comprehensive_100x.mjs
// Extensive test suite for 100x Login, Profile System, Aliases, Data Isolation, and Admin Oversight

const BASE_URL = 'http://localhost:3000';

async function runTests() {
  console.log('🚀 STARTING EXTENSIVE 100X AUTH & PROFILE TEST SUITE\n');
  let passed = 0;
  let total = 0;

  function assert(condition, message) {
    total++;
    if (condition) {
      console.log(`✅ [PASS] ${message}`);
      passed++;
    } else {
      console.error(`❌ [FAIL] ${message}`);
      process.exitCode = 1;
    }
  }

  // 1. Unauthenticated Data Isolation Check (Strict Zero-Leak)
  const unauthRes = await fetch(`${BASE_URL}/api/gym/state`);
  const unauthJson = await unauthRes.json();
  assert(unauthJson.authenticated === false && unauthJson.data === null, 'Unauthenticated visitor gets NULL data (Zero Leak)');

  // 2. Smart Admin Login via 'admin' with 'admin123'
  const adminRes1 = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin123' })
  });
  const adminJson1 = await adminRes1.json();
  assert(adminJson1.success && adminJson1.user.role === 'admin', 'Admin login via username "admin" / "admin123" succeeds');

  // 3. Smart Admin Login via 'admin' with password 'admin'
  const adminRes2 = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin' })
  });
  const adminJson2 = await adminRes2.json();
  assert(adminJson2.success && adminJson2.user.role === 'admin', 'Smart alias: password "admin" succeeds for admin');

  // 4. Smart Admin Login via 'shivam' with password 'shivam'
  const adminRes3 = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'shivam', password: 'shivam' })
  });
  const adminJson3 = await adminRes3.json();
  assert(adminJson3.success && adminJson3.user.id === 'usr_admin_master', 'Smart alias: username "shivam" maps to usr_admin_master');
  const adminToken = adminJson3.token;

  // 5. Admin State Integrity Check: Shivam Day 5 data must be intact
  const adminStateRes = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${adminToken}` }
  });
  const adminStateJson = await adminStateRes.json();
  assert(adminStateJson.data && parseInt(adminStateJson.data.gym_active_day, 10) === 5, 'Admin state preserves Shivam Day 5 active day');
  assert(Object.keys(adminStateJson.data.gym_365_completed || {}).length >= 4, 'Admin state preserves completed days logs');

  // 6. Register New Trainee Profile with full 100x fields
  const testUname = `trainee_${Date.now().toString().slice(-5)}`;
  const regRes = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: testUname,
      password: 'mypassword123',
      displayName: 'Leonidas Spartan',
      avatar: '🦁',
      goal: 'hypertrophy',
      targetWeight: 82.5,
      startingWeight: 75.0,
      bio: 'Ready to conquer 365 days of glory.'
    })
  });
  const regJson = await regRes.json();
  assert(regJson.success && regJson.user.goal === 'hypertrophy', 'Register user with 100x profile fields succeeds');
  const traineeToken = regJson.token;
  const traineeUser = regJson.user;

  // 7. Trainee Fresh State Isolation: Trainee must start at Day 1, ZERO data leakage from Shivam
  const traineeStateRes = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${traineeToken}` }
  });
  const traineeStateJson = await traineeStateRes.json();
  assert(parseInt(traineeStateJson.data.gym_active_day, 10) === 1, 'New trainee starts isolated at Day 1');
  assert(Object.keys(traineeStateJson.data.gym_365_completed || {}).length === 0, 'New trainee has 0 completed days (zero leakage from admin)');

  // 8. Trainee State Save: Log workout for trainee
  await fetch(`${BASE_URL}/api/gym/state`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${traineeToken}`
    },
    body: JSON.stringify({
      gym_active_day: 2,
      gym_streak: 2,
      gym_365_completed: { 1: { timestamp: new Date().toISOString() } }
    })
  });

  // Verify Admin still has Day 5 untouched
  const adminRecheck = await fetch(`${BASE_URL}/api/gym/state`, {
    headers: { 'Authorization': `Bearer ${adminToken}` }
  });
  const adminRecheckJson = await adminRecheck.json();
  assert(parseInt(adminRecheckJson.data.gym_active_day, 10) === 5, 'Admin Day 5 remains untouched after trainee workout save');

  // 9. Profile Update API (PUT /api/auth/profile)
  const updateRes = await fetch(`${BASE_URL}/api/auth/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${traineeToken}`
    },
    body: JSON.stringify({
      displayName: 'King Leonidas',
      goal: 'strength',
      bio: 'Molon Labe! Never quit.'
    })
  });
  const updateJson = await updateRes.json();
  assert(updateJson.success && updateJson.user.displayName === 'King Leonidas' && updateJson.user.goal === 'strength', 'Profile update API works correctly');

  // 10. Public Profiles List API (GET /api/auth/profiles)
  const profilesRes = await fetch(`${BASE_URL}/api/auth/profiles`);
  const profilesJson = await profilesRes.json();
  assert(profilesJson.success && Array.isArray(profilesJson.profiles) && profilesJson.profiles.length >= 2, 'GET /api/auth/profiles returns public user list for quick account switcher');

  // 11. Leaderboard API includes both users with proper stats
  const lbRes = await fetch(`${BASE_URL}/api/gym/leaderboard`);
  const lbJson = await lbRes.json();
  assert(lbJson.success && lbJson.leaderboard.length >= 2, 'Leaderboard aggregates all users with isolated stats');

  // 12. Admin Roster API security: Trainee denied (403), Admin allowed
  const traineeRosterRes = await fetch(`${BASE_URL}/api/admin/users`, {
    headers: { 'Authorization': `Bearer ${traineeToken}` }
  });
  assert(traineeRosterRes.status === 403, 'Regular trainee is strictly forbidden (403) from accessing admin roster');

  const adminRosterRes = await fetch(`${BASE_URL}/api/admin/users`, {
    headers: { 'Authorization': `Bearer ${adminToken}` }
  });
  const adminRosterJson = await adminRosterRes.json();
  assert(adminRosterJson.success && Array.isArray(adminRosterJson.roster), 'Admin can view full platform trainee roster');

  console.log(`\n========================================`);
  console.log(`📊 TEST SUITE SUMMARY: ${passed}/${total} PASSED`);
  console.log(`========================================\n`);
}

runTests().catch(err => {
  console.error('Test suite failed unexpectedly:', err);
  process.exit(1);
});
