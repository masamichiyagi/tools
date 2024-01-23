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
# Script
##########################
# perl
sudo apt-get install perl -y
# python-pip
sudo apt-get install python-pip -y
sudo apt-get install python3-pip -y

##########################
# Utility
##########################
# imagemagick convert
sudo apt-get install imagemagick -y

##########################
# PDF editor
##########################
## pdfs to pdf
sudo apt-get install ghostscript -y
## pdftotext, etc.
sudo apt-get install poppler-utils -y

##########################
# Video and audio editor
##########################
## youtube-dl
pip install youtube-dl
pip install -U yt-dlp
## ffmpeg
sudo apt-get install ffmpeg -y
### If you are unable to install ffmpeg,
### you install ffmpeg from a non-PPT public repository.
### -E option is proxy.
#sudo -E add-apt-repository ppa:mc3man/trusty-media
#sudo apt-get update
#sudo apt-get install ffmpeg


##########################
# Text editor
##########################
# markdown
sudo apt install npm nodejs-legacy fonts-ipafont-gothic
sudo npm -g install markdown-pdf
# usage
# markdown-pdf document.md

