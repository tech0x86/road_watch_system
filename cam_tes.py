import subprocess
from datetime import datetime

# 現在のタイムスタンプを取得
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 画像のファイル名を設定（ISO準拠のタイムスタンプ形式）
filename = f"{timestamp}.jpg"

# libcamera-stillコマンドを使用してHD画質（1280x720）で画像を撮影
#subprocess.run(["libcamera-still", "-o", filename, "-w", "1280", "-h", "720"])
# libcamera-stillコマンドを使用してHD画質（1280x720）で画像を撮影し保存
subprocess.run(["libcamera-still","--nopreview", "-o", filename, "--width", "1280", "--height", "720"])

print(f"画像が保存されました: {filename}")

