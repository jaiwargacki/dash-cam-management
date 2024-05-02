""" Test database related elements of the project 
@Author: Jai Wargacki"""

import database

def test_database_connection():
    try:
        db = database.Database()
        assert True
    except Exception as e:
        print(e)
        assert False

def test_database_number_of_tables():
    db = database.Database()
    result = db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    count = result[0][0]
    assert count == 11

def test_database_save_color():
    db = database.Database()
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    assert color_id > 0

def test_database_save_camera():
    db = database.Database()
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    assert camera_id > 0

def test_database_save_vehicle():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    assert True

def test_database_save_event_type():
    db = database.Database()
    event_type = 'Test Event Type'
    event_type_id = db.save_event_type(event_type)
    assert event_type_id > 0

def test_database_save_plate():
    db = database.Database()
    plate = '123ABC'
    plate_id = db.save_plate(plate)
    assert plate_id > 0

def test_database_get_text_location_data():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    result = db.getTextLocationData(1)
    assert len(result) == 8
    assert 'time_location_x_min' in result
    assert 'time_location_x_max' in result
    assert 'time_location_y_min' in result
    assert 'time_location_y_max' in result
    assert 'gps_location_x_min' in result
    assert 'gps_location_x_max' in result
    assert 'gps_location_y_min' in result

def test_database_createTrip():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    start_date_time = '2024-01-01 00:00:00'
    end_date_time = '2024-01-01 00:05:00'
    trip_id = db.createTrip(1, start_date_time, end_date_time)
    assert trip_id > 0

def test_database_createVideoArchive():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    start_date_time = '2024-01-01 00:00:00'
    end_date_time = '2024-01-01 00:05:00'
    trip_id = db.createTrip(1, start_date_time, end_date_time)
    video_archive = {
        'trip_id': trip_id,
        'file_path': 'test.mp4'
    }
    video_archive_id = db.createVideoArchive(trip_id, 'test.mp4')
    assert video_archive_id > 0

def test_database_insertTripData():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    start_date_time = '2024-01-01 00:00:00'
    end_date_time = '2024-01-01 00:05:00'
    trip_id = db.createTrip(1, start_date_time, end_date_time)
    data = [{'time': '2024-01-01 00:00:00', 'lat': 0, 'lon': 0 }]
    db.insertTripData(trip_id, data)
    assert True

def test_database_insertEvent():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    start_date_time = '2024-01-01 00:00:00'
    end_date_time = '2024-01-01 00:05:00'
    trip_id = db.createTrip(1, start_date_time, end_date_time)
    event_type = 'Test Event Type'
    event_type_id = db.save_event_type(event_type)
    start_time = '2024-01-01 00:00:00'
    end_time = '2024-01-01 00:05:00'
    event_id = db.insertEvent(trip_id, event_type_id, start_time, end_time)
    assert event_id > 0

def test_database_insertEventPlate():
    db = database.Database()
    # Insert color
    color = {
        'name': 'Test Color',
        'hex': 'FFFFFF'
    }
    color_id = db.save_color(color)
    # Insert camera
    camera = {
        'name': 'Test Camera',
        'time_location_x_min': 1,
        'time_location_x_max': 2,
        'time_location_y_min': 3,
        'time_location_y_max': 4,
        'gps_location_x_min': 5,
        'gps_location_x_max': 6,
        'gps_location_y_min': 7,
        'gps_location_y_max': 8,
        'speed_location_x_min': 9,
        'speed_location_x_max': 10,
        'speed_location_y_min': 11,
        'speed_location_y_max': 12
    }
    camera_id = db.save_camera(camera)
    vehicle = {
        'make': 'Test Make',
        'model': 'Test Model',
        'year': 2021,
        'color_id': color_id,
        'camera_id': camera_id
    }
    db.save_vehicle(vehicle)
    start_date_time = '2024-01-01 00:00:00'
    end_date_time = '2024-01-01 00:05:00'
    trip_id = db.createTrip(1, start_date_time, end_date_time)
    event_type = 'Test Event Type'
    event_type_id = db.save_event_type(event_type)
    start_time = '2024-01-01 00:00:00'
    end_time = '2024-01-01 00:05:00'
    event_id = db.insertEvent(trip_id, event_type_id, start_time, end_time)
    plate = '123ABC'
    plate_id = db.save_plate(plate)
    db.insertEventPlate(event_id, plate_id)
    assert True
