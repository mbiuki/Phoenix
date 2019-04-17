'''
This program converts earth coordinates to cartesian
'''
import sys
import math
import csv
import numpy as np

path = ''
with open('cartesian.csv', mode='w', newline='') as outfile:
 employee_writer = csv.writer( outfile, delimiter=',')

 employee_writer.writerow(['X', 'Y', 'Z'])  
 with open( path +"20180925_112643.csv", "r") as file:
    reader = csv.reader(file)
    for idx,row in enumerate(reader):
        if idx>0:
             # print(row)
             f  =  np.float64(1.0/298.257223563) # flattening
             ls = math.atan((1.0 - f)**2 * math.tan(np.float64(row[2]))) # lambda
             rad = np.float64(6378137.0)
             C = 1/np.sqrt(math.cos(np.float64(row[2]))**2 + ls * \
             								math.sin(np.float64(row[2]))**2)
             S = C * ls
             x = rad * math.cos(ls) * math.cos(np.float64(row[3])) + \
             			np.float64(row[1]) * math.cos(np.float64(row[2])) * \
             							 math.cos(np.float64(row[3]))
             # print(x)
             y = rad * math.sin(float(row[3])) * math.sin(float(row[2]))
             # print(y)
             z = rad *  math.cos(float(row[2]))
             # print(z)
             employee_writer.writerow([x, y, z])
#EoF
