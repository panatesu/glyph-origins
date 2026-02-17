#!/bin/bash
docker run --rm -p 1313:1313 -v "$(pwd)":/project ghcr.io/gohugoio/hugo server --buildDrafts --bind 0.0.0.0