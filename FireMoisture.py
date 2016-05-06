import botbook_mcp3002 as mcp
import datetime
import time
import sys
from twython import Twython
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

execfile("azm_keys.py") # execute file containing AzmRpi twitter app secret passwords
api = Twython(C_KEY,C_SECRET,A_TOKEN,A_SECRET)

Pump = 40 # pump pin
FlameValue = 0

GPIO.setup(Pump, GPIO.OUT) # set pump pin as an output pin

FlameValue = mcp.readAnalog(0,1) # read flame sensor value

DT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get date and time

TweetStatus = 'Fire detected at TAL001, ' + str(DT) # twitter status sentence including date time

while True:
    
    DT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get date and time
    
    TweetStatus = 'Fire detected at TAL001, ' + str(DT) # twitter status sentence including date time
    
    MoistureValue = mcp.readAnalog(0,0) # read moisture sensor value
    FlameValue = mcp.readAnalog(0,1) # read flame sensor value
    
    print "Moisture = ", MoistureValue
    print "Flame = ", FlameValue

    if(FlameValue > 500): # if flame sensor value is high, there is fire so tweet fire alarm status
        api.update_status(status=TweetStatus) #update tweet using TweetStatus sentence
        print "Flame", TweetStatus
        time.sleep(1)
    
    if(MoistureValue <= 200):
        GPIO.output(Pump,GPIO.HIGH)
        print "Pump ON"
        time.sleep(0.5)
        GPIO.output(Pump,GPIO.LOW)
        print "Pump Off"
        time.sleep(0.2)
    elif(MoistureValue > 200):
        GPIO.output(Pump,GPIO.LOW)
    
    time.sleep( 0.5)
