'use strict';

const CACHE_VERSION = 2;
const CACHE_PREFIX = "glyph-fonts";
const BASE_URL = "{{ .Site.BaseURL }}";
const CACHE_NAME = `${CACHE_PREFIX}-v${CACHE_VERSION}`;

// key is the url, value is the cache duration in days or 'version_change'
const CACHE_DESCRIPTION = {
    [`${BASE_URL}BabelStoneHan.woff`]: 'version_change',
    [`${BASE_URL}index.json`]: 1,
}

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

function fetch_from_network(request, cache) {
    return fetch(request)
        .then((response) => {
            console.debug("  Response for %s from network is: %O", request.url, response);

            if (response.status < 400) {
                const headers = new Headers(response.headers);
                headers.set('sw-cached-at', Date.now());
                response.clone().arrayBuffer().then((buffer) => {
                    console.debug("  Caching the response to", request.url);
                    cache.put(request, new Response(buffer, { headers, url: request.url }));
                })
                return response;
            } else {
                console.debug("  Not caching the response to", request.url);
                return response;
            }
        })
        .catch((error) => {
            console.error("  Error in fetch handler:", error);
            throw error;
        });
}

self.addEventListener("fetch", (event) => {
    const url = event.request.url;
    const cache_duration = CACHE_DESCRIPTION[url];
    if (cache_duration) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((response) => {
                    if (response) {
                        const cached_time = Number(response.headers.get('sw-cached-at'));
                        const cache_age_days = (Date.now() - cached_time) / (24 * 60 * 60 * 1000);
                        console.debug(" Found response %O for %s, %s days old:", response, url, cache_age_days.toFixed(2));
                        if (cache_duration !== 'version_change' && cache_age_days > cache_duration) {
                            console.debug(" Cache expired for %s", url);
                            return fetch_from_network(event.request, cache);
                        }
                        return response;
                    }
                    console.debug(" Cache miss for %s", url);
                    return fetch_from_network(event.request, cache);
                });
            }),
        );
    }
});
