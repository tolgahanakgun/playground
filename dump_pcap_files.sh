#!/bin/bash

if [ $# -eq 0 ]; then
    echo "This script dumps all the tcp streams in a pcap file to files."
    echo "Usage: ./dump_pcap_files.sh file.pcap"
    exit
fi

END=$(tshark -r $1 -T fields -e tcp.stream | sort -n | tail -1)
for ((i=0;i<=END;i++))
do
    tshark -r $1 -qz follow,tcp,raw,$i | tail -n +7 | head -n -1 | xxd -r -p - > follow-stream-$i.bin
    file follow-stream-$i.bin
done
