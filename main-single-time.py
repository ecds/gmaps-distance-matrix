from datetime import datetime
import sys, googlemaps, csv, json

#########################################################################
# Please define these variables before you use this application

# Your Google Maps Developer API Key
gMapsAPIKey = ''

# Source CSV filename
source_filename = "sample.csv"

# Source CSV labels
idLabel = "FID"
fromLongLabel = 'FROM_X'
fromLatLabel = 'FROM_Y'
toLongLabel = 'NEAR_X'
toLatLabel = 'NEAR_Y'

# Output CSV labels
distanceLabel = "Distance"
durationLabel = "Duration"
durationValueLabel = "Duration (seconds)"
jsonLabel = "JSON"

# Log status field label
statusLabel = "Status"
#########################################################################

# Print the initial welcome message that explains what this application does and what to expect
def print_welcome():
    message = '''
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

================================================
'''
    # Print out welcome message
    print(message)

    # Prompt for user input to proceed or abort
    if not query_yes_no("Have you read above information and have the required parameters defined?"):
        print("Google Maps Distance Matrix App exited. Thank you for using.")
        sys.exit()

# A method to prompt the user to provide yes/no input to the application
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# Create a CSV DictReader object
def read_source_file(source_filename):
    source = open(source_filename, "r")
    return csv.DictReader(source)

# Create a CSV DictWriter object for the output
def create_output_file(source_filename, fields):
    timestamp_str = datetime.now().strftime("%m-%d-%Y--%I-%M-%S")
    output = open("%s--%s.csv" % (source_filename.split('.')[0], timestamp_str), 'w')
    logFilename = "%s--%s.log" % (source_filename.split('.')[0], timestamp_str)
    output_writer = csv.DictWriter(output, fieldnames=fields)
    output_writer.writeheader()
    return output_writer, logFilename

# Create a CSV DictWriter object for logging
def create_log_file(source_filename, fields):
    output = open(logFilename, 'w')
    output_writer = csv.DictWriter(output, fieldnames=fields)
    output_writer.writeheader()
    return output_writer

# Print the welcome message
print_welcome()

# Create a Google Maps Python client
gmaps = googlemaps.Client(key=gMapsAPIKey)

# Create a CSV DictWriter object for output
output_writer, logFilename = create_output_file(source_filename, [idLabel, distanceLabel, durationLabel, durationValueLabel, jsonLabel])

# Create a CSV DictReader object for source
source_reader = read_source_file(source_filename)

# Create a CSV DictWriter object for logging
log_writer = create_log_file(source_filename, [idLabel, statusLabel])

# Process each row from the source, make a Google Maps API call, and store data in the output file
for row in source_reader:

    try: 
        # Make the directions Google Maps API call
        directions_result = gmaps.directions( "%s, %s" % (row[fromLatLabel], row[fromLongLabel]),
                                                "%s, %s" % (row[toLatLabel], row[toLongLabel]),
                                                mode="driving",
                                            #   traffic_model="pessimistic",
                                            #   departure_time=datetime.now()
                                            )

        # Convert returned data into a stringified JSON for CSV writing
        directions_result_json = json.dumps(directions_result[0])

        # Extracted value fields
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']
        durationValue = directions_result[0]['legs'][0]['duration']['value']

        # Construct a row for the CSV DictWriter to write into the output CSV file
        output_row = {idLabel: row[idLabel], distanceLabel: distance, durationLabel: duration, durationValueLabel: durationValue, jsonLabel: directions_result_json}
        
        # Write into the output file
        output_writer.writerow(output_row)

        # Construct a log row
        log_row = {idLabel: row[idLabel], statusLabel: "Success"}
        
        # Log success
        log_writer.writerow(log_row)

        # Print on screen to update status
        print("[FID %s] (%s, %s) -> (%s, %s) - %s - %s" % (row[idLabel], row[fromLatLabel], row[fromLongLabel], row[toLatLabel], row[toLongLabel], distance, duration))
    
    except:
        # Print on screen to update status
        print("[FID %s] An error has occured." % (row[idLabel]))

        # Construct a log row
        log_row = {idLabel: row[idLabel], statusLabel: "An error has occured"}
        
        # Log errors
        log_writer.writerow(log_row)