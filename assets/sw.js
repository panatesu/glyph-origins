const CACHE_VERSION = 1;
const CACHE_PREFIX = "glyph-fonts";
const CACHE_NAME = `${CACHE_PREFIX}-v${CACHE_VERSION}`;

const FONT_REGEX = /BabelStoneHan\.woff$/;

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) =>
            Promise.all(
                cacheNames.map((cacheName) => {
                    if (
                        cacheName.startsWith(CACHE_PREFIX) &&
                        cacheName.slice(CACHE_PREFIX.length + 1) !== `v${CACHE_VERSION}`
                    ) {
                        console.debug("Deleting out of date cache:", cacheName);
                        return caches.delete(cacheName);
                    }
                    return undefined;
                }),
            ),
        ),
    );
});

self.addEventListener("fetch", (event) => {
    if (!FONT_REGEX.test(event.request.url)) {
    } else {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((response) => {
                    if (response) {
                        console.debug(" Found response in cache:", response);
                        return response;
                    }
                    console.debug(" No response for %s found in cache. About to fetch from network…", event.request.url);

                    return fetch(event.request.url)
                        .then((response) => {
                            console.debug("  Response for %s from network is: %O", event.request.url, response);

                            if (response.status < 400) {
                                console.debug("  Caching the response to", event.request.url);
                                cache.put(event.request, response.clone());
                            } else {
                                console.debug("  Not caching the response to", event.request.url);
                            }

                            return response;
                        })
                        .catch((error) => {
                            console.error("  Error in fetch handler:", error);
                            throw error;
                        });
                });
            }),
        );
    }
});
