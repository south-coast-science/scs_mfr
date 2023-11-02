#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The rtc utility is used to set the real-time clock on the South Coast Science digital front-end (DFE) for
BeagleBone.

The real-time clock is not available on Raspberry Pi systems.

SYNOPSIS
rtc.py [-i] [-s] [-v]

EXAMPLES
./rtc.py -s

BUGS
In some operating system configurations, the real-time clock is under control of the operating system time module,
and therefore the user is not granted access.
"""

import sys

import tzlocal

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify
from scs_core.data.rtc_datetime import RTCDatetime

from scs_dfe.time.ds1338 import DS1338

from scs_host.bus.i2c import I2C

from scs_mfr.cmd.cmd_rtc import CmdRTC


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdRTC()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("rtc: %s" % cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    now = LocalizedDatetime.now()

    if cmd.verbose:
        print("rtc: system time: %s" % now, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        I2C.Sensors.open()

        if cmd.initialise:
            DS1338.init()

        if cmd.set:
            rtc_datetime = RTCDatetime.construct_from_localized_datetime(now)
            DS1338.set_time(rtc_datetime)

        # get current...
        rtc_datetime = DS1338.get_time()
        localized_datetime = rtc_datetime.as_localized_datetime(tzlocal.get_localzone())

        if cmd.verbose:
            print("rtc: datetime: %s" % localized_datetime, file=sys.stderr)
            sys.stderr.flush()

        print(JSONify.dumps(localized_datetime))

    finally:
        I2C.Sensors.close()
