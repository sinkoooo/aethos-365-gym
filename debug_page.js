import fs from 'fs';

const html = fs.readFileSync('god_level_system_design.html', 'utf-8');

// Find all inline scripts
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let scriptIndex = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  scriptIndex++;
  const scriptContent = match[1];
  console.log(`\n--- INLINE SCRIPT ${scriptIndex} ---`);

  // Check getElementById references
  const idRegex = /document\.getElementById\(['"]([^'"]+)['"]\)/g;
  let idMatch;
  const ids = [];
  while ((idMatch = idRegex.exec(scriptContent)) !== null) {
    ids.push(idMatch[1]);
  }

  const missing = [];
  for (const id of ids) {
    const hasDouble = html.includes(`id="${id}"`);
    const hasSingle = html.includes(`id='${id}'`);
    if (!hasDouble && !hasSingle) {
      missing.push(id);
    }
  }

  console.log(`Script ${scriptIndex} referenced ${ids.length} IDs.`);
  if (missing.length > 0) {
    console.log(`MISSING IDs in HTML for Script ${scriptIndex}:`, [...new Set(missing)]);
  } else {
    console.log(`All referenced IDs present in HTML.`);
  }
}
