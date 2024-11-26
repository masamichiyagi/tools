##########################
# Utility
##########################
# zip, unrar
sudo apt-get update -y
sudo apt-get install zip -y
sudo apt-get install unrar -y

# wget
sudo apt-get install wget -y
sudo apt-get install curl -y

# zsh
sudo apt-get install zsh -y

# nkf
sudo apt-get install nkf -y

# git
sudo apt-get install git -y
# git config --global user.name "My Name"
# git config --global user.email "myname@example.com"
# cp vimrc ~/.vimrc

##########################
# Utility
##########################
# imagemagick convert
sudo apt-get install imagemagick -y
## sudo vim /etc/ImageMagick-6/policy.xml 
## -<policy domain="coder" rights="none" pattern="PDF" />
## +<policy domain="coder" rights="read|write" pattern="PDF" />
# image to text
sudo apt -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev libleptonica-dev tesseract-ocr-script-jpan tesseract-ocr-script-jpan-vert 


##########################
# PDF editor
##########################
## pdfs to pdf
sudo apt-get install ghostscript -y
## pdftotext, etc.
sudo apt-get install poppler-utils -y

##########################
# Text editor
##########################
# markdown
sudo apt install npm nodejs-legacy fonts-ipafont-gothic
sudo npm -g install markdown-pdf
# usage
# markdown-pdf document.md

##########################
# Script
##########################
# perl
sudo apt-get install perl -y
# python-pip
sudo apt-get install python-pip -y
sudo apt-get install python3-pip -y
sudo apt install -y python3.8
#デフォルトを変更
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
sudo update-alternatives --config python3

##########################
# Python tools
##########################
pip3 install numpy
pip3 install opencv-python
pip3 install pdf2image
pip3 install pdfkit
pip3 install pandas
pip3 install bs4
pip3 install lxml
pip3 install markdown
#pip3 install matplotlib
## PIL
pip3 install pillow

##########################
# Video and audio editor
##########################
## youtube-dl
# pip install youtube-dl
pip3 install -U yt-dlp
## ffmpeg
sudo apt-get install ffmpeg -y
### If you are unable to install ffmpeg,
### you install ffmpeg from a non-PPT public repository.
### -E option is proxy.
#sudo -E add-apt-repository ppa:mc3man/trusty-media
#sudo apt-get update
#sudo apt-get install ffmpeg
######## old version ffmpeg instal sumple
#sudo apt-get install build-essential automake autoconf zlib1g-dev libtool libx264-dev yasm
#wget http://ffmpeg.org/releases/ffmpeg-3.2.2.tar.bz2
#tar xjf ffmpeg-3.2.2.tar.bz2
#cd ffmpeg-3.2.2
#./configure --enable-libx264 --enable-gpl
#make
#sudo make install

##########################
# wav to text tool (English)
##########################
sudo apt install pocketsphinx pocketsphinx-en-us
#### how to use
## ffmpeg -i file.mp3 -ar 16000 -ac 1 file.wav
## pocketsphinx_continuous -infile file.wav 2> pocketsphinx.log > myspeech.txt
##########################


