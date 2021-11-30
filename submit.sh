#!/usr/bin/bash
if [ -d "~/.themisSubmitter" ] 
then
    mkdir ~/.themisSubmitter
    cp Peristéri.py ~/.themisSubmitter
    chmod +x ~/.themisSubmitter/Peristéri.py
fi

~/.themisSubmitter/Peristéri.py $1 $2