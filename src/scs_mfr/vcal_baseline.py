#!/usr/bin/env python3

"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset of the reported vCal value. A positive offset value
cause the output to be higher.

In normal circumstances, the vCal offset should be set so that the minimum vCal value for the given gas on the given
device matches the minimum vCal value in the model compendium.

IMPORTANT NOTE: the vCal baseline does not change the vCal value as reported by the gases_sampler utility. Instead,
it is used by the gas exegesis system, as part of the preprocessing of data that is passed to the interpretation
model.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the greengrass processes must be restarted for changes to take effect.

SYNOPSIS
vcal_baseline.py [{ -b GAS  | { { -s | -o } GAS VALUE [-r SAMPLE_REC -t SAMPLE_TEMP -m SAMPLE_HUMID] } | -d }] [-v]

EXAMPLES
./vcal_baseline.py -o NO2 -5

DOCUMENT EXAMPLE
{"NO2": {"calibrated-on": "2022-06-23T08:40:06Z", "offset": 134, "env": null}}

FILES
~/SCS/conf/baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/gas_model_conf
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.sensor_baseline import SensorBaseline, SensorBaselineSample

from scs_core.model.gas.vcal_baseline import VCalBaseline

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_vcal_baseline import CmdVCalBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    model = None
    primary = None

    now = LocalizedDatetime.now().utc()

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVCalBaseline()

    Logging.config('vcal_baseline', verbose=cmd.verbose)
    logger = Logging.getLogger()

    if not cmd.is_valid_sample_rec():
        logger.error("invalid format for sample rec.")
        exit(2)

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        baseline = VCalBaseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # sample...
        sample = SensorBaselineSample(cmd.sample_rec, cmd.sample_humid, cmd.sample_temp, None) if cmd.has_sample() \
            else None

        # update...
        if cmd.update():
            if cmd.offset and cmd.gas_name() not in baseline.gases:
                logger.error("gas '%s' not in baseline group." % cmd.gas_name())
                exit(2)

            old_offset = baseline.sensor_offset(cmd.gas_name())
            new_offset = int(round(old_offset + cmd.offset_value())) if cmd.offset else cmd.set_value()

            baseline.set_sensor_baseline(cmd.gas_name(), SensorBaseline(now, new_offset, sample=sample))
            baseline.save(Host)

            if cmd.verbose:
                logger.info("%s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset))

        # baseline...
        if cmd.baseline:
            gas_name = cmd.gas_name()
            sensor_baseline = baseline.sensor_baseline(gas_name)

            if sensor_baseline is None:
                logger.error("%s is not included in the calibration document." % gas_name)
                exit(1)

            baseline = VCalBaseline({gas_name: sensor_baseline})

        # delete...
        if cmd.delete:
            VCalBaseline.delete(Host)
            baseline = None

        # report...
        if baseline:
            print(JSONify.dumps(baseline, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)
