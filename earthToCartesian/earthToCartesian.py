'''
UBC Security of IoT Lab
March 2019
Mehdi Karimi
Description: 
Function generalization
drop all trajectories on to a single line
'''
import os
import math
import csv
import matplotlib.pyplot as plt
import earthConverter

# MACROS
num_of_csv = 3

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

def generalize(row):
	'''
	generalize each row
	:param row:
	:return:
	'''
	global prev_row, prev_row_general
	#calculate distance travelled between two points
	a = row[0] - prev_row[0]
	b = row[1] - prev_row[1]
	length = math.sqrt(a ** 2 + b ** 2)
	#plot distance on 45 degree line
	increment = math.sqrt(length ** 2 / 2)
	row_generalized = [x + increment for x in prev_row_general]

	prev_row = row
	prev_row_general = row_generalized

	return row_generalized

if __name__ == "__main__":

	#convert coords to cartesion
	earthConverter.convert()

	#create list of csv files with _cartesian
	files = [f for f in os.listdir() if os.path.isfile(f)]
	csv_files = [f for f in files if '_cartesian.csv' in f]

	for file in csv_files:

		#variables
		prev_row = [0, 0]
		prev_row_general = [0, 0]

		#name output file
		file_split = os.path.splitext(file)
		output_file = file_split[0] + '_generalized' + file_split[1]

		#check if file exists, and remove if it does
		if os.path.isfile(output_file):

			os.remove(output_file)

		#opens new file and writes header
		output_csv = open(output_file, 'w', newline = '')
		csv.writer(output_csv).writerow(['x', 'y'])

		#open csv
		with open(file, newline = '') as csv_file:

			csvreader = csv.reader(csv_file)

			#skip first line
			next(csvreader)

			#parse csv
			for row in csvreader:
				#set prev_row if first line of data
				if csvreader.line_num == 2:
					prev_row = [float(x) for x in row]
				#generalize and write to file
				csv.writer(output_csv).writerow(generalize([float(row[0]), float(row[1])]))