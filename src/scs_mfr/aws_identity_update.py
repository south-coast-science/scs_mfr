#!/usr/bin/env python3

"""
Created on 5 Jul 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
Experimental - this may be impossible with Greengrass v1.

SYNOPSIS
aws_identity_update.py [-s [-g GROUP_NAME] [-c CORE_NAME]] [-i INDENT] [-v]

EXAMPLES
./aws_identity_update.py -s -g scs-test-003-group -c scs-test-003-core -v

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
"""

import os
import sys

from botocore.exceptions import NoCredentialsError, ClientError

from scs_core.aws.client.client import Client
from scs_core.aws.greengrass.v1.aws_group_version import AWSGroupVersion
from scs_core.aws.greengrass.v1.aws_identity_update import AWSIdentityUpdate

from scs_core.aws.security.access_key_manager import AccessKeyManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_identity_update import CmdAWSIdentityUpdate


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSIdentityUpdate()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_identity_update', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    if os.geteuid() != 0:
        logger.error("you must have root privileges to update the identity.")
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # authentication...

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
    # resources...

    group_version = AWSGroupVersion.load(Host)

    iot_client = Client.construct('iot', key)
    gg_client = Client.construct('greengrass', key)

    identity = AWSIdentityUpdate(iot_client, gg_client, group_version)
    logger.info(identity)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        group_arn = identity.update_device()
        logger.info("group_arn: %s" % group_arn)

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except ClientError as error:
        if error.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            logger.error("the resources for this group already exist.")
        else:
            raise error

    except (EOFError, NoCredentialsError):
        logger.error("credentials error.")
