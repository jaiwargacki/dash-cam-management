""" Submodule extracting the position, time, and speed of the vehicle from the video. 
@author: Jai Wargacki """

import cv2, easyocr

from processing import Feature
from database import Database

class TripData(Feature):
    """ A feature to extract the position, time, and speed of the vehicle from the video """
    def __init__(self, text_location_data: dict):
        super().__init__("TripData", "Extracts the position, time, and speed of the vehicle from the video", 30)
        self.data_points = []
        self.reader = easyocr.Reader(['en'])
        self.text_location_data = text_location_data

    def clear(self):
        self.data_points = []

    def get_date_time(self, frame) -> str:
        """ Get the time of the video """
        cropped = frame[self.text_location_data["time_location_y_min"]:self.text_location_data["time_location_y_max"], \
                        self.text_location_data["time_location_x_min"]:self.text_location_data["time_location_x_max"], :]
        date_time = self.reader.readtext(cropped)
        if len(date_time) == 2:
            date_time = date_time[0][1].replace(" ", "") + " " + date_time[1][1].replace(" ", "")
            return date_time.replace("/", "-")
        return ""

    def get_location(self, frame) -> list:
        """ Get the location of the vehicle. 
        [0] is the latitude, [1] is the longitude """
        cropped = frame[self.text_location_data["gps_location_y_min"]:self.text_location_data["gps_location_y_max"], \
                        self.text_location_data["gps_location_x_min"]:self.text_location_data["gps_location_x_max"], :]
        location = self.reader.readtext(cropped)
        if len(location) >= 1:
            lat_lon = location[0][1].replace(". ", ".").split(" ")
            if len(location) == 2:
                lat_lon += location[1][1].replace(". ", ".").split(" ")
            return lat_lon
        return []

    def process(self, frame):
        """ Process a frame of the video """
        lat_lon = self.get_location(frame)
        if len(lat_lon) == 2:
            lat = lat_lon[0]
            lon = lat_lon[1]
            date_time = self.get_date_time(frame)
            if date_time != "":
                self.data_points.append({"time": date_time, "lat": lat, "lon": lon})

    def save(self, db: Database, vehicle_id: int, trip_id: int):
        """ Save the feature data """
        db.insertTripData(trip_id, self.data_points)
        