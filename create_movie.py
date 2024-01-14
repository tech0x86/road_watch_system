import cv2
import glob
import os
from datetime import datetime, timedelta

def create_timelapse(date, base_input_dir, output_dir):
    input_dir = os.path.join(base_input_dir, date)  # 日付ディレクトリを追加
    images = sorted(glob.glob(f'{input_dir}/detect_{date}_*.jpg'), key=lambda x: os.path.basename(x))

    if not images:
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    size = (width, height)

    out = cv2.VideoWriter(f'{output_dir}/timelapse_{date}.mp4', cv2.VideoWriter_fourcc(*'avc1'), 5, size)

    for filename in images:
        img = cv2.imread(filename)

        # ファイル名を抽出し、テキストとして追加
        text = os.path.basename(filename)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5  # フォントサイズを小さくする
        font_color = (255, 255, 255)
        line_type = 1

        # テキストのサイズを取得
        text_size = cv2.getTextSize(text, font, font_scale, line_type)[0]

        # テキストの位置を動的に設定
        text_position = (width - text_size[0] - 10, 20) # 画像の右下に位置するように調整

        cv2.putText(img, text, text_position, font, font_scale, font_color, line_type)

        out.write(img)

    out.release()

base_dir = os.path.dirname(os.path.abspath(__file__))
base_input_dir = os.path.join(base_dir, 'detect_pic')  # ベースの入力ディレクトリ
output_dir = os.path.join(base_dir, 'movie')

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime('%Y%m%d')
#date_str = '20240107'
create_timelapse(date_str, base_input_dir, output_dir)  # 関数呼び出し時の引数を変更



