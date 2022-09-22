#!/bin/env bash

cat << "HEAD"
{
    "text": {
HEAD
echo '        '\"in_64\": \"$(base64 - << "TO_ENCODE"
from time import time

start = time()

for i in range(9):
TO_ENCODE
)\"
cat << "TAIL"
    },
    "do_sample": true,
    "top_k": 10,
    "temperature": 0.5,
    "max_length": 256
}
TAIL
