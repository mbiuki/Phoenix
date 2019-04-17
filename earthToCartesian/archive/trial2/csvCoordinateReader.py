'''
UBC Security of IoT Lab
April 2019
Mehdi Karimi
Description:
Description:
Function generalization in cartesian space
'''
import csv
import os
import matplotlib.pyplot as plt
from archive.trial2.earthConverter import cartesian_conversion

if __name__ == "__main__":
    # Initialzes a list of CSV files from the same directory to read
    file_list = []
    for file in os.listdir(os.getcwd()):
        if file.lower().endswith('.csv') \
                and not file.lower().endswith('_cartesian.csv'):
            file_list.append(file.lower())

    for file in file_list:
        # Sets the target file to write new Cartesian coordinates to
        dest_file = file.replace('.csv', '_cartesian.csv')

        with open(file, 'r') as raw_file, \
                open(dest_file, 'w', newline='') as cartesian_file:
            raw_reader = csv.reader(raw_file, delimiter=',')
            cartesian_writer = csv.writer(cartesian_file, delimiter=',')

            # Initializes some variables for storing converted coordinates and
            # minimum values of respective axes for normalization
            x_list = []
            y_list = []
            z_list = []
            x_min = 0
            y_min = 0
            z_min = 0

            for index, row in enumerate(raw_reader):

                # Searches the header row for respective axis columns, and stores
                # the index of their column
                if index == 0:
                    for column in row:
                        if column.lower().startswith('altitude'):
                            alt_index = row.index(column)
                        elif column.lower().startswith('latitude'):
                            lat_index = row.index(column)
                        elif column.lower().startswith('longitude'):
                            lon_index = row.index(column)

                elif index == 1:
                    try:
                        lat, lon, alt = (
                            float(row[lat_index]),
                            float(row[lon_index]),
                            float(row[alt_index])
                            )
                        # Stores the starting point of the vector
                        initial_x, initial_y, initial_z = (
                            cartesian_conversion(lat, lon, alt)
                            )
                        x_list.append(0)
                        y_list.append(0)
                        z_list.append(0)
                    # Fails if the CSV file does not have proper header names
                    except NameError:
                        print(
                            'The file %s is not properly formatted for reading.'
                            % file
                            )
                        break

                else:
                    lat, lon, alt = (
                        float(row[lat_index]),
                        float(row[lon_index]),
                        float(row[alt_index])
                        )
                    x, y, z = cartesian_conversion(lat, lon, alt)

                    # Shifts entire vector to an origin point of (0, 0, 0)
                    this_x = x-initial_x
                    this_y = y-initial_y
                    this_z = z-initial_z

                    # Checks for smallest negative Cartesian coordinate value
                    if this_x < x_min:
                        x_min = this_x
                    if this_y < y_min:
                        y_min = this_y
                    if this_z < z_min:
                        z_min = this_z

                    x_list.append(this_x)
                    y_list.append(this_y)
                    z_list.append(this_z)

            # Normalizes the entire list of coordinates to the positive axes
            x_list = [i - x_min for i in x_list]
            y_list = [i - y_min for i in y_list]
            z_list = [i - z_min for i in z_list]

            # Writes coordinates into the target file
            cartesian_writer.writerow(['x', 'y', 'z'])
            for row in zip(x_list, y_list, z_list):
                cartesian_writer.writerow(row)

        # Deletes the target file if no coordinates were converted
        if not x_list:
            os.remove(dest_file)
        else:
            print('%s successfully converted into Cartesian coordinates.' % file)
            print('Displaying graph...\n')

            # Displays the graph of the resulting vector
            fig = plt.figure()
            fig.canvas.set_window_title(file)
            ax = fig.gca(projection='3d')
            ax.plot(x_list, [0]*len(x_list), [0]*len(x_list))
            ax.plot([0]*len(x_list), y_list, [0]*len(x_list))
            ax.plot([0]*len(x_list), [0]*len(x_list), z_list)
            ax.plot(x_list, y_list, z_list)
            plt.show()

#EoF