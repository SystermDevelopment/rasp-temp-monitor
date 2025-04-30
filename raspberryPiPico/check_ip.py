import urequests
import network
import time

# Wi-Fi接続
ssid = config.SSID
password = config.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print('Wi-Fi接続中...')
    time.sleep(1)

print('接続完了:', wlan.ifconfig())



