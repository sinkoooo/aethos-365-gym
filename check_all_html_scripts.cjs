const fs = require('fs');
const { execSync } = require('child_process');

const html = fs.readFileSync('god_level_system_design.html', 'utf-8');
const scriptRegex = /<script(?:\s+type=["'](?:text\/javascript)?["'])?>([\s\S]*?)<\/script>/gi;
let match;
let idx = 0;
let errors = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  const code = match[1].trim();
  if (!code || code.includes('tailwind.config')) continue;
  idx++;
  const filename = `temp_check_script_${idx}.js`;
  fs.writeFileSync(filename, code);
  try {
    execSync(`node --check ${filename}`);
    console.log(`Script ${idx} is VALID syntax (bytes: ${code.length})`);
  } catch (err) {
    console.error(`ERROR in Script ${idx}:`, err.message);
    errors++;
  } finally {
    try { fs.unlinkSync(filename); } catch(e){}
  }
}

if (errors === 0) {
  console.log(`ALL SCRIPTS (${idx} scripts) PASSED SYNTAX CHECK WITH 0 ERRORS!`);
} else {
  console.error(`${errors} scripts failed syntax check!`);
  process.exit(1);
}
