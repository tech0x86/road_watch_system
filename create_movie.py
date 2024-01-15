import cv2
import glob
import os
import sys
from datetime import datetime, timedelta

def create_timelapse(date, base_input_dir, output_dir):
    input_dir = os.path.join(base_input_dir, date)
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
        text = os.path.basename(filename)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (255, 255, 255)
        black_color = (0, 0, 0)
        line_type = 1
        thickness = 1

        text_size = cv2.getTextSize(text, font, font_scale, line_type)[0]
        text_position = (width - text_size[0] - 10, 20)

        # Add a black outline for better visibility
        cv2.putText(img, text, (text_position[0], text_position[1]), font, font_scale, black_color, thickness + 1, lineType=cv2.LINE_AA)
        cv2.putText(img, text, text_position, font, font_scale, font_color, line_type, lineType=cv2.LINE_AA)

        out.write(img)

    out.release()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_input_dir = os.path.join(base_dir, 'detect_pic')
    output_dir = os.path.join(base_dir, 'movie')

    # Check if a date argument is passed from the command line
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y%m%d')

    create_timelapse(date_str, base_input_dir, output_dir)

if __name__ == "__main__":
    main()
