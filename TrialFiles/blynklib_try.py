import machine,time
import secrets
import network, rp2
import urequests

led = machine.Pin('LED', machine.Pin.OUT)

rp2.country('UK')
ssid = secrets.SSID
password = secrets.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() and wlan.status() >= 0:
 print("Waiting to connect:")
 time.sleep(1)

print(wlan.ifconfig())

#while True:
#    r = urequests.get("https://api.bitpanda.com/v1/ticker")
#    print(r.content)
#    r.close()
#    time.sleep(1)

import BlynkLib
BLYNK_AUTH = secrets.BLYNK_AUTH_TOKEN
blynk = BlynkLib.Blynk(BLYNK_AUTH,
                       insecure=True,          # disable SSL/TLS
                       server='blynk.cloud',   # set server address
                       port=80,                # set server port
                       heartbeat=30,           # set heartbeat to 30 secs
                       log=print               # use print function for debug logging
                       )

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

@blynk.on("V*")
def blynk_handle_vpins(pin, value):
    print("V{} value: {}".format(pin, value))
    if value == ['1']:
        led.on()
    else:
        led.off()

while True:
    blynk.run()


#accessPoints = wlan.scan()
#for ap in accessPoints: #this loop prints each AP found in a single row on shell
#    print(ap)
