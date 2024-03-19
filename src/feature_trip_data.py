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

    def process(self, frame):
        """ Process a frame of the video """
        cropped_for_location = frame[self.text_location_data["gps_location_y_min"]:self.text_location_data["gps_location_y_max"], \
                                self.text_location_data["gps_location_x_min"]:self.text_location_data["gps_location_x_max"], :]
        location = self.reader.readtext(cropped_for_location)
        if len(location) >= 1:
            lat_lon = location[0][1].replace(". ", ".").split(" ")
            if len(location) == 2:
                lat_lon += location[1][1].replace(". ", ".").split(" ")
            lat = lat_lon[0]
            lon = lat_lon[1]
            
            cropped_for_time = frame[self.text_location_data["time_location_y_min"]:self.text_location_data["time_location_y_max"], \
                                self.text_location_data["time_location_x_min"]:self.text_location_data["time_location_x_max"], :]
            date_time_capture = self.reader.readtext(cropped_for_time)
            if len(date_time_capture) == 2:
                date_time = date_time_capture[0][1].replace(" ", "") 
                date_time += " " + date_time_capture[1][1].replace(" ", "")
                self.data_points.append({"time": date_time, "lat": lat, "lon": lon})

    def save(self, db: Database, vehicle_id: int, trip_id: int):
        print(self.data_points)
        