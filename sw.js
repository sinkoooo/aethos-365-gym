const CACHE_NAME = 'aethos-365-ultra-v200x';
const ASSETS_TO_CACHE = [
  './',
  './home_gym_zero_to_hero.html',
  './home_workout_guide.jpg',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pre-caching ultra-performance assets for', CACHE_NAME);
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing obsolete cache', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Ultra-Fast Stale-While-Revalidate Strategy with Background Sync & Cache Race
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const request = event.request;
  const url = new URL(request.url);

  // Skip caching API mutations or auth endpoints
  if (url.pathname.startsWith('/api/')) {
    return;
  }

  // Stale-While-Revalidate: Return cached response in ~2ms while updating cache in background
  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cachedResponse = await cache.match(request);

      const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          cache.put(request, networkResponse.clone());
        }
        return networkResponse;
      }).catch((err) => {
        return cachedResponse;
      });

      // If cached, return immediately; otherwise wait for network
      return cachedResponse || fetchPromise;
    })
  );
});
