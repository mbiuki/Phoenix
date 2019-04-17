'''
UBC Security of IoT Lab
March 2019
Mehdi Karimi
Description:
Convert Earth Coordinates to Cartesian
'''

import math


def cartesian_conversion(lat, lon, alt):
    lat = math.radians(lat)
    lon = math.radians(lon)

    # a in metres, see: https://en.wikipedia.org/wiki/Earth_radius
    equatorial_radius = 6378137.0
    # b in metres, see: https://en.wikipedia.org/wiki/Earth_radius
    polar_radius = 6356752.3
    ellipsoid_squared = (1.0
                         - (polar_radius**2 / equatorial_radius**2)
                         )
    radius_of_curvature = (equatorial_radius
                           / math.sqrt(
                                 1.0 - (ellipsoid_squared * (math.sin(lat)**2))
                                 )
                           )

    cartesian_x = (radius_of_curvature+alt) * math.cos(lat) * math.cos(lon)
    cartesian_y = (radius_of_curvature+alt) * math.cos(lat) * math.sin(lon)
    cartesian_z = (((polar_radius**2/equatorial_radius**2)
                   * radius_of_curvature + alt)
                   * math.sin(lat)
                   )

    return (cartesian_x, cartesian_y, cartesian_z)
