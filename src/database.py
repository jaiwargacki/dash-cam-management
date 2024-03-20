""" Module for database connections and operations. 
@author: Jai Wargacki """

import argparse, json
import psycopg2

class Database:
    """ Class to handle database connections and operations. """
    def __init__(self, dbname: str = 'dashcam', user: str = 'postgres', host: str = 'localhost', password: str = 'postgres'):
        self.conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def execute(self, query: str):
        """ Execute a query on the database and return the result. """
        self.cur.execute(query)
        return self.cur.fetchall()

    def commit(self):
        """ Commit the current transaction to the database. """
        self.conn.commit()

    def save_color(self, color: dict):
        """ Save a color to the database return the color's id """
        query = f"INSERT INTO COLOR (COLOR_NAME, COLOR_HEX) VALUES ('{color['name']}', '{color['hex']}') RETURNING ID;"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def save_camera(self, camera: dict):
        """ Save a camera to the database return the camera's id """
        query = f"INSERT INTO DASH_CAM (DASH_CAM_NAME, TIME_LOCATION_X_MIN, TIME_LOCATION_X_MAX, \
            TIME_LOCATION_Y_MIN, TIME_LOCATION_Y_MAX, GPS_LOCATION_X_MIN, GPS_LOCATION_X_MAX, \
            GPS_LOCATION_Y_MIN, GPS_LOCATION_Y_MAX, SPEED_LOCATION_X_MIN, SPEED_LOCATION_X_MAX, \
            SPEED_LOCATION_Y_MIN, SPEED_LOCATION_Y_MAX) VALUES ('{camera['name']}', \
            {camera['time_location_x_min']}, {camera['time_location_x_max']}, \
            {camera['time_location_y_min']}, {camera['time_location_y_max']}, \
            {camera['gps_location_x_min']}, {camera['gps_location_x_max']}, \
            {camera['gps_location_y_min']}, {camera['gps_location_y_max']}, \
            {camera['speed_location_x_min']}, {camera['speed_location_x_max']}, \
            {camera['speed_location_y_min']}, {camera['speed_location_y_max']}) \
            RETURNING ID;"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def save_vehicle(self, vehicle: dict):
        """ Save a vehicle to the database return the vehicle's id """
        query = f"INSERT INTO VEHICLE (MAKE, MODEL, VEHICLE_YEAR, COLOR_ID, DASH_CAM_ID) \
            VALUES ('{vehicle['make']}', '{vehicle['model']}', {vehicle['year']}, \
            {vehicle['color_id']}, {vehicle['camera_id']})"
        self.cur.execute(query)

    def getTextLocationData(self, vehicle_id: int) -> dict:
        """ Get the text location data for a vehicle """
        query = f"SELECT D.TIME_LOCATION_X_MIN, D.TIME_LOCATION_X_MAX, D.TIME_LOCATION_Y_MIN, D.TIME_LOCATION_Y_MAX, \
            D.GPS_LOCATION_X_MIN, D.GPS_LOCATION_X_MAX, D.GPS_LOCATION_Y_MIN, D.GPS_LOCATION_Y_MAX FROM VEHICLE V \
            JOIN DASH_CAM D ON V.DASH_CAM_ID = D.ID WHERE V.ID = {vehicle_id}"
        result = self.execute(query)
        return {
            "time_location_x_min" : result[0][0],
            "time_location_x_max" : result[0][1],
            "time_location_y_min" : result[0][2],
            "time_location_y_max" : result[0][3],
            "gps_location_x_min" : result[0][4],
            "gps_location_x_max" : result[0][5],
            "gps_location_y_min" : result[0][6],
            "gps_location_y_max" : result[0][7]
        }

    def createTrip(self, vehicle_id: int, start_date_time: str, end_date_time: str) -> int:
        """ Create a trip in the database and return the trip's id """
        query = f"INSERT INTO TRIP (VEHICLE_ID, START_TIME, END_TIME) VALUES ({vehicle_id}, '{start_date_time}', '{end_date_time}') RETURNING ID;"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def createVideoArchive(self, trip_id: int, video_path: str) -> None:
        """ Create a video archive in the database """
        query = f"INSERT INTO VIDEO (TRIP_ID, FILE_PATH) VALUES ({trip_id}, '{video_path}')"
        self.cur.execute(query)

    def insertTripData(self, trip_id: int, data: list) -> None:
        """ Insert trip data into the database """
        query = f"INSERT INTO TRIP_DATA (TRIP_ID, TRIP_DATA_TIME, LATITUDE, LONGITUDE, SPEED) VALUES "
        for point in data:
            query += f"({trip_id}, '{point['time']}', '{point['lat']}', '{point['lon']}', 0),"
        query = query[:-1] + ";"
        self.cur.execute(query)

def main():
    """ Load a configuration file and save it to the database """
    # Arg parsing
    parser = argparse.ArgumentParser(description="Load configuration to the database")
    parser.add_argument("config_file", type=str, help="JSON file with configuration data")
    args = parser.parse_args()

    # Load the configuration
    config = {}
    try: 
        with open(args.config_file) as f:
            config = json.load(f)
    except Exception as e:
        print("Error loading configuration")
        print(e)
        return

    if not config:
        print("Configuration is empty")
        return

    # Save the configuration
    db = Database()
    print("Saving configuration")

    # Colors
    for color in config['colors']:
        color_id = db.save_color(color)
        color['id'] = color_id

    # Cameras
    for camera in config['dash_cams']:
        camera_id = db.save_camera(camera)
        camera['id'] = camera_id

    # Vehicles
    for vehicle in config['vehicles']:
        vehicle['color_id'] = next((color['id'] for color in config['colors'] if color['name'] == vehicle['color']), None)
        vehicle['camera_id'] = next((camera['id'] for camera in config['dash_cams'] if camera['name'] == vehicle['dash_cam']), None)
        if not vehicle['color_id'] or not vehicle['camera_id']:
            print(f"Error saving vehicle: {vehicle['make']} {vehicle['model']} {vehicle['year']}")
            continue
        db.save_vehicle(vehicle)

    db.commit()
    print("Configuration saved")

if __name__ == "__main__":
    main()
    