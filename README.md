# Dash Cam Management Project

## Project Description

This project consists of a locally run python application which manages 
the storage of dash cam footage. Besides managing data stored from the dash cam,
the application also extracts additional metadata from the footage and stores 
it along with the footage.

## Feature Overview

Coming soon...

## Setting up the Database
Docker is needed to run the database. The following commands will start and stop the database.

``` docker-compose up -d ```

``` docker-compose down ```

The data persists even after the database is stopped on 
the host machine at the location specified by the `DATA_PATH_FROM_SRC_DIR` environment variable.

## Running the Application

Coming soon...

## Other Details

### .ENV Variables

The following are environment variables that are needed for setting up the 
database and running the application. Default values are provided for each.

| Variable Name | Default Value | Description |
| ------------- | ------------- | ----------- |
| POSTGRES_USER | postgres | The username for the postgres database |
| POSTGRES_PASSWORD | postgres | The password for the postgres database |
| DATABASE_PORT | 5432 | The port for the postgres database |
| DATA_PATH_FROM_SRC_DIR | ../data | The location where the database will be stored |

