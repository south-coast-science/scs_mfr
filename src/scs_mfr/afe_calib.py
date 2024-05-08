#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_calib utility is used to retrieve or install the calibration sheet for the Alphasense analogue front-end (AFE)
board or single sensor installed on the host system.

Alphasense electrochemical sensors are calibrated in the factory when fitted to their AFE board, or individually.
The calibration values are provided in a structured document, either on paper or - for sensors provided by South Coast
Science - in electronic form. The afe_calib utility is used to retrieve this JSON document via a web API.

The --pid-test-sens flag is used to correct the sensitivity of PID sensors, based on the result of a bump test.
Prior to the bump test, sensor should have its zero offset set to the match the ambient VOC concentration.
The afe_baseline utility should be set once more, following the sensitivity correction.

The afe_calib utility may also be used to set a "test" calibration sheet, for use in an R & D environment.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_calib.py [{ -f SERIAL_NUMBER | -a SERIAL_NUMBER | -s SERIAL_NUMBER YYYY-MM-DD | -r | -p CORRECT REPORTED |
-t  | -d }] [-i INDENT] [-v]

EXAMPLES
./afe_calib.py -vi4 -s 143800348 2023-03-01

./afe_calib.py -vi4 -p 14000 12000

DOCUMENT EXAMPLE
{"serial_number": null, "type": "DSI", "calibrated_on": "2024-01-01", "dispatched_on": null, "pt1000_v20": null,
"sn1": {"serial_number": "143351067", "sensor_type": "PIDH2", "pid_zero_mv": null, "pid_sensitivity_mv_ppm": 44.9,
"bump-calib": {"sensitivity": 0.857, "calibrated-on": "2024-01-05T13:16:04Z"}}}

FILES
~/SCS/conf/afe_calib.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_baseline

RESOURCES
https://calibration.southcoastscience.com/
"""

import json
import sys

from scs_core.client.http_exception import HTTPException

from scs_core.data.datetime import Date, LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.dsi_calib import DSICalib
from scs_core.gas.pid.pid import PID
from scs_core.gas.pid.pid_calib import PIDTestCalib

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    calib = None
    calibrated_on = None
    we_sens_mv = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFECalib()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('afe_calib', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        calib = AFECalib.load(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.find_serial_number:
            if '-' in cmd.find_serial_number:
                calib = AFECalib.download(cmd.find_serial_number, parse=False)
            else:
                calib = DSICalib.download(cmd.find_serial_number, parse=False)

        if cmd.set():
            if cmd.afe_serial_number is not None:
                calib = AFECalib.download(cmd.afe_serial_number)

            else:
                calib = DSICalib.download(cmd.sensor_serial_number)

                if not Date.is_valid_iso_format(cmd.sensor_calibration_date_str):
                    logger.error("invalid ISO date: '%s'." % cmd.sensor_calibration_date_str)
                    exit(2)

                calib.calibrated_on = cmd.sensor_calibration_date

        if cmd.reload:
            if calib is None:
                logger.error("No AFECalib found.")
                exit(1)

            if calib.afe_type == DSICalib.TYPE:
                calibrated_on = calib.calibrated_on
                calib = DSICalib.download(calib.sensor_calib(0).serial_number)
                calib.calibrated_on = calibrated_on

            else:
                calib = AFECalib.download(calib.serial_number)

        if cmd.pid_test_correct:
            index = calib.sensor_index('VOC')

            if index is None:
                logger.error('PID not present.')
                exit(1)

            sensitivity = PID.sensitivity(cmd.pid_test_correct, cmd.pid_test_reported)

            sensor_calib = calib.sensor_calib(index)
            sensor_calib.bump_calib = PIDTestCalib(sensitivity, LocalizedDatetime.now())

        if cmd.test:
            jdict = json.loads(AFECalib.TEST_LOAD)
            calib = AFECalib.construct_from_jdict(jdict)

        if cmd.update():
            calib.save(Host)

        elif cmd.delete:
            AFECalib.delete(Host)
            calib = None

        if calib:
            print(JSONify.dumps(calib, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ValueError as ex:                        # incorrect sensitivity found in calibration document
        logger.error(str(ex) + ':')
        logger.error(JSONify.dumps(calib))
        exit(1)

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except HTTPException as ex:
        logger.error(ex.error_report)
        exit(1)

    except Exception as ex:
        logger.error(ex.__class__.__name__)
        exit(1)
