""" Submodule extracting the position, time, and speed of the vehicle from the video. 
@author: Jai Wargacki """

import easyocr
import re 

from processing import Feature
from database import Database

class TripData(Feature):
    """ A feature to extract the position, time, and speed of the vehicle from the video """
    def __init__(self, text_location_data: dict, freq: int = 30, verbose: bool=False):
        super().__init__("TripData", "Extracts the position, time, and speed of the vehicle from the video", freq, verbose)
        self.data_points = dict()
        self.reader = easyocr.Reader(['en'])
        self.text_location_data = text_location_data

    def clear(self):
        self.data_points = dict()

    def text_clean_up(self, text: str) -> str:
        """ Clean up the text """
        return "".join(text.split())
    
    def get_text(self, cropped) -> str:
        """ Get the text from the cropped image """
        text = ''
        for e in self.reader.readtext(cropped):
            text += self.text_clean_up(e[1])
        return text.strip()

    def get_date_time(self, frame) -> str:
        """ Get the time of the video """
        cropped = frame[self.text_location_data["time_location_y_min"]:self.text_location_data["time_location_y_max"], \
                        self.text_location_data["time_location_x_min"]:self.text_location_data["time_location_x_max"], :]
        date_text = self.get_text(cropped).replace("/", "-")
        date = re.findall(r"\d{1,2}-\d{2}-\d{4}", date_text)
        time_text = date_text.replace(date[0], "")
        time = re.findall(r"\d{2}.\d{2}.\d{2}", time_text)
        if len(date) == 1 and len(time) == 1:
            return date[0] + " " + time[0].replace(".", ":")
        return ""

    def get_location(self, frame) -> list:
        """ Get the location of the vehicle. 
        [0] is the latitude, [1] is the longitude """
        cropped = frame[self.text_location_data["gps_location_y_min"]:self.text_location_data["gps_location_y_max"], \
                        self.text_location_data["gps_location_x_min"]:self.text_location_data["gps_location_x_max"], :]
        location = self.get_text(cropped)
        lat_lon = re.findall(r"[NSEW]\d+\.\d*", location)
        if len(lat_lon) == 2:
            return [lat_lon[0], lat_lon[1]]
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
            else:
                if self.verbose:
                    print(f"Could not extract date time from frame {frame_number}", end=" ")
                    cropped = frame[self.text_location_data["time_location_y_min"]:self.text_location_data["time_location_y_max"], \
                        self.text_location_data["time_location_x_min"]:self.text_location_data["time_location_x_max"], :]
                    print(f"(Text: {self.get_text(cropped)})")
        else:
            if self.verbose:
                print(f"Could not extract location from frame {frame_number} ({lat_lon})")

    def save(self, db: Database, trip_id: int):
        """ Save the feature data """
        list_of_points = list(self.data_points.values())
        db.insertTripData(trip_id, list_of_points)

