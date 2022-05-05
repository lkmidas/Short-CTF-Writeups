#!/bin/sh
gcc -pthread -o exploit -static $1
mv ./exploit ./rootfs
cd ./rootfs
find . | cpio -o --format=newc > ../rootfs.cpio
