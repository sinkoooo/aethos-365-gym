const fs = require('fs');

// Extract TOOLS_JS from data_interactive_tools.py
const fileContent = fs.readFileSync('data_interactive_tools.py', 'utf-8');
const match = fileContent.match(/TOOLS_JS\s*=\s*"""([\s\S]*?)"""/);

if (!match) {
  console.error('TOOLS_JS not found!');
  process.exit(1);
}

const jsCode = match[1];
console.log('Found TOOLS_JS code length:', jsCode.length);

try {
  new Function(jsCode);
  console.log('TOOLS_JS syntax is 100% VALID!');
} catch (err) {
  console.error('TOOLS_JS SYNTAX ERROR:', err);
}
