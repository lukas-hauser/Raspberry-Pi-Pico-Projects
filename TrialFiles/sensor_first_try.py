from machine import Pin
import time
import utime
 
green_led = machine.Pin('LED', machine.Pin.OUT)
sensor = Pin(17, Pin.IN, Pin.PULL_DOWN)
 
i=0
while True:
    utime.sleep(1)
    dateTime = time.localtime()
    hour = dateTime[3]
    minute = dateTime[4]
    second = dateTime[6]
    if hour == 22 and dateTime[4] < 19:
        if sensor.value():
            i+=1
            print(i)
            print("pump_on()")
        else:
            print("pump_off()")
    elif hour == 22 and minute == 19 and i != 0:
        print("Today, we watered for ", i," seconds")
        i=0
