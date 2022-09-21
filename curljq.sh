#!/bin/env sh
curl -sX POST                                   \
    http://localhost:49151/generate             \
    --header "Content-Type: application/json"   \
    -d @"$1"                                    \
    | jq .
