""" Module to demonstrate that the media is slow and big
@author: Jai Wargacki"""

import argparse, cv2, time
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Demonstrate that the media is slow and big")
    parser.add_argument("file_path", type=str, help="The path to the video file")
    args = parser.parse_args()

    video_capture = cv2.VideoCapture(args.file_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    print("fps:", fps)
    print("frame_count:", frame_count)
    print("duration:", f'{duration:.0f}', "seconds")
    frame_size = 0
    running_diff = 0
    previous_frame = None
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        if previous_frame is not None:
            diff = cv2.absdiff(previous_frame, frame)
            diff = diff.astype(np.uint8)
            running_diff += (np.count_nonzero(diff) * 100)/ diff.size
        previous_frame = frame
        if frame_size == 0:
            frame_size = frame.nbytes
        elif frame_size != frame.nbytes:
            print("frame size is not consistent")
    video_capture.release()

    video_capture = cv2.VideoCapture(args.file_path)
    start = time.time()
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
    end = time.time()
    video_capture.release()
    print("time to read:", f'{end - start:.2f}', "seconds")
    print("total memory of raw video:", f'{frame_size * frame_count:.0f}', "Bytes")
    print("average difference between frames:", f'{running_diff / frame_count:.0f}', "%")
    

if __name__ == "__main__":
    main()