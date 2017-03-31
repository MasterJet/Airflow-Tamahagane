#!/bin/bash

# Positional arguments:
# inputFile, NumberOFRows, OutPutFile
# NumberOFRows is also work for + and - values

if [ "$#" -ne 3 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, NumberOFRows, OutPutFile"
    exit 1
else
    fileName=$1
    lines=$2
    outPutFile=$3
    head $fileName -n $lines > $outPutFile
fi

