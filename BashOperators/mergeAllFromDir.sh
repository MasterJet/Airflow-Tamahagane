#!/bin/bash

# Positional arguments:
# inputDir, OutPutFile
# will merge all files from inputDir to OutPutFile

if [ "$#" -ne 2 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputDir, OutPutFile"
    exit 1
else
    inputDir=$1
    OutPutFile=$2
    
    cat $inputDir/* > $OutPutFile
fi

