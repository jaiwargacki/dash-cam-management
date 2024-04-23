""" Submodule extracting the position, time, and speed of the vehicle from the video. 
@author: Jai Wargacki """

import easyocr

from processing import Feature
from database import Database

class TripData(Feature):
    """ A feature to extract the position, time, and speed of the vehicle from the video """
    def __init__(self, text_location_data: dict, verbose: bool=False):
        super().__init__("TripData", "Extracts the position, time, and speed of the vehicle from the video", 30, verbose=False)
        self.data_points = dict()
        self.reader = easyocr.Reader(['en'])
        self.text_location_data = text_location_data

    def clear(self):
        self.data_points = dict()

    def get_date_time(self, frame) -> str:
        """ Get the time of the video """
        cropped = frame[self.text_location_data["time_location_y_min"]:self.text_location_data["time_location_y_max"], \
                        self.text_location_data["time_location_x_min"]:self.text_location_data["time_location_x_max"], :]
        date_time = ''
        for e in self.reader.readtext(cropped):
            date_time += self.text_clean_up(e[1]) + " "
        return date_time.strip().replace("/", "-")
    
    def text_clean_up(self, text: str) -> str:
        """ Clean up the text """
        # replace all white space with a single space
        text = " ".join(text.split())
        text = text.replace(". ", ".")
        text = text.replace(" .", ".")
        text = text.replace(": ", ":")
        text = text.replace(" :", ":")
        return text.strip()

    def get_location(self, frame) -> list:
        """ Get the location of the vehicle. 
        [0] is the latitude, [1] is the longitude """
        cropped = frame[self.text_location_data["gps_location_y_min"]:self.text_location_data["gps_location_y_max"], \
                        self.text_location_data["gps_location_x_min"]:self.text_location_data["gps_location_x_max"], :]
        location = self.reader.readtext(cropped)
        if len(location) >= 1:
            lat_lon = self.text_clean_up(location[0][1]).split(" ")
            if len(location) == 2:
                lat_lon += self.text_clean_up(location[1][1]).split(" ")
            return lat_lon
        return []

    def process(self, frame, frame_number: int):
        """ Process a frame of the video """
        lat_lon = self.get_location(frame)
        if len(lat_lon) == 2:
            lat = lat_lon[0]
            lon = lat_lon[1]
            date_time = self.get_date_time(frame)
            if date_time != "":
                self.data_points[frame_number] = {"frame_number": frame_number, "time": date_time, "lat": lat, "lon": lon}

    def save(self, db: Database, trip_id: int):
        """ Save the feature data """
        list_of_points = list(self.data_points.values())
        db.insertTripData(trip_id, list_of_points)

