#!/bin/bash

# Positional arguments:
# inputFile, FiledSep, FieldRange, remove 1/0, outputFile, output-delimiter

# inputFile file subject file
# FiledSep --delimiter default is ','
# FieldRange can be 3,7,9 or one like mention below
# N     N'th byte, character or field, counted from 1
# N-    from N'th byte, character or field, to end of line
# N-M   from N'th to M'th (included) byte, character or field
# -M    from first to M'th (included) byte, character or field
# remove --complement delete selected bytes or fields

# --output-delimiter '|'

if [ "$#" -lt 5 ]; then
	echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, FiledSep, FieldRange, remove 1/0, outputFile, [output-delimiter]"
    exit 1
else
    inputFile=$1
    FiledSep=$2
    FieldRange=$3
    remve=$4
    outputFile=$5
    cmdFiledSep=""
    cmdRemove=""
    cmdOutputDelimiter=""

    if [ "$FiledSep" == " " ]; then
        cmdFiledSep=" -d, " 
    else
        cmdFiledSep=" -d$FiledSep "
    fi
    if [ "$remve" == 1 ]; then
        cmdRemove=" --complement " 
    fi

    if [ -z ${6+x} ]; then 
    	cmdOutputDelimiter=""
    else
    	cmdOutputDelimiter=" --output-delimiter $6 "
    fi	
  cut $cmdOutputDelimiter --only-delimited $cmdRemove -f $FieldRange $cmdFiledSep $inputFile > $outputFile
fi

