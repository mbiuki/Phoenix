import math
import csv

def wgs84ToCartesian(inp_altitude, inp_latitude, inp_longitude):
	
	altitude = math.radians(inp_altitude)
	latitude = math.radians(inp_latitude)
	longitude = math.radians(inp_longitude)

	POLAR_SEMI_MAJOR_AXIS = 6356752.314245
	EQUITORIAL_SEMI_MINOR_AXIS = 6378137.0
	FLATTENING_FACTOR = 1 - EQUITORIAL_SEMI_MINOR_AXIS / POLAR_SEMI_MAJOR_AXIS
	ECCENTRICITY_SQUARED = 2 * FLATTENING_FACTOR - FLATTENING_FACTOR ** 2
	n_denom = math.sqrt(1 - ECCENTRICITY_SQUARED * math.sin(latitude) ** 2)
	r = POLAR_SEMI_MAJOR_AXIS / n_denom

	z = abs(((1 - ECCENTRICITY_SQUARED) * r + altitude) * math.sin(latitude))
	x = (r + altitude) * math.cos(latitude) * math.cos(longitude)
	y = (r + altitude) * math.cos(latitude) * math.sin(longitude)

	return x, y, z,

with open('wgs84 - 1.csv', 'r') as csvfile:
	wgs_reader = csv.reader(csvfile, delimiter=',')
	altlatlon = []
	first_row_flag = True
	for row in wgs_reader:
		if first_row_flag == True:
			first_row_flag = False
			continue
		index = row[0]
		coords = [float(cell) for cell in row[1:4]]
		altlatlon.append(wgs84ToCartesian(coords[0],coords[1],coords[2]))
title = ['X (meters)', 'Y (meters)', 'Z (meters)']
with open('xyzcoords.csv', 'w', newline='') as csvfile:
	xyzwriter = csv.writer(csvfile)
	xyzwriter.writerow(title)
	for li in altlatlon:
		xyzwriter.writerow(li)