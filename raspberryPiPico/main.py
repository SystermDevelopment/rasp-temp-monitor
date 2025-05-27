import network
import socket
import json
import time
import machine
from machine import Pin, I2C
import bme280
import config  # Wi-Fi設定を別ファイルで管理

# Wi-Fi接続設定
ssid = config.SSID
password = config.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print('Wi-Fi接続中...')
    time.sleep(5)
print('接続完了:', wlan.ifconfig())

# センサー初期化
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
sensor = bme280.BME280(i2c=i2c, address=0x76)

# ソケット初期化
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(1)
print('Pico WHサーバー起動中:', addr)

# Wi-Fi再接続関数
def reconnect_wifi():
    if not wlan.isconnected():
        print('Wi-Fi再接続中...')
        wlan.disconnect()
        wlan.connect(ssid, password)
        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print('Wi-Fi再接続成功:', wlan.ifconfig())
        else:
            print('Wi-Fi再接続失敗')

# メインループ
last_wifi_check = time.time()

while True:
    current_time = time.time()

    # 5分ごとのWi-Fiチェック
    if current_time - last_wifi_check > 300:
        reconnect_wifi()
        last_wifi_check = current_time

    cl = None
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

    except OSError as e:
        if e.args[0] != 110:
            print('予期せぬエラー:', e)
            machine.reset()

    finally:
        if cl:
            cl.close()

    time.sleep(0.5)

