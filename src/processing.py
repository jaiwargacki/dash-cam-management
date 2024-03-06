""" General functions for processing video data
@author: Jai Wargacki"""

import cv2, os, time, math
from concurrent.futures import ThreadPoolExecutor

def move_to_storage(file_path: str, storage_path: str, delete: bool=False) -> None:
    """ Move a file to the storage location
    :param file_path: The path of the file to move
    :param storage_path: The path to move the file to
    :param delete: Whether or not to delete the file after moving
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist at {file_path}")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    file = os.path.basename(file_path)
    if delete:
        os.rename(file_path, os.path.join(storage_path, file))
    else:
        with open(file_path, 'rb') as f:
            with open(os.path.join(storage_path, file), 'wb') as s:
                s.write(f.read())

class Feature: 
    """ A metadata feature of a video """
    def __init__(self, name: str, description: str, frame_frequency: int=1):
        self.name = name
        self.description = description
        self.frame_frequency = frame_frequency

    def __str__(self):
        return f"{self.name}: {self.description}"

    def clear(self) -> None:
        """ Clear the feature data """
        raise NotImplementedError("Subclasses must implement this method")

    def process(self, frame) -> None:
        """ Process a frame of the video """
        raise NotImplementedError("Subclasses must implement this method")

    def save(self, trip_id: int) -> None:
        """ Save the feature data """
        raise NotImplementedError("Subclasses must implement this method")

class Processing:
    """ A processing object """
    def __init__(self, verbose: bool=False):
        self.features = []
        self.verbose = verbose
        self.video_path = None

    def add_feature(self, feature: Feature):
        self.features.append(feature)

    def video_info(self, video: cv2.VideoCapture) -> dict:
        """ Get the information of the video """
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        return {
            "fps": fps,
            "frame_count": frame_count,
            "duration": duration
        }

    def process(self, video_path: str) -> None:
        """ Process the video file using a list of features
        :param video_path: The path to the video file
        """
        # Clear the features
        for feature in self.features:
            feature.clear()
        self.video_path = video_path
        video_capture = cv2.VideoCapture(self.video_path)
        video_info = self.video_info(video_capture)

        if self.verbose:
            print(f"Processing video at {self.video_path}")
            print(f"Video Info: {video_info}")
     
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            frame_count = 0
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                for feature in self.features:
                    if frame_count % feature.frame_frequency == 0:
                        executor.submit(feature.process, frame)
                frame_count += 1
            executor.shutdown(wait=True)
        video_capture.release()

        if self.verbose:
            print(f"Processing took {time.time() - start_time} seconds")

    def save(self) -> None:
        """ Save the features """
        if self.video_path is None:
            raise ValueError("No video path was given")

        if self.verbose:
            print("Saving features")

        # Create or get the trip id
        trip_id = 1

        # Save the features
        for feature in self.features:
            feature.save(trip_id)

