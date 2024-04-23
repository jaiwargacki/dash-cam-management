""" General functions for processing video data
@author: Jai Wargacki"""

import cv2, os, time
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor

from database import Database

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

def extract_clip(video_path: str, start_frame: int, end_frame: int, storage_path: str, feature: str = "clip") -> str:
    """ Extract a clip from a video file
    :param video_path: The path to the video file
    :param start_frame: The start frame of the clip
    :param end_frame: The end frame of the clip
    :param storage_path: The path to save the clip
    :param feature: The feature of the clip
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File does not exist at {video_path}")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    start_time = start_frame / 30
    end_time = end_frame / 30
    clip = VideoFileClip(video_path).subclip(start_time, end_time)
    clip_path = os.path.join(storage_path, feature + "_" + os.path.basename(video_path))
    clip.write_videofile(clip_path)
    clip.close()
    return clip_path

class Feature: 
    """ A metadata feature of a video """
    def __init__(self, name: str, description: str, frame_frequency: int=1, verbose: bool=False):
        self.name = name
        self.description = description
        self.frame_frequency = frame_frequency
        self.verbose = verbose

    def __str__(self):
        return f"{self.name}: {self.description}"

    def clear(self) -> None:
        """ Clear the feature data """
        raise NotImplementedError("Subclasses must implement this method")

    def process(self, frame, frame_number: int) -> None:
        """ Process a frame of the video """
        raise NotImplementedError("Subclasses must implement this method")

    def save(self, db: Database, trip_id: int) -> None:
        """ Save the feature data """
        raise NotImplementedError("Subclasses must implement this method")

class Processing:
    """ A processing object """
    def __init__(self, storage_path: str = "archive", verbose: bool=False):
        self.features = []
        self.storage_path = storage_path
        self.verbose = verbose
        self.video_paths = []
        self.TripData = None
        self.trip_start_date_time = None
        self.trip_end_date_time = None

    def add_feature(self, feature: Feature):
        self.features.append(feature)
        if feature.name == "TripData":
            self.TripData = feature

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
        self.video_paths.append(video_path)
        video_capture = cv2.VideoCapture(video_path)
        video_info = self.video_info(video_capture)

        if self.verbose:
            print(f"Processing video at {video_path}")
            print(f"Video Info: {video_info}")
     
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            frame_count = 0
            previous_frame = None
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    if self.TripData is not None:
                        self.trip_end_date_time = self.TripData.get_date_time(previous_frame)
                    break

                if self.TripData is not None and frame_count == 0:
                    self.trip_start_date_time = self.TripData.get_date_time(frame)

                for feature in self.features:
                    if frame_count % feature.frame_frequency == 0:
                        executor.submit(feature.process, frame, frame_count)
                frame_count += 1
                previous_frame = frame
            executor.shutdown(wait=True)
        video_capture.release()

        if self.verbose:
            print(f"Processing took {time.time() - start_time} seconds")

    def save(self, db: Database, vehicle_id: int) -> None:
        """ Save the features """
        if self.verbose:
            print("Saving features")

        # Save trip
        trip_id = db.createTrip(vehicle_id, self.trip_start_date_time, self.trip_end_date_time)
        if self.verbose:
            print(f"Trip ID: {trip_id}")

        # Save video entries
        for video_path in self.video_paths:
            archive_path = f"{self.storage_path}/{vehicle_id}/{trip_id}"
            filename = os.path.basename(video_path)
            move_to_storage(video_path, f"{self.storage_path}/{vehicle_id}/{trip_id}", delete=False)
            db.createVideoArchive(trip_id, f"{archive_path}/{filename}")
            if self.verbose:
                print(f"Video Archive: {archive_path}/{filename}")

        # Give features access to trip data
        for feature in self.features:
            if feature.name != "TripData":
                feature.trip_data = self.TripData.data_points
        
        # Save the features
        archive_path = f"{self.storage_path}/{vehicle_id}/{trip_id}/features"
        for feature in self.features:
            # Set archive path and video path for clip extraction
            feature.archive_path = archive_path
            feature.video_path = self.video_paths[0]
            feature.save(db, trip_id)

        db.commit()
