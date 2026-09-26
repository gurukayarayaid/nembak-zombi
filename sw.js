/* Service Worker Nembak Zombi — cache-first agar game jalan offline penuh. */
const CACHE = 'nembak-zombi-v2';

const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './assets/favicon.svg',
  './assets/favicon-48.png',
  './assets/favicon.ico',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/apple-touch-icon.png',
  './assets/bg-city.jpeg',
  './assets/btn-1p.png',
  './assets/btn-2p.png',
  './assets/btn-easy.png',
  './assets/btn-medium.png',
  './assets/btn-hard.png',
  './assets/header-mode.png',
  './assets/zombie1.png',
  './assets/zombie2.png',
  './assets/zombie3.png',
  './assets/zombie4.png',
  './assets/zombie5.png',
  './assets/zombie6.png',
  './assets/zombie7.png',
  './assets/bgm-menu.mp3',
  './assets/bgm-game.mp3',
  './assets/sfx-shoot.mp3',
  './assets/sfx-win.mp3',
  './assets/sfx-wrong.mp3'
];

// Pasang: pre-cache semua aset. Abaikan range header utk audio (baca penuh ke cache).
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// Aktifkan: hapus cache versi lama.
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Ambil: cache-first; audio/video dilewati range-request lalu disimpan utuh.
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return;   // biarkan request lintas origin lewat

  const isAudio = /\.(mp3|m4a|ogg|wav)$/i.test(url.pathname);

  e.respondWith((async () => {
    const cache = await caches.open(CACHE);

    // Halaman (navigasi): network-first supaya update cepat sampai ke pemain;
    // saat offline jatuh ke cache.
    if (e.request.mode === 'navigate') {
      try {
        const fresh = await fetch(e.request);
        try { cache.put('./index.html', fresh.clone()); } catch (_) {}
        return fresh;
      } catch (_) {
        return (await cache.match('./index.html')) || Response.error();
      }
    }

    const hit = await cache.match('./' + url.pathname.split('/').pop(), { ignoreSearch: true })
      || await cache.match(e.request, { ignoreSearch: true });
    if (hit) return hit;

    try {
      const res = await fetch(isAudio ? new Request(e.request, { headers: {} }) : e.request);
      if (res && (res.ok || res.type === 'opaque')) {
        try { cache.put(e.request, res.clone()); } catch (_) {}
      }
      return res;
    } catch (err) {
      const fallback = await cache.match('./index.html');
      if (fallback) return fallback;
      throw err;
    }
  })());
});
