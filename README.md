# rasp-temp-monitor

Raspberry Pi Picoを使用した温湿度モニタープロジェクトです。このプロジェクトは、BME280センサーを使用して温度、湿度、気圧のデータを取得し、Wi-Fi経由でデータを提供します。

## プロジェクトファイル

- **bme280.py**: BME280センサーを操作するためのクラス`BME280`を定義しています。センサーから温度、湿度、気圧のデータを取得し、補正された値を返すメソッドを含んでいます。

- **check_ip.py**: Wi-Fi接続を管理するスクリプトです。指定されたSSIDとパスワードを使用してWi-Fiに接続し、接続が完了するまで待機します。

- **config.py**: Wi-FiのSSIDとパスワードが定義されています。他のスクリプトから設定を簡単に管理できます。

- **main.py**: プロジェクトのエントリーポイントです。Wi-Fi接続を確立し、BME280センサーを初期化し、HTTPサーバーを起動してセンサーのデータを提供します。

- **temp_humid.py**: BME280センサーから温度と湿度のデータを取得し、定期的に表示するスクリプトです。

## 使用方法

1. `config.py`ファイルを開き、Wi-FiのSSIDとパスワードを設定します。
2. `main.py`を実行して、Wi-Fiに接続し、センサーを初期化します。
3. HTTPサーバーが起動し、センサーのデータを取得できるようになります。

## 必要な設定

- Raspberry Pi Pico
- BME280センサー
- MicroPythonがインストールされた環境

このプロジェクトを使用して、オフィスや自宅の温湿度をモニタリングし、データをリアルタイムで取得することができます。

## ライセンス情報

本プロジェクトで使用している`bme280.py`は、[robert-hh/BME280](https://github.com/robert-hh/BME280) のリポジトリにあるコード（MITライセンス）を利用しています。

```
Copyright (c) 2016-2020 Robert Hammelrath  
Released under the MIT license  
https://opensource.org/licenses/MIT
```
