#!/usr/bin/env python3

"""
Created on 29 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The configuration utility is used to marshal all of the device configuration settings into a single JSON document.
It is intended to be used as one component of a centralised estate management system.

The utility can be used to update a setting on the device. To do this, a JSON document containing at least one field
of the configuration document must be supplied on the command line. Any fields that are not named will not be updated.

Note that the hostname field cannot be updated by the configuration utility. If this field is included in the
update JSON specification, it is silently ignored.

SYNOPSIS
configuration.py [-s CONFIGURATION] [-x] [{ -i INDENT | -t }] [-v]

EXAMPLES
./configuration.py -i4 -s '{"timezone-conf": {"name": "Europe/London"}}'

DOCUMENT EXAMPLE
{
    "rec": "2024-04-04T09:28:16Z",
    "tag": "scs-be2-3",
    "ver": 1.4,
    "val": {
        "hostname": "scs-bbe-003",
        "platform": {
            "os": "10.13",
            "kernel": "6.1.77-bone30"
        },
        "packs": {
            "scs_comms": {
                "repo": "scs_comms_ge910",
                "version": null
            },
            "scs_core": {
                "repo": "scs_core",
                "version": "3.11.2"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "3.4.5"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "3.2.2"
            },
            "scs_exegesis": {
                "repo": "scs_exegesis",
                "version": null
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.5.0"
            },
            "scs_host": {
                "repo": "scs_host_bbe_southern",
                "version": "3.5.2"
            },
            "scs_inference": {
                "repo": "scs_inference",
                "version": null
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "3.8.11"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "2.6.2"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn2": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn3": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn4": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            }
        },
        "afe-id": {
            "serial_number": "26-000345",
            "type": "810-0023-01",
            "calibrated_on": "2020-11-18",
            "sn1": {
                "serial_number": "212632052",
                "sensor_type": "NO2A43F"
            },
            "sn2": {
                "serial_number": "214250436",
                "sensor_type": "OXA431"
            },
            "sn3": {
                "serial_number": "130631043",
                "sensor_type": "NO A4"
            },
            "sn4": {
                "serial_number": "134200204",
                "sensor_type": "SO2A4"
            }
        },
        "aws-group-config": {
            "group-name": "scs-bbe-003-group",
            "time-initiated": "2024-03-07T12:45:28Z",
            "unix-group": 987,
            "ml": "uE.1"
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/development/loc/1",
            "device-path": "south-coast-science-dev/development/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "is-available": true,
            "on-root": false,
            "used": 6
        },
        "display-conf": null,
        "vcal-baseline": null,
        "gas-baseline": null,
        "gas-model-conf": null,
        "gps-conf": {
            "model": "SAM8Q",
            "sample-interval": 10,
            "tally": 60,
            "debug": false
        },
        "interface-conf": {
            "model": "DFE"
        },
        "mpl115a2-calib": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177050912",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "opc-errors": 8,
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2",
            "model-map": "uE.1"
        },
        "pressure-conf": null,
        "psu-conf": {
            "model": "OsloV1",
            "batt-model": null,
            "ignore-threshold": false,
            "reporting-interval": 10,
        },
        "psu-version": {
            "id": "South Coast Science PSU Oslo",
            "tag": "2.2.5"
        },
        "scd30-baseline": null,
        "scd30-conf": null,
        "schedule": {
            "scs-climate": {
                "interval": 60.0,
                "tally": 1
            },
            "scs-gases": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-particulates": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-status": {
                "interval": 60.0,
                "tally": 1
            }
        },
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "modem": {
            "id": "992c3ac6da0b68d58005d20ea5e957d409001e42",
            "imei": "860425041573914",
            "mfr": "QUALCOMM INCORPORATED",
            "rev": "XXX"
        },
        "sim": {
            "imsi": "234301951432537",
            "iccid": "8944303382697124823",
            "operator-code": "23430",
            "operator-name": "EE"
        },
        "system-id": {
            "set-on": "2024-01-09T16:02:09Z",
            "vendor-id": "SCS",
            "model-id": "BE2",
            "model": "Alpha BB Eng",
            "config": "V2",
            "system-sn": 3
        },
        "timezone-conf": {
            "set-on": "2017-08-15T12:50:05Z",
            "name": "Europe/London"
        }
    }
}

SEE ALSO
scs_mfr/modem
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.configuration import Configuration

from scs_core.psu.psu_version import PSUVersion

from scs_core.sample.configuration_sample import ConfigurationSample

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.lock.lock_timeout import LockTimeout
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_configuration import CmdConfiguration

try:
    from scs_psu.psu.psu_conf import PSUConf
except ImportError:
    from scs_core.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    psu_version = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdConfiguration()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('configuration', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        logger.error('SystemID not available.')
        exit(1)

    logger.info(system_id)

    # PSU...
    interface_conf = InterfaceConf.load(Host)
    interface_model = None if interface_conf is None else interface_conf.model

    psu_conf = None if interface_model is None else PSUConf.load(Host)
    psu = None if psu_conf is None else psu_conf.psu(Host, interface_model)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if psu:
        try:
            psu.open()
            psu_version = psu.version()
        except LockTimeout:
            psu_version = PSUVersion.load(Host)         # a report will be present if psu_monitor is running
        except OSError:
            psu_version = None                          # PSU fault

    try:
        if cmd.save():
            conf = Configuration.construct_from_jstr(cmd.configuration)

            if conf is None:
                logger.error('invalid configuration: %s' % cmd.configuration)
                exit(2)

            try:
                conf.save(Host)
            except ValueError as ex:
                logger.error(repr(ex))
                exit(1)

        configuration = Configuration.load(Host, psu_version=psu_version, exclude_sim=cmd.exclude_sim)
        sample = ConfigurationSample(system_id.message_tag(), LocalizedDatetime.now().utc(), configuration)

        if cmd.table:
            for row in sample.as_table():
                print(row)

        elif cmd.indent is not None:
            print(JSONify.dumps(sample, indent=cmd.indent))

        else:
            print(JSONify.dumps(sample, separators=(',', ':')))         # maximum compactness

    finally:
        if psu:
            psu.close()
