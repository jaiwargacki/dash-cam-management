""" Submodule extracting the position, time, and speed of the vehicle from the video. 
@author: Jai Wargacki """

import cv2, easyocr
from processing import Feature

class TripData(Feature):
    """ A feature to extract the position, time, and speed of the vehicle from the video """
    def __init__(self):
        super().__init__("TripData", "Extracts the position, time, and speed of the vehicle from the video", 15)
        self.data_points = []
        self.reader = easyocr.Reader(['en'])

    def clear(self):
        self.data_points = []

    def process(self, frame):
        """ Process a frame of the video """
        cropped_for_location = frame[1380:1430, 10:410, :] # TODO: Need to use db to get value
        location = self.reader.readtext(cropped_for_location)
        if len(location) >= 1:
            lat_lon = location[0][1].replace(". ", ".").split(" ")
            if len(location) == 2:
                lat_lon += location[1][1].replace(". ", ".").split(" ")
            lat = lat_lon[0]
            lon = lat_lon[1]
            
            cropped_for_time = frame[1380:1430, 2190:2550, :] # TODO: Need to use db to get value
            date_time_capture = self.reader.readtext(cropped_for_time)
            if len(date_time_capture) == 2:
                date_time = date_time_capture[0][1].replace(" ", "") 
                date_time += " " + date_time_capture[1][1].replace(" ", "")
                self.data_points.append({"time": date_time, "lat": lat, "lon": lon})

    def save(self, trip_id):
        print(self.data_points)

def main():
    feature = TripData()

    # Load from from frame.jpg
    frame = "tests/test_data/frame01.jpg"
    image = cv2.imread(frame)

    # Process the frame
    feature.process(image)

    # Save the data
    feature.save(1)


if __name__ == "__main__":
    main()
        