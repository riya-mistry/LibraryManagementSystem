var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/administrator/base_layout',
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
  //console.log(event.request.url)
  //console.log(requestUrl.origin)
  //console.log(location.origin)
  //console.log(requestUrl.pathname)
    if (requestUrl.origin === location.origin) {
        //console.log('inside if');
        //console.log(requestUrl.pathname);
      if ((requestUrl.pathname === '/administrator/Books')) {
          //console.log('inside if');
        event.respondWith(caches.match('/administrator/base_layout'));
        return;
      }
    }
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
});