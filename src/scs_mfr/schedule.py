#!/usr/bin/env python3

"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The schedule utility is used to set timing and averaging specifications for environmental sampling and device status
reporting.

The configuration file generated by the schedule utility contains fields that name Unix semaphores that
will be used to communicate with each sampler process. By convention, these are:

* scs-climate
* scs-gases
* scs-particulates
* scs-status

The schedule interval is the period between sampling operations in seconds. The minimum is one second. The tally
represents the number of samples between reporting operations. If the tally is greater than 1, reports contain
averaged data.

Note that the ssc_dev_/scheduler process must be restarted for changes to take effect.

SYNOPSIS
schedule.py [{-s NAME INTERVAL TALLY | -d NAME }] [-v]

EXAMPLES
./schedule.py -s scs-climate 10.0 1

DOCUMENT EXAMPLE
{"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}

FILES
~/SCS/conf/schedule.json

SEE ALSO
scs_dev/scheduler

BUGS
Currently, averaging is not available. The tally should therefore be set to 1.
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sync.schedule import Schedule
from scs_core.sync.schedule import ScheduleItem

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_schedule import CmdSchedule


# TODO: check sampling interval against OPCConf

# TODO: implement tally / averaging functionality on sampling processes

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSchedule()

    if cmd.verbose:
        print("schedule: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    schedule = Schedule.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        item = ScheduleItem(cmd.name, cmd.interval, cmd.count)

        # if not item.is_valid():
        #     print("Item is not valid: %s" % item)
        #     exit(1)

        schedule.set(item)
        schedule.save(Host)

    if cmd.delete():
        schedule.clear(cmd.name)
        schedule.save(Host)

    print(JSONify.dumps(schedule))
