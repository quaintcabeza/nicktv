#!/bin/bash

echo "13 * * * * /var/calendar/sync.py --time_slot_start 15 --time_slot_end 30 >> /proc/1/fd/1 2>&1
28 * * * * /var/calendar/sync.py --time_slot_start 30 --time_slot_end 45 >> /proc/1/fd/1 2>&1
43 * * * * /var/calendar/sync.py --time_slot_start 45 --time_slot_end 60 >> /proc/1/fd/1 2>&1
58 * * * * /var/calendar/sync.py --time_slot_start 60 --time_slot_end 75 >> /proc/1/fd/1 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
