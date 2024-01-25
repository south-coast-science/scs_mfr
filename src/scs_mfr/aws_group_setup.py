#!/usr/bin/env python3

"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The aws_group_setup utility is designed to automate the creation of AWS Greengrass groups using South
Coast Science's configurations.

Note that the template name for the AWS group is specified by the group name as set by the gas_model_conf utility.

When setting the group, the group must already exist and the ML lambdas must be associated with the greengrass
account for which the IAM auth keys are given.

If neither --retrieve or --set flags are used, the aws_group_setup utility reports the group summary as stored on
the device, if it exists.

SYNOPSIS
aws_group_setup.py [{ -r | -s [-a AWS_GROUP_NAME] [-f] }] [-i INDENT] [-v]

EXAMPLES
./aws_group_setup.py -s oE.1 -a scs-test-001-group -f

EXAMPLE DOCUMENT - SHORTFORM (LOCAL)
{"group-name": "scs-cube-001-group", "time-initiated": "2022-04-07T13:26:59Z", "unix-group": 984, "ml": "oE.1"}

FILES
~/SCS/aws/aws_group_config.json

SEE ALSO
scs_mfr/aws_deployment
scs_mfr/aws_identity
scs_mfr/gas_model_conf
scs_mfr/pmx_model_conf

RESOURCES
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html
"""

import os
import sys

from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError

from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.aws.greengrass.gg_errors import ProjectMissingError

from scs_core.aws.security.access_key_manager import AccessKeyManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.model.model_conf import ModelConf
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_group_setup import CmdAWSGroupSetup


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    client = None
    gg_ml_template = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSGroupSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_group_setup', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    if cmd.set:
        if os.geteuid() != 0:
            logger.error("you must have root privileges to set up the group.")
            exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # model conf...

    if cmd.set:
        gas_model_conf = GasModelConf.load(Host)
        pmx_model_conf = PMxModelConf.load(Host)

        try:
            gg_ml_template = ModelConf.gg_ml_template(gas_model_conf, pmx_model_conf)

        except ValueError as ex:
            logger.error(ex)
            exit(1)

        logger.info("gg_ml_template: %s" % gg_ml_template)


    # ----------------------------------------------------------------------------------------------------------------
    # authentication...

    # AWSGroupConfiguration...
    conf = AWSGroupConfiguration.load(Host)

    if cmd.requires_aws_client():
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

        # client...
        client = Client.construct('greengrass', key)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.set:
            if conf and not cmd.force:
                user_choice = input("Group configuration already exists. Type Yes to overwrite: ")
                if not user_choice.lower() == "yes":
                    exit(0)

            try:
                now = LocalizedDatetime.now()
                conf = AWSGroupConfiguration(AWS.group_name(), now, ml=gg_ml_template)
                configurator = conf.configurator(client)

                configurator.collect_information(Host)
                configurator.define_aws_group_resources(Host)
                configurator.define_aws_group_functions()
                configurator.define_aws_group_subscriptions()
                # configurator.define_aws_logger()
                configurator.create_aws_group_definition()

                conf.save(Host)

                print(JSONify.dumps(conf, indent=cmd.indent))

            except ClientError as error:
                if error.response['Error']['Code'] == 'BadRequestException':
                    logger.error("Invalid request.")

                if error.response['Error']['Code'] == 'InternalServerErrorException':
                    logger.error("AWS server error.")

            except ProjectMissingError:
                logger.error("Project configuration not set.")

        elif cmd.retrieve:
            try:
                aws_group_info = AWSGroup(AWS.group_name(), client)

                aws_group_info.get_group_info_from_name()
                aws_group_info.get_group_arns()
                aws_group_info.output_current_info()

                print(JSONify.dumps(aws_group_info, indent=cmd.indent))

            except KeyError:
                logger.error("group may not have been configured.")

        else:
            if conf:
                print(JSONify.dumps(conf, indent=cmd.indent))


    except KeyboardInterrupt:
        print(file=sys.stderr)

    except (EOFError, NoCredentialsError):
        logger.error("credentials error.")

    except EndpointConnectionError as ex:
        logger.error(repr(ex))
