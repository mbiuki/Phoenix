'''
UBC Security of IoT Lab
April 2019
Mehdi Karimi
Description: Convert earth coordinates to cartesian
'''
import math
import csv
import os

# static values
equatorial_radius = 6378137.0 # in m
polar_radius = 6356752.3 # in m

# calculate prime vertical radius
def prime_vertical_radius(lat_rad):

    output = (equatorial_radius ** 2) / (math.sqrt(equatorial_radius ** 2 * (math.cos(lat_rad)) ** 2 + polar_radius ** 2 * (math.sin(lat_rad)) ** 2))

    return output

# convert to cartesian coords
def wgs84_to_cartesian(lat, long, height):

    # convert lat/long to radians
    lat_rad = math.radians(lat)
    long_rad = math.radians(long)

    # calculate x, y, and z
    x = (prime_vertical_radius(lat_rad) + height) * math.cos(lat_rad) * math.cos(long_rad)
    y = (prime_vertical_radius(lat_rad) + height) * math.cos(lat_rad) * math.sin(long_rad)
    z = ((polar_radius ** 2 / equatorial_radius ** 2) * prime_vertical_radius(lat_rad) + height) * math.sin(lat_rad)

    return (x, y, z)

def convert():

    # get list of csv files in input
    file_list = [os.path.join('samples', f) for f in os.listdir('samples') if os.path.isfile(os.path.join('samples', f)) and '.csv' in f]

    for file in file_list:

        # output file
        path_split = os.path.split(file)
        output_file = os.path.join('converted', path_split[1])

        # check if output file exists and remove
        if os.path.isfile(output_file):
            os.remove(output_file)

        # check and make directory of output if needed
        if not os.path.isdir(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))


        # open file and write header
        output_csv = open(output_file, 'w', newline = '')
        csv.writer(output_csv).writerow(['x', 'y', 'z'])

        # open csv
        with open(file, newline = '') as csv_file:

            csvreader = csv.reader(csv_file)

            # skip first line of csv
            next(csvreader)

            # parse csv
            for row in csvreader:

                # convert and write to output file
                csv.writer(output_csv).writerow(wgs84_to_cartesian(float(row[2]), float(row[3]), float(row[1])))

    return

# run if main
if __name__ == '__main__':
    convert()
