#!/usr/bin/env python3

"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_group_setup utility is designed to automate the creation of AWS Greengrass groups using South
Coast Science's configuration

The group must already exist and the ML lambdas must be associated with the greengrass account for which the IAM auth
keys are given

SYNOPSIS
aws_group_setup.py [{  [-c] | [-s] } [-m] [-a AWS_Group_Name]] [-v]

EXAMPLES
./aws_group_setup.py -s -a scs-test-001-group -m

FILES
A conf file is placed in a default directory referencing the group name and when it was created

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html
"""

import boto3
import socket
import sys

from botocore.exceptions import ClientError

from getpass import getpass

from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.aws_group_configurator import AWSGroupConfigurator
from scs_core.aws.greengrass.gg_errors import ProjectMissingError

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_group_setup import CmdAWSGroupSetup


# --------------------------------------------------------------------------------------------------------------------

def create_aws_client():
    access_key_secret = ""
    access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
    if access_key_id:
        access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

    if access_key_id and access_key_secret:
        client = boto3.client(
            'greengrass',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        client = boto3.client('greengrass', region_name=aws_region)

    return client


def return_group_name():
    host_name = socket.gethostname()
    return host_name + "-group"


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSGroupSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    aws_group_name = cmd.aws_group_name if cmd.aws_group_name else return_group_name()
    aws_region = "us-west-2"

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # ClientAuth...
    awsGroupConf = AWSGroupConfigurator.load(Host)

    if cmd.set:
        if awsGroupConf:
            user_choice = input("Group configuration already exists. Type Yes to update: ")
            print("")
            if not user_choice.lower() == "yes":
                print("Operation cancelled")
                exit()
        try:
            aws_configurator = AWSGroupConfigurator(aws_group_name, create_aws_client(), cmd.use_ml)

            aws_configurator.collect_information(Host)
            aws_configurator.define_aws_group_resources(Host)
            aws_configurator.define_aws_group_functions()
            aws_configurator.define_aws_group_subscriptions()
            aws_configurator.define_aws_logger()
            aws_configurator.create_aws_group_definition()
            aws_configurator.save(Host)

        except ClientError as error:
            if error.response['Error']['Code'] == 'BadRequestException':
                print("aws_group_setup: Invalid request.", file=sys.stderr)
            if error.response['Error']['Code'] == 'InternalServerErrorException':
                print("aws_group_setup: AWS server error.", file=sys.stderr)

        except ProjectMissingError:
            print("aws_group_setup: Project configuration not set.", file=sys.stderr)

    if cmd.show_current:

        try:
            aws_group_info = AWSGroup(aws_group_name, create_aws_client())

            aws_group_info.get_group_info_from_name()
            aws_group_info.get_group_arns()
            aws_group_info.output_current_info()

            if cmd.indent:
                print(JSONify.dumps(aws_group_info, indent=cmd.indent))
            else:
                print(JSONify.dumps(aws_group_info))

        except KeyError:
            print("Group may not have been configured", file=sys.stderr)


