import fs from 'fs';

const html = fs.readFileSync('god_level_system_design.html', 'utf-8');

// Let's create a minimal DOM simulation in Node.js to test every single function
const domElements = {};

// Extract all elements with an ID from html
const idMatches = [...html.matchAll(/id=["']([^"']+)["']/g)].map(m => m[1]);
for (const id of idMatches) {
  domElements[id] = {
    id: id,
    innerHTML: '',
    innerText: '',
    value: '100',
    className: '',
    classList: {
      add: (c) => {},
      remove: (c) => {},
      contains: (c) => false
    },
    setAttribute: (k, v) => {},
    getAttribute: (k) => '',
    style: {}
  };
}

// Global browser mocks
global.document = {
  getElementById: (id) => {
    return domElements[id] || null;
  },
  querySelectorAll: (selector) => {
    return [];
  },
  querySelector: (selector) => {
    return null;
  },
  addEventListener: (event, cb) => {}
};

global.window = {
  addEventListener: (event, cb) => {},
  AudioContext: class {
    constructor() { this.currentTime = 0; }
    createOscillator() { return { type: '', frequency: { setValueAtTime: () => {} }, connect: () => {}, start: () => {}, stop: () => {} }; }
    createGain() { return { gain: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} }, connect: () => {} }; }
  },
  localStorage: {
    getItem: (k) => null,
    setItem: (k, v) => {}
  }
};

global.localStorage = global.window.localStorage;

global.lucide = {
  createIcons: () => {}
};

global.confetti = () => {};

// Extract inline scripts
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let scriptIdx = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  scriptIdx++;
  const code = match[1];
  console.log(`\nEvaluating Script ${scriptIdx} in mock environment...`);
  try {
    (0, eval)(code);
    console.log(`Script ${scriptIdx} evaluated without syntax errors.`);
    if (scriptIdx === 2) {
      console.log('Testing renderSidebar()...');
      eval('renderSidebar()');
      console.log('renderSidebar() SUCCESS! Container innerHTML length:', domElements['sidebar-items-list'].innerHTML.length);

      console.log('Testing loadTopic()...');
      eval('loadTopic()');
      console.log('loadTopic() SUCCESS! Title:', domElements['topic-title'].innerText);
      console.log('Guidebook length:', domElements['topic-guidebook-body'].innerHTML.length);
      console.log('Topology length:', domElements['topic-topology-svg'].innerHTML.length);
      console.log('Code block length:', domElements['topic-code-block'].innerText.length);
      console.log('Disaster length:', domElements['topic-disaster-body'].innerHTML.length);
      console.log('Interview length:', domElements['topic-interview-body'].innerHTML.length);

      console.log('Testing renderBattleCard()...');
      eval('renderBattleCard()');
      console.log('renderBattleCard() SUCCESS! Question:', domElements['bc-drill-q'].innerText);

      console.log('Testing updateMasteryStatus()...');
      eval('updateMasteryStatus()');
      console.log('updateMasteryStatus() SUCCESS!');
    }
  } catch (err) {
    console.error(`Script ${scriptIdx} CRASHED:`, err);
  }
}
