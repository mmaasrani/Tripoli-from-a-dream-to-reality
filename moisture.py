#Raspberry Pi Potentiometer Circuit Code
import RPi.GPIO as GPIO
import botbook_mcp3002 as mcp
import time

LED = 40
lightvalue = 0

minMoisture = 200

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

    
while True:
    moisturevalue = mcp.readAnalog(0,1)
    print "Moisture = ", moisturevalue
    time.sleep( 0.2)
    if (moisturevalue <= minMoisture):
        GPIO.output(LED, GPIO.HIGH)
    elif (moisturevalue > minMoisture):
        GPIO.output(LED, GPIO.LOW)
