#!/bin/bash

# Positional arguments:
# inputFile, NumberOfPieces, Suffix, outputPath
# NumberOfPieces, split in that many pieces 
# Suffix, add suffix in file names 


if [ "$#" -lt 4 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, NumberOfPieces, Suffix, outputPath"
    exit 1
else
    inputFile=$1
    NumberOfPieces=$2
    Suffix=$3
    OutputPath=$4
   
   
   split -n l/$NumberOfPieces -a1 -d $inputFile $OutputPath/$Suffix  

    
   
fi

