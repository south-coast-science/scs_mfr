#!/usr/bin/env python3

"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The provision_new_root utility is used to provide device and AWS Greengrass configuration tasks that require
superuser privileges. This utility should be run as the root user, the provision_new_scs utility should be run
simultaneously as the scs user.

The provision_new_root utility is used for both new devices and servicing / update tasks.

WARNING: do not use the --prep-sd  / -s flag when doing a service or upgrade.

SYNOPSIS
provision_new_root.py [-s] [-x] [-v]

EXAMPLES
provision_new_root -sv

SEE ALSO
scs_mfr/provision_new_scs
scs_mfr/provision_service_scs
"""

import os
import sys

from scs_core.sys.logging import Logging

from scs_mfr.cmd.cmd_provision_new_root import CmdProvisionNewRoot
from scs_mfr.provision.provision_root import ProvisionRoot


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdProvisionNewRoot()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('provision_new_root', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    logger.info("Validation...")

    if os.getcwd() != '/etc/systemd/system':
        logger.error("must be run in /etc/systemd/system.")
        exit(1)

    if os.geteuid() != 0:
        logger.error("you must have root privileges to set the identity.")
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    provision = ProvisionRoot(verbose=cmd.verbose)
    logger.info(provision)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # Check...

        logger.info("Check...")

        if not cmd.exclude_test:
            provision.os_check()
            provision.kernel_check()

        provision.greengrass_check()


        # ------------------------------------------------------------------------------------------------------------
        # Stage 1...

        logger.info("Stage 1...")

        provision.stop()

        if cmd.prep_sd:
            provision.prep_sd()


        # ------------------------------------------------------------------------------------------------------------
        # Stage 2...

        provision.wait_for_scs_configuration_completed()

        logger.info("Stage 2...")

        provision.identity()            # TODO: not for service version
        provision.setup()

        provision.raise_root_setup_completed()


        # ------------------------------------------------------------------------------------------------------------
        # Stage 3...

        provision.wait_for_scs_deployment_completed()

        logger.info("Stage 3...")

        provision.set_greengrass_log_level(cmd.log_level)


        # ----------------------------------------------------------------------------------------------------------------
        # end...

        provision.lower_scs_configuration_completed()
        provision.lower_scs_deployment_completed()

    except KeyboardInterrupt:
        print(file=sys.stderr)
