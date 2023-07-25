#!/usr/bin/env python3

"""
Created on 22 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The display_conf utility is used to specify the content of a visual display, such as the Pimoroni Inky pHAT eInk
module. In particular, it specifies some of the initial screen content.

The configuration managed by this utility is used by the scs_dev/display utility.

SYNOPSIS
display_conf.py [{ [-m MODE] [-n NAME] [-u STARTUP] [-s SHUTDOWN] [-t { 0 | 1 }] | -d }] [-v]

EXAMPLES
./display_conf.py -m SYS -n "SCS Praxis/Handheld v1.0" -u RUNNING -s STANDBY -t 1

DOCUMENT EXAMPLE
{"mode": "SYS", "device-name": "SCS Praxis/Handheld (dev)", "startup-message": "ON", "shutdown-message": "STANDBY",
"show-time": true}

FILES
~/SCS/conf/display_conf.json

SEE ALSO
scs_dev/display
"""

import sys

from scs_core.data.json import JSONify
from scs_core.display.display_conf import DisplayConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_display_conf import CmdDisplayConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    conf = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDisplayConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("display_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DisplayConf...
    try:
        conf = DisplayConf.load(Host)

    except NotImplementedError:
        print("display_conf: not available.", file=sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if conf is None and cmd.set() and not cmd.is_complete():
        print("display_conf: No configuration is stored - you must therefore set all fields.", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        mode = cmd.mode if cmd.mode is not None else conf.mode

        device_name = cmd.device_name if cmd.device_name is not None else conf.device_name
        startup_message = cmd.startup_message if cmd.startup_message is not None else conf.startup_message
        shutdown_message = cmd.shutdown_message if cmd.shutdown_message is not None else conf.shutdown_message

        show_time = cmd.show_time if cmd.show_time is not None else conf.show_time

        conf = DisplayConf(mode, device_name, startup_message, shutdown_message, show_time)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
