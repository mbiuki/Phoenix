#!/usr/bin/env python
'''
Mehdi Karimi
UBC Security Lab
August 4, 2018
This script automates our drone
simulations runs for number_of_missions
'''
from subprocess import call, Popen
import time
import os
import sys
import signal
import subprocess

number_of_missions= 30

for number in range(number_of_missions):
	print("----->mission number %d "% number)

	# sim = Popen('''source ~/.time.sh;
	# 	sim_vehicle.py -j4 --aircraft=$NOW --location=UBC -S 4''',
	# 	stdout=subprocess.PIPE,
	# 	shell=True,
	# 	executable='/bin/bash',
	# 	preexec_fn=os.setsid )

	# sim = Popen('''source ~/.time.sh;
	# sim_vehicle.py -j4 --aircraft=$NOW --location=Monash -S 4''',
	# stdout=subprocess.PIPE,
	# shell=True,
	# executable='/bin/bash',
	# preexec_fn=os.setsid )

	# sim = Popen('''source ~/.time.sh;
	# sim_vehicle.py -j4 --aircraft=$NOW --location=CMAC -S 4''',
	# stdout=subprocess.PIPE,
	# shell=True,
	# executable='/bin/bash',
	# preexec_fn=os.setsid )

	sim = Popen('''source ~/.time.sh;
	sim_vehicle.py -j4 --aircraft=$NOW --location=Snarbyeidet -S 4''',
	stdout=subprocess.PIPE,
	shell=True,
	executable='/bin/bash',
	preexec_fn=os.setsid )

	# sim = Popen('''source ~/.time.sh;
	# sim_vehicle.py -j4 --aircraft=$NOW --location=Carstensz -S 4''',
	# stdout=subprocess.PIPE,
	# shell=True,
	# executable='/bin/bash',
	# preexec_fn=os.setsid )
	

	print("*************AFTER SIM*************")

	# call(['python',  'simulate.py' , '--connect', '127.0.0.1:14550', '--WIND_DIR', '90','--WIND_SPD', '10'])
	call(['python',  'simulate.py' , '--connect', '127.0.0.1:14550'])
	os.killpg(os.getpgid(sim.pid), signal.SIGKILL)

	print("*************&&&&&&&KILLED&&&&&&&&*************")

print("============end of work ============")
sys.exit(0)