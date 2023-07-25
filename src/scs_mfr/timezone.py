#!/usr/bin/env python3

"""
Created on 12 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The timezone utility is used to specify the timezone in which a sensing device is operating. The timezone set here is
reported by the scs_dev/status_sampler utility.

Typically, the operating system of the device is set to UTC. Environmental sensing documents always include an ISO 8601
localised date / time, and this localised date / time is set to the timezone of the operating system.

All time zones specified by the Internet Assigned Numbers Authority (IANA) are available.

Note that the scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
timezone.py [{ -z | -s TIMEZONE_NAME | - l }] [-v]

EXAMPLES
./timezone.py -s Europe/London -v

DOCUMENT EXAMPLE
{"set-on": "2017-08-14T14:25:29.794+00:00", "name": "Europe/London"}

FILES
~/SCS/conf/timezone.conf

SEE ALSO
scs_dev/status_sampler

RESOURCES
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.location.timezone import Timezone
from scs_core.location.timezone_conf import TimezoneConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_timezone import CmdTimezone


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdTimezone()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("timezone: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    conf = TimezoneConf.load(Host, skeleton=True)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    now = LocalizedDatetime.now()

    if cmd.list:
        for zone in Timezone.zones():
            print(zone, file=sys.stderr)
        exit(0)

    elif cmd.set():
        if not Timezone.is_valid(cmd.zone):
            print("timezone: unrecognised name: %s" % cmd.zone, file=sys.stderr)
            exit(2)

        if cmd.zone != conf.name:
            conf = TimezoneConf(now, cmd.zone)
            conf.save(Host)

    elif cmd.link:
        if not conf.uses_system_name() or conf.set_on is None:
            conf = TimezoneConf(now, None)
            conf.save(Host)

    print(JSONify.dumps(conf))

    if cmd.verbose:
        print(JSONify.dumps(conf.timezone()), file=sys.stderr)
