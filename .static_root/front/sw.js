// 스토리지에 저장될 이름, 캐싱 할 파일 목록

var CACHE_NAME = 'ICISTS-offline-v1';
var filesToCache = [
    'index.html',
    '/',
    '/img',
    '/img/logo.png',
    '/img/icons/144x.png',
    '/img/icons/192x.png',
    '/img/icons/512x.png',
    '/css',
    '/css/reset.css',
    '/css/style.css',
    '/html/',
    '/html/NewsFeed.html',
    '/html/Schedule.html',
    '/html/Survey.html',
    '/html/QnA.html',
    '/html/Map.html',
    '/js',
    '/js/jquery-2.1.1.js',
    '/js/main.js',
    '/js/modernizr.js'
];

self.addEventListener('install', function(event) {
    console.log('[ServiceWorker Install]');
    event.waitUntil(
        // 웹 자원 캐싱
        caches.open(CACHE_NAME)
        .then(function(cache) {
            // PWA 파일 넣기
            // console.log('Opened cache');
            return cache.addAll(filesToCache);
        })
        .catch(function(error) {
            return console.log(error);
        })
    );
});

self.addEventListener('fetch', function(event) {
    console.log('[ServiceWorker fetch]', event.request);
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                return response || fetch(event.request);
            })
            .catch(function(error) {
                return console.log(error);
            })
    );
});

// self.addEventListener('activate', function(event) {
//     var newCacheList = ['ICISTS-offline-v2']
//     event.waitUntil(
//         caches.keys().then(function(cacheList) {
//             return Promise.all(
//                 cacheList.map(function(cacheName) {
//                     if(newCacheList.IndexOf(cacheName) === -1) {
//                         return caches.delete(cacheName);
//                     }
//                 })
//             );
//         }).catch(function(error) {
//             return console.log(error);
//         })
//     );
// });