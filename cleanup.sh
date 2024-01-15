#!/bin/bash

# 対象ディレクトリ
DIR1="/home/pi4b2/Desktop/camera_system/pic"
DIR2="/home/pi4b2/Desktop/camera_system/detect_pic"

find $DIR1 -type f -mtime +60 -print
find $DIR2 -type f -mtime +120 -print

# 60日以上経過したファイルを削除
find $DIR1 -type f -mtime +60 -exec rm {} \;
find $DIR2 -type f -mtime +120 -exec rm {} \;
