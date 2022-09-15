from machine import Pin
import utime as time
import secrets
import network, rp2
import urequests as requests

def send_notification(notification_text):
    request_headers = {'Content-Type': 'application/json'}
    payload = { 'value1':notification_text}
    ifttt_url = "https://maker.ifttt.com/trigger/thirsty_plant/with/key/"+secrets.IFTTT_KEY
    request = requests.post(ifttt_url, json=payload, headers=request_headers)
    request.close()
    
def save_data():
    request_headers = {'Content-Type': 'application/json'}
    payload = { 'value1':status,'value2':notification_text }
    ifttt_url = "https://maker.ifttt.com/trigger/thristy_plant_data/with/key/"+secrets.IFTTT_KEY
    request = requests.post(ifttt_url, json=payload, headers=request_headers)
    request.close()

def pump_on():
    green_led.on()
    pump1a.high()
    pump1b.low()

def pump_off():
    green_led.off()
    pump1a.low()
    pump1b.low()

def add_water():
    pump_on()
    time.sleep(5)
    pump_off()
    
led = Pin('LED', Pin.OUT)
pump1a = Pin(14, Pin.OUT)
pump1b = Pin(15, Pin.OUT)

rp2.country('UK')
ssid = secrets.SSID
password = secrets.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() and wlan.status() >= 0:
 print("Waiting to connect:")
 time.sleep(1)

#print(wlan.ifconfig())
#send_notification("Thirsty Plant's wlan connected.")

green_led = Pin('LED', Pin.OUT)
sensor = Pin(17, Pin.IN, Pin.PULL_DOWN)
sensor_power = Pin(16, Pin.OUT)

status='moist'

while True:
    time.sleep(60)
    sensor_power.on()
    sensor_value=sensor.value()
    time.sleep(0.01)
    sensor_power.off()
    if sensor_value == 1:
        if status == 'moist':
            notification_text = "Your plant is thirsty."
            status = "dry"
        else:
            notification_text = "We watered again as the plant was still thirsty."
    else:
        if status == "dry":
            notification_text = "Awesome, the plant has enough water again!"
            status= "moist"
        else:
            notification_text = ""
            pass
    save_data()
    if status == 'dry':
        add_water()
    send_notification(notification_text)
    time.sleep(3600)
