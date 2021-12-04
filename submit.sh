#!/usr/bin/bash
if [ -d "~/.themisSubmitter" ] 
then
    mkdir ~/.themisSubmitter
    echo "Please make sure to copy Peristéri.py into ~/.themisSubmitter"
else
    ~/.themisSubmitter/Peristéri.py $@
fi
