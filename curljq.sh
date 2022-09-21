#!/bin/env sh

# $1 being the json input to POST to the API.
# (And included curl's -s for silence.)
curl -sX POST                                   \
    http://localhost:49151/generate             \
    --header "Content-Type: application/json"   \
    -d @"$1"                                    \
    | jq .
