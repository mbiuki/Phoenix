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
args = parser.parse_args()

def wait_heartbeat(m):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))

def send_message(m):
    msg = m.recv_match(type='SYS_STATUS', blocking=True)
    if not msg:
        return
    if msg.get_type() == "BAD_DATA":
        if mavutil.all_printable(msg.data):
            print("Bad data")
            sys.stdout.write(msg.data)
            sys.stdout.flush()
    else:
        # Message is valid
        # m.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
        #                                   mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

        m.param_set_send("WP_RADIUS", 101, mavlink1.MAV_PARAM_TYPE_REAL32)
        m.param_set_send("COPTER_MODE", 0)
        # Use the attribute
        # print('Mode: %s' % msg.mode)
        print("Message sent")


# create a mavlink serial instance
master = mavutil.mavlink_connection(args.device, baud=args.baudrate, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
wait_heartbeat(master)
# master.reboot_autopilot()

count = 0
while True:
    message = master.recv_match()

    if message:
        # print(message)
        count += 1
        print(count)
    # send_message(master)
