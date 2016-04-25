
import sys
from twython import Twython
import RPi.GPIO as GPIO
import time


TRIG =16 
ECHO =18 
LED = 22

dist2 = 15
dist1 = 20
dist0 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

t0 = 0
delay = 3


tweetStr = "Double parking Fault!!"

execfile("azm_keys.py")
api = Twython(C_KEY,C_SECRET,A_TOKEN,A_SECRET)

while True:
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


    print int(distance),"cm"        
        
    
    if (distance < dist2):
        time.sleep(1)
        delay = delay - 1
        print delay
        if (delay == 0):
            GPIO.output(LED, GPIO.HIGH)
            #api.update_status(status=tweetStr)
            print "status updated"
            
    if (distance > dist2):
        delay = 5
        GPIO.output(LED, GPIO.LOW)
        
    if (int(distance) >= dist0):
        print "no car!"
    if (int(distance) <= dist1 and int (distance) > dist2):
        print "1 car!"
    
GPIO.cleanup()
    
