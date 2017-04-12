#!/bin/bash

# Positional arguments:
# inputFile, Search, multiple 0/1, completeWord 0/1, ignore-case  0/1, invert-match 0/1, max-count=NUM -1/any positive number,OutPutFile
# 


# -w, --word-regexp         force PATTERN to match only whole words
# -i, --ignore-case         ignore case distinctions
# -v, --invert-match        select non-matching lines
# -m, --max-count=NUM       stop after NUM matches

# -o, --only-matching       show only the part of a line matching PATTERN

if [ "$#" -lt 8 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, Search, -word-regexp 0/1, --ignore-case  0/1, --invert-match 0/1, --max-count=NUM -1/any positive number,OutPutFile"
    exit 1
else
    inputFile=$1
    Search=$2
    multiple=$3
    completeWord=$4
    ignoreCase=$5
    reverseSearch=$6
    rowLimit=$7

    outPutFile=$8

    switches=""
    if [ "$multiple" == 1 ]; then
        switches="$switches -E "    
    fi  
    if [ "$completeWord" == 1 ]; then
    	switches="$switches -w "	
    fi	
    if [ "$ignoreCase" == 1 ]; then
    	switches="$switches -i "	
    fi
    if [ "$reverseSearch" == 1 ]; then
    	switches="$switches -v "	
    fi	
    if [ "$rowLimit" != -1 ]; then
    	switches="$switches -m  $rowLimit"	
    fi
    
    cmd="grep $switches '$Search' $inputFile > $outPutFile"
    
    eval $cmd
fi

