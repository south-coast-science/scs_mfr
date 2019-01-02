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

Note that, currently, only the u-blox PAM7Q GPS module is supported.

SYNOPSIS
gps_conf.py [{ [-m MODEL] [-i INTERVAL] [-t TALLY] | -d }] [-v]

EXAMPLES
./gps_conf.py -m PAM7Q -i 10 -t 60

DOCUMENT EXAMPLE
{"model": "PAM7Q", "sample-interval": 10, "tally": 60}

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
    # resources...

    # GPSConf...
    conf = GPSConf.load(Host)


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
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("gps_conf: No configuration is stored. You must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        interval = cmd.sample_interval if cmd.sample_interval else conf.sample_interval
        tally = cmd.tally if cmd.tally is not None else conf.tally

        conf = GPSConf(model, interval, tally)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
