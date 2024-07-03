#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gps_conf utility is used to specify whether a GPS receiver module is present and if so, which model is provided.
It also specifies the interval between samples of the GPS location, and the number of samples to be averaged.

The PAM7Q module provides a report every two seconds, but a sample interval of 10 seconds is usually appropriate. The
averaging tally depends on the mode of use of the device: for a fixed device, 10 minutes (60 samples) is effective in
rejecting "quality 0" readings, whereas a mobile device requires a tally of 1.

The u-blox PAM-7Q and SAM-M8Q GPS modules are supported.

The REPORT_FILE parameter, if set, indicates where the latest queue length value should be stored.

The status_sampler must be restarted for changes to take effect.

SYNOPSIS
gps_conf.py [{ [-m MODEL] [-i INTERVAL] [-t TALLY] [-f REPORT_FILE] [-l { 0 | 1 }] | -d }] [-v]

EXAMPLES
./gps_conf.py -m SAM8Q -i 10 -t 60 -f /dev/shm/southcoastscience/gps_report.json -l 1

DOCUMENT EXAMPLE
{"model": "PAM7Q", "sample-interval": 10, "tally": 1, "report-file": "/dev/shm/southcoastscience/gps_report.json",
"debug": true}

FILES
~/SCS/conf/gps_conf.json

SEE ALSO
scs_dev/status_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gps.gps_conf import GPSConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_gps_conf import CmdGPSConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdGPSConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("gps_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GPSConf...
    conf = GPSConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("gps_conf: No configuration is stored - you must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        conf_report_file = None if conf is None else conf.report_file

        model = cmd.model if cmd.model else conf.model
        interval = cmd.sample_interval if cmd.sample_interval else conf.sample_interval
        tally = cmd.tally if cmd.tally is not None else conf.tally
        report_file = cmd.report_file if cmd.report_file is not None else conf_report_file
        debug = cmd.debug if cmd.debug is not None else conf.debug

        conf = GPSConf(model, interval, tally, report_file, debug)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
