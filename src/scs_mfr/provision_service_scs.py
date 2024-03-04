#!/usr/bin/env python3

"""
Created on 9 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The provision_service_scs utility is used to upgrade a device, together with its AWS Greengrass presence. This
utility should be run as the scs user, the provision_new_root utility should be run simultaneously as the root user.

The project location ID may be an integer or an alphanumeric string. Alternatively, the location may be the underscore
character "_", indicating that the project location ID should be set as the device serial number.

The provision_service_scs utility should only be used for servicing / update tasks. New devices should be
configured using the provision_service_scs utility.

SYNOPSIS
provision_service_scs.py [-p ORG GROUP LOCATION [-f]] [-u] [-s] [{ -a AFE | -d DSI DATE }] [-c] [-b]
[-m MODEL_MAP] [-t TIMEZONE] [-v]

EXAMPLES
./provision_service_scs.py -v -a 26-000345 -b

SEE ALSO
scs_mfr/provision_new_root
scs_mfr/provision_new_scs
"""

import sys

from scs_core.client.http_exception import HTTPNotFoundException

from scs_core.data.datetime import Date

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.dsi_calib import DSICalib

from scs_core.location.timezone import Timezone

from scs_core.model.model_map import ModelMap

from scs_core.sys.logging import Logging

from scs_mfr.cmd.cmd_provision_service_scs import CmdProvisionServiceSCS
from scs_mfr.provision.provision_scs import ProvisionSCS


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdProvisionServiceSCS()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('provision_service_scs', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    provision = ProvisionSCS(model_map=cmd.model_map, verbose=cmd.verbose)
    logger.info(provision)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

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

        if cmd.barometric:
            provision.include_pressure()

        if cmd.set_gases():
            provision.include_gases(cmd.afe_serial, cmd.dsi_serial, cmd.dsi_calibration_date, cmd.scd30)

        provision.update_models(cmd.electrochems_are_being_set())

        if cmd.timezone:
            provision.timezone(cmd.timezone)

        if cmd.project:
            provision.aws_project(cmd.project_org, cmd.project_group, cmd.project_location, cmd.force)

        provision.clear_opc_errors()
        provision.set_schedule()

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
