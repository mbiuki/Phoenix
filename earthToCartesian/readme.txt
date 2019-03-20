workflow
Refer to World Geodetic System 1984 (WGS84)
----------------------------------------------
The formulas for WGS-84 to Cartesian: 
https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates

The values for equatorial radius and polar radius: 
https://en.wikipedia.org/wiki/Earth_radius#/media/File:WGS84_mean_Earth_radius.svg

The math and cvs portions:
https://docs.python.org/3/library/math.html 
https://docs.python.org/3/library/csv.html 

The check for file line:
https://therenegadecoder.com/code/how-to-check-if-a-file-exists-in-python/ 

The calculations were compared with an online convertor:
http://www.apsalin.com/convert-geodetic-to-cartesian.aspx 

Actions:
- modify output to multiple files
- Generalized data by:
    - Using Pythagorean Theorem to get the distance travelled between each point
    - using Pythagorean Theorem to plot the distance on a 45 degree line
