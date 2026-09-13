/* Offline app shell for ZabAudioBooker.
 *
 * Caches only the page itself and its small local assets — not the model
 * weights or the CDN libraries (kokoro-js, lamejs, pdfjs, fflate). Those are
 * many megabytes, already cached by the browser's own HTTP cache and by
 * kokoro-js's own storage, and out of scope here: this service worker's job
 * is just "the app opens even with no network", not "the whole model is
 * guaranteed offline". Bump CACHE_NAME to ship a new shell version; the old
 * cache is dropped on activate.
 */

const CACHE_NAME = "zab-shell-v1";
const SHELL_FILES = ["./zabaudiobooker.html", "./zabaudiobooker.webmanifest", "./icon.svg"];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_FILES))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(names => Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  // Only the app shell, same-origin, GET requests. Everything else — CDN
  // libraries, the model weights, cross-origin anything — passes straight
  // through untouched.
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async cache => {
      const cached = await cache.match(req);
      // Stale-while-revalidate: serve the cached shell instantly, and if the
      // network is reachable, quietly refresh the cache for next time.
      const network = fetch(req).then(res => {
        if (res.ok) cache.put(req, res.clone());
        return res;
      }).catch(() => null);
      return cached || (await network) || Response.error();
    })
  );
});
