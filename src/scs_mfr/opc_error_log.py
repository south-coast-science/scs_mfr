#!/usr/bin/env python3

"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_error_log utility is used to view, trim or delete the OPC error log.

SYNOPSIS
opc_error_log.py [{ -t | -d }] [-i INDENT] [-v]

EXAMPLES
./opc_error_log.py -v | node.py -vs

DOCUMENT EXAMPLE
[{"rec": "2024-01-10T11:55:45Z", "cause": "checksum error"}]

FILES
~/SCS/log/opc_error_log.csv

SEE ALSO
scs_dev/particulates_sampler
"""

import sys

from scs_core.data.json import JSONify
from scs_core.particulate.opc_error_log import OPCErrorLog
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_error_log import CmdOPCErrorLog


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCErrorLog()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('opc_error_log', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.trim:
        OPCErrorLog.trim(Host, OPCErrorLog.max_permitted_entries())
        log = OPCErrorLog.load(Host)

    elif cmd.delete:
        OPCErrorLog.delete(Host)
        log = None

    else:
        log = OPCErrorLog.load(Host)

    if log:
        print(JSONify.dumps(log, indent=cmd.indent))
        logger.info("rows: %s" % len(log))
