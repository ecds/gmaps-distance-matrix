# google-maps-distance-matrix

Google Maps Distance Matrix App 0.1
===================================
10/30/2018 Monday | Created at Emory Center for Digital Scholarship
Developer: Yang Li (yang.li@emory.edu)

Documentation
=============
Originally written for Gilead COMPASS Initiative at Emory University Rollins School of Public Health.

The application uses Google Maps Distance Matrix API to calculate the distance and driving time between 
an HIV facility and a pre-defined community center. In order to calculate for a large volume of from-to
coordinate pairs, the application reads them from a CSV in which the from and to coordinates are defined.
The output is a CSV where the distance, duration in human readable format, duration in seconds, and a 
raw Google Maps API JSON are stored for each coordinate pair.

In order to use this application, please provide the followings:

Google Maps Developer API Key
=============================
gMapsAPIKey - Google Maps Developer API Key

Source (Input) file and attributes (Attributes need to match the source file header)
====================================================================================
source_filename - Filename of the CSV where the from and to coordinates are provided
idLabel - Label for the unique identifier for each coordinate pair
fromLongLabel - Label for the longtitude of the from location
fromLatLabel - Label for the latitude of the from location
toLongLabel - Label for the longtitude of the to location
toLatLabel - Label for the latitude of the to location

Output file and attributes (Attributes can be customized)
=========================================================
distanceLabel - Label for distance column
durationLabel - Label for duration column (in human readable format)
durationValueLabel - Label for duration column (in value format, seconds)
jsonLabel - Label for raw JSON returned by Google Maps; can extract more information in the future without
making another query

Log file attribute (Attribute can be customized)
================================================
statusLabel - Label for the status of query for each row