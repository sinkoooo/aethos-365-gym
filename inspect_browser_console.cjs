const http = require('http');

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const targets = JSON.parse(data);
      console.log('Open targets in Edge:', targets.length);
      for (const t of targets) {
        console.log(`- Target: [${t.type}] ${t.title} (${t.url})`);
        console.log(`  WebSocketDebuggerUrl: ${t.webSocketDebuggerUrl}`);
      }
    } catch(e) {
      console.error('Error parsing JSON:', e.message);
    }
  });
}).on('error', err => {
  console.error('HTTP Error:', err.message);
});
