#!/usr/bin/env bash

SUMI_DIR=$HOME/.sumi
SUMI_UDOCKER_DIR=$SUMI_DIR/udocker
UDOCKER_DIR=$HOME/.udocker
TMP_DIR=$HOME/.tmp

UDOCKER_TARBALL=$HOME/udocker-1.1.1.tar.gz
IMAS_IMAGE=$HOME/imas-installer-20180529181447.tar.xz

if [ -f "$SUMI_UDOCKER_DIR/udocker.py" ]
then
    >&2 echo "It looks like uDocker is already installed."
    >&2 echo "Run the following commands if you want to remove uDocker"
    >&2 echo rm -r $UDOCKER_DIR
    >&2 echo rm -r $SUMI_UDOCKER_DIR
    exit
fi

if [ ! -d "$SUMI_UDOCKER_DIR" ]
then
    mkdir -p $SUMI_UDOCKER_DIR
fi

cd $SUMI_UDOCKER_DIR

curl -O https://raw.githubusercontent.com/indigo-dc/udocker/devel/udocker.py
chmod +x udocker.py

#Check
$SUMI_UDOCKER_DIR/udocker.py version

#Creat udocker dir to be linked
mkdir $SUMI_UDOCKER_DIR/dot-udocker

if [ -d "$UDOCKER_DIR" ]
then
    >&2 echo Cannot continue. $UDOCKER_DIR already exists. 
    >&2 echo Please remove the directory and run the script again
    exit
fi

#Create configuration
ln -s $SUMI_UDOCKER_DIR/dot-udocker $UDOCKER_DIR
mkdir $TMP_DIR
echo "tmpdir='$TMP_DIR'" > ~/.udocker/udocker.conf
echo "UDOCKER_TARBALL='$UDOCKER_TARBALL'" >> ~/.udocker/udocker.conf

cd ~

#Load image
$SUMI_UDOCKER_DIR/udocker.py load -i $IMAS_IMAGE
$SUMI_UDOCKER_DIR/udocker.py create --name=imas imas-installer:20180529181447
