#!/usr/bin/env python3

import platform, subprocess, json

def getlinuxdisks():

	result = subprocess.run(
		["lsblk", "-J", "-d", "-o", "NAME,SIZE,MODEL,TRAN"],
		capture_output=True,
		text=True,
	)
	
	data = json.loads(result.stdout)

	usbdisks = []

	for disk in data["blockdevices"]:

		if disk.get("tran") == "usb":

			usbdisks.append(disk)

	return usbdisks

def getwindowsdisks():

	result = subprocess.run(
    		[
        		"powershell",
        		"-Command",
        		"Get-Disk | Select-Object Number,FriendlyName,Size,BusType | ConvertTo-Json"
    		],
    		capture_output=True,
    		text=True
	)

	data = json.loads(result.stdout)
	
	return data

osname = platform.system()

if osname == "Linux":
	
	for disk in getlinuxdisks():
	        print(
			f"/dev/{disk['name']} - ",
			f"{disk['size']} - ",
			f"{disk.get('model', 'Unknown')}"
		)
	while True:

		disk = input("Please enter the USB disk (example: /dev/sdc")
		
		if disk:
			continue

		confirm = input("WARNING: This will erase everything on $disk. Type YES to continue: ")
		
		if confirm == "YES":
			continue
		break
			

elif osname == "Windows":

	for disk in getwindowsdisks():

		if disk["BusType"] == "USB":

			print(
				f"Disk {disk['Number']} - "
				f"{disk['FriendlyName']} - "
				f"{disk['BusType']}"
			)

else:
	raise Exception("Unsupported OS")
