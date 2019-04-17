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
    - using Pythagorean Theorem to plot the distance and their projections

Plotting using python in a 3d space:
- https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html

Steps:
- output to folders and to generalize 3 axes
- add normalization for 3 axes
- add plotting to both files

Requirements:
- matplotlib

## Input files go in samples folder
### Run generalization.py to get a graph on the axis x=y=z (don't use this, use the one below!)
### Run normalization.py to get a normalized graph (vector starts at (0, 0, 0) and goes in positive axes)

#EoF
