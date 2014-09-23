#!/bin/bEEEEEsh
# Unofficial patch for CVE-2014-4377 applicable only to iPhone4  (iPhone 3,1) 
# Jailbroken (tested with Pangu 1.1.0) with firmware version 7.1.2 
# Please dont use this! SERIOUSLY DON'T! 
# 56647db26e03d954fa2c428b289db3c7  dyld_shared_cache_armv7.ORIGINAL
# dc28e09b4f146934909aafd57dfcc962 dyld_shared_cache_armv7.PATCHED


# First copy the patcher (is this shellscript)
# scp patch.sh root@192.168.1.101:

# Then log into your iphone4
# ssh root@192.168.1.101

# Run the shellscript
# iphone:~ root# . ./patch.sh 
#  48+0 records in
#  48+0 records out
#  Applying patch
#  1+0 records in
#  1+0 records out
#  done.

#Now you need to reboot for the patch to loaded up
# iphone:~ root# reboot


TEMPFILE1=`mktemp`
TEMPFILE2=`mktemp`
dd if=/System/Library/Caches/com.apple.dyld/dyld_shared_cache_armv7 skip=22458724 count=48 bs=1 of=$TEMPFILE1 status=noxfer 
printf "\xFF\x3F\x40\xF3\x4E\x81\x2E\xAA\x20\x46\x03\x21\x26\xF0\x86\xFC\x01\x28\x40\xf0\x4c\x81\x2e\x98\x30\xa9\xdd\xf8\xb0\x80\xd0\xf7\x43\xFa\x04\x46\x00\x26\x00\x2c\x00\xf0\x87\x82\x30\x98\x00\x28" > $TEMPFILE2

if `cmp -s $TEMPFILE1 $TEMPFILE2`; 
then
    echo Applying patch
    printf '\x91' | dd of=/System/Library/Caches/com.apple.dyld/dyld_shared_cache_armv7 bs=1 seek=22458740 count=1 conv=notrunc status=noxfer 
    echo done.
else
    echo Patch not applicable, sorry.
fi
rm -f $TEMPFILE1 $TEMPFILE2

