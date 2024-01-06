import cv2
import csv
import numpy as np
from collections import Counter
import os
import subprocess
from datetime import datetime

# 現在のタイムスタンプを取得
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
date_only = timestamp[:8]
# 画像のファイル名を設定
filename = f"{timestamp}.jpg"
csv_filename=f"{date_only}.csv"
# オブジェクト一覧
objects_list = ['bicycle', 'car', 'motorbike', 'bus', 'truck', 'person', 'bird', 'cat', 'dog', 'umbrella', 'suitcase']

base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, 'pic/', filename)
csv_path = os.path.join(base_path, 'csv/', csv_filename)
detect_image_path = os.path.join(base_path, 'detect_pic/','detect_'+filename)
subprocess.run(["libcamera-still", "--nopreview", "-o", image_path, "--width", "2592", "--height", "1944"])

# パスの設定
config_path = os.path.join(base_path, 'yolov4-tiny.cfg')
weights_path = os.path.join(base_path, 'yolov4-tiny.weights')
labels_path = os.path.join(base_path, 'coco.names')

# 表示画像の最大1辺長
max_size = 800

def load_labels(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def load_network(config_path, weights_path):
    return cv2.dnn.readNetFromDarknet(config_path, weights_path)

def get_output_layers(net):
    layer_names = net.getLayerNames()
    return [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

def detect_objects(net, image, output_layers):
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    return net.forward(output_layers)

def draw_predictions(image, detections, labels, original_width, original_height, scale_width, scale_height):
    H, W = image.shape[:2]
    boxes = []
    confidences = []
    class_ids = []
    detected_labels = []

    for detection in detections:
        for output in detection:
            scores = output[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.1:
                # 元の画像サイズに基づくバウンディングボックスの座標
                box = output[:4] * np.array([original_width, original_height, original_width, original_height])
                centerX, centerY, width, height = box.astype('int')

                # リサイズされた画像に合わせて座標をスケーリング
                centerX = int(centerX * scale_width)
                centerY = int(centerY * scale_height)
                width = int(width * scale_width)
                height = int(height * scale_height)
                x, y = int(centerX - width / 2), int(centerY - height / 2)

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.1, nms_threshold=0.1)

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            color = [int(c) for c in np.random.randint(0, 255, size=(3,))]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(labels[class_ids[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            detected_labels.append(labels[class_ids[i]])
    # 画像を保存する
    cv2.imwrite(detect_image_path, image)

    return Counter(detected_labels)

def resize_image(image, max_size):
    h, w = image.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_image = cv2.resize(image, (new_w, new_h))
        return resized_image, scale
    return image, 1

def update_csv(label_counts, csv_path, objects_list):
    # "other"のカウント用
    other_count = 0

    # データを整理
    data = {'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")}
    for label in objects_list:
        data[label] = label_counts.get(label, 0)
    for label, count in label_counts.items():
        if label not in objects_list:
            other_count += count
    data['other'] = other_count

    # CSVファイルへの書き込み
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp'] + objects_list + ['other'])
        if not file_exists:
            writer.writeheader()  # ヘッダーの書き込み
        writer.writerow(data)


# ニューラルネットワークモデルとラベルのロード
net = load_network(config_path, weights_path)
labels = load_labels(labels_path)
output_layers = get_output_layers(net)

# 実行部分
original_image = cv2.imread(image_path)

# 元の画像で物体検出を実行
original_height, original_width = original_image.shape[:2]
detections = detect_objects(net, original_image, output_layers)

# 表示のために画像をリサイズし、スケールを取得
resized_image, scale = resize_image(original_image, max_size)

# 元の画像とリサイズされた画像のサイズの比率を計算
scale_width = resized_image.shape[1] / original_image.shape[1]
scale_height = resized_image.shape[0] / original_image.shape[0]

# リサイズされた画像に検出結果を描画
label_counts = draw_predictions(resized_image, detections, labels, original_width, original_height, scale_width, scale_height)

# CSVファイルに追記
update_csv(label_counts, csv_path, objects_list)

for label, count in label_counts.items():
    print(f"{label}: {count}")

#cv2.imshow('Result', resized_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
