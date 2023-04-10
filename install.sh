#!/bin/bash

printf "Welcome to the installer of Peristeri 2.0\n"
printf "Please make sure you do not already have a binary called 'submit'\n"

printf "Installing...\n"

if [ -f "/usr/local/bin/submit" ]; then
    printf "Moving old binary to $(pwd)...\n"
    mv /usr/local/bin/submit .
fi

chmod +x submit.sh
sudo cp submit.sh /usr/local/bin/submit