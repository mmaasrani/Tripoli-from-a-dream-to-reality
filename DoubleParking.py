import sys
from twython import Twython # twitter app library on python
import RPi.GPIO as GPIO # to use GPIO pins on raspberry & python
import datetime # to get date and time from raspberry pi
import time # delay sleep 
import os
import botbook_mcp3002 as mcp # analog input library

TRIG =16 # define ultrasonic pins for easy pins replacement
ECHO =18

light = 38 # street lights pin

dist3 = 10 # traffic distance in cm
dist2 = 15 # double parking distance in cm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # board numbering 

GPIO.setup(TRIG, GPIO.OUT) # set pin as output or input
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(light, GPIO.OUT)

nodeID = " Tal001 ";

delayDB = 5 #double parking threshold time
delayTR = 8 # traffic threshold time

captime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #capture time, get date and time when picture have been token

tweetStr = "Double parking at ", nodeID + captime # sentence contatining node id and capture time

execfile("azm_keys.py") # twitter app passwords contains C_KEY,C_SECRET,A_TOKEN,A_SECRET

api = Twython(C_KEY,C_SECRET,A_TOKEN,A_SECRET) # set twitter app passwords 

while True:
    lightval = mcp.readAnalog() # read light sensor
    
    captime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    tweetStr = ("Double parking at ", nodeID + captime) 

    GPIO.output(TRIG, False)
    time.sleep(0.3)
    GPIO.output(TRIG, True)
    time.sleep(0.001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        signalOff = time.time()
    while GPIO.input(ECHO)==1:
        signalOn = time.time()
    
    timePassed=signalOn - signalOff
    distance=timePassed*17150

    print "distance = ", int(distance) # casting to convert from float (comma) to integer number     
    print "light = ", lightval
    
    if (distance < dist2 and distance > dist3): # if double parking exist
        time.sleep(1)
        delayDB = delayDB - 1 
        print delayDB
        if (delayDB == 0):
            os.system('fswebcam -r 1280x720 /home/pi/%captime.jpg') # camera capture command for database with date and time title         
            os.system('fswebcam -r 1280x720 /home/pi/image.jpg') # camera capture command for twitter image
            print "Double parking Car capture",tweetStr
            photo = open('/home/pi/image.jpg', 'rb') # select captured image directory in pi files
            response = api.upload_media(media=photo)
            api.update_status(status='Double parking Detection Region Tal001', media_ids=[response['media_id']])# tweet image with title
            print "status updated"
            
            
    if (distance > dist2): # if not double parking then reset timer delayDB
        delayDB = 5
    
    if (distance < dist3): # if traffic detected as car is too close to sensor 
        time.sleep(1)
        delayTR = delayTR - 1
        print delayTR
        if (delayTR == 0):
            print "Traffic at ", nodeID
            os.system('fswebcam -r 1280x720 /home/pi/image2.jpg')
            photo = open('/home/pi/image2.jpg', 'rb')
            response = api.upload_media(media=photo)
            api.update_status(status='Traffic at Region Tal001', media_ids=[response['media_id']])

    if (distance > dist3):# if no traffic detected, reset traffic timer delayTR
        delayTR = 8
        
    if (lightval < 600): # if ambient light is low then turn on LED lights automatically
        GPIO.output(light, GPIO.HIGH)
    elif (lightval > 600): # if ther is enough ambient light then turn off LED lights
        GPIO.output(light, GPIO.LOW)
        
GPIO.cleanup()
