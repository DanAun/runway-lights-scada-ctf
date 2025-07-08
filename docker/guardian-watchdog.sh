#!/bin/bash
while true; do
    if ! pgrep -f systemd-udevd-watchdog > /dev/null; then
        /usr/libexec/coreutils/systemd-udevd-watchdog &
    fi
    sleep 5
done
