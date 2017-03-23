#!/bin/sh

if [ -z "$1" ]; then
    echo "Missing image file"
    exit 1
elif [ -z "$2" ]; then
    echo "Missing wireless config file"
    exit 1
fi

IMG_FILE=$1
WPA_CONFIG=$2

SECTOR_OFFSET=$(sudo /sbin/fdisk -l $IMG_FILE | awk '$7 == "W95" { print $2 }')
BYTE_OFFSET=$(expr 512 \* $SECTOR_OFFSET)

IMG_DIR=$(basename "$IMG_FILE")
IMG_DIR="${IMG_DIR%.*}"

echo Mounting at /mnt/$IMG_DIR

sudo mkdir -p /mnt/$IMG_DIR
sudo mount -o loop,offset=$BYTE_OFFSET $IMG_FILE /mnt/$IMG_DIR

echo Enabling SSH
sudo touch /mnt/$IMG_DIR/ssh

echo Copying WPA config
sudo cp -f $2 /mnt/$IMG_DIR/wpa_supplicant.conf

echo Unmounting
sudo umount /mnt/$IMG_DIR
