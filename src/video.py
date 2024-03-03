""" Utility functions for loading and saving videos. 
@author: Jai Wargacki"""

import cv2
import numpy as np

import time
from concurrent.futures import ThreadPoolExecutor

def process(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply Canny Edge Detection
    edges = cv2.Canny(blur, 50, 150)

def info(path):
    video_capture = cv2.VideoCapture(path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    print("fps: ", fps)
    print("frame_count: ", frame_count)
    print("duration: ", duration)
    video_capture.release()
    return duration


def linear_testing(path):
    video_capture = cv2.VideoCapture(path)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        process(frame)
    video_capture.release()

def parrallel_testing(path, num_workers=7):
    video_capture = cv2.VideoCapture(path)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            executor.submit(process, frame)
        executor.shutdown(wait=True)
    video_capture.release()


def main():
    path = "../working-data/20240131103244_021233_short.MP4"
    duration = info(path)
    start = time.time()
    linear_testing(path)
    end = time.time()
    print("time linear: ", end - start)
    print("percentage: ", (end - start) / duration)

    start = time.time()
    parrallel_testing(path)
    end = time.time()
    print("time parrallel: ", end - start)
    print("percentage: ", (end - start) / duration)

if __name__ == "__main__":
    main()
