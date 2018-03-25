#!/bin/bash

WIFIMON=wlan1
if [! -z "$1" ]; then
    WIFIMON=$1
fi

#  put wlan0 in monitoring mode
sudo airmon-ng start $WIFIMON 

# activate airodump and have it output data to /tmp directory
sudo airodump-ng --output-format csv --write /tmp/capture ${WIFIMON}mon
