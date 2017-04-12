#!/bin/bash

# Positional arguments:
# inputFile, FiledSep, ColuNumberToSort, Order, Unique, outPutFile
# is also work for + and - values

if [ "$#" -lt 6 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, FiledSep, ColuNumberToSort, Order d/R/n, Unique, outPutFile"
    exit 1
else
    inputFile=$1
    FiledSep=$2
    ColuNumberToSort=$3
    Order=$4
    unique=$5
    outPutFile=$6

    cmdUnique=""
    cmdOrder=""

    if [ $unique == 1 ]; then
        cmdUnique=" --unique "
        ColuNumberToSort=$ColuNumberToSort,1
    fi    

    if [ "$FiledSep" == " " ]; then
        cmdFiledSep=""
    else
        cmdFiledSep=" -t$FiledSep "
    fi

    if [ "$Order" == "d" ] ; then
      cmdOrder=" -r "
    elif [ "$Order" == "R" ] ; then
      cmdOrder=" -R "
    else 
       cmdOrder=""
    fi

    sort $cmdFiledSep $cmdUnique $cmdOrder -V -f -k $ColuNumberToSort $inputFile > $outPutFile
fi

