# road_watch_system
Raspi4とカメラモジュール(中華製)で道路を監視するシステム

## 要インストール
sudo apt-get install python3-opencv

## 定期起動設定　crontab -e
*/10 * * * * /usr/bin/python3 /home/pi4b2/Desktop/camera_system/main.py

## Raspi4b　OS Ver
cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
