#!/bin/bash

lsblk -d -o NAME,SIZE,MODEL,TRAN | grep usb # lists only usb disks, -d omits slaves or holders, -o outputs in columns

while true; do # asks for name of disk and warns that the script will erase everything

	read -e -i "$disk" -p "Enter the USB disk (example: /dev/sdc): " disk

	if [ -z $disk ] || [ ! -b $disk ]; then

		echo "Invalid disk."
		continue
	fi
	
	read -p "WARNING: This will erase everything on $disk. Type YES to continue: " confirm

	if [ -z $confirm ] || [ $confirm != "YES" ]; then
        	continue
	fi

	break
done

sudo umount $disk* 2>/dev/null # unmounts selected disk to prevent corruption

while true; do # asks for path to recovery file

	read -e -i "$path" -p "Enter the folder path containing the .bin file: " path	

	if [ -z $path ] || [ ! -e $path ]; then

		echo "Enter a valid path."
		continue
	else
		cd $path
		break
	fi
done

while true; do # asks for the name of the bin file

	read -e -i "$file" -p "Enter the .bin file name: " file

	if [ -z $file ] || [ ! -f $file ]; then

		echo "Enter a valid .bin."
		continue
	else
		echo "creating image..."
		break
	fi
done

sudo dd if=$file of=$disk bs=4M status=progress conv=fsync # pulls user provided information and writes to usb
echo "Your recovery USB is ready."

