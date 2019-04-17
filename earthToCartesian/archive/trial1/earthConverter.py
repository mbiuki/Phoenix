'''
UBC Security of IoT Lab
March 2019
Mehdi Karimi
Description: 
Convert Earth Coordinates to Cartesian
'''
import math
import csv
import os

# MACROS, static values
EQUATORIAL_RADIUS = 6378137.0 # in m
POLAR_RADIUS = 6356752.3 # in m

"""
path_to_dir is the folder that has sample trajectories
for conversion
"""
path_to_dir = "./sample_trajecotries"

def list_csv_files(path_to_dir, suffix=".csv"):
    '''
    get a list of available csv files
    :param path_to_dir: provide the subdir name
    :param suffix: suffix is csv
    :return: a list of csv files
    '''
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

# calculate prime vertical radius
def prime_vertical_radius(lat_rad):

    output = (EQUATORIAL_RADIUS ** 2) / (math.sqrt(EQUATORIAL_RADIUS ** 2 * (math.cos(lat_rad)) ** 2 + POLAR_RADIUS ** 2 * (math.sin(lat_rad)) ** 2))

    return output

# convert to cartesian coords
def wgs84_to_cartesian(lat, long, height):
    '''
    :param lat: gps coordinate latitude
    :param long: gps coordinate longitude
    :param height: sea level latitude
    :return: cartesian xyz
    '''
    # convert lat/long to radians
    lat_rad = math.radians(lat)
    long_rad = math.radians(long)

    # calculate x, y, and z
    x = (prime_vertical_radius(lat_rad) + height) * math.cos(lat_rad) * math.cos(long_rad)
    y = (prime_vertical_radius(lat_rad) + height) * math.cos(lat_rad) * math.sin(long_rad)
    z = ((POLAR_RADIUS ** 2 / EQUATORIAL_RADIUS ** 2) * prime_vertical_radius(lat_rad) + height) * math.sin(lat_rad)

    return (x, y, z)

def convert():
    '''
    convert to cartesian
    :return: none, just do the conversion
    '''

    csvFiles= []
    for file in list_csv_files(path_to_dir):
        csvFiles.append(os.path.join(path_to_dir,file))

    for file in csvFiles:
        #create output name
        file_split = os.path.splitext(file)
        output_file = file_split[0] + '_cartesian' + file_split[1]

        # check if output file exists
        if not os.path.isfile(output_file):
            output_csv = open(output_file, 'w', newline = '')
            csv.writer(output_csv).writerow(['x', 'y', 'z'])

        else:
            output_csv = open(output_file, 'a', newline = '')

        # open csv
        with open(file, newline = '') as csv_file:
            csvreader = csv.reader(csv_file)

            # skip first line of csv
            next(csvreader)
            # parse csv
            for row in csvreader:
                # convert and write to output file
                csv.writer(output_csv).writerow(wgs84_to_cartesian(float(row[2]), float(row[3]), float(row[1])))

#run if main
if __name__ == '__main__':
    convert()