# Dash Cam Management Project

## Project Description

This project consists of a locally run python application which manages 
the storage of dash cam footage. Besides managing data stored from the dash cam,
the application also extracts additional metadata from the footage and stores 
it along with the footage. Current supported features are time, GPS, and plate extraction. 

## Setting up the Database
Docker is needed to run the database. The following commands will start and stop the database.

``` docker-compose up -d ```

``` docker-compose down ```

The data persists even after the database is stopped on 
the host machine at the location specified by the `DATA_PATH_FROM_SRC_DIR` environment variable.

The main function of `database.py` is used to a load configuration file into the database. 
See `config.json` for an example of this file layout. The config file creates and 
links entries for colors, dash cams, and vehicles. This can also be set up using 
INSERT statements directly in the database. 

## Running the Application

The main program is `dash_cam_management.py` it calls for a video to be loaded
and processed by the system. Additional fine tuning can be done by providing
a vehicle id (1 by default) and a feature frequency (30 by default).

## .ENV Variables

The following are environment variables that are needed for setting up the 
database and running the application. Default values are provided for each.

| Variable Name | Default Value | Description |
| ------------- | ------------- | ----------- |
| POSTGRES_USER | postgres | The username for the postgres database |
| POSTGRES_PASSWORD | postgres | The password for the postgres database |
| DATABASE_PORT | 5432 | The port for the postgres database |
| DATA_PATH_FROM_SRC_DIR | ../data | The location where the database will be stored |

