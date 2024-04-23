""" Submodule extracting plate data from the video.
@author: Jai Wargacki """

import cv2
import requests

from processing import Feature, extract_clip
from database import Database

class PlateData(Feature):
    """ A feature to extract the plate data from the video """
    PLATE_TYPE_NAME = "Plate" # Must match config file
    CONFIDENT_THRESHOLD = 85.0
    URL_DETECTION = "http://localhost:3000/detect"
    MAX_HEIGHT = 1080
    MAX_WIDTH = 1920

    def __init__(self, verbose: bool=False):
        super().__init__("PlateData", "Extracts the plate data from the video", 30, verbose)
        self.trip_data = None

    def clear(self):
        self.plate_sites = dict()

    def plate_request(self, sub_frame):
        """ Get the plates from the frame by making a post request to the plate detection.
        The post contains form data with the frame image as png (upload) and the country_code """
        country_code = "us"
        sub_frame_encoded = cv2.imencode('.jpg', sub_frame)[1].tobytes()
        response = requests.post(self.URL_DETECTION, files={"upload": sub_frame_encoded}, data={"country_code": country_code})
        results = dict()
        for result in response.json()['results']:
            plate = result['plate']
            confidence = result['confidence']
            coordinates = result['coordinates']
            if confidence > self.CONFIDENT_THRESHOLD:
                results[plate] = {"confidence": confidence, "coordinates": coordinates}
        return results

    def get_plates(self, frame) -> str:
        """ Get the plates from the frame, the top half of the frame is cut out and not processed """
        height, width, _ = frame.shape
        plates = set()
        if height > self.MAX_HEIGHT or width > self.MAX_WIDTH:
            # Resize the frame
            frame = cv2.resize(frame, (self.MAX_WIDTH, self.MAX_HEIGHT))
            # Cut out top half of the frame
            frame = frame[self.MAX_HEIGHT // 2:, :]
            # Split to 3 images
            left = frame[:, :self.MAX_WIDTH // 2]
            center = frame[:, self.MAX_WIDTH // 2:]
            right = frame[:, self.MAX_WIDTH // 4:3 * self.MAX_WIDTH // 4]
            for f in [left, center, right]:
                plates.update(self.plate_request(f).keys())
        return plates

    def process(self, frame, frame_number: int):
        """ Process a frame of the video """
        for plate in self.get_plates(frame):
            if plate not in self.plate_sites:
                self.plate_sites[plate] = []
            self.plate_sites[plate].append(frame_number)

    def save(self, db: Database, trip_id: int):
        """ Save the feature data (and extract clip)"""
        if self.trip_data is None:
            raise ValueError("Trip data must be set before saving")
        if self.verbose:
            print(f"Saving {len(self.plate_sites)} plates")
        event_type_id = db.save_event_type(self.PLATE_TYPE_NAME)
        for plate, frames in self.plate_sites.items():
            if len(frames) < 2:
                continue
            plate_id = db.save_plate(plate)
            start_frame = min(frames)
            end_frame = max(frames)
            start_time = self.trip_data[start_frame]["time"]
            end_time = self.trip_data[end_frame]["time"]
            event_data = f"Plate: {plate}"
            clip_path = extract_clip(self.video_path, start_frame, end_frame, self.archive_path, plate)
            event_id = db.insertEvent(trip_id, event_type_id, start_time, end_time, clip_path, event_data)
            db.insertEventPlate(event_id, plate_id)
        