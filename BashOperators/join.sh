#!/bin/bash

# Positional arguments:
# FirstFile, SecondFile, FirstKey, SecondKey, FieldSep, HasHeader/0/1, NumberOfHeaderRows, join left or right l/r , wdir,outputfile

if [ "$#" -lt 9 ]; then
    echo "*** Too Few Parameters" 
    echo "*** Required Parameters are"     
    echo "*** FirstFile, SecondFile, FirstKey, SecondKey, FieldSep, HasHeader/0/1, join left or right l/r , outputfile"
    exit 1
else
    FirstFile=$1
    SecondFile=$2
    FirstCol=$3
    SecondCol=$4
    FiledSep=$5
    HasHeader=$6
    Unpared=$7
    tempDir=$8
    outPutFile=$9
    unpare=""
    cmdHasHeader=""
    #LOCALE=C
    if [ $Unpared == "l" ] ; then
      unpare=" -a1 "
    elif [ $Unpared == "r" ] ; then
      unpare=" -a2 "
    else 
       unpare=""
    fi

    if [ "$FiledSep" == " " ]; then
        cmdFiledSep=""
    else
        cmdFiledSep=" -t$FiledSep "
    fi
      
    if [ $HasHeader == 1 ]; then
        cmdHasHeader=" --header "
        

      (head -n 1 $FirstFile && tail -n +2 $FirstFile | sort $cmdFiledSep -d -V -f -k $FirstCol) > $tempDir/tempFile1
      (head -n 1 $SecondFile && tail -n +2 $SecondFile | sort $cmdFiledSep -d -V -f -k  $SecondCol) > $tempDir/tempFile2
    else
      sort $cmdFiledSep -d -V -f -k $FirstCol $FirstFile > $tempDir/tempFile1
      sort $cmdFiledSep -d -V -f -k  $SecondCol $SecondFile > $tempDir/tempFile2 
   fi  

     join $cmdFiledSep $unpare $cmdHasHeader -1 $FirstCol -2 $SecondCol $tempDir/tempFile1 $tempDir/tempFile2 > $outPutFile


fi
