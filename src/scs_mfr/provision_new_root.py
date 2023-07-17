#!/usr/bin/env python3

"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The provision_new_root utility is used to

SYNOPSIS
provision_new_root.py [-v]

EXAMPLES
provision_new_root -v

SEE ALSO
scs_mfr/provision_new_scs
"""

import os
import sys

from scs_core.sys.logging import Logging

from scs_host.sync.flag import Flag

from scs_mfr.cmd.cmd_provision_new_root import CmdProvisionNewRoot
from scs_mfr.provision.provision_root import ProvisionRoot


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdProvisionNewRoot()

    # logging...
    Logging.config('provision_new_root', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    if os.getcwd() != '/etc/systemd/system':
        logger.error("must be run in /etc/systemd/system.")

    if os.geteuid() != 0:
        logger.error("you must have root privileges to set the identity.")
        exit(1)

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    provision = ProvisionRoot(cmd.verbose)

    scs_configuration_completed = Flag('scs-configuration-completed')
    root_setup_completed = Flag('root-setup-completed')

    try:
        # ------------------------------------------------------------------------------------------------------------
        # stage 1...

        logger.info("stage 1...")

        provision.prepare()


        # ------------------------------------------------------------------------------------------------------------
        # stage 2...

        scs_configuration_completed.wait_for_raised()

        logger.info("stage 2...")

        provision.setup()

        root_setup_completed.raise_flag()


        # ----------------------------------------------------------------------------------------------------------------
        # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        scs_configuration_completed.lower_flag()
