#!/usr/bin/env python3

"""
Created on 09 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The aws_identity script allows the user to change the identity of an already-configured greengrass install,
in our use case it is to change the greengrass identity of a device which was set up using a cloned
base image without having to reinstall the greengrass software

The script could also be used to set up a "blank" greengrass install, which does not already have an identity, but
does already have the greengrass software.

If no group name is provided, the host name will be read from the device.
If no core name is provided, the host name will be read from the device.

SYNOPSIS
aws_identity.py [-s [-g GROUP_NAME] [-c CORE_NAME]] [-i INDENT] [-v]

EXAMPLES
./aws_identity.py -s -g scs-test-003-group -c scs-test-003-core -v

DOCUMENT EXAMPLE
{"core-name": "scs-cube-001-core", "group-name": "scs-cube-001-group"}

SEE ALSO
scs_mfr/aws_deployment
scs_mfr/aws_group_setup

RESOURCES
Created with reference to amazon's own device setup script (URL may change if updated)
https://d1onfpft10uf5o.cloudfront.net/greengrass-device-setup/downloads/gg-device-setup-latest.sh
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html

NOTES
ATS_ROOT_CA_RSA_2048_REMOTE_LOCATION in core.aws.greengrass aws_identity is a certificate provided by
amazon itself and may be subject to change e.g. via obsolescence - check here:
https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html
"""

import os
import sys

from botocore.exceptions import NoCredentialsError, ClientError

from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_identity import AWSIdentity

from scs_core.aws.security.access_key_manager import AccessKeyManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_identity import CmdAWSIdentity


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    key = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSIdentity()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_identity', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    if cmd.setup and os.geteuid() != 0:
        logger.error("you must have root privileges to set the identity.")
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # authentication...

    if cmd.setup:
        # credentials...
        credentials = CognitoDeviceCredentials.load_credentials_for_device(Host)

        # AccessKey...
        gatekeeper = CognitoLoginManager()
        auth = gatekeeper.device_login(credentials)

        if not auth.is_ok():
            logger.error(auth.authentication_status.description)
            exit(1)

        manager = AccessKeyManager()
        key = manager.get(auth.id_token)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.setup:
            iot_client = Client.construct('iot', key)
            gg_client = Client.construct('greengrass', key)

            identity = AWSIdentity(iot_client, gg_client, AWS.core_name(), AWS.group_name())
            identity.setup_device()
            identity.save(Host)

        else:
            identity = AWSIdentity.load(Host)

        if identity:
            print(JSONify.dumps(identity, indent=cmd.indent))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except ClientError as error:
        if error.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            logger.error("the resources for this group already exist.")
        else:
            raise error

    except (EOFError, NoCredentialsError):
        logger.error("credentials error.")
