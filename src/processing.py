""" General functions for processing video data
@author: Jai Wargacki"""

import cv2, os
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
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

class Video:
    """ A video file """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.features = []

    def add_feature(self, feature: Feature):
        self.features.append(feature)

    def process(self, features: list[Feature], num_workers: int=7) -> None:
        """ Process the video file using a list of features
        :param features: A list of Feature objects to derive from the video
        :param num_workers: The number of workers to use in parallel processing (default 7)
        """
        video_capture = cv2.VideoCapture(self.file_path)
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break
                for feature in features:
                    executor.submit(feature.process, frame)
            executor.shutdown(wait=True)
        video_capture.release()

    def save(self, storage_path: str, delete: bool=False) -> None:
        """ Save the video file to the storage location
        :param storage_path: The path to move the file to
        :param delete: Whether or not to delete the file after moving
        """
        move_to_storage(self.file_path, storage_path, delete)

    def __str__(self):
        return f"Video: {self.file_path}"

