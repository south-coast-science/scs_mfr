#!/usr/bin/env python3

"""
Created on 13 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_conf utility is used to inspect or update Alphasense OPC configuration variables. Alternative values can be
tested, then subsequently committed to the OPC's non-volatile memory.

SYNOPSIS
opc_firmware_conf.py [-n NAME] [{ -s FIELD VALUE | -f CONF_FILE }] [-c] [-v]

EXAMPLES
./opc_firmware_conf.py -v -s bin-weighting-index 2 -c

DOCUMENT EXAMPLE
{"bin-boundaries": [14, 40, 80, 120, 145, 215, 340, 590, 846, 1363, 2029, 2848, 4119, 5527, 7076, 8624, 10204, 11815,
13457, 15897, 18305, 20698, 22966, 25140, 27158],
"bin-boundaries-diameter": [35, 46, 66, 100, 130, 170, 230, 300, 400, 520, 650, 800, 1000, 1200, 1400, 1600, 1800,
2000, 2200, 2500, 2800, 3100, 3400, 3700, 4000],
"bin-weightings": [165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165,
165, 165, 165, 165, 165],
"pm-diameter-a": 100, "pm-diameter-b": 250, "pm-diameter-c": 1000, "max-tof": 4095,
"am-sampling-interval-count": 1, "am-middle-interval-count": 0, "am-max-data_arrays-in-file": 61798,
"am-only-save-pm-data": false, "am-fan-on-in-idle": false, "am-laser-on-in-idle": false,
"tof-to-sfr-factor": 56, "pvp": 48, "bin-weighting-index": 2}

SEE ALSO
scs_dev/particulates_sampler

scs_mfr/opc_cleaning_interval
scs_mfr/opc_conf
scs_mfr/opc_version

BUGS
Currently, the array fields 'bin-boundaries', 'bin-boundaries-diameter', and 'bin-weightings' cannot be updated.
"""

import json
import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_firmware_conf import CmdOPCFirmwareConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    opc = None
    firmware_conf = None
    jdict = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCFirmwareConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("opc_firmware_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # OPCConf...
        opc_conf = OPCConf.load(Host, name=cmd.name)

        if opc_conf is None:
            print("opc_firmware_conf: OPCConf not available.", file=sys.stderr)
            exit(1)

        # I2C...
        if opc_conf.uses_spi():
            I2C.Utilities.open()
        else:
            I2C.Sensors.open_for_bus(opc_conf.bus)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("opc_firmware_conf: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("opc_firmware_conf: Interface not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and interface:
            print("opc_firmware_conf: %s" % interface, file=sys.stderr)

        # OPC...
        opc = opc_conf.opc(interface, Host)

        if cmd.verbose:
            print("opc_firmware_conf: %s" % opc, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        opc.power_on()

        try:
            # get...
            firmware_conf = opc.get_firmware_conf()
        except NotImplementedError:
            print("opc_firmware_conf: OPC does not support firmware configuration.", file=sys.stderr)
            exit(1)

        if not firmware_conf:
            print("opc_firmware_conf: OPC not available", file=sys.stderr)
            exit(1)

        if cmd.set_field:
            # set...
            jdict = firmware_conf.as_json()

            if cmd.set_field not in jdict:
                print("opc_firmware_conf: field name '%s' is not valid." % cmd.set_field, file=sys.stderr)
                exit(2)

            jdict[cmd.set_field] = cmd.set_value

            try:
                # write...
                opc.set_firmware_conf(jdict)
            except NotImplementedError:
                print("opc_firmware_conf: OPC does not support firmware updates.", file=sys.stderr)
                exit(1)

            # re-read...
            firmware_conf = opc.get_firmware_conf()

        elif cmd.file:
            jstr = '{"bin-boundaries": [0, 27, 57, 95, 140, 205, 296, 473, 682, 920, 1184, 1473, 1786, 2123, 2481, ' \
                   '2861, 4095], "bin-boundaries-diameter": [0.35, 0.7, 1.1, 1.5, 1.9, 2.4, 3.0, 4.0, 5.0, 6.0, ' \
                   '7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 12.4], "bin-weightings": [1.65, 1.65, 1.65, 1.65, 1.65, 1.65, ' \
                   '1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65], "gain-scaling-coefficient": 1.0, ' \
                   '"sample-flow-rate": 3.7, "tof-to-sfr-factor": 87, "pm-concentration-a": 1.0, ' \
                   '"pm-concentration-b": 2.5, "pm-concentration-c": 10.0, "pvp": 48, "power-status": 0, ' \
                   '"max-tof": 4095, "laser-dac": 150, "bin-weighting-index": 2}'

            jdict = json.loads(jstr)

            opc.set_firmware_conf(jdict)

            # re-read...
            firmware_conf = opc.get_firmware_conf()

        if cmd.commit:
            # commit...
            opc.commit_firmware_conf()

        if firmware_conf:
            # report...
            print(JSONify.dumps(firmware_conf.as_json()))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        pass

    finally:
        if opc:
            opc.power_off()

        I2C.Sensors.close()
        I2C.Utilities.close()
