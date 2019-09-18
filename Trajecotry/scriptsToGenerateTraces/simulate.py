#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mehdi Karimi
August 4, 2018
UBC Security Lab
Simulate the drone to 
takeoff 20 and go to a destination
"""

import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import math

# Set up option parsing to get connection string
import argparse

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. \
                    If not specified, SITL automatically started and used.")
# parser.add_argument('--WIND_DIR',
#                     help="Wind direction from north. \
#                     If not specified, pass zero.")
# parser.add_argument('--WIND_SPD',
#                     help="Wind speed. \
#                     If not specified, pass zero.")
args = parser.parse_args()

connection_string = args.connect
# wind_speed = args.WIND_SPD
# wind_dir = args.WIND_DIR


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def guidedToWaypoints(point):
    global vehicle
    poitionDiff = calculateGlobalDistance(vehicle.location.global_relative_frame.lat, 
        vehicle.location.global_relative_frame.lon,
        point.lat, point.lon)

    vehicle.simple_goto(point)
    while poitionDiff >= 1:
        poitionDiff = calculateGlobalDistance(vehicle.location.global_relative_frame.lat, 
            vehicle.location.global_relative_frame.lon,
            point.lat,
            point.lon)
        time.sleep(0.3)
        # print("Distance from Position: %s %s is: %s" % (
        #             vehicle.location.global_relative_frame.lat, 
        #             vehicle.location.global_relative_frame.lon, poitionDiff))
    print("Reached Position %s %s" % (point.lat, point.lon))

def calculateGlobalDistance(lat1, lon1, lat2, lon2):
    R = 6378.137  # earth raiud
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = \
    math.sin(dLat / 2) * math.sin(dLat / 2) + \
     math.cos(lat1 * math.pi / 180) * math.cos( \
        lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c;
    return d * 1000;  # meters

arm_and_takeoff(20)

# vehicle.airspeed = 3

print("Going towards destination...")

'''
==== Destinations ====


'''
# UBC Detour
# guidedToWaypoints(LocationGlobalRelative(49.257257,-123.242463, 20))
# UBC
# guidedToWaypoints(LocationGlobalRelative(49.256881, -123.241939, 20))

# Monash
# guidedToWaypoints(LocationGlobalRelative(-37.911437, 145.140270, 20))

# CMAC
# guidedToWaypoints(LocationGlobalRelative(-35.36188901,149.165221801, 20))

# Snarbyeidet
guidedToWaypoints(LocationGlobalRelative(69.75661,19.558415, 20))

# Carstensz
# guidedToWaypoints(LocationGlobalRelative(-35.331200, 149.129543, 20))
############################################################################

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
#EoF