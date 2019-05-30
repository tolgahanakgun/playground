#!/bin/bash

declare -a base58=(
      1 2 3 4 5 6 7 8 9
    A B C D E F G H   J K L M N   P Q R S T U V W X Y Z
    a b c d e f g h i j k   m n o p q r s t u v w x y z
)

convertToBase58() {
    echo -n "$1" | sed -e's/^\(\(00\)*\).*/\1/' -e's/00/1/g' | tr -d '\n'
    dc -e "16i ${1^^} [3A ~r d0<x]dsxx +f" |
    while read -r n; do echo -n "${base58[n]}"; done
}

# idetintifying byte is $1
# key is $2
IDENTIFYINGBYTE=$1 # first arg
KEY=$2 # second arg

# add idetintifying byte to beginning, for bitcoin identifying byte is 0x80
EXTENDEDKEY=$(echo $IDENTIFYINGBYTE$KEY)
FIRSTHASH=$(echo -n "$EXTENDEDKEY" |xxd -r -p |sha256sum -b|awk '{print $1}')
SECONDHASH=$(echo -n "$FIRSTHASH" |xxd -r -p |sha256sum -b|awk '{print $1}')
CHECKSUM=$(echo $SECONDHASH|cut -c1-8)
FINAL=$(echo $EXTENDEDKEY$CHECKSUM)
FINAL=$(convertToBase58 $FINAL)
echo $FINAL
