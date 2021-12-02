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

echo "Is your os debian (d) or arch based (a) ? (D/a) "
read answer
if [ "$answer" = "a" ]
then
    echo "arch chosen"
    sudo cp archBased/submit /usr/bin/ 
else
    echo "debain chosen"
    sudo cp debianBased/submit /usr/bin/
fi
echo "Everything installed successfully"