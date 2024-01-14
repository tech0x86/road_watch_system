# road_watch_system
Raspi4とカメラモジュール(中華製)で道路を監視するシステム

## 要インストール
sudo apt-get install python3-opencv

## 定期起動設定　crontab -e
*/10 * * * * /usr/bin/python3 /home/pi4b2/Desktop/camera_system/main.py

main.py: hh:m0分　10分ごと起動
画像の取得と物体判定、画像の保存

create_movie.py 0:03 毎日1回
物体判定した画像から1日のタイムラプス動画を生成

## Raspi4b　OS Ver
cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"



