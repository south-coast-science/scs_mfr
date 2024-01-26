#!/usr/bin/env python3

"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The provision_new_scs utility is used to configure a device, together with its AWS Greengrass presence. This utility
should be run as the scs user, the provision_new_root utility should be run simultaneously as the root user.

The project location ID may be an integer or an alphanumeric string. Alternatively, the location may be the underscore
character "_", indicating that the project location ID should be set as the device serial number.

SYNOPSIS
provision_new_scs.py -i INVOICE -p ORG GROUP LOCATION [-f] [-u] [{ -a AFE | -d DSI DATE }] [-c] [-s PSU_MODEL]
[-m MODEL_MAP] [-t TIMEZONE] [-v]

EXAMPLES
./provision_new_scs.py -v -i INV-0000 -p south-coast-science-dev development _ -a 26-000345 -m OPCubeV1

SEE ALSO
scs_mfr/provision_new_root
scs_mfr/provision_service_scs
"""

import sys

from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator

from scs_core.client.http_exception import HTTPNotFoundException

from scs_core.data.datetime import Date

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.dsi_calib import DSICalib

from scs_core.location.timezone import Timezone

from scs_core.model.model_map import ModelMap

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_provision_new_scs import CmdProvisionNewSCS
from scs_mfr.provision.provision_scs import ProvisionSCS


# TODO: re-provisioning did not add gas lambda - is there an ordering problem?
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdProvisionNewSCS()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('provision_new_scs', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    provision = ProvisionSCS(model_map=cmd.model_map, verbose=cmd.verbose)
    logger.info(provision)

    creator = CognitoDeviceCreator()


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    system_id = SystemID.load(Host)

    system_id.system_serial_number = Host.numeric_component_of_name()
    tag = system_id.message_tag()

    if not creator.may_create(tag):
        logger.error("device tag '%s' is not whitelisted." % tag)
        exit(1)

    if not CognitoDeviceIdentity.is_valid_invoice_number(cmd.invoice_number):
        logger.error("invalid invoice number: '%s'." % cmd.invoice_number)
        exit(2)

    try:
        if cmd.afe_serial is not None:
            AFECalib.download(cmd.afe_serial, parse=False)
    except HTTPNotFoundException:
        logger.error("unrecognised AFE serial number: '%s'." % cmd.afe_serial)
        exit(2)

    try:
        if cmd.dsi_serial is not None:
            DSICalib.download(cmd.dsi_serial, parse=False)
    except HTTPNotFoundException:
        logger.error("unrecognised DSI serial number: '%s'." % cmd.dsi_serial)
        exit(2)

    if cmd.dsi_calibration_date is not None and not Date.is_valid_iso_format(cmd.dsi_calibration_date):
        logger.error("invalid ISO date: '%s'." % cmd.dsi_calibration_date)
        exit(2)

    if cmd.model_map is not None and cmd.model_map not in ModelMap.names():
        logger.error("model map '%s' cannot be found." % cmd.model_map)
        exit(2)

    if cmd.timezone is not None and not Timezone.is_valid(cmd.timezone):
        logger.error("unrecognised timezone: '%s'." % cmd.timezone)
        exit(2)


    try:
        # ------------------------------------------------------------------------------------------------------------
        # Check...

        logger.info("Check...")

        provision.os_check()


        # ------------------------------------------------------------------------------------------------------------
        # Stage 1...

        logger.info("Stage 1...")

        if cmd.upgrade_pips:
            provision.upgrade_pips()

        provision.include_pressure()

        if cmd.has_gases():
            provision.include_gases(cmd.afe_serial, cmd.dsi_serial, cmd.dsi_calibration_date, cmd.scd30)
        else:
            provision.remove_gases()

        provision.update_models(cmd.electrochems_are_being_set())

        if cmd.psu_model:
            provision.psu_model(cmd.psu_model)

        if cmd.timezone:
            provision.timezone(cmd.timezone)

        provision.system_id()
        provision.cognito_identity(cmd.invoice_number)
        provision.aws_project(cmd.project_org, cmd.project_group, cmd.project_location, cmd.force)

        provision.raise_scs_configuration_completed()


        # ------------------------------------------------------------------------------------------------------------
        # Stage 2...

        provision.wait_for_root_setup_completed()
        provision.lower_root_setup_completed()

        logger.info("Stage 2...")

        provision.aws_deployment()

        provision.test()


        # ----------------------------------------------------------------------------------------------------------------
        # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)
