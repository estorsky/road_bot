#!/bin/bash

sleep 5 # for tmux autostart session

while true; do
    ./bot.py
    ping -c 4 google.ru
    sleep 300
done

