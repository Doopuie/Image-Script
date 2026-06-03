#!/usr/bin/env python3

import platform, subprocess, json

def getlinuxdisks():

	result = subprocess.run(
		["lsblk", "-J", "-d", "-o", "NAME,SIZE,MODEL,TRAN"],
		capture_output=True,
		text=True,
		check=True
	)
	
	data = json.loads(result.stdout)

	usbdisks = []

	for disk in data["blockdevices"]:
		if disk.get("tran") == "usb":
			usbdisks.append(disk)

	return usbdisks

def getwindowsdisks():
	
	pass

def getmacdisks():

	pass

osname=platform.system()

if osname == "Linux":
	
	for disk in getlinuxdisks():
	        print(f"/dev/{disk['name']} - {disk['size']} - {disk.get('model', 'Unknown')}")

elif osname == "Windows":

	disks = getwindowsdisks()
	pass

elif osname == "Darwin":

	disks = getmacdisks()
	pass

else:
	raise Exception("Unsupported OS")
