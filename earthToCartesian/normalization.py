'''
UBC Security of IoT Lab
April 2019
Mehdi Karimi
Description:
Description:  normalization and save as .png 
'''
import os
import csv
import math
import earthConverter
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# normalize a row
def normalize(row):

    # normalize coords
    temp = [row[0] - first_row[0], row[1] - first_row[1], row[2] - first_row[2]]
    row_normalized = [abs(x) for x in temp]

    return row_normalized

# convert coords to cartesion
earthConverter.convert()

# create list of csv files in the dir 'converted'
files = [os.path.join('converted', f) for f in os.listdir(os.path.join('converted')) if os.path.isfile(os.path.join('converted', f))]
csv_files = [f for f in files if '.csv' in f]

for file in csv_files:

    # variables
    first_row = [0, 0, 0]
    x_coords = []
    y_coords = []
    z_coords = []

    # output file
    path_split = os.path.split(file)
    file_split = os.path.splitext(path_split[1])
    output_file = os.path.join('normalized', file_split[0] + '_cartesian' + file_split[1])

    # check if file exists, and remove if it does
    if os.path.isfile(output_file):
        os.remove(output_file)

    # check and make directory of output if needed
    if not os.path.isdir(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))


    # opens new file and writes header
    with open(output_file, 'w', newline = '') as output_csv:
        csv.writer(output_csv).writerow(['x', 'y', 'z'])

        # open csv
        with open(file, newline = '') as csv_file:

            csvreader = csv.reader(csv_file)

            # skip first line
            next(csvreader)

            # parse csv
            for row in csvreader:

                # set first_row if first line of data
                if csvreader.line_num == 2:
                    first_row = [float(x) for x in row]

                # generalize and write to file
                csv.writer(output_csv).writerow(normalize([float(x) for x in row]))

    # open output file
    with open(output_file) as plot_csv:

        csvreader = csv.reader(plot_csv)

        # skip first line
        next(csvreader)

        # plot csv file
        for row in csvreader:
            x_coords.append(float(row[0]))
            y_coords.append(float(row[1]))
            z_coords.append(float(row[2]))

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        ax.plot3D(x_coords, y_coords, z_coords, 'blue')

        # save to file
        plt.savefig(os.path.splitext(os.path.split(output_file)[1])[0] + '.png')
