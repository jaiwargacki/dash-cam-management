""" Test feature trip data module
@Author: Jai Wargacki"""

import cv2

from feature_trip_data import TripData

def test_trip_data_init():
    text_location_data = {
        "time_location_x_min" : 2190,
        "time_location_x_max" : 2550,
        "time_location_y_min" : 1380,
        "time_location_y_max" : 1430,
        "gps_location_x_min" : 10,
        "gps_location_x_max" : 410,
        "gps_location_y_min" : 1380,
        "gps_location_y_max" : 1430
    }
    feature = TripData(text_location_data)
    assert feature.name == "TripData"
    assert feature.description == "Extracts the position, time, and speed of the vehicle from the video"
    assert feature.frame_frequency == 30
    assert feature.data_points == []
    assert feature.text_location_data == text_location_data
    assert feature.reader is not None

def test_trip_data_clear():
    text_location_data = {
        "time_location_x_min" : 2190,
        "time_location_x_max" : 2550,
        "time_location_y_min" : 1380,
        "time_location_y_max" : 1430,
        "gps_location_x_min" : 10,
        "gps_location_x_max" : 410,
        "gps_location_y_min" : 1380,
        "gps_location_y_max" : 1430
    }
    feature = TripData(text_location_data)
    feature.data_points = ["test"]
    feature.clear()
    assert feature.data_points == []

def _test_trip_data_process(path, expected_time, expected_lat, expected_lon):
    text_location_data = {
        "time_location_x_min" : 2190,
        "time_location_x_max" : 2550,
        "time_location_y_min" : 1380,
        "time_location_y_max" : 1430,
        "gps_location_x_min" : 10,
        "gps_location_x_max" : 410,
        "gps_location_y_min" : 1380,
        "gps_location_y_max" : 1430
    }
    feature = TripData(text_location_data)
    frame = cv2.imread(path)
    feature.process(frame)

    assert len(feature.data_points) == 1
    actual = feature.data_points[0]
    assert actual["time"] == expected_time
    assert actual["lat"] == expected_lat
    assert actual["lon"] == expected_lon

def test_trip_data_process_1():
    path = "tests/test_data/frame01.jpg"
    expected_time = "01-23-2024 11:43:06"
    expected_lat = "N43.093457"
    expected_lon = "W77.649113"
    _test_trip_data_process(path, expected_time, expected_lat, expected_lon)

def test_trip_data_process_2():
    path = "tests/test_data/frame02.jpg"
    expected_time = "01-23-2024 11:44:12"
    expected_lat = "N43.093270"
    expected_lon = "W77.659285"
    _test_trip_data_process(path, expected_time, expected_lat, expected_lon)

def test_trip_data_process_3():
    path = "tests/test_data/frame03.jpg"
    expected_time = "01-27-2024 21:01:46"
    expected_lat = "N43.087085"
    expected_lon = "W77.593351"
    _test_trip_data_process(path, expected_time, expected_lat, expected_lon)

def test_trip_data_process_4():
    path = "tests/test_data/frame04.jpg"
    expected_time = "01-31-2024 11:49:43"
    expected_lat = "N43.088721"
    expected_lon = "W77.677018"
    _test_trip_data_process(path, expected_time, expected_lat, expected_lon)

def test_trip_data_process_5():
    path = "tests/test_data/frame05.jpg"
    expected_time = "01-31-2024 17:52:51"
    expected_lat = "N43.086873"
    expected_lon = "W77.679858"
    _test_trip_data_process(path, expected_time, expected_lat, expected_lon)
