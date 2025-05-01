import network
import socket
import json
import time
from machine import Pin, I2C
import bme280
import config  # Wi-Fi設定を別ファイルで管理

# Wi-Fi接続
ssid = config.SSID
password = config.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print('Wi-Fi接続中...')
    time.sleep(10)
print('接続完了:', wlan.ifconfig())

# センサー準備
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
sensor = bme280.BME280(i2c=i2c, address=0x76)

# Webサーバー起動
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(1)
print('Pico WHサーバー起動中', addr)

while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)

        temperature, pressure, humidity = sensor.values
        response_data = json.dumps({
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure
        })

        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
        cl.send(response_data)
        cl.close()

    except OSError as e:
        if e.args[0] == 110:  # ETIMEDOUTの場合は無視する
            pass
        else:
            print('予期せぬエラー:', e)

    # 負荷軽減のスリープ
    time.sleep(0.5)


