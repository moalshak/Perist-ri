FILE=~/.themisSubmitter/Peristeri.py

if [ -f "$FILE" ]; then
    echo "$FILE exists"
    echo "Do you want to overwrite it? (y/N)"
    read -n 1 -s answer
    if [ [ "$answer" -eq "y" || "$answer" -eq "Y" ] ]
        then
        echo "Overwriting $FILE"
        rm $FILE
        pip install -r requierments
        mkdir ~/.themisSubmitter
        cp Peristeri.py ~/.themisSubmitter 
        chmod +x ~/.themisSubmitter/Peristeri.py

        echo "Are you using Ubuntu? (y/N) "
        read answer
        if [ "$answer" = "y" ] || [ "$answer" = "Y" ]
        then
            echo "Using Ubuntu"
            sudo add-apt-repository ppa:neurobin/ppa
            sudo apt-get update
            sudo apt-get install shc
        else
            git clone https://github.com/neurobin/shc.git
            cd shc
            ./configure
            ./autogen.sh
            make
            sudo make install
            cd ..
        fi
        shc -f submit.sh -o submit
        sudo cp submit /usr/bin
        rm submit.sh.x.c
        rm -r -f shc
        rm submit
        echo "Everything installed successfully"
        echo "Conguratulations! You can now use the program!"
    else
        echo "Not overwriting $FILE"
    fi
fi
