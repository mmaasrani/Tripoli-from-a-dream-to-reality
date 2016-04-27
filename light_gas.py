#Raspberry Pi Potentiometer Circuit Code
import RPi.GPIO as GPIO
import botbook_mcp3002 as mcp
import time

LED = 40
lightvalue = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

    
while True:
    lightvalue = mcp.readAnalog(0,0)
    gasValue = mcp.readAnalog(0,1)
    print "LightValue = ", lightvalue, "CO Gas Value= ", gasValue
    time.sleep( 0.2)
    if (lightvalue <=700):
        GPIO.output(LED, GPIO.HIGH)
    elif (lightvalue >700):
        GPIO.output(LED, GPIO.LOW)
