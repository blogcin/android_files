#!/usr/bin/env python3
#
# Copyright (c) 2017 Song Hyeon Sik (blogcin@naver.com)
#
import subprocess

def runProcess(exe):    
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
      retcode = p.poll() #returns None while subprocess is running
      line = p.stdout.readline()
      yield line
      if(retcode is not None):
        break

def is_device_found():
	result = runProcess("adb devices".split())

	adb_title = next(result)
	device_name = next(result).decode("utf-8")
	if device_name != "\n":
		return True
	else:
		return False

def is_adb_found():
	try:
		result = runProcess("adb devices".split())
		adb_title = next(result)
	except FileNotFoundError:
		return False
	
	return True

def get_files():
#adb shell "sh -c 'echo aa'"
	result = runProcess(["adb", "shell", "sh -c 'find /system'"])
	
	files = ""
	
	for line_byte in result:
		line = line_byte.decode("utf-8")
		if "Permission denied" in line:
			files += line.split(' ')[1][:len(line)-1]
		else:
			files += line
			
	return files
	
if not is_device_found():
	print("android device is not found")

if not is_adb_found():
	print("adb is not found")

print(get_files(), end="", flush=True)
