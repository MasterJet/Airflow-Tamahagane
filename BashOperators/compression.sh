#!/bin/bash

# Positional arguments:
# inputFile, Operation, type
#
# This Operator can archive or extract  
# with a given type, 

if [ "$#" -ne 4 ]
 then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** inputFile, Operation a/e, type tar/zip/gzip/bzip2"
    exit 1
else
  fileName=$1
  operation=$2
  type=$3
  outputDirectory=$4

  if [ $operation == "a" ]
    then
      case $type in 
        
        "zip") tar -czf $fileName.zip $fileName ;;
        "tar") tar -czf $fileName.tar $fileName ;;
        "gzip") tar -czf $fileName.gz $fileName ;;
        "bzip2") tar -czf $fileName.bz2 $fileName ;;
        *) echo "Unsupported archive type" ;;
       esac	    	

    elif [ $operation == "e" ]; 
    then
         case $type in 
        
        "zip") tar xzf  $fileName -C $outputDirectory ;;
        "tar") tar xzf  $fileName -C $outputDirectory;;
        "gzip") tar xzf  $fileName -C $outputDirectory;;
        "bzip2") tar xzf  $fileName -C $outputDirectory;;
        *) echo "Unsupported archive type" ;;
       esac        
    else
        echo "Invalid argument"
    fi
fi

