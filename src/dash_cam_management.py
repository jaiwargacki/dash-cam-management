""" Main module for the dash cam management system. 
@author: Jai Wargacki """

import argparse, time

import processing, feature_trip_data, feature_plate_data, database

def main() -> None:
    """ Main function for processing a video file """
    start_time = time.time()
    # Arg parsing
    parser = argparse.ArgumentParser(description="Process a video file")
    parser.add_argument("video_path", type=str, help="The path to the video file")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("--vehicle_id", type=int, help="The vehicle id to process", default=1)
    parser.add_argument("--feature_frequency", type=int, help="The frequency of the features", default=30)
    args = parser.parse_args()

    vehicle_id = args.vehicle_id
    db = database.Database()

    # Setup processing
    processor = processing.Processing("../archived", args.verbose)
    text_location_data = db.getTextLocationData(vehicle_id)
    processor.add_feature(feature_trip_data.TripData(text_location_data, args.feature_frequency, args.verbose))
    processor.add_feature(feature_plate_data.PlateData(args.feature_frequency, args.verbose))

    # Process the video
    processor.process(args.video_path)

    # Save the data
    processor.save(db, vehicle_id)

    print(f"Total run time of {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()