#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import RPi.GPIO as GPIO
import time
import os
import dropbox
import sys
import requests
import smbus2


# trigger_pin = 23
# echo_pin = 24

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(trigger_pin, GPIO.OUT)
# GPIO.setup(echo_pin, GPIO.IN)


dbx = dropbox.Dropbox('8v5hwjJC9gAAAAAAAAAAjUBwI0c6uuV1voodtcgSpGbiYnAR9XsZovlZOXsZ4uB_')
work_path = "/root/"
txt = ""
flate = False

sys.modules['smbus'] = smbus2
from RPLCD.i2c import CharLCD

ADDRESS = 0x27

# def send_trigger_pulse():
# GPIO.output(trigger_pin, True)
# time.sleep(0.001)
# GPIO.output(trigger_pin, False)

# def wait_for_echo(value, timeout):
# count = timeout
# while GPIO.input(echo_pin) != value and count > 0:
# count = count - 1

# def get_distance():
# send_trigger_pulse()
# wait_for_echo(True, 5000)
# start = time.time()
# wait_for_echo(False, 5000)
# finish = time.time()
# pulse_len = finish - start
# distance_cm = (pulse_len * 340 *100) /2
# print("%.1f" % distance_cm)
# if(30<=distance_cm<=40):
# print("%.1f" % distance_cm)
# os.system('fswebcam -r 640x480 -p YUYV -S 10 -d /dev/video0 --no-banner plate.jpg')


def microsoft_ocr():
	#subscription_key = "c9183d61764a4c2c85d46c85dd8d0d22"    #old
	subscription_key = "ea24897a38464a2baa32799b5c7aa315"   #new
	assert subscription_key
	vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
	text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"
	image_url = "/root/plate.jpg"
	image_data = open(image_url, "rb").read()
	headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
				  'Content-Type': 'application/octet-stream'}
	params  = {'language': 'en', 'detectOrientation': 'true'}
	response = requests.post(text_recognition_url, headers=headers, params=params, data=image_data)
	response.raise_for_status()

	operation_url = response.headers["Operation-Location"]

	analysis = {}
	poll = True
	while (poll):
		response_final = requests.get(
			response.headers["Operation-Location"], headers=headers)
		analysis = response_final.json()
		if ("recognitionResults" in analysis):
			poll= False 
		if ("status" in analysis and analysis['status'] == 'Failed'):
			poll= False

	polygons=[]
	if ("recognitionResults" in analysis):
		polygons = [(line["text"])
			for line in analysis["recognitionResults"][0]["lines"]]	
	for polygon in polygons:
		if 7<= len(polygon) <=9:
			text = polygon 
			#text  = polygon[1]
			with open("/root/plate.txt",'a') as f:
				print(text,file=f)
			break


def get_plate():
	for file in os.listdir(work_path):
		if "plate.jpg" in file:
			global flate
			flate = True
			microsoft_ocr()
			os.system("grep  '[0-9]' plate.txt > result.txt")
			os.system("sed 's/[ \t]*$//g' -i result.txt")
			os.system("sed -i 's/[ ()$_-.^]//g'  result.txt")
			fp = open("result.txt")
			global txt
			try:
				txt = fp.read().splitlines()[0]
			except:
				flate = False
				os.system("cat /dev/null > result.txt")
				txt = ""
				print("License Plate not found!")
			if txt.strip() != "":
				txt_jpg = txt + ".jpg"
				os.rename("plate.jpg", txt_jpg)
			else:
				os.system("rm -f plate.jpg")
				os.system("rm -f .jpg")
			fp.close()


def lcd_display():
	global flate
	if flate:
		lcd = CharLCD('PCF8574', address=ADDRESS, port=1, backlight_enabled=True)
		lcd.clear()
		lcd.cursor_pos = (0, 5)
		lcd.write_string("Welcome!")
		lcd.cursor_pos = (1, 5)
		global txt
		lcd.write_string(txt)
		flate = False
		os.system("cat /dev/null > plate.txt")
	else:
		lcd = CharLCD('PCF8574', address=ADDRESS, port=1, backlight_enabled=False)
		os.system("cat /dev/null > plate.txt")


def camera():
	os.system('fswebcam -r 640x480 -p YUYV -S 10 -d /dev/video0 --no-banner plate.jpg')
	lcd = CharLCD('PCF8574', address=ADDRESS, port=1, backlight_enabled=False)


def jpg_upload_db():
    for files in os.listdir(work_path):
        if ".jpg" in files:
            jpg = files
            with open(work_path + files, 'rb') as f:
                dbx.files_upload(f.read(), "/pictures_jpg/" + jpg,
                                 mode=dropbox.files.WriteMode("overwrite"))
    os.system('mv *.jpg /mnt/ 2>/dev/null')


while True:
    # get_distance()
    camera()
    get_plate()
    lcd_display()
    jpg_upload_db()
    time.sleep(2)
