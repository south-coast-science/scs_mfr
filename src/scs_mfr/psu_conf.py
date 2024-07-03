#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The psu_conf utility is used to specify whether a South Coast Science power supply (PSU) board is present
and if so, which model is provided. Three models are currently available:

* MobileV1 - I2C - PZHBt1 or PZHBt2 interface
* MobileV2 - I2C - PZHBt1 or PZHBt2 interface
* OPCubeV1 - I2C - charger is PCA9534A at 0x38
* OPCubeV1.1 - I2C - charger is PCA9849 at 0x20
* OsloV1 - serial port
* PrototypeV1 - serial port

A battery pack may also be specified. A warning is given if a battery is specified for a PSU that does not use one,
or if a battery is not specified for one that does.

Note that the scs_dev/psu_monitor process must be restarted for changes to take effect.

SYNOPSIS
psu_conf.py { [-p PSU_MODEL] [-b BATT_MODEL] [-t { 0 | 1 }] [-i REPORTING_INTERVAL] [-f REPORT_FILE] | -d } [-v]

EXAMPLES
./psu_conf.py -m OsloV1 -i 10 -f /dev/shm/southcoastscience/psu_status_report.json

DOCUMENT EXAMPLE
{"model": "MobileV2", "batt-model": "PackV1", "ignore-threshold": true, "reporting-interval": 10,
"report-file": "/dev/shm/southcoastscience/psu_status_report.json"}

FILES
~/SCS/conf/psu_conf.json

SEE ALSO
scs_mfr/fuel_gauge_calib
scs_dev/psu
scs_dev/psu_monitor
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_psu_conf import CmdPSUConf

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdPSUConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("psu_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PSUConf...
    conf = PSUConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        psu_model = cmd.psu_model if cmd.psu_model is not None else conf.psu_model
        batt_model = cmd.batt_model if cmd.batt_model is not None else conf.batt_model
        ignore_threshold = cmd.ignore_threshold if cmd.ignore_threshold is not None else conf.ignore_threshold
        reporting_interval = cmd.reporting_interval if cmd.reporting_interval is not None else conf.reporting_interval
        report_file = cmd.report_file if cmd.report_file is not None else conf.report_file

        try:
            conf = PSUConf(psu_model, batt_model, ignore_threshold, reporting_interval, report_file)
        except ValueError as ex:
            print("psu_conf: %s" % ex, file=sys.stderr)

        psu_class = conf.psu_class()
        psu_uses_batt_pack = psu_class.uses_batt_pack()

        if batt_model is None and psu_uses_batt_pack:
            print("psu_conf: WARNING: %s uses a battery pack but none was specified" % psu_model, file=sys.stderr)

        if batt_model is not None and not psu_uses_batt_pack:
            print("psu_conf: WARNING: %s does not use a battery pack but %s was specified" % (psu_model, batt_model),
                  file=sys.stderr)

        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
