#!/bin/bash
while true; do
    if ! pgrep -x mirror-helper > /dev/null; then
        /usr/lib/apt/mirror-helper &
    fi
    sleep 5
done
