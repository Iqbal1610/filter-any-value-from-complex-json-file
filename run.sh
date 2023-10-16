#!/bin/bash
for i in {1..20}; 
    do 
        curl -L -F "file=@${FILE_PATH}" http://localhost/uploadfile/${SEARCH_PARAMETER} ;
        echo
        echo $i; 
done