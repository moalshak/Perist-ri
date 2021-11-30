#!/usr/bin/bash
if [ -d "~/.themisSubmitter" ] 
then
    mkdir ~/.themisSubmitter
    echo "Please make sure to copy Peristéri.py into ~/.themisSubmitter"
else
    python3 ~/.themisSubmitter/Peristéri.py $1 $2
fi