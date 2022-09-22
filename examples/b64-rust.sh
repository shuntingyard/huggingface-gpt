#!/bin/env bash

cat << "HEAD"
{
    "text": {
HEAD
echo '        '\"in_64\": \"$(base64 - << "TO_ENCODE"
#[derive(Deserialize, Debug)]
struct Timeout(u32);
impl Default for Timeout {
TO_ENCODE
)\"
cat << "TAIL"
    },
    "do_sample": true,
    "top_k": 10,
    "temperature": 0.05,
    "max_length": 256
}
TAIL
