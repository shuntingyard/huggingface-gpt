#!/bin/env bash

cat << "HEAD"
{
    "text": {
HEAD
echo '        '\"in_64\": \"$(base64 - << "TO_ENCODE"
#!/bin/bash
for i in {0..9}
do
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
