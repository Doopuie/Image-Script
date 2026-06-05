#!/usr/bin/env python3

from pathlib import Path
import platform, subprocess, json

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
	
	script_dir = Path(__file__).resolve().parent
	shell_script = script_dir / "is.txt"

	subprocess.run([str(shell_script)])

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
