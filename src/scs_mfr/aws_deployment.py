#!/usr/bin/env python3

"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The aws_deployment utility is used to invoke a deployment by the AWS cloud to the device. The deployment
configuration should already be in place - see aws_identity.py and aws_group_setup.py.

The greengrass service must be running for the deployment to complete.

SYNOPSIS
aws_deployment.py [-w] [-i INDENT] [-v]

EXAMPLES
./aws_deployment.py -vw

DOCUMENT EXAMPLE - OUTPUT
{"ResponseMetadata": {"RequestId": "72fce673", "HTTPStatusCode": 200,
"HTTPHeaders": {"date": "Fri, 15 Jan 2021 11:50:15 GMT", "content-type": "application/json", "content-length": "220",
"connection": "keep-alive", "x-amzn": "72fce673", "x-amzn-greengrass-trace-id": "Root=1-60018176",
"x-amz-id": "ZMEqkE=", "x-amzn-trace-id": "Root=1-60018176"}, "RetryAttempts": 0},
"DeploymentArn": "arn:aws:greengrass:us-west-2:696437392763:/greengrass/groups//deployments/cb645f98-7737",
"DeploymentId": "cb645f98-7737"}

SEE ALSO
scs_mfr/aws_group_setup.py
scs_mfr/aws_identity.py
"""

import sys
import time

from botocore.exceptions import ClientError, NoCredentialsError

from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_deployer import AWSGroupDeployer

from scs_core.aws.security.access_key_manager import AccessKeyManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_deployment import CmdAWSDeployment


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSDeployment()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_deployment', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


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

    manager = AccessKeyManager()
    key = manager.get(auth.id_token)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    client = Client.construct('greengrass', key)

    # AWSGroupDeployer...
    deployer = AWSGroupDeployer(AWS.group_name(), client)
    logger.info(deployer)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        # run...
        try:
            response = deployer.deploy()
        except KeyError:
            logger.error("group may not have been configured.")
            exit(1)

        print(JSONify.dumps(response, indent=cmd.indent))

        # wait...
        while True:
            status = deployer.status(response)

            if status == AWSGroupDeployer.FAILURE:
                logger.error("deployment failed.")
                exit(1)

            logger.info(status)

            if not cmd.wait or status == AWSGroupDeployer.SUCCESS:
                break

            time.sleep(5.0)

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except ClientError as ex:
        logger.error(repr(ex))

    except (EOFError, NoCredentialsError):
        logger.error("credentials error.")
