#!/usr/bin/env python3

"""
Created on 11 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The set_hostname utility is used to set the hostname in /etc/hosts and /etc/hostname, given the supplied serial number.

The utility may only be run as root.

SYNOPSIS
set_hostname.py [-v] SERIAL_NUMBER

EXAMPLES
set_hostname 999

FILES
/etc/hostname
/etc/hosts
"""

import os
import sys

from scs_core.sys.hostname import Hostname
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_set_hostname import CmdSetHostname


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSetHostname()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('set_hostname', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # authentication...

        if os.geteuid() != 0:
            logger.error("you must have root privileges to set the hostname.")
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # validation...

        if not Hostname.is_valid_serial_number(cmd.serial_number):
            logger.error("the serial number '%s' is not valid." % cmd.serial_number)
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        hostname = Hostname(Host.hostname_prefix(), cmd.serial_number)

        try:
            hostname.set()
        except ValueError:
            logger.error("hosts and hostname files are out of sync - exiting.")
            exit(1)

        logger.error("hostname set to '%s'." % hostname.new_hostname)

    except KeyboardInterrupt:
        print(file=sys.stderr)
