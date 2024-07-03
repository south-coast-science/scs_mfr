#!/usr/bin/env python3

"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration
from scs_core.psu.psu_version import PSUVersion

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.lock.lock_timeout import LockTimeout
from scs_host.sys.host import Host

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

conf = '''
    {
        "hostname": "scs-cube-001",
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "1.4.18"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "2.1.6"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "2.1.3"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.3.1"
            },
            "scs_host": {
                "repo": "scs_host_cpc",
                "version": "1.0.12"
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.4.8"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.1.4"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2022-11-16T15:14:30Z",
                "offset": 272,
                "env": {
                    "rec": "2022-11-15T21:40:00Z",
                    "hmd": 58.9,
                    "tmp": 20.6
                }
            },
            "sn2": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            },
            "sn3": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            },
            "sn4": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            }
        },
        "afe-id": {
            "serial_number": null,
            "type": "DSI",
            "calibrated_on": "2022-01-01",
            "sn1": {
                "serial_number": "212060325",
                "sensor_type": "NO2A43F"
            }
        },
        "aws-group-config": {
            "group-name": "scs-cube-001-group",
            "time-initiated": "2022-11-15T13:20:17Z",
            "unix-group": 984,
            "ml": "oE.1"
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/cube/loc/1",
            "device-path": "south-coast-science-dev/cube/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "available": true,
            "on-root": false
        },
        "display-conf": null,
        "vcal-baseline": {
            "NO2": {
                "calibrated-on": "2022-11-16T15:04:46Z",
                "offset": 206,
                "env": null
            }
        },
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "oE.1"
        },
        "gps-conf": null,
        "interface-conf": {
            "model": "OPCubeT1"
        },
        "greengrass-identity": null,
        "mpl115a2-calib": null,
        "mqtt-conf": null,
        "ndir-conf": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177336702",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": null,
        "psu-conf": {
            "model": "OPCubeV1",
            "batt-model": "PackV2",
            "ignore-threshold": false,
            "reporting-interval": 10,
            "report-file": "/dev/shm/southcoastscience/psu_status_report.json"
        },
        "psu-version": {
            "id": "SCS OPCube Controller type 1 firmware 1",
            "tag": "001.001.003",
            "c-date": null,
            "c-time": null
        },
        "pt1000-calib": null,
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
        "shared-secret": {
            "key": "IuIIGqwQWX5c7Z0Z"
        },
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "networks": {
            "eth0": {
                "kind": "ethernet",
                "state": "connected",
                "connection": "Ethernet eth0"
            },
            "cdc-wdm0": {
                "kind": "gsm",
                "state": "unavailable",
                "connection": null
            }
        },
        "modem": {
            "id": "3f07553c31ce11715037ac16c24a0b",
            "imei": null,
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC216A01M4G"
        },
        "sim": null,
        "system-id": {
            "set-on": "2022-11-15T13:17:28Z",
            "vendor-id": "SCS",
            "model-id": "OPC",
            "model": "Praxis/OPCube",
            "config": "v1",
            "system-sn": 1
        },
        "timezone-conf": {
            "set-on": "2022-11-15T13:46:10Z",
            "name": "Europe/London"
        }
    }
'''

# --------------------------------------------------------------------------------------------------------------------
# resources...

psu_version = None

interface_conf = InterfaceConf.load(Host)
interface_model = None if interface_conf is None else interface_conf.model

psu_conf = None if interface_model is None else PSUConf.load(Host)
psu = None if psu_conf is None else psu_conf.psu(Host, interface_model)

if psu:
    try:
        psu.open()
        psu_version = psu.version()
    except LockTimeout:
        psu_version = PSUVersion.load(Host)

# --------------------------------------------------------------------------------------------------------------------
# run...

conf1 = Configuration.load(Host, psu_version=psu_version)
print(conf1)
print("-")

# conf1.save(Host)
# conf1 = Configuration.load(Host, psu=psu)
# print(conf1)
# print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("===")

conf2 = Configuration.construct_from_jdict(json.loads(jstr))
print(conf2)
print("-")

jstr = JSONify.dumps(conf1, indent=4)

print(jstr)
print("-")

equals = conf1 == conf2

print("equals: %s" % equals)
