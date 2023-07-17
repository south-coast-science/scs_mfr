#!/usr/bin/env python3

"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The provision_new_scs utility is used to

SYNOPSIS
provision_new_scs.py -i INVOICE -p ORG GROUP LOCATION [{ -a AFE | -d DSI DATE }] [-s] [-t] [-v]

EXAMPLES
./provision_new_scs.py -v -i INV-0000 -p south-coast-science-dev development 1 -a 26-000345

SEE ALSO
scs_mfr/provision_new_root
"""

import sys

from scs_core.sys.logging import Logging

from scs_host.sync.flag import Flag

from scs_mfr.cmd.cmd_provision_new_scs import CmdProvisionNewSCS
from scs_mfr.provision.provision_scs import ProvisionSCS


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

    provision = ProvisionSCS(cmd.verbose)

    scs_configuration_completed = Flag('scs-configuration-completed')
    root_setup_completed = Flag('root-setup-completed')

    try:
        # ------------------------------------------------------------------------------------------------------------
        # stage 1...

        logger.info("stage 1...")

        provision.upgrade()

        if cmd.has_gases():
            provision.include_gases(cmd.afe_serial, cmd.dsi_serial, cmd.dsi_calibration_date, cmd.scd30)
        else:
            provision.remove_gases()

        if cmd.timezone:
            provision.timezone(cmd.timezone)

        provision.system_id(cmd.invoice_number)
        provision.aws_project(cmd.project_org, cmd.project_group, cmd.project_location)

        scs_configuration_completed.raise_flag()


        # ------------------------------------------------------------------------------------------------------------
        # stage 2...

        root_setup_completed.wait_for_raised()

        logger.info("stage 2...")

        provision.aws_deployment()
        provision.test()


    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        root_setup_completed.lower_flag()
