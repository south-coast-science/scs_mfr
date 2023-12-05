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

The specified location path set is tested to check whether it is in use by another device. If so, the utility
terminated. The validation can be circumvented with the --force flag.

When the "verbose" "-v" flag is used, the aws_project utility reports all the topic paths derived from
its specification.

Note that the sampling process must be restarted for changes to take effect.

SYNOPSIS
aws_project.py [-s ORG GROUP LOCATION [-f]] [-d] [-v]

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

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager
from scs_core.aws.security.organisation_manager import DeviceOrganisationManager

from scs_core.client.http_exception import HTTPException

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_project import CmdAWSProject


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSProject()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_project', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # authentication...

        # credentials...
        credentials = CognitoDeviceCredentials.load_credentials_for_device(Host)

        # AccessKey...
        gatekeeper = CognitoLoginManager()
        auth = gatekeeper.device_login(credentials)

        if not auth.is_ok():
            logger.error(auth.authentication_status.description)
            exit(1)


        # ----------------------------------------------------------------------------------------------------------------
        # resources...

        # SystemID...
        system_id = SystemID.load(Host)

        if system_id is None:
            logger.error("SystemID not available.")
            exit(1)

        logger.info(system_id)

        # DeviceOrganisation...
        manager = DeviceOrganisationManager()

        # Project...
        project = Project.load(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.set():
            location = system_id.system_serial_number if cmd.location == '_' else cmd.location

            project = Project.construct(cmd.organisation, cmd.group, location)
            location_path = project.location_path + '/'

            if not cmd.force and manager.location_path_in_use(auth.id_token, location_path):
                logger.error("The location path '%s' is in use." % location_path)
                exit(1)

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

    except HTTPException as ex:
        logger.error(ex.error_report)
        exit(1)

    except Exception as ex:
        logger.error(ex.__class__.__name__)
        exit(1)

