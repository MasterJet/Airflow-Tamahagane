#!/bin/bash

# Positional arguments:
# inputFile, NumberOFRows, OutPutFile


if [ "$#" -ne 3 ]; then
    exit 1
else
    fileName=$1
    lines=$2
    outPutFile=$3
    sort -R $fileName | head -n $lines > $outPutFile
fi

