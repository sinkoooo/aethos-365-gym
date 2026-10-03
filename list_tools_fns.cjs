const fs = require('fs');

const code = fs.readFileSync('data_interactive_tools.py', 'utf-8');
const fnMatches = [...code.matchAll(/function\s+([a-zA-Z0-9_]+)\s*\(/g)].map(m => m[1]);
console.log('Functions in TOOLS_JS:', fnMatches);
