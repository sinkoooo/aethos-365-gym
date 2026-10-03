const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = 8080;
const BASE_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=UTF-8',
  '.js': 'application/javascript; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.json': 'application/manifest+json; charset=UTF-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

function getLocalIp() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const net of interfaces[name]) {
      if (net.family === 'IPv4' && !net.internal && (name.toLowerCase().includes('wi-fi') || name.toLowerCase().includes('wireless') || name.toLowerCase().includes('ethernet') || net.address.startsWith('192.168.') || net.address.startsWith('10.'))) {
        return net.address;
      }
    }
  }
  return 'localhost';
}

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/' || reqPath === '') {
    reqPath = '/home_gym_zero_to_hero.html';
  }

  const filePath = path.join(BASE_DIR, decodeURIComponent(reqPath));
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
        res.end('404 Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain; charset=UTF-8' });
        res.end('500 Server Error: ' + err.code);
      }
      return;
    }

    res.writeHead(200, {
      'Content-Type': contentType,
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-cache'
    });
    res.end(content);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  const localIp = getLocalIp();
  console.clear();
  console.log('================================================================');
  console.log('       AETHOS 365 PRO - GOOGLE PIXEL MOBILE INSTALLER          ');
  console.log('================================================================\n');
  console.log(' 1. Connect your Google Pixel to the SAME Wi-Fi network.');
  console.log(' 2. Open Google Chrome on your Pixel and go to:\n');
  console.log(`       👉  http://${localIp}:${PORT}  👈\n`);
  console.log(' 3. In Chrome, tap "📲 Install App" or tap the three dots (⋮)');
  console.log('    in the top-right corner and select "Install app".\n');
  console.log(' 4. The app icon will appear in your Google Pixel app drawer.');
  console.log('    The Service Worker caches everything for 100% offline use.\n');
  console.log('----------------------------------------------------------------');
  console.log(' Server is live on 0.0.0.0:' + PORT + ' (Press Ctrl+C to stop)');
  console.log('================================================================\n');
});
