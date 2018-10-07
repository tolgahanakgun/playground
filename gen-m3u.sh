#!/bin/bash
# This script creates a m3u playlist from the radio stations in www.internet-radio.com
if [ $# -ne 2 ]
then
	echo "Plesase supply two paramters"
	echo "Usage: gen-m3u.sh https://www.internet-radio.com/stations/MUSIC_TYPE/ filename"
	exit 1
fi
URL=$1
OUT=$2
wget -qO- ${URL} | grep -o "/servers/tools/*.*listen\.pls" | grep -Po "http://*.*listen\.pls" | uniq > ${OUT}.m3u