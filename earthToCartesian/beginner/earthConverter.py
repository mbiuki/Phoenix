# Write a function(s) to turn the GPS and altitude variables 
# to the Cartesian x y z coordinates.
import math

# wgs84ToCartesian finds the XYZ coords based off wgs84 lat lon alt
# WGS https://en.wikipedia.org/wiki/World_Geodetic_System
# it takes 3 variables inp_altitude, inp_latitude, inp_longitude
# inp_altitude is a non negative float that is the altitudei n meters
# inp_latitude is a float that is the latitude in degrees
# inp_longitude is a float that is the longitude in degrees
# returns the x, y, z coordinates in meters, which are all floats
# for more information see the readme
def wgs84ToCartesian(inp_altitude, inp_latitude, inp_longitude):
	# altitude, latitude, longitude
	# must be converted from degrees into radians
	altitude = math.radians(inp_altitude)
	latitude = math.radians(inp_latitude)
	longitude = math.radians(inp_longitude)
	#""""""
	POLAR_SEMI_MAJOR_AXIS = 6356752.314245
	EQUITORIAL_SEMI_MINOR_AXIS = 6378137.0
	FLATTENING_FACTOR = 1 - EQUITORIAL_SEMI_MINOR_AXIS / POLAR_SEMI_MAJOR_AXIS
	ECCENTRICITY_SQUARED = 2 * FLATTENING_FACTOR - FLATTENING_FACTOR ** 2
	n_denom = math.sqrt(1 - ECCENTRICITY_SQUARED * math.sin(latitude) ** 2)
	r = POLAR_SEMI_MAJOR_AXIS / n_denom

	# math.cos and math.sin require radians, not degrees
	z = abs(((1 - ECCENTRICITY_SQUARED) * r + altitude) * math.sin(latitude))
	x = (r + altitude) * math.cos(latitude) * math.cos(longitude)
	y = (r + altitude) * math.cos(latitude) * math.sin(longitude)
	#"""

	# here's how to do it if you just assume a spherical earth
	# block comment the above to test
	"""
	RADIUS =  6378100
	x = (RADIUS + altitude) * math.cos(latitude) * math.cos(longitude)
	y = (RADIUS + altitude) * math.cos(latitude) * math.sin(longitude)
	z = abs(RADIUS + altitude) * math.sin(latitude)
	"""
	return x, y, z,
	
# Use these to test my function
# while True:
# 	inp = input("altitude, latitude, longitude: ").split(' ')
# 	print(wgs84ToCartesian(float(inp[0]), float(inp[1]), float(inp[2])))