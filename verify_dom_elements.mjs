// verify_dom_elements.mjs
import fs from 'node:fs';

const html = fs.readFileSync('home_gym_zero_to_hero.html', 'utf-8');
console.log('HTML size:', html.length, 'bytes');

const checkIds = [
  'authModal', 'profilePassportModal', 'quickAccountChipsContainer',
  'authDisplayNameInput', 'authGoalInput', 'authStartWeightInput', 'authTargetWeightInput', 'authBioInput',
  'authUsernameInput', 'authPasswordInput', 'authErrorMsg', 'authSubmitBtn',
  'passportAvatar', 'passportDisplayName', 'passportUsernameBadge', 'passportBio',
  'passportDayVal', 'passportStreakVal', 'passportWorkoutsVal', 'passportGoalBadge', 'passportRoleBadge',
  'editDisplayNameInput', 'editGoalInput', 'editTargetWeightInput', 'editBioInput', 'editProfileMsg'
];

let missing = 0;
for (const id of checkIds) {
  if (!html.includes(`id="${id}"`)) {
    console.error(`❌ MISSING ID: ${id}`);
    missing++;
  }
}

if (missing === 0) {
  console.log(`✅ ALL ${checkIds.length} CRITICAL 100X DOM IDs ARE PRESENT!`);
} else {
  console.error(`❌ ${missing} DOM IDs missing`);
  process.exit(1);
}
