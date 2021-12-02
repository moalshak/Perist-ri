pip install PyYAML 
pip install tk 
pip install bs4 
pip install easygui 
pip install requests 
pip install BeautifulSoup 
pip install termcolor 
pip install pathlib
pip install html5lib
mkdir ~/.themisSubmitter 
cp Peristéri.py ~/.themisSubmitter 
chmod +x ~/.themisSubmitter/Peristéri.py

echo "Are you using Ubuntu? (y/N) "
read answer
if [ "$answer" = "y" ]
then
    echo "Using Ubuntu"
    sudo add-apt-repository ppa:neurobin/ppa
    sudo apt-get update
    sudo apt-get install shc
else
    git clone git@github.com:neurobin/shc.git
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
rm sumit
echo "Everything installed successfully"