#!/usr/bin/env python3

"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_conf utility is used to specify whether an Alphasense optical particle counter (OPC) is present and if so,
which model is attached. An option is also available to override the host's default SPI device file path for the OPC.

The specification also includes the number of seconds between readings by the OPC monitor sub-process. The maximum
time between readings is 10 seconds, the minimum five. A 10-second period provides the highest precision, but sampling
at this rate may be subject to clipping in extremely polluted environments.

The --restart-on-zeroes flag can be used to test the OPC in some situations, by overriding the default behaviour,
which is to restart the OPC if repeated zero readings are presented.

Flags are included to add or remove data interpretation exegetes, together with the source of T / rH readings.
Use of these is under development.

Sampling is performed by the scs_dev/particulates_sampler utility. If an opc_conf.json document is not present, the
scs_dev/particulates_sampler utility terminates.

Note that the scs_dev/particulates_sampler process must be restarted for changes to take effect.

The Alphasense OPC-N2, OPC-N3, OPC-R1, and Sensirion SPS30 models are supported.

Alternate exegetes (data interpretation models) can be added or removed - available interpretations can be listed with
the --help flag.

Note that, although support is provided for multiple named configurations, the configuration utility will only access
unnamed (solitary) configurations.

SYNOPSIS
opc_conf.py [-n NAME] [{ [-m MODEL] [-s SAMPLE_PERIOD] [-z { 0 | 1 }] [-p { 0 | 1 }] [-b BUS] [-a ADDRESS] | -d }] [-v]

EXAMPLES
./opc_conf.py -m S30 -b 1

DOCUMENT EXAMPLE
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false}

FILES
~/SCS/conf/opc_conf.json

SEE ALSO
scs_dev/particulates_sampler
scs_mfr/opc_cleaning_interval
scs_mfr/opc_version

REFERENCES
https://github.com/south-coast-science/scs_core/blob/develop/src/scs_core/particulate/exegesis/exegete_catalogue.py

BUGS
The specification allows for a power saving mode - which enables the OPC to shut down between readings - but
this is not currently implemented.
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_conf import CmdOPCConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    incompatibles = []

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("opc_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = OPCConf.load(Host, name=cmd.name)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("opc_conf: No configuration is stored - you must therefore set the required fields.",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        model = cmd.model if cmd.model else conf.model
        sample_period = cmd.sample_period if cmd.sample_period else conf.sample_period

        if conf is None:
            conf = OPCConf(None, 10, True, False, None, None)

        restart_on_zeroes = cmd.restart_on_zeroes if cmd.restart_on_zeroes is not None else conf.restart_on_zeroes
        power_saving = cmd.power_saving if cmd.power_saving is not None else conf.power_saving
        bus = conf.bus if cmd.bus is None else cmd.bus
        address = conf.address if cmd.address is None else cmd.address

        conf = OPCConf(model, sample_period, restart_on_zeroes, power_saving,
                       bus, address)

        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host, name=cmd.name)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
