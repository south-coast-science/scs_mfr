#!/usr/bin/env python3

"""
Created on 3 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The aws_project utility is used to specify the topic path names for devices using the South Coast Science / AWS IoT
messaging infrastructure. For each device, topics are divided into two groups:

Location path, e.g.:

* south-coast-science-dev/development/loc/1/climate
* south-coast-science-dev/development/loc/1/gases
* south-coast-science-dev/development/loc/1/particulates

Device path, e.g.:

* south-coast-science-dev/development/device/alpha-pi-eng-000006/control
* south-coast-science-dev/development/device/alpha-pi-eng-000006/status

Typically, the device paths should remain fixed throughout the lifetime of the device. In contrast, a given set of
location paths are used by the device only when it is installed at a given location.

The location ID may be an integer or an alphanumeric string. Alternatively, the location may be the underscore
character "_", indicating that the location ID should be set as the device serial number.

When the "verbose" "-v" flag is used, the aws_project utility reports all the topic paths derived from
its specification.

Note that the scs_mfr/aws_mqtt_client process must be restarted for changes to take effect.

SYNOPSIS
aws_project.py [-s ORG GROUP LOCATION] [-d] [-v]

EXAMPLES
./aws_project.py -s south-coast-science-dev development 1

DOCUMENT EXAMPLE
{"location-path": "south-coast-science-dev/development/loc/1",
"device-path": "south-coast-science-dev/development/device"}

FILES
~/SCS/aws/aws_project.json

SEE ALSO
scs_dev/aws_mqtt_client
scs_mfr/aws_client_auth
"""

import sys

from scs_core.aws.config.project import Project

from scs_core.data.json import JSONify

from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_project import CmdAWSProject


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSProject()

    if cmd.verbose:
        print("aws_project: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ----------------------------------------------------------------------------------------------------------------
        # resources...

        # SystemID...
        if cmd.verbose:
            system_id = SystemID.load(Host)

            if system_id is None:
                print("aws_project: SystemID not available.", file=sys.stderr)
                exit(1)

            print("aws_project: %s" % system_id, file=sys.stderr)
        else:
            system_id = None


        # ClientAuth...
        project = Project.load(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.set():
            location = system_id.system_serial_number if cmd.location == '_' else cmd.location

            project = Project.construct(cmd.organisation, cmd.group, location)
            project.save(Host)

        if cmd.delete and project is not None:
            project.delete(Host)
            project = None

        if project:
            print(JSONify.dumps(project))

            if cmd.verbose:
                print("-")
                for channel in Project.CHANNELS:
                    print(project.channel_path(channel, system_id), file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

