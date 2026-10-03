const fs = require('fs');

const fileContent = fs.readFileSync('data_interactive_tools.py', 'utf-8');
const match = fileContent.match(/TOOLS_JS\s*=\s*"""([\s\S]*?)"""/);
const jsCode = match[1];

// Let's create a full DOM mock for TOOLS_JS
const dom = {};
const html = fs.readFileSync('god_level_system_design.html', 'utf-8');
const idMatches = [...html.matchAll(/id=["']([^"']+)["']/g)].map(m => m[1]);
for (const id of idMatches) {
  dom[id] = {
    id,
    value: '100',
    innerText: '',
    innerHTML: '',
    style: {},
    className: '',
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    setAttribute: () => {},
    getAttribute: () => '',
    appendChild: () => {},
    scrollIntoView: () => {}
  };
}

global.document = {
  getElementById: (id) => dom[id] || null,
  querySelectorAll: () => [],
  querySelector: () => null,
  createElement: (tag) => ({ style: {}, classList: { add: () => {} }, appendChild: () => {}, textContent: '' })
};

global.window = {
  setInterval: () => 1,
  clearInterval: () => {},
  setTimeout: (cb) => cb(),
  clearTimeout: () => {}
};

eval(jsCode);

console.log('Testing inspectNode...');
inspectNode('client');
inspectNode('cdn');
inspectNode('l4');
console.log('inspectNode passed!');

console.log('Testing recomputeCost...');
recomputeCost();
console.log('recomputeCost passed!');

console.log('Testing renderLiveHashRing...');
renderLiveHashRing();
console.log('renderLiveHashRing passed!');

console.log('Testing startLiveRlEngine...');
startLiveRlEngine();
console.log('startLiveRlEngine passed!');

console.log('Testing renderStudioTimer...');
renderStudioTimer();
console.log('renderStudioTimer passed!');

console.log('ALL TOOLS FUNCTIONS TESTED & PASSED 100%!');
