#!/usr/bin/env python

'''
test mavlink messages
'''
from __future__ import print_function
from pymavlink import mavutil
from argparse import ArgumentParser
from pymavlink.dialects.v10 import ardupilotmega as mavlink1
import sys

DISPLAY_MESSAGE = True

parser = ArgumentParser(description=__doc__)

parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=115200)
parser.add_argument("--device", required=True, help="serial device")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=255, help='MAVLink source system for this GCS')
parser.add_argument("--message", type=str, help="Choose from arm, disarm", required=True)
args = parser.parse_args()

def wait_heartbeat(m):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))

def send_message(master):
    if args.message is "arm":
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)

    # Disarm
    # master.arducopter_disarm() or:
        if args.message is "disarm":
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                0, 0, 0, 0, 0, 0, 0)

    # TODO: mode control
    # TODO: random message
    print("Mode sent")


# create a mavlink serial instance
master = mavutil.mavlink_connection(args.device, baud=args.baudrate, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
wait_heartbeat(master)
# master.reboot_autopilot()

count = 0
while True:
    send_message(master)
