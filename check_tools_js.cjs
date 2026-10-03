const fs = require('fs');

const code = fs.readFileSync('data_interactive_tools.py', 'utf-8');
const lines = code.split('\n');
lines.forEach((l, i) => {
  if (l.includes('addEventListener') || l.includes('onload')) {
    console.log(`Line ${i+1}: ${l.trim()}`);
  }
});
