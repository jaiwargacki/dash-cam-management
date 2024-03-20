""" Main module for the dash cam management system. 
@author: Jai Wargacki """

import argparse

import processing, feature_trip_data, database

def main() -> None:
    """ Main function for processing a video file """
    # Arg parsing
    parser = argparse.ArgumentParser(description="Process a video file")
    parser.add_argument("video_path", type=str, help="The path to the video file")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    args = parser.parse_args()

    vehicle_id = 1
    db = database.Database()

    # Setup processing
    processor = processing.Processing("../archived", args.verbose)
    text_location_data = db.getTextLocationData(vehicle_id)
    processor.add_feature(feature_trip_data.TripData(text_location_data))

    # Process the video
    processor.process(args.video_path)

    # Save the data
    processor.save(db, vehicle_id)

if __name__ == "__main__":
    main()