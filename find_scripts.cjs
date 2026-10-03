const fs = require('fs');
const html = fs.readFileSync('god_level_system_design.html', 'utf-8');
const lines = html.split('\n');
lines.forEach((l, i) => {
  if (l.includes('<script') || l.includes('</script>')) {
    console.log(`Line ${i+1}: ${l.trim().substring(0, 80)}`);
  }
});
