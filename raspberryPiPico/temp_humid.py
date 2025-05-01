from machine import Pin, I2C
import bme280
import time

# I2C設定（GPIOピン設定）
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# I2Cアドレスを0x76に固定
sensor = bme280.BME280(i2c=i2c, address=0x76)

while True:
    try:
        temperature, pressure, humidity = sensor.values
        print('温度:', temperature)
        print('湿度:', humidity)
        print('気圧:', pressure)
        print('-------------------')
    except OSError as e:
        print("通信エラーが発生しました。再試行します...", e)

    time.sleep(2)
