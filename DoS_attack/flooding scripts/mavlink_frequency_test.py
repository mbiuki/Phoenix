#!/usr/bin/env python

"""
Generate a message using different MAVLink versions, put in a buffer and then read from it.
Sourced from https://github.com/ArduPilot/pymavlink/blob/master/examples/mavtest.py
"""

from __future__ import print_function

import time

from builtins import object

import pymavlink
print(pymavlink.__file__)

from pymavlink.dialects.v10 import ardupilotmega as mavlink1
from pymavlink.dialects.v20 import ardupilotmega as mavlink2

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument("--mavlink_type", default= 1, help="type 1 or 2 for mavlink v1.0 or v2.0", type=int)
parser.add_argument("--signed", default= 0, help= "type 1 or 0 for using secured mode for mavlink v2.0 or not", type=int)
parser.add_argument("--num_msg", default=1000, type=int)
args = parser.parse_args()

DISPLAY_MESSAGE = False

NUM_ITERATION = args.num_msg

class fifo(object):
    def __init__(self):
        self.buf = []
    def write(self, data):
        self.buf += data
        return len(data)
    def read(self):
        return self.buf.pop(0)

def test_protocol(mavlink, signing=args.signed):
    # we will use a fifo as an encode/decode buffer
    f = fifo()
    if DISPLAY_MESSAGE:
        print("Creating MAVLink message...")
    # create a mavlink instance, which will do IO on file object 'f'
    mav = mavlink.MAVLink(f)

    if signing:
        mav.signing.secret_key = chr(42)*32
        mav.signing.link_id = 0
        mav.signing.timestamp = 0
        mav.signing.sign_outgoing = True

    # set the WP_RADIUS parameter on the MAV at the end of the link
    mav.param_set_send(7, 1, "WP_RADIUS", 101, mavlink.MAV_PARAM_TYPE_REAL32)

    # alternatively, produce a MAVLink_param_set object
    # this can be sent via your own transport if you like
    m = mav.param_set_encode(7, 1, "WP_RADIUS", 101, mavlink.MAV_PARAM_TYPE_REAL32)

    m.pack(mav)

    # get the encoded message as a buffer
    b = m.get_msgbuf()

    bi=[]
    for c in b:
        bi.append(int(c))
    if DISPLAY_MESSAGE:
        print("Buffer containing the encoded message:")
        print(bi)

        print("Decoding message...")
    # decode an incoming message
    m2 = mav.decode(b)

    # show what fields it has
    if DISPLAY_MESSAGE:
        print("Got a message with id %u and fields %s" % (m2.get_msgId(), m2.get_fieldnames()))

        # print out the fields
        print(m2)


print("START: total of %d iterations" % NUM_ITERATION)
start_time = time.time()

for i in range(1, NUM_ITERATION):
    if args.mavlink_type == 1:
        test_protocol(mavlink1)
    else:
        test_protocol(mavlink2, True if args.signed == 1 else False)

end_time = time.time()

print("FINISHED: complete with %f seconds / %d message" % (end_time - start_time, NUM_ITERATION))
print("Locally transfer with average of %f seconds/messages" % ((end_time - start_time)/(1.0 *NUM_ITERATION)))
