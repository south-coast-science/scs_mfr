#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The system_id utility is used to specify the identity of a sensing device, as it appears on either the South Coast
Science / AWS or OpenSensors.io Community Edition messaging infrastructures.

The identity is also used to tag all environmental sensing records. It is therefore important that a device retains
a fixed identity throughout its lifetime.

When the "verbose" "-v" flag is used, the system_id utility reports all the identity formats derived from
its specification.

SYNOPSIS
system_id.py [-d VENDOR_ID] [-g MODEL_GROUP] [-i MODEL_ID] [-c CONFIG] [{-s SYSTEM_SERIAL_NUMBER | -a }] [-v]

EXAMPLES
./system_id.py -v -d SCS -g Praxis -i BGX -c BGX -s 401

DOCUMENT EXAMPLE
{"set-on": "2024-01-09T16:02:09Z",
"vendor-id": "SCS", "model": "Alpha BB Eng", "model-id": "BE2", "config": "V2", "system-sn": 3}

FILES
~/SCS/conf/system_id.json

SEE ALSO
scs_dev/aws_topic_publisher
scs_dev/aws_topic_subscriber
scs_dev/climate_sampler
scs_dev/gases_sampler
scs_dev/particulates_sampler
scs_dev/status_sampler
scs_dev/control_receiver
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_system_id import CmdSystemID


# TODO: update documentation
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    serial_number = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSystemID()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("system_id: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # check for existing document...
    system_id = SystemID.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if system_id is None and not cmd.is_complete():
            print("system_id: No ID is present - you must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.auto_serial:
            try:
                serial_number = Host.numeric_component_of_name()
            except ValueError as ex:
                print("system_id: hostname '%s' cannot provide a serial number." % ex, file=sys.stderr)
                exit(1)
        else:
            serial_number = system_id.system_serial_number if cmd.serial_number is None else cmd.serial_number

        vendor_id = system_id.vendor_id if cmd.vendor_id is None else cmd.vendor_id
        model_group = system_id.model_group if cmd.model_group is None else cmd.model_group
        model_id = system_id.model_id if cmd.model_id is None else cmd.model_id
        configuration = system_id.configuration if cmd.configuration is None else cmd.configuration

        system_id = SystemID(vendor_id, model_group, model_id, configuration, serial_number)
        system_id.save(Host)

        system_id = SystemID.load(Host)     # update last_modified

    if system_id:
        print(JSONify.dumps(system_id))

    if cmd.verbose:
        print("-", file=sys.stderr)
        print("box:   %s" % system_id.box_label(), file=sys.stderr)
        print("topic: %s" % system_id.topic_label(), file=sys.stderr)
        print("tag:   %s" % system_id.message_tag(), file=sys.stderr)
