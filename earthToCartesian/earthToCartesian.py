'''
UBC Security of IoT Lab
March 2019
Mehdi Karimi
Description: 
Function generalization
Convert Earth Coordinates to Cartesian
'''
import math
import csv
import matplotlib.pyplot as plt

# MACROS
num_of_csv = 3

def wgs84ToCartesian(inp_altitude, inp_latitude, inp_longitude):
	'''
	main conversion method
	:param inp_altitude: altitude of the drone
	:param inp_latitude: latitude of the drone
	:param inp_longitude: longitude of the drone
	:return:
	'''
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

def make_xyzcoords():
	'''
	callout the conversion
	automatically read the csv files and do the conversion
	:return:
	'''
	for i in range(1, num_of_csv + 1):
		with open('%d_earthwgs84.csv'%i, 'r') as csvfile:
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
		with open('%d_xyzcoords.csv'%i, 'w', newline='') as csvfile:
			xyzwriter = csv.writer(csvfile)
			xyzwriter.writerow(title)
			for li in altlatlon:
				xyzwriter.writerow(li)

def make_graph():
	'''
	make the nice graph
	:return:
	'''
	toplot = dict()
	for i in range(1, num_of_csv + 1):
		with open('%d_xyzcoords.csv'%i, 'r') as csvfile:
			wgs_reader = csv.reader(csvfile, delimiter=',')
			first_row_flag = True
			x = []
			y = []
			for row in wgs_reader:
				if first_row_flag == True:
					first_row_flag = False
					continue
				x.append(float(row[0]))
				y.append(float(row[1]))
			x, y = zip(*sorted(zip(x, y)))

			distance =  math.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
			toplot[i] = distance

	toplot = sorted(toplot.items(), key=lambda kv: kv[1])[::-1]
	print(toplot)
	for l in toplot:
		point = [0, l[1]]
		plt.plot(point,point, label=l[0])
	plt.xlim(left=0.0)
	plt.ylim(bottom=0.0)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('X and Y on a Single Line')
	plt.legend()
	plt.show()

if __name__ == "__main__":
	make_xyzcoords()
	make_graph()