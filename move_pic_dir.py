import os
import glob
import shutil
import argparse

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description='ファイルを日付ごとのサブディレクトリに移動します。')
parser.add_argument('dir', help='ファイルが格納されているディレクトリのパス')
args = parser.parse_args()

# 指定されたディレクトリのJPGファイルを取得
jpg_files = glob.glob(os.path.join(args.dir, '*.jpg'))

for file in jpg_files:
    # ファイル名から日付を抽出 *_yyyymmdd_*の場合
    date_str = os.path.basename(file).split('_')[1]

    # サブディレクトリのパスを作成
    subdir = os.path.join(args.dir, date_str)

    # サブディレクトリが存在しない場合は作成
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    # ファイルをサブディレクトリに移動
    shutil.move(file, os.path.join(subdir, os.path.basename(file)))
