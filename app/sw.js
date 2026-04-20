const CACHE_NAME = 'dips-tester-v9';
const URLS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './data/topics.json',
  './data/questions_sv.json',
  './data/questions_en.json',
  './data/flashcards.json',
  './data/essays.json',
  './data/mocks.json',
  './data/audio_map.json',
  './data/resources.json',
  './data/question_batteries.json',
  './data/source_index.json',
  './data/leaders.json',
  './data/translations.json',
  './data/regents.json',
  './data/world-110m.json',
  './data/world-map.svg',
  './data/world-map.svg',
  '../data/topics.json',
  '../data/questions_sv.json',
  '../data/questions_en.json',
  '../data/flashcards.json',
  '../data/essays.json',
  '../data/mocks.json',
  '../data/audio_map.json',
  '../data/resources.json',
  '../data/question_batteries.json',
  '../data/source_index.json',
  '../data/leaders.json',
  '../data/translations.json',
  '../data/regents.json',
  '../data/world-110m.json',
  '../data/world-map.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    }).catch(() => caches.match('./index.html'))
  );
});
